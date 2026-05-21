# Auditoria pré-publicação — Sentinela Proxmox v1.0 (canônica)

**Data:** 2026-05-20  
**Escopo:** repositório pronto para GitHub público  
**Responsável:** revisão interna (Projeto Colaborativo VIPs-com)  
**Veredito:** **APROVADO para publicação** — ressalvas menores documentadas abaixo.

---

## 1. Estrutura do repositório

| Critério | Resultado |
|----------|-----------|
| Guia canônico único | OK — [../sentinela-proxmox-v1.0.md](../sentinela-proxmox-v1.0.md) em `docs/` |
| Versão publicada | OK — **v1.0 (canônica)**; sem referências v4/v5 no material do aluno |
| Pasta `docs/interno/` | OK — changelog, revisão, validação, esta auditoria |
| Pasta `scripts/` | OK — apenas `sentinela-*` (sem duplicatas `fortaleza-*`) |
| Raiz limpa | OK — README, LICENSE, CONTRIBUTING, Makefile, `.gitignore` |

**Árvore publicada (25 ficheiros de conteúdo):**

```
README.md, LICENSE, CONTRIBUTING.md, Makefile, .gitignore
docs/sentinela-proxmox-v1.0.md, INDICE-CURSO.md, manual-usabilidade.md, mapa-do-curso.md, README.md
docs/audit-matrix.md, glossario.md, linux-comandos-fundamentos.md, roadmap-hardware.md, monitoramento-telegram.md
docs/interno/ (4 ficheiros + README)
scripts/ (health-check, telegram, pc/, systemd/)
```

---

## 2. Navegação do aluno (modelo Zero-Trust-Core)

| Peça | Ficheiro | Status |
|------|----------|--------|
| Cartão de visita | [../../README.md](../../README.md) | OK |
| Manual de uso | [../manual-usabilidade.md](../manual-usabilidade.md) | OK |
| Índice §1 | [../INDICE-CURSO.md](../INDICE-CURSO.md) | OK — 31 âncoras HTML no guia |
| Curso | [../sentinela-proxmox-v1.0.md](../sentinela-proxmox-v1.0.md) | OK — ~6288 linhas |

**Âncoras verificadas:** fases -1→10b, VM-01, apêndices A–N, `antes-de-comecar`, `dicas-aluno`, `glossario-completo`, `setor-2-host`.

---

## 3. Marca e consistência

| Verificação | Resultado |
|-------------|-----------|
| Título do guia | OK — `Sentinela Proxmox – VERSÃO 1.0 (canônica)` |
| Autor no guia | OK — Projeto Colaborativo (VIPs-com) |
| Referências «Fortaleza» no material aluno | OK — nenhuma no guia/README/docs públicos |
| Histórico v5 em `interno/CHANGELOG` | OK — aceitável (só manutenção) |
| Scripts e paths no host | OK — `sentinela-lab`, `chave_sentinela`, Host `sentinela` |

---

## 4. Segurança e `.gitignore`

| Item | Resultado |
|------|-----------|
| `.env`, chaves, `authorized_keys` | OK — no `.gitignore` |
| `**/etc-pve*.tar.gz`, `sentinela-backups/` | OK |
| `estado.json` (Telegram) | OK |
| Segredos de exemplo no guia | OK — passwords de lab claramente fictícias (Grafana etc.) com aviso «trocar» |
| Pasta `.claude/` | Adicionada ao `.gitignore` — não publicar worktrees locais |

---

## 5. Licença e contribuição

| Item | Resultado |
|------|-----------|
| [LICENSE](../../LICENSE) | CC BY-SA 4.0 presente |
| [CONTRIBUTING.md](../../CONTRIBUTING.md) | OK — fonte oficial em PRs |
| Alinhamento autor LICENSE vs guia | **Nota** — LICENSE diz «Renato»; guia diz «VIPs-com». Harmonizar no próximo commit se desejado (ambos válidos com atribuição). |

---

## 6. Conteúdo técnico (resumo)

| Área | Fonte cruzada | Status |
|------|---------------|--------|
| Fases 0–10 | [../audit-matrix.md](../audit-matrix.md) | OK + ressalvas documentadas (tech preview firewall, supply chain scripts) |
| Tailscale subnet | sysctl pós-`tailscale up` | OK — secção 5.4b |
| needrestart Fase 0.6 | modo `-r i` | OK |
| Trilha integrada | [Zero-Trust-Core](https://github.com/VIPs-com/Zero-Trust-Core) | OK — link no README e manual |

---

## 7. Ressalvas (não bloqueiam publicação)

1. **PVE 9.x em evolução** — aluno deve confirmar `pveversion` após updates; matriz data 2026-05-12/13.
2. **`proxmox-firewall` tech preview** — aviso explícito no README e guia.
3. **Scripts remotos** (`curl|sh`, community-scripts, Tailscale install) — avisos de supply chain presentes.
4. **Repositório local `.claude/`** — não versionar; está no `.gitignore`.

---

## 8. Checklist de publicação GitHub

- [x] Repositório público: [VIPs-com/Sentinela-Proxmox-VE-9](https://github.com/VIPs-com/Sentinela-Proxmox-VE-9) (renomeado de `sentinela-proxmox`)
- [ ] `git push` da branch `main` / `master`
- [ ] Tag **`v1.0.0`** com release notes (copiar resumo do README)
- [ ] Descrição do repo: link para [manual-usabilidade.md](../manual-usabilidade.md) e [INDICE-CURSO.md](../INDICE-CURSO.md)
- [ ] Topics sugeridos: `proxmox`, `homelab`, `debian`, `security`, `tutorial`, `portuguese`
- [ ] Link recíproco no [Zero-Trust-Core](https://github.com/VIPs-com/Zero-Trust-Core) (opcional, recomendado)

---

## 9. Sign-off

| Papel | Decisão | Data |
|-------|---------|------|
| Auditoria estrutura + links | Aprovado | 2026-05-20 |
| Material do aluno (sem legado Fortaleza/v5) | Aprovado | 2026-05-20 |
| Publicação GitHub | **Pronto** | 2026-05-20 |

---

*Projeto considerado **encerrado** na versão 1.0 (canônica). Evoluções futuras: v1.0.1 (correções) ou v1.1 (novas fases) com entrada em `CHANGELOG-repositorio.md`.*
