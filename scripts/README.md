# Scripts e exemplos — Fortaleza Proxmox (bónus)

Estes ficheiros **não substituem** as [fases 0–10 do guia principal](../fortaleza-proxmox-v5.0.md): são **atalhos** depois de entenderes o que cada passo faz — ideais na **segunda instalação**, revisão anual, ou para fechares o lab com confiança.

**Segurança:** nunca faças commit de `.env`, tokens Telegram, chaves privadas, nem dumps de `/etc/pve` com segredos.

---

## 1. `fortaleza-health-check.sh` (host Proxmox)

Verificações **só-leitura**: NTP, serviço `ssh`, `sshd -T` (password/root), `pveversion`, disco `/`, ZFS (se existir), último backup `etc-pve-*.tar.gz` com `tar tzf`, CrowdSec + bouncer + `proxmox-firewall` se estiverem instalados, CTs 100/200 se existirem.

```bash
# No host (a partir da raiz do repositório clonado, ou copia o .sh para /root)
sudo bash scripts/fortaleza-health-check.sh
sudo bash scripts/fortaleza-health-check.sh --verbose
sudo bash scripts/fortaleza-health-check.sh --json
```

- Saída **verde / amarelo / vermelho** no terminal (modo normal); com **`--json`** imprime **só** uma linha: `{"failures":N,"warnings":M,"ok":true|false}` — útil para **cron**, CI ou agendadores.
- Exit `0` se não houver falhas críticas; `1` se houver pelo menos uma falha `[XX]`.

---

## 2. `fortaleza-telegram-monitor.py` (host Proxmox)

Alertas Telegram (RAM, disco, ZFS, CrowdSec digest, etc.). Instalação e variáveis de ambiente: [docs/monitoramento-telegram-fortaleza-proxmox.md](../docs/monitoramento-telegram-fortaleza-proxmox.md).

---

## 3. Systemd — backup diário de `/etc/pve` (alternativa ao cron)

Ficheiros em [systemd/](systemd/) (suffixo `.example` — copia **sem** o sufixo para `/etc/systemd/system/`):

| Ficheiro | Descrição |
|----------|-----------|
| [systemd/fortaleza-etc-pve-backup.service.example](systemd/fortaleza-etc-pve-backup.service.example) | Oneshot que chama `/usr/local/bin/backup-fortaleza.sh` (script da Fase 10). |
| [systemd/fortaleza-etc-pve-backup.timer.example](systemd/fortaleza-etc-pve-backup.timer.example) | Dispara todos os dias às **03:00** (ajusta `OnCalendar` se precisares). |

```bash
sudo cp scripts/systemd/fortaleza-etc-pve-backup.service.example /etc/systemd/system/fortaleza-etc-pve-backup.service
sudo cp scripts/systemd/fortaleza-etc-pve-backup.timer.example /etc/systemd/system/fortaleza-etc-pve-backup.timer
sudo systemctl daemon-reload
sudo systemctl enable --now fortaleza-etc-pve-backup.timer
systemctl list-timers | grep fortaleza
```

---

## 4. PC pessoal — `sync-fortaleza-backups.example.sh`

Em [pc/sync-fortaleza-backups.example.sh](pc/sync-fortaleza-backups.example.sh): `rsync` de `fortaleza:/root/backups/` ou `FORTALEZA_SSH=renato@IP ./sync-fortaleza-backups.example.sh`. Ver **Fase 10 §10.4** do guia.

---

## Árvore resumida

Na **raiz** do repositório existe também um [Makefile](../Makefile) com `make check`, `make check-verbose` e `make check-json` (Linux/PVE ou WSL).

```
scripts/
├── README.md
├── fortaleza-health-check.sh
├── fortaleza-telegram-monitor.py
├── systemd/
│   ├── fortaleza-etc-pve-backup.service.example
│   └── fortaleza-etc-pve-backup.timer.example
└── pc/
    └── sync-fortaleza-backups.example.sh
```
