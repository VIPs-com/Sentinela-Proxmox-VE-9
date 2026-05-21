# Monitoramento via Telegram — Sentinela Proxmox

> **Escopo:** documento de **operação** opcional; **não** substitui nem acrescenta fases ao [guia Sentinela](sentinela-proxmox-v1.0.md) (fases 0–10). Índice da pasta `docs/`: [README.md](README.md).

**Autor:** Renato (sysadmin)  
**Data:** Maio/2026  
**Hardware:** Mini PC · 16 GB RAM · Proxmox VE 9.x (Debian 13 Trixie)  
**Relacionado:** [sentinela-proxmox-v1.0.md](sentinela-proxmox-v1.0.md) (Fases 4–7: CrowdSec, firewall, rede)

**Objetivo:** receber no celular **alertas** sobre RAM, disco, estado de VMs/CTs, **mudanças em bloqueios CrowdSec**, **sinais de hardware** (temperatura, ZFS) e consultar **comandos** sob demanda — sem Prometheus/Grafana no homelab.

> **Filosofia:** stack mínima — `python3` + `python3-requests` (APT), um script no **host** PVE, Bot Telegram, `cron` para alertas periódicos e `systemd` opcional para *long polling*. **Não** versionar tokens nem arquivos `.env` com segredos no Git.

---

## Documentação oficial (leitura de apoio)

