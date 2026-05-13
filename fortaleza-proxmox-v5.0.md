# 🛡️ Fortaleza Proxmox — Guia Definitivo v5.0

**Autor:** Renato
**Data:** Maio/2026
**Hardware:** Mini PC · 16 GB RAM
**Base:** Proxmox VE 9.x (ex.: 9.1) sobre Debian 13 “Trixie”; kernel e OpenSSH variam com `apt full-upgrade` — confirme com `pveversion`, `uname -r`, `ssh -V`.
**Objetivo:** Construir uma infraestrutura **segura, invisível, documentada e recuperável** antes de começar a estudar.

> **Status da documentação:** guia de homelab **revisado contra fontes oficiais** em 2026-05-12. Não substitui suporte enterprise nem auditoria profissional. Matriz fase × fonte × conclusão: [docs/audit-matrix.md](docs/audit-matrix.md).

> **Perdido nos estudos?** Visão geral por setores (onboarding, blocos A–G, VM, GPG): [docs/mapa-do-curso.md](docs/mapa-do-curso.md).

---

## 📌 O que mudou em relação às versões anteriores

A v4.0 já cobria SSH, 2FA, CrowdSec, Tailscale, nftables e ShellHub. A v5.0 é uma reescrita completa — do zero ao servidor seguro, invisível e expandível:

### Fundação (fases obrigatórias — novato começa aqui)

| Adição na v5.0 | Por que é crítico |
|----------------|-------------------|
| **Fase -1:** ISO, pendrive, BIOS, ZFS vs LVM-Thin | Começa antes do PVE existir |
| **Configurar timezone + NTP** (Fase 0) | TOTP só funciona com relógio sincronizado. Erro silencioso. |
| **Trocar repositório Enterprise por No-Subscription** (Fase 0) | Sem isso, `apt update` falha com `401 Unauthorized` |
| **Configurar IP fixo** (Fase 0) | DHCP do roteador pode trocar o IP e você perde acesso |
| **Hostname + /etc/hosts coerente** (Fase 0) | Proxmox quebra se hostname não resolve |
| **Backup do `/etc/pve`** antes de cada fase | Seu seguro de vida |
| **Fase 10b:** vzdump + Proxmox Backup Server | Backups completos de VMs/CTs com deduplicação |
| **Fase VM-01:** VM Debian 13 de estudo + Cloud-Init + snapshot | Ambiente de lab descartável em < 1 min |

### Apêndices técnicos (referência pós-fases)

| Apêndice | Conteúdo novo na v5.0 |
|----------|-----------------------|
| **A** | Rotinas semanal/trimestral/anual + calendário ZFS completo + scrub cron automatizado |
| **B** | btop, fastfetch, lynis, ss, sensors, digest CrowdSec |
| **C** | Template de documentação de serviço (metadados, dependências, troubleshooting) |
| **G** | Lista completa do que guardar no Bitwarden |
| **H** | Plano de recuperação de desastre + ZFS rollback + criação CT/VM referência rápida |
| **J** | Macetes PVE 9: diagnóstico, hardware, Cloud-Init, CPU governor, vulnerabilidades Intel |
| **K** | Postura de segurança — o que protege e o que **não** protege (honestidade) |
| **L** | Sequência de aprendizagem Fortaleza → DNS → nginx → nftables → Docker → k3s |
| **M** | Aliases e funções de shell para host PVE e VM de estudo |
| **N** | Tor Hidden Service completo — CT 103, `.onion`, Tails OS, Android/Orbot |

### Expansão — guias completos (Apêndice D)

| Seção | O que você ganha |
|-------|-----------------|
| **D.2.1 AdGuard Home** | DNS bloqueador de anúncios para a LAN inteira |
| **D.2.2 Vaultwarden** | Bitwarden self-hosted com Docker Compose |
| **D.2.3 Nginx Proxy Manager** | HTTPS com Let's Encrypt para todos os serviços |
| **D.2.4 Uptime Kuma** | Alertas Telegram quando qualquer serviço cair |
| **D.3.1 bind9 do zero** | Zonas DNS, SOA, A/CNAME/MX, dig, named-checkzone |
| **D.3.2 nginx do zero** | Virtual hosts, HTTPS self-signed, proxy_pass |
| **D.3.3 nftables do zero** | Chains, DROP vs REJECT, stateful, persistência |
| **D.3.4 LAN simulada** | vmbr1 isolada, duas redes, VLAN tags |
| **D.4.1 Prometheus + Grafana** | Métricas do N5095, dashboard Node Exporter Full |
| **D.4.2 Ansible** | 3 playbooks prontos: health-check, criar CT, update-all |

### Bônus `scripts/`

Health-check só-leitura (`--json`), systemd timer, sync de backups para o PC, `Makefile` — [scripts/README.md](scripts/README.md).

---

## 📖 Como usar este guia

Cada fase segue sempre a mesma estrutura:

> 🎯 **OBJETIVO** — o que você vai conquistar
> 📚 **FUNDAMENTO** — por que estamos fazendo isso
> ⚙️ **COMANDOS** — passo a passo, comentados linha por linha
> ✅ **VERIFIQUE** — como ter certeza de que deu certo
> 🆘 **SE DEU ERRADO** — troubleshooting do erro mais comum

> ⚠️ **Não pule fases.** A ordem foi escolhida para você nunca perder o acesso ao servidor.

Para uma leitura “de cima” antes de mergulhar nas fases, use o [mapa do curso](docs/mapa-do-curso.md). A **ordem dos arquivos** em `docs/` (núcleo vs complemento vs operação) está em [docs/README.md](docs/README.md).

---

## Dicas para o aluno — como usar este guia (fundamentos)

Estas dicas valem para **todas** as fases. O objetivo é reduzir ansiedade e erros por pressa.

### 1. Leia antes de copiar

- Cada bloco **COMANDOS** mistura linhas que são **comentários** (começam por `#` no shell) com linhas que são **ordens reais** para o terminal.
- Quando o guia mostra **conteúdo de arquivo** (ex.: `interfaces`, `sshd_config`), o bloco pode ser “cole isto no editor” — não execute isso na shell como se fosse `bash`.
- Se um comando tiver `grep`, `|`, `&&` ou `$(...)`, é **composto**: leia o comentário acima para saber o que o filtro ou a condição fazem.

### 2. Duas sessões SSH (regra de ouro)

A partir do momento em que você mexe em **rede** ou **SSH**, mantenha **sempre** duas conexões abertas ao servidor (duas janelas de terminal, ou uma janela + console física / `Shell` no painel web). A primeira sessão é a “corda de segurança”; a segunda serve para testar. Se você fechar a única sessão no meio de um `restart` de rede ou SSH, o stress aumenta muito.

### 3. Exemplos não são a sua rede

Endereços como `192.168.1.100`, gateway `192.168.1.1`, interface `vmbr0` / `enp1s0` são **modelos**. Substitua pelos valores **da sua** LAN e pelos nomes que o **seu** `ip addr show` mostrar. Erro típico de novato: copiar IP do guia e depois não bater com o roteador.

### 4. O que é o bloco “Tradução”

Quando aparece **Tradução** (ou glossário inline), o guia está explicando **o significado** das linhas anteriores (opções do `sshd`, campos do `interfaces`, etc.). Nem todos os passos têm esse rótulo — muitas vezes a explicação está nos **comentários** `#` dentro do `bash`. Se você não entender uma flag, use `man comando` no Debian ou a wiki Proxmox ligada na fase.

### 5. Legenda rápida dos rótulos das fases

| Rótulo | Função |
|--------|--------|
| **OBJETIVO** | O que você vai ganhar ao terminar o passo. |
| **FUNDAMENTO** | Por que isso importa (segurança, rede, relógio…). |
| **COMANDOS** | Passos concretos. |
| **VERIFIQUE** | Provas de que funcionou; não avance sem isto quando a fase for crítica. |
| **SE DEU ERRADO** | O erro mais comum e como sair dele. |

### 6. Ferramentas e contexto

- **Bitwarden** (ou outro gerenciador): guarde segredos e códigos de recuperação **no momento** em que o guia os gera — ver Apêndice G.
- **Acesso físico** ao mini PC: trate-o como “plano B” sempre que você mexer em rede ou firewall.
- **Documentação satélite** (matriz de auditoria, mapa, cheat sheet Linux): ajudam a **orientar** e a **cruzar fontes**; não substituem executar as fases na ordem no host.

### 7. Se travar

1. Volte ao [manual de usabilidade](docs/manual-usabilidade-fortaleza.md) e confirme o **estágio** (A–E) em que você está.  
2. Volte ao [mapa do curso](docs/mapa-do-curso.md) e confirme em que **bloco** do host você está.  
3. Releia só o **FUNDAMENTO** e o **SE DEU ERRADO** dessa subseção no guia.  
4. Consulte a [matriz de auditoria](docs/audit-matrix.md) se a dúvida for “isso ainda bate com a documentação oficial?”.  
5. Apêndice H (recuperação) no guia se você perdeu acesso.

### 8. Manual de usabilidade do repositório (GPS)

Se não souber **em que “andar” do projeto** você está (repo vs host vs VM vs scripts bônus), abra o [manual de usabilidade em `docs/`](docs/manual-usabilidade-fortaleza.md) — estágios A a E e o que abrir em cada um. Depois volte a este guia na fase correta.

## Changelog da documentação

| Data | Alteração |
|------|-----------|
| 2026-05 | **v5.0** — rascunho inicial do guia (fases 0–10 e apêndices). |
| 2026-05-12 | Revisão do texto do guia contra fontes oficiais; matriz em [docs/audit-matrix.md](docs/audit-matrix.md). Secção **Dicas para o aluno** (usabilidade); relatório [docs/revisao-geral-projeto.md](docs/revisao-geral-projeto.md); validação linha-a-linha do guia principal **concluída** (Partes 1–7): [docs/validacao-linha-a-linha.md](docs/validacao-linha-a-linha.md). **Histórico detalhado** de arquivos satélites e reorganização da pasta `docs/`: [docs/CHANGELOG-repositorio.md](docs/CHANGELOG-repositorio.md). |
| 2026-05-12 | **Bónus `scripts/`:** [scripts/README.md](scripts/README.md) — `fortaleza-health-check.sh` (`--json`), [Makefile](Makefile) (`make check`), exemplos systemd para backup de `/etc/pve`, `pc/sync-fortaleza-backups.example.sh`; remissões na Fase 10 e Apêndice B. |
| 2026-05-12 | **Manual de usabilidade do repo:** [docs/manual-usabilidade-fortaleza.md](docs/manual-usabilidade-fortaleza.md) (estágios A–E); entradas no [README](README.md) raiz, [docs/README.md](docs/README.md), [mapa-do-curso.md](mapa-do-curso.md) e **Dicas para o aluno** §7–8. |

<span id="glossario-completo"></span>

## 📚 Glossário completo

