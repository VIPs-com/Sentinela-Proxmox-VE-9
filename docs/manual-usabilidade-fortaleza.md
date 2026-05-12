# Manual de usabilidade — repositório Fortaleza Proxmox

**Para quem é:** abriste o GitHub ou o ZIP do projecto e queres **saber em que “andar” estás** e **qual ficheiro abrir a seguir** — sem misturar host Proxmox com VM de estudo, nem script bónus com fase obrigatória.

**O que este manual *não* é:** não substitui o [guia principal](../fortaleza-proxmox-v5.0.md); é o **GPS** até lá. Os passos técnicos continuam todos no guia.

---

## 1. Descobre o teu estágio (30 segundos)

Percorre a tabela **de cima para baixo**. A **primeira linha que descreve a tua situação** indica o estágio (A–E) onde deves começar na secção 2 em diante.

| Se a tua situação for… | Estágio |
|------------------------|---------|
| Ainda não sei se isto é “curso de Linux na VM” ou “endurecer o Proxmox no metal” | **A** |
| Já percebi que é o host PVE, mas não sei a ordem nem onde está cada coisa no repo | **B** |
| Tenho o Proxmox instalado e quero **executar** passo a passo | **C** |
| Já concluí (ou quase) as fases 0–10 e quero rever / automatizar / celebrar | **D** |
| Quero alertas Telegram ou sync de backups no meu PC **sem** refazer o curso | **E** |

---

## 2. Estágio A — “O que é isto mesmo?”

**O que fazer:** parar 10 minutos de instalar coisas.

1. Lê o [README](../README.md) da raiz (tabela de ficheiros).
2. Abre o [mapa do curso](mapa-do-curso.md) — explica **HOST** (nó Proxmox) vs **VM** (laboratório dentro do PVE) vs **EXT** (material fora do repo).
3. Só depois abre o [índice `docs/README.md`](README.md) para ver **trilhas 0 a 4b**.

**Dica de usabilidade:** guarda nos favoritos do browser **dois** separadores fixos: o [guia principal](../fortaleza-proxmox-v5.0.md) e este manual — voltas aqui sempre que te perderes.

---

## 3. Estágio B — “Onde está o ‘curso’ e o que é satélite?”

| Pergunta | Resposta curta |
|----------|------------------|
| Onde está o **único** passo-a-passo do host? | [fortaleza-proxmox-v5.0.md](../fortaleza-proxmox-v5.0.md) — fases **0 a 10** + apêndices |
| Onde está a **ordem** das pastas e links? | [README.md](README.md) (esta pasta `docs/`) |
| O que é a **matriz**? | [audit-matrix.md](audit-matrix.md) — cruzamento com **fontes oficiais**; *não* é lista de comandos para correr à cega |
| O que é **validação linha-a-linha**? | [validacao-linha-a-linha.md](validacao-linha-a-linha.md) — registo de revisão do guia; **não** é checklist de laboratório |

**O que fazer a seguir:** no guia principal, usa `Ctrl+F` / `FASE 0` e lê a secção **“Dicas para o aluno”** no topo (regra das **duas sessões** SSH, IPs de exemplo, etc.).

---

## 4. Estágio C — “Estou a executar no laboratório”

**Regra de ouro:** **uma fase de cada vez**, na ordem 0 → 10. Não saltes fases “porque já vi num vídeo”.

| Fase / bloco | Onde no guia | Lembrete de usabilidade |
|--------------|--------------|-------------------------|
| Bloco A (Fase 0) | Fundação, NTP, rede, APT | Sem NTP sincronizado, **TOTP falha** silenciosamente |
| Blocos B–C (1–4) | Utilizador, SSH, 2FA, CrowdSec | Duas janelas SSH antes de `restart` de rede ou `sshd` |
| Bloco D (5–6) | Tailscale no CT, 2FA painel | Comandos no **CT** vs no **host** — o guia indica; lê o título da secção |
| Bloco E (7) | Firewall nftables | ACCEPT antes de DROP; lê *tech preview* na wiki |
| Bloco F (8) | Lab ShellHub / GPG | É **LXC**, não VM — texto do guia já alinha isto |
| Bloco G (9–10) | Updates, diário, backups | Aqui nasce o `~/fortaleza-lab/` e o runbook |

