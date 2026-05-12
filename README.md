# Fortaleza Proxmox

Documentação em Markdown para um homelab **Proxmox VE 9.x** (Debian 13 Trixie): rede, APT, SSH com 2FA, CrowdSec, Tailscale em LXC, firewall `proxmox-firewall`, ShellHub e rotinas de backup — com foco em não ficar trancado fora do servidor.

## Conteúdo

| Ficheiro | Descrição |
|----------|-----------|
| [fortaleza-proxmox-v5.0.md](fortaleza-proxmox-v5.0.md) | Guia principal (fases 0–10 e apêndices). |
| [docs/audit-matrix.md](docs/audit-matrix.md) | Matriz de auditoria: fases × fontes oficiais × conclusão (última revisão 2026-05-12). |

## Avisos

- Isto é **documentação de laboratório**, não substitui [suporte Proxmox](https://proxmox.com/en/proxmox-virtual-environment/pricing) nem auditoria profissional.
- **Não** faça commit de chaves SSH, `authorized_keys`, dumps de `/etc/pve` com segredos, nem ficheiros `.env` com passwords.
- O backend **nftables** do firewall Proxmox está descrito na [wiki](https://pve.proxmox.com/wiki/Firewall#nftables) como *tech preview*; leia a matriz de auditoria antes de usar em ambiente crítico.

## Ferramenta opcional (terceiros)

[ProxMenux](https://proxmenux.com/) — menu interactivo na shell para tarefas comuns em Proxmox VE ([documentação](https://proxmenux.com/docs/introduction)). **Não** é da Proxmox GmbH; revê o código e a política do projecto antes de instalar. O guia principal menciona-a na secção “Antes de Começar” e no FAQ.

## Contribuir

Issues e merge requests são bem-vindos para corrigir desatualizações ou melhorar o texto — cite sempre a **fonte oficial** quando alterar passos técnicos.
