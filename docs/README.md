# Índice da pasta `docs/`

**Primeira vez no repositório?** Abra primeiro o [manual de usabilidade](manual-usabilidade-fortaleza.md) (estágios A–E: onde você está, o que abrir a seguir). **Primeira vez só na pasta `docs`?** Leia isto na ordem da tabela. Os arquivos aqui **complementam** o guia principal na raiz; nenhum substitui as fases 0–10 do host.

| Trilha | Arquivo | O que é |
|--------|---------|---------|
| **Guia de uso do repo** | [manual-usabilidade-fortaleza.md](manual-usabilidade-fortaleza.md) | **Pega na mão:** estágios A–E, arquivo certo em cada momento, dicas para não se perder entre host / VM / scripts. |
| **0 — Entrada** | [mapa-do-curso.md](mapa-do-curso.md) | Visão geral por setores (onboarding, blocos A–G no host, VM, GPG). **Comece aqui** se já leu o manual e quer o mapa do laboratório. |
| **1 — Núcleo do curso (host)** | [fortaleza-proxmox-v5.0.md](../fortaleza-proxmox-v5.0.md) | Guia canônico: fases -1 a 10b + VM-01 e apêndices A–N. É o único "curso" passo a passo do Proxmox endurecido. |
| **2 — Rastreio técnico** | [audit-matrix.md](audit-matrix.md) | Matriz fase × fonte oficial × conclusão. **Não** é lista de comandos a executar; serve para cruzar com a wiki e docs Proxmox/CrowdSec/etc. |
| **3 — Complementos pedagógicos** | [linux-comandos-fundamentos.md](linux-comandos-fundamentos.md) | Cheat sheet Linux para **VMs/CTs** de estudo (não confundir com checklist do host). |
| | [roadmap-hardware.md](roadmap-hardware.md) | Narrativa de hardware (mini PC → evolução). Opcional. |
| | [glossario.md](glossario.md) | Atalho ao glossário; a lista canônica longa está no guia principal (âncora `#glossario-completo`). |
| **4 — Operação (pós-lab)** | [monitoramento-telegram-fortaleza-proxmox.md](monitoramento-telegram-fortaleza-proxmox.md) | Alertas no celular (Telegram). **Não faz parte das fases 0–10**; use depois da base segura (idealmente após Fases 4–7: CrowdSec, firewall, rede). Script: [../scripts/fortaleza-telegram-monitor.py](../scripts/fortaleza-telegram-monitor.py). |
| **4b — Bônus automação** | [../scripts/README.md](../scripts/README.md) | Health-check (`--json`), exemplos **systemd**, sync no PC; na raiz: [Makefile](../Makefile) (`make check`). |
| **Meta — Revisão do projeto** | [revisao-geral-projeto.md](revisao-geral-projeto.md) | Relatório de auditoria pedagógica/usabilidade (o que foi revisado, P1/P2, próximos passos). **Não** é fase de laboratório. |
| **Meta — Validação linha-a-linha** | [validacao-linha-a-linha.md](validacao-linha-a-linha.md) | Registro **por partes** da releitura do **guia principal** (Partes 1–7 concluídas). Os arquivos na seção «Outros arquivos» do mesmo doc continuam com validação em separado. |

## Histórico do repositório (não é matéria de exame)

Alterações a vários arquivos do repo (matriz, mapa, refinamentos, etc.) estão em [CHANGELOG-repositorio.md](CHANGELOG-repositorio.md). O **Changelog** no arquivo do guia principal mantém-se **curto** para não misturar histórico editorial com o conteúdo das fases.

## Raiz do repositório (fora de `docs/`)

| Caminho | Uso |
|---------|-----|
| [../README.md](../README.md) | Cartão de visita do projeto e tabela resumida de arquivos. |
| [../CONTRIBUTING.md](../CONTRIBUTING.md) | Como contribuir e o que citar em PRs. |
| [../Makefile](../Makefile) | `make help` / `make check` / `make check-json` (Linux/PVE ou WSL; chama o health-check na raiz do clone). |
