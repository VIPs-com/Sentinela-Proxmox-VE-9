# Fortaleza Proxmox

![Status](https://img.shields.io/badge/status-em_construção-yellow)
![Base](https://img.shields.io/badge/PVE-9.x-blue)

Documentação em Markdown para um homelab **Proxmox VE 9.x** (Debian 13 Trixie): rede, APT, SSH com 2FA, CrowdSec, Tailscale em LXC, firewall `proxmox-firewall`, ShellHub e rotinas de backup — com foco em não ficar trancado fora do servidor.

Perdido? Começa pelo [mapa do curso](docs/mapa-do-curso.md) (visão geral por setores: host, VM, GPG). **Lista ordenada de tudo em `docs/`:** [docs/README.md](docs/README.md) (trilhas 0 a 4).

**Filosofia:** o projecto assume *fundamentos antes da escala* — segurança e documentação no host, laboratório que podes partir e recuperar, sem fingir um datacenter no primeiro dia. Parte da narrativa veio do plano anterior **Linux Foundation Lab** (Debian 13 bare metal); o caminho actual é **Proxmox-first** no mini PC N5095, com evolução de hardware documentada para fases futuras.

## Conteúdo

| Ficheiro | Descrição |
|----------|-----------|
| [docs/README.md](docs/README.md) | **Índice da pasta docs** — ordem de leitura (trilhas 0 a 4); núcleo vs complemento vs operação. |
| [docs/mapa-do-curso.md](docs/mapa-do-curso.md) | Mapa do laboratório: onboarding, blocos A–G do host, trilha Linux em VM, ponte GPG/Obsidian. |
| [fortaleza-proxmox-v5.0.md](fortaleza-proxmox-v5.0.md) | Guia principal (fases 0–10 e apêndices). |
| [docs/audit-matrix.md](docs/audit-matrix.md) | Matriz de auditoria: fases × fontes oficiais × conclusão (última revisão 2026-05-12). |
| [docs/linux-comandos-fundamentos.md](docs/linux-comandos-fundamentos.md) | Cheat sheet Linux para **VMs/CTs de estudo** (não é checklist do host PVE). |
| [docs/roadmap-hardware.md](docs/roadmap-hardware.md) | Narrativa de hardware: mini PC actual → i7 → Xeon (opcional). |
| [docs/glossario.md](docs/glossario.md) | Atalho para o glossário (lista canónica no guia principal). |
| [docs/monitoramento-telegram-fortaleza-proxmox.md](docs/monitoramento-telegram-fortaleza-proxmox.md) | Operação opcional: alertas Telegram + script em `scripts/` (após base segura no host). |
| [docs/CHANGELOG-repositorio.md](docs/CHANGELOG-repositorio.md) | Histórico editorial do repositório (separado do changelog curto no guia). |
| [docs/revisao-geral-projeto.md](docs/revisao-geral-projeto.md) | Revisão geral (didáctica, usabilidade, checklist); meta-documentação. |
| [docs/validacao-linha-a-linha.md](docs/validacao-linha-a-linha.md) | Validação manual do guia **por partes** (registo vivo). |

## Avisos

- Isto é **documentação de laboratório**, não substitui [suporte Proxmox](https://proxmox.com/en/proxmox-virtual-environment/pricing) nem auditoria profissional.
- **Não** faça commit de chaves SSH, `authorized_keys`, dumps de `/etc/pve` com segredos, nem ficheiros `.env` com passwords.
- O backend **nftables** do firewall Proxmox está descrito na [wiki](https://pve.proxmox.com/wiki/Firewall#nftables) como *tech preview*; leia a matriz de auditoria antes de usar em ambiente crítico.

## Ferramenta opcional (terceiros)

[ProxMenux](https://proxmenux.com/) — menu interactivo na shell para tarefas comuns em Proxmox VE ([documentação](https://proxmenux.com/docs/introduction)). **Não** é da Proxmox GmbH; revê o código e a política do projecto antes de instalar. O guia principal menciona-a na secção “Antes de Começar” e no FAQ.

## Contribuir

Issues e merge requests são bem-vindos para corrigir desatualizações ou melhorar o texto — cite sempre a **fonte oficial** quando alterar passos técnicos. Ver [CONTRIBUTING.md](CONTRIBUTING.md) para o mínimo esperado em PRs e reportes de comando desatualizado.
