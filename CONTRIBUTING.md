# Contribuir

Obrigado por considerares melhorar o Fortaleza Proxmox.

## Alterações técnicas (comandos, versões, caminhos)

- Cita sempre uma **fonte oficial** (wiki Proxmox, documentação Debian, Tailscale, CrowdSec, OpenSSH, etc.) no texto do PR ou na descrição do issue — link estável preferível.
- Se alterares uma fase do guia, verifica se a [matriz de auditoria](docs/audit-matrix.md) continua coerente; actualiza a linha da fase quando o risco ou o alinhamento mudar.

## Reportar comando desatualizado

- Abre um issue com: versão do PVE (`pveversion`), saída do comando que falhou, e o que a documentação oficial diz agora (link).
- Se tiveres patch, um MR pequeno é preferível a um issue longo.

## Estilo

- Mantém o tom e vocabulário do guia (português europeu onde o repositório já o usa).
- Evita duplicar blocos longos entre ficheiros; prefere um link para a secção canónica no [guia principal](fortaleza-proxmox-v5.0.md).
