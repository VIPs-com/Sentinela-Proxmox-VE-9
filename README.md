# 🛡️ Fortaleza Proxmox

![Status](https://img.shields.io/badge/status-pronto-brightgreen)
![Versão](https://img.shields.io/badge/versão-5.0-blue)
![Base](https://img.shields.io/badge/PVE-9.x_Debian_13_Trixie-blue)
[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC_BY--SA_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0/)

**Guia completo de homelab Proxmox VE 9.x** — do zero ao servidor seguro, invisível para a internet, com backups automáticos, acesso remoto sem expor portas e laboratório Linux pronto para estudar.

Escrito para o **mini PC N5095 com 16 GB RAM** (hardware barato, aprendizado real), mas funciona em qualquer hardware com Proxmox VE 9.x sobre Debian 13 Trixie.

---

## O que este guia cobre

### 🔒 Segurança do host (Fases -1 a 10b)

| Fase | O que você ganha |
|------|-----------------|
| **Fase -1** | Instalação via ISO: pendrive, BIOS, ZFS vs LVM-Thin |
| **Fase 0** | Fundação: IP fixo, NTP, repositórios, backup `/etc/pve`, snapshot ZFS |
| **Fase 1–2** | Usuário com `sudo` + SSH só com chave Ed25519 (adeus senhas) |
| **Fase 3–4** | 2FA TOTP no SSH + CrowdSec (ban automático de IPs agressivos) |
| **Fase 5–6** | Tailscale em LXC (acesso remoto zero-port) + 2FA no painel web |
| **Fase 7** | Firewall nftables: política DROP, servidor invisível para a internet |
| **Fase 8** | Lab isolado para o irmão: ShellHub + Docker + exercício GPG |
| **Fase 9–10** | Atualizações automáticas, diário de lab, runbook de recuperação |
| **Fase 10b** | Backups vzdump + Proxmox Backup Server |
| **Fase VM-01** | VM Debian 13 de estudo com Cloud-Init + snapshot base-limpa |

### 🚀 Expansão após a Fortaleza (Apêndice D — guias completos)

**Nível 1 — Serviços sempre ligados:**
- **§D.2.1 AdGuard Home** — DNS bloqueador de anúncios para a LAN inteira
- **§D.2.2 Vaultwarden** — Bitwarden self-hosted, senhas fora da nuvem
- **§D.2.3 Nginx Proxy Manager** — HTTPS para todos os serviços via Let's Encrypt
- **§D.2.4 Uptime Kuma** — alertas Telegram quando qualquer serviço cair

**Nível 2 — Laboratórios de estudo (construa, aprenda, destrua):**
- **§D.3.1 bind9 do zero** — zonas DNS, SOA, A/CNAME/MX, resolução recursiva
- **§D.3.2 nginx do zero** — virtual hosts, HTTPS com openssl, proxy reverso
- **§D.3.3 nftables do zero** — chains, DROP vs REJECT, stateful, persistência
- **§D.3.4 LAN simulada** — vmbr1 isolada, duas redes, VLAN tags

**Nível 3 — Infraestrutura avançada:**
- **§D.4.1 Prometheus + Grafana** — métricas do N5095, dashboard Node Exporter Full
- **§D.4.2 Ansible** — 3 playbooks prontos: health-check, criar CT, update-all

### 📚 Apêndices de referência (A–N)

| Apêndice | Conteúdo |
|----------|---------|
| **A** | Checklist final + rotinas semanal/trimestral/anual + calendário ZFS + scrub cron |
| **B** | Comandos de monitoramento diário (btop, fastfetch, ss, lynis, sensors) |
| **C** | Padrão de IDs/nomes/tags + template de documentação de serviço |
| **D** | Roadmap completo de expansão (Níveis 1, 2 e 3) |
| **E** | FAQ (Port Knocking, Tails OS, Termius 4G, Tor) |
| **F** | Glossário expandido |
| **G** | O que guardar no Bitwarden (checklist de segredos) |
| **H** | Plano de recuperação de desastre + ZFS rollback |
| **I** | Fontes oficiais por fase |
| **J** | Macetes PVE 9: J.1–J.10 (diagnóstico, hw, Cloud-Init, governor, vulnerabilidades CPU) |
| **K** | Postura de segurança — o que protege e o que não protege (honestidade) |
| **L** | Sequência de aprendizagem pós-Fortaleza |
| **M** | Aliases e boas práticas de shell (host PVE + VM estudo) |
| **N** | Tor Hidden Service completo — CT 103, `.onion`, Tails OS, Android/Orbot |

---

## Como começar

```
1. Clone ou baixe o repositório
2. Abra docs/manual-usabilidade-fortaleza.md — descubra em qual estágio você está (A–E)
3. Abra docs/mapa-do-curso.md — veja o mapa completo (host, VM, GPG)
4. Execute fortaleza-proxmox-v5.0.md na ordem: Fase -1 → Fase 0 → ... → Fase 10b
```

> **Perdido?** [Manual de usabilidade](docs/manual-usabilidade-fortaleza.md) (30 segundos para descobrir seu estágio) → [Mapa do curso](docs/mapa-do-curso.md) → [Índice docs/](docs/README.md)

---

## Arquivos

| Arquivo | O que é |
|---------|---------|
| [`fortaleza-proxmox-v5.0.md`](fortaleza-proxmox-v5.0.md) | **Guia principal** (~6200 linhas, Fases -1 a 10b + VM-01 + Apêndices A–N) |
| [`docs/manual-usabilidade-fortaleza.md`](docs/manual-usabilidade-fortaleza.md) | GPS do repositório: estágios A–E |
| [`docs/mapa-do-curso.md`](docs/mapa-do-curso.md) | Visão geral: HOST, VM, GPG, blocos A–G |
| [`docs/README.md`](docs/README.md) | Índice ordenado da pasta docs/ |
| [`docs/linux-comandos-fundamentos.md`](docs/linux-comandos-fundamentos.md) | Cheat sheet Linux para VMs/CTs de estudo |
| [`docs/audit-matrix.md`](docs/audit-matrix.md) | Matriz fase × fonte oficial × conclusão |
| [`docs/monitoramento-telegram-fortaleza-proxmox.md`](docs/monitoramento-telegram-fortaleza-proxmox.md) | Alertas Telegram (operação opcional, pós-base) |
| [`scripts/README.md`](scripts/README.md) | Health-check (`--json`), systemd, sync no PC |
| [`Makefile`](Makefile) | `make check` / `make check-json` |

---

## Filosofia

> **"Fundamentos antes da escala."**

Segurança e documentação no host primeiro. Laboratório que você pode destruir e recriar em segundos. Sem fingir um datacenter no primeiro dia.

Cada fase termina com **VERIFIQUE** (prova de que funcionou) e **SE DEU ERRADO** (troubleshooting do erro mais comum). A ordem das fases foi pensada para você nunca perder o acesso ao servidor.

---

## Hardware de referência

| Componente | Especificação |
|------------|--------------|
| CPU | Intel N5095 (Jasper Lake, 4 cores / 4 threads) |
| RAM | 16 GB DDR4 |
| Storage | SSD NVMe (ZFS RAID0) |
| Rede | Ethernet 1 GbE |
| Sistema | Proxmox VE 9.x sobre Debian 13 "Trixie" |

O guia funciona em qualquer hardware compatível com PVE 9.x — o N5095 é o hardware de referência com notas específicas de temperatura, ARC ZFS e CPU governor.

---

## Avisos

- Este é um **guia de laboratório pessoal**, não substitui [suporte Proxmox](https://proxmox.com/en/proxmox-virtual-environment/pricing) nem auditoria profissional de segurança.
- **Nunca** faça commit de chaves SSH, `authorized_keys`, dumps de `/etc/pve` com segredos ou arquivos `.env` com senhas.
- O backend **nftables** do `proxmox-firewall` está descrito na [wiki oficial](https://pve.proxmox.com/wiki/Firewall#nftables) como *tech preview*. Leia a [matriz de auditoria](docs/audit-matrix.md) antes de usar em produção.
- Verificado contra fontes oficiais em **2026-05-12/13**. Reexecute `apt-cache policy` e releia as seções relevantes após upgrades major do PVE ou Debian.

## Ferramenta opcional (terceiro)

[ProxMenux](https://proxmenux.com/) — menu interativo na shell para tarefas comuns em Proxmox VE. **Não** é da Proxmox GmbH; revise o código e a política do projeto antes de instalar. O guia menciona na seção "Antes de Começar" e no FAQ (Apêndice E).

## Contribuir

Issues e pull requests são bem-vindos para corrigir desatualizações ou melhorar o texto. Cite sempre a **fonte oficial** quando alterar passos técnicos. Ver [CONTRIBUTING.md](CONTRIBUTING.md) para o mínimo esperado em PRs.

---

*Licença: [CC BY-SA 4.0](LICENSE) — compartilhe e adapte com atribuição.*
