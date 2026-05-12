# Fortaleza Proxmox — alvos de conveniência (bónus pós-guia)
# Correr na raiz do repositório; no Windows usa WSL ou Git Bash se tiveres `make` + `sudo` no alvo Linux.

.DEFAULT_GOAL := help
SHELL := /bin/bash

.PHONY: help check check-verbose check-json

help:
	@echo "Fortaleza Proxmox — make na raiz do repo (host Linux/PVE recomendado):"
	@echo "  make check          — health-check só-leitura (sudo)"
	@echo "  make check-verbose  — idem com --verbose"
	@echo "  make check-json     — idem com --json (uma linha: failures, warnings, ok)"

check:
	sudo bash scripts/fortaleza-health-check.sh

check-verbose:
	sudo bash scripts/fortaleza-health-check.sh --verbose

check-json:
	sudo bash scripts/fortaleza-health-check.sh --json
