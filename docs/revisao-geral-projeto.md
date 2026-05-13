# Revisão geral do projeto Fortaleza Proxmox — auditoria pedagógica e técnica

**Data da revisão:** 2026-05-12  
**Escopo:** repositório `Fortaleza Proxmox` — guia principal, pasta `docs/`, `scripts/`, README.  
**Objetivo:** avaliar didática, consistência de comandos, usabilidade para iniciantes e lacunas; **não** substitui auditoria profissional nem pen-test.

---

## Metodologia (o que foi feito de fato)

| Atividade | Detalhe |
|-----------|---------|
| Leitura estrutural | Início do guia ("Como usar", Fase 0 parcial), seções de rede/SSH, changelog e remissões a `docs/`. |
| Métricas rápidas | Contagem de blocos `bash` vs blocos explícitos "Tradução" no [fortaleza-proxmox-v5.0.md](../fortaleza-proxmox-v5.0.md). |
| Coerência do repo | [docs/README.md](README.md), [CHANGELOG-repositorio.md](CHANGELOG-repositorio.md), [audit-matrix.md](audit-matrix.md). |

**Limite honesto:** não foi feita leitura linha-a-linha das ~6200 linhas do guia nem execução dos comandos num nó PVE nesta sessão. A matriz de auditoria continua sendo a referência cruzada com **fontes oficiais** por fase.

---

## Resultado global

| Critério | Avaliação |
|----------|-----------|
| Ordem pedagógica (Fases 0→10) | **Boa** — NTP antes de 2FA, backup antes de firewall, mensagem explícita "não pule fases". |
| Comentários nos comandos | **Boa na amostra** (Fase 0 rede, repos) — muitos blocos explicam com `#` sem precisar do rótulo "Tradução". |
| Blocos formais "Tradução" | **Poucos** no arquivo inteiro; a maior parte da explicação está em comentários inline (aceitável, mas o novato pode não associar). |
| Consistência de voz | **PT-BR puro** — toda a documentação usa **você**; PT-PT zerado em 2026-05-13. |
| Risco de cópia cega de IP | **Médio** — mitigado no texto da Fase 0; reforçado na seção **Dicas para o aluno** no guia principal. |
| Documentação satélite | **Organizada** — trilhas 0–4 em [README.md](README.md) da pasta `docs/`. |
| Changelog no guia | **Enxuto** — histórico editorial em [CHANGELOG-repositorio.md](CHANGELOG-repositorio.md). |

**Veredicto:** o projeto está **coerente e utilizável por um iniciante disciplinado** que segue o mapa e as dicas. Para "100%" no sentido enterprise, faltariam testes automatizados, revisão por segundo par e validação em múltiplas versões minor do PVE.

---

## Achados por prioridade

### P0 — Nenhum bloqueante legal/segurança detectado nesta revisão

Não foram encontrados tokens ou chaves versionadas na amostragem; o `.gitignore` cobre padrões sensíveis (ver README).

### P1 — Didática e usabilidade (melhorias contínuas)

1. **Seção "Dicas para o aluno"** — acrescentada ao [fortaleza-proxmox-v5.0.md](../fortaleza-proxmox-v5.0.md) (duas sessões SSH, ler antes de copiar, exemplos de IP, legenda OBJETIVO/FUNDAMENTO, onde ir quando travar). ✅ Concluído.
2. **Uniformizar você** — padronizado em PT-BR em todo o repositório. ✅ Concluído em 2026-05-13.
3. **Mais blocos "Tradução"** — opcional, nas fases 4–7 onde há muitas opções de firewall/CrowdSec, para quem aprende melhor com glossário após o bloco.

### P2 — Polish do produto

| Item | Nota |
|------|------|
| `LICENSE` na raiz | ✅ Criado — CC-BY-SA 4.0. |
| `scripts/README.md` | ✅ Atualizado com todas as ferramentas bônus. |
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

## Próximos passos sugeridos (checklist para você)

- [x] Ler a nova seção **Dicas para o aluno** no guia.
- [x] Padronizar voz **você** (PT-BR) em todo o repositório.
- [x] Arquivo `LICENSE` (CC-BY-SA 4.0).
- [ ] Após cada grande alteração no guia: uma linha em [CHANGELOG-repositorio.md](CHANGELOG-repositorio.md) e, se mudou risco técnico, atualizar [audit-matrix.md](audit-matrix.md).

---

*Este documento é metadocumentação: descreve o estado da revisão; não altera comandos do guia por si só.*
