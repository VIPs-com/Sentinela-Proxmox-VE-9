# Índice da pasta `docs/`

**Primeira vez na pasta `docs`? Lê isto na ordem.** Os ficheiros aqui **complementam** o guia principal na raiz do repositório; nenhum deles substitui as fases 0–10 do host.

| Trilha | Ficheiro | O que é |
|--------|----------|---------|
| **0 — Entrada** | [mapa-do-curso.md](mapa-do-curso.md) | Visão geral por setores (onboarding, blocos A–G no host, VM, GPG). **Começa aqui** se estiveres perdido. |
| **1 — Núcleo do curso (host)** | [fortaleza-proxmox-v5.0.md](../fortaleza-proxmox-v5.0.md) | Guia canónico: fases 0–10 e apêndices. É o único “curso” passo a passo do Proxmox endurecido. |
| **2 — Rastreio técnico** | [audit-matrix.md](audit-matrix.md) | Matriz fase × fonte oficial × conclusão. **Não** é lista de comandos a executar; serve para cruzar com a wiki e docs Proxmox/CrowdSec/etc. |
| **3 — Complementos pedagógicos** | [linux-comandos-fundamentos.md](linux-comandos-fundamentos.md) | Cheat sheet Linux para **VMs/CTs** de estudo (não confundir com checklist do host). |
| | [roadmap-hardware.md](roadmap-hardware.md) | Narrativa de hardware (mini PC → evolução). Opcional. |
| | [glossario.md](glossario.md) | Atalho ao glossário; a lista canónica longa está no guia principal (âncora `#glossario-completo`). |
| **4 — Operação (pós-lab)** | [monitoramento-telegram-fortaleza-proxmox.md](monitoramento-telegram-fortaleza-proxmox.md) | Alertas no telemóvel (Telegram). **Não faz parte das fases 0–10**; usa depois da base segura (idealmente após Fases 4–7: CrowdSec, firewall, rede). Script: [../scripts/fortaleza-telegram-monitor.py](../scripts/fortaleza-telegram-monitor.py). |
| **Meta — Revisão do projecto** | [revisao-geral-projeto.md](revisao-geral-projeto.md) | Relatório de auditoria pedagógica/usabilidade (o que foi revisto, P1/P2, próximos passos). **Não** é fase de laboratório. |
| **Meta — Validação linha-a-linha** | [validacao-linha-a-linha.md](validacao-linha-a-linha.md) | Registo **por partes** da releitura do **guia principal** (Partes 1–7 concluídas). Os ficheiros na secção «Outros ficheiros» do mesmo doc continuam com validação em separado. |

## Histórico do repositório (não é matéria de exame)

Alterações a vários ficheiros do repo (matriz, mapa, refinamentos, etc.) estão em [CHANGELOG-repositorio.md](CHANGELOG-repositorio.md). O **Changelog** no ficheiro do guia principal mantém-se **curto** para não misturar histórico editorial com o conteúdo das fases.

## Raiz do repositório (fora de `docs/`)

| Caminho | Uso |
|---------|-----|
| [../README.md](../README.md) | Cartão de visita do projecto e tabela resumida de ficheiros. |
| [../CONTRIBUTING.md](../CONTRIBUTING.md) | Como contribuir e o que citar em PRs. |
| [../scripts/README.md](../scripts/README.md) | Índice mínimo dos scripts opcionais (Telegram). |