**Se empatares:** no guia, salta para **“SE DEU ERRADO”** dessa fase; depois abre o [guia principal](../fortaleza-proxmox-v5.0.md) e procura pelo título **«Apêndice E — FAQ»**. Checklist final: secção **«Apêndice A — Checklist Final Consolidado»** no mesmo ficheiro.

---

## 5. Estágio D — “Já fechei (ou quase) o lab”

**Objetivo:** confiança e manutenção sem refazer o curso.

| Acção | Onde |
|-------|------|
| Verificação **só-leitura** no host | [scripts/README.md](../scripts/README.md) → `fortaleza-health-check.sh` ou `make check` / `make check-json` no [Makefile](../Makefile) |
| Backup agendado (alternativa ao cron) | Exemplos `systemd/` no mesmo índice |
| Copiar backups para o teu PC | `scripts/pc/sync-fortaleza-backups.example.sh` + Fase 10 §10.4 do guia |

**Dica:** corre o health-check **depois** de teres backups em `/root/backups` e SSH estável; assim vês `[OK]` em verde e ganhas moral para o resto.

---

## 6. Estágio E — “Operação contínua (opcional)”

Só faz sentido **depois** da base segura (idealmente após CrowdSec + firewall + rede, conforme o próprio doc).

| Quero… | Documento |
|--------|-------------|
| Alertas no Telegram | [monitoramento-telegram-fortaleza-proxmox.md](monitoramento-telegram-fortaleza-proxmox.md) + `scripts/fortaleza-telegram-monitor.py` |

**Usabilidade:** tokens e `.env` **nunca** no Git — usa `EnvironmentFile` no servidor com permissões restritas, como descrito nesse documento.

---

## 7. Dicas extra (fechar com chave de ouro)

1. **Diário em tempo real:** o guia pede `echo ... >> ~/fortaleza-lab/diario.md` ao fim de cada fase — não acumules para “depois escrevo”; em 48h já não te lembras do que correu mal.  
2. **Screenshot ou export:** após cada fase crítica (firewall, Tailscale), um print da GUI ou uma linha no diário poupa horas no futuro.  
3. **Versões:** antes de abrir issue ou perguntar ao professor, corre `pveversion` e `uname -r` e anota no diário — metade dos “comandos quebrados” são mismatch de versão.  
4. **Cheat sheet Linux:** [linux-comandos-fundamentos.md](linux-comandos-fundamentos.md) é para **VMs/CTs de estudo**, não para substituires o endurecimento do **host** — mantém essa fronteira mental.  
5. **Queres contribuir?** [CONTRIBUTING.md](../CONTRIBUTING.md) — cita sempre fonte oficial em PRs que mudem comandos.

---

## 8. Mapa mental (uma frase por ficheiro)

| Ficheiro | Uma frase |
|----------|-----------|
| [fortaleza-proxmox-v5.0.md](../fortaleza-proxmox-v5.0.md) | O curso; executas isto no **host** na ordem. |
| [mapa-do-curso.md](mapa-do-curso.md) | Onde encaixa HOST, VM e GPG. |
| [manual-usabilidade-fortaleza.md](manual-usabilidade-fortaleza.md) | Este GPS (estágios A–E). |
| [audit-matrix.md](audit-matrix.md) | Porque confiar (ou não) em cada bloco técnico. |
| [scripts/README.md](../scripts/README.md) | Bónus **após** dominares as fases. |

---

*Documento de usabilidade do repositório Fortaleza Proxmox. O conteúdo técnico canónico continua no guia principal e na wiki oficial citada na matriz.*
