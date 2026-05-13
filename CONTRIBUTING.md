# Contribuir

Obrigado por considerar melhorar o Fortaleza Proxmox.

## Alterações técnicas (comandos, versões, caminhos)

- Cite sempre uma **fonte oficial** (wiki Proxmox, documentação Debian, Tailscale, CrowdSec, OpenSSH, etc.) no texto do PR ou na descrição do issue — link estável preferível.
- Se alterar uma fase do guia, verifique se a [matriz de auditoria](docs/audit-matrix.md) continua coerente; atualize a linha da fase quando o risco ou o alinhamento mudar.

## Reportar comando desatualizado

- Abra um issue com: versão do PVE (`pveversion`), saída do comando que falhou, e o que a documentação oficial diz agora (link).
- Se tiver um patch, um PR pequeno é preferível a um issue longo.

## Scripts opcionais (`scripts/`)

- Mantenha o **health-check** estritamente **só-leitura** (sem alterar firewall, APT nem arquivos de configuração).
- Exemplos **systemd** (`.example`): são modelos — o caminho canônico continua sendo criar o script na Fase 10 e escolher `cron` **ou** `timer` conscientemente.
- No PR: indique se testou no PVE (versão `pveversion`) ou no bash do seu PC (para `pc/*.sh`). O alvo `make check-json` requer `make` + `sudo` no ambiente Linux (ou WSL).

## Estilo

- Mantenha o tom e vocabulário do guia: **português brasileiro (PT-BR)**, voz **você**.
- Evite duplicar blocos longos entre arquivos; prefira um link para a seção canônica no [guia principal](fortaleza-proxmox-v5.0.md).
