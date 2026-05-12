# Validação linha-a-linha — Fortaleza Proxmox

Este ficheiro regista a **revisão manual** do conteúdo, **por partes**, com calma. Não substitui a [matriz de auditoria](audit-matrix.md) (fontes oficiais por fase).

**Como usar:** cada parte indica o intervalo de linhas do ficheiro [fortaleza-proxmox-v5.0.md](../fortaleza-proxmox-v5.0.md) (ou outro). O estado **Concluída** significa leitura + notas; **Correcções** lista alterações já aplicadas no repo.

---

## Convenções

| Estado | Significado |
|--------|-------------|
| Concluída | Texto relido; problemas anotados ou “nenhum bloqueante”. |
| Pendente | Ainda não revisto nesta sessão. |
| Correcção aplicada | Commit / diff associado (referência breve no texto da parte). |

---

## Parte 1 — Linhas 1–305 (cabeçalho, Dicas, Changelog, Antes de Começar, início Fase 0 até fim §0.1 NTP)

**Ficheiro:** `fortaleza-proxmox-v5.0.md`  
**Estado:** Concluída (2026-05-12)

### Verificações feitas

- Links relativos `docs/audit-matrix.md`, `docs/mapa-do-curso.md`, `docs/README.md`, `docs/revisao-geral-projeto.md`, `docs/CHANGELOG-repositorio.md` — coerentes com a árvore do repo.
- Secção **Dicas para o aluno** — coerente com a estrutura anunciada em “Como usar este guia”.
- **Pré-requisitos** — checklist alinhada ao fluxo (PVE 9, web, SSH root, físico, Bitwarden, TOTP, cabo).
- **§0.1 Timezone/NTP** — `timedatectl list-timezones | grep -i sao_paulo` e `set-timezone` correctos; bloco de saída esperada é ilustrativo (data de exemplo); nota de `systemd-timesyncd` adequada a Debian/PVE típico.

### Problemas encontrados e correcções

| Linha (aprox.) | Problema | Acção |
|----------------|----------|--------|
| Diagrama (~L144) | Texto `← "Some" da internet` — erro tipográfico / inglês ambíguo. | Substituído por texto claro em PT: tráfego da internet barrado (DROP). |
| ~L193 | `~/lab-diario.md` inconsistente com o resto do guia (`~/fortaleza-lab/diario.md` a partir da Fase 1). | Unificado com explicação: pasta na Fase 1 ou `mkdir` antecipado. |

### Observações não bloqueantes (P2)

- Mistura **você** / **tu** / **perceberes** no mesmo capítulo “Antes de Começar” e nas Dicas — tarefa editorial global (Parte futura ou PR só de idioma).
- Diagrama: “Roteador da sua casa” com espaços duplos antes do `│` — cosmético.
- **§0.2 em diante:** coberto na **Parte 2** (ver abaixo).

---

## Parte 2 — Linhas 306–647 (Fase 0: §0.2 IP fixo até checklist e nota ZFS)

**Ficheiro:** `fortaleza-proxmox-v5.0.md`  
**Estado:** Concluída (2026-05-12)

> **Nota:** o intervalo foi alargado em relação ao rascunho inicial (306–620) para incluir o **fecho completo da Fase 0** (checklist, lembrete do dataset), evitando cortar a §0.8 a meio.

### Verificações feitas

- **§0.2** — `ifreload` / `ifupdown2`, aviso de `restart networking`, exemplos `vmbr0` / `enp1s0` coerentes com o guia; lembrete de IP de exemplo.
- **§0.3** — `/etc/hosts` e `hostname -i` alinhados à [wiki](https://pve.proxmox.com/wiki/Network_Configuration) e quebras típicas de cluster.
- **§0.4** — deb822, painel vs `Enabled: no`, aviso contra `sed` em massa; ficheiro `pve-no-subscription.sources` com `Suites: trixie` coerente com PVE 9.
- **§0.5** — risco *supply chain* explícito; URL `community-scripts/ProxmoxVE` como referência auditável.
- **§0.6** — `apt full-upgrade` como root; `needrestart -k -r i` com comentário sobre o significado de `-k`.
- **§0.7** — `tar czf` de `/etc/pve` com data no nome; verificação `ls`.
- **§0.8** — snapshot ZFS com aviso de dataset; alternativa LVM-Thin.
- **Checklist Fase 0** — itens alinhados aos passos anteriores.

### Problemas encontrados e correcções

| Secção | Problema | Acção |
|--------|----------|--------|
| §0.3 | `ping -c 1 pve` assume hostname `pve`; quem tem `mini` ou outro nome falha o teste. | `ping -c 1 "$(hostname)"` + comentário; comandos `hostname` / `cat` com texto que exige consistência nome/IP. |
| Checklist Fase 0 | Item ZFS obrigatório mesmo sem pool ZFS. | Texto **ou N/A** com ênfase no backup `tar` quando não há ZFS. |

### Observações P2 (não corrigidas agora)

- Mistura **você** / **tu** / **activo** (PT-PT) vs **ativo** — harmonização global em parte futura.
- `wget` da chave GPG a partir de `enterprise.proxmox.com` na secção “Se deu errado” — funcional para obter keyring; quem bloqueia DNS a enterprise pode precisar de espelho (caso raro em homelab).

---

## Parte 3 — Linhas 648–1050 (Fase 1 e Fase 2–3 parcial)

**Estado:** Pendente

*(Intervalo ajustado após fecho da Parte 2.)*

---

## Parte 4 — Linhas 1051–1450 (Fase 4–5 CrowdSec / Tailscale)

**Estado:** Pendente

---

## Parte 5 — Linhas 1451–1850 (Fase 6–8)

**Estado:** Pendente

---

## Parte 6 — Linhas 1851–2250 (Fase 9–10 e apêndices iniciais)

**Estado:** Pendente

---

## Parte 7 — Linhas 2251–fim (FAQ, apêndices finais, fontes)

**Estado:** Pendente

---

## Outros ficheiros (validação separada)

| Ficheiro | Estado |
|----------|--------|
| [README.md](../README.md) raiz | Pendente |
| [docs/mapa-do-curso.md](mapa-do-curso.md) | Pendente |
| [docs/monitoramento-telegram-fortaleza-proxmox.md](monitoramento-telegram-fortaleza-proxmox.md) | Pendente |
| [scripts/fortaleza-telegram-monitor.py](../scripts/fortaleza-telegram-monitor.py) | Pendente |

---

*Última actualização: Parte 1 e Parte 2 — 2026-05-12.*