| Termo | O que é |
|-------|---------|
| **Host** | O Proxmox em si, o sistema "pai" rodando no Mini PC |
| **LXC** | Container Linux leve (compartilha o kernel do host) |
| **CT** | Sigla do Proxmox para container LXC |
| **VM** | Máquina virtual completa (kernel próprio, mais pesada) |
| **PAM** | Sistema de autenticação do Linux ("quem pode logar?") |
| **TOTP** | Código de 6 dígitos que muda a cada 30s (Google Authenticator, Bitwarden) |
| **Bouncer** | Componente que efetivamente bloqueia IPs (o "braço" do CrowdSec) |
| **nftables** | Firewall moderno do kernel Linux (sucessor do iptables) |
| **`proxmox-firewall`** | Serviço do Proxmox VE 9 que aplica o firewall via nftables (backend **tech preview** na [wiki](https://pve.proxmox.com/wiki/Firewall#nftables)) |
| **`pve-firewall`** | Serviço legado (iptables); ainda existe mas é substituído |
| **drop-in config** | Arquivo separado em `/etc/.../conf.d/` que sobrescreve config principal |
| **Snapshot** | Foto do estado do sistema; permite voltar no tempo |
| **Realm** | "Reino" de autenticação do Proxmox (`pam` = Linux, `pve` = interno) |
| **deb822** | Formato moderno do APT para fontes (`.sources` em vez de `.list`) |
| **subnet routing** | Tailscale anunciando uma rede inteira para os peers |
| **TUN device** | Interface virtual de rede usada por VPNs (Tailscale precisa) |
| **`pct`** | Comando CLI do Proxmox para gerenciar containers |
| **`qm`** | Comando CLI do Proxmox para gerenciar VMs |

---

## 🏗️ Diagrama da arquitetura final

```
                    INTERNET
                        │
                        ▼
            ┌───────────────────────┐
            │ Roteador da sua casa  │  ← Sem port forwarding
            └───────────┬───────────┘
                        │ Rede local (192.168.1.0/24)
                        ▼
        ┌────────────────────────────────────────┐
        │  Mini PC — Proxmox VE 9.x              │
        │  ┌──────────────────────────────────┐  │
        │  │ proxmox-firewall (nftables) DROP │  │  ← tráfego da internet barrado (DROP)
        │  │  ▲ SSH (chave Ed25519 + 2FA)     │  │
        │  │  ▲ Web GUI (senha + 2FA TOTP)    │  │
        │  │  ▲ CrowdSec bouncer (nftables)   │  │  ← Bana IPs maliciosos
        │  └──────────────────────────────────┘  │
        │                                        │
        │  ┌──────────┐    ┌──────────────────┐  │
        │  │ CT 100   │    │ CT 200           │  │
        │  │ Tailscale│    │ lab-irmao        │  │
        │  │ + TUN    │    │ ShellHub Agent   │  │
        │  └──────────┘    └──────────────────┘  │
        └────────────────────────────────────────┘
                ▲                  ▲
                │                  │
        ┌───────┴───────┐  ┌──────┴──────────┐
        │ Tailscale     │  │ ShellHub Cloud  │
        │ (rede privada)│  │ (túnel reverso) │
        └───────┬───────┘  └────────┬────────┘
                │                   │
                ▼                   ▼
            Você (PC,           Seu irmão
            celular,            (acesso só à
            qualquer lugar)     VM dele)
```

---

## ⚠️ Antes de Começar — Leia Tudo

### Sobre o root no Proxmox

No Debian/Ubuntu puro, você costuma deixar o `root` sem senha e usar só sudo. **No Proxmox isso NÃO funciona.** O Proxmox usa o root internamente para vários serviços (cluster, `pveproxy`, `pvedaemon`). Travar a conta root começa a quebrar coisas silenciosamente.

A estratégia correta é **isolar** o root, não eliminá-lo:

| Onde | O que fazer |
|------|-------------|
| Senha root | Manter forte, guardada offline (Bitwarden) |
| SSH (porta 22) | Bloquear: `PermitRootLogin no` |
| Painel web (8006) | Criar `renato@pam` com Administrator + 2FA, nunca usar `root@pam` no dia-a-dia |
| Dia-a-dia | `ssh renato@ip` → `sudo -i` quando precisar |
| Emergência | Console físico (monitor + teclado no Mini PC) |

### Regras de ouro

1. 🔒 **Nunca feche todas as sessões SSH antes de testar a nova.** Mantenha sempre 2 janelas abertas durante mudanças críticas.
2. 📸 **Snapshot antes de cada fase grande.** No painel: `pve → Disks → ZFS → Snapshot`.
3. 📱 **Celular do lado** durante a Fase 3 (2FA). Sem ele, você não loga.
4. 🖥️ **Acesso físico ao Mini PC** funciona como "plano B" se tudo travar.
5. 📝 **Documente cada mudança** no diário do laboratório `~/fortaleza-lab/diario.md` (a pasta é criada na **Fase 1**; se ainda estiver na Fase 0, pode fazer uma vez `mkdir -p ~/fortaleza-lab` e usar esse arquivo, ou anotar temporariamente em outro lugar até chegar lá).

### Mini PC, RAM e o que fica ligado 24/7

O **Proxmox (host)** pode ficar **sempre ligado** — agendamentos de backup, rede e endurecimento do guia **não exigem** que todas as VMs/CTs do seu laboratório (oficina, DMZ, etc.) estejam **acesas ao mesmo tempo**. Em hosts com **pouca RAM** (ex.: 16 GB), o uso típico é: **infra leve no host** (e eventualmente um CT como o Tailscale) **+ só as VMs que precisar naquele momento**; desligue ou suspenda o resto quando não estiver estudando esse módulo. A **segurança do host** (SSH, 2FA, firewall, CrowdSec) protege a plataforma mesmo com poucos guests ligados — não é necessário “encher” o servidor para o guia fazer sentido.

### Pré-requisitos

- [ ] Proxmox VE 9.x instalado (`pveversion` retorna `pve-manager/9.x.x`)
- [ ] Você consegue acessar `https://IP-DO-PROXMOX:8006` no navegador
- [ ] Você consegue fazer `ssh root@IP-DO-PROXMOX` do seu PC
- [ ] Você tem acesso físico ao Mini PC (monitor + teclado) em caso de emergência
- [ ] Bitwarden (ou outro gerenciador de senhas) instalado e funcionando
- [ ] App TOTP no celular (Bitwarden, Aegis, Google Authenticator, 1Password)
- [ ] Cabo de rede conectado (não tente isso por Wi-Fi)

**Substitua nos comandos:** todo `192.168.1.100` pelo IP real do seu Proxmox.

### O que vai pro Bitwarden ANTES de começar

Crie uma pasta "Fortaleza Proxmox" e prepare entradas para:

1. **Senha do root do Proxmox** (definida na instalação)
2. **Senha do usuário `renato`** (vamos criar)
3. **Passphrase da chave SSH** (vamos criar)
4. **QR code/chave secreta do 2FA SSH** (vamos gerar)
5. **Códigos de recuperação 2FA SSH** (5 códigos)
6. **QR code/chave secreta do 2FA painel web** (vamos gerar)
7. **Códigos de recuperação 2FA painel** (vamos gerar)
8. **Conta Tailscale** (Google/GitHub OAuth)
9. **Conta ShellHub Cloud** (email + senha)
10. **Senha do root dos containers** (CT 100, CT 200)
11. **Senha do usuário `irmao`** (no CT 200)

> Apêndice G traz a lista completa para conferir no final.

### (Opcional) ProxMenux — menu interactivo na shell

[ProxMenux](https://proxmenux.com/) é uma ferramenta **de terceiros** (open source, projeto comunitário) que oferece um **menu interativo** na linha de comandos para tarefas comuns em Proxmox VE (recursos, rede, storage, VM/LXC, manutenção). Documentação introdutória: [Introduction](https://proxmenux.com/docs/introduction).

> **Segurança:** não é produto da Proxmox GmbH. O próprio ProxMenux avisa para **verificar a fonte** antes de executar scripts da Internet — o mesmo princípio do guia sobre `curl|bash`. Revê o [repositório GitHub](https://github.com/MacRimi/proxmenux) e a [instalação](https://proxmenux.com/docs/installation) **antes** de instalar em produção. Usar ProxMenux **não substitui** perceberes o que as Fases 0–7 fazem (rede, repos, SSH, firewall); serve sobretudo para **ganhar tempo** no dia-a-dia depois de dominares o básico.

---

# 🟢 FASE -1 — Instalação do Proxmox VE pela ISO

🎯 **OBJETIVO:** Instalar o Proxmox VE 9.x no Mini PC a partir do zero — baixar a ISO, gravar num pendrive, configurar a BIOS e concluir o assistente de instalação.
⏱ **Tempo estimado:** 30–60 min (mais tempo de download da ISO)

> ⚠️ **Já tem o Proxmox instalado?** Pule direto para a **Fase 0**. Esta fase é só para quem está começando do absoluto zero.

---

📚 **FUNDAMENTO**

O instalador do Proxmox VE é um sistema Debian mínimo com o ambiente web já configurado. A escolha de filesystem (ZFS vs LVM-Thin) feita aqui **não tem volta fácil** — escolha com atenção. O Proxmox precisa de virtualização de hardware habilitada na BIOS para criar VMs (não só containers LXC).

---

## -1.1 Download da ISO oficial

```bash
# No seu PC — verifique a versão mais recente em:
# https://www.proxmox.com/en/downloads/proxmox-virtual-environment/iso

# Baixe a ISO mais recente (ex.: proxmox-ve_9.1-1.iso)
# SEMPRE verifique o SHA256 publicado na mesma página:
sha256sum proxmox-ve_9.1-1.iso
# Compare com o valor publicado no site antes de continuar
```

> Fonte oficial: [Proxmox VE ISO Downloads](https://www.proxmox.com/en/downloads/proxmox-virtual-environment/iso)

---

## -1.2 Criar pendrive bootável

Escolha **um** dos métodos abaixo conforme o seu sistema:

**Linux / macOS (dd):**
```bash
# CUIDADO: substitua /dev/sdX pelo dispositivo do pendrive (verifique com lsblk)
# Este comando apaga TUDO no pendrive
sudo dd if=proxmox-ve_9.1-1.iso of=/dev/sdX bs=1M status=progress
sync
```

**Windows — Ventoy (recomendado para múltiplas ISOs):**
1. Baixe o [Ventoy](https://www.ventoy.net/en/download.html) e instale no pendrive
2. Copie o arquivo `.iso` para a partição Ventoy
3. Boot pelo pendrive → selecione a ISO no menu

**Windows — Rufus (alternativa simples):**
1. Baixe o [Rufus](https://rufus.ie/) (sem instalação)
2. Seleccione o pendrive e a ISO → clique em "Iniciar"
3. Modo recomendado: DD Image (Rufus pergunta automaticamente para ISOs híbridas)

> ⚠️ **Balena Etcher** também funciona mas foi descontinuado; prefira Rufus ou Ventoy.

---

## -1.3 Configurar a BIOS do Mini PC

Ligue o Mini PC e entre na BIOS (geralmente **Delete**, **F2** ou **F12** durante o POST):

| Configuração | Valor recomendado | Porquê |
|-------------|-------------------|--------|
| **Intel VT-x** (ou AMD-V) | **Habilitado** | Obrigatório para criar VMs. Sem isto só LXC funciona |
| **Intel VT-d** (ou AMD-Vi) | Habilitado (se disponível) | Opcional agora; necessário para passthrough de GPU/USB no futuro |
| **Boot Mode** | **UEFI** (recomendado) | Compatível com ZFS EFI e Secure Boot futuro |
| **Secure Boot** | Desabilitado | O instalador Proxmox 9 pode não ter Shim assinado; desabilite durante a instalação |
| **Fast Boot / Quick Boot** | Desabilitado | Pode ignorar dispositivo USB no boot |
| **Boot Order** | USB primeiro | Para arrancar pelo pendrive |

> Se o Mini PC N5095 (ou similar) não mostrar VT-x, verifique se está num submenu "Advanced" ou "CPU Configuration".

---

## -1.4 Assistente de instalação do Proxmox VE

Após bootar pelo pendrive, o instalador gráfico apresenta estas escolhas:

### Escolha do filesystem (passo mais crítico)

| Opção | Quando escolher | Notas |
|-------|----------------|-------|
| **ZFS (RAID0)** | Um disco — **recomendado para homelab** | Snapshots nativos (usados extensivamente neste guia); compressão; integridade de dados |
| **ZFS (RAID1)** | Dois discos iguais | Espelho; melhor resiliência, mesma capacidade de um disco |
| **ext4 em LVM-Thin** | Se ZFS der problema de RAM (mín. 8 GB recomendado para ZFS) | Sem snapshots nativos; mais simples |
| **ext4 / xfs** | Raramente — só se tiver razão específica | Sem LVM-Thin, sem snapshots |

> **Para o Mini PC com 16 GB RAM:** escolha **ZFS (RAID0)** num único disco. É o que este guia assume nas fases seguintes (`zfs snapshot`, `zfs rollback`).

### Configurações do assistente

```
Hostname (FQDN): fortaleza.local       ← ou o nome que quiser; deve ter .local ou .domínio
IP Address:      192.168.1.100         ← use o IP que quer fixar (veja Fase 0.3)
Netmask:         255.255.255.0
Gateway:         192.168.1.1           ← IP do seu roteador
DNS:             1.1.1.1               ← ou o DNS do seu roteador
```

> **Anote** estas configurações — vão ser usadas na tabela Pré-voo da Fase 0.

### Senha root

- Defina uma senha **forte** (mín. 20 caracteres, aleatória)
- Guarde **imediatamente** no Bitwarden → pasta "Fortaleza Proxmox" → entrada "Root Proxmox"

---

## -1.5 Primeiro acesso após instalação

```bash
# No browser do seu PC:
https://192.168.1.100:8006
# Utilizador: root
# Senha: a que definiu no instalador
# ⚠️ Aviso de certificado SSL: clique "Avançado" → "Aceitar" (é normal — certificado auto-assinado)

# Também pode abrir SSH já neste momento:
ssh root@192.168.1.100
```

✅ **VERIFIQUE**

```bash
# No shell do Proxmox (SSH ou terminal web):
pveversion          # deve mostrar pve-manager/9.x...
uname -r            # deve mostrar kernel recente (ex.: 6.x.x-pve)
zpool list          # deve mostrar o pool ZFS (ex.: rpool) se escolheu ZFS
ip addr show vmbr0  # deve mostrar o IP que configurou no instalador
```

---

🆘 **SE DEU ERRADO**

| Sintoma | Causa provável | Solução |
|---------|---------------|---------|
| Pendrive não aparece no boot | Fast Boot ativo ou USB 3.x incompatível | Desabilite Fast Boot; tente porta USB 2.0 |
| "VT-x not found" no instalador | VT-x desabilitado na BIOS | Entre na BIOS → CPU Configuration → habilite Intel VT-x |
| Instalação falha no ZFS | RAM insuficiente ou disco com setores ruins | Tente ext4+LVM-Thin; ou teste disco com `badblocks` |
| `https://IP:8006` não abre | IP errado no instalador ou firewall do roteador | Aceda pelo console físico; `ip addr show vmbr0` para verificar IP real |
| Aviso de certificado SSL | Normal — certificado auto-assinado | Clique "Avançar" / "Accept Risk" no browser |

---

```bash
echo "## $(date +"%F %H:%M") - Fase -1 concluída" >> ~/fortaleza-lab/diario.md
echo "- Proxmox VE instalado, acesso web e SSH OK" >> ~/fortaleza-lab/diario.md
```

> **Próximo passo:** [Fase 0 — Preparação do Sistema](#-fase-0--preparação-do-sistema-fundação)

---

# 🟢 FASE 0 — Preparação do Sistema (FUNDAÇÃO)

🎯 **OBJETIVO:** Deixar o Proxmox saudável **antes** de aplicar qualquer hardening. Atualizar, fixar IP, ajustar relógio, corrigir repositórios.
⏱ **Tempo estimado:** 45–90 min (fase mais longa — faça com calma)

---

## 📋 Pré-voo — Recolha estes valores UMA VEZ antes de começar

> Execute estes comandos no terminal do Proxmox (ainda como root) e anote os resultados **no seu editor** — vai usá-los em múltiplas fases.

```bash
ip addr show       # → anote a interface física (ex.: enp1s0) e o IP atual de vmbr0
ip route           # → anote a linha "default via X.X.X.X" (gateway/roteador)
hostname           # → anote o hostname atual
timedatectl        # → anote o timezone atual
```

| Campo | Comando relevante | **O seu valor** |
|-------|-------------------|-----------------|
| IP atual do Proxmox | `ip -4 addr show vmbr0 \| grep inet` | ____________ |
| Gateway (roteador) | `ip route \| grep default` | ____________ |
| Interface física | `ip addr show` (ex.: `enp1s0`, `eth0`) | ____________ |
| Hostname | `hostname` | ____________ |
| Timezone pretendido | `timedatectl list-timezones \| grep -i brasil` | ____________ |

> **Porquê agora?** Os IPs e nomes de interface variam com cada hardware. Saber os valores reais **antes** de copiar comandos evita o erro mais comum: copiar o IP `192.168.1.100` do guia sem verificar se é o seu.

---

> ⚠️ **Esta fase é a mais importante de todas.** Pular ela causa bugs que aparecem só depois (TOTP falhando, `apt update` quebrando, IP mudando). Faça com calma.

### Login inicial

Use SSH normalmente (ainda como root, vamos trocar isso na Fase 1):

```bash
ssh root@192.168.1.100
```

> Não se trancou em nenhum lugar ainda. Tranquilo.

---

## 0.1 Configurar Timezone e NTP

📚 **FUNDAMENTO:** O TOTP (2FA) usa o **relógio do servidor** sincronizado com o **relógio do seu celular**. Se houver diferença de mais de 30s, os códigos não batem e você não consegue logar. Por isso, **antes** de configurar 2FA, garantimos que o relógio está certo via NTP (Network Time Protocol).

### Definir timezone

```bash
# Lista timezones disponíveis — filtre pelo seu país/cidade
timedatectl list-timezones | grep -i sao_paulo   # Brasil (São Paulo)
timedatectl list-timezones | grep -i lisbon       # Portugal (Lisboa)
timedatectl list-timezones | grep -i america      # América em geral
# Ou liste tudo e procure manualmente:
# timedatectl list-timezones | less

# Define o timezone (substitua pelo resultado do grep acima)
# Exemplos: America/Sao_Paulo | Europe/Lisbon | America/Recife | Atlantic/Azores
timedatectl set-timezone America/Sao_Paulo   # ← substitua pelo seu timezone
```

### Verificar sincronização NTP

```bash
timedatectl status
```

**Saída esperada:**
```
               Local time: Tue 2026-05-12 14:30:15 -03
           Universal time: Tue 2026-05-12 17:30:15 UTC
                 RTC time: Tue 2026-05-12 17:30:15
                Time zone: America/Sao_Paulo (-03, -0300)
System clock synchronized: yes
              NTP service: active
          RTC in local TZ: no
```

> ⚠️ **`System clock synchronized: yes`** e **`NTP service: active`** são obrigatórios. Se aparecer `no`, force a sincronização:

```bash
# Garantir que o systemd-timesyncd está rodando
systemctl enable --now systemd-timesyncd
systemctl status systemd-timesyncd --no-pager
```

### ✅ Verifique

```bash
date
# Saída esperada: data e hora REAL (compare com seu celular)
```

---

## 0.2 Configurar IP Fixo

📚 **FUNDAMENTO:** Por padrão, o Proxmox usa o IP que recebeu durante a instalação. Se ele estiver via DHCP, **pode mudar** quando o roteador reiniciar — e você perde o acesso porque seu firewall (Fase 7) só permite IPs específicos.

Existem duas formas: **(a)** reservar IP no roteador (DHCP reservation) ou **(b)** configurar IP estático no Proxmox.

A forma mais segura é **fazer as duas**.

### Opção A — Reserva no roteador (recomendado fazer ANTES)

No painel do roteador, encontre a seção `DHCP Reservation` (ou `Static Leases`). Adicione:
- MAC address do Mini PC: descubra com `ip addr show` no Proxmox (campo `link/ether`)
- IP desejado: `192.168.1.100`
- Hostname: `pve`

### Opção B — IP estático no Proxmox

⚠️ **Cuidado nesta etapa.** Errar aqui pode te deixar sem rede. Tenha acesso físico ao Mini PC.

```bash
# Ver interfaces atuais
ip addr show

# Identifique o nome da interface (geralmente enp1s0 ou eno1)
# E a bridge do Proxmox (vmbr0)
```

Edite o arquivo de rede:

```bash
nano /etc/network/interfaces
```

Você verá algo como:
```
auto vmbr0
iface vmbr0 inet dhcp
    bridge-ports enp1s0
    bridge-stp off
    bridge-fd 0
```

Mude `dhcp` para `static` e adicione IP/gateway/DNS:

```
auto vmbr0
iface vmbr0 inet static
    address 192.168.1.100/24
    gateway 192.168.1.1
    bridge-ports enp1s0
    bridge-stp off
    bridge-fd 0
    dns-nameservers 1.1.1.1 8.8.8.8
```

> **Tradução:**
> - `address 192.168.1.100/24` — IP do Proxmox / máscara de 24 bits (255.255.255.0)
> - `gateway 192.168.1.1` — IP do seu roteador
> - `dns-nameservers 1.1.1.1 8.8.8.8` — DNS público (Cloudflare + Google)

Salve (`Ctrl+O`, Enter, `Ctrl+X`) e aplique:

```bash
# ifreload vem do pacote ifupdown2 (normalmente já instalado no PVE novo; em upgrades antigos pode faltar)
command -v ifreload >/dev/null || apt install -y ifupdown2

# Aplica a config nova sem reiniciar
ifreload -a
# Saída típica inclui algo como: applying /etc/network/interfaces ...
```

> Se `ifreload` falhar com «command not found» mesmo após instalar `ifupdown2`, usa o caminho mais conservador: `systemctl restart networking` (pode cortar SSH momentaneamente — tenha console físico ou segunda sessão).

```bash
# OU se preferir mais conservador (reinicia stack de rede inteira):
# systemctl restart networking
```

### ✅ Verifique

```bash
ip -4 addr show vmbr0
# Saída esperada: inet 192.168.1.100/24 ...

ping -c 3 1.1.1.1
# Saída esperada: 3 pacotes recebidos

ping -c 3 google.com
# Saída esperada: 3 pacotes recebidos (testa DNS também)
```

### 🆘 Se deu errado

**Erro:** Perdeu conexão SSH ao reiniciar rede
**Solução:** Console físico do Mini PC, logue como root, edite o arquivo de volta para `dhcp` ou corrija a sintaxe.

---

## 0.3 Configurar Hostname e `/etc/hosts`

📚 **FUNDAMENTO:** O Proxmox tem uma quirk importante: o hostname **precisa resolver** para o IP do nó no `/etc/hosts`. Se isso quebra, vários serviços do Proxmox (cluster, pveproxy) começam a falhar de formas estranhas.

### Verificar configuração atual

```bash
hostname              # Anote o nome curto (ex.: pve) — usa-o nas linhas de /etc/hosts abaixo
hostname -i           # Deve retornar o IP correto do nó, NÃO 127.0.1.1
cat /etc/hosts        # Deve mapear esse IP ao hostname (ex.: 192.168.1.100 pve.local pve)
```

### Corrigir se necessário

Se `hostname -i` retornou `127.0.1.1` ou erro:

```bash
nano /etc/hosts
```

Garanta que tenha (substitua pelo seu IP):
```
127.0.0.1 localhost
192.168.1.100 pve.local pve

# Linhas IPv6 padrão (mantenha)
::1 localhost ip6-localhost ip6-loopback
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
```

### ✅ Verifique

```bash
ping -c 1 "$(hostname)"
# Saída esperada: ping para o mesmo IP que hostname -i mostrou (não 127.0.0.1)
```

---

## 0.4 Corrigir Repositórios (Enterprise → No-Subscription)

📚 **FUNDAMENTO:** Por padrão, o Proxmox vem configurado para usar o repositório **Enterprise**, que só funciona com subscription paga. Sem subscription, todo `apt update` falha com erro `401 Unauthorized`. Para uso doméstico, trocamos para o repositório **No-Subscription** (gratuito, mesmas atualizações com pequeno atraso).

> ⚠️ **Proxmox VE 9 (Debian 13 Trixie) usa o formato moderno `deb822` (`.sources`).** Não confunda com o formato antigo `.list` — o APT em Trixie avisa sobre formato legacy; veja [Repository formats](https://pve.proxmox.com/wiki/Package_Repositories#sysadmin_apt_repo_formats) na wiki.

### Desabilitar o repositório Enterprise

O método **documentado na wiki** é desactivar a entrada **sem** partir o formato deb822: `Enabled: no` no bloco correto, ou desligar a entrada no painel.

**Recomendado (menos erro que `sed` em arquivo `.sources`):**

1. No painel web: **nó (pve) → Updates → Repositories** — selecione `pve-enterprise` → **Disable** (equivalente a `Enabled: no` no deb822).
2. **Ou** no host: `nano /etc/apt/sources.list.d/pve-enterprise.sources` e acrescente `Enabled: no` ao bloco do repositório enterprise (mantém o arquivo legível para voltar a `yes` com subscription).

> **Evite** `sed -i 's/^/# /'` em `.sources` deb822: comentar **todas** as linhas (incluindo cabeçalhos de seção) pode deixar o APT com arquivo malformado. Se **só** tiver shell, edite manualmente ou use o painel.

Faça o equivalente para o repositório **Ceph** (não usamos em lab pequeno): no mesmo ecrã **Repositories**, desactive `ceph-enterprise` / entradas Ceph, **ou** `Enabled: no` no arquivo `ceph.sources` correspondente — **não** uses comentário em massa com `sed` no deb822.

### Adicionar o repositório No-Subscription

Crie o arquivo no formato `deb822` (a wiki sugere o nome [`/etc/apt/sources.list.d/proxmox.sources`](https://pve.proxmox.com/wiki/Package_Repositories); qualquer nome `.sources` em `sources.list.d/` é válido):

```bash
nano /etc/apt/sources.list.d/pve-no-subscription.sources
```

Cole exatamente:

```
Types: deb
URIs: http://download.proxmox.com/debian/pve
Suites: trixie
Components: pve-no-subscription
Signed-By: /usr/share/keyrings/proxmox-archive-keyring.gpg
```

Salve e saia.

### ✅ Verifique

```bash
apt update
```

**Saída esperada:** lista de repos lidos, terminando com `Reading package lists... Done`. **Sem** erros `401 Unauthorized`.

```bash
apt list --upgradable 2>/dev/null | head
# Saída esperada: lista de pacotes a atualizar (ou vazia se já tá tudo)
```

### 🆘 Se deu errado

**Erro:** `The repository 'https://enterprise.proxmox.com/debian/pve trixie InRelease' is not signed`
**Solução:** O repositório enterprise ainda está ativo. No painel **Updates → Repositories**, desactive `pve-enterprise`, **ou** em `pve-enterprise.sources` use `Enabled: no` no bloco correto (evite `sed` que comenta o arquivo inteiro em deb822).

**Erro:** Chave GPG do Proxmox faltando
**Solução:**
```bash
wget https://enterprise.proxmox.com/debian/proxmox-archive-keyring-trixie.gpg \
  -O /usr/share/keyrings/proxmox-archive-keyring.gpg
```

---

## 0.5 (Opcional) Remover o "Subscription Nag" do Painel Web

📚 **FUNDAMENTO:** Quando você loga no painel web sem subscription, aparece um popup chato "No valid subscription". Isso não afeta segurança nem funcionalidade, é só visual. Você pode:
- **(a)** ignorar e clicar OK toda vez
- **(b)** comprar uma subscription (R$ ~600/ano para Community)
- **(c)** aplicar um patch que remove o popup

Se preferir (c), use o script da comunidade **community-scripts** (amplamente usado em homelab; **não** é da Proxmox GmbH — mesmo tipo de risco de *supply chain* que `curl|sh` ou ProxMenux de terceiros).

> **Cadeia de confiança:** `wget|bash` executa código remoto com os privilégios que o script pedir. Abre o script no GitHub **antes** (compare o URL `raw` com o repositório oficial), lê o que ele altera em `/etc` e no APT, usa só o commit/branch em que confias, e testa primeiro em máquina descartável se possível. Não há substituto «oficial Proxmox» para este patch — ou ignoras o popup ou aceitas o risco com consciência.

```bash
# Versão "tteck" / "community-scripts" — auditar em https://github.com/community-scripts/ProxmoxVE/blob/main/misc/post-pve-install.sh
bash -c "$(wget -qLO - https://github.com/community-scripts/ProxmoxVE/raw/main/misc/post-pve-install.sh)"
```

> Esse script é interativo. Ele pergunta:
> - **Disable the Enterprise Repository?** → **Yes** (já fizemos manualmente, mas confirma)
> - **Enable the No-Subscription Repository?** → **Yes**
> - **Correct ceph.sources?** → **Yes**
> - **Add or correct the test Repository?** → **No**
> - **Disable the subscription nag?** → **Yes**
> - **Update Proxmox VE Now?** → **Yes**

Depois, faça **hard reload** do navegador (`Ctrl+Shift+R`) para limpar o cache do popup.

### ✅ Verifique

Saia do painel web e entre de novo. O popup não deve mais aparecer.

---

## 0.6 Atualizar o Sistema

```bash
apt update && apt full-upgrade -y
apt install sudo curl wget nano gnupg ca-certificates git -y
```

> **O que cada pacote faz:**
> - `sudo` — permite usuário comum executar comandos como root
> - `curl` / `wget` — baixam arquivos da internet (scripts de instalação)
> - `nano` — editor de texto simples
> - `gnupg` / `ca-certificates` — necessários para repositórios externos seguros
> - `git` — vai ser útil para clonar configs/scripts depois

Se kernel foi atualizado, reinicie:

```bash
# Modo interactivo: pergunta o que reiniciar (mais seguro para novatos que a Fase 9.1b ainda não leu)
# -k = só kernel/módulos (lista mais curta). Sem -k, o needrestart também propõe serviços — útil se quiser rever tudo.
needrestart -k -r i

# OU reboot total se preferir
reboot
```

> O modo `-r a` (reinício **automático** de serviços) existe mas **não** é «só uma pergunta» — lê a seção **9.1b** antes de usar ou de editar `/etc/needrestart/needrestart.conf`.

### ✅ Verifique

```bash
pveversion
# Saída esperada: pve-manager/9.x.x/xxxxx (running kernel: conforme uname)

uname -r
# Saída esperada: kernel PVE atual (ex.: 6.x.x-pve — varia com updates)

cat /etc/debian_version
# Saída esperada: 13.x (Trixie) ou superior
```

---

## 0.7 Backup Inicial do `/etc/pve`

📚 **FUNDAMENTO:** O diretório `/etc/pve` contém **toda a configuração** do Proxmox (firewall, usuários, VMs, containers, certificates). Se algo corromper, você perdeu tudo. Antes de cada fase grande, faça um tar dessa pasta.

```bash
# Cria pasta de backups
mkdir -p /root/backups

# Backup inicial
tar czf /root/backups/etc-pve-fase0-$(date +%F).tar.gz /etc/pve/

# Verifica
ls -lh /root/backups/
```

> Recomendo copiar esse arquivo para fora do servidor (seu PC, OneDrive, etc.) depois de cada fase importante.

---

## 0.8 Snapshot ZFS Inicial

Se você instalou Proxmox com ZFS (padrão recomendado):

> **Dataset ZFS:** o caminho `rpool/ROOT/pve-1` usado nos comandos deste guia é um **exemplo** comum após instalação pela ISO. O seu pode ser outro — confirme com `zfs list` (dataset montado em `/`) e substitua em **todos** os `zfs snapshot` das fases seguintes.

No painel web:
1. `pve → Disks → ZFS`
2. Selecione o pool root (`rpool`)
3. **Snapshot** → Nome: `snap-fase0-instalacao-limpa`

Pelo terminal (alternativa):

```bash
# Exemplo — ajuste o dataset ao output de: zfs list
zfs snapshot rpool/ROOT/pve-1@snap-fase0-instalacao-limpa
zfs list -t snapshot
```

> Se você usa LVM-Thin (instalação antiga), snapshots de host são limitados. Use o backup `tar` do `/etc/pve` como alternativa principal.

---

## ✅ Checklist da Fase 0

- [ ] Timezone configurado para sua região
- [ ] `timedatectl status` mostra `NTP service: active` e `synchronized: yes`
- [ ] IP fixo configurado (reservado no roteador OU estático no PVE)
- [ ] `hostname -i` retorna o IP correto (não `127.0.1.1`)
- [ ] Repositório Enterprise desabilitado
- [ ] Repositório No-Subscription habilitado
- [ ] `apt update` funciona sem erros
- [ ] Sistema atualizado (`pveversion` mostra última versão)
- [ ] Backup inicial do `/etc/pve` em `/root/backups/`
- [ ] Snapshot ZFS `snap-fase0-instalacao-limpa` criado **ou** N/A (instalação sem ZFS — nesse caso o backup `tar` do `/etc/pve` é ainda mais importante)

---

## Dataset ZFS nos comandos seguintes

Sempre que aparecer `rpool/ROOT/pve-1` num `zfs snapshot`, use o **mesmo** dataset que você confirmou em **0.8** (não copie cegamente se o seu `zfs list` mostrar outro nome).

---

# 🟢 FASE 1 — Identidade e Privilégios

🎯 **OBJETIVO:** Criar `renato` com poder de virar root quando precisar (via `sudo`).
⏱ **Tempo estimado:** 15–20 min

📚 **FUNDAMENTO:** O `root` é o "Deus" do Linux — pode destruir o sistema com um comando errado. Trabalhar com usuário comum + sudo cria uma barreira intencional: quando você digita `sudo`, é como passar a chave do cofre. Você pensa duas vezes antes de fazer algo destrutivo.

### 📸 Snapshot antes de começar

```bash
# Como root (sessão onde criou o usuário renato)
zfs snapshot rpool/ROOT/pve-1@snap-pre-fase1
```

### ⚙️ Comandos

Logado como root:

```bash
adduser renato
```

> Vai pedir senha. **Forte, e guarde no Bitwarden.** Perguntas extras (Full Name, etc.) podem ficar em branco — só apertar Enter.

```bash
usermod -aG sudo renato
```

> **Tradução:** `usermod` modifica usuário, `-a` append (adiciona, não substitui), `-G sudo` ao grupo sudo, `renato` o alvo.

### ✅ Verifique

**Em um SEGUNDO terminal** (não feche o primeiro!):

```bash
ssh renato@192.168.1.100      # Senha do renato

sudo whoami                    # Pede a senha do renato de novo
# Saída esperada: root
```

✅ Se apareceu `root`, sudo OK. Pode prosseguir.

### 📝 Documente no diário

```bash
# Como renato
mkdir -p ~/fortaleza-lab
echo "## $(date +"%F %H:%M") - Fase 1 concluída" >> ~/fortaleza-lab/diario.md
echo "- Criado usuário renato com sudo" >> ~/fortaleza-lab/diario.md
```

### 🆘 Se deu errado

**Erro:** `renato is not in the sudoers file`
**Solução:** Você precisa estar **logado como root** (não como renato com sudo) para executar `usermod`:
```bash
# Pelo terminal do root original:
usermod -aG sudo renato
```
Saia (`exit`) e entre de novo. Grupos só são lidos no login.

---

# 🟢 FASE 2 — Chaves SSH (Adeus Senhas)

🎯 **OBJETIVO:** Substituir senha por chave Ed25519. Só entra quem tem o arquivo da chave privada.
⏱ **Tempo estimado:** 20–30 min

📚 **FUNDAMENTO:** Uma chave Ed25519 tem segurança matemática equivalente a milhares de anos de computação para quebrar. É o padrão atual usado por GitHub, AWS, etc.

> ⚠️ **OpenSSH 10 no Debian 13 REMOVEU suporte a DSA** completamente. Use Ed25519.

### 📸 Snapshot

```bash
# Como root
zfs snapshot rpool/ROOT/pve-1@snap-pre-fase2
```

### 2.1 Gerar a chave (no SEU PC pessoal)

⚠️ **Esta etapa é no seu computador, não no Proxmox.**

```bash
ssh-keygen -t ed25519 -C "renato-mini-pc" -f "$HOME/.ssh/chave_fortaleza"
```

> **Tradução:**
> - `-t ed25519` — tipo de chave (moderno e seguro)
> - `-C "renato-mini-pc"` — comentário descritivo (fica no final da chave pública)
> - `-f "$HOME/.ssh/chave_fortaleza"` — onde salvar (evita sobrescrever sua chave padrão)

```
Enter passphrase (empty for no passphrase):
```

> 🔐 **Recomendação forte: coloque uma passphrase.** Se alguém roubar o arquivo da chave, ainda precisa dessa senha. **Guarde a passphrase no Bitwarden.**

**Resultado:** dois arquivos criados em `~/.ssh/`:
- `chave_fortaleza` (privada — **NUNCA compartilhe, nunca faça upload**)
- `chave_fortaleza.pub` (pública — pode ser distribuída)

### 2.2 Enviar a chave pública para o Proxmox

```bash
ssh-copy-id -i "$HOME/.ssh/chave_fortaleza.pub" renato@192.168.1.100
```

> Pede a senha do renato uma última vez. Depois disso, a chave está registrada em `/home/renato/.ssh/authorized_keys` no servidor.

### 2.3 Testar o acesso sem senha

```bash
ssh -i "$HOME/.ssh/chave_fortaleza" renato@192.168.1.100
```

> Se entrou direto (pedindo só a passphrase da chave que VOCÊ definiu localmente), sucesso! ✅

### 2.4 (Opcional mas recomendado) Configurar `~/.ssh/config` no seu PC

Cria atalhos para não precisar digitar `-i` e IP todas as vezes:

No seu PC pessoal:

```bash
nano ~/.ssh/config
```

Cole:

```
Host fortaleza
    HostName 192.168.1.100
    User renato
    IdentityFile ~/.ssh/chave_fortaleza
    IdentitiesOnly yes
```

Salve. Agora você acessa só com:

```bash
ssh fortaleza
```

### 2.5 Hardening do SSH via drop-in config

📚 **FUNDAMENTO:** No Debian 13, a melhor prática é criar arquivos em `/etc/ssh/sshd_config.d/` em vez de editar o `sshd_config` principal. Por quê?
- O `sshd_config` principal pode ser sobrescrito em atualizações
- Configs em `sshd_config.d/` têm prioridade e sobrevivem
- Mais fácil de versionar e reverter mudanças

⚠️ **Mantenha 2 sessões SSH abertas durante esta etapa.**

```bash
sudo nano /etc/ssh/sshd_config.d/99-hardening.conf
```

Cole exatamente:

```
# ===========================================
# Hardening SSH - Fortaleza Proxmox
# ===========================================

# Autenticação
PasswordAuthentication no
PubkeyAuthentication yes
PermitRootLogin no
PermitEmptyPasswords no

# Limites e timeouts
MaxAuthTries 3
LoginGraceTime 30
ClientAliveInterval 300
ClientAliveCountMax 2

# Reduzir superfície de ataque
X11Forwarding no
AllowAgentForwarding no
AllowTcpForwarding no

# PAM (necessário pro 2FA da Fase 3)
UsePAM yes
```

> **Tradução de cada linha:**
> - `PasswordAuthentication no` — proíbe login por senha
> - `PubkeyAuthentication yes` — permite login por chave pública
> - `PermitRootLogin no` — bloqueia root via SSH completamente
> - `PermitEmptyPasswords no` — defensive (nunca permite senha vazia)
> - `MaxAuthTries 3` — desconecta após 3 tentativas falhas
> - `LoginGraceTime 30` — só 30s para completar login
> - `ClientAliveInterval 300` — checa se cliente está vivo a cada 5min
> - `ClientAliveCountMax 2` — desconecta após 2 checks sem resposta
> - `X11Forwarding no` — desabilita encaminhamento gráfico
> - `AllowAgentForwarding no` — proíbe forward do ssh-agent
> - `AllowTcpForwarding no` — proíbe túneis TCP locais `ssh -L` / `-D` / `-R` **neste host** (**endurecimento forte**). Se no futuro precisares de port forwarding SSH para debug, o sintoma típico é falha **silenciosa** ou recusa sem mensagem clara — aí comenta temporariamente ou muda para `yes` **só** no drop-in. **Não** afecta o ShellHub no CT do irmão (túnel reverso do *agent* para a cloud ShellHub); afecta **só** o que passa pelo `sshd` do host PVE.
> - `UsePAM yes` — habilita PAM (vamos usar pro 2FA)

Salve (`Ctrl+O`, Enter) e saia (`Ctrl+X`).

### Validar a sintaxe ANTES de reiniciar

```bash
sudo sshd -t
```

> Não deve retornar nada (silêncio = OK). Se retornar erro, **corrija antes** de reiniciar.

> ⚠️ **No Debian 13 o serviço chama-se `ssh`, não `sshd`.** `systemctl restart sshd` dá erro.

```bash
sudo systemctl restart ssh
```

### ✅ Verifique

**Em uma TERCEIRA sessão**:

```bash
ssh fortaleza                      # Deve entrar direto
ssh root@192.168.1.100             # Deve dar: Permission denied (publickey)
```

Verifique configurações ativas:

```bash
sudo sshd -T | grep -E 'passwordauthentication|permitrootlogin|pubkeyauthentication|maxauthtries'
# Saída esperada:
# passwordauthentication no
# pubkeyauthentication yes
# permitrootlogin no
# maxauthtries 3
```

### 🆘 Se deu errado

**Erro:** `Permission denied (publickey)` para renato
**Causa:** Chave não foi instalada corretamente.
**Solução:** Pelo console do Proxmox (físico ou `pve → Shell`):
```bash
cat /home/renato/.ssh/authorized_keys
# Verifique se sua chave pública aparece

ls -la /home/renato/.ssh/
# Permissões devem ser: 700 para .ssh, 600 para authorized_keys
```

**Erro:** Fechou tudo e não consegue mais entrar
**Solução:** Console físico ou `pve → Shell` no painel web. Logue como root, edite o arquivo `/etc/ssh/sshd_config.d/99-hardening.conf`, remova as restrições, `systemctl restart ssh`.

### 📝 Documente

```bash
echo "## $(date +"%F %H:%M") - Fase 2 concluída" >> ~/fortaleza-lab/diario.md
echo "- SSH só com chave Ed25519, drop-in em sshd_config.d/" >> ~/fortaleza-lab/diario.md
```

---

# 🟢 FASE 3 — 2FA no SSH (TOTP)

🎯 **OBJETIVO:** Mesmo que sua chave privada seja roubada, sem o código do app autenticador o atacante não entra.
⏱ **Tempo estimado:** 20–30 min

📚 **FUNDAMENTO:** A chave SSH é "algo que você tem" (arquivo). O TOTP é "algo que muda a cada 30s" (gerado pelo celular). Combinação praticamente inquebrável.

> ⚠️ **A partir daqui, perder o celular = perder o acesso.** Guarde os códigos de recuperação no Bitwarden!

> ⚠️ Esta fase só funciona porque você sincronizou o relógio na Fase 0. Sem NTP, o TOTP falha silenciosamente.

### 📸 Snapshot

```bash
# Como renato (sudo) — o dataset continua a ser o que ajustaste na Fase 0.8
sudo zfs snapshot rpool/ROOT/pve-1@snap-pre-fase3
```

### 3.1 Instalar o módulo PAM

```bash
sudo apt install libpam-google-authenticator -y
```

> "Google Authenticator" aqui é só o nome do projeto. Você pode usar qualquer app TOTP (Bitwarden, Aegis, etc.).

### 3.2 Configurar o 2FA para o renato

⚠️ **Logado como `renato`** (não como root, não com sudo):

```bash
google-authenticator
```

Responda:

| Pergunta | Resposta | Por quê |
|----------|----------|---------|
| Time-based tokens? | **y** | Códigos que mudam por tempo (padrão TOTP) |
| Update the file? | **y** | Salva a configuração |
| Disallow multiple uses? | **y** | Cada código só serve uma vez |
| Increase time skew? | **n** | Só ative se seu celular tem relógio errado |
| Enable rate-limiting? | **y** | Limita tentativas (anti-bruteforce) |

**Vai aparecer:**
- Um **QR Code** gigante
- Uma **chave secreta** (`Your new secret key is: XXXXX`)
- Cinco **emergency scratch codes** (recuperação)

> 🔐 **AGORA, sem fechar o terminal:**
> 1. Escaneie o QR Code com seu app de TOTP no celular
> 2. **Salve a chave secreta no Bitwarden** ("2FA SSH renato@pve - chave secreta")
> 3. **Salve TODOS os 5 códigos de recuperação no Bitwarden** ("2FA SSH renato@pve - recovery codes")
> 4. Confirme no app que o código de 6 dígitos está aparecendo

### 3.3 Configurar o PAM

```bash
sudo nano /etc/pam.d/sshd
```

Vá ao **final do arquivo** e adicione:

```
# 2FA TOTP via Google Authenticator
auth required pam_google_authenticator.so nullok
```

> **Tradução:**
> - `auth required` — etapa obrigatória de autenticação
> - `pam_google_authenticator.so` — módulo TOTP
> - `nullok` — permite logar sem 2FA configurado (temporário! removemos depois)

Salve e saia.

### 3.4 Exigir chave + 2FA via drop-in config

Edite o arquivo de hardening que criamos antes:

```bash
sudo nano /etc/ssh/sshd_config.d/99-hardening.conf
```

Adicione no final:

```
# 2FA TOTP - requer chave + código
KbdInteractiveAuthentication yes
AuthenticationMethods publickey,keyboard-interactive
```

> ⚠️ **CRÍTICO no Debian 13:** Use `KbdInteractiveAuthentication`. A diretiva antiga `ChallengeResponseAuthentication` foi **REMOVIDA** no OpenSSH 10 — vai dar erro se você usar.

> 🆘 **Bloqueado fora?** Consulta o **[Apêndice H](../fortaleza-proxmox-v5.0.md#apêndice-h--recuperação-de-desastre)** (Recuperação de desastre) — final do guia.

> **PARA AQUI — não apliques a nova config do `sshd` até confirmares o TOTP (evita ficar trancado fora)**  
> Com `AuthenticationMethods publickey,keyboard-interactive` ativo, um `sshd` mal alinhado com o PAM/TOTP pode **rejeitar** o login mesmo com chave correta. **Checklist obrigatório:**
> 1. Concluíste o §3.2 (`google-authenticator`) e o código de 6 dígitos **já aparece** no telemóvel?
> 2. O §3.3 está gravado em `/etc/pam.d/sshd` com `nullok` (ainda) na linha do `pam_google_authenticator`?
> 3. Mantém **esta** sessão SSH aberta e prepara **outra** janela de terminal (mesmo PC ou outro na LAN).

Valide a sintaxe e **aplica** a configuração (preferir `reload` para manter esta sessão; se falhar, `restart` sem fechar esta janela):

```bash
sudo sshd -t                   # Não deve retornar nada
sudo systemctl reload ssh || sudo systemctl restart ssh
```

> 4. **Na nova janela:** `ssh fortaleza` (ou `ssh -i ~/.ssh/chave_fortaleza renato@SEU_IP` se não usaste o §2.4) → deves ver `Verification code:` depois da autenticação por chave. Se **não** pedir código, o código falhar sempre, ou a ligação cair, **não** avances para o §3.5 nem removas o `nullok` — reverifica `/etc/pam.d/sshd`, o drop-in e `sudo sshd -T | grep -iE 'authenticationmethods|kbdinteractiveauthentication'`.

### ✅ Verifique

```bash
# Se configuraste o Host "fortaleza" no §2.4:
ssh fortaleza
# Senão: ssh -i ~/.ssh/chave_fortaleza renato@192.168.1.100   (troca o IP)
```

Deve aparecer:
```
Authenticated using "publickey".
(renato@192.168.1.100) Verification code:
```

Digite o código do app. Se entrou, ✅ 2FA ativo!

### 3.5 Remover o `nullok` (passo CRÍTICO de segurança)

⚠️ **Não pule este passo.** Sem ele, qualquer outro usuário (futuro) pode entrar sem 2FA.

Confirmado que funciona? Remova o `nullok`:

```bash
sudo nano /etc/pam.d/sshd
```

Mude:
```
auth required pam_google_authenticator.so nullok
```
para:
```
auth required pam_google_authenticator.so
```

```bash
sudo sshd -t
# Debian 13: unidade systemd = ssh (não sshd)
sudo systemctl reload ssh || sudo systemctl restart ssh
```

### 🆘 Se deu errado

**Erro:** Login não pede código TOTP, entra só com chave
**Causa:** `AuthenticationMethods` não foi aplicado.
**Solução:**
```bash
sudo sshd -T | grep authenticationmethods
# Deve mostrar: authenticationmethods publickey,keyboard-interactive
```

**Erro:** `Bad configuration option: ChallengeResponseAuthentication`
**Causa:** Você usou a diretiva antiga (removida no OpenSSH 10).
**Solução:** Remova essa diretiva do config. Use só `KbdInteractiveAuthentication yes`.

**Erro:** Código TOTP é rejeitado mesmo correto
**Causa:** Relógio dessincronizado (Fase 0 não foi feita direito).
**Solução:**
```bash
sudo timedatectl set-ntp true
sudo systemctl restart systemd-timesyncd
timedatectl status              # Confirme synchronized: yes
```

**Erro:** Perdi o celular
**Solução:** Use um dos 5 códigos de recuperação salvos no Bitwarden.

### 📝 Documente

```bash
echo "## $(date +"%F %H:%M") - Fase 3 concluída" >> ~/fortaleza-lab/diario.md
echo "- 2FA TOTP ativo no SSH, nullok removido" >> ~/fortaleza-lab/diario.md
```

---

# 🟢 FASE 4 — CrowdSec (Vigilante Inteligente)

🎯 **OBJETIVO:** Detectar ataques e banir IPs maliciosos automaticamente, usando inteligência coletiva global.
⏱ **Tempo estimado:** 30–45 min

📚 **FUNDAMENTO:** O CrowdSec compartilha dados entre milhares de servidores. Se um IP malicioso ataca outro servidor no mundo, ele chega banido no seu Mini PC.

### 📸 Snapshot

```bash
# No host Proxmox — dataset conforme §0.8 (ex.: rpool/ROOT/pve-1); renato com sudo
sudo zfs snapshot rpool/ROOT/pve-1@snap-pre-fase4
```

### 4.1 Instalar o CrowdSec

> **Cadeia de confiança:** o método oficial documentado começa por `curl -s https://install.crowdsec.net | sudo sh`. Se preferir não executar scripts remotos, siga [Manual Repository Installation](https://docs.crowdsec.net/u/getting_started/installation/linux/#manual-repository-installation) na documentação CrowdSec.

```bash
curl -s https://install.crowdsec.net | sudo sh
sudo apt update
sudo apt install crowdsec crowdsec-firewall-bouncer-nftables -y
```

> O pacote `crowdsec-firewall-bouncer-nftables` aplica decisões via **nftables** (adequado quando o host usa firewall nft). A doc de instalação Linux exemplifica muitas vezes o bouncer **iptables**; no Proxmox com `proxmox-firewall`, o variante nftables costuma ser o mais coerente. Em caso de dúvida, veja [Firewall bouncer](https://docs.crowdsec.net/u/bouncers/firewall).

**O que cada componente faz:**

- `crowdsec` — o "cérebro" que lê logs e detecta padrões  
- `crowdsec-firewall-bouncer-nftables` — o "braço" que bloqueia IPs via nftables

### 4.2 Whitelist (CRÍTICO para não se banir)

⚠️ **Sem whitelist, errar a senha algumas vezes te bana do seu próprio servidor.**

```bash
sudo nano /etc/crowdsec/parsers/s02-enrich/whitelists.yaml
```

> **Caminho do arquivo:** em versões recentes do CrowdSec a árvore sob `/etc/crowdsec/` pode diferir. Se o arquivo acima não existir, procure `whitelists` com `find /etc/crowdsec -name '*hitelist*' 2>/dev/null` ou consulte a documentação da sua versão (`cscli version`).

Cole exatamente:

```yaml
name: my_whitelist
description: "Trusted internal networks"
whitelist:
  reason: "Rede local e Tailscale são confiáveis"
  ip:
    - "127.0.0.1"
  cidr:
    - "192.168.1.0/24"   # Ajuste para sua rede (confira com 'ip addr')
    - "100.64.0.0/10"    # Faixa completa do Tailscale
```

> **Como descobrir sua faixa local:** `ip -4 addr show vmbr0` → procure `inet 192.168.X.X/24`. Use a rede (`192.168.X.0/24`).

```bash
sudo systemctl restart crowdsec
# Unidade do bouncer (pacote nftables): em Debian costuma ser crowdsec-firewall-bouncer
sudo systemctl enable --now crowdsec-firewall-bouncer
```

### ✅ Verifique

```bash
sudo systemctl status crowdsec --no-pager
sudo systemctl status crowdsec-firewall-bouncer --no-pager
# Ambos: Active: active (running)
```

```bash
sudo cscli bouncers list
# Saída esperada: tabela com cs-firewall-bouncer e status válido
```

```bash
sudo cscli collections list
# Saída esperada: coleções linux, sshd, etc.
```

```bash
sudo cscli decisions list
# Saída esperada: tabela (pode estar vazia ou com bans do feed comunitário)
```

**Confirmar que o nftables tem a chain do CrowdSec:**

```bash
sudo nft list ruleset | grep -i crowdsec
# Saída esperada: pelo menos uma linha mencionando 'crowdsec'
```

> **CrowdSec + `proxmox-firewall` (nftables):** o host pode ter **vários** consumidores de nftables ao mesmo tempo. Os nomes de tabela/chain do bouncer **mudam entre versões**. Se, após a Fase 7, bans ou comportamentos estranhos deixarem de bater com o esperado, inspecione o conjunto completo com `sudo nft list ruleset` e cruze com a [documentação do bouncer](https://docs.crowdsec.net/u/bouncers/firewall) e a [wiki Firewall](https://pve.proxmox.com/wiki/Firewall) — não assumas um único nome de chain fixo copiado da internet.

> **Prioridade das chains (ordem de processamento):** quando CrowdSec bane um IP e a PVE firewall tem uma regra ACCEPT para esse IP (ex.: regra LAN), qual prevalece? Em nftables, a prioridade é definida pelo número (`priority`) da chain — menor número = executado primeiro. O bouncer CrowdSec usa prioridade `0` (inet filter); o `proxmox-firewall` usa prioridades distintas. **Na prática:** a whitelist do CrowdSec em `/etc/crowdsec/parsers/s02-enrich/whitelists.yaml` impede que IPs da LAN (`192.168.1.0/24`) e Tailscale (`100.64.0.0/10`) sejam banidos — verifique sempre com `sudo cscli decisions list` se suspeitar de auto-ban. Para diagnóstico completo: `sudo nft list ruleset | grep -E 'priority|chain'`.

### 4.3 (Opcional) Conectar ao CrowdSec Console

Para ter um dashboard web bonito:

1. Crie conta gratuita em `https://app.crowdsec.net`
2. Obtenha o enrollment token
3. Execute:
```bash
sudo cscli console enroll <SEU_TOKEN>
sudo systemctl reload crowdsec
```
4. Confirme o device no dashboard web.

### 🆘 Se deu errado

**Erro:** `cscli: command not found`
**Solução:** Instalação não completou. Repita 4.1.

**Erro:** Bouncer com `valid: false`
**Solução:**
```bash
sudo apt reinstall crowdsec-firewall-bouncer-nftables
sudo systemctl restart crowdsec-firewall-bouncer
```

**Erro:** Você foi banido por engano
> 🆘 **Bloqueado fora do servidor?** Consulta o **Apêndice H** (Recuperação de desastre) — especialmente o "Cenário 4: Me banni acidentalmente no CrowdSec".
**Solução:**
```bash
sudo cscli decisions list                          # ver IPs banidos
sudo cscli decisions delete --ip SEU_IP            # remover ban específico
sudo cscli decisions delete --all                  # emergência: remover TODOS
```

### 📝 Documente

```bash
echo "## $(date +"%F %H:%M") - Fase 4 concluída" >> ~/fortaleza-lab/diario.md
echo "- CrowdSec + bouncer nftables ativo" >> ~/fortaleza-lab/diario.md
```

---

# 🟢 FASE 5 — Acesso Invisível (Tailscale em LXC)

🎯 **OBJETIVO:** Acessar o Proxmox de qualquer lugar do mundo, sem abrir uma única porta no roteador.
⏱ **Tempo estimado:** 30–45 min

📚 **FUNDAMENTO:** Em vez de "ouvir" conexões da internet (alvo de scanners 24/7), seu servidor faz o caminho contrário: cria um túnel criptografado de SAÍDA até o Tailscale. Vocês se encontram numa "rede privada virtual" que ninguém de fora consegue ver.

### 📸 Snapshot

```bash
# No host Proxmox — mesmo dataset que nas outras fases; renato com sudo
sudo zfs snapshot rpool/ROOT/pve-1@snap-pre-fase5
```

### 5.1 Baixar o template Debian 13

No painel web:
1. Árvore lateral → `local (pve)`
2. Aba **CT Templates** → **Templates**
3. Procure `debian-13-standard` → **Download**

### 5.2 Criar o Container LXC

**Create CT** (canto superior direito):

| Aba | Campo | Valor |
|-----|-------|-------|
| General | CT ID | `100` |
| General | Hostname | `vpn-tailscale` |
| General | Password | (senha forte, guarde no Bitwarden como "CT 100 root") |
| General | SSH key | (cole sua chave pública aqui) |
| Template | Template | `debian-13-standard_13.x...` |
| Disks | Disk size | `4` (GB) |
| CPU | Cores | `1` |
| Memory | Memory | `512` (MB) — ⚠️ não use 256 |
| Memory | Swap | `512` (MB) |
| Network | IPv4 | `Static` |
| Network | IPv4/CIDR | `192.168.1.110/24` |
| Network | Gateway | `192.168.1.1` |
| Network | DNS | `1.1.1.1 8.8.8.8` |
| Confirm | Start after created | ✅ |

> 🔍 **Por que IP estático no container?** Para você poder criar regras de firewall específicas depois.

### 5.3 Habilitar TUN e features (método moderno via CLI)

⚠️ **Etapa crítica.** Sem isso, o Tailscale **NÃO** funciona em LXC unprivileged.

No terminal SSH do **Proxmox host** (como renato com sudo):

```bash
# Para o container primeiro
sudo pct stop 100

# Habilita keyctl e nesting (necessários para Tailscale)
sudo pct set 100 --features keyctl=1,nesting=1

# Passa o device /dev/net/tun para o container (método moderno)
sudo pct set 100 --dev0 /dev/net/tun

# Inicia o container
sudo pct start 100
```

> 📚 **O que isso faz:**
> - `keyctl=1` — permite chamadas de sistema para retenção de chaves do kernel
> - `nesting=1` — expõe procfs/sysfs do host (necessário para namespaces aninhados)
> - `--dev0 /dev/net/tun` — passa o dispositivo TUN do host para dentro do container, permitindo modo kernel do Tailscale (sem isso, ele cairia em modo userspace, que tem desempenho ruim)

### 5.4 Instalar o Tailscale dentro do container

Abra o **Console** do CT 100 (`>_ Console` no topo), logue como root:

Antes de instalar o Tailscale, confirme **rede e DNS** dentro do CT (sem isso, `curl`/`install.sh` falham sem diagnóstico claro):

```bash
ping -c 2 1.1.1.1 && echo "Rede IP OK" || echo "Sem reachability IP — verifique gateway/IP estático do CT no Proxmox"
ping -c 1 -W 3 tailscale.com && echo "Resolução DNS OK (tailscale.com)" || echo "Falhou ICMP ou DNS — confira /etc/resolv.conf; se o ping falhar mas a rede estiver OK, teste: curl -fsSI --max-time 5 https://tailscale.com/ | head -n1"
```

```bash
apt update && apt install curl -y
# Cadeia de confiança: o script oficial de instalação é remoto — reveja https://tailscale.com/install.sh se quiser auditar antes.
curl -fsSL https://tailscale.com/install.sh | sh
```

Verifique se o TUN está acessível dentro do CT:

```bash
ls -l /dev/net/tun
# Deve mostrar: crw-rw-rw- 1 nobody nogroup 10, 200 ...
```

### 5.4b Subnet router — encaminhamento IP no CT

Para o Linux **encaminhar** tráfego entre `tailscale0` e a LAN (`192.168.1.x`), o kernel do CT precisa de `ip_forward` ativo. Isto é **dentro do CT 100** (console como root), não no host Proxmox.

> O comando `tailscale up --advertise-routes=...` **aceita sem erro** mesmo com forwarding em `0` — o sintoma é subnet aprovada no admin e **mesmo assim** tráfego que não roteia. Em clientes Tailscale recentes no Debian, o instalador ou o próprio serviço **podem** criar `/etc/sysctl.d/99-tailscale.conf` com forwarding; **não assuma**: confirme no seu CT após o primeiro `tailscale up`. Ver [Subnet routers](https://tailscale.com/kb/1019/subnets/).

Inicie o Tailscale anunciando a rede local como subnet:

```bash
tailscale up --advertise-routes=192.168.1.0/24 --accept-routes
```

> **Tradução:**
> - `--advertise-routes=192.168.1.0/24` — anuncia "eu sei chegar nessa rede" (permite que seus dispositivos cheguem ao IP local do Proxmox via Tailscale)
> - `--accept-routes` — aceita rotas anunciadas por outros peers

Vai aparecer um link `https://login.tailscale.com/a/...`. Abra no navegador, autentique (Google, GitHub, etc.).

Depois de autenticado, **ainda no CT**, verifica se o forwarding já ficou ativo:

```bash
sysctl net.ipv4.ip_forward net.ipv6.conf.all.forwarding
```

- Se `net.ipv4.ip_forward = 1` (e `net.ipv6.conf.all.forwarding = 1` se precisar de IPv6 na rota), **não** precisa do bloco manual abaixo — o Tailscale ou o sistema já aplicaram.
- Se `net.ipv4.ip_forward` for **0**, aplica manualmente (arquivo separado para não sobrescrever um `99-tailscale.conf` eventualmente criado pelo cliente):

```bash
echo 'net.ipv4.ip_forward = 1' | tee /etc/sysctl.d/99-fortaleza-tailscale-forward.conf
echo 'net.ipv6.conf.all.forwarding = 1' | tee -a /etc/sysctl.d/99-fortaleza-tailscale-forward.conf
sysctl -p /etc/sysctl.d/99-fortaleza-tailscale-forward.conf
```

### 5.5 Aprovar a subnet route

`https://login.tailscale.com/admin/machines`:
1. Encontre `vpn-tailscale`
2. **⋯ → Edit route settings**
3. Marque ✅ `192.168.1.0/24`
4. **Save**

### 5.6 Tailscale no seu PC e celular

- **Windows/macOS/Linux:** https://tailscale.com/download
- **Android/iOS:** Play Store / App Store
- Logue com a **mesma conta**

### 5.6b Termius no Android/iOS via 4G (acesso SSH pelo celular)

O Termius é um cliente SSH popular para Android e iOS. Para usá-lo em 4G sem expor o servidor à internet:

**Pré-requisito:** Tailscale instalado no celular (passo acima).

```bash
# No nó PVE — descobrir o IP Tailscale do servidor:
sudo pct exec 100 -- tailscale ip -4
# Exemplo de saída: 100.84.23.115  ← este é o IP que o Termius vai usar
```

**No Termius (celular):**
1. Adicionar novo Host
2. **Hostname:** `100.84.23.115` (o IP Tailscale do servidor, não o IP da LAN)
3. **Port:** `22`
4. **Username:** `renato`
5. **Auth:** Key — importe a chave privada `chave_fortaleza` (transfira via AirDrop, e-mail cifrado, ou Bitwarden Attachment)
6. Conectar → pede `Verification code:` (TOTP) → digitar código do app

> **Por que IP Tailscale e não IP público?** O guia remove port forwarding do router (§7.5) — o IP público da sua casa **não tem porta 22 aberta**. O Tailscale cria um túnel WireGuard direto entre o celular e o CT 100, funcionando em qualquer rede (4G, Wi-Fi de café, hotel) sem expor nada à internet.

**Fluxo completo pelo celular em 4G:**
```
Termius (celular 4G)
    → WireGuard (Tailscale) — cifrado, peer-to-peer
        → CT 100 (Tailscale LXC) — subnet routing
            → host PVE porta 22
                → chave SSH + TOTP
```

---

### 5.6c ⚠️ Tailscale SSH vs SSH regular — não confunda

O Tailscale tem uma funcionalidade chamada **Tailscale SSH** (configurável no Admin Console em `tailscale.com/admin`). Se ativada, ela **substitui** o OpenSSH no dispositivo e gere a autenticação pela identidade Tailscale — **bypassando completamente o TOTP e a chave SSH** configurados nas Fases 2–3.

**Nunca ative "Tailscale SSH" no Admin Console para o nó PVE.** O guia usa SSH regular (OpenSSH) *tunnelado através da rede Tailscale* — são coisas distintas:

| | SSH regular via Tailscale | Tailscale SSH |
|--|--------------------------|---------------|
| Auth | Chave Ed25519 + TOTP (Fases 2–3) | Identidade Tailscale (OAuth) |
| Porta | 22 no OpenSSH | Gerido pelo Tailscale daemon |
| 2FA | ✅ TOTP obrigatório | ❌ Bypassa o TOTP |
| Controlo | Você controla | Tailscale controla |

Confirme que Tailscale SSH está **desligado** no Admin Console:
`tailscale.com/admin` → Machines → seu servidor → SSH → **Off**

---

### ✅ Verifique

No console do CT 100:
```bash
tailscale status                 # Lista de peers conectados
tailscale ip                     # IP da VPN (100.x.x.x)

# Confirmar que está em modo kernel (não userspace):
ip addr show tailscale0
# Deve existir interface tailscale0 com IP 100.x.x.x
```

> Se **`tailscale0` não existir**, o TUN/capabilities podem estar incompletos — reveja a Fase 5 (`pct set`, device passthrough) ou a doc [Tailscale em LXC](https://tailscale.com/docs/features/containers/lxc/lxc-unprivileged) (modo userspace só como último recurso, com pior desempenho típico).

No seu PC/celular (Tailscale ativo):
```
https://192.168.1.100:8006
```
Deve carregar o painel mesmo via 4G.

### 🆘 Se deu errado

**Erro:** `tstun.New("tailscale0"): operation not permitted`
**Causa:** Features e/ou device TUN não habilitados.
**Solução:** Repita `sudo pct set 100 --dev0 /dev/net/tun` com container parado.

**Erro:** Conecta no Tailscale mas não enxerga `192.168.1.100`
**Causa:** Subnet route não aprovada, `sysctl` ainda em `0` após `tailscale up`, ou firewall.
**Solução:** Passo 5.5; em 5.4b confirma `sysctl net.ipv4.ip_forward` e aplica o bloco manual se for `0`.

### 📝 Documente

```bash
echo "## $(date +"%F %H:%M") - Fase 5 concluída" >> ~/fortaleza-lab/diario.md
echo "- CT 100 vpn-tailscale ativo com subnet routing" >> ~/fortaleza-lab/diario.md
echo "- IP Tailscale (IPv4) do CT 100: $(sudo pct exec 100 -- tailscale ip -4)" >> ~/fortaleza-lab/diario.md
```

---

# 🟢 FASE 6 — 2FA no Painel Web do Proxmox

🎯 **OBJETIVO:** Criar `renato@pam` como administrador com 2FA, nunca mais usar `root@pam` na interface.
⏱ **Tempo estimado:** 15–20 min

📚 **FUNDAMENTO:** O painel web tem dois "realms":
- `pam` — usuários do sistema Linux
- `pve` — usuários internos do Proxmox

Vamos usar `pam`. **O 2FA do painel é separado do 2FA do SSH** — tem que configurar de novo.

### 📸 Snapshot (recomendado)

```bash
# No host Proxmox — dataset conforme §0.8; renato com sudo
sudo zfs snapshot rpool/ROOT/pve-1@snap-pre-fase6
```

### ⚙️ Passo a passo

Acesse `https://192.168.1.100:8006` (via Tailscale ou rede local) e logue como **root@pam** pela última vez.

**1. Criar o usuário no Proxmox:**
- **Datacenter → Permissions → Users → Add**
- User name: `renato`
- Realm: `Linux PAM standard authentication`
- Enabled: ✅
- **Add**

**2. Dar Administrator:**
- **Datacenter → Permissions → Add → User Permission**
- Path: `/`
- User: `renato@pam`
- Role: `Administrator`
- Propagate: ✅
- **Add**

**3. Sair e entrar como renato@pam:**
- **Logout**
- User: `renato`, Realm: `Linux PAM`, Password: (a do renato)

**4. Ativar TOTP:**
- Canto superior direito (`renato@pam`) → **TFA**
- **Add → TOTP**
- Description: `Celular Renato`
- Escaneie o QR Code com o app
- Digite o código de 6 dígitos
- **Add**

> 🔐 **Salve no Bitwarden:**
> - QR code / chave secreta
> - "2FA painel Proxmox - renato@pam"

**5. Adicionar Recovery Keys (importante!):**
- **Add → Recovery Keys**
- Salve TODAS no Bitwarden

### ✅ Verifique

Logout e logue como `renato@pam`. Deve pedir senha + código TOTP.

### 📝 Documente

```bash
echo "## $(date +"%F %H:%M") - Fase 6 concluída" >> ~/fortaleza-lab/diario.md
echo "- renato@pam Administrator com 2FA TOTP" >> ~/fortaleza-lab/diario.md
```

---

# 🟢 FASE 7 — Firewall nftables (proxmox-firewall)

🎯 **OBJETIVO:** Migrar para o backend `nftables` moderno do Proxmox 9 e fazer o servidor "sumir" da internet.
⏱ **Tempo estimado:** 30–45 min

📚 **FUNDAMENTO:** O Proxmox VE 9 oferece **proxmox-firewall**, implementação do mesmo modelo de regras da GUI mas sobre **nftables** (em alternativa ao serviço clássico baseado em iptables). A [wiki oficial](https://pve.proxmox.com/wiki/Firewall#nftables) classifica o **nftables backend** como *tech preview*: pode haver bugs ou diferenças face ao firewall “stock”; **não é descrita como adequada para produção** na documentação (homelab com backups e consciência do risco é outra história). Vantagens citadas na wiki: melhor desempenho, regras **forward** e regras a nível de VNet em SDN — funcionalidades ignoradas pelo `pve-firewall` clássico.

### 📸 Snapshot e backup

```bash
# No host Proxmox — dataset conforme §0.8; renato com sudo
sudo zfs snapshot rpool/ROOT/pve-1@snap-pre-fase7
sudo tar czf /root/backups/etc-pve-fase7-$(date +%F).tar.gz /etc/pve/
```

### 7.1 Instalar o pacote proxmox-firewall

```bash
sudo apt install proxmox-firewall -y
```

> Geralmente já vem instalado no PVE 9.x, mas garantia não faz mal.

### 7.2 Criar regras de ACCEPT (ANTES de habilitar DROP)

⚠️ **SEMPRE crie ACCEPT antes de mudar para DROP, senão você se tranca fora.**

**Datacenter → Firewall → Rules → Add** — crie estas 6 regras:

| Direction | Action | Source | Dest. port | Protocol | Comment |
|-----------|--------|--------|------------|----------|---------|
| in | ACCEPT | `100.64.0.0/10` | `22` | tcp | SSH via Tailscale |
| in | ACCEPT | `100.64.0.0/10` | `8006` | tcp | Web GUI via Tailscale |
| in | ACCEPT | `192.168.1.0/24` | `22` | tcp | SSH rede local (emergência) |
| in | ACCEPT | `192.168.1.0/24` | `8006` | tcp | Web GUI rede local (emergência) |
| in | ACCEPT | `100.64.0.0/10` | — | icmp | Ping via Tailscale (diagnóstico VPN) |
| in | ACCEPT | `192.168.1.0/24` | — | icmp | Ping rede local (diagnóstico LAN) |

✅ Marque **Enable** em cada regra.

> **Por que ICMP explícito?** A política DROP já bloqueia ping da internet — o servidor fica invisível para scanners externos. Mas sem as duas regras ICMP acima, o servidor também fica invisível para **você** na LAN e no Tailscale, o que complica o diagnóstico ("o servidor está vivo?"). Com essas regras: `ping 192.168.1.100` do seu PC funciona; `ping fortaleza` via Tailscale funciona; `ping IP_PUBLICO` da internet → timeout (host não existe para o mundo).

### 7.3 Habilitar o firewall

**Datacenter → Firewall → Options → Edit:**
- Firewall: **Yes**
- Input Policy: **DROP**
- Output Policy: **ACCEPT**
- Log level in: **info**
- Log level out: **nolog**

**No nível do Nó:** `pve → Firewall → Options → Edit:`
- Firewall: **Yes**

### 7.4 Migrar para o backend nftables

📚 **FUNDAMENTO:** Por padrão, o nó pode ainda usar o serviço clássico (`pve-firewall`, iptables). Ativar **nftables: Yes** no host passa o trabalho para o serviço `proxmox-firewall`.

**No painel:** `pve (seu nó) → Firewall → Options → Edit:`
- nftables: **Yes**

> A interface pode mostrar *tech preview* — coincide com a [documentação Proxmox](https://pve.proxmox.com/wiki/Firewall#nftables). Depois de alternar o backend, a wiki recomenda **reiniciar todas as VMs e CTs** para o novo firewall atuar de forma consistente; planeje uma janela curta de manutenção.

### ✅ Verifique

```bash
sudo systemctl status proxmox-firewall --no-pager
# Saída esperada: active (running)
```

```bash
sudo nft list tables
# Deve aparecer, entre outras possíveis:
# table inet proxmox-firewall        ← backend do PVE (nftables)
# table bridge proxmox-firewall-guests
# ... e uma tabela do bouncer CrowdSec (nome típico: contém "crowdsec" — ex.: table inet crowdsec)
```

Se a tabela do CrowdSec **não** aparecer mas a Fase 4 já instalou o bouncer nftables:

```bash
sudo systemctl status crowdsec-firewall-bouncer --no-pager
sudo systemctl restart crowdsec-firewall-bouncer
sudo nft list tables
```

```bash
sudo nft list ruleset | head -50
# Inspeção do ruleset ativo
```

Confirmar que o firewall clássico **não** está a empilhar regras iptables quando esperas só nftables:

```bash
systemctl is-active pve-firewall
```

> **Ler o estado:** com **nftables: Yes** e `proxmox-firewall` a tratar do host, o serviço `pve-firewall` pode aparecer como `inactive` (esperado) **ou** `active` em algumas versões/configurações sem isso significar que ainda está no backend iptables clássico. O sinal mais útil para “ainda há regras estilo pve-firewall em iptables” são **cadeias PVEFW** em `iptables -L`. Cruza sempre com `sudo systemctl status proxmox-firewall` e a [wiki Firewall](https://pve.proxmox.com/wiki/Firewall).

Se `iptables` existir no host:

```bash
if sudo iptables -L 2>/dev/null | grep -q "PVEFW"; then
  echo "ATENÇÃO: PVEFW detectado — o pve-firewall clássico ainda pode estar a gerar regras iptables."
  echo "          Confirma: systemctl is-active pve-firewall && sudo systemctl status proxmox-firewall --no-pager"
else
  echo "OK: sem chains PVEFW visíveis em iptables (ou iptables vazio / não usado neste nó)."
fi
```

> Em hosts **só nftables**, `iptables -L` pode estar vazio ou mapear para nft — o objectivo é não ficar com **duas** camadas de firewall por engano; se vires PVEFW massivo enquanto esperas nft-only, investiga antes de declarar a fase fechada.

**Teste de conectividade:**

```bash
# Do seu PC (com Tailscale):
ssh fortaleza                 # → deve funcionar (se configuraste Host no §2.4)
# Senão: ssh -i ~/.ssh/chave_fortaleza renato@192.168.1.100

# Do seu PC (na rede local):
ssh renato@192.168.1.100      # → deve funcionar (troca o IP se o seu nó for outro)

# Do celular no 4G (sem Tailscale):
# Tente acessar IP_PUBLICO_CASA porta 22 → deve dar timeout
```

### 7.5 Fechar port forwarding no roteador

No painel do roteador, remova qualquer:
- Port Forwarding / NAT
- DMZ
- UPnP apontando para o Mini PC

Especialmente as portas 22 e 8006.

### 🆘 Se deu errado

**Erro:** Você se trancou fora
> 🆘 **Bloqueado fora?** Consulte o **Apêndice H** → "Cenário 5: Firewall me trancou fora".
**Solução imediata:** Console físico ou web:
```bash
# Parar TODOS os firewalls
sudo systemctl stop proxmox-firewall
sudo systemctl stop pve-firewall
sudo pve-firewall stop
```
Edite como root (ex.: `sudo nano /etc/pve/firewall/cluster.fw`), mude `enable: 1` para `enable: 0` na seção `[OPTIONS]`. Reinicie o serviço quando corrigir as regras.

**Erro:** `proxmox-firewall.service: failed`
**Solução:**
```bash
sudo journalctl -u proxmox-firewall -n 50 --no-pager
# Veja os erros e corrija as regras inválidas
# Acompanhar em tempo real (Ctrl+C para sair):
sudo journalctl -u proxmox-firewall -f
```

### 7.6 Verificar invisibilidade — o teste do ping

Com a política DROP e as 6 regras acima, o comportamento esperado é:

| De onde | Para onde | Resultado esperado |
|---------|-----------|-------------------|
| Seu PC (LAN 192.168.1.x) | `ping 192.168.1.100` | ✅ Responde (regra ICMP LAN) |
| Tailscale client | `ping fortaleza` (100.x.x.x) | ✅ Responde (regra ICMP Tailscale) |
| Celular no **4G** (internet) | `ping IP_PUBLICO` | ❌ Timeout — host invisível |
| Qualquer scanner externo | porta 22, 8006, qualquer ICMP | ❌ DROP — host não existe |

```bash
# Confirmar as regras ICMP estão activas (no nó PVE):
sudo nft list ruleset | grep -A3 icmp
# Deve aparecer bloco com "icmp" e "accept" para as duas sub-redes

# Testar da LAN (no seu PC):
ping -c 3 192.168.1.100   # deve responder

# Testar via Tailscale (no seu PC com Tailscale ativo):
ping -c 3 fortaleza        # deve responder (se hostname configurado)

# Simular internet (da LAN sem Tailscale — via porta pública):
# Peça a alguém noutra rede fazer: ping IP_PUBLICO_DA_SUA_CASA
# Ou use: https://ping.eu/ → deve mostrar "timeout" ou "100% packet loss"
```

> **Resumo:** o servidor é **invisível para a internet** (DROP tudo por omissão, sem ICMP externo) e **visível para você** na LAN e no Tailscale. ShellHub e Tailscale funcionam porque **eles é que fazem a conexão de saída** — não dependem de portas abertas no roteador.

---

### 7.7 Port Knocking — por que este guia não o usa (e não precisa)

**O que é Port Knocking:** uma técnica em que a porta SSH fica fechada no firewall e só abre temporariamente se receber uma sequência secreta de pacotes (ex.: tentar porta 1111, 2222, 3333 em ordem). Contra `nmap`, a porta 22 aparece como `filtered` ou `closed` mesmo com o serviço ativo.

**Por que é incompatível com este setup:**

Port Knocking só faz sentido quando a porta 22 **está exposta à internet** — o router tem port forwarding ativo e o firewall filtra (não a NAT). O knock sequence "abre" a porta para o IP do atacante.

Neste guia:
- §7.5 remove **todo** o port forwarding do router
- O servidor está atrás de NAT sem qualquer forwarding para porta 22
- A política DROP bloqueia tudo — mas o router já descarta antes de chegar ao servidor

**Resultado:** a sequência de knock nunca chegaria ao servidor. Os pacotes morrem no router da operadora.

**O que já temos que é melhor que Port Knocking:**

| Técnica | Protege contra nmap? | Criptografia real? | Complexidade |
|---------|---------------------|-------------------|-------------|
| Port Knocking | ✅ Sim | ❌ Não (cleartext) | Média |
| **Tailscale (este guia)** | ✅ Sim (porta nem existe) | ✅ WireGuard | Baixa |

- Port Knocking = obscuridade (sequência em cleartext, capturável por sniffer do ISP)
- Tailscale = criptografia real (WireGuard, chave pública, sem porta exposta)

**Quando Port Knocking FAZ sentido:** em servidores sem VPN onde a porta 22 *precisa* estar exposta à internet por outros requisitos. Não é o caso aqui.

> **Conclusão:** não implemente Port Knocking neste setup — é redundante, provavelmente não funcionaria, e adiciona complexidade desnecessária. O Tailscale já resolve o problema de forma superior.

---

### 7.8 Os três níveis do firewall PVE — entendendo a hierarquia

O PVE Firewall opera em **três camadas independentes**. Entender a hierarquia evita confusões de "habilitei a regra mas não funcionou":

| Nível | Onde configurar | O que protege | Herança |
|-------|----------------|---------------|---------|
| **Datacenter** | Datacenter → Firewall | Todos os nós do cluster (regras globais) | Base — aplicada primeiro |
| **Nó (host)** | Nó → Firewall | Apenas o host PVE (eth0, vmbr0) | Herda Datacenter + regras próprias |
| **VM / CT** | VM/CT → Firewall | Apenas aquela instância (vNIC) | Herda Datacenter + regras próprias |

> **Como a hierarquia funciona:** regras do Datacenter se aplicam a todos. O nó pode ter regras extras que não afetam VMs. Cada VM/CT tem sua própria chain — se o firewall da VM está desligado, o tráfego passa mesmo que o nó esteja em DROP.

#### Security Groups — criar uma vez, aplicar em muitas VMs

Em vez de copiar regras manualmente para cada VM, use **Security Groups**:

1. **Datacenter → Firewall → Security Groups → Create** → nome: `allow-ssh-tailscale`
2. Adicione a regra: `IN ACCEPT -source 100.64.0.0/10 -p tcp --dport 22`
3. Para aplicar em qualquer VM: **VM → Firewall → Security Groups → Add** → selecione `allow-ssh-tailscale`

Agora ao atualizar a regra no grupo, todas as VMs que o usam herdam a atualização automaticamente.

#### Princípio "Keep the Host Lean"

> Nunca instale serviços (nginx, databases, apps) diretamente no host PVE. O host deve executar **apenas** o que o Proxmox precisa. Cada serviço vai num CT ou VM isolado.

**Por quê:**
- Uma vulnerabilidade num serviço no host compromete **todo o hypervisor** (e todas as VMs)
- CTs/VMs têm isolamento de namespace — um ataque fica contido
- Mais fácil de fazer backup, migrar e destruir um CT do que "desfazer" uma instalação no host

#### SDN — diretiva de compatibilidade

Se você usar SDN (Software Defined Networking) do Proxmox, o arquivo `/etc/network/interfaces` precisa desta linha para carregar a configuração:

```bash
# /etc/network/interfaces — adicionar ao final se usar SDN:
source /etc/network/interfaces.d/sdn
# Sem esta linha, as bridges SDN não sobrevivem a um reboot.
```

---

### 📝 Documente

```bash
echo "## $(date +"%F %H:%M") - Fase 7 concluída" >> ~/fortaleza-lab/diario.md
echo "- Firewall nftables com DROP, 6 regras ACCEPT (SSH, GUI, ICMP para LAN e Tailscale)" >> ~/fortaleza-lab/diario.md
echo "- Host invisível para internet, visível na LAN e Tailscale" >> ~/fortaleza-lab/diario.md
echo "- Port forwarding removido do roteador" >> ~/fortaleza-lab/diario.md
```

---

# 🟢 FASE 8 — Laboratório do Irmão (ShellHub + GPG)

🎯 **OBJETIVO:** Container (LXC) isolado para o irmão estudar GPG, sem expor sua rede e sem entregar acesso ao lab.
⏱ **Tempo estimado:** 60–90 min

📚 **FUNDAMENTO:** ShellHub usa **túnel reverso via Docker**. O CT do irmão "liga" para o ShellHub na nuvem. Quando ele se conecta, o tráfego escorrega pelo túnel até cair no container. Você não abre porta nenhuma.

> ⚠️ **O método oficial do ShellHub Agent requer Docker.** Por isso vamos habilitar `nesting=1` e instalar Docker no LXC. **Nota:** Docker dentro de LXC usa namespaces aninhados — mais overhead que um CT “só Debian”; para **laboratório isolado** (como o do irmão) é aceitável; não é o padrão típico de produção.

### 📸 Snapshot

```bash
# No host Proxmox — dataset conforme §0.8; renato com sudo
sudo zfs snapshot rpool/ROOT/pve-1@snap-pre-fase8
```

### 8.1 Criar o LXC

**Create CT:**

| Campo | Valor |
|-------|-------|
| CT ID | `200` |
| Hostname | `lab-irmao-gpg` |
| Password | (senha forte do root, Bitwarden) |
| Template | `debian-13-standard...` |
| Disk | `10 GB` |
| Cores | `1` |
| Memory | `1024 MB` |
| Swap | `512 MB` |
| Network | IPv4 Static `192.168.1.120/24`, Gateway `192.168.1.1`, DNS `1.1.1.1` |
| Tags | `lab`, `irmao` |
| Unprivileged | ✅ |

### 8.2 Habilitar features para Docker rodar dentro

```bash
sudo pct stop 200
sudo pct set 200 --features keyctl=1,nesting=1
sudo pct start 200
```

### 8.3 Hardening básico dentro do container

Console do CT 200, logado como root:

```bash
apt update && apt full-upgrade -y
apt install sudo gnupg curl nano ca-certificates -y

# Criar usuário do irmão
adduser irmao
usermod -aG sudo irmao
```

### 8.4 Instalar Docker no container

```bash
# Cadeia de confiança: script remoto da Docker Inc. — alternativa: instalar docker.io dos repos Debian, se preferir pacote só Debian.
curl -fsSL https://get.docker.com | sh
systemctl enable --now docker
docker --version
docker run hello-world
```

### 8.5 Registrar o device no ShellHub Cloud

1. Crie conta gratuita em **https://cloud.shellhub.io**
2. Painel: **Devices → Add Device**
3. Copie o comando de instalação (envolve `curl`/`install.sh` da ShellHub). Confira o procedimento atual em [ShellHub Documentation](https://docs.shellhub.io/).
4. Cole no console do CT 200
5. Volte ao painel ShellHub → device em **Pending** → **Accept**

### 8.6 Como o irmão acessa

No painel ShellHub, **Connect** ao lado do device:

```
ssh irmao@SSHID.shellhub.io
```

Mande esse comando para o irmão. Ele cola no terminal dele e cai direto no CT (console ShellHub).

### 8.7 Bônus pedagógico — GPG na prática

Primeiro exercício para ele:

```bash
# No CT dele (como irmao)
gpg --full-generate-key
# Os números de menu variam com a versão do GnuPG — escolha ECC (preferencialmente Curve25519 / Ed25519) se existir.
# Exemplo típico (GnuPG 2.2.x): tipo 9 (ECC sign and encrypt) → curva 1 (Curve25519); validade: 1y; nome e email dele.

gpg --armor --export irmao@email.com > irmao.pub
cat irmao.pub
```

Ele te manda o bloco. Você importa:

```bash
nano irmao.pub      # Cole o conteúdo
gpg --import irmao.pub
gpg --list-keys
```

Criptografa uma mensagem:

```bash
echo "Bem-vindo ao lab, mano!" | gpg --encrypt --armor -r irmao@email.com > msg.asc
cat msg.asc
```

Ele cola e descriptografa:

```bash
nano msg.asc        # cola, salva, sai
gpg --decrypt msg.asc
```

🎉 **Criptografia assimétrica aplicada na prática.**

### 8.8 ShellHub como acesso de emergência pessoal (bônus)

O CT 200 foi criado para o "irmão" — mas ShellHub também pode ser **o seu canal de último recurso** se o Tailscale falhar ou ficar sem o app de TOTP.

**Opção A — usar o CT 200 do irmão como acesso de emergência:**
```bash
# No painel ShellHub Cloud (app.shellhub.io):
# Connect ao CT 200 → você cai numa shell Debian dentro do CT
# De lá, pode fazer SSH para o host PVE pela LAN interna:
ssh renato@192.168.1.100   # funciona porque CT está na mesma rede que o host
```

**Opção B — instalar agente ShellHub directamente no host PVE (avançado):**
```bash
# Cria um usuário de emergência no host (sem sudo completo):
sudo adduser shellhub-rescue
# Instala o ShellHub agent no host — siga os passos do §8.5 mas no host PVE
# Usa shell ShellHub → sudo su - renato  (ou acede directamente como rescue)
```

> **Quando usar:** Tailscale CT 100 caiu, app 2FA perdido, PC sem acesso à LAN. ShellHub Cloud é o "arrombador" — acesso via browser/Termius através da cloud ShellHub sem depender da sua rede local.

> **Segurança:** ShellHub protege com credenciais da conta ShellHub Cloud (2FA disponível no app.shellhub.io). Tratar com o mesmo cuidado que o Tailscale.

### 📝 Documente

```bash
echo "## $(date +"%F %H:%M") - Fase 8 concluída" >> ~/fortaleza-lab/diario.md
echo "- CT 200 lab-irmao-gpg com Docker + ShellHub agent" >> ~/fortaleza-lab/diario.md
echo "- ShellHub Cloud pode ser usado como canal de emergência pessoal" >> ~/fortaleza-lab/diario.md
```

---

# 🟢 FASE 9 — Manutenção Automática

🎯 **OBJETIVO:** Atualizações de segurança automáticas + observabilidade.
⏱ **Tempo estimado:** 20–30 min

### 📸 Snapshot (recomendado)

```bash
# No host Proxmox — dataset conforme §0.8; renato com sudo
sudo zfs snapshot rpool/ROOT/pve-1@snap-pre-fase9
```

### 9.1 Atualizações automáticas (Proxmox host)

```bash
sudo apt install unattended-upgrades needrestart apt-listchanges -y
sudo dpkg-reconfigure --priority=low unattended-upgrades
# Responda: Yes
```

Verifique o que será atualizado:

```bash
grep -A 12 'Unattended-Upgrade::Allowed-Origins' /etc/apt/apt.conf.d/50unattended-upgrades
# Procure por origens de segurança (ex.: ...-security ou Debian-Security) sem estar comentadas.
# Em algumas instalações o arquivo usa sobretudo Origins-Pattern — veja a wiki Debian UnattendedUpgrades se este grep não mostrar o esperado.
```

### 9.1b `needrestart` e desconexão SSH (leia antes de reclamar do `unattended-upgrades`)

O pacote **needrestart** (instalado na seção anterior) detecta daemons que precisam de reinício após atualização de bibliotecas. No arquivo de exemplo [upstream](https://github.com/liske/needrestart/blob/master/ex/needrestart.conf), o modo de reinício é: **`l`** = só listar, **`i`** = interativo, **`a`** = **reinício automático**. Em ambientes **não interativos** (como o hook do `unattended-upgrades`), o modo interativo pode fazer **fallback** para “só listar” — ou seja, **não** confunda definir o modo **a** (automático) com “evitar surpresas”: o modo **a** pode **reiniciar serviços sem perguntar**, o que em acesso remoto pode ser **pior** se não souber o que vai ser tocado.

**Recomendações práticas (homelab com SSH remoto):**

- Trate janelas de `full-upgrade` / reinícios como **manutenção**: duas sessões SSH, ou console física.  
- Leia a documentação Debian sobre [UnattendedUpgrades](https://wiki.debian.org/UnattendedUpgrades) e o projeto [needrestart](https://github.com/liske/needrestart) antes de alterar `/etc/needrestart/needrestart.conf`.  
- **Não copie** da internet receitas `sed` que mudam `$nrconf{restart}` para `'a'` sem entender o efeito — pode aumentar reinícios automáticos.

### 9.2 Ferramentas essenciais

```bash
sudo apt install htop iotop iftop ncdu tree -y
```

| Comando | Para que serve |
|---------|----------------|
| `htop` | CPU/RAM/processos em tempo real |
| `iotop` | Quem está usando o disco |
| `iftop` | Tráfego de rede |
| `ncdu` | Descobrir o que ocupa espaço |
| `tree` | Ver árvore de diretórios |

### 9.3 Repetir em cada CT/VM

Os CTs 100, 200 (e os que você criar depois) também precisam de:

```bash
# Dentro de cada CT (console como root no Proxmox; se estiver como usuário normal: sudo -i e depois estes comandos)
apt update && apt install unattended-upgrades -y
dpkg-reconfigure --priority=low unattended-upgrades
```

### 📝 Documente

```bash
echo "## $(date +"%F %H:%M") - Fase 9 concluída" >> ~/fortaleza-lab/diario.md
echo "- unattended-upgrades + ferramentas instaladas" >> ~/fortaleza-lab/diario.md
```

---

# 🟢 FASE 10 — Documentação Viva e Recuperação

🎯 **OBJETIVO:** Garantir que daqui a 6 meses, **mesmo esquecendo tudo**, você consegue recuperar/manter o lab.
⏱ **Tempo estimado:** 30–45 min

📚 **FUNDAMENTO:** Um homelab sem documentação vira lixo eletrônico. Esta fase cria três artefatos vitais:
1. **README local** — visão geral atualizada do estado do lab
2. **Diário de mudanças** — histórico do que você fez
3. **Plano de recuperação** — passos para reconstruir do zero

### 📸 Snapshot (recomendado)

```bash
# No host Proxmox — dataset conforme §0.8; renato com sudo
sudo zfs snapshot rpool/ROOT/pve-1@snap-pre-fase10
```

> **Laboratório descartável (filosofia):** aprender inclui quebrar, reinstalar e documentar. No Proxmox isso traduz-se em **snapshots** antes de mudanças grandes, **`vzdump`** e cópias de `/etc/pve` para disco externo — separar o que é **configuração do nó** do que são **dados das VMs**. Podes ainda manter pastas tipo `~/scripts` e `~/notes` dentro de `~/fortaleza-lab/` ou nas VMs de estudo (ver [docs/linux-comandos-fundamentos.md](docs/linux-comandos-fundamentos.md)).

### 10.1 README local

Como `renato` no Proxmox:

```bash
cat > ~/fortaleza-lab/README.md << 'EOF'
# Fortaleza Proxmox — Estado Atual

## Hardware
- Mini PC, 16 GB RAM, Proxmox VE 9.x (Debian 13 Trixie)

## Rede
- IP local: 192.168.1.100/24
- Gateway: 192.168.1.1
- DNS: 1.1.1.1, 8.8.8.8
- Tailscale IP: (preencher após Fase 5)

## Acesso
- SSH: `ssh fortaleza` (alias no ~/.ssh/config)
- Web GUI: https://192.168.1.100:8006 (renato@pam)
- Emergência: console físico do Mini PC

## Containers Ativos
| ID  | Nome             | IP             | Função                   |
|-----|------------------|----------------|--------------------------|
| 100 | vpn-tailscale    | 192.168.1.110  | VPN Tailscale + subnet   |
| 200 | lab-irmao-gpg    | 192.168.1.120  | Lab GPG do irmão         |

## Segurança Ativa
- SSH: chave Ed25519 + 2FA TOTP (renato)
- root SSH: BLOQUEADO
- Painel web: senha + 2FA TOTP
- CrowdSec + bouncer nftables
- Firewall proxmox-firewall (nftables) em DROP
- Acesso externo: APENAS via Tailscale
- Port forwarding no roteador: DESATIVADO

## Backups
- /root/backups/etc-pve-*.tar.gz (locais)
- Snapshots ZFS: rpool/ROOT/pve-1@snap-*

## Próximos Projetos
- [ ] AdGuard Home (CT 101)
- [ ] Nginx Proxy Manager (CT 102)
- [ ] Vaultwarden (CT 300)
- [ ] Uptime Kuma (CT 301)
EOF

cat ~/fortaleza-lab/README.md
```

### 10.2 Diário de mudanças

Você já vem fazendo isso desde a Fase 1. Continue:

```bash
# Sempre que mudar algo significativo:
echo "## $(date +"%F %H:%M") - <Título da mudança>" >> ~/fortaleza-lab/diario.md
echo "- <O que foi feito>" >> ~/fortaleza-lab/diario.md
echo "- <Comando ou config relevante>" >> ~/fortaleza-lab/diario.md
echo "" >> ~/fortaleza-lab/diario.md
```

### 10.3 Backup completo do `/etc/pve`

Crie um script de backup:

```bash
sudo nano /usr/local/bin/backup-fortaleza.sh
```

Cole:

```bash
#!/bin/bash
# Backup do /etc/pve para /root/backups/
set -e

DATE=$(date +%F-%H%M)
BACKUP_DIR="/root/backups"
mkdir -p "$BACKUP_DIR"

# Backup do /etc/pve (configurações Proxmox)
tar czf "$BACKUP_DIR/etc-pve-$DATE.tar.gz" /etc/pve/

# Verificação básica: o tar deve listar sem erro (não extrai)
tar tzf "$BACKUP_DIR/etc-pve-$DATE.tar.gz" >/dev/null && echo "OK: arquivo tar legível"

# Manter só os últimos 30 backups
ls -t "$BACKUP_DIR"/etc-pve-*.tar.gz | tail -n +31 | xargs -r rm

echo "Backup OK: $BACKUP_DIR/etc-pve-$DATE.tar.gz"
ls -lh "$BACKUP_DIR/etc-pve-$DATE.tar.gz"
```

Permissões e teste:

```bash
sudo chmod +x /usr/local/bin/backup-fortaleza.sh
sudo /usr/local/bin/backup-fortaleza.sh
```

Teste manual do último backup (opcional, a qualquer momento):

```bash
LATEST=$(ls -t /root/backups/etc-pve-*.tar.gz | head -1)
tar tzf "$LATEST" >/dev/null && echo "Backup íntegro: $LATEST"
```

### Agendar backup diário via cron

```bash
sudo crontab -e
```

Adicione no final:
```
# Backup diário às 03:00
0 3 * * * /usr/local/bin/backup-fortaleza.sh >> /var/log/backup-fortaleza.log 2>&1
```

> **Bónus (repositório Git):** exemplos **systemd** (`.timer` + `.service`) para o mesmo horário sem editar `crontab`, o script **só-leitura** `fortaleza-health-check.sh` (opção `--json` para agendadores), e **`make check`** / **`make check-json`** na raiz ([Makefile](Makefile)). Índice: [scripts/README.md](scripts/README.md).

### 10.4 Copiar backups para fora do servidor

⚠️ **Backup que fica só no servidor não é backup.** Configure para copiar para seu PC:

No seu PC pessoal, crie um script:

```bash
nano ~/sync-fortaleza-backups.sh
```

```bash
#!/bin/bash
# Sincroniza backups do Proxmox para o PC
# Ajuste o destino SSH: use o Host do §2.4 (ex.: fortaleza) ou renato@IP_DO_PVE
rsync -avz --delete \
  fortaleza:/root/backups/ \
  ~/fortaleza-backups/
```

```bash
chmod +x ~/sync-fortaleza-backups.sh
~/sync-fortaleza-backups.sh
```

> Rode esse comando uma vez por semana, manualmente, ou agende um cron no seu PC.

### 10.5 Plano de Recuperação (RUNBOOK)

Crie um runbook para o seu "eu do futuro":

```bash
cat > ~/fortaleza-lab/recuperacao.md << 'EOF'
# Plano de Recuperação — Fortaleza Proxmox

## Cenário 1: Perdi acesso SSH (não consigo logar)

1. Acesso físico ao Mini PC (monitor + teclado)
2. Logue como root (senha no Bitwarden)
3. Verifique:
   - `systemctl status ssh`
   - `cat /etc/ssh/sshd_config.d/99-hardening.conf`
4. Se config quebrada: comente as linhas problemáticas e reinicie o SSH (Debian 13: unidade `ssh`, não `sshd`):
   - `sudo systemctl restart ssh`

## Cenário 2: Perdi o celular do 2FA

1. Use um dos 5 códigos de recuperação salvos no Bitwarden
2. Reconfigure o 2FA imediatamente após logar:
   - `google-authenticator` (gerar novo segredo)
   - Atualizar Bitwarden com novos códigos

## Cenário 3: Mini PC quebrou / disco morreu

1. Compre/recupere hardware
2. Reinstale Proxmox VE 9.x (ISO atual da série 9)
3. Configure rede igual: IP 192.168.1.100/24
4. Restaure `/etc/pve` do último backup (como **root** no novo nó; ajuste o nome do arquivo):
   - `sudo tar xzf etc-pve-DATE.tar.gz -C /`
5. **TLS / certificado do painel:** após restaurar numa máquina nova ou com hostname/IP diferentes, o browser pode alertar certificado não confiável até alinhares certificados com o nó atual. Consulte a wiki [Certificate Management](https://pve.proxmox.com/wiki/Certificate_Management) e `man pvenode` na sua versão — **não** forces comandos de cluster (`pvecm`) copiados da internet sem ler a doc (contexto *single node* vs *cluster*).
6. Restaure containers (templates + backups VM)
7. Reconfigure Tailscale (re-autenticar device)

## Cenário 4: Me banni acidentalmente no CrowdSec

1. Console físico ou web → terminal local
2. `sudo cscli decisions delete --ip MEU_IP`
3. Ou: `sudo cscli decisions delete --all` (emergência)

## Cenário 5: Firewall me trancou fora

1. Console físico do Mini PC
2. `sudo pve-firewall stop`
3. `sudo systemctl stop proxmox-firewall`
4. Editar como root (ex.: `sudo nano /etc/pve/firewall/cluster.fw`) → `enable: 0`
5. Corrigir as regras, depois `enable: 1` e reinicie os serviços de firewall conforme a [wiki Firewall](https://pve.proxmox.com/wiki/Firewall)

## Senhas e Segredos Críticos
- TODOS no Bitwarden, pasta "Fortaleza Proxmox"
- Console físico do Mini PC: sempre acessível (não trancar a sala!)
- Códigos de recuperação 2FA: impressos e guardados separadamente também

EOF

cat ~/fortaleza-lab/recuperacao.md
```

### 10.6 Versionar no Git (opcional mas recomendado)

```bash
cd ~/fortaleza-lab
git init
git add README.md diario.md recuperacao.md
git config user.email "renato@example.com"
git config user.name "Renato"
git commit -m "Estado inicial da Fortaleza Proxmox v5.0"
```

> Se quiser, depois pode fazer push para um repo privado no GitHub.

### 🔍 10.7 Verificação final do sistema — `make check`

Agora que completou **todas as fases**, execute o health-check para confirmar que nada ficou para trás:

```bash
# No host Proxmox, como renato (com sudo):
sudo bash /caminho/para/scripts/fortaleza-health-check.sh --verbose
```

Se clonou o repositório no host (opção Git do §10.6), ainda mais simples:

```bash
cd ~/fortaleza-lab   # ou onde tiver o repo clonado
make check           # equivalente ao health-check com output amigável
```

> **Resultado esperado:** todas as verificações a verde ✅. Qualquer item a vermelho ❌ merece atenção antes de considerar o lab "em produção". O script verifica: NTP, SSH sem password, root bloqueado, versão do PVE, ZFS, backups de `/etc/pve`, CrowdSec + bouncer, e `proxmox-firewall`. Índice: [scripts/README.md](scripts/README.md).

### 📝 Documente

```bash
echo "## $(date +"%F %H:%M") - Fase 10 concluída" >> ~/fortaleza-lab/diario.md
echo "- README, diário, recuperação criados" >> ~/fortaleza-lab/diario.md
echo "- Backup automático via cron 03:00" >> ~/fortaleza-lab/diario.md
```

---

# 🟢 FASE 10b — Backup de VMs e CTs (vzdump + PBS)

🎯 **OBJETIVO:** Configurar backups automáticos das suas VMs e containers LXC — o único seguro real contra corrupção de dados, ransomware ou erro humano.
⏱ **Tempo estimado:** 30–45 min

📚 **FUNDAMENTO**

O backup de `/etc/pve` (feito nas fases anteriores) protege a **configuração** do nó. Mas se um CT ou VM tiver dados importantes (base de dados, arquivos, projetos), é preciso backup do **conteúdo** da VM/CT também. O Proxmox oferece duas ferramentas:

- **`vzdump`**: backup de VMs/CTs para arquivo `.vma.zst` (local ou NFS)
- **Proxmox Backup Server (PBS)**: solução dedicada com deduplicação, verificação de integridade e restauro incremental

Para homelab com um único nó, `vzdump` com armazenamento local ou externo (USB, NFS) é o ponto de partida ideal.

---

## 10b.1 Backup manual com vzdump

```bash
# No nó PVE como root — substitua 100 pelo VMID da sua VM ou CT
# Listar VMs e CTs disponíveis:
pct list       # containers LXC
qm list        # VMs

# Backup de um CT para o storage local (diretório padrão: /var/lib/vz/dump/)
vzdump 100 --compress zstd --storage local

# Backup de uma VM:
vzdump 101 --compress zstd --storage local

# Verificar o arquivo criado:
ls -lh /var/lib/vz/dump/
# Esperado: vzdump-lxc-100-2026_05_12-03_00_00.tar.zst (ou .vma.zst para VM)
```

> **`--compress zstd`** é o formato mais eficiente no Proxmox 9 — mais rápido que gzip com melhor compressão.

```bash
# Testar integridade do backup (sem restaurar):
zstd -t /var/lib/vz/dump/vzdump-lxc-100-*.tar.zst
# Saída esperada: OK
```

---

## 10b.2 Backup agendado via painel web (recomendado)

O painel web do Proxmox permite configurar backups automáticos sem editar crontab manualmente:

1. No browser: **Datacenter** (raiz da árvore à esquerda) → separador **Backup**
2. Clique **Add**
3. Configure:
   - **Storage:** `local` (ou outro storage configurado)
   - **Schedule:** `00:03` (ou `sun 03:00` para semanal)
   - **Selection:** `All` (todas as VMs e CTs) ou selecione individualmente
   - **Compression:** `ZSTD`
   - **Mode:** `Snapshot` (para VMs com QEMU Agent) ou `Suspend` (para CTs)
   - **Max Backups:** `3` (mantém os 3 mais recentes; ajuste conforme espaço em disco)
4. Clique **Create**

> O Proxmox mostrará o próximo agendamento. Pode clicar **Run now** para testar imediatamente.

---

## 10b.3 Restaurar um backup (vzdump)

```bash
# Restaurar CT do backup (substitua 100 e o caminho):
pct restore 100 /var/lib/vz/dump/vzdump-lxc-100-2026_05_12-03_00_00.tar.zst \
  --storage local-lvm \
  --unprivileged 1

# Restaurar VM do backup:
qmrestore /var/lib/vz/dump/vzdump-qemu-101-2026_05_12-03_00_00.vma.zst 101 \
  --storage local-lvm

# Ou via painel web: selecione o arquivo em Datacenter → Storage → local → Backups
# Clique no backup → botão "Restore"
```

> **Atenção:** restaurar por cima de um VMID existente pára e substitui a VM/CT. Para restaurar em paralelo, use um VMID diferente (ex.: `pct restore 200 ...`).

---

## 10b.4 Proxmox Backup Server (PBS) — introdução

O PBS é um servidor dedicado a backups, separado do nó PVE. Para homelab num único mini PC, pode correr o PBS:

- Numa VM dentro do próprio Proxmox (cria isolação)
- Num segundo mini PC ou Raspberry Pi na rede
- Num servidor NAS (Synology/TrueNAS têm pacotes PBS)

**Vantagens do PBS sobre vzdump local:**
- Backups incrementais (só envia o que mudou — muito mais rápido após o primeiro)
- Deduplicação — 5 backups ocupam muito menos que 5× o tamanho da VM
- Verificação de integridade agendada automática (`proxmox-backup-client verify`)
- Interface web própria em `https://PBS_IP:8007`

```bash
# Adicionar PBS como storage no nó PVE (após instalar PBS):
# Painel web PVE → Datacenter → Storage → Add → Proxmox Backup Server
# Preencha: ID, Server (IP do PBS), Datastore (nome criado no PBS), credenciais

# Fazer backup direto para PBS (linha de comando):
vzdump 100 --storage pbs-storage --compress zstd

# Verificar backups no PBS (no nó PBS):
proxmox-backup-client list
```

> Para instalar o PBS do zero: [Proxmox Backup Server — Installation](https://pbs.proxmox.com/docs/installation.html)

---

✅ **VERIFIQUE**

```bash
# Confirmar que existe pelo menos um backup:
ls -lh /var/lib/vz/dump/

# Testar integridade:
for f in /var/lib/vz/dump/*.tar.zst; do
  zstd -t "$f" && echo "OK: $f" || echo "ERRO: $f"
done

# Via painel: Datacenter → Backup → ver próximo agendamento e histórico
```

---

🆘 **SE DEU ERRADO**

| Sintoma | Causa | Solução |
|---------|-------|---------|
| `vzdump: ERROR: unable to freeze CT` | CT não suporta snapshot no mode escolhido | Use `--mode suspend` em vez de `snapshot` |
| Espaço insuficiente no storage | Backup muito grande para o disco local | Aumente `--maxfiles` (menos retenção) ou use storage externo (USB/NFS) |
| `zstd: ERROR: Corrupted block` na verificação | Backup corrompido durante escrita (ex.: disco cheio) | Delete o arquivo e refaça o backup; verifique `df -h` antes |
| PBS não aparece como storage | Certificado PBS não confiado pelo PVE | No PVE: `pvecm updatecerts` ou adicione o fingerprint do PBS manualmente |

---

```bash
echo "## $(date +"%F %H:%M") - Fase 10b concluída" >> ~/fortaleza-lab/diario.md
echo "- Backup vzdump configurado (agendado via painel)" >> ~/fortaleza-lab/diario.md
echo "- Testar restauro de CT/VM antes de confiar como único backup" >> ~/fortaleza-lab/diario.md
```

---

# 🟢 FASE VM-01 — VM Debian 13 de Estudo (Linux Fundamentals)

🎯 **OBJETIVO:** Criar uma VM Debian 13 "Trixie" limpa, isolada e com snapshot — o seu laboratório pessoal de Linux Fundamentals. Pode destruir e recriar em minutos.
⏱ **Tempo estimado:** 20–30 min (com Cloud-Init) ou 45–60 min (instalação manual)

📚 **FUNDAMENTO**

O host Proxmox (Fortaleza) é o cofre — não se aprende Linux dentro do cofre. A VM de estudo é o laboratório onde você experimenta, erra, aprende e recomeça sem medo. Com ZFS e Cloud-Init, recriar do zero demora menos de 2 minutos.

A diferença crítica:

| Contexto | Filosofia |
|----------|-----------|
| **Host PVE** | Não toque. CrowdSec, firewall, backups — mínimo de mudanças. |
| **VM de estudo** | Destrua à vontade. É para aprender. Snapshot antes de cada experiência. |

---

## VM-01.1 Criar a VM com Cloud-Init (método rápido)

```bash
# No nó PVE como root — aproveita a infraestrutura Cloud-Init do Apêndice J.5

# 1. Baixar imagem cloud Debian 12 (Bookworm — estável e bem suportada para labs):
wget https://cloud.debian.org/images/cloud/bookworm/latest/debian-12-genericcloud-amd64.qcow2 \
  -O /var/lib/vz/template/iso/debian-12-cloud.qcow2

# 2. Criar VM base:
qm create 110 \
  --name debian-estudo \
  --memory 2048 \
  --cores 2 \
  --net0 virtio,bridge=vmbr0 \
  --serial0 socket \
  --vga serial0 \
  --agent enabled=1

# 3. Importar disco cloud:
qm importdisk 110 /var/lib/vz/template/iso/debian-12-cloud.qcow2 local-lvm

# 4. Configurar disco e boot:
qm set 110 --scsihw virtio-scsi-pci --scsi0 local-lvm:vm-110-disk-0
qm set 110 --ide2 local-lvm:cloudinit
qm set 110 --boot order=scsi0
qm set 110 --ipconfig0 ip=192.168.1.110/24,gw=192.168.1.1

# 5. Configurar Cloud-Init — usuário, senha e chave SSH:
qm set 110 --ciuser aluno
qm set 110 --cipassword SenhaForteParaOLab
# Opcional — copiar a sua chave SSH pública da Fase 2:
qm set 110 --sshkeys /root/.ssh/authorized_keys

# 6. Iniciar:
qm start 110
# Em ~30–60 segundos a VM está pronta
```

> **Não tem chave SSH ainda?** A Fase 2 do guia ensina a criar `chave_fortaleza`. Use a mesma chave para a VM de estudo — mais seguro e sem senha.

---

## VM-01.2 Configuração inicial da VM de estudo

```bash
# Conectar SSH (do seu PC — use o IP configurado acima):
ssh aluno@192.168.1.110

# Se configurou chave SSH:
ssh -i ~/.ssh/chave_fortaleza aluno@192.168.1.110

# --- Dentro da VM ---

# Atualizar sistema:
sudo apt update && sudo apt upgrade -y

# Instalar ferramentas de estudo (tudo que você vai precisar nos labs):
sudo apt install -y \
  git curl wget vim nano tmux \
  net-tools dnsutils iputils-ping traceroute \
  nmap \
  gpg gnupg2 openssl \
  bind9-utils \
  htop tree jq \
  build-essential

# Verificar versão do sistema:
cat /etc/os-release
uname -r
```

> **Por que `nmap`?** Só para uso local/educacional — verificar quais portas a VM tem abertas, testar o firewall. Nunca use em redes que não são suas.

---

## VM-01.3 Snapshot da VM base (antes de começar a estragar)

```bash
# No nó PVE — não dentro da VM (volte ao SSH do host PVE):
# Parar a VM para snapshot consistente (opcional, mas recomendado):
qm shutdown 110 --timeout 30

# Criar snapshot:
zfs snapshot rpool/data/vm-110-disk-0@base-limpa
# Ou via qm (snapshot QEMU — inclui estado de RAM se VM estiver ligada):
qm snapshot 110 base-limpa --description "VM Debian 12 limpa + ferramentas de estudo"

# Verificar:
qm listsnapshot 110
# Esperado: ver "base-limpa" na lista

# Iniciar VM novamente:
qm start 110
```

> **Regra de ouro do laboratório:** antes de cada experiência nova (instalar bind9, testar iptables, etc.), faça um snapshot com nome descritivo. Se quebrar, reverta. Se funcionar, avance.

```bash
# Exemplos de snapshots que você vai criar ao longo dos estudos:
qm snapshot 110 antes-dns        # antes de instalar bind9
qm snapshot 110 antes-nginx      # antes de instalar nginx
qm snapshot 110 antes-iptables   # antes de configurar firewall
```

---

## VM-01.4 Conectar e começar os estudos

```bash
# Conectar SSH (do seu PC):
ssh aluno@192.168.1.110

# Primeiro exercício — explorar o sistema:
whoami          # aluno
hostname        # debian-estudo
ip addr show    # ver interfaces de rede
df -h           # espaço em disco
free -h         # RAM disponível
systemctl list-units --type=service --state=running  # serviços ativos
```

> **Próximo passo de estudo:** abra o [cheat sheet Linux](docs/linux-comandos-fundamentos.md) e siga os exercícios na VM 110. Cada seção tem comandos para praticar — use a VM, não o host PVE.

---

✅ **VERIFIQUE**

```bash
# No nó PVE:
qm status 110          # deve mostrar "status: running"
qm listsnapshot 110    # deve mostrar "base-limpa"

# Do seu PC:
ping -c 3 192.168.1.110        # responde
ssh aluno@192.168.1.110 "id"   # retorna: uid=1000(aluno) gid=1000(aluno)...

# Dentro da VM:
sudo apt update   # deve completar sem erros
gpg --version     # deve mostrar versão GPG instalada
```

---

🆘 **SE DEU ERRADO**

| Sintoma | Causa | Solução |
|---------|-------|---------|
| `qm start 110` falha com "VMID already in use" | VMID 110 já existe | Use `qm destroy 110` se for lixo, ou escolha outro VMID (ex.: 120) |
| SSH recusa conexão (Connection refused) | VM ainda não terminou boot, ou sshd não instalado | Aguarde 60 s; ou abra console no painel PVE e verifique status da VM |
| Cloud-Init não configurou usuário `aluno` | Sintaxe do `--ciuser` incorreta | `qm cloudinit dump 110 user` para ver o que foi gerado; `qm set 110 --ciuser aluno` e reiniciar |
| IP 192.168.1.110 não acessível | IP já em uso na rede | Mude para IP livre; verifique com `ping 192.168.1.110` no router |
| `wget` lento para imagem cloud | Conexão lenta | Use `curl -C - -O URL` para retomar download interrompido |

---

```bash
echo "## $(date +"%F %H:%M") - Fase VM-01 concluída" >> ~/fortaleza-lab/diario.md
echo "- VM 110 (debian-estudo) criada com Cloud-Init" >> ~/fortaleza-lab/diario.md
echo "- Snapshot base-limpa criado — laboratório pronto" >> ~/fortaleza-lab/diario.md
```

> **Próximo passo:** siga os [Fundamentos Linux](docs/linux-comandos-fundamentos.md) na VM 110. Quando quiser instalar DNS bind9, nginx ou iptables, veja o **Apêndice D** (roadmap de labs).

---

# 📋 Apêndice A — Checklist Final Consolidado

## FASE 0 — Preparação
- [ ] Timezone correto, NTP ativo (`timedatectl status` → synchronized: yes)
- [ ] IP fixo configurado (estático no PVE OU reserva no roteador)
- [ ] `hostname -i` retorna IP correto (não 127.0.1.1)
- [ ] Repositório Enterprise desabilitado
- [ ] Repositório No-Subscription habilitado
- [ ] `apt update` sem erros
- [ ] Sistema atualizado, reboot se kernel mudou
- [ ] Backup inicial do /etc/pve em /root/backups/
- [ ] Snapshot ZFS `snap-fase0-instalacao-limpa`

## FASE 1 — Identidade
- [ ] Usuário `renato` criado, `sudo whoami` retorna `root`
- [ ] Senha do `renato` no Bitwarden

## FASE 2 — SSH
- [ ] Chave Ed25519 gerada, passphrase no Bitwarden
- [ ] `~/.ssh/config` no PC com alias `fortaleza`
- [ ] `/etc/ssh/sshd_config.d/99-hardening.conf` criado
- [ ] `sshd -T | grep passwordauthentication` retorna `no`
- [ ] Root SSH bloqueado (`ssh root@...` recusado)

## FASE 3 — 2FA SSH
- [ ] 2FA TOTP configurado, QR/chave/recovery no Bitwarden
- [ ] Login SSH pede chave + código
- [ ] **`nullok` REMOVIDO** de `/etc/pam.d/sshd`

## FASE 4 — CrowdSec
- [ ] `cscli bouncers list` mostra bouncer válido
- [ ] Whitelist com 192.168.1.0/24 + 100.64.0.0/10
- [ ] `nft list ruleset | grep crowdsec` retorna resultado

## FASE 5 — Tailscale
- [ ] CT 100 `vpn-tailscale` rodando
- [ ] `tailscale0` aparece em `ip addr` (modo kernel)
- [ ] Subnet route aprovada no admin Tailscale
- [ ] Acesso ao PVE via 100.x.x.x funcionando

## FASE 6 — 2FA painel
- [ ] Snapshot ZFS `snap-pre-fase6` (recomendado antes de alterar permissões/TFA na GUI)
- [ ] `renato@pam` Administrator no painel
- [ ] TOTP ativo, recovery keys no Bitwarden
- [ ] `root@pam` não mais usado no dia-a-dia

## FASE 7 — Firewall
- [ ] Snapshot ZFS `snap-pre-fase7` + backup `tar` de `/etc/pve` antes do DROP
- [ ] 6 regras ACCEPT criadas ANTES do DROP (SSH + GUI para LAN e Tailscale + ICMP para LAN e Tailscale)
- [ ] Firewall enabled em Datacenter E no Nó
- [ ] nftables: Yes habilitado
- [ ] `systemctl status proxmox-firewall` active
- [ ] `nft list tables` mostra proxmox-firewall e proxmox-firewall-guests
- [ ] Port forwarding removido do roteador
- [ ] Teste de 4G confirma servidor invisível

## FASE 8 — Lab Irmão
- [ ] Snapshot ZFS `snap-pre-fase8` (recomendado antes de Docker/ShellHub)
- [ ] CT 200 com nesting=1
- [ ] Docker rodando dentro
- [ ] ShellHub device accepted
- [ ] Irmão consegue conectar

## FASE 9 — Manutenção
- [ ] Snapshot ZFS `snap-pre-fase9` (recomendado antes de automatizar upgrades)
- [ ] unattended-upgrades ativo no PVE e nos CTs
- [ ] Ferramentas de monitoramento instaladas: `htop`, `iotop`, `iftop`, `btop`, `fastfetch`

## FASE 10 — Documentação
- [ ] Snapshot ZFS `snap-pre-fase10` (recomendado antes de cron de backups em massa)
- [ ] README.md em ~/fortaleza-lab/
- [ ] diario.md com histórico
- [ ] recuperacao.md (runbook)
- [ ] Script de backup automático no cron
- [ ] Backups sendo copiados para fora do servidor
- [ ] **Verificação final:** `sudo bash scripts/fortaleza-health-check.sh --verbose` (ou `make check`) — todos os itens a verde ✅ — [scripts/README.md](scripts/README.md)

---

## Rotina de administração semanal

Após concluir todas as fases, reserve **5 minutos por semana** para estes comandos — eles cobrem os pontos de falha mais comuns num homelab:

```bash
# 1. Saúde do storage (ZFS pool + erros por disco)
zpool status

# 2. Saúde dos discos físicos (SMART — valor "PASSED" é o esperado)
smartctl -H /dev/sda   # substitua sda pelo disco correto (lsblk)

# 3. IPs banidos e atividade CrowdSec
sudo cscli metrics | head -20
sudo cscli decisions list | head -10

# 4. Erros de sistema nas últimas 48 h
journalctl -p err --since "48 hours ago" --no-pager | tail -20

# 5. Tarefas PVE com falha (backups, vzdump, etc.)
pvesh get /nodes/fortaleza/tasks --limit 30 | grep -i error || echo "Sem erros ✅"
```

> **Rotina mensal:** `make check` na raiz do repositório ([Makefile](Makefile)) — cobre NTP, SSH endurecido, CrowdSec, firewall, ZFS, CTs 100/200 e integridade do último backup.

### Automação do scrub mensal ZFS (configure uma vez, funciona para sempre)

```bash
# Adicionar cron para scrub automático todo dia 1 do mês às 03:00:
(crontab -l 2>/dev/null; echo "0 3 1 * * /sbin/zpool scrub rpool") | crontab -

# Verificar que foi adicionado:
crontab -l | grep scrub
# Esperado: 0 3 1 * * /sbin/zpool scrub rpool

# Adicionar também um cron para verificar o resultado e alertar se houver erros:
(crontab -l 2>/dev/null; echo "0 4 2 * * /sbin/zpool status rpool | grep -q 'errors: No known' || echo 'ZFS ALERT: pool rpool com erros!' | mail -s 'ZFS Alert - Fortaleza' root") | crontab -

# Ver todos os crons ativos:
crontab -l
```

> **Por que dia 1 às 03:00?** O scrub leva 15–30 min num pool de 500 GB. Rodar de madrugada evita impacto na latência do AdGuard/Vaultwarden. O resultado fica disponível em `zpool status` — verifique no dia 2 (rotina semanal já faz isso).

---

## Rotina trimestral

```bash
# 1. Teste de velocidade de rede interna (instalar iperf3 num CT de teste):
apt install -y iperf3
# No CT servidor: iperf3 -s
# No host PVE:    iperf3 -c 192.168.1.X
# Esperado: próximo de 1 Gbit/s na LAN — queda indica cabo ruim ou switch degradado

# 2. Auditoria de usuários e permissões PVE:
pveum user list          # quem tem acesso?
pveum acl list           # quais permissões?
# Remover acessos não mais necessários

# 3. Self-test SMART completo (demora horas — agendar para madrugada):
sudo smartctl -t long /dev/nvme0n1
# Verificar resultado no dia seguinte:
sudo smartctl -l selftest /dev/nvme0n1   # deve mostrar "Completed without error"

# 4. Verificar CPU governor e mitigações:
cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor
grep . /sys/devices/system/cpu/vulnerabilities/* | grep -v "Not affected\|Mitigation"
# Resultado vazio = tudo mitigado (bom)
```

---

## Rotina anual

```bash
# 1. Teste de disaster recovery — restaurar uma VM/CT de backup:
qmrestore <backup.zst> 999 --storage local-zfs
qm start 999
# Confirmar que arranca, serviços funcionam, dados íntegros
qm stop 999 && qm destroy 999   # limpar após teste

# 2. Revisão de hardware:
inxi -Fxz > /root/backups/inxi-$(date +%F).txt    # baseline anual
hw-check >> /root/backups/hw-check-$(date +%F).txt

# 3. Expansão e planeamento:
# - O N5095 ainda é suficiente? Ver Apêndice D para roadmap de expansão
# - Avaliar upgrade de hardware ou adição de nó PBS dedicado
# - Reler audit-matrix.md para verificar se algo mudou de status (nftables tech preview → estável?)
```

---

## Calendário de manutenção ZFS

O ZFS é robusto, mas não é mágico — precisa de manutenção periódica para garantir integridade dos dados. Esta tabela centraliza **tudo que o guia menciona sobre ZFS** em um único lugar de referência.

| Frequência | Tarefa | Comando | Por quê |
|------------|--------|---------|---------|
| **Após qualquer queda de energia** | Verificar erros no pool | `zpool status -v` | ZFS detecta inconsistências após power loss |
| **Semanal** | Verificar saúde geral | `zpool status` | Detectar degradação precoce (read/write/cksum errors) |
| **Mensal** | Scrub completo | `zpool scrub rpool` | Verifica integridade de todos os blocos — detecta bit rot |
| **Mensal** | Confirmar scrub OK | `zpool status \| grep -E "scan\|errors"` | Resultado esperado: "repaired 0B" ou "with no errors" |
| **Trimestral** | Self-test SMART longo | `smartctl -t long /dev/nvme0n1` | Testa o hardware físico do disco, não só os dados |
| **Trimestral** | Ler resultado SMART | `smartctl -l selftest /dev/nvme0n1` | "Completed without error" = disco saudável |
| **Anual** | Verificar SMART atributos críticos | `smartctl -a /dev/nvme0n1 \| grep -i reallocated` | `REALLOCATED_SECTOR_CT > 5` = planejare substituição |
| **Após incidente** | Limpar contadores de erro | `zpool clear rpool` | Só após investigar — não limpar sem saber a causa |

### Quando substituir o disco

| Sinal | Urgência | Ação |
|-------|----------|------|
| `REALLOCATED_SECTOR_CT` crescendo | 🟡 Planejar | Fazer backup extra, comprar substituto |
| `REALLOCATED_SECTOR_CT > 20` | 🔴 Imediato | Substituir antes da próxima semana |
| `PENDING_SECTOR` > 0 | 🔴 Imediato | Backup agora + substituir |
| Scrub com `repaired > 0` | 🟡 Investigar | Pode ser soft error (comum); se recorrente → substituir |
| `zpool status` mostra `DEGRADED` | 🔴 Emergência | Seguir Apêndice H — Plano de Recuperação |
| `zpool status` mostra `FAULTED` | 🔴 Emergência | Disco morto — substituir + `zpool replace` |

### Sequência pós-queda de energia (execute nesta ordem)

```bash
# 1. Verificar estado do pool:
zpool status -v
# Se mostrar ONLINE sem errors: tudo bem, continuar

# 2. Se houver erros, verificar eventos:
zpool events -v | head -30

# 3. Verificar se algum dado foi comprometido:
zpool scrub rpool
# Aguardar conclusão (5–30 min dependendo do tamanho)
watch -n 5 'zpool status | grep -E "scan|action|errors"'

# 4. Verificar SMART do disco físico:
smartctl -H /dev/nvme0n1   # ou /dev/sda para HDD

# 5. Se tudo OK, limpar contadores de erro:
zpool clear rpool
zpool status   # deve mostrar: errors: No known data errors
```

### Comandos úteis de diagnóstico ZFS

```bash
# Ver uso real do pool (deduplicação, compressão, fragmentação):
zpool list -v
zfs list -o name,used,avail,compressratio,fragmentation

# Histórico de scrubs e substituições:
zpool history rpool | grep -E "scrub|replace|clear" | tail -20

# Limite de cache ARC atual:
cat /sys/module/zfs/parameters/zfs_arc_max   # em bytes (0 = sem limite)
# Uso atual do ARC:
cat /proc/spl/kstat/zfs/arcstats | grep -E "^c |^size |^hits |^misses" | head

# Ver fragmentação (acima de 20% é atenção; acima de 50% → desfragmentar):
zpool list -o name,frag
```

> **N5095 com 1 disco:** sem RAID, uma falha de disco = perda de dados. A proteção é o **backup externo** (vzdump → PBS ou disco USB). O scrub mensal detecta problemas *antes* de o disco morrer completamente — dando tempo de agir.

---

# 📊 Apêndice B — Comandos de Monitoramento Diário

Cole isso em um arquivo `~/fortaleza-lab/comandos.md`:

### Segurança e rede

| O que verificar | Comando | O que esperar |
|-----------------|---------|---------------|
| IPs banidos pelo CrowdSec | `sudo cscli decisions list` | Tabela de IPs bloqueados |
| Estatísticas CrowdSec | `sudo cscli metrics` | Logs lidos, detections, bouncer ativo |
| Tentativas SSH em tempo real | `sudo journalctl -u ssh -f` | Stream — Ctrl+C para sair |
| Tentativas de login falhas | `sudo journalctl -u ssh \| grep -i fail` | Lista de falhas |
| Status firewall nftables | `sudo systemctl status proxmox-firewall` | active (running) |
| Regras nftables ativas | `sudo nft list ruleset \| less` | Chains proxmox-firewall |
| Status Tailscale (CT 100) | `sudo pct exec 100 -- tailscale status` | Lista de peers online |
| Portas em escuta | `ss -tuln` | Apenas portas esperadas (22, 8006…) |
| Bridges e interfaces | `brctl show` | vmbr0 com enp1s0 |
| DNS do sistema | `resolvectl status` | DNS resolving OK |

### Sistema e hardware

| O que verificar | Comando | O que esperar |
|-----------------|---------|---------------|
| Snapshot do sistema (rápido) | `fastfetch` | OS, CPU, RAM, uptime |
| Recursos interativos | `btop` | CPU/RAM/disco/rede — pressione q para sair |
| Serviços com falha | `sudo systemctl --failed` | 0 listed |
| Erros no kernel (últimas 6h) | `dmesg -T \| grep -i "error\|fail" \| tail -20` | Silêncio esperado |
| Atualizações pendentes | `sudo apt list --upgradable 2>/dev/null` | Lista (aplicar com `apt upgrade`) |
| Sincronização NTP | `timedatectl status` | synchronized: yes |
| Temperatura da CPU | `sensors \| grep -i temp \| head` | N5095: <65°C em carga |
| Saúde do ZFS | `zpool status` | state: ONLINE, sem errors |

### Backups e tarefas PVE

| O que verificar | Comando | O que esperar |
|-----------------|---------|---------------|
| Backups recentes `/etc/pve` | `ls -lh /root/backups/ \| tail` | Arquivo com data de hoje |
| Testar integridade do backup | `L=$(ls -t /root/backups/etc-pve-*.tar.gz \| head -1); tar tzf "$L" >/dev/null && echo OK` | `OK` |
| Tarefas PVE com erro | `pvesh get /nodes/fortaleza/tasks --limit 20 \| grep -i error` | Silêncio esperado |
| Backups vzdump recentes | `pvesm list local \| grep -i backup` | Lista de .zst recentes |

### Auditoria de segurança (mensal)

```bash
# Score de hardening do sistema (0–100):
sudo lynis audit system 2>/dev/null | grep -E "Hardening index|WARNING|SUGGESTION" | head -20
# Alvo homelab: índice acima de 70
```

### Bônus — automação só-leitura (repositório)

Depois de dominar as fases, use o script **`scripts/fortaleza-health-check.sh`** no host (com `sudo`): confirma NTP, SSH endurecido, último `tar` de `/etc/pve`, CrowdSec/firewall, ZFS, CTs 100/200 — **sem alterar nada**. Opção **`--json`** (uma linha para cron/CI) e **`make check`** / **`make check-json`** na raiz do clone ([Makefile](Makefile)). Índice completo (Telegram, systemd de exemplo, sync no PC): [scripts/README.md](scripts/README.md).

### Bônus — alertas Telegram automáticos

Quer receber uma mensagem no celular quando RAM estiver alta, um CT cair, CrowdSec banir um IP novo ou o ZFS tiver erro? O guia completo está em **[docs/monitoramento-telegram-fortaleza-proxmox.md](docs/monitoramento-telegram-fortaleza-proxmox.md)**.

Setup resumido em 3 passos:
1. Criar um bot no Telegram via `@BotFather` → obter `TELEGRAM_TOKEN`
2. Pegar seu `chat_id` mandando `/start` para o bot
3. Script Python no host + `cron` para rodar a cada 5 min

```bash
# Teste rápido — confirmar que o host chega ao Telegram:
curl -sS -o /dev/null -w "%{http_code}\n" https://api.telegram.org/
# Esperado: 200 (se retornar timeout, verifique regra OUT no proxmox-firewall)

# Instalar dependência:
apt install -y python3-requests

# Script fica em /opt/fortaleza-monitor/ — detalhes completos no doc acima
```

> **Por que não Prometheus/Grafana agora?** Para homelab com 1 nó, Python + Telegram + cron tem zero overhead e avisa o que importa. Grafana faz sentido quando você tiver múltiplos serviços para correlacionar — ver Apêndice L (Nível 3 do roadmap).

---

# 🗂️ Apêndice C — Padrão de Organização (IDs, Nomes, Tags)

### Faixas de ID

| Faixa | Função |
|-------|--------|
| 100–199 | Infraestrutura (VPN, DNS, Proxy reverso) |
| 200–299 | Labs isolados (irmão, testes) |
| 300–399 | Serviços (Home Assistant, Jellyfin) |
| 400–499 | Bancos de dados |
| 500–599 | Dev/Build (CI runners, etc) |
| 900+ | Templates limpos |

### Padrão de hostname: `[função]-[sistema]-[ambiente]`

Exemplos:
- `vpn-tailscale-prod`
- `lab-irmao-gpg`
- `net-adguard-dns`
- `srv-jellyfin-prod`
- `db-postgres-prod`

### Padrão de tags

- `infra` — infraestrutura crítica (não desligar)
- `network` — relacionado a rede
- `prod` — produção
- `lab` — laboratório (pode quebrar)
- `irmao` — acesso compartilhado
- `database` — banco de dados
- `critical` — não pode cair

### Snapshots descritivos

- `snap-pre-instalacao-docker`
- `snap-fase4-crowdsec-ok`
- `snap-2026-05-12-funcionando`

---

### Template de documentação de serviço (CT/VM)

Copie este template para o seu `~/fortaleza-lab/diario.md` sempre que criar um novo CT ou VM. Um diário bem estruturado vale mais do que qualquer wiki.

```markdown
## Serviço: [nome] — CT/VM [ID]
**Data de criação:** AAAA-MM-DD
**Status:** ativo / parado / lab

### Metadados
| Campo | Valor |
|-------|-------|
| Tipo | CT (LXC) / VM (KVM) |
| ID | 1xx / 2xx / 3xx |
| Hostname | funcao-app-env (ex: net-adguard-prod) |
| IP | 192.168.1.xxx/24 |
| OS | Debian 12 / Ubuntu 24.04 / Alpine |
| Storage | local-lvm / rpool/data |
| RAM alocada | 256 MB / 512 MB / 1 GB |
| Backup | sim (Apêndice A) / não (lab descartável) |
| Tags PVE | infra, network, prod, lab, critical |

### Configuração específica
- Porta(s) exposta(s): ...
- Volumes/mounts extras: ...
- Variáveis de ambiente / config files: ...
- Comando de restart: `systemctl restart <serviço>` / `docker compose restart`

### Dependências
- Precisa de: CT 100 (Tailscale ativo), bridge vmbr0, ...
- Usado por: ...

### Troubleshooting próprio
| Sintoma | Causa provável | Solução rápida |
|---------|---------------|----------------|
| Serviço não inicia | ... | `journalctl -u <serviço> -n 50` |
| Sem acesso externo | Firewall PVE ou rota | `pve-firewall compile; brctl show` |
| RAM alta | Memory leak / config | `pct exec ID -- ps aux --sort=-%mem \| head` |

### Histórico de mudanças
- AAAA-MM-DD: criado
- AAAA-MM-DD: [mudança relevante]
```

> **Dica:** mantenha um arquivo por serviço em `~/fortaleza-lab/servicos/CT-101-adguard.md`. Em 6 meses você vai agradecer por ter documentado o motivo de cada decisão.

---

# 🚀 Apêndice D — Plano de Expansão com LXCs e Labs de Estudo

Com a Fortaleza operacional, o hardware N5095 (16 GB RAM, 4 cores) tem capacidade para muito mais. Aqui está o roteiro completo — utilitários da rede, laboratórios de estudo e infraestrutura avançada.

---

## D.1 Capacidade do hardware — o que cabe no N5095

| CT/VM | App | RAM usada | CPU | Quando fica ligado |
|-------|-----|-----------|-----|-------------------|
| Host PVE | Proxmox + CrowdSec + bouncer | ~600 MB | — | Sempre |
| CT 100 | Tailscale | 256 MB | 0.5 | Sempre |
| CT 200 | ShellHub (irmão) | 512 MB | 0.5 | Opcional |
| VM 110 | Debian 13 estudo | 1–2 GB | 2 | Durante sessão de estudo |
| **Disponível** | | **~11–13 GB** | **~3–4 cores** | Para expansão |

> **Regra prática:** máximo 3–4 CTs/VMs ligados simultaneamente para uso confortável. LXC consome 10× menos overhead que VM KVM — prefira CT para serviços, VM para labs de SO.

---

## D.2 Nível 1 — Utilitários da rede (instale um de cada vez)

Serviços sempre ligados que melhoram a rede inteira. Baixo risco, alto ganho imediato.

| # | ID | App | RAM | O que aprende ao instalar |
|---|----|-----|-----|--------------------------|
| 1 | CT 101 | **AdGuard Home** | 256 MB | DNS recursivo, listas de bloqueio, protocolo DoH/DoT, configuração de DNS do roteador |
| 2 | CT 102 | **Nginx Proxy Manager** | 512 MB | Reverse proxy HTTP/HTTPS, Let's Encrypt automático, routing por domínio/path |
| 3 | CT 300 | **Vaultwarden** | 256 MB | Bitwarden self-hosted, TLS, gerenciamento de segredos, API de senhas |
| 4 | CT 301 | **Uptime Kuma** | 256 MB | Monitoramento HTTP/TCP/ping, alertas Telegram/email, SLA pessoal |

```bash
# Fluxo padrão para qualquer CT do Nível 1:
# 1. Baixar template Debian 12:
pveam update && pveam download local debian-12-standard_12.7-1_amd64.tar.zst

# 2. Criar CT (substitua CTID e IP):
pct create 101 local:vztmpl/debian-12-standard_12.7-1_amd64.tar.zst \
  --hostname adguard-home \
  --memory 256 \
  --rootfs local-lvm:4 \
  --net0 name=eth0,bridge=vmbr0,ip=192.168.1.101/24,gw=192.168.1.1 \
  --unprivileged 1 \
  --start 1

# 3. Snapshot antes de instalar a app:
pct shutdown 101 && \
  zfs snapshot $(pct config 101 | grep rootfs | awk -F: '{print $2}' | awk '{print $1}')@antes-install && \
  pct start 101

# 4. Instalar a app (dentro do CT):
pct exec 101 -- bash -c “apt update && apt install -y curl”
```

### D.2.1 AdGuard Home — guia rápido (CT 101)

AdGuard Home é um servidor DNS recursivo com bloqueio de anúncios e rastreadores para **toda a rede**. Depois de instalado, você aponta o DNS do roteador para ele — todos os dispositivos da casa ficam limpos sem instalar nada em cada um.

🎯 **OBJETIVO:** CT 101 com AdGuard Home respondendo DNS na LAN + painel web acessível via Tailscale  
⏱ **Tempo estimado:** 20–30 min

```bash
# ── 1. Criar o CT 101 no host PVE ──
# Baixar template Debian 12 (se ainda não tiver):
pveam update && pveam download local debian-12-standard_12.7-1_amd64.tar.zst

# Criar CT:
pct create 101 local:vztmpl/debian-12-standard_12.7-1_amd64.tar.zst \
  --hostname net-adguard-prod \
  --memory 256 \
  --rootfs local-lvm:4 \
  --net0 name=eth0,bridge=vmbr0,ip=192.168.1.101/24,gw=192.168.1.1 \
  --nameserver 1.1.1.1 \
  --unprivileged 1 \
  --start 1

# ── 2. Snapshot antes de instalar ──
pct exec 101 -- bash -c "apt update && apt upgrade -y"
pct stop 101
zfs snapshot rpool/data/subvol-101-disk-0@antes-adguard
pct start 101

# ── 3. Instalar AdGuard Home dentro do CT ──
pct exec 101 -- bash -c "curl -sSL https://raw.githubusercontent.com/AdguardTeam/AdGuardHome/master/scripts/install.sh | sh -s -- -v"
# Isso baixa e instala o binário + cria serviço systemd automaticamente

# ── 4. Verificar que o serviço está ativo ──
pct exec 101 -- systemctl status AdGuardHome
# Esperado: active (running)
```

**Configuração inicial (painel web):**

1. Acesse `http://192.168.1.101:3000` no navegador (primeira configuração)
2. Defina usuário e senha → **salve no Bitwarden**
3. Interface de escuta: `eth0` (porta 53 DNS + porta 80 painel)
4. Após setup, o painel fica em `http://192.168.1.101:80`

**Apontar DNS do roteador para o CT 101:**
- Acesse painel do roteador → configurações DHCP → DNS primário: `192.168.1.101`
- DNS secundário: `1.1.1.1` (fallback se o CT estiver parado)
- Aguarde 5–10 min para os dispositivos renovarem o DHCP

**Listas de bloqueio recomendadas** (AdGuard Home → Filters → DNS Blocklists):
```
https://adguardteam.github.io/HostlistsRegistry/assets/filter_1.txt   # AdGuard DNS filter
https://adguardteam.github.io/HostlistsRegistry/assets/filter_2.txt   # AdAway Default
https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts      # Steven Black (ads+malware)
```

**✅ Verifique:**
```bash
# Do seu PC (após apontar DNS para 101):
nslookup doubleclick.net 192.168.1.101
# Esperado: responde com 0.0.0.0 (bloqueado)

nslookup google.com 192.168.1.101
# Esperado: IP real do Google (não bloqueado)

# Painel web mostra queries sendo filtradas:
# http://192.168.1.101 → Dashboard → Queries today
```

**🆘 Se DEU ERRADO:**
- `pct exec 101 -- journalctl -u AdGuardHome -n 50` — log do serviço
- Porta 53 já em uso: `pct exec 101 -- ss -tuln | grep :53` — systemd-resolved pode estar na frente; `pct exec 101 -- systemctl disable --now systemd-resolved`
- CT sem acesso à internet: verifique `pct exec 101 -- ping 1.1.1.1` — rota ou bridge errada

> **O que você aprende ao instalar:** como DNS funciona na prática, diferença entre DNS recursivo e autoritativo, DoH/DoT (DNS over HTTPS/TLS), listas de bloqueio e formatos (hosts file, Adblock), impacto de um DNS lento na rede inteira.

---

### D.2.2 Vaultwarden — guia rápido (CT 300)

Vaultwarden é o Bitwarden server reimplementado em Rust — leve, auto-hospedado, compatível com todos os clientes Bitwarden (Android, iOS, extensão de browser). Com ele, você tira suas senhas da nuvem e as guarda em casa, criptografadas, acessíveis via Tailscale de qualquer lugar.

🎯 **OBJETIVO:** CT 300 com Vaultwarden respondendo HTTPS na porta 443 via Tailscale  
⏱ **Tempo estimado:** 30–45 min

> **Pré-requisito:** CT 100 Tailscale funcionando (Fase 5). O Vaultwarden é acessado **exclusivamente via Tailscale** — nenhuma porta é aberta na internet.

```bash
# ── 1. Criar o CT 300 no host PVE ──
pct create 300 local:vztmpl/debian-12-standard_12.7-1_amd64.tar.zst \
  --hostname srv-vaultwarden-prod \
  --memory 256 \
  --rootfs local-lvm:4 \
  --net0 name=eth0,bridge=vmbr0,ip=192.168.1.300/24,gw=192.168.1.1 \
  --nameserver 192.168.1.101 \
  --unprivileged 1 \
  --start 1

# ── 2. Atualizar e instalar Docker (Vaultwarden roda em container) ──
pct exec 300 -- bash -c "apt update && apt upgrade -y"
pct exec 300 -- bash -c "apt install -y curl"
pct exec 300 -- bash -c "curl -fsSL https://get.docker.com | sh"

# ── 3. Snapshot antes de subir o serviço ──
pct stop 300
zfs snapshot rpool/data/subvol-300-disk-0@antes-vaultwarden
pct start 300

# ── 4. Criar estrutura de dados e subir Vaultwarden ──
pct exec 300 -- bash -c "mkdir -p /opt/vaultwarden/data"

# Criar o docker-compose.yml:
pct exec 300 -- bash -c "cat > /opt/vaultwarden/docker-compose.yml << 'EOF'
services:
  vaultwarden:
    image: vaultwarden/server:latest
    container_name: vaultwarden
    restart: unless-stopped
    ports:
      - \"80:80\"
    volumes:
      - /opt/vaultwarden/data:/data
    environment:
      - DOMAIN=http://192.168.1.300    # trocar pelo IP Tailscale quando configurado
      - SIGNUPS_ALLOWED=true           # desabilitar após criar a conta: SIGNUPS_ALLOWED=false
      - LOG_LEVEL=warn
EOF"

# Subir:
pct exec 300 -- bash -c "cd /opt/vaultwarden && docker compose up -d"

# Verificar:
pct exec 300 -- docker ps
# Esperado: vaultwarden Up X seconds
```

**Configuração inicial:**

1. Acesse `http://192.168.1.300` no navegador
2. Clique **Create account** → crie sua conta master
3. **IMEDIATAMENTE** após criar: `SIGNUPS_ALLOWED=false` no `docker-compose.yml` e `docker compose up -d` para reodar
4. Instale o cliente Bitwarden no browser/celular e aponte para `http://192.168.1.300`

**Acesso via Tailscale (recomendado):**
```bash
# No CT 300 — instalar Tailscale para acessar de fora de casa:
pct exec 300 -- bash -c "curl -fsSL https://tailscale.com/install.sh | sh"
pct exec 300 -- tailscale up --accept-routes

# Descobrir o IP Tailscale do CT 300:
pct exec 300 -- tailscale ip -4
# Exemplo: 100.x.x.x

# Atualizar DOMAIN no docker-compose.yml para o IP Tailscale:
# DOMAIN=http://100.x.x.x
# docker compose up -d (no CT 300)
```

**✅ Verifique:**
```bash
# Vaultwarden responde:
pct exec 300 -- curl -s http://localhost/alive
# Esperado: ok

# Container rodando após reboot:
pct exec 300 -- docker ps | grep vaultwarden
# Esperado: Up X hours (restart: unless-stopped garante reinício automático)

# Do seu celular via Tailscale:
# Bitwarden → Configurações → URL do servidor → http://100.x.x.x
# Fazer login → ver seus itens
```

**🆘 Se DEU ERRADO:**
- Container não sobe: `pct exec 300 -- docker compose logs` — ver erro específico
- Porta 80 em uso: `pct exec 300 -- ss -tuln | grep :80` — outro serviço na frente
- Dados perdidos após atualização: estão em `/opt/vaultwarden/data/` — snapshot ZFS protege
- Reset de senha master: impossível por design (E2E encryption) — use os recovery codes

**Backup do Vaultwarden:**
```bash
# Os dados ficam em /opt/vaultwarden/data/ no CT 300
# vzdump já inclui no backup agendado da Fase 10b — mas um backup manual extra:
pct exec 300 -- tar czf /tmp/vault-backup-$(date +%F).tar.gz -C /opt/vaultwarden/data .
pct pull 300 /tmp/vault-backup-$(date +%F).tar.gz /root/backups/
```

> **O que você aprende ao instalar:** Docker Compose na prática, variáveis de ambiente, volumes persistentes, diferença entre container stateless e stateful, por que `restart: unless-stopped` importa, End-to-End Encryption em aplicações web.

---

### D.2.3 Nginx Proxy Manager — guia rápido (CT 102)

Nginx Proxy Manager (NPM) é um reverse proxy com painel web que distribui tráfego HTTPS para seus serviços internos. Com ele, você transforma `http://192.168.1.300` (Vaultwarden) em `https://vault.casa` — com certificado Let's Encrypt real, sem linha de comando.

🎯 **OBJETIVO:** CT 102 com NPM como ponto central de HTTPS para todos os serviços do Nível 1  
⏱ **Tempo estimado:** 30–45 min

> **Pré-requisito 1:** um domínio próprio (ex.: `seunome.duckdns.org` — gratuito) **ou** uso só na LAN/Tailscale com certificado autoassinado.  
> **Pré-requisito 2:** CT 100 Tailscale ativo. O NPM fica acessível via Tailscale e roteia para os outros CTs.

```bash
# ── 1. Criar o CT 102 ──
pct create 102 local:vztmpl/debian-12-standard_12.7-1_amd64.tar.zst \
  --hostname net-nginx-proxy \
  --memory 512 \
  --rootfs local-lvm:6 \
  --net0 name=eth0,bridge=vmbr0,ip=192.168.1.102/24,gw=192.168.1.1 \
  --nameserver 192.168.1.101 \
  --unprivileged 1 \
  --start 1

# ── 2. Instalar Docker ──
pct exec 102 -- bash -c "apt update && apt upgrade -y && apt install -y curl"
pct exec 102 -- bash -c "curl -fsSL https://get.docker.com | sh"

# ── 3. Snapshot antes de subir ──
pct stop 102
zfs snapshot rpool/data/subvol-102-disk-0@antes-npm
pct start 102

# ── 4. Subir Nginx Proxy Manager ──
pct exec 102 -- bash -c "mkdir -p /opt/npm/data /opt/npm/letsencrypt"

pct exec 102 -- bash -c "cat > /opt/npm/docker-compose.yml << 'EOF'
services:
  npm:
    image: jc21/nginx-proxy-manager:latest
    container_name: nginx-proxy-manager
    restart: unless-stopped
    ports:
      - \"80:80\"      # HTTP (redireciona para HTTPS)
      - \"443:443\"    # HTTPS
      - \"81:81\"      # Painel de administração do NPM
    volumes:
      - /opt/npm/data:/data
      - /opt/npm/letsencrypt:/etc/letsencrypt
EOF"

pct exec 102 -- bash -c "cd /opt/npm && docker compose up -d"

# Verificar:
pct exec 102 -- docker ps
# Esperado: nginx-proxy-manager Up X seconds
```

**Acesso inicial ao painel:**

1. Abra `http://192.168.1.102:81` no browser
2. Login padrão: `admin@example.com` / senha `changeme`
3. **Troque imediatamente** o email e senha → salve no Bitwarden
4. Painel pronto — agora configure os Proxy Hosts

**Configurar Proxy Host para o Vaultwarden:**

No painel NPM → **Hosts → Proxy Hosts → Add Proxy Host**:

| Campo | Valor |
|-------|-------|
| Domain Names | `vault.192.168.1.102.nip.io` (LAN sem domínio) ou `vault.seudominio.com` |
| Scheme | `http` |
| Forward Hostname | `192.168.1.300` |
| Forward Port | `80` |
| Block Common Exploits | ✅ |
| SSL → Force SSL | ✅ (após configurar certificado) |

> **`nip.io` — domínio mágico sem cadastro:** `vault.192.168.1.102.nip.io` resolve automaticamente para `192.168.1.102`. Funciona na LAN sem configurar DNS. Não suporta Let's Encrypt (só LAN), mas resolve o HTTPS com certificado autoassinado.

**Let's Encrypt com DuckDNS (domínio gratuito):**

```bash
# 1. Cadastre-se em https://www.duckdns.org → crie subdomínio (ex: meuhomelab.duckdns.org)
# 2. Aponte para o IP do CT 102 (ou IP Tailscale)
# 3. No painel NPM → SSL Certificates → Add → Let's Encrypt
#    - Domain: *.meuhomelab.duckdns.org
#    - DNS Challenge: DuckDNS
#    - Token: (pego no painel duckdns.org)
# 4. Certificado wildcard válido para todos os subdomínios
```

**✅ Verifique:**
```bash
# NPM respondendo nas portas corretas:
pct exec 102 -- ss -tuln | grep -E ":80|:443|:81"

# Testar proxy do Vaultwarden via NPM (da sua LAN):
curl -Lk https://vault.192.168.1.102.nip.io
# Esperado: redirecionamento para o Vaultwarden

# Certificado válido (com domínio configurado):
curl -v https://vault.seudominio.com 2>&1 | grep -E "SSL|issuer|expire"
```

**🆘 Se DEU ERRADO:**
- Porta 80/443 não abre: verifique se o CT 102 tem rota para internet — `pct exec 102 -- curl -I https://google.com`
- Let's Encrypt falha: DuckDNS token errado ou propagação DNS ainda pendente (aguardar 5 min)
- Vaultwarden não abre via proxy: verifique se CT 300 responde em `http://192.168.1.300` diretamente
- `502 Bad Gateway`: forward hostname/port errado no Proxy Host

**Padrão para todos os serviços do Nível 1:**

```
AdGuard  → http://192.168.1.101  →  adguard.seudominio.com  (HTTPS via NPM)
Vault    → http://192.168.1.300  →  vault.seudominio.com    (HTTPS via NPM)
Kuma     → http://192.168.1.301  →  status.seudominio.com   (HTTPS via NPM)
```

> **O que você aprende ao instalar:** reverse proxy (como nginx distribui tráfego), TLS/SSL (certificados, CA, Let's Encrypt, ACME protocol), DNS challenge vs HTTP challenge, subdomínios wildcard, por que HTTPS importa mesmo na LAN (senhas em plaintext sem TLS).

---

### D.2.4 Uptime Kuma — guia rápido (CT 301)

Uptime Kuma monitora se seus serviços estão online e manda alerta no Telegram quando algo cair.

🎯 **OBJETIVO:** CT 301 com dashboard de status dos serviços + alertas Telegram automáticos  
⏱ **Tempo estimado:** 15–20 min

```bash
# ── 1. Criar CT 301 ──
pct create 301 local:vztmpl/debian-12-standard_12.7-1_amd64.tar.zst \
  --hostname srv-uptime-kuma \
  --memory 256 \
  --rootfs local-lvm:4 \
  --net0 name=eth0,bridge=vmbr0,ip=192.168.1.301/24,gw=192.168.1.1 \
  --unprivileged 1 --start 1

pct exec 301 -- bash -c "apt update && apt install -y curl && curl -fsSL https://get.docker.com | sh"

# ── 2. Subir Uptime Kuma ──
pct exec 301 -- bash -c "mkdir -p /opt/kuma && cat > /opt/kuma/docker-compose.yml << 'EOF'
services:
  uptime-kuma:
    image: louislam/uptime-kuma:1
    container_name: uptime-kuma
    restart: unless-stopped
    ports:
      - \"3001:3001\"
    volumes:
      - /opt/kuma/data:/app/data
EOF"

pct exec 301 -- bash -c "cd /opt/kuma && docker compose up -d"
```

**Configuração inicial:**

1. Acesse `http://192.168.1.301:3001` → crie usuário/senha → **Bitwarden**
2. **Add Monitor** → HTTP(s) → URL: `http://192.168.1.101` (AdGuard) → Friendly Name: `AdGuard Home`
3. Repetir para cada serviço: Vaultwarden, NPM, Tailscale (`http://100.x.x.x`)
4. **Settings → Notifications → Add → Telegram** → insira o Bot Token e Chat ID (do doc [docs/monitoramento-telegram-fortaleza-proxmox.md](../docs/monitoramento-telegram-fortaleza-proxmox.md))

**Resultado:** se o CT 300 (Vaultwarden) cair, você recebe mensagem no Telegram em menos de 2 minutos.

> **O que você aprende ao instalar:** conceito de health check HTTP, diferença entre monitoramento ativo (poll) e passivo (push), latência de rede interna, por que alertas são mais úteis que dashboards em homelabs pequenos.

---

## D.3 Nível 2 — Laboratórios de estudo (construa, aprenda, destrua)

VMs dedicadas a aprender tecnologias do zero — sem o peso de “não posso quebrar isso”. Cada VM tem snapshot antes de cada experiência.

| # | VM | Lab | O que vai aprender |
|---|----|-----|--------------------|
| 5 | VM 111 | **DNS bind9 do zero** | Zonas DNS, registros A/MX/CNAME/PTR, resolução recursiva, DNSSEC básico |
| 6 | VM 112 | **nginx do zero** | Virtual hosts, HTTPS com certbot, `proxy_pass`, `rate_limit`, gzip |
| 7 | VM 113 | **iptables/nftables raiz** | Chains INPUT/FORWARD/OUTPUT, MASQUERADE, DROP vs REJECT, regras stateful |
| 8 | VM 114 | **LAN cliente simulada** | Segmentar VMs em redes distintas (vmbr1), testar firewall, VLAN básico no PVE |

```bash
# Criar VM de lab rapidamente (clone da VM 110 base-limpa):
qm clone 110 111 --name lab-dns --full
qm set 111 --ipconfig0 ip=192.168.1.111/24,gw=192.168.1.1
qm start 111
# Em 30 segundos: ssh aluno@192.168.1.111 — ambiente limpo igual à VM 110

# Snapshot antes de instalar bind9:
qm snapshot 111 antes-bind9 --description “Lab DNS — antes de instalar bind9”

# Se tudo correu mal — rollback:
qm rollback 111 antes-bind9
```

**Sequência recomendada de estudo:**

```
VM 111 (DNS)  →  VM 112 (nginx)  →  VM 113 (firewall)  →  VM 114 (LAN)
    ↓                  ↓                    ↓                    ↓
 bind9 local      virtual hosts        iptables -L           vmbr1 isolada
 zonas DNS        SSL certbot          nft list ruleset       ping entre VMs
 dig/nslookup     proxy_pass           MASQUERADE             VLAN tag 10
```

---

### D.3.1 Lab DNS — bind9 do zero (VM 111)

🎯 **OBJETIVO:** Entender como o DNS funciona por dentro — criar seu próprio servidor autoritativo para uma zona inventada (`lab.local`) e responder queries reais com `dig`.  
⏱ **Tempo estimado:** 45–60 min

```bash
# ── No host PVE — clonar VM 110 (base-limpa) ──
qm clone 110 111 --name lab-dns --full
qm set 111 --ipconfig0 ip=192.168.1.111/24,gw=192.168.1.1
qm start 111
# Aguardar ~30 s → SSH:
ssh aluno@192.168.1.111

# ── Dentro da VM 111 ──
# Snapshot antes de começar:
# (do host: qm snapshot 111 antes-bind9)

# Instalar bind9:
sudo apt update && sudo apt install -y bind9 bind9-utils dnsutils

# Verificar serviço:
systemctl status named   # "active (running)"
```

**Criar a zona `lab.local` (servidor autoritativo):**

```bash
# Editar configuração principal:
sudo nano /etc/bind/named.conf.local
```

Cole no arquivo:
```
zone "lab.local" {
    type master;
    file "/etc/bind/zones/db.lab.local";
};
```

```bash
# Criar pasta de zonas:
sudo mkdir -p /etc/bind/zones

# Criar arquivo de zona:
sudo nano /etc/bind/zones/db.lab.local
```

Cole no arquivo:
```
$TTL    604800
@       IN  SOA  ns1.lab.local. admin.lab.local. (
                  2026051301  ; Serial (AAAAMMDDNN)
                  604800      ; Refresh
                  86400       ; Retry
                  2419200     ; Expire
                  604800 )    ; Negative Cache TTL

; Nameservers
@       IN  NS   ns1.lab.local.

; Registros A
ns1     IN  A    192.168.1.111
web     IN  A    192.168.1.112
mail    IN  A    192.168.1.120

; Alias (CNAME)
www     IN  CNAME web.lab.local.

; Registro MX
@       IN  MX   10 mail.lab.local.
```

```bash
# Verificar sintaxe do arquivo de zona:
sudo named-checkzone lab.local /etc/bind/zones/db.lab.local
# Esperado: "OK"

# Reiniciar bind9:
sudo systemctl restart named

# ── Testes com dig ──
# Query ao servidor local:
dig @192.168.1.111 web.lab.local
# Esperado: ANSWER SECTION com 192.168.1.112

dig @192.168.1.111 www.lab.local
# Esperado: CNAME → web.lab.local → 192.168.1.112

dig @192.168.1.111 lab.local MX
# Esperado: mail.lab.local. com prioridade 10

# Query a um domínio público (teste recursão):
dig @192.168.1.111 google.com
# Esperado: resposta (bind9 por padrão resolve recursivamente)
```

**Experimentos para aprofundar:**
```bash
# 1. Adicionar registro PTR (reverse DNS):
#    Crie zona "1.168.192.in-addr.arpa" e aponte 111 → ns1.lab.local.

# 2. Observar queries em tempo real:
sudo journalctl -u named -f
# Abra outro terminal e faça dig — veja os logs

# 3. Medir tempo de resposta com cache vs. sem cache:
dig @192.168.1.111 google.com | grep "Query time"  # primeira query
dig @192.168.1.111 google.com | grep "Query time"  # segunda (deve ser <5ms)

# 4. Destruir e recriar do zero:
# Do host: qm rollback 111 antes-bind9
```

> **O que você aprendeu:** estrutura de uma zona DNS (SOA, NS, A, CNAME, MX), como `dig` lê respostas (AUTHORITY vs ANSWER SECTION), diferença entre servidor autoritativo e recursivo, TTL e cache, por que o Serial importa ao atualizar zonas.

---

### D.3.2 Lab Web — nginx do zero (VM 112)

🎯 **OBJETIVO:** Servir uma página HTML real, configurar dois virtual hosts no mesmo servidor e entender como o nginx decide qual responder.  
⏱ **Tempo estimado:** 45–60 min

```bash
# ── No host PVE ──
qm clone 110 112 --name lab-nginx --full
qm set 112 --ipconfig0 ip=192.168.1.112/24,gw=192.168.1.1
qm start 112
ssh aluno@192.168.1.112

# ── Dentro da VM 112 ──
sudo apt update && sudo apt install -y nginx curl

# Verificar:
systemctl status nginx   # "active (running)"
curl http://localhost    # página padrão do nginx
```

**Criar dois virtual hosts:**

```bash
# Site 1 — site-a.local:
sudo mkdir -p /var/www/site-a
echo "<h1>Site A — funcionando!</h1>" | sudo tee /var/www/site-a/index.html

sudo nano /etc/nginx/sites-available/site-a
```

Cole:
```nginx
server {
    listen 80;
    server_name site-a.local 192.168.1.112;

    root /var/www/site-a;
    index index.html;

    access_log /var/log/nginx/site-a-access.log;
    error_log  /var/log/nginx/site-a-error.log;
}
```

```bash
# Site 2 — site-b.local:
sudo mkdir -p /var/www/site-b
echo "<h1>Site B — também funciona!</h1>" | sudo tee /var/www/site-b/index.html

sudo nano /etc/nginx/sites-available/site-b
```

Cole:
```nginx
server {
    listen 80;
    server_name site-b.local;

    root /var/www/site-b;
    index index.html;
}
```

```bash
# Ativar os sites:
sudo ln -s /etc/nginx/sites-available/site-a /etc/nginx/sites-enabled/
sudo ln -s /etc/nginx/sites-available/site-b /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default   # remover site padrão

# Verificar sintaxe:
sudo nginx -t
# Esperado: "syntax is ok" + "test is successful"

sudo systemctl reload nginx

# Testar (do seu PC — adicione ao /etc/hosts ou use curl com Host header):
curl -H "Host: site-a.local" http://192.168.1.112
# Esperado: <h1>Site A — funcionando!</h1>

curl -H "Host: site-b.local" http://192.168.1.112
# Esperado: <h1>Site B — também funciona!</h1>
```

**HTTPS com certificado autoassinado (para lab):**

```bash
# Gerar certificado autoassinado:
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /etc/ssl/private/lab.key \
  -out /etc/ssl/certs/lab.crt \
  -subj "/CN=site-a.local/O=Lab/C=BR"

# Adicionar bloco SSL no site-a:
sudo nano /etc/nginx/sites-available/site-a
```

Adicione após o bloco `server` existente:
```nginx
server {
    listen 443 ssl;
    server_name site-a.local;

    ssl_certificate     /etc/ssl/certs/lab.crt;
    ssl_certificate_key /etc/ssl/private/lab.key;

    root /var/www/site-a;
    index index.html;
}
```

```bash
sudo nginx -t && sudo systemctl reload nginx

# Testar HTTPS (ignorar aviso de cert autoassinado):
curl -k https://192.168.1.112
```

**Experimentos para aprofundar:**
```bash
# 1. Proxy reverso (nginx como intermediário para outro serviço):
#    No site-b, troque root/index por:
#    location / { proxy_pass http://192.168.1.101; }  # proxeia para AdGuard

# 2. Ver logs de acesso em tempo real:
sudo tail -f /var/log/nginx/site-a-access.log
# Faça um curl de outro terminal — veja o log aparecer

# 3. Rate limiting (proteção básica):
#    No nginx.conf, dentro de http{}: limit_req_zone $binary_remote_addr zone=one:10m rate=10r/s;
#    No server{}: limit_req zone=one burst=20;
```

> **O que você aprendeu:** como o nginx usa o header `Host` para selecionar o virtual host, blocos `server {}` e `location {}`, diferença entre `sites-available` (existe) e `sites-enabled` (ativo), como TLS funciona (chave privada + certificado público), por que `nginx -t` antes de `reload` é obrigatório.

---

### D.3.3 Lab Firewall — nftables do zero (VM 113)

🎯 **OBJETIVO:** Construir um firewall do zero com nftables — entender chains, hooks, tabelas e a lógica de DROP vs REJECT sem abstração de ferramentas.  
⏱ **Tempo estimado:** 45–60 min

```bash
# ── No host PVE ──
qm clone 110 113 --name lab-nftables --full
qm set 113 --ipconfig0 ip=192.168.1.113/24,gw=192.168.1.1
qm start 113
ssh aluno@192.168.1.113

# ── Dentro da VM 113 ──
sudo apt update && sudo apt install -y nftables

# Ver o estado atual (Debian já tem nftables ativo):
sudo nft list ruleset
# Deve mostrar tabelas existentes (ou vazio se limpo)
```

**Construir um firewall do zero:**

```bash
# Limpar tudo e começar do zero:
sudo nft flush ruleset

# Criar tabela e chains:
sudo nft add table inet filtro

# Chain de entrada (tráfego chegando à VM):
sudo nft add chain inet filtro entrada '{ type filter hook input priority 0; policy drop; }'

# Chain de saída (tráfego saindo da VM):
sudo nft add chain inet filtro saida '{ type filter hook output priority 0; policy accept; }'

# Chain de encaminhamento (entre interfaces — não usamos aqui):
sudo nft add chain inet filtro encaminhamento '{ type filter hook forward priority 0; policy drop; }'

# Regras essenciais (sem estas, você perde o SSH!):
sudo nft add rule inet filtro entrada ct state established,related accept   # respostas de conexões existentes
sudo nft add rule inet filtro entrada iif lo accept                          # loopback sempre OK
sudo nft add rule inet filtro entrada ip protocol icmp accept                # ping (diagnóstico)
sudo nft add rule inet filtro entrada tcp dport 22 accept                    # SSH

# Ver o resultado:
sudo nft list ruleset
```

**Testar o firewall na prática:**

```bash
# Do seu PC — confirmar SSH ainda funciona:
ssh aluno@192.168.1.113   # deve continuar funcionando

# Tentar uma porta bloqueada (do seu PC):
curl --connect-timeout 3 http://192.168.1.113
# Esperado: timeout (porta 80 não está na allowlist)

# Abrir porta 80 temporariamente:
sudo nft add rule inet filtro entrada tcp dport 80 accept

# Testar novamente:
curl --connect-timeout 3 http://192.168.1.113
# Esperado: conexão recusada (porta aberta mas nginx não instalado) ou página nginx

# Remover a regra de porta 80 (índice da regra):
sudo nft list ruleset -a          # ver handle de cada regra
sudo nft delete rule inet filtro entrada handle <N>   # N = handle da regra porta 80
```

**DROP vs REJECT — a diferença real:**

```bash
# DROP: pacote some sem resposta (atacante não sabe se porta existe)
# REJECT: responde com "connection refused" (mais rápido para o cliente legítimo, mas revela que a porta existe)

# Adicionar REJECT para SSH de IP específico (exemplo de blocklist):
sudo nft add rule inet filtro entrada ip saddr 192.168.1.50 tcp dport 22 reject

# Ver contadores de pacotes por regra:
sudo nft list ruleset -a    # mostra packets e bytes por regra
```

**Persistir as regras após reboot:**

```bash
# Exportar configuração atual:
sudo nft list ruleset > /etc/nftables.conf

# Habilitar serviço de persistência:
sudo systemctl enable nftables
sudo systemctl start nftables

# Verificar após reboot (do host: qm reboot 113):
sudo nft list ruleset   # regras devem estar intactas
```

> **O que você aprendeu:** estrutura do nftables (tabelas → chains → regras), conceito de hook e priority, `ct state established,related` (stateful firewall), diferença entre DROP e REJECT, por que a **ordem das regras importa** (primeira que bate ganha), como persistir regras. Agora você entende o que o `proxmox-firewall` faz por baixo dos panos.

---

### D.3.4 Lab Rede — LAN simulada com duas redes (VM 114)

🎯 **OBJETIVO:** Criar duas redes virtuais isoladas no Proxmox, colocar VMs em cada uma e testar o roteamento — entender como VLANs e bridges funcionam na prática.  
⏱ **Tempo estimado:** 30–45 min

```bash
# ── No host PVE — criar uma segunda bridge vmbr1 ──
# Editar configuração de rede:
sudo nano /etc/network/interfaces
```

Adicione ao final:
```
# Bridge para lab isolado (sem gateway — rede interna pura):
auto vmbr1
iface vmbr1 inet static
    address 10.10.10.1/24
    bridge-ports none
    bridge-stp off
    bridge-fd 0
    # Rede de lab — não conectada à internet
```

```bash
# Aplicar sem reboot:
sudo ifreload -a

# Confirmar:
ip addr show vmbr1
# Esperado: 10.10.10.1/24 UP
```

**Criar duas VMs na rede isolada:**

```bash
# VM 114-A — "servidor" na rede 10.10.10.x:
qm clone 110 114 --name lab-lan-servidor --full
qm set 114 --net0 virtio,bridge=vmbr1   # conectar à bridge isolada
qm set 114 --ipconfig0 ip=10.10.10.10/24,gw=10.10.10.1
qm start 114

# VM 115-B — "cliente" na mesma rede:
qm clone 110 115 --name lab-lan-cliente --full
qm set 115 --net0 virtio,bridge=vmbr1
qm set 115 --ipconfig0 ip=10.10.10.20/24,gw=10.10.10.1
qm start 115
```

**Testar conectividade entre as VMs:**

```bash
# Na VM 114 (10.10.10.10):
ssh aluno@10.10.10.10   # via Tailscale ou console PVE

ping 10.10.10.20        # deve responder (mesma bridge)
ping 192.168.1.1        # DEVE FALHAR — rede isolada, sem rota para fora

# Na VM 115 (10.10.10.20):
ping 10.10.10.10        # responde
traceroute 10.10.10.10  # 1 hop direto (mesma L2)

# Do host PVE:
ping 10.10.10.10        # responde (host é o gateway 10.10.10.1)
ping 10.10.10.20        # responde
```

**Experimento: VM com duas interfaces (uma LAN, uma interna):**

```bash
# Adicionar segunda NIC à VM 112 (nginx) para ela falar com a rede de lab:
qm set 112 --net1 virtio,bridge=vmbr1
qm set 112 --ipconfig1 ip=10.10.10.112/24

# Dentro da VM 112:
ip addr   # ver eth0 (192.168.1.112) + eth1 (10.10.10.112)

# Da VM 114 (rede isolada):
curl http://10.10.10.112   # acessa o nginx da VM 112 pela rede interna
```

**Entender VLAN tags (conceito):**

```bash
# No PVE, ao criar uma NIC você pode adicionar VLAN tag:
qm set 114 --net0 virtio,bridge=vmbr0,tag=10
# VLAN 10 — o switch/bridge só entrega esse tráfego para interfaces com tag=10
# Útil para isolar IoT, câmeras, VMs de lab sem criar bridge separada

# Ver VLANs ativas:
bridge vlan show
```

**Limpar o lab:**

```bash
# Parar e destruir as VMs de teste:
qm stop 114 && qm destroy 114
qm stop 115 && qm destroy 115

# Remover vmbr1 (opcional — pode manter para labs futuros):
# Editar /etc/network/interfaces → remover bloco vmbr1 → ifreload -a
```

> **O que você aprendeu:** diferença entre L2 (bridge/switch) e L3 (roteamento IP), por que VMs na mesma bridge se veem sem gateway, como o host PVE age como roteador entre bridges, conceito de VLAN tag e isolamento de tráfego, por que "rede isolada" é importante para labs com serviços perigosos.

---

## D.4 Nível 3 — Infraestrutura avançada (quando os fundamentos estiverem sólidos)

| # | CT/VM | App | Pré-requisito | O que aprende |
|---|-------|-----|---------------|---------------|
| 9 | VM 900 | **Proxmox Backup Server** | Ter feito Fase 10b | Backups incrementais, deduplicação, datastores, verificação de integridade |
| 10 | PC | **Ansible** | Ter instalado 3+ CTs manualmente | IaC, playbooks, roles, `community.general.proxmox` module |
| 11 | CT | **Prometheus + Grafana** | Ter Uptime Kuma funcionando | Métricas de sistema, PromQL, dashboards, alertas por threshold |
| 12 | VM | **k3s (Kubernetes leve)** | Dominar Docker Compose | Pods, Services, Ingress, ConfigMaps, PersistentVolumes |
| 13 | CT 103 | **Tor Hidden Service (rede .onion)** | Fases 0–7 concluídas + entender TCP/IP | Anonimato em camadas, Hidden Services `.onion`, acesso SSH via Tor sem expor IP público, Tails OS compatível |

> **Docker / Kubernetes:** não é preciso Swarm nem cluster completo para começar — primeiro containers, volumes e redes isoladas. Ver Fase 8 do guia. Orquestração vem depois dos fundamentos.

> **Tor Hidden Service:** guia completo no Apêndice N — CT 103, configuração `.onion`, Tails OS, Android/Orbot, backup de chaves GPG.

---

### D.4.1 Prometheus + Grafana — métricas do N5095 (CT 400)

🎯 **OBJETIVO:** Dashboard visual em tempo real do host PVE — CPU, RAM, temperatura, ZFS, CTs/VMs — acessível pelo browser via Tailscale.  
⏱ **Tempo estimado:** 45–60 min  
> **Pré-requisito:** Uptime Kuma funcionando (D.2.4) — você já entende monitoramento. Prometheus é o próximo nível: métricas numéricas em séries temporais com queries.

```bash
# ── No host PVE — instalar Node Exporter (coleta métricas do host) ──
# Node Exporter roda no HOST (não em CT) para ter acesso real ao hardware
wget https://github.com/prometheus/node_exporter/releases/download/v1.8.2/node_exporter-1.8.2.linux-amd64.tar.gz
tar xzf node_exporter-*.tar.gz
sudo cp node_exporter-*/node_exporter /usr/local/bin/
sudo chmod +x /usr/local/bin/node_exporter

# Criar serviço systemd:
sudo tee /etc/systemd/system/node-exporter.service << 'EOF'
[Unit]
Description=Prometheus Node Exporter
After=network.target

[Service]
User=nobody
ExecStart=/usr/local/bin/node_exporter \
  --collector.systemd \
  --collector.processes \
  --web.listen-address=127.0.0.1:9100
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable --now node-exporter

# Verificar (só acessível localmente por segurança):
curl -s http://127.0.0.1:9100/metrics | grep node_load1
# Esperado: node_load1{} 0.XX
```

```bash
# ── Criar CT 400 com Prometheus + Grafana ──
pct create 400 local:vztmpl/debian-12-standard_12.7-1_amd64.tar.zst \
  --hostname srv-prometheus \
  --memory 512 \
  --rootfs local-lvm:8 \
  --net0 name=eth0,bridge=vmbr0,ip=192.168.1.400/24,gw=192.168.1.1 \
  --unprivileged 1 --start 1

pct exec 400 -- bash -c "apt update && apt install -y curl && curl -fsSL https://get.docker.com | sh"
pct exec 400 -- bash -c "mkdir -p /opt/monitoring"

# Criar docker-compose com Prometheus + Grafana:
pct exec 400 -- bash -c "cat > /opt/monitoring/docker-compose.yml << 'EOF'
services:
  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus
    restart: unless-stopped
    ports:
      - \"9090:9090\"
    volumes:
      - /opt/monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    command:
      - \"--config.file=/etc/prometheus/prometheus.yml\"
      - \"--storage.tsdb.retention.time=30d\"

  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    restart: unless-stopped
    ports:
      - \"3000:3000\"
    volumes:
      - grafana_data:/var/lib/grafana
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=fortaleza123   # trocar após login!

volumes:
  prometheus_data:
  grafana_data:
EOF"

# Criar configuração do Prometheus (scrape do Node Exporter no host):
pct exec 400 -- bash -c "cat > /opt/monitoring/prometheus.yml << 'EOF'
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'node-pve'
    static_configs:
      - targets: ['192.168.1.100:9100']   # IP do host PVE
    relabel_configs:
      - source_labels: [__address__]
        target_label: instance
        replacement: 'fortaleza-pve'
EOF"

# Nota: Node Exporter escuta em 127.0.0.1:9100 no host.
# Para o CT 400 alcançar, abra para a LAN:
# No host: editar /etc/systemd/system/node-exporter.service
# Trocar --web.listen-address=127.0.0.1:9100 por --web.listen-address=192.168.1.100:9100
# sudo systemctl daemon-reload && sudo systemctl restart node-exporter

pct exec 400 -- bash -c "cd /opt/monitoring && docker compose up -d"
```

**Configurar Grafana:**

1. Acesse `http://192.168.1.400:3000` → login `admin` / `fortaleza123` → **troque a senha** → Bitwarden
2. **Connections → Data Sources → Add → Prometheus** → URL: `http://prometheus:9090` → Save & Test
3. **Dashboards → Import** → ID: `1860` (Node Exporter Full — dashboard pronto da comunidade)
4. Resultado: dashboard com CPU, RAM, disco, rede, temperatura, carga — tudo do N5095

**Queries PromQL úteis para explorar:**

```promql
# Percentual de CPU usada:
100 - (avg(rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)

# RAM disponível em MB:
node_memory_MemAvailable_bytes / 1024 / 1024

# Uso do disco raiz:
(node_filesystem_size_bytes{mountpoint="/"} - node_filesystem_avail_bytes{mountpoint="/"}) / node_filesystem_size_bytes{mountpoint="/"} * 100

# Load average 1 min:
node_load1
```

> **O que você aprendeu:** pull vs push em monitoramento (Prometheus coleta ativamente), séries temporais e labels, PromQL (query language), por que retenção de 30 dias é suficiente para homelab, diferença entre alertas reativos (Uptime Kuma) e análise de tendência (Grafana — "a RAM vem crescendo há 3 dias").

---

### D.4.2 Ansible — automatizar tudo que você já faz à mão

🎯 **OBJETIVO:** Criar um playbook que instala e configura um CT novo em segundos — o que antes levava 20 min de comandos manuais, agora é `ansible-playbook` e pronto.  
⏱ **Tempo estimado:** 60–90 min  
> **Pré-requisito:** ter criado pelo menos 3 CTs manualmente (D.2.x). Você precisa saber o que está automatizando antes de automatizar.

```bash
# ── No seu PC (Linux/WSL/Mac) — instalar Ansible ──
# Ubuntu/Debian:
sudo apt update && sudo apt install -y ansible

# Verificar:
ansible --version
# Esperado: ansible [core 2.x.x]
```

**Estrutura do projeto Ansible:**

```bash
mkdir -p ~/ansible-fortaleza/{inventory,playbooks,roles}
cd ~/ansible-fortaleza

# Arquivo de inventário — define os hosts que o Ansible gerencia:
cat > inventory/hosts.ini << 'EOF'
[pve]
fortaleza ansible_host=100.X.X.X ansible_user=renato ansible_python_interpreter=/usr/bin/python3

[cts]
adguard    ansible_host=192.168.1.101 ansible_user=root ansible_python_interpreter=/usr/bin/python3
vaultwarden ansible_host=192.168.1.300 ansible_user=root ansible_python_interpreter=/usr/bin/python3

[all:vars]
ansible_ssh_private_key_file=~/.ssh/id_ed25519
EOF

# Testar conectividade:
ansible all -i inventory/hosts.ini -m ping
# Esperado: fortaleza | SUCCESS, adguard | SUCCESS, vaultwarden | SUCCESS
```

**Playbook 1 — verificar saúde de todos os hosts:**

```bash
cat > playbooks/health-check.yml << 'EOF'
---
- name: Health check de todos os hosts
  hosts: all
  gather_facts: yes
  tasks:

    - name: Mostrar uptime
      command: uptime -p
      register: uptime_output
      changed_when: false

    - name: Mostrar uso de RAM
      shell: free -h | grep Mem | awk '{print "Total:" $2 " Usado:" $3 " Livre:" $4}'
      register: ram_output
      changed_when: false

    - name: Verificar serviços críticos (só no PVE)
      systemd:
        name: "{{ item }}"
      loop:
        - pvedaemon
        - proxmox-firewall
        - ssh
      when: "'pve' in group_names"
      check_mode: yes

    - name: Exibir resultados
      debug:
        msg:
          - "Host: {{ inventory_hostname }}"
          - "Uptime: {{ uptime_output.stdout }}"
          - "RAM: {{ ram_output.stdout }}"
EOF

# Rodar:
ansible-playbook -i inventory/hosts.ini playbooks/health-check.yml
```

**Playbook 2 — criar e configurar um novo CT:**

```bash
cat > playbooks/criar-ct-base.yml << 'EOF'
---
- name: Criar CT base no Proxmox
  hosts: pve
  vars:
    ct_id: 105
    ct_name: "novo-servico"
    ct_ip: "192.168.1.105"
    ct_memory: 256
  tasks:

    - name: Criar CT com pct
      command: >
        pct create {{ ct_id }}
        local:vztmpl/debian-12-standard_12.7-1_amd64.tar.zst
        --hostname {{ ct_name }}
        --memory {{ ct_memory }}
        --rootfs local-lvm:4
        --net0 name=eth0,bridge=vmbr0,ip={{ ct_ip }}/24,gw=192.168.1.1
        --unprivileged 1
        --start 1
      register: ct_create
      changed_when: ct_create.rc == 0

    - name: Aguardar CT iniciar
      wait_for:
        host: "{{ ct_ip }}"
        port: 22
        delay: 5
        timeout: 60

    - name: Confirmar criação
      debug:
        msg: "CT {{ ct_id }} ({{ ct_name }}) criado em {{ ct_ip }}"

- name: Configurar CT recém-criado
  hosts: "{{ ct_ip }}"     # conecta direto ao CT
  gather_facts: yes
  tasks:

    - name: Atualizar pacotes
      apt:
        update_cache: yes
        upgrade: dist

    - name: Instalar pacotes base
      apt:
        name:
          - curl
          - vim
          - htop
          - unattended-upgrades
        state: present

    - name: Tirar snapshot pós-configuração
      delegate_to: "{{ groups['pve'][0] }}"
      command: "pct snapshot {{ ct_id }} pos-ansible --description 'Configurado via Ansible'"
EOF

ansible-playbook -i inventory/hosts.ini playbooks/criar-ct-base.yml \
  -e "ct_id=105 ct_name=teste-ansible ct_ip=192.168.1.105"
```

**Playbook 3 — atualizar todos os CTs de uma vez:**

```bash
cat > playbooks/update-all.yml << 'EOF'
---
- name: Atualizar todos os hosts gerenciados
  hosts: all
  become: yes
  serial: 2          # atualizar 2 hosts em paralelo
  tasks:

    - name: apt update + upgrade
      apt:
        update_cache: yes
        upgrade: dist
        autoremove: yes

    - name: Verificar se precisa de reboot
      stat:
        path: /var/run/reboot-required
      register: reboot_needed

    - name: Avisar se reboot for necessário
      debug:
        msg: "⚠️  {{ inventory_hostname }} precisa de reboot!"
      when: reboot_needed.stat.exists
EOF

ansible-playbook -i inventory/hosts.ini playbooks/update-all.yml
```

> **O que você aprendeu:** idempotência (rodar o mesmo playbook duas vezes não quebra nada), inventário (Ansible não sabe nada sem um inventário), `gather_facts` (Ansible coleta info do host antes de agir), `delegate_to` (executar tarefa em host diferente do target), `serial` (quantos hosts em paralelo), por que IaC (Infrastructure as Code) escala e "fazer na mão" não escala.

---

## D.5 Como abusar dos LXCs sem sobrecarregar o servidor

```bash
# Ver RAM usada por todos os guests (CTs e VMs):
for vmid in $(pct list | awk 'NR>1{print $1}'); do
  name=$(pct config $vmid | grep hostname | cut -d' ' -f2)
  mem=$(pct config $vmid | grep memory | cut -d' ' -f2)
  status=$(pct status $vmid | cut -d' ' -f2)
  echo “CT $vmid ($name): ${mem}MB — $status”
done

# Ver RAM usada pelas VMs:
qm list

# Desligar o que não está a usar (libera RAM instantaneamente):
pct stop 301   # Uptime Kuma — desliga quando não precisar de alertas
qm stop 113    # Lab iptables — só liga quando estiver estudando

# Clonar CT em segundos para um lab novo:
pct clone 101 115 --hostname lab-novo --full
pct set 115 --ipconfig0 ip=192.168.1.115/24,gw=192.168.1.1
pct start 115

# Ver uso de disco de cada CT/VM:
pct df 101
```

**Regras para não sobrecarregar o N5095:**
- Mantenha sempre ligados: host PVE + CT 100 (Tailscale) = ~860 MB
- Liga CTs de serviço (AdGuard, Vaultwarden) só quando precisar de testar
- VMs de lab: uma de cada vez — estudar duas coisas ao mesmo tempo não funciona bem
- ZFS ARC usa RAM livre automaticamente como cache — é normal ver 70–80% de RAM “usada”

---

## D.6 VM vs LXC — tabela de decisão rápida

Sempre que for criar um novo ambiente, use esta tabela para decidir o tipo certo:

| Critério | VM (KVM/QEMU) | LXC (Container) |
|----------|---------------|-----------------|
| **Sistema operacional** | Qualquer (Windows, BSD, Linux) | Apenas Linux |
| **Isolamento** | Total — kernel próprio | Parcial — compartilha kernel do host |
| **Performance** | Mais pesado (~200–500 MB RAM base) | Muito leve (~50–100 MB RAM base) |
| **Snapshots ZFS** | ✅ Sim | ✅ Sim |
| **Tempo de criação** | 2–5 min (com Cloud-Init) | 30 segundos |
| **Docker dentro** | ✅ Sim (direto) | ✅ Sim (com `nesting=1`) |
| **Passthrough hardware** | ✅ USB, GPU, PCIe | ❌ Limitado |
| **Uso ideal** | Windows, banco de dados pesado, apps que exigem kernel próprio | DNS, proxy, Tailscale, serviços leves, labs Linux |

**Regra prática para o Fortaleza:**
- `lxc-*` → serviços de infraestrutura (CT 100 Tailscale, CT 103 Tor, CT 101 AdGuard)
- `vm-*` → laboratórios de estudo (VM 110 Debian, VM 111 DNS lab, VM 112 nginx lab)
- Dúvida? Comece com LXC — se precisar de kernel próprio ou Windows, mude para VM.

---

# ❓ Apêndice E — FAQ

**P: Por que migrar para nftables se iptables ainda funciona?**
R: No Proxmox VE 9, `proxmox-firewall` (nftables) é onde a equipa investe (regras forward, VNets SDN, etc.). O backend clássico `pve-firewall` (iptables) continua disponível. A wiki descreve o backend nftables como *tech preview* e **não recomendada para produção** — em homelab, com backups e consciência do risco, é uma escolha comum.

**P: Port Knocking (bater na porta) é necessário neste setup?**
R: **Não** — e seria incompatível. Port Knocking pressupõe que a porta 22 está exposta à internet e filtrada pelo firewall. Neste guia, §7.5 remove todo o port forwarding do router — a porta 22 **não existe** na internet, está atrás de NAT. A sequência de knock nunca chegaria ao servidor. Além disso, o Tailscale já resolve o problema de forma superior: WireGuard cifrado, zero portas expostas, autenticado por chave criptográfica. Port Knocking é segurança por obscuridade; Tailscale é segurança por criptografia real. Ver §7.7 para análise completa.

**P: Posso acessar o servidor a partir do Tails OS?**
R: **Com dificuldade — Tails é um caso especial.** O Tails roteia todo o tráfego pelo Tor e bloqueia conexões directas para prevenir leaks de IP. Isso torna Tailscale inoperacional no Tails. As opções são:

1. **Tor Hidden Service no servidor (recomendado para Tails):** instalar `tor` no host PVE, configurar um Hidden Service `.onion` para a porta 22, e ligar com `ssh -o ProxyCommand="nc -X 5 -x 127.0.0.1:9050 %h %p" user@XXXXX.onion` no Tails. Requer configuração adicional não coberta neste guia — ver [Tor Hidden Service](https://community.torproject.org/onion-services/setup/).
2. **ShellHub Cloud via browser Tor:** aceder `app.shellhub.io` pelo browser Tor no Tails → conectar ao CT 200 → SSH para o host pela LAN interna. Funciona sem configuração extra no servidor.

Para uso ocasional a partir do Tails, a opção 2 (ShellHub via browser) é a mais simples.

**P: Posso usar Termius no celular em 4G?**
R: **Sim** — via Tailscale. Instale o Tailscale no celular (Play Store / App Store), logue com a mesma conta, e configure o Termius para conectar ao IP Tailscale do servidor (ex.: `100.x.x.x`, descoberto com `sudo pct exec 100 -- tailscale ip -4`). Funciona em 4G, Wi-Fi de café, qualquer rede — sem expor a porta 22 à internet. Ver §5.6b para o guia passo a passo.

**P: Posso usar este guia em outro servidor Debian, sem Proxmox?**
R: Fases 0 (parcial), 1–4, 9 e 10 funcionam em qualquer Debian 13. Fases 5, 7 e 8 envolvem features específicas do Proxmox.

**P: Este guia substitui o plano “Linux Foundation Lab” (Debian bare metal)?**
R: **Evolui** a partir da mesma filosofia (fundamentos, segurança, GPG, redes, sem port forwarding), mas o **caminho atual** é **Proxmox no mini PC**, não Debian minimal como único SO no metal. Comandos de estudo e UFW/`fail2ban` **dentro de VMs** continuam no cheat sheet [docs/linux-comandos-fundamentos.md](docs/linux-comandos-fundamentos.md); o **host** segue as fases Fortaleza (firewall PVE, CrowdSec, etc.). Ver também [docs/roadmap-hardware.md](docs/roadmap-hardware.md).

**P: E se eu errar e me trancar fora?**
R: Console físico do Mini PC sempre funciona. O **detalhe** do runbook está em `~/fortaleza-lab/recuperacao.md` (Fase 10); o **Apêndice H** abaixo é só um resumo dos primeiros passos.

**P: Preciso pagar por algo?**
R: Não. Tailscale (até 100 dispositivos), ShellHub Cloud Community, CrowdSec, Proxmox Community — todos gratuitos.

**P: Quanto de RAM isso tudo gasta?**
R: ~600 MB extras com tudo rodando (Proxmox + Tailscale CT + ShellHub CT + CrowdSec + bouncer). Sobra ~14-15 GB para seus labs.

**P: Comandos e versões deste guia vão desatualizar com o tempo?**
R: **Sim.** Nomes de pacotes, menus da GUI e detalhes de `nft`/`sshd` mudam entre *point releases*. Antes de cada `dist-upgrade` ou mudança grande, confirme com `pveversion`, [wiki Proxmox](https://pve.proxmox.com/wiki/Main_Page), [release notes / anúncios](https://forum.proxmox.com/forums/announcements.11/) e a [matriz de auditoria](docs/audit-matrix.md). A **ordem das fases** e a lógica (NTP antes de 2FA, backup antes de firewall) permanecem válidas.

**P: Posso usar ProxMenux para facilitar a administração?**
R: **Sim, como opcional.** O [ProxMenux](https://proxmenux.com/) é um menu interativo para tarefas no host e em guests — veja a seção no início do guia e a [documentação](https://proxmenux.com/docs/introduction). Trate-o como **terceiro**: revise código e guias de instalação antes de executar; não invalida a ordem nem a segurança das fases Fortaleza.

**P: E se eu perder o celular do 2FA?**
R: Use os códigos de recuperação salvos no Bitwarden. Em última instância, acesse pelo console físico como root e edite com cuidado `/etc/pam.d/sshd` (ex.: `sudo nano /etc/pam.d/sshd`).

**P: O Proxmox 9.x atualiza entre minor (ex. 9.1 → 9.2) sem quebrar isso?**
R: Em geral, sim: configurações em `sshd_config.d/`, snapshots e regras de firewall na GUI tendem a ser preservadas em *point releases*. Sempre leia as [release notes](https://forum.proxmox.com/forums/announcements.11/) e faça backup de `/etc/pve` antes de subir major/minor.

**P: Devo usar Wi-Fi no Mini PC?**
R: NÃO. Sempre cabo Ethernet. Wi-Fi adiciona instabilidade e complexidade desnecessária.

**P: O `AllowTcpForwarding no` no host impede o meu irmão de usar ShellHub ou `ssh -L` para debug?**
R: **ShellHub (CT do irmão):** não depende de `AllowTcpForwarding` no **sshd** do host Proxmox — o agente fala com a cloud ShellHub por fora do seu endurecimento SSH do PVE. **`ssh -L` / `-D` para o host PVE:** sim, com `AllowTcpForwarding no` o OpenSSH desativa esse encaminhamento; se precisares, ajusta só no drop-in (com consciência do risco) ou faz o túnel **a partir de uma VM/CT** de laboratório, não do host endurecido.

**P: O NTP é mesmo tão importante?**
R: SIM. Sem NTP sincronizado, o 2FA TOTP simplesmente não funciona — os códigos do servidor não batem com os do celular.

**P: Posso usar este guia em produção (empresa)?**
R: Os fundamentos sim. Mas para produção, considere também: backups offsite obrigatórios, monitoring centralizado (Prometheus + Grafana), alertas, gestão de patches mais rigorosa, e Proxmox Subscription Enterprise (suporte oficial).

---

# 📚 Apêndice F — Glossário Expandido

Veja a seção **Glossário completo** no topo do documento (âncora interna `#glossario-completo`), ou o atalho [docs/glossario.md](docs/glossario.md).

---

# 🔐 Apêndice G — O Que Guardar no Bitwarden

Crie a pasta "Fortaleza Proxmox" com:

| # | Item | Onde aparece no guia |
|---|------|----------------------|
| 1 | Senha root Proxmox | Instalação inicial |
| 2 | Senha usuário `renato` | Fase 1 |
| 3 | Passphrase chave SSH `chave_fortaleza` | Fase 2 |
| 4 | Conteúdo da chave privada `chave_fortaleza` | Fase 2 (backup) |
| 5 | 2FA SSH renato — chave secreta TOTP | Fase 3 |
| 6 | 2FA SSH renato — 5 códigos de recuperação | Fase 3 |
| 7 | 2FA painel renato@pam — chave secreta TOTP | Fase 6 |
| 8 | 2FA painel renato@pam — recovery keys | Fase 6 |
| 9 | Senha root CT 100 (vpn-tailscale) | Fase 5 |
| 10 | Conta Tailscale (Google/GitHub OAuth) | Fase 5 |
| 11 | Senha root CT 200 (lab-irmao-gpg) | Fase 8 |
| 12 | Senha usuário `irmao` no CT 200 | Fase 8 |
| 13 | Conta ShellHub Cloud (email/senha) | Fase 8 |
| 14 | CrowdSec Console enroll token (se usar) | Fase 4 |

**Bônus:** imprima os códigos de recuperação 2FA e guarde **fisicamente** em local seguro (cofre, gaveta trancada). Se Bitwarden cair, você ainda tem como entrar.

---

# 🛟 Apêndice H — Plano de Recuperação de Desastre

Já está documentado em `~/fortaleza-lab/recuperacao.md` (criado na Fase 10).

Resumo:

| Cenário | Primeiro passo |
|---------|----------------|
| Não consigo logar SSH | Console físico do Mini PC |
| Perdi celular do 2FA | Códigos de recuperação no Bitwarden |
| Mini PC quebrou | Reinstala PVE, restaura backup de `/etc/pve` |
| Me bani no CrowdSec | Console físico → `sudo cscli decisions delete --ip MEU_IP` |
| Firewall me trancou | Console → `sudo pve-firewall stop` |
| VM/CT corrompida | Restaurar com `pct restore` / `qmrestore` (ver Fase 10b) |
| Snapshot ZFS errado | `zfs rollback` (ver abaixo) |

---

## H.1 Restaurar snapshot ZFS

Os snapshots criados em cada fase (ex.: `zfs snapshot rpool/ROOT/pve-1@antes-fase-2`) podem ser revertidos com `zfs rollback`.

```bash
# Listar snapshots disponíveis:
zfs list -t snapshot -o name,creation,used | sort -k2

# Reverter para um snapshot específico (CUIDADO: apaga tudo feito DEPOIS do snapshot):
# Primeiro, confirme o nome exato:
zfs list -t snapshot | grep antes-fase

# Fazer o rollback (requer que a VM/CT associada esteja parada se for dataset de dados):
zfs rollback rpool/ROOT/pve-1@antes-fase-3

# Verificar que o rollback funcionou:
zfs list -t snapshot | grep pve-1
# O snapshot alvo deve ser o mais recente agora
```

> ⚠️ **`zfs rollback` apaga snapshots mais recentes** que o alvo (por padrão). Use `zfs rollback -r` para forçar se houver snapshots intermediários. Verifique **duas vezes** o nome do snapshot antes de executar.

```bash
# Exemplo completo — reverter o nó para o estado antes da Fase 3:
# 1. Confirmar o snapshot:
zfs list -t snapshot rpool/ROOT/pve-1

# 2. Parar serviços críticos (opcional mas recomendado):
systemctl stop pveproxy pvedaemon

# 3. Fazer rollback:
zfs rollback rpool/ROOT/pve-1@antes-fase-3

# 4. Reiniciar:
reboot
```

---

## H.2 Criar uma VM ou CT do zero (referência rápida)

```bash
# Criar um container LXC (CT) — substitua valores conforme a sua rede:
# 1. Baixar template (ex.: Debian 12):
pveam update
pveam available | grep debian
pveam download local debian-12-standard_12.7-1_amd64.tar.zst

# 2. Criar CT:
pct create 200 local:vztmpl/debian-12-standard_12.7-1_amd64.tar.zst \
  --hostname meu-ct \
  --memory 512 \
  --rootfs local-lvm:8 \
  --net0 name=eth0,bridge=vmbr0,ip=192.168.1.200/24,gw=192.168.1.1 \
  --unprivileged 1 \
  --password

# 3. Iniciar:
pct start 200
pct enter 200    # ou: ssh root@192.168.1.200
```

```bash
# Criar uma VM (ex.: Ubuntu Server):
# 1. Baixar ISO (via painel: Datacenter → Storage → local → ISO Images → Upload)
# 2. Criar VM:
qm create 101 \
  --name ubuntu-server \
  --memory 2048 \
  --cores 2 \
  --net0 virtio,bridge=vmbr0 \
  --cdrom local:iso/ubuntu-24.04-live-server-amd64.iso \
  --scsi0 local-lvm:20 \
  --boot order=ide2 \
  --ostype l26

# 3. Iniciar e abrir console:
qm start 101
# No painel: clique na VM → Console
```

> Para Cloud-Init (VMs sem ISO interativa), veja o **Apêndice J**.

---

# 🧰 Apêndice J — Macetes Proxmox 9.x e Cloud-Init

Comandos e truques úteis para o dia-a-dia que não cabem nas fases mas que todo administrador Proxmox usa regularmente.

---

## J.1 Diagnóstico e performance

```bash
# Relatório completo do nó (hardware, storage, rede, VMs):
pvereport | less
# Guarda em arquivo (útil para pedir ajuda no fórum):
pvereport > /tmp/pvereport-$(date +%F).txt

# Benchmark de CPU e I/O do nó:
pveperf
# Saída esperada: GHz, HD, DNS — valores de referência para comparar após upgrades

# Ver versão detalhada do PVE e componentes:
pveversion -v
# Inclui: pve-manager, pve-kernel, qemu-server, lxc, ceph (se instalado)

# Upgrade completo do nó (com confirmação de cada pacote):
pveupgrade
# Equivalente a: apt update && apt full-upgrade (mas com verificações PVE)
```

---

## J.2 Gestão de usuários e tokens via CLI

```bash
# Listar usuários e grupos PVE:
pveum user list
pveum group list

# Criar token de API (para scripts e automação):
pveum user token add renato@pam monitoring --expire 0
# Saída: token ID e valor (guarde no Bitwarden — não é recuperável depois)

# Verificar permissões de um usuário:
pveum user permissions renato@pam

# Criar usuário somente-leitura (ex.: para monitoring):
pveum user add monitor@pve
pveum aclmod / -user monitor@pve -role PVEAuditor
```

---

## J.3 LXC — comandos úteis do dia-a-dia

```bash
# Espaço em disco dentro de um CT:
pct df 100          # mais rápido que entrar no CT e fazer df -h

# Executar comando dentro de um CT sem entrar:
pct exec 100 -- df -h
pct exec 100 -- systemctl status nginx

# Clonar CT (snapshot clone — muito mais rápido que criar do zero):
pct clone 100 201 --full 0    # linked clone (partilha blocos com origem)
pct clone 100 202 --full 1    # full clone (independente)

# Ver configuração de um CT:
pct config 100

# Definir limite de CPU de um CT em execução:
pct set 100 --cpulimit 1.5    # máx 1.5 cores

# ── Diagnóstico de memória dentro de um CT ──
# Top 10 processos por uso de RAM dentro de um CT sem entrar nele:
pct exec 100 -- ps aux --sort=-%mem | head -11

# ── Firewall PVE ──
# Compilar e validar regras (mostra erros de sintaxe sem aplicar):
pve-firewall compile
# Recarregar firewall após edição manual de /etc/pve/firewall/*.fw:
pve-firewall reload

# ── Rede ──
# Ver bridges configuradas e quais interfaces estão ligadas a cada uma:
brctl show
# Estado da resolução DNS do sistema (systemd-resolved):
resolvectl status

# ── ZFS histórico e recuperação de erros ──
# Histórico completo de comandos ZFS executados no pool:
zpool history rpool | tail -30
# Limpar contadores de erro do pool (após investigação e disco substituído):
zpool clear rpool
```

---

## J.4 Boot e certificados

```bash
# Verificar estado do boot loader (UEFI / Legacy) e kernels instalados:
proxmox-boot-tool status
# Mostra: EFI System Partitions sincronizadas, kernels disponíveis

# Renovar certificado TLS do painel web (auto-assinado):
pvenode cert reset --restart

# Ou gerar certificado ACME (Let's Encrypt) se tiver domínio público:
pvenode config set --acme domains=proxmox.meudominio.com
pvenode acme cert order

# Informação do certificado atual:
pvenode cert info
```

---

## J.5 Cloud-Init — VMs sem instalação manual

Cloud-Init permite criar VMs a partir de imagens pré-configuradas (sem assistente de instalação). Ideal para criar VMs de estudo rapidamente.

```bash
# 1. Baixar imagem Cloud (ex.: Ubuntu 24.04 Cloud Image — no nó PVE):
wget https://cloud-images.ubuntu.com/noble/current/noble-server-cloudimg-amd64.img \
  -O /var/lib/vz/template/iso/ubuntu-24.04-cloud.img

# 2. Criar VM base a partir da imagem:
qm create 9000 --name ubuntu-cloud-template --memory 2048 --cores 2 \
  --net0 virtio,bridge=vmbr0 --serial0 socket --vga serial0

# Importar disco da imagem cloud:
qm importdisk 9000 /var/lib/vz/template/iso/ubuntu-24.04-cloud.img local-lvm

# Configurar Cloud-Init drive e boot:
qm set 9000 --scsihw virtio-scsi-pci --scsi0 local-lvm:vm-9000-disk-0
qm set 9000 --ide2 local-lvm:cloudinit
qm set 9000 --boot order=scsi0
qm set 9000 --agent enabled=1

# 3. Configurar Cloud-Init (IP, usuário, chave SSH):
qm set 9000 --ciuser renato --cipassword SenhaForte123
qm set 9000 --ipconfig0 ip=192.168.1.110/24,gw=192.168.1.1
qm set 9000 --sshkeys ~/.ssh/id_ed25519.pub

# 4. Converter em template (opcional — para clonar múltiplas VMs):
qm template 9000

# 5. Clonar template para nova VM:
qm clone 9000 110 --name lab-vm-01 --full
qm start 110
# Em ~30 segundos: ssh renato@192.168.1.110
```

> **Vantagem:** criar uma VM de estudo demora menos de 1 minuto com Cloud-Init vs. 15–20 min com instalação manual. Ideal para testar configurações e destruir sem remorso.

---

## J.6 pvesh — API REST via linha de comandos

```bash
# pvesh permite aceder a toda a API Proxmox localmente (sem token):
# Ver nós disponíveis:
pvesh get /nodes

# Ver VMs de um nó:
pvesh get /nodes/fortaleza/qemu

# Ver status de uma VM:
pvesh get /nodes/fortaleza/qemu/101/status/current

# Iniciar/parar VM via API:
pvesh create /nodes/fortaleza/qemu/101/status/start
pvesh create /nodes/fortaleza/qemu/101/status/stop

# Ver storage disponível:
pvesh get /nodes/fortaleza/storage

# Útil para scripts e automação sem precisar de token externo
```

---

## J.7 Saúde do hardware — ferramentas essenciais para o host

> **Professor falando:** O Proxmox instala o mínimo. Sem estas ferramentas, você não sabe se o disco está a falhar, se a CPU está a 95°C ou se o NIC está em half-duplex. No mini PC N5095 em espaço fechado, monitorar temperatura e disco não é opcional — é prevenção de desastre.

```bash
# Instalar tudo de uma vez (no host PVE como root/renato com sudo):
sudo apt install -y \
  smartmontools \
  nvme-cli \
  lm-sensors \
  sysstat \
  ethtool \
  mc
```

---

### smartmontools — saúde dos discos (SATA e NVMe)

```bash
# Listar todos os discos detectados:
sudo smartctl --scan

# Saúde geral do disco (passa/falha):
sudo smartctl -H /dev/sda      # disco SATA (ex.: Samsung 870 EVO)
sudo smartctl -H /dev/nvme0    # disco NVMe (ex.: WD Red SN700)

# Relatório — temperatura, horas de uso, sectores com erro:
sudo smartctl -a /dev/nvme0 | grep -E "Temperature|Power_On|Reallocated|Media_and_Data"

# Teste rápido (~2 min, não interrompe o sistema):
sudo smartctl -t short /dev/nvme0
# Ver resultado:
sudo smartctl -l selftest /dev/nvme0
```

> **O que observar:** `PASSED` = saudável · `Reallocated_Sector_Ct > 0` = disco a degradar · `Temperature > 70°C` = calor excessivo

```bash
# Alias rápido (adicionar ao ~/.bash_aliases — Apêndice M):
alias disk-health='for d in $(sudo smartctl --scan | awk "{print \$1}"); do echo "=== $d ==="; sudo smartctl -H $d | grep -E "overall|PASSED|FAILED"; done'
```

---

### nvme-cli — informação específica de SSDs NVMe

```bash
# Listar dispositivos NVMe:
sudo nvme list

# Saúde detalhada (temperatura, horas, erros):
sudo nvme smart-log /dev/nvme0 | grep -E "temperature|power_on|unsafe|media"
# temperature    : 38°C   ← temperatura atual
# power_on_hours : 1250   ← horas de uso total
# media_errors   : 0      ← erros de leitura/escrita (0 = perfeito)
# unsafe_shutdowns: 3     ← quedas de energia abruptas (manter ao mínimo)
```

---

### lm-sensors — temperatura da CPU e placa-mãe

```bash
# Primeiro uso — detectar sensores disponíveis:
sudo sensors-detect --auto

# Ver temperaturas atuais:
sensors
# Core 0: +42.0°C  (high = +80.0°C, crit = +100.0°C)

# Monitorar em tempo real:
watch -n 2 sensors

alias temp='sensors | grep -E "Core|temp|fan"'
```

> **Referências N5095:** idle 35–45°C · carga leve 50–65°C · **acima de 85°C = problema de ventilação**

---

### sysstat — histórico de CPU e I/O de disco

```bash
# Activar recolha automática (cron a cada 10 min):
sudo systemctl enable --now sysstat

# I/O de disco em tempo real (%util = % do tempo que o disco está ocupado):
iostat -x 2
# %util > 80% de forma consistente = disco é gargalo

# Histórico de CPU de hoje:
sar -u -f /var/log/sysstat/sa$(date +%d)

alias io='iostat -x 1 5 | grep -v "^$\|^Linux\|^avg"'
```

---

### ethtool — verificar a placa de rede

```bash
# Velocidade e estado do link (troque enp1s0 pela sua interface):
sudo ethtool enp1s0
# Speed: 1000Mb/s  ← deve ser 1000 (Gigabit), nunca 100
# Duplex: Full     ← nunca Half (metade da banda)
# Link detected: yes

# Erros de transmissão:
sudo ethtool -S enp1s0 | grep -E "error|drop|miss" | grep -v " 0$"
# Se aparecer algo: verificar cabo, switch ou driver

alias nic-status='sudo ethtool $(ip route | grep default | awk "{print \$5}") | grep -E "Speed|Duplex|Link"'
```

---

### mc — Midnight Commander (explorador de arquivos visual)

```bash
mc   # abre o explorador de dois painéis

# Atalhos essenciais:
# F5 → copiar  · F6 → mover/renomear  · F8 → apagar
# Tab → alternar painéis  · Ctrl+O → mostrar terminal
# Útil para navegar /etc/pve/, comparar backups, copiar arquivos sem decorar caminhos
```

---

### Script de diagnóstico rápido do hardware

```bash
# Criar script reutilizável:
sudo tee /usr/local/bin/hw-check > /dev/null << 'EOF'
#!/bin/bash
echo "=== $(date) — Diagnóstico de Hardware ==="
echo "── Temperatura ──"
sensors 2>/dev/null | grep -E "Core|Package|temp" || echo "(lm-sensors não instalado)"
echo "── Saúde dos discos ──"
for d in $(smartctl --scan 2>/dev/null | awk '{print $1}'); do
  echo -n "$d: "; smartctl -H "$d" 2>/dev/null | grep -E "PASSED|FAILED|overall" || echo "sem dados"
done
echo "── NVMe temperatura ──"
for d in /dev/nvme*; do [ -e "$d" ] || continue
  echo -n "$d: "; nvme smart-log "$d" 2>/dev/null | grep temperature || echo "(nvme-cli não instalado)"
done
echo "── NIC ──"
iface=$(ip route | grep default | awk '{print $5}' | head -1)
ethtool "$iface" 2>/dev/null | grep -E "Speed|Duplex|Link" || echo "(ethtool não instalado)"
echo "── I/O disco (3 seg) ──"
iostat -x 1 3 2>/dev/null | tail -8 || echo "(sysstat não instalado)"
EOF
sudo chmod +x /usr/local/bin/hw-check

# Executar:
hw-check

# Alias (Apêndice M):
alias hw='hw-check'
```

> **Quando executar `hw-check`:** após instalar as ferramentas (baseline), e sempre que o servidor parecer lento, quente ou com disco a fazer ruído. Os valores do baseline são a referência para comparar no futuro.

---

### inxi — inventário completo do hardware em uma linha

```bash
# Instalar:
sudo apt install -y inxi

# Relatório completo: CPU, RAM, discos, rede, temperatura, kernel:
inxi -Fxz
# -F = full  -x = extra info  -z = oculta dados pessoais (MACs, IPs)

# Só CPU e memória:
inxi -Cm

# Só discos e temperatura:
inxi -Ds
```

> **Quando usar:** ao abrir um ticket de suporte, compartilhar no fórum Proxmox ou fazer baseline antes de upgrade de hardware. O `inxi -Fxz` é o "passaporte" do servidor.

---

### dmidecode — detalhes dos módulos de RAM

```bash
# Ver velocidade, tipo, fabricante e slots de cada módulo de RAM:
sudo dmidecode -t memory | grep -E "Size|Speed|Type|Manufacturer|Locator" | grep -v "No Module"

# Exemplo de saída N5095 (2x 8 GB DDR4 3200):
# Size: 8192 MB
# Speed: 3200 MT/s
# Type: DDR4
# Manufacturer: Samsung

# Ver slots disponíveis vs ocupados:
sudo dmidecode -t memory | grep "Size:" | sort | uniq -c
```

> **Útil para:** confirmar se a RAM está rodando na velocidade correta (dual-channel), verificar ECC, planejar upgrade.

---

### powertop — medir e otimizar consumo de energia

```bash
# Instalar:
sudo apt install -y powertop

# Modo interativo (ver consumo por processo/dispositivo):
sudo powertop

# Aplicar otimizações automáticas (USB, PCI, NIC em power save):
sudo powertop --auto-tune

# Persistir no boot via systemd:
sudo tee /etc/systemd/system/powertop.service > /dev/null << 'EOF'
[Unit]
Description=Powertop auto-tune
After=multi-user.target

[Service]
Type=oneshot
ExecStart=/usr/sbin/powertop --auto-tune

[Install]
WantedBy=multi-user.target
EOF
sudo systemctl enable powertop.service
```

> **Resultado esperado no N5095:** redução de ~5–10W em idle. Ideal se o servidor ficar ligado 24/7.

---

### Otimizações de storage e energia

```bash
# ── ZFS ARC — limitar cache para evitar RAM excessiva ──
# Por padrão, ZFS pode usar até metade da RAM para cache.
# Para N5095 com 16 GB, limitar a 4 GB é seguro:
echo "options zfs zfs_arc_max=4294967296" | sudo tee /etc/modprobe.d/zfs.conf
sudo update-initramfs -u
# Confirmar após reboot:
cat /sys/module/zfs/parameters/zfs_arc_max

# ── HDD spindown — desligar discos mecânicos em idle ──
# (apenas se tiver HDD, não aplicar em SSD/NVMe)
sudo apt install -y hdparm
sudo hdparm -S 120 /dev/sda   # 120 × 5 seg = 10 min de idle antes de dormir
# Persistir via /etc/hdparm.conf:
echo -e "/dev/sda {\n  spindown_time = 120\n}" | sudo tee -a /etc/hdparm.conf
```

> **Nota ZFS ARC:** o limite só entra em vigor após reboot. Para ver o uso atual: `arc_summary` (instalar com `apt install arc-summary`) ou `cat /proc/spl/kstat/zfs/arcstats | grep c_max`.

```bash
# ── Ferramentas modernas de diagnóstico (instalar uma vez) ──
sudo apt install -y btop fastfetch lynis

# btop — monitor de CPU/RAM/disco/rede com interface gráfica no terminal:
btop
# (pressione q para sair; F9 para kill de processo; F5 para filtrar)

# fastfetch — resumo rápido do sistema em 2 segundos (ótimo para "foto" do estado):
fastfetch
# Mostra: OS, kernel, uptime, CPU, RAM, ZFS pools, IP

# lynis — auditoria de segurança completa do sistema:
sudo lynis audit system
# Gera relatório em /var/log/lynis.log e /var/log/lynis-report.dat
# Foco: itens com [WARNING] e [SUGGESTION] — ações concretas de hardening
# Score "Hardening index" de 0–100: acima de 70 é bom para homelab

# ── Rede — substituir netstat (deprecated) ──
# Mostrar todas as portas TCP/UDP em escuta (equivalente ao netstat -tuln):
ss -tuln
# Com nome do processo:
ss -tulnp

# ── Kernel log com timestamps legíveis ──
dmesg -T | tail -50          # últimas 50 mensagens do kernel com hora real
dmesg -T | grep -i "error\|fail\|warn" | tail -20  # só problemas

# ── Histórico de reboots/desligamentos ──
last -x | grep -E "shutdown|reboot" | head -10
# Mostra: quando o servidor foi desligado e reiniciado — útil para detectar quedas inesperadas

# ── Discos — identificadores persistentes ──
# UUID e tipo de filesystem de cada partição (sobrevive a renomeações /dev/sdX):
blkid
# Identificadores por hardware (por fabricante/serial — não muda com troca de porta SATA):
ls -lh /dev/disk/by-id/
# Use estes IDs em /etc/fstab e no ZFS para evitar erros após reboot

# ── Rede — recarregar configuração sem reiniciar ──
# Aplicar mudanças em /etc/network/interfaces sem reboot (PVE usa ifupdown2):
ifreload -a
# Mais seguro que: systemctl restart networking (que pode derrubar conexões ativas)
```

---

## J.8 Logs e tarefas PVE — onde ver o que correu mal

O Proxmox mantém logs de todas as tarefas (backups, migrações, criação de CTs/VMs) e de todos os serviços internos. Saber onde procurar é a diferença entre um diagnóstico de 2 minutos e uma hora de adivinhação.

```bash
# ── Tarefas recentes do nó (últimas 20) ──
pvesh get /nodes/fortaleza/tasks --limit 20
# Campos importantes: status (OK / ERROR), starttime, type (vzdump, qmcreate, vzcreate…)

# Ver log completo de uma tarefa específica (UPID vem do comando acima):
pvesh get /nodes/fortaleza/tasks/<UPID>/log
# Exemplo de UPID: UPID:fortaleza:001A2B3C:00001234:6640A1B2:vzdump:110:root@pam:

# Filtrar só tarefas com erro:
pvesh get /nodes/fortaleza/tasks --limit 50 | grep -i error

# ── Logs dos daemons PVE ──
journalctl -u pvedaemon -n 50          # daemon principal (API, tarefas)
journalctl -u pveproxy -n 30           # proxy HTTPS do painel web
journalctl -u pve-cluster -n 30        # cluster (único nó = poucas mensagens)
journalctl -u proxmox-firewall -n 30   # firewall nftables

# Erros de qualquer serviço nas últimas 24 h:
journalctl -p err --since "24 hours ago"

# ── Pasta de logs de tarefas (arquivos brutos) ──
ls /var/log/pve/tasks/           # subpastas por inicial do UPID
# Cada arquivo = saída completa de uma tarefa (útil para backup failures)

# Últimas 5 tarefas de backup vzdump:
find /var/log/pve/tasks/ -name "*.gz" | xargs zgrep -l "vzdump" | sort -r | head -5

# ── Storage e erros ZFS ──
zpool status -v                  # degradado, erros de read/write/cksum
zpool events -v | head -40       # eventos ZFS recentes (inclui scrubs, erros)
journalctl -k | grep -i "zfs\|zpool" | tail -20   # erros no kernel log

# ── Resumo rápido de saúde (combina tudo) ──
echo "=== Tarefas com erro ===" && pvesh get /nodes/fortaleza/tasks --limit 30 | grep -i error || echo "Nenhum"
echo "=== Serviços com falha ===" && systemctl --failed --no-legend
echo "=== ZFS status ===" && zpool status | grep -E "state:|errors:"
echo "=== Erros kernel (últimas 6h) ===" && journalctl -k -p err --since "6 hours ago" --no-pager | tail -10
```

| Log / Comando | O que mostra | Quando usar |
|---------------|--------------|-------------|
| `pvesh get .../tasks` | Histórico de todas as tarefas PVE | Backup falhou? Criação de CT deu erro? |
| `journalctl -u pvedaemon` | Daemon principal — erros de API e agendamentos | Painel web não responde |
| `journalctl -p err --since "24h"` | Todos os erros do sistema nas últimas 24 h | Servidor lento sem motivo aparente |
| `/var/log/pve/tasks/` | Logs brutos de cada tarefa (detalhados) | Analisar saída completa de um vzdump |
| `zpool status -v` | Saúde do ZFS pool, erros por disco | Após queda de energia ou disco suspeito |
| `zpool events -v` | Histórico de eventos ZFS | Investigar scrub ou erro pontual |

> **Dica:** se um backup noturno falhou mas você só viu no dia seguinte, `pvesh get /nodes/fortaleza/tasks --limit 50 | grep -i error` mostra o UPID exato. Use o UPID para ler o log completo e saber exatamente o que falhou.

---

## J.9 CPU Governor — controlar frequência da CPU

O N5095 (e qualquer Intel moderno) suporta diferentes modos de operação da CPU. O padrão do kernel Proxmox varia — controlar isso permite equilibrar **consumo de energia vs. desempenho** dependendo da carga.

```bash
# Instalar ferramenta de controlo de frequência:
sudo apt install -y linux-cpupower

# Ver governor atual e frequências disponíveis:
cpupower frequency-info

# Ver governors disponíveis:
cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_available_governors
# Saída típica: conservative ondemand userspace powersave performance

# Definir governor:
sudo cpupower frequency-set -g ondemand      # recomendado (equilibrado)
sudo cpupower frequency-set -g powersave     # economia máxima (idle/madrugada)
sudo cpupower frequency-set -g performance   # força bruta (builds, vídeo)

# Confirmar:
cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor
```

| Governor | CPU clock | Consumo | Quando usar |
|----------|-----------|---------|-------------|
| `performance` | Máximo sempre | Alto | Transcodificação (Jellyfin), builds, VMs Windows interativas |
| `ondemand` | Sobe quando precisa | Médio | **Uso geral — VMs Linux, containers, NAS** (recomendado) |
| `powersave` | Mínimo sempre | Baixo | Servidor em idle, madrugada, só serviços leves |

```bash
# ── Tornar permanente via systemd ──
sudo tee /etc/systemd/system/cpupower.service > /dev/null << 'EOF'
[Unit]
Description=Set CPU governor
After=multi-user.target

[Service]
Type=oneshot
ExecStart=/usr/bin/cpupower frequency-set -g ondemand

[Install]
WantedBy=multi-user.target
EOF
sudo systemctl enable cpupower.service

# Alias para troca rápida (adicionar ao ~/.bash_aliases):
alias cpu-max='sudo cpupower frequency-set -g performance && echo "🔥 Performance"'
alias cpu-bal='sudo cpupower frequency-set -g ondemand   && echo "⚖️ Ondemand"'
alias cpu-eco='sudo cpupower frequency-set -g powersave  && echo "🌿 Powersave"'
alias cpu-gov='cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor'
```

> **N5095 em homelab 24/7:** use `ondemand` como padrão. Se quiser economizar na conta de luz em períodos sem uso, troque para `powersave` com `cpu-eco` — volte com `cpu-bal` quando retomar os labs.

---

## J.10 Vulnerabilidades de CPU Intel — o que são e o que fazer

Todo Intel moderno tem vulnerabilidades conhecidas (Spectre, Meltdown, L1TF, MDS). O kernel detecta e aplica mitigações automáticas, mas você precisa entender as opções — especialmente em homelab com múltiplas VMs.

```bash
# Ver todas as vulnerabilidades detectadas e status de mitigação:
grep . /sys/devices/system/cpu/vulnerabilities/*
# Saída exemplo N5095:
# /sys/devices/system/cpu/vulnerabilities/spectre_v1: Mitigation: usercopy/swapgs barriers
# /sys/devices/system/cpu/vulnerabilities/spectre_v2: Mitigation: Retpolines; IBPB conditional
# /sys/devices/system/cpu/vulnerabilities/meltdown:   Mitigation: PTI
# /sys/devices/system/cpu/vulnerabilities/mmio_stale_data: Mitigation: Clear CPU buffers
# /sys/devices/system/cpu/vulnerabilities/l1tf:       Not affected (Jasper Lake não afetado)

# Como interpretar:
# "Mitigation: ..."  → protegido
# "Not affected"     → seu CPU não tem essa falha
# "Vulnerable"       → exposto (raro com kernel atualizado)
```

| Modo GRUB | Segurança | Desempenho | Quando usar |
|-----------|-----------|------------|-------------|
| `mitigations=off` | ❌ Sem proteção | Máximo | Apenas benchmarks isolados |
| `mitigations=auto` | ✅ Padrão do kernel | Bom | **Homelab — recomendado (já é o padrão)** |
| `mitigations=auto,nosmt` | ✅✅ Máxima (desliga HT) | −20–30% | Se compartilhar host com usuários externos |

```bash
# Para homelab: o padrão já é mitigations=auto — geralmente não precisa mexer.
# Verificar o que está ativo:
cat /proc/cmdline

# Se quiser alterar (ex.: forçar auto explicitamente):
sudo nano /etc/default/grub
# Linha: GRUB_CMDLINE_LINUX="mitigations=auto"

# ⚠️ NO PROXMOX — NÃO use update-grub. Use sempre:
sudo proxmox-boot-tool refresh
sudo reboot

# Confirmar após reboot:
cat /proc/cmdline
grep . /sys/devices/system/cpu/vulnerabilities/*
```

> **N5095 (Jasper Lake, 2021):** não é afetado por L1TF. Tem mitigações para Spectre V1/V2 e MMIO — todas aplicadas automaticamente pelo kernel. Em homelab com apenas as suas VMs, o risco real é mínimo. **Não precisa desabilitar SMT** (o N5095 não tem Hyper-Threading de qualquer forma — 4 cores = 4 threads).

---

# 🛡️ Apêndice K — Postura de Segurança (o que você ganhou)

Após concluir as fases Fortaleza, o seu Mini PC tem uma **base de segurança sólida para homelab**. Aqui está o que está protegido — e o que não está.

---

## K.1 O que está protegido

| Camada | Proteção aplicada | Fase |
|--------|-------------------|------|
| **Acesso remoto** | SSH só com chave Ed25519 + TOTP obrigatório | Fases 2–3 |
| **Root SSH** | Bloqueado (`PermitRootLogin no`) | Fase 2 |
| **Painel web** | HTTPS + 2FA TOTP para `renato@pam` | Fase 6 |
| **Força bruta** | CrowdSec bane IPs automaticamente após tentativas falhas | Fase 4 |
| **Firewall de rede** | nftables com política DROP por padrão — só portas necessárias abertas | Fase 7 |
| **Acesso remoto seguro** | Tailscale — zero portas abertas na internet, VPN mesh cifrada | Fase 5 |
| **Configuração do nó** | Backup automático de `/etc/pve` via cron | Fase 10 |
| **VMs e CTs** | vzdump agendado com retenção configurada | Fase 10b |
| **Atualizações** | `unattended-upgrades` aplica patches de segurança sem intervenção | Fase 9 |
| **Segredos** | Todas as senhas, chaves e códigos 2FA no Bitwarden | Apêndice G |

---

## K.2 O que este guia NÃO protege (honestidade)

É importante saber o que fica **fora do escopo** desta configuração:

| O que não está coberto | Por quê | O que fazer |
|------------------------|---------|-------------|
| **Aplicações dentro das VMs/CTs** | Cada app (nginx, bind9, Vaultwarden…) tem sua própria superfície de ataque | Configure cada app com TLS, autenticação e atualizações independentes |
| **Outros dispositivos da LAN** | PCs, celulares e IoT da rede doméstica não passam pelo firewall do PVE | Configura firewall no roteador e/ou usa VLANs para isolar IoT |
| **Ataques físicos** | Quem tem acesso físico ao Mini PC tem acesso root via console | Garante segurança física (quarto fechado, rack trancado) |
| **Zero-days no Proxmox/Debian** | Vulnerabilidades não públicas não têm defesa prévia | `unattended-upgrades` mitiga quando o patch sai — sem mais que isso |
| **Port forwarding para a internet** | O guia intencionalmente não abre portas no roteador | Use Tailscale para acesso externo seguro, não port forwarding |
| **Redes Wi-Fi** | O guia assume Ethernet — Wi-Fi adiciona vetores de ataque | Use cabo; se Wi-Fi for obrigatório, use WPA3 + rede isolada |
| **Monitoramento de segurança** | CrowdSec cobre força bruta; não há SIEM nem correlação de logs | Nível 3 do roadmap: Prometheus + alertas Telegram |

---

## K.3 A filosofia da Fortaleza

> **A infraestrutura segura é a base — não o destino.**

O que você construiu é o **chão firme** para estudar, experimentar e crescer sem medo de comprometer a rede doméstica. Cada aplicação que você instalar dentro das VMs/CTs precisa ser tratada com a mesma filosofia:

- Autenticação forte
- Princípio do mínimo privilégio
- Atualizações automáticas
- Backups antes de mudanças
- Documentação do que foi feito

```bash
# Verificação rápida de postura (executar mensalmente):
make check   # ou: sudo bash scripts/fortaleza-health-check.sh --verbose
# Todos os itens ✅ = postura mantida
```

---

# 🎓 Apêndice L — Dicas Finais e Próximos Estudos

Você concluiu a Fortaleza. O que vem a seguir?

---

## L.1 Sequência natural de aprendizagem

```
🏰 Fortaleza (host seguro)
        ↓
🐧 Fundamentos Linux (VM 110 + docs/linux-comandos-fundamentos.md)
        ↓
🔐 GPG + Criptografia (Fase 8 intro + curso externo)
        ↓
🌐 DNS bind9 (VM 111 — como a internet funciona por dentro)
        ↓
🌍 nginx + HTTPS (VM 112 — como um servidor web funciona)
        ↓
🔥 nftables/iptables (VM 113 — firewall do zero, sem abstração)
        ↓
🧅 Tor Hidden Service (CT 103 — rede .onion, acesso anónimo, compatível com Tails)
        ↓
🐳 Docker (VM 110 — containers sem orquestração)
        ↓
⚙️  Ansible (automatize o que aprendeu)
        ↓
☸️  Kubernetes k3s (quando precisar escalar)
```

> Cada passo é uma porta que abre a próxima. Não pule — cada nível usa o anterior.

---

## L.2 O que mais explorar neste hardware

| Área | Recurso / Guia | Tipo |
|------|----------------|------|
| **Linux Fundamentals** | [docs/linux-comandos-fundamentos.md](docs/linux-comandos-fundamentos.md) + VM 110 | Interno |
| **GPG / OpenPGP** | Fase 8 (prática) + seu curso externo | EXT |
| **AdGuard Home** | §D.2.1 — DNS bloqueador para a LAN inteira | Guia |
| **Vaultwarden** | §D.2.2 — Bitwarden self-hosted, senhas fora da nuvem | Guia |
| **Nginx Proxy Manager** | §D.2.3 — HTTPS para todos os serviços via Let's Encrypt | Guia |
| **Uptime Kuma** | §D.2.4 — Alertas Telegram quando serviço cair | Guia |
| **DNS bind9** | §D.3.1 + `man named.conf` — como a internet funciona por dentro | Lab |
| **nginx do zero** | §D.3.2 + [nginx.org/en/docs](https://nginx.org/en/docs/) — virtual hosts, SSL, proxy_pass | Lab |
| **nftables do zero** | §D.3.3 + [wiki.nftables.org](https://wiki.nftables.org/) — firewall sem abstração | Lab |
| **LAN simulada** | §D.3.4 — duas redes, vmbr1, roteamento, VLANs | Lab |
| **Prometheus + Grafana** | §D.4.1 — métricas do N5095, dashboard Node Exporter Full | Lab |
| **Ansible** | §D.4.2 — 3 playbooks: health-check, criar CT, update-all | Lab |
| **Tor Hidden Service** | Apêndice N + [Tor Onion Services](https://community.torproject.org/onion-services/setup/) | Lab |
| **Redes TCP/IP** | Livro "Computer Networks" (Tanenbaum) ou Cisco NetAcad | EXT |
| **Segurança ofensiva** | TryHackMe / HackTheBox (VMs isoladas) | EXT |
| **k3s (Kubernetes leve)** | §D.4 — quando dominar Docker Compose | Lab |

---

## L.3 Dicas práticas para continuar

**Antes de cada lab novo:**
```bash
qm snapshot 110 antes-$(date +%Y%m%d) --description "Checkpoint antes de novo lab"
# Se tudo correr mal:
qm rollback 110 antes-$(date +%Y%m%d)
```

**Quando a VM "quebrar completamente":**
```bash
# Não tente consertar — destrua e recomece:
qm stop 111
qm destroy 111
qm clone 110 111 --name lab-dns --full
qm start 111
# Em 60 segundos está de volta — é para isso que existe o snapshot base-limpa
```

**Para não perder o que aprendeu:**
```bash
# Diário de estudos — escreva uma linha por sessão:
echo "$(date +"%F") — aprendi: [o que foi]" >> ~/fortaleza-lab/diario.md
# Reveja o diário antes de cada sessão — reforça a memória
```

**Regra dos 3 antes de avançar:**
1. Consegue explicar o que cada comando faz? (não só copiar)
2. Sabe reverter se der errado? (snapshot, rollback, `pct restore`)
3. Documentou no diário o que funcionou e por quê?

Se sim para os 3 → avance para o próximo lab.

---

## L.4 A filosofia do laboratório que vale guardar

> **"Um laboratório bom é um laboratório que pode ser destruído e recriado sem estresse."**
>
> ZFS snapshot antes. Aprendeu? Snapshot de novo. Quebrou? Rollback. Evoluiu? Nova fase.
>
> O Mini PC N5095 com 16 GB RAM não é um servidor de produção — é um professor de silício.  
> Trate-o como tal: experimente, quebre, conserte, documente.

---

# 🖥️ Apêndice M — Aliases e Boas Práticas de Shell

> **Professor falando:** Um alias é uma abreviação que você ensina ao terminal. Em vez de digitar o mesmo comando longo 50 vezes por dia, você digita 3 letras. Parece pequeno — mas depois de um mês de lab, você vai ter digitado esses comandos centenas de vezes. Aliases não são "preguiça": são **precisão e consistência**.

---

## M.1 Como funcionam os aliases (fundamento antes da prática)

```bash
# Um alias é definido assim:
alias nome='comando completo'

# Exemplo:
alias ll='ls -lh --color=auto'

# Agora "ll" executa "ls -lh --color=auto"
ll   # funciona!

# Mas se você fechar o terminal... o alias some.
# Para ser permanente, o alias tem que estar num arquivo que o bash carrega ao iniciar.
```

**Onde guardar aliases permanentes:**

```bash
# Opção correta — arquivo dedicado (não polua o .bashrc):
nano ~/.bash_aliases

# O ~/.bashrc já tem (em Debian) um bloco que carrega o .bash_aliases automaticamente:
# if [ -f ~/.bash_aliases ]; then
#     . ~/.bash_aliases
# fi

# Se não tiver, adicione manualmente ao final do .bashrc:
echo 'if [ -f ~/.bash_aliases ]; then . ~/.bash_aliases; fi' >> ~/.bashrc

# Depois de editar .bash_aliases, recarregue sem fechar o terminal:
source ~/.bash_aliases
# ou
. ~/.bash_aliases
```

> **Regra de ouro:** aliases no `~/.bash_aliases`, configurações do shell no `~/.bashrc`, variáveis de ambiente no `~/.profile`. Cada arquivo tem o seu propósito.

---

## M.2 Aliases para o host Proxmox VE (como root ou renato com sudo)

Cole este bloco em `/root/.bash_aliases` (para root) **e** em `~/.bash_aliases` (para renato):

```bash
# ── STATUS RÁPIDO ─────────────────────────────────────────────
alias pve-status='pveversion -v && echo "---" && uptime && echo "---" && free -h'
alias pve-guests='echo "=== CTs ===" && pct list && echo "=== VMs ===" && qm list'
alias pve-ram='ps aux --sort=-%mem | head -20'
alias pve-disk='df -h | grep -v tmpfs'

# ── ZFS ───────────────────────────────────────────────────────
alias zfs-list='zfs list -o name,used,avail,refer,mountpoint'
alias zfs-snaps='zfs list -t snapshot -o name,creation,used | sort -k2'
alias zfs-pool='zpool status && zpool list'

# ── CONTAINERS (pct) ──────────────────────────────────────────
alias cts='pct list'
alias ct-start='pct start'       # uso: ct-start 100
alias ct-stop='pct stop'         # uso: ct-stop 100
alias ct-enter='pct enter'       # uso: ct-enter 100
alias ct-ram='for id in $(pct list | awk "NR>1{print \$1}"); do echo "CT $id: $(pct config $id | grep memory | awk "{print \$2}")MB — $(pct status $id | cut -d" " -f2)"; done'

# ── VMs (qm) ──────────────────────────────────────────────────
alias vms='qm list'
alias vm-start='qm start'        # uso: vm-start 110
alias vm-stop='qm stop'          # uso: vm-stop 110

# ── CROWDSEC ──────────────────────────────────────────────────
alias cs-status='sudo systemctl status crowdsec crowdsec-firewall-bouncer --no-pager'
alias cs-bans='sudo cscli decisions list'
alias cs-unban='sudo cscli decisions delete --ip'   # uso: cs-unban 1.2.3.4
alias cs-alerts='sudo cscli alerts list | tail -20'

# ── TAILSCALE ─────────────────────────────────────────────────
alias ts-ip='sudo pct exec 100 -- tailscale ip -4'
alias ts-status='sudo pct exec 100 -- tailscale status'

# ── LOGS ──────────────────────────────────────────────────────
alias log-ssh='sudo journalctl -u ssh -f'
alias log-firewall='sudo journalctl -u proxmox-firewall -f'
alias log-cs='sudo journalctl -u crowdsec -f'
alias log-pve='sudo journalctl -u pvedaemon -f'

# ── BACKUPS ───────────────────────────────────────────────────
alias bkp-check='ls -lh /var/lib/vz/dump/ | tail -20'
alias bkp-etc='sudo tar czf /root/backups/etc-pve-$(date +%F).tar.gz /etc/pve/ && echo "Backup /etc/pve OK"'

# ── SEGURANÇA RÁPIDA ──────────────────────────────────────────
alias fw-rules='sudo nft list ruleset | grep -E "chain|accept|drop|reject" | head -40'
alias fw-status='sudo systemctl is-active proxmox-firewall pve-firewall crowdsec-firewall-bouncer'
alias health='sudo bash /root/scripts/fortaleza-health-check.sh --verbose 2>/dev/null || make check'
```

**Como instalar no host:**

```bash
# Como renato (com sudo):
nano ~/.bash_aliases
# Cole o bloco acima, salve

# Recarregar:
source ~/.bash_aliases

# Testar:
pve-guests   # deve listar CTs e VMs
zfs-snaps    # deve listar snapshots
cs-bans      # deve mostrar decisões do CrowdSec
```

---

## M.3 Aliases para a VM de estudo (Debian 13 — usuário aluno)

Cole em `~/.bash_aliases` dentro da VM 110:

```bash
# ── NAVEGAÇÃO ─────────────────────────────────────────────────
alias ll='ls -lhF --color=auto'
alias la='ls -lahF --color=auto'
alias lt='ls -lhFt --color=auto | head -20'   # 20 arquivos mais recentes
alias ..='cd ..'
alias ...='cd ../..'
alias ~='cd ~'

# ── SEGURANÇA (sempre pede confirmação) ───────────────────────
alias rm='rm -i'      # pergunta antes de apagar
alias cp='cp -i'      # pergunta antes de sobrescrever
alias mv='mv -i'      # pergunta antes de mover

# ── REDE ──────────────────────────────────────────────────────
alias meuip='ip -4 addr show | grep inet | grep -v 127 | awk "{print \$2}"'
alias ports='ss -tlnp'                          # portas abertas
alias rotas='ip route'
alias dns-test='dig +short google.com @1.1.1.1' # testa resolução DNS

# ── SISTEMA ───────────────────────────────────────────────────
alias mem='free -h'
alias disco='df -h | grep -v tmpfs'
alias cpu='top -bn1 | grep "Cpu(s)"'
alias servicos='systemctl list-units --type=service --state=running'
alias logs='journalctl -f'          # logs em tempo real
alias log-ssh='journalctl -u ssh -f'

# ── PACOTES ───────────────────────────────────────────────────
alias update='sudo apt update && sudo apt list --upgradable 2>/dev/null'
alias upgrade='sudo apt update && sudo apt full-upgrade -y'
alias instalar='sudo apt install'   # uso: instalar nginx
alias remover='sudo apt remove'

# ── GPG ───────────────────────────────────────────────────────
alias gpg-chaves='gpg --list-keys --keyid-format LONG'
alias gpg-priv='gpg --list-secret-keys --keyid-format LONG'
alias gpg-fp='gpg --fingerprint'

# ── GIT ───────────────────────────────────────────────────────
alias gs='git status'
alias gl='git log --oneline --graph --decorate -15'
alias ga='git add'
alias gc='git commit -m'      # uso: gc "mensagem do commit"
alias gp='git push'
alias gpl='git pull'

# ── UTILIDADES ────────────────────────────────────────────────
alias h='history | tail -30'             # últimos 30 comandos
alias grep='grep --color=auto'
alias path='echo $PATH | tr ":" "\n"'   # mostra PATH linha a linha
alias data='date +"%Y-%m-%d %H:%M:%S"'
alias diario='echo "## $(date +"%F %H:%M") - " >> ~/diario.md && nano ~/diario.md'
```

---

## M.4 Shell functions — quando aliases não chegam

Um alias não aceita argumentos variáveis complexos. Para isso usamos **funções**:

```bash
# Adicione ao ~/.bash_aliases (ou ~/.bashrc):

# Snapshot ZFS com nome descritivo — uso: snap-ct 100 antes-nginx
snap-ct() {
  local ctid="$1" label="$2"
  [ -z "$ctid" ] || [ -z "$label" ] && echo "Uso: snap-ct <CTID> <label>" && return 1
  local dataset=$(pct config "$ctid" | grep rootfs | awk -F: '{print $2}' | awk '{print $1}')
  local snapname="${dataset}@${label}-$(date +%Y%m%d)"
  sudo zfs snapshot "$snapname" && echo "✅ Snapshot criado: $snapname"
}

# Snapshot de VM — uso: snap-vm 110 antes-bind9
snap-vm() {
  local vmid="$1" label="$2"
  [ -z "$vmid" ] || [ -z "$label" ] && echo "Uso: snap-vm <VMID> <label>" && return 1
  qm snapshot "$vmid" "${label}-$(date +%Y%m%d)" --description "Snapshot antes de $label" \
    && echo "✅ Snapshot VM $vmid: ${label}-$(date +%Y%m%d)"
}

# Criar CT Debian rápido — uso: novo-ct 115 lab-dns 192.168.1.115
novo-ct() {
  local ctid="$1" nome="$2" ip="$3"
  [ -z "$ctid" ] || [ -z "$nome" ] || [ -z "$ip" ] && \
    echo "Uso: novo-ct <CTID> <hostname> <IP>" && return 1
  pct create "$ctid" local:vztmpl/debian-12-standard_12.7-1_amd64.tar.zst \
    --hostname "$nome" --memory 512 --rootfs local-lvm:8 --unprivileged 1 \
    --net0 "name=eth0,bridge=vmbr0,ip=${ip}/24,gw=192.168.1.1" \
    && echo "✅ CT $ctid ($nome) criado — inicie com: pct start $ctid"
}

# Entrar num CT e ver seus logs — uso: ct-log 100
ct-log() {
  pct exec "${1:?Uso: ct-log <CTID>}" -- journalctl -f
}

# Testar se uma porta está aberta — uso: porta-aberta 192.168.1.100 22
porta-aberta() {
  timeout 3 bash -c "cat < /dev/null > /dev/tcp/$1/$2" 2>/dev/null \
    && echo "✅ $1:$2 — ABERTA" || echo "❌ $1:$2 — FECHADA/FILTRADA"
}
```

**Como usar as funções:**

```bash
source ~/.bash_aliases   # recarregar após editar

snap-ct 100 antes-update          # snapshot do CT 100
snap-vm 110 antes-nginx           # snapshot da VM 110
novo-ct 116 lab-nginx 192.168.1.116  # criar novo CT
porta-aberta 192.168.1.100 22     # testar SSH
```

---

## M.5 Boas práticas — o que um professor de shell ensina

**Regra 1 — Nunca faça alias de comandos destrutivos sem `-i`:**
```bash
# ❌ Perigoso — apaga sem perguntar:
alias rm='rm -rf'

# ✅ Seguro — sempre pede confirmação:
alias rm='rm -i'
```

**Regra 2 — Documente cada alias com um comentário:**
```bash
# ❌ Sem contexto:
alias ct='pct exec 100 -- bash'

# ✅ Com contexto:
alias ct-vpn='pct exec 100 -- bash'   # entra no CT Tailscale (100)
```

**Regra 3 — Teste antes de guardar:**
```bash
# Na linha de comandos, defina o alias temporariamente:
alias teste='ls -lah /tmp'
teste   # se funcionar como esperado, adicione ao .bash_aliases
```

**Regra 4 — Use `type` para ver o que um comando faz antes de criar alias:**
```bash
type ll     # mostra se já existe alias, função ou binário com esse nome
type rm     # deve mostrar: rm is aliased to 'rm -i'
```

**Regra 5 — `history` é seu melhor amigo para descobrir aliases novos:**
```bash
history | awk '{print $2}' | sort | uniq -c | sort -rn | head -20
# Mostra os 20 comandos que você mais digita — candidatos perfeitos para alias
```

---

## M.6 Exercício prático — instale e teste

```bash
# 1. No host PVE (como renato):
nano ~/.bash_aliases
# Cole os aliases do §M.2 → salve → source ~/.bash_aliases

# 2. Teste imediato:
pve-guests     # lista CTs e VMs
zfs-snaps      # lista snapshots
cs-bans        # decisões CrowdSec (pode estar vazia — é OK)
ts-ip          # IP Tailscale do CT 100

# 3. Na VM 110 (como aluno):
nano ~/.bash_aliases
# Cole os aliases do §M.3 → source ~/.bash_aliases

# 4. Teste imediato:
ll             # listagem detalhada com cores
meuip          # IP da VM
ports          # portas abertas
dns-test       # teste DNS

# 5. Instale as funções do §M.4 no host:
# Adicione ao final do ~/.bash_aliases do renato → source

snap-vm 110 teste-aliases         # cria snapshot de teste
qm listsnapshot 110               # confirma que aparece
```

> **Desafio:** descubra com `history | awk '{print $2}' | sort | uniq -c | sort -rn | head -10` quais são os seus 10 comandos mais frequentes depois de 1 semana de lab. Crie aliases para os que tiver mais de 5 ocorrências.

---

# 🧅 Apêndice N — Tor Hidden Service (Rede .onion)

> **Pré-requisito:** Fases 0–7 concluídas. O host está seguro, CrowdSec ativo, firewall DROP configurado. Sem essa base, não faz sentido adicionar Tor.

🎯 **OBJETIVO:** Criar um endereço `.onion` para o seu servidor — acessível via rede Tor sem expor o IP público da sua casa, sem port forwarding, e compatível com Tails OS.
⏱ **Tempo estimado:** 30–45 min

---

📚 **FUNDAMENTO**

O Tor (The Onion Router) cifra o tráfego em múltiplas camadas e roteia por relays voluntários pelo mundo. Um **Hidden Service** (serviço oculto) é o inverso de um proxy: o servidor *anuncia* a sua existência na rede Tor sem revelar o IP real. O cliente liga ao `.onion` sem saber (nem precisar saber) onde o servidor está fisicamente.

**Arquitectura deste guia:**

```
Tails OS / Cliente Tor
        ↓ (rede Tor — 3 relays cifrados)
CT 103 (Tor daemon — Hidden Service)
        ↓ (LAN interna 192.168.1.x)
Host PVE porta 22 (SSH + chave Ed25519 + TOTP)
```

**Por que CT 103 e não directo no host?**
- Isolamento: o processo Tor corre num container separado, não no host endurecido
- Se o Tor tiver uma vulnerabilidade, fica confinado ao CT 103
- O host PVE nunca fala directamente com a rede Tor — só com o CT na LAN

**O que o Tor protege e o que não protege:**

| Protege | Não protege |
|---------|-------------|
| IP público da sua casa | Autenticação SSH (ainda precisa de chave + TOTP) |
| Localização geográfica | Vulnerabilidades no serviço SSH em si |
| Metadados de rede | O conteúdo da sessão SSH (cifrado pelo SSH, não pelo Tor) |
| Acesso a partir do Tails | Ataques dentro do servidor após login |

---

## N.1 Criar o CT 103 (nó Tor)

```bash
# No nó PVE como root/renato — template Debian 12 já deve existir da Fase 5:
pveam update
# Se não tiver o template:
pveam download local debian-12-standard_12.7-1_amd64.tar.zst

# Criar CT 103:
pct create 103 local:vztmpl/debian-12-standard_12.7-1_amd64.tar.zst \
  --hostname tor-hidden \
  --memory 256 \
  --rootfs local-lvm:4 \
  --net0 name=eth0,bridge=vmbr0,ip=192.168.1.103/24,gw=192.168.1.1 \
  --unprivileged 1 \
  --nameserver 1.1.1.1

# Snapshot antes de começar:
sudo zfs snapshot rpool/ROOT/pve-1@snap-pre-tor

# Iniciar:
pct start 103
pct enter 103
```

---

## N.2 Instalar e configurar o Tor

```bash
# Dentro do CT 103 (como root):

# Atualizar e instalar Tor:
apt update && apt upgrade -y
apt install tor -y

# Verificar versão instalada:
tor --version
# Saída esperada: Tor 0.4.x.x (git-...) — confirma instalação

# Confirmar serviço ativo:
systemctl status tor --no-pager
# Deve mostrar: Active: active (running)
```

---

## N.3 Configurar o Hidden Service para SSH

```bash
# Dentro do CT 103:
nano /etc/tor/torrc
```

Adicione estas linhas ao **final** do arquivo (não remova o conteúdo existente):

```
## Hidden Service para SSH do host Proxmox
HiddenServiceDir /var/lib/tor/ssh_hidden/
HiddenServicePort 22 192.168.1.100:22
```

> **Tradução:**
> - `HiddenServiceDir` — directório onde o Tor guarda as chaves do .onion e o endereço gerado
> - `HiddenServicePort 22 192.168.1.100:22` — quando alguém liga ao `.onion` porta 22, reencaminha para `192.168.1.100:22` (o host PVE na LAN) — **substitua pelo IP real do seu host** (`ip addr show vmbr0`)

```bash
# Reiniciar o Tor para gerar o Hidden Service:
systemctl restart tor

# Aguardar 10–30 segundos e ler o endereço .onion gerado:
cat /var/lib/tor/ssh_hidden/hostname
# Saída: algo como: abc123xyz456defg.onion
```

> ⚠️ **Guarde este endereço no Bitwarden** — pasta "Fortaleza Proxmox" → "Endereço .onion SSH". Sem ele não consegue aceder via Tor.

```bash
# Verificar que as chaves foram criadas:
ls -la /var/lib/tor/ssh_hidden/
# Deve existir: hostname, hs_ed25519_public_key, hs_ed25519_secret_key
```

> **As chaves `hs_ed25519_*` são o seu .onion.** Faça backup delas se quiser preservar o mesmo endereço após reinstalação do CT.

---

## N.4 Adicionar CT 103 à whitelist do CrowdSec

O SSH do host vai receber conexões vindas do IP do CT 103 (`192.168.1.103`). O CrowdSec já tem `192.168.1.0/24` na whitelist — o CT está coberto. Confirme:

```bash
# No host PVE (sair do CT 103 com exit, ou noutra sessão):
sudo cscli decisions list
# O IP 192.168.1.103 não deve aparecer banido

# Confirmar whitelist ativa:
cat /etc/crowdsec/parsers/s02-enrich/whitelists.yaml | grep cidr -A5
# Deve mostrar 192.168.1.0/24 e 100.64.0.0/10
```

---

## N.5 Ligar ao servidor via Tor (do seu PC)

Para testar antes do Tails, instale `torsocks` ou configure o SSH com ProxyCommand:

**Método 1 — torsocks (mais simples):**
```bash
# No seu PC Linux/Mac — instalar torsocks:
# Ubuntu/Debian: sudo apt install torsocks
# Mac: brew install tor

# Iniciar Tor localmente (se não estiver rodando):
# Ubuntu: sudo systemctl start tor
# Mac: brew services start tor

# Conectar ao .onion:
torsocks ssh -i ~/.ssh/chave_fortaleza renato@abc123xyz456defg.onion
# Pede: Verification code: (TOTP — código do app)
```

**Método 2 — ProxyCommand (sem instalar torsocks):**
```bash
# Requer Tor rodando localmente (SOCKS5 em 127.0.0.1:9050):
ssh -i ~/.ssh/chave_fortaleza \
    -o ProxyCommand="nc -X 5 -x 127.0.0.1:9050 %h %p" \
    renato@abc123xyz456defg.onion
```

**Método 3 — Entrada no ~/.ssh/config do PC (para uso permanente):**
```
Host fortaleza-onion
    HostName abc123xyz456defg.onion
    User renato
    IdentityFile ~/.ssh/chave_fortaleza
    ProxyCommand nc -X 5 -x 127.0.0.1:9050 %h %p
```

```bash
# Depois basta:
ssh fortaleza-onion
# → pede Verification code: (TOTP)
```

---

## N.6 Ligar ao servidor via Tails OS

O Tails roteia todo o tráfego pelo Tor automaticamente — não é preciso configuração adicional no cliente.

```bash
# No terminal do Tails:
ssh -i /caminho/para/chave_fortaleza \
    -o ProxyCommand="nc -X 5 -x 127.0.0.1:9050 %h %p" \
    renato@abc123xyz456defg.onion

# Ou com torsocks (disponível no Tails):
torsocks ssh -i /caminho/para/chave_fortaleza renato@abc123xyz456defg.onion
```

> **Como levar a chave SSH para o Tails:**
> O Tails não persiste arquivos entre sessões (por design). Opções:
> 1. **Tails Persistent Storage** — active em Tails → Configure Persistent Storage → guarde a chave em `/home/amnesia/Persistent/`
> 2. **Pendrive cifrado separado** — importe a chave no início de cada sessão
> 3. **Bitwarden Web** — aceda via browser Tor, copie a chave privada para um arquivo temporário na sessão

> **Tempo de ligação via Tor:** espere 5–15 segundos de latência — normal na rede Tor. O SSH pode parecer lento a responder inicialmente.

---

## N.7 Termius no celular via Tor (Android)

Para usar Termius com o endereço .onion em 4G:

1. Instalar **Orbot** (Android) — cliente Tor oficial: [Orbot no Play Store](https://play.google.com/store/apps/details?id=org.torproject.android)
2. Activar Orbot → modo "VPN" (roteia todo o tráfego pelo Tor)
3. No Termius: host = `abc123xyz456defg.onion`, porta `22`
4. Autenticação: chave SSH + TOTP

> **Alternativa iOS:** usar Onion Browser + Terminus — o fluxo é mais complexo no iOS; o Orbot para iOS também existe mas com limitações.

---

✅ **VERIFIQUE**

```bash
# No CT 103 — confirmar Hidden Service ativo:
pct exec 103 -- systemctl status tor --no-pager
# Active: active (running)

pct exec 103 -- cat /var/lib/tor/ssh_hidden/hostname
# Mostra o endereço .onion

# No host PVE — confirmar que CT 103 não está banido:
sudo cscli decisions list | grep 192.168.1.103
# Não deve aparecer

# Teste de conectividade (com torsocks ou Tor Browser rodando):
torsocks ssh renato@abc123xyz456defg.onion
# Deve pedir: Verification code:
```

---

🆘 **SE DEU ERRADO**

| Sintoma | Causa | Solução |
|---------|-------|---------|
| `cat /var/lib/tor/ssh_hidden/hostname` — arquivo não existe | Tor ainda a inicializar, ou erro no torrc | `systemctl status tor` → ver logs; verificar sintaxe do torrc |
| `Connection refused` ao ligar ao .onion | Tor não iniciou ou HiddenService mal configurado | `journalctl -u tor -n 50` no CT 103 |
| `Connection timed out` | Tor está a tentar mas o host PVE não responde | Confirmar IP do host em `HiddenServicePort`; testar `ping 192.168.1.100` dentro do CT 103 |
| CrowdSec baniu o CT 103 | Múltiplas tentativas falhadas | `sudo cscli decisions delete --ip 192.168.1.103`; adicionar CT à whitelist se necessário |
| SSH pede só senha (sem chave) | Chave não passada corretamente | Usar `-i /caminho/para/chave`; confirmar `IdentityFile` no `~/.ssh/config` |
| Tails: `nc: invalid option -- 'X'` | Versão antiga do netcat no Tails | Usar `socat` em vez de `nc`: `ProxyCommand="socat - SOCKS4A:127.0.0.1:%h:%p,socksport=9050"` |

---

## N.8 Segurança e boas práticas

```bash
# Backup das chaves do Hidden Service (guarde em local seguro cifrado):
pct exec 103 -- tar czf - /var/lib/tor/ssh_hidden/ | \
  gpg --symmetric --cipher-algo AES256 -o tor-hidden-keys-backup.tar.gz.gpg
# Transferir para o PC e guardar no Bitwarden como anexo cifrado

# O endereço .onion é determinístico a partir das chaves:
# Se perder as chaves → perde o endereço .onion → terá de gerar um novo
# (o servidor continua a funcionar, mas clientes que sabiam o .onion antigo perdem o acesso)

# Verificar logs do Tor para actividade suspeita:
pct exec 103 -- journalctl -u tor -f
```

> **Nunca partilhe o endereço .onion publicamente** — ele não revela o seu IP, mas qualquer pessoa com ele pode tentar aceder ao SSH (ainda protegido por chave + TOTP, mas reduz o obscurantismo).

> **Hidden Service v3** (padrão desde Tor 0.3.5+): endereços têm 56 caracteres (`.onion` v3 — mais seguro que v2 de 16 caracteres). O Tor instala v3 por omissão desde 2021. Confirme: `cat /var/lib/tor/ssh_hidden/hostname | wc -c` → deve ser 63 (56 chars + `.onion` + newline).

---

```bash
echo "## $(date +"%F %H:%M") - Apêndice N concluído" >> ~/fortaleza-lab/diario.md
echo "- CT 103 (tor-hidden) ativo com Hidden Service" >> ~/fortaleza-lab/diario.md
echo "- Endereço .onion guardado no Bitwarden" >> ~/fortaleza-lab/diario.md
echo "- Chaves Tor com backup cifrado GPG" >> ~/fortaleza-lab/diario.md
```

---

# 🔗 Apêndice I — Fontes oficiais por fase

Este guia é **pedagógico** e foi confrontado com documentação oficial em 2026-05-12 (detalhe em [docs/audit-matrix.md](docs/audit-matrix.md)). Use sempre as fontes abaixo como verdade final quando houver ambiguidade.

### Fase 0 — SO, rede, APT

| Tópico | Fonte |
|--------|--------|
| Repositórios deb822, enterprise, no-subscription, Ceph, chave GPG Trixie | [Package Repositories](https://pve.proxmox.com/wiki/Package_Repositories) |
| Instalação PVE em Debian 13 | [Install Proxmox VE on Debian 13 Trixie](https://pve.proxmox.com/wiki/Install_Proxmox_VE_on_Debian_13_Trixie) |
| Debian 13 “Trixie” | [Debian Releases — Trixie](https://www.debian.org/releases/trixie/) |
| NTP / relógio | [timedatectl](https://www.freedesktop.org/software/systemd/man/systemd.time.html) (systemd); prática TOTP alinhada a [RFC 6238](https://www.rfc-editor.org/rfc/rfc6238) |

### Fases 1–3 — usuário, SSH, 2FA

| Tópico | Fonte |
|--------|--------|
| OpenSSH 10 (ex.: remoção DSA) | [OpenSSH 10.0 release notes](https://www.openssh.com/txt/release-10.0) |
| Manual `sshd_config` / `UsePAM` / `AuthenticationMethods` | `man sshd_config` na sua instalação Debian |
| PAM / Google Authenticator | [Debian Wiki — Two-factor authentication with SSH](https://wiki.debian.org/Two-factor_authentication_with_SSH) (referência geral; pacote `libpam-google-authenticator`) |

### Fase 4 — CrowdSec

| Tópico | Fonte |
|--------|--------|
| Instalação Linux (repositório + `apt install`) | [Install on Linux](https://docs.crowdsec.net/u/getting_started/installation/linux/) |
| Bouncers / firewall | [Firewall bouncer](https://docs.crowdsec.net/u/bouncers/firewall) |

### Fase 5 — LXC + Tailscale

| Tópico | Fonte |
|--------|--------|
| Tailscale em LXC não privilegiado | [Tailscale in LXC containers](https://tailscale.com/docs/features/containers/lxc/lxc-unprivileged) |
| `pct` / containers | [Proxmox VE Administration Guide — pct](https://pve.proxmox.com/pve-docs/chapter-pct.html) |

### Fase 6 — usuário e TFA na GUI

| Tópico | Fonte |
|--------|--------|
| Permissões e usuários | [User Management](https://pve.proxmox.com/wiki/User_Management) (wiki PVE) |

### Fase 7 — firewall

| Tópico | Fonte |
|--------|--------|
| Firewall (incl. nftables, `proxmox-firewall`, arquivos em `/etc/pve/firewall/`) | [Firewall](https://pve.proxmox.com/wiki/Firewall) |

### Fases 8–10 — ShellHub, manutenção, backups

| Tópico | Fonte |
|--------|--------|
| ShellHub | [ShellHub Documentation](https://docs.shellhub.io/) |
| Atualizações não interactivas Debian | [UnattendedUpgrades](https://wiki.debian.org/UnattendedUpgrades) |
| Política de reinício após upgrades (`needrestart`) | [needrestart (GitHub)](https://github.com/liske/needrestart) — ler `needrestart.conf` antes de alterar `$nrconf{restart}` |
| Certificados TLS / GUI após restore ou novo nó | [Certificate Management](https://pve.proxmox.com/wiki/Certificate_Management) |

### Anúncios de versão Proxmox

- [Fórum — anúncios / release notes](https://forum.proxmox.com/forums/announcements.11/) (ex.: tópicos VE 9.1, 9.2, …)

### Ferramentas de terceiros (opcional, não oficiais PVE)

| Ferramenta | Nota |
|-------------|------|
| [ProxMenux](https://proxmenux.com/) | Menu shell para administração; [intro](https://proxmenux.com/docs/introduction). Verificar fonte antes de instalar. |
| [linux-comandos-fundamentos.md](docs/linux-comandos-fundamentos.md) | Cheat sheet Linux (VMs de estudo); ver aviso de âmbito no cabeçalho. |
| [roadmap-hardware.md](docs/roadmap-hardware.md) | Evolução prevista do hardware do lab. |

---

*Repositório: documentação do projeto Fortaleza Proxmox (homelab).*
*Última revisão cruzada com fontes oficiais: 2026-05-12 — ver [docs/audit-matrix.md](docs/audit-matrix.md).*
*Dúvidas, correções ou sugestões? Abra uma Issue no GitHub.*

**Próximo passo:** Quando estiver pronto para executar no laboratório, siga **uma fase de cada vez**, com backup e duas sessões SSH nas alterações críticas. Comece pela **Fase 0**.
