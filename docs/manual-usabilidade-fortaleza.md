# Manual de usabilidade — repositório Fortaleza Proxmox

**Para quem é:** você abriu o GitHub ou o ZIP do projeto e quer **saber em que "andar" está** e **qual arquivo abrir a seguir** — sem misturar host Proxmox com VM de estudo, nem script bônus com fase obrigatória.

**O que este manual *não* é:** não substitui o [guia principal](../fortaleza-proxmox-v5.0.md); é o **GPS** até lá. Os passos técnicos continuam todos no guia.

---

## 1. Descubra o seu estágio (30 segundos)

Percorra a tabela **de cima para baixo**. A **primeira linha que descreve a sua situação** indica o estágio (A–E) onde deve começar na seção 2 em diante.

| Se a sua situação for… | Estágio |
|------------------------|---------|
| Ainda não sei se isto é "curso de Linux na VM" ou "endurecer o Proxmox no metal" | **A** |
| Já entendi que é o host PVE, mas não sei a ordem nem onde está cada coisa no repo | **B** |
| Tenho o Proxmox instalado e quero **executar** passo a passo | **C** |
| Já concluí (ou quase) as fases 0–10 e quero rever / automatizar / celebrar | **D** |
| Quero alertas Telegram ou sync de backups no meu PC **sem** refazer o curso | **E** |

---

## 2. Estágio A — "O que é isto mesmo?"

**O que fazer:** parar 10 minutos de instalar coisas.

1. Leia o [README](../README.md) da raiz (tabela de arquivos).
2. Abra o [mapa do curso](mapa-do-curso.md) — explica **HOST** (nó Proxmox) vs **VM** (laboratório dentro do PVE) vs **EXT** (material fora do repo).
3. Só depois abra o [índice `docs/README.md`](README.md) para ver **trilhas 0 a 4b**.

**Dica de usabilidade:** guarde nos favoritos do browser **dois** separadores fixos: o [guia principal](../fortaleza-proxmox-v5.0.md) e este manual — volte aqui sempre que se perder.

---

## 3. Estágio B — "Onde está o 'curso' e o que é satélite?"

| Pergunta | Resposta curta |
|----------|------------------|
| Onde está o **único** passo-a-passo do host? | [fortaleza-proxmox-v5.0.md](../fortaleza-proxmox-v5.0.md) — fases **-1 a 10b** + VM-01 + apêndices A–N |
| Onde fica a **ordem** das pastas e links? | [README.md](README.md) (esta pasta `docs/`) |
| O que é a **matriz**? | [audit-matrix.md](audit-matrix.md) — cruzamento com **fontes oficiais**; *não* é lista de comandos para rodar às cegas |
| O que é **validação linha-a-linha**? | [validacao-linha-a-linha.md](validacao-linha-a-linha.md) — registro de revisão do guia; **não** é checklist de laboratório |

**O que fazer a seguir:** no guia principal, use `Ctrl+F` / `FASE 0` e leia a seção **"Dicas para o aluno"** no topo (regra das **duas sessões** SSH, IPs de exemplo, etc.).

---

## 4. Estágio C — "Estou executando no laboratório"

**Regra de ouro:** **uma fase de cada vez**, na ordem -1 → 10. Não pule fases "porque já vi num vídeo".

| Fase / bloco | Onde no guia | Lembrete de usabilidade |
|--------------|--------------|-------------------------|
| Bloco A (Fase -1 + 0) | Instalação ISO + Fundação, NTP, rede, APT | Sem NTP sincronizado, **TOTP falha** silenciosamente |
| Blocos B–C (1–4) | Usuário, SSH, 2FA, CrowdSec | Duas janelas SSH antes de `restart` de rede ou `sshd` |
| Bloco D (5–6) | Tailscale no CT, 2FA painel | Comandos no **CT** vs no **host** — o guia indica; leia o título da seção |
| Bloco E (7) | Firewall nftables | ACCEPT antes de DROP; leia *tech preview* na wiki |
| Bloco F (8) | Lab ShellHub / GPG | É **LXC**, não VM — texto do guia já alinha isto |
| Bloco G (9–10) | Updates, diário, backups | Aqui nasce o `~/fortaleza-lab/` e o runbook |

