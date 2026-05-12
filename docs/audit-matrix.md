# Matriz de auditoria — Fortaleza Proxmox v5.0

**Data da revisão cruzada com fontes oficiais:** 2026-05-12  
**Artefato auditado:** [fortaleza-proxmox-v5.0.md](../fortaleza-proxmox-v5.0.md)

Legenda: **OK** alinhado à documentação oficial; **Ajuste** texto ou comando precisava de correção/nota; **Risco** decisão de segurança ou supply chain a aceitar conscientemente.

---

## Visão por fase

| Fase | Tópico principal | Fontes oficiais consultadas | Resultado |
|------|------------------|----------------------------|-----------|
| 0 | NTP, rede estática, hostname, APT deb822, repos, updates, backup `/etc/pve`, ZFS | [Package Repositories](https://pve.proxmox.com/wiki/Package_Repositories), [Debian Trixie](https://www.debian.org/releases/trixie/), `timedatectl` (systemd) | **OK** + **Ajuste** (repos: wiki recomenda `Enabled: no` no enterprise; nome de ficheiro `proxmox.sources` vs nome arbitrário; ZFS: dataset varia; `ifreload` requer `ifupdown2` — guia verifica antes de aplicar rede) |
| 1 | Utilizador `sudo` | Debian Admin / `adduser` | **OK** |
| 2 | SSH Ed25519, `sshd_config.d`, `PermitRootLogin no` | [OpenSSH 10.0 release](https://www.openssh.com/txt/release-10.0) (remoção DSA), `sshd_config(5)` | **OK** + **Risco** `AllowTcpForwarding no` (endurecimento vs. túneis) |
| 3 | PAM TOTP, `KbdInteractiveAuthentication` | OpenSSH + `libpam-google-authenticator` | **OK** (evitar `ChallengeResponseAuthentication` obsoleto) |
| 4 | CrowdSec + bouncer | [Install on Linux](https://docs.crowdsec.net/u/getting_started/installation/linux/), [Firewall bouncer](https://docs.crowdsec.net/u/bouncers/firewall) | **OK** + **Risco** `curl \| sh`; pacote `crowdsec-firewall-bouncer-nftables` adequado em hosts nft; caminho de whitelist pode mudar entre versões — validar em `/etc/crowdsec/` após instalação |
| 5 | LXC + Tailscale + TUN | [Tailscale in LXC](https://tailscale.com/docs/features/containers/lxc/lxc-unprivileged), [Subnet routers](https://tailscale.com/kb/1019/subnets/), [pct](https://pve.proxmox.com/pve-docs/chapter-pct.html) | **OK** (`pct set --dev0 /dev/net/tun`, `keyctl`, `nesting`) + **Ajuste** (após `tailscale up`, verificar `sysctl net.ipv4.ip_forward`; aplicar `sysctl.d` manual só se `0`; cliente recente pode já configurar) + **Risco** `install.sh` |
| 6 | 2FA painel `pam` | Documentação GUI Proxmox (TFA) | **OK** (fluxo coerente com permissões PVE) |
| 7 | `proxmox-firewall`, nftables | [Firewall (Proxmox VE)](https://pve.proxmox.com/wiki/Firewall) | **Ajuste** — wiki: *tech preview*, **não indicada para produção**; após mudança de backend, VMs/CT podem precisar de reinício (citado na wiki); guia: `systemctl is-active pve-firewall` (interpretação `active` vs `inactive`) + `if`/`grep -q` em `iptables -L` para PVEFW |
| 8 | Docker em LXC, ShellHub, GPG | [ShellHub docs](https://docs.shellhub.io/), Docker [get.docker.com](https://get.docker.com/) | **OK** (padrão homelab) + **Risco** scripts remotos e nesting |
| 9 | `unattended-upgrades`, `needrestart` | Debian [UnattendedUpgrades](https://wiki.debian.org/UnattendedUpgrades), [needrestart](https://github.com/liske/needrestart) | **OK** + **Ajuste** (secção 9.1b: não promover `restart=a` como “fix” para SSH; ler modos `l`/`i`/`a`) |
| 10 | Backups, cron, documentação | Alinhado a boas práticas; `tar tzf` para integridade básica | **OK** |

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
| Interacção CrowdSec (nft) + `proxmox-firewall` | Vários consumidores nft no mesmo host; inspeccionar `nft list ruleset` + docs bouncer + wiki Firewall | **Ajuste** (nota qualitativa no guia Fase 4) |

---

## Sugestões externas analisadas e **não** incorporadas (ou incorporadas corrigidas)

| Sugestão | Motivo |
|----------|--------|
| `sed` para `$nrconf{restart} = 'a'` como “solução” a desconexões SSH | Modo **`a`** = reinício **automático** de serviços; pode **aumentar** surpresas. Em `unattended-upgrades` não-interactivo, o modo interactivo pode fazer fallback a *list-only* — ver [needrestart.conf](https://github.com/liske/needrestart/blob/master/ex/needrestart.conf). |
| `mv /etc/apt/sources.list.d/pve-enterprise.sources /root/` | Desorganiza o APT; a wiki documenta **`Enabled: no`** no deb822. |
| `ifupdown2` obrigatório para todos após IP fixo | Já é **default** em instalações PVE novas desde 7.x; só necessário se instalaste PVE em cima de Debian manual — ver [Network Configuration](https://pve.proxmox.com/wiki/Network_Configuration). |
| `tailscale status \| grep Userspace` como verificação canónica | Frágil entre versões; o guia usa **`ip addr show tailscale0`** (teste objectivo). |
| [ProxMenux](https://proxmenux.com/) como atalho de administração | Projecto de terceiros; o guia trata-o como **opcional** com aviso de *supply chain* (ver secção “Antes de Começar” e FAQ). |

---

## Documentação complementar (não substitui a auditoria por fase)

| Documento | Uso |
|-----------|-----|
| [linux-comandos-fundamentos.md](linux-comandos-fundamentos.md) | Cheat sheet Linux para **VMs/CTs** de estudo; explícito que **não** é checklist do host PVE. |
| [roadmap-hardware.md](roadmap-hardware.md) | Narrativa N5095 → i7 → Xeon; contexto do legado *Linux Foundation Lab*. |
| [mapa-do-curso.md](mapa-do-curso.md) | Visão geral por setores: onboarding, blocos A–G do guia Fortaleza, trilha Linux em VM, ponte para curso GPG externo/Obsidian. |
| [README.md](README.md) | Índice numerado da pasta `docs/` (trilhas 0 a 4); separa núcleo, complementos e operação opcional. |
| [CHANGELOG-repositorio.md](CHANGELOG-repositorio.md) | Histórico editorial do repositório; o changelog **curto** no guia principal remete aqui. |
| [validacao-linha-a-linha.md](validacao-linha-a-linha.md) | Validação manual do guia por partes (registo vivo; Partes 1–4 concluídas). |

## Próximas reverificações recomendadas

- Reexecutar `apt-cache policy` / versões CrowdSec ao mudar de minor PVE ou Debian.
- Reler a secção **nftables** da [wiki Firewall](https://pve.proxmox.com/wiki/Firewall#nftables) antes de cada major upgrade do Proxmox.