| Tema | Fonte |
|------|--------|
| `pvesh` (quem pode usar, formato JSON) | [pvesh(1) — Proxmox VE 9.x](https://pve.proxmox.com/pve-docs/pvesh.1.html) — o manual indica que **apenas root** pode invocar `pvesh` directamente. |
| API REST, tokens, ACL (alternativa futura sem root no script) | [Proxmox VE API](https://pve.proxmox.com/wiki/Proxmox_VE_API), [pveum(1)](https://pve.proxmox.com/pve-docs/pveum.1.html) |
| Telegram — envio e recepção de updates | [Bot API](https://core.telegram.org/bots/api) (`sendMessage`, `getUpdates`); [Bots FAQ](https://core.telegram.org/bots/faq) (*webhook* e *long polling* são mutuamente exclusivos) |
| Decisões / bloqueios CrowdSec | [cscli decisions list](https://docs.crowdsec.net/docs/cscli/cscli_decisions) |
| Credenciais no arranque | [systemd.exec(5)](https://www.freedesktop.org/software/systemd/man/latest/systemd.exec.html) — diretiva `EnvironmentFile=` |

---

## Visão geral da arquitetura

```text
Host Proxmox (root)
    │
    ├─ /opt/sentinela-monitor/estado.json   ← anti-spam + últimos valores (CrowdSec, VMs…)
    ├─ /etc/sentinela-monitor.env           ← TELEGRAM_* (chmod 600, fora do Git)
    │
    ├─ cron (root) → sentinela-telegram-monitor.py alertas
    │       ├─ RAM / disco / VMs caídas
    │       ├─ Opcional: digest CrowdSec (novos bans / contagem)
    │       └─ Opcional: thermal sysfs, ZFS health
    │
    └─ systemd (opcional) → … polling
            └─ comandos /status, /vms, … (só o seu chat_id)
                    │
                    └──► https://api.telegram.org  (HTTPS saída)
```

**Pré-requisitos no guia Sentinela:** concluir **Fase 0** (rede, NTP), **Fases 1–3** (SSH estável), idealmente **Fases 4–7** (CrowdSec + firewall). Garantir que o host pode sair para a Internet (regra **OUT** aceitar HTTPS se o seu `proxmox-firewall` for restritivo). Teste rápido:

```bash
curl -sS -o /dev/null -w "%{http_code}\n" https://api.telegram.org/
# Esperado: 200 ou 302 (não timeout / bloqueio)
```

---

## Fase 0 — Bot Telegram e Chat ID

### 0.1 Criar o bot (@BotFather)

1. No Telegram, fala com **@BotFather** → `/newbot`  
2. Guarda o **token** no Bitwarden (Apêndice G do guia principal).  
3. Envie uma mensagem ao seu bot.

### 0.2 Obter o Chat ID

Abre no browser (substitui o token):

`https://api.telegram.org/bot<TOKEN>/getUpdates`

No JSON, procura `"chat":{"id": NNN, ...}`. Esse **NNN** é o `TELEGRAM_CHAT_ID` (pode ser negativo em grupos).

---

## Fase 1 — Dependências no host PVE

```bash
sudo apt update
sudo apt install -y python3 python3-requests
python3 -c "import requests; print('requests OK')"
```

---

## Fase 2 — Instalar script a partir deste repositório

No seu PC (com o clone do repo) você pode copiar via `scp` para o PVE. O script versionado está em [scripts/sentinela-telegram-monitor.py](../scripts/sentinela-telegram-monitor.py). No **host** PVE:

```bash
sudo mkdir -p /opt/sentinela-monitor
sudo cp /caminho/para/clone/scripts/sentinela-telegram-monitor.py /opt/sentinela-monitor/
sudo chmod 700 /opt/sentinela-monitor/sentinela-telegram-monitor.py
sudo chown root:root /opt/sentinela-monitor/sentinela-telegram-monitor.py
```

> **Porque root:** o manual [pvesh(1)](https://pve.proxmox.com/pve-docs/pvesh.1.html) indica que só **root** pode usar `pvesh`. O script lista QEMU/LXC por essa via. Alternativa avançada: token API PVE + `curl` à REST API com ACL mínima — fora do escopo deste guia curto.

### 2.1 Arquivo de ambiente (segredos)

```bash
sudo install -m 600 /dev/null /etc/sentinela-monitor.env
sudo nano /etc/sentinela-monitor.env
```

Conteúdo mínimo:

```ini
TELEGRAM_TOKEN=123456789:AA...seu_token...
TELEGRAM_CHAT_ID=123456789
# Opcional — força o nó se o auto-detect falhar (nome em "Datacenter → Nó")
# PVE_NODE=pve
# Limites (percentagem inteira)
LIMITE_RAM_PORCENTO=80
LIMITE_DISCO_PORCENTO=80
# Digest de segurança / hardware (1=ligado, 0=desligado)
DIGEST_CROWDSEC=1
DIGEST_THERMAL=1
DIGEST_ZFS=1
# Temperatura máx. zona0 em miligrau Celsius (85°C)
THERMAL_MAX_MC=85000
```

```bash
sudo chmod 600 /etc/sentinela-monitor.env
sudo chown root:root /etc/sentinela-monitor.env
```

**Bitwarden:** duplica `TELEGRAM_TOKEN` e `TELEGRAM_CHAT_ID` na pasta Sentinela (Apêndice G).

### 2.2 Teste de envio

```bash
sudo set -a; source /etc/sentinela-monitor.env; set +a
sudo -E python3 /opt/sentinela-monitor/sentinela-telegram-monitor.py teste
```

Deves receber uma mensagem no Telegram.

---

## Fase 3 — Alertas periódicos (`cron`, usuário **root**)

O usuário `renato` **não** deve escrever em `/var/log/` por omissão. Usa **crontab de root** ou `/etc/cron.d/`.

Cria o log uma vez:

```bash
sudo touch /var/log/sentinela-monitor.log
sudo chown root:root /var/log/sentinela-monitor.log
sudo chmod 640 /var/log/sentinela-monitor.log
```

`sudo crontab -e` — exemplo (alertas a cada 5 minutos):

```cron
SHELL=/bin/bash
PATH=/usr/sbin:/usr/bin:/sbin:/bin

*/5 * * * * set -a; . /etc/sentinela-monitor.env; set +a; /usr/bin/python3 /opt/sentinela-monitor/sentinela-telegram-monitor.py alertas >> /var/log/sentinela-monitor.log 2>&1
```

Rotação simples semanal (truncar; em produção preferir `logrotate`):

```cron
30 3 * * 0 truncate -s 0 /var/log/sentinela-monitor.log 2>/dev/null || true
```

Teste manual:

```bash
sudo set -a; source /etc/sentinela-monitor.env; set +a
sudo -E python3 /opt/sentinela-monitor/sentinela-telegram-monitor.py alertas
```

---

## Fase 4 — Comandos em tempo real (systemd + polling)

O [Bot API](https://core.telegram.org/bots/api) permite `getUpdates` com *long polling*. **Não** uses *webhook* em paralelo (ver [FAQ](https://core.telegram.org/bots/faq)).

```bash
sudo nano /etc/systemd/system/sentinela-monitor.service
```

```ini
[Unit]
Description=Sentinela Proxmox — Telegram monitor (polling)
After=network-online.target crowdsec.service
Wants=network-online.target

[Service]
Type=simple
User=root
EnvironmentFile=/etc/sentinela-monitor.env
ExecStart=/usr/bin/python3 /opt/sentinela-monitor/sentinela-telegram-monitor.py polling
Restart=always
RestartSec=15

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now sentinela-monitor.service
sudo systemctl status sentinela-monitor.service --no-pager
```

No Telegram: `/start` ou `/ajuda` (só o `chat_id` configurado é aceite).

---

## O que o modo `alertas` cobre (sysadmin)

| Categoria | O que verifica | Notas |
|-----------|----------------|--------|
| **Recursos** | RAM (`/proc/meminfo`), disco `/` | Limites configuráveis; anti-spam até baixar do limite |
| **Guests** | QEMU + LXC via `pvesh` no **nome real do nó** | Detecta `running → stopped` e o inverso |
| **Segurança (CrowdSec)** | Contagem de decisões activas (`cscli decisions list`) | Alerta quando **aumenta** face ao último ciclo (novo ban / nova decisão). Detalhe: [cscli decisions](https://docs.crowdsec.net/docs/cscli/cscli_decisions) |
| **Hardware** | `thermal_zone*` (m°C), `zpool list` se ZFS existir | Temperatura é **aproximação** do que o kernel expõe; não substitui IPMI |
| **SMART** | Não automático no script base | Opcional: `smartctl -H /dev/nvme0` manual ou extensão futura — discos errados destroem contexto |

**Firewall / drops nft:** o script **não** parseia `nft` linha a linha (frágil entre versões). Para ver drops recentes do backend PVE, usa o que o guia Sentinela já documenta — por exemplo `journalctl` no serviço `proxmox-firewall` — e correlaciona com [wiki Firewall](https://pve.proxmox.com/wiki/Firewall). Podes acrescentar mais tarde um digest de `journalctl` com filtros **muito** específicos se precisar.

---

## Comandos Telegram (polling)

| Comando | Função |
|---------|--------|
| `/start`, `/ajuda` | Menu |
| `/status` | RAM, disco `/`, carga, versão PVE |
| `/vms` | Lista QEMU/LXC e estado |
| `/top` | Top 5 guests em execução por RAM (API) |
| `/seg` | Resumo CrowdSec (contagem + amostra) |
| `/hw` | Thermal + ZFS curto |

---

## Alternativa: métricas a partir de uma VM

- **Prós:** não corres código como root no host.  
- **Contras:** precisa de SSH com chave (ou API só leitura em outro endpoint), latência, e **não** pode usar `pvesh` localmente na VM — teria de usar a **API HTTPS** do PVE com token e ACL restrita ([wiki API](https://pve.proxmox.com/wiki/Proxmox_VE_API))).  
- Recomendação Sentinela: **primeiro** o caminho host+root deste documento; a VM como “painel” só quando dominar tokens ACL.

---

## Checklist final

```bash
sudo systemctl is-active sentinela-monitor.service   # se usares polling
sudo crontab -l | grep sentinela
sudo ls -l /opt/sentinela-monitor/estado.json
sudo tail -30 /var/log/sentinela-monitor.log
sudo pvesh get /nodes --output-format json | head -c 200
sudo cscli decisions list 2>/dev/null | head
```

---

## Troubleshooting

| Sintoma | Acção |
|---------|--------|
| `pvesh: error ... permission` ao rodar como `renato` | Esperado: use **root** ou API token + HTTPS. |
| Bot não responde | `systemctl status sentinela-monitor`; confirma `TELEGRAM_*`; `curl api.telegram.org`. |
| Lista de VMs vazia | Confirma `pvesh get /nodes` e o nome do nó; define `PVE_NODE=` no `.env`. |
| `cscli` falha no digest | CrowdSec não instalado ou PATH; define `DIGEST_CROWDSEC=0` temporariamente. |
| Muitas mensagens CrowdSec | Ajusta intervalo do `cron` ou desliga digest até calibrares listas/whitelists (guia Fase 4). |

---

## Evolução futura (não incluído no script base)

- Webhook atrás de reverse proxy com TLS.  
- Métricas por dataset ZFS (`zfs list -o name,used,avail`).  
- Integração com estado de `vzdump` / último backup.  
- Relatório diário agendado (`cron` + modo `relatorio` a implementar).

---

**Ver também:** índice de todos os scripts opcionais (health-check, systemd, sync no PC) em [../scripts/README.md](../scripts/README.md).

*Documento complementar ao repositório Sentinela Proxmox — operações e observabilidade leve.*