**Se travar:** no guia, vá para **"SE DEU ERRADO"** dessa fase; depois abra o [guia principal](../fortaleza-proxmox-v5.0.md) e procure pelo título **«Apêndice E — FAQ»**. Checklist final: seção **«Apêndice A — Checklist Final Consolidado»** no mesmo arquivo.

---

## 5. Estágio D — "Já fechei (ou quase) o lab"

**Objetivo:** confiança e manutenção sem refazer o curso.

| Ação | Onde |
|------|------|
| Verificação **só-leitura** no host | [scripts/README.md](../scripts/README.md) → `fortaleza-health-check.sh` ou `make check` / `make check-json` no [Makefile](../Makefile) |
| Backup agendado (alternativa ao cron) | Exemplos `systemd/` no mesmo índice |
| Copiar backups para o seu PC | `scripts/pc/sync-fortaleza-backups.example.sh` + Fase 10 §10.4 do guia |

**Dica:** rode o health-check **depois** de ter backups em `/root/backups` e SSH estável; assim você vê `[OK]` em verde e ganha moral para o resto.

---

## 6. Estágio E — "Operação contínua (opcional)"

Só faz sentido **depois** da base segura (idealmente após CrowdSec + firewall + rede, conforme o próprio doc).

| Quero… | Documento |
|--------|-------------|
| Alertas no Telegram | [monitoramento-telegram-fortaleza-proxmox.md](monitoramento-telegram-fortaleza-proxmox.md) + `scripts/fortaleza-telegram-monitor.py` |

**Usabilidade:** tokens e `.env` **nunca** no Git — use `EnvironmentFile` no servidor com permissões restritas, como descrito nesse documento.

---

## 7. Dicas extra (fechar com chave de ouro)

1. **Diário em tempo real:** o guia pede `echo ... >> ~/fortaleza-lab/diario.md` ao fim de cada fase — não acumule para "depois escrevo"; em 48h você já não vai lembrar do que deu errado.  
2. **Screenshot ou export:** após cada fase crítica (firewall, Tailscale), um print da GUI ou uma linha no diário poupa horas no futuro.  
3. **Versões:** antes de abrir issue ou perguntar ao professor, rode `pveversion` e `uname -r` e anote no diário — metade dos "comandos quebrados" são mismatch de versão.  
4. **Cheat sheet Linux:** [linux-comandos-fundamentos.md](linux-comandos-fundamentos.md) é para **VMs/CTs de estudo**, não para substituir o endurecimento do **host** — mantenha essa fronteira mental.  
5. **Quer contribuir?** [CONTRIBUTING.md](../CONTRIBUTING.md) — cite sempre fonte oficial em PRs que mudem comandos.

---

## 8. Mapa mental (uma frase por arquivo)

| Arquivo | Uma frase |
|---------|-----------|
| [fortaleza-proxmox-v5.0.md](../fortaleza-proxmox-v5.0.md) | O curso; você executa isto no **host** na ordem. |
| [mapa-do-curso.md](mapa-do-curso.md) | Onde encaixa HOST, VM e GPG. |
| [manual-usabilidade-fortaleza.md](manual-usabilidade-fortaleza.md) | Este GPS (estágios A–E). |
| [audit-matrix.md](audit-matrix.md) | Por que confiar (ou não) em cada bloco técnico. |
| [scripts/README.md](../scripts/README.md) | Bônus **após** dominar as fases. |

---

*Documento de usabilidade do repositório Fortaleza Proxmox. O conteúdo técnico canônico continua no guia principal e na wiki oficial citada na matriz.*
