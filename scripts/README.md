# Scripts e exemplos — Sentinela Proxmox (bônus)

Esses arquivos **não substituem** as [fases 0–10 do guia principal](../🛡️ Sentinela-Proxmox - Versão 1.0.md): são **atalhos** depois de entender o que cada passo faz — ideais na **segunda instalação**, revisão anual, ou para fechar o lab com confiança. **Antes de tudo:** se se perder no *repo*, leia o [manual de usabilidade](../docs/manual-usabilidade.md) (estágios A–E).

**Segurança:** nunca faça commit de `.env`, tokens Telegram, chaves privadas, nem dumps de `/etc/pve` com segredos.

---

## 1. `sentinela-health-check.sh` (host Proxmox)

Verificações **só-leitura**: NTP, serviço `ssh`, `sshd -T` (password/root), `pveversion`, disco `/`, ZFS (se existir), último backup `etc-pve-*.tar.gz` com `tar tzf`, CrowdSec + bouncer + `proxmox-firewall` se estiverem instalados, CTs 100/200 se existirem.

```bash
# No host (a partir da raiz do repositório clonado, ou copie o .sh para /root)
sudo bash scripts/sentinela-health-check.sh
sudo bash scripts/sentinela-health-check.sh --verbose
sudo bash scripts/sentinela-health-check.sh --json
```

- Saída **verde / amarelo / vermelho** no terminal (modo normal); com **`--json`** imprime **só** uma linha: `{"failures":N,"warnings":M,"ok":true|false}` — útil para **cron**, CI ou agendadores.
- Exit `0` se não houver falhas críticas; `1` se houver pelo menos uma falha `[XX]`.

---

## 2. `sentinela-telegram-monitor.py` (host Proxmox)

Alertas Telegram (RAM, disco, ZFS, CrowdSec digest, etc.). Instalação e variáveis de ambiente: [docs/monitoramento-telegram.md](../docs/monitoramento-telegram.md).

---

## 3. Systemd — backup diário de `/etc/pve` (alternativa ao cron)

Arquivos em [systemd/](systemd/) (sufixo `.example` — copie **sem** o sufixo para `/etc/systemd/system/`):

| Arquivo | Descrição |
|---------|-----------|
| [systemd/sentinela-etc-pve-backup.service.example](systemd/sentinela-etc-pve-backup.service.example) | Oneshot que chama `/usr/local/bin/backup-sentinela.sh` (script da Fase 10). |
| [systemd/sentinela-etc-pve-backup.timer.example](systemd/sentinela-etc-pve-backup.timer.example) | Dispara todos os dias às **03:00** (ajuste `OnCalendar` se precisar). |

```bash
sudo cp scripts/systemd/sentinela-etc-pve-backup.service.example /etc/systemd/system/sentinela-etc-pve-backup.service
sudo cp scripts/systemd/sentinela-etc-pve-backup.timer.example /etc/systemd/system/sentinela-etc-pve-backup.timer
sudo systemctl daemon-reload
sudo systemctl enable --now sentinela-etc-pve-backup.timer
systemctl list-timers | grep sentinela
```

---

## 4. PC pessoal — `sync-sentinela-backups.example.sh`

Em [pc/sync-sentinela-backups.example.sh](pc/sync-sentinela-backups.example.sh): `rsync` de `sentinela:/root/backups/` ou `SENTINELA_SSH=renato@IP ./sync-sentinela-backups.example.sh`. Ver **Fase 10 §10.4** do guia.

---

## Árvore resumida

Na **raiz** do repositório existe também um [Makefile](../Makefile) com `make check`, `make check-verbose` e `make check-json` (Linux/PVE ou WSL).

```
scripts/
├── README.md
├── sentinela-health-check.sh
├── sentinela-telegram-monitor.py
├── systemd/
│   ├── sentinela-etc-pve-backup.service.example
│   └── sentinela-etc-pve-backup.timer.example
└── pc/
    └── sync-sentinela-backups.example.sh
```
