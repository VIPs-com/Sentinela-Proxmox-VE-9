#!/usr/bin/env bash
# fortaleza-health-check.sh — Verificações só-leitura no host Proxmox (Fortaleza Proxmox).
# Não altera o sistema. Ideal após concluíres as fases 0–10 ou para revisão periódica.
#
# Uso:
#   sudo ./fortaleza-health-check.sh
#   sudo ./fortaleza-health-check.sh --verbose
#
# SPDX-License-Identifier: MIT

set -uo pipefail

VERBOSE=0
FAILURES=0
WARNINGS=0

case "${1:-}" in
-v | --verbose) VERBOSE=1 ;;
-h | --help)
	echo "Uso: sudo $0 [--verbose]"
	echo "  Verificações só-leitura. Usa sudo no host PVE para ler /root/backups e estado dos serviços."
	exit 0
	;;
esac

C_R='\033[0;31m'
C_G='\033[0;32m'
C_Y='\033[0;33m'
C_B='\033[0;34m'
C_N='\033[0m'

pass() { echo -e "${C_G}[OK]${C_N} $*"; }
warn() { echo -e "${C_Y}[!!]${C_N} $*"; WARNINGS=$((WARNINGS + 1)); }
fail() { echo -e "${C_R}[XX]${C_N} $*"; FAILURES=$((FAILURES + 1)); }
info() { [[ "$VERBOSE" -eq 1 ]] && echo -e "${C_B}[..]${C_N} $*" || true; }

if [[ "$(id -u)" -ne 0 ]]; then
	warn "Não estás como root/sudo — alguns testes (backups em /root/backups, pvesh) podem falhar ou omitir-se."
fi

# --- NTP ---
if timedatectl status 2>/dev/null | grep -qi 'synchronized: yes'; then
	pass "NTP: relógio sincronizado (timedatectl)."
else
	if timedatectl status 2>/dev/null | grep -qi 'System clock synchronized: yes'; then
		pass "NTP: relógio sincronizado."
	else
		fail "NTP: relógio não reporta sincronizado — TOTP/SSH podem falhar. Ver Fase 0."
	fi
fi

# --- SSH (unidade Debian 13) ---
if systemctl is-active --quiet ssh 2>/dev/null; then
	pass "Serviço ssh está activo."
elif systemctl is-active --quiet sshd 2>/dev/null; then
	pass "Serviço sshd está activo (não Debian típico)."
else
	fail "Serviço SSH não está activo (esperado: ssh no Debian 13)."
fi

if command -v sshd >/dev/null 2>&1; then
	pa="$(sshd -T 2>/dev/null | awk '/^passwordauthentication /{print $2}')"
	pr="$(sshd -T 2>/dev/null | awk '/^permitrootlogin /{print $2}')"
	info "sshd -T: passwordauthentication=$pa permitrootlogin=$pr"
	if [[ "${pa,,}" == "no" ]]; then
		pass "SSH: PasswordAuthentication desactivado."
	else
		fail "SSH: PasswordAuthentication não está 'no' (ver Fase 2)."
	fi
	if [[ "${pr,,}" == "no" ]] || [[ "${pr,,}" == "without-password" ]] || [[ "${pr,,}" == "prohibit-password" ]]; then
		pass "SSH: root não entra com password (PermitRootLogin coerente com endurecimento)."
	else
		warn "SSH: PermitRootLogin='$pr' — confirma se é intencional (Fase 2)."
	fi
else
	warn "Comando sshd não encontrado no PATH (teste SSH omitido)."
fi

# --- Proxmox ---
if command -v pveversion >/dev/null 2>&1; then
	v="$(pveversion | head -1)"
	pass "Proxmox: $v"
else
	warn "pveversion não encontrado (não parece host PVE?)."
fi

# --- Disco raiz ---
usep="$(df -P / 2>/dev/null | awk 'NR==2 {gsub(/%/,"",$5); print $5}')"
if [[ -n "$usep" ]] && [[ "$usep" -lt 90 ]]; then
	pass "Disco / com ~${usep}% de uso."
