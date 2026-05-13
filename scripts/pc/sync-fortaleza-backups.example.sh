#!/usr/bin/env bash
# Exemplo para o SEU PC (Linux/macOS com bash) — puxa /root/backups do Proxmox.
# Copie para ~/bin ou similar, chmod +x, edite FORTALEZA_SSH.
#
# Variável FORTALEZA_SSH:
#   - Host do seu ~/.ssh/config (ex.: fortaleza) — Fase 2 §2.4 do guia
#   - OU usuario@IP (ex.: renato@192.168.1.100)
#
# Uso: ./sync-fortaleza-backups.example.sh
#
# SPDX-License-Identifier: MIT

set -euo pipefail

FORTALEZA_SSH="${FORTALEZA_SSH:-fortaleza}"
DEST="${HOME}/fortaleza-backups"

echo "Origem: ${FORTALEZA_SSH}:/root/backups/"
echo "Destino local: $DEST"
mkdir -p "$DEST"

rsync -avz --delete \
  "${FORTALEZA_SSH}:/root/backups/" \
  "$DEST/"

echo "OK. Lembre-se: isso não substitui cópia para disco externo / nuvem (Fase 10)."
