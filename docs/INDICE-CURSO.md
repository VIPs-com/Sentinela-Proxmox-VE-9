# §1 — Índice do curso (links diretos)

**Arquivo do curso:** [sentinela-proxmox-v1.0.md](sentinela-proxmox-v1.0.md) — use este índice para pular fases e apêndices no GitHub ou no editor (`Ctrl+Click`).

**GPS do repositório:** [manual-usabilidade.md](manual-usabilidade.md) · **Mapa HOST/VM/GPG:** [mapa-do-curso.md](mapa-do-curso.md)

---

## Antes de começar (no guia)

| Seção | Link |
|-------|------|
| Antes de Começar — Leia Tudo | [Abrir](sentinela-proxmox-v1.0.md#antes-de-comecar) |
| Dicas para o aluno | [Abrir](sentinela-proxmox-v1.0.md#dicas-aluno) |
| Glossário completo | [Abrir](sentinela-proxmox-v1.0.md#glossario-completo) |

---

## Fases obrigatórias (ordem)

Execute **na sequência**. Não pule fases críticas de rede, SSH ou firewall.

| # | Fase | O que você ganha | Link |
|---|------|------------------|------|
| -1 | Instalação ISO | Pendrive, BIOS, ZFS vs LVM | [Fase -1](sentinela-proxmox-v1.0.md#fase-m1) |
| 0 | Fundação | IP fixo, NTP, APT, backup `/etc/pve` | [Fase 0](sentinela-proxmox-v1.0.md#fase-0) |
| 1 | Identidade | Usuário `sudo` no host | [Fase 1](sentinela-proxmox-v1.0.md#fase-1) |
| 2 | SSH | Chave Ed25519, adeus senha | [Fase 2](sentinela-proxmox-v1.0.md#fase-2) |
| 3 | 2FA SSH | TOTP no terminal | [Fase 3](sentinela-proxmox-v1.0.md#fase-3) |
| 4 | CrowdSec | Ban automático de IPs agressivos | [Fase 4](sentinela-proxmox-v1.0.md#fase-4) |
| 5 | Tailscale | Acesso remoto sem abrir portas | [Fase 5](sentinela-proxmox-v1.0.md#fase-5) |
| 6 | 2FA painel | `renato@pam` + TOTP na GUI | [Fase 6](sentinela-proxmox-v1.0.md#fase-6) |
| 7 | Firewall | `proxmox-firewall` / nftables | [Fase 7](sentinela-proxmox-v1.0.md#fase-7) |
| 8 | Lab irmão | ShellHub + exercício GPG | [Fase 8](sentinela-proxmox-v1.0.md#fase-8) |
| 9 | Manutenção | `unattended-upgrades`, `needrestart` | [Fase 9](sentinela-proxmox-v1.0.md#fase-9) |
| 10 | Documentação | Diário, runbook, `~/sentinela-lab/` | [Fase 10](sentinela-proxmox-v1.0.md#fase-10) |
| 10b | Backups vzdump | VMs/CTs + PBS (opcional avançado) | [Fase 10b](sentinela-proxmox-v1.0.md#fase-10b) |

---

## Laboratório Linux (após base do host)

| Fase | Link |
|------|------|
| VM-01 — Debian 13 de estudo + Cloud-Init | [Fase VM-01](sentinela-proxmox-v1.0.md#fase-vm-01) |
| Cheat sheet (dentro das VMs) | [linux-comandos-fundamentos.md](linux-comandos-fundamentos.md) |

---

## Apêndices (consulta e pós-curso)

| Apêndice | Conteúdo | Link |
|----------|----------|------|
| **A** | Checklist final + rotinas | [A](sentinela-proxmox-v1.0.md#apendice-a) |
| **B** | Monitoramento diário | [B](sentinela-proxmox-v1.0.md#apendice-b) |
| **C** | IDs, nomes, template de serviço | [C](sentinela-proxmox-v1.0.md#apendice-c) |
| **D** | Expansão: AdGuard, Vaultwarden, labs DNS/nginx… | [D](sentinela-proxmox-v1.0.md#apendice-d) |
| **E** | FAQ | [E](sentinela-proxmox-v1.0.md#apendice-e) |
| **F** | Glossário expandido | [F](sentinela-proxmox-v1.0.md#apendice-f) |
| **G** | Bitwarden — o que guardar | [G](sentinela-proxmox-v1.0.md#apendice-g) |
| **H** | Recuperação de desastre | [H](sentinela-proxmox-v1.0.md#apendice-h) |
| **I** | Fontes oficiais por fase | [I](sentinela-proxmox-v1.0.md#apendice-i) |
| **J** | Macetes PVE 9 + Cloud-Init | [J](sentinela-proxmox-v1.0.md#apendice-j) |
| **K** | Postura de segurança (honestidade) | [K](sentinela-proxmox-v1.0.md#apendice-k) |
| **L** | Próximos estudos | [L](sentinela-proxmox-v1.0.md#apendice-l) |
| **M** | Aliases de shell | [M](sentinela-proxmox-v1.0.md#apendice-m) |
| **N** | Tor Hidden Service | [N](sentinela-proxmox-v1.0.md#apendice-n) |

---

## Blocos do mapa (atalho mental)

| Bloco | Fases | Link mapa |
|-------|-------|-----------|
| **A** | -1, 0 | [mapa-do-curso.md — Setor 2](mapa-do-curso.md#setor-2-host) |
| **B** | 1–2 | idem |
| **C** | 3–4 | idem |
| **D** | 5–6 | idem |
| **E** | 7 | idem |
| **F** | 8 | idem |
| **G** | 9–10, 10b | idem |

---

*Sentinela Proxmox v1.0 (canônica) — [VIPs-com/Sentinela-Proxmox-VE-9](https://github.com/VIPs-com/Sentinela-Proxmox-VE-9)*
