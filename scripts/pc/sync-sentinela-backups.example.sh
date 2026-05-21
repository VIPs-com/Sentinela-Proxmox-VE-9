#!/usr/bin/env bash
# Exemplo para o SEU PC (Linux/macOS com bash) — puxa /root/backups do Proxmox.
# Copie para ~/bin ou similar, chmod +x, edite SENTINELA_SSH.
#
# Variável SENTINELA_SSH:
#   - Host do seu ~/.ssh/config (ex.: sentinela) — Fase 2 §2.4 do guia
#   - OU usuario@IP (ex.: renato@192.168.1.100)
#
# Uso: ./sync-sentinela-backups.example.sh
#
# SPDX-License-Identifier: MIT

set -euo pipefail

SENTINELA_SSH="${SENTINELA_SSH:-sentinela}"
DEST="${HOME}/sentinela-backups"

echo "Origem: ${SENTINELA_SSH}:/root/backups/"
echo "Destino local: $DEST"
mkdir -p "$DEST"

rsync -avz --delete \
  "${SENTINELA_SSH}:/root/backups/" \
  "$DEST/"

echo "OK. Lembre-se: isso não substitui cópia para disco externo / nuvem (Fase 10)."
