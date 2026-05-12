# Matriz de auditoria — Fortaleza Proxmox v5.0

**Data da revisão cruzada com fontes oficiais:** 2026-05-12  
**Artefato auditado:** [fortaleza-proxmox-v5.0.md](../fortaleza-proxmox-v5.0.md)

Legenda: **OK** alinhado à documentação oficial; **Ajuste** texto ou comando precisava de correção/nota; **Risco** decisão de segurança ou supply chain a aceitar conscientemente.

---

## Visão por fase

| Fase | Tópico principal | Fontes oficiais consultadas | Resultado |
|------|------------------|----------------------------|-----------|
| 0 | NTP, rede estática, hostname, APT deb822, repos, updates, backup `/etc/pve`, ZFS | [Package Repositories](https://pve.proxmox.com/wiki/Package_Repositories), [Debian Trixie](https://www.debian.org/releases/trixie/), `timedatectl` (systemd) | **OK** + **Ajuste** (repos: wiki recomenda `Enabled: no` no enterprise; nome de ficheiro `proxmox.sources` vs nome arbitrário; ZFS: dataset varia) |
| 1 | Utilizador `sudo` | Debian Admin / `adduser` | **OK** |
| 2 | SSH Ed25519, `sshd_config.d`, `PermitRootLogin no` | [OpenSSH 10.0 release](https://www.openssh.com/txt/release-10.0) (remoção DSA), `sshd_config(5)` | **OK** + **Risco** `AllowTcpForwarding no` (endurecimento vs. túneis) |
| 3 | PAM TOTP, `KbdInteractiveAuthentication` | OpenSSH + `libpam-google-authenticator` | **OK** (evitar `ChallengeResponseAuthentication` obsoleto) |
| 4 | CrowdSec + bouncer | [Install on Linux](https://docs.crowdsec.net/u/getting_started/installation/linux/), [Firewall bouncer](https://docs.crowdsec.net/u/bouncers/firewall) | **OK** + **Risco** `curl \| sh`; pacote `crowdsec-firewall-bouncer-nftables` adequado em hosts nft; caminho de whitelist pode mudar entre versões — validar em `/etc/crowdsec/` após instalação |
| 5 | LXC + Tailscale + TUN | [Tailscale in LXC](https://tailscale.com/docs/features/containers/lxc/lxc-unprivileged), [pct](https://pve.proxmox.com/pve-docs/chapter-pct.html) | **OK** (`pct set --dev0 /dev/net/tun`, `keyctl`, `nesting` conforme doc Tailscale) + **Risco** `install.sh` |
| 6 | 2FA painel `pam` | Documentação GUI Proxmox (TFA) | **OK** (fluxo coerente com permissões PVE) |
| 7 | `proxmox-firewall`, nftables | [Firewall (Proxmox VE)](https://pve.proxmox.com/wiki/Firewall) | **Ajuste** — wiki: *tech preview*, **não indicada para produção**; após mudança de backend, VMs/CT podem precisar de reinício (citado na wiki) |
| 8 | Docker em LXC, ShellHub, GPG | [ShellHub docs](https://docs.shellhub.io/), Docker [get.docker.com](https://get.docker.com/) | **OK** (padrão homelab) + **Risco** scripts remotos e nesting |
| 9 | `unattended-upgrades` | Debian [AutomaticUpdates](https://wiki.debian.org/UnattendedUpgrades) | **OK** |
| 10 | Backups, cron, documentação | Alinhado a boas práticas; sem conflito com PVE | **OK** |

---

## Itens sensíveis (detalhe)

| Afirmação / comando no guia | Verificação oficial | Status |
|------------------------------|---------------------|--------|
| deb822 `pve-no-subscription` com `Suites: trixie` | [Package Repositories](https://pve.proxmox.com/wiki/Package_Repositories) — exemplo idêntico (ficheiro sugerido `proxmox.sources`) | **OK** |
| Comentar enterprise com `sed` | Wiki prefere `Enabled: no` na entrada deb822 | **Ajuste** (ambos funcionam; `Enabled: no` é o método documentado) |
| `wget` keyring Trixie para `/usr/share/keyrings/proxmox-archive-keyring.gpg` | Mesma URL e caminho na wiki + verificação `sha256sum`/`sha512sum` publicada | **OK** |
| `proxmox-firewall` “estável no 9.1” | Wiki: *tech preview*, bugs possíveis, **not suited for production use** | **Ajuste** (corrigido no guia) |
| Reinício de VMs/CT após alternar backend firewall | Explícito na secção nftables da wiki | **OK** — considerar adicionar nota no guia |
| OpenSSH 10 remove DSA | [OpenSSH 10.0 release notes](https://www.openssh.com/txt/release-10.0) | **OK** |
| Serviço `ssh` vs `sshd` no Debian | Debian usa unidade `ssh` | **OK** |
| Tailscale + `/dev/net/tun` em LXC Proxmox | [Tailscale LXC doc](https://tailscale.com/docs/features/containers/lxc/lxc-unprivileged) cita `pct set` | **OK** |
| Instalação CrowdSec `curl -s https://install.crowdsec.net \| sudo sh` | Documentação oficial CrowdSec Linux | **OK** + **Risco** supply chain |
| `crowdsec-firewall-bouncer-nftables` | Pacote suportado (alternativa ao bouncer iptables); doc Linux mostra iptables como exemplo genérico | **OK** para host com nftables |
| Ficheiro whitelist `parsers/s02-enrich/whitelists.yaml` | Estrutura pode variar; pós-instalação: confirmar com `cscli parsers list` / árvore `/etc/crowdsec` | **Ajuste** (nota de validação no guia) |

---

## Próximas reverificações recomendadas

- Reexecutar `apt-cache policy` / versões CrowdSec ao mudar de minor PVE ou Debian.
- Reler a secção **nftables** da [wiki Firewall](https://pve.proxmox.com/wiki/Firewall#nftables) antes de cada major upgrade do Proxmox.