elif [[ -n "$usep" ]]; then
	warn "Disco / com ${usep}% de uso — considera limpeza ou mais storage."
else
	warn "Não foi possível ler uso de disco em /."
fi

# --- ZFS (opcional) ---
if command -v zpool >/dev/null 2>&1; then
	npools="$(zpool list -H -o name 2>/dev/null | wc -l)"
	npools="$(echo "${npools:-0}" | tr -d '[:space:]')"
	npools="${npools:-0}"
	if [[ "${npools}" -eq 0 ]]; then
		info "ZFS: sem pools importadas neste nó (OK se não usas ZFS)."
	else
		bad="$(zpool list -H -o health 2>/dev/null | grep -vc '^ONLINE$' || true)"
		if [[ "${bad:-0}" -eq 0 ]]; then
			pass "ZFS: $npools pool(s) com estado ONLINE."
		else
			warn "ZFS: existe pool com health != ONLINE — corre 'zpool status'."
		fi
	fi
else
	info "ZFS não instalado (N/A)."
fi

# --- Backups /etc/pve ---
BKDIR="/root/backups"
if [[ -d "$BKDIR" ]] && [[ -r "$BKDIR" ]]; then
	latest="$(ls -t "$BKDIR"/etc-pve-*.tar.gz 2>/dev/null | head -1 || true)"
	if [[ -n "${latest:-}" ]]; then
		if tar tzf "$latest" >/dev/null 2>&1; then
			pass "Backup legível: $(basename "$latest") (tar tzf OK)."
		else
			fail "Backup corrupto ou ilegível: $latest"
		fi
	else
		warn "Pasta $BKDIR existe mas sem etc-pve-*.tar.gz (Fase 0 / 10)."
	fi
else
	warn "Sem leitura em $BKDIR — corre com sudo ou cria backups (Fase 0 / 10)."
fi

# --- CrowdSec (opcional, pós-Fase 4) ---
if systemctl list-unit-files 2>/dev/null | grep -q '^crowdsec\.service'; then
	if systemctl is-active --quiet crowdsec 2>/dev/null; then
		pass "CrowdSec (crowdsec) activo."
	else
		warn "CrowdSec instalado mas serviço não activo."
	fi
else
	info "CrowdSec não instalado (N/A se ainda não fizeste Fase 4)."
fi

if systemctl list-unit-files 2>/dev/null | grep -q '^crowdsec-firewall-bouncer\.service'; then
	if systemctl is-active --quiet crowdsec-firewall-bouncer 2>/dev/null; then
		pass "Bouncer CrowdSec (nftables) activo."
	else
		warn "Bouncer CrowdSec instalado mas não activo."
	fi
fi

# --- proxmox-firewall (opcional, pós-Fase 7) ---
if systemctl list-unit-files 2>/dev/null | grep -q '^proxmox-firewall\.service'; then
	if systemctl is-active --quiet proxmox-firewall 2>/dev/null; then
		pass "proxmox-firewall activo."
	else
		info "proxmox-firewall instalado mas inactive (pode ser normal em algumas transições — ver Fase 7)."
	fi
fi

# --- CTs 100 / 200 (opcional) ---
if command -v pct >/dev/null 2>&1; then
	for id in 100 200; do
		if [[ -f "/etc/pve/lxc/${id}.conf" ]]; then
			st="$(pct status "$id" 2>/dev/null | awk '{print $2}')"
			if [[ "$st" == "running" ]]; then
				pass "CT $id em execução."
			else
				info "CT $id existe mas estado=${st:-?} (pode estar parado de propósito)."
			fi
		fi
	done
fi

echo ""
echo -e "${C_B}=== Resumo ===${C_N}"
echo " Avisos: $WARNINGS"
echo " Falhas: $FAILURES"
if [[ "$FAILURES" -eq 0 ]]; then
	echo -e "${C_G}Resultado: nenhuma falha crítica detectada nesta passagem.${C_N}"
	echo " Continua a documentar mudanças em ~/fortaleza-lab/diario.md"
	exit 0
else
	echo -e "${C_R}Resultado: corrige as falhas acima antes de considerar o nó 'fechado'.${C_N}"
	exit 1
fi
