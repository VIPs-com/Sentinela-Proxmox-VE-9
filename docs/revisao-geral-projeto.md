# Revisão geral do projecto Fortaleza Proxmox — auditoria pedagógica e técnica

**Data da revisão:** 2026-05-12  
**Âmbito:** repositório `Fortaleza Proxmox` — guia principal, pasta `docs/`, `scripts/`, README.  
**Objectivo:** avaliar didáctica, consistência de comandos, usabilidade para iniciantes e lacunas; **não** substitui auditoria profissional nem pen-test.

---

## Metodologia (o que foi feito de facto)

| Actividade | Detalhe |
|------------|---------|
| Leitura estrutural | Início do guia (“Como usar”, Fase 0 parcial), secções de rede/SSH, changelog e remissões a `docs/`. |
| Métricas rápidas | Contagem de blocos `bash` vs blocos explícitos “Tradução” no [fortaleza-proxmox-v5.0.md](../fortaleza-proxmox-v5.0.md). |
| Coerência do repo | [docs/README.md](README.md), [CHANGELOG-repositorio.md](CHANGELOG-repositorio.md), [audit-matrix.md](audit-matrix.md). |

**Limite honesto:** não foi feita leitura linha-a-linha das ~2300 linhas do guia nem execução dos comandos num nó PVE nesta sessão. A matriz de auditoria continua a ser a referência cruzada com **fontes oficiais** por fase.

---

## Resultado global

| Critério | Avaliação |
|----------|-----------|
| Ordem pedagógica (Fases 0→10) | **Boa** — NTP antes de 2FA, backup antes de firewall, mensagem explícita “não pule fases”. |
| Comentários nos comandos | **Boa na amostra** (Fase 0 rede, repos) — muitos blocos explicam com `#` sem precisar do rótulo “Tradução”. |
| Blocos formais “Tradução” | **Poucos** no ficheiro inteiro; a maior parte da explicação está em comentários inline (aceitável, mas o novato pode não associar). |
| Consistência de voz (tu / você) | **Mista** — predominio de **você** (PT-BR); algumas frases em **tu** (PT-PT) em secções mais recentes; não afecta comandos. |
| Risco de cópia cega de IP | **Médio** — mitigado no texto da Fase 0; reforçado na nova secção **Dicas para o aluno** no guia principal. |
| Documentação satélite | **Organizada** — trilhas 0–4 em [README.md](README.md) da pasta `docs/`. |
| Changelog no guia | **Enxuto** — histórico editorial em [CHANGELOG-repositorio.md](CHANGELOG-repositorio.md). |

**Veredicto:** o projecto está **coerente e utilizável por um iniciante disciplinado** que segue o mapa e as dicas. Para “100%” no sentido enterprise, faltariam testes automatizados, revisão por segundo par e validação em múltiplas versões minor do PVE.

---

## Achados por prioridade

### P0 — Nenhum bloqueante legal/segurança detectado nesta revisão

Não foram encontrados tokens ou chaves versionadas na amostragem; o `.gitignore` cobre padrões sensíveis (ver README).

### P1 — Didáctica e usabilidade (melhorias contínuas)

1. **Secção “Dicas para o aluno”** — acrescentada ao [fortaleza-proxmox-v5.0.md](../fortaleza-proxmox-v5.0.md) (duas sessões SSH, ler antes de copiar, exemplos de IP, legenda OBJETIVO/FUNDAMENTO, onde ir quando empatar).  
2. **Uniformizar tu/você** — tarefa editorial longa; sugerido padronizar para **você** (ou **tu**) numa passagem única antes de “revisão final” pública.  
3. **Mais blocos “Tradução”** — opcional, nas fases 4–7 onde há muitas opções de firewall/CrowdSec, para quem aprende melhor com glossário após o bloco.

### P2 — Polish do produto

| Item | Nota |
|------|------|
| `LICENSE` na raiz | Ausente — útil se o repo for público. |
| `scripts/README.md` | Uma frase a apontar para [monitoramento-telegram-fortaleza-proxmox.md](monitoramento-telegram-fortaleza-proxmox.md). |
| Testes de comandos | Reexecutar passos críticos após cada `pveversion` / upgrade documentado na matriz. |

---

## O que já estava bem encaminhado (não mudar sem motivo)

- **Fase 0.2** — aviso de `ifreload` vs `restart networking`, comentários no `interfaces`.  
- **Fase 3.4** — alerta antes de reload/restart do SSH e teste em segunda janela.  
- **Fase 5.4** — ping antes do Tailscale no CT.  
- **Fase 7** — coexistência nft PVE + CrowdSec documentada.  
- **Apêndices** (G Bitwarden, H recuperação, I links).  
- **Script Telegram** — segredos por `EnvironmentFile`, `pvesh` como root documentado.

---

## Próximos passos sugeridos (checklist para ti)

- [ ] Ler a nova secção **Dicas para o aluno** no guia e dizer se queres mais exemplos (ex.: screenshot mental do `nano`).  
- [ ] Escolher **uma** variante de tratamento (você vs tu) e fazer um PR só de idioma.  
- [ ] Opcional: ficheiro `LICENSE` (MIT/CC-BY-SA conforme a tua decisão).  
- [ ] Após cada grande alteração no guia: uma linha em [CHANGELOG-repositorio.md](CHANGELOG-repositorio.md) e, se mudou risco técnico, actualizar [audit-matrix.md](audit-matrix.md).

---

*Este documento é metadocumentação: descreve o estado da revisão; não altera comandos do guia por si só.*
