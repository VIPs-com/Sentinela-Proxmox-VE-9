#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""
fortaleza-telegram-monitor.py — alertas Telegram para homelab Fortaleza Proxmox.

Credenciais: variáveis de ambiente (ex.: systemd EnvironmentFile=/etc/fortaleza-monitor.env).
O manual pvesh(1) indica que apenas root pode usar pvesh — este script espera euid 0 para API PVE.

Uso:
  python3 fortaleza-telegram-monitor.py teste|alertas|polling|status|vms|top|seg|hw
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from typing import Any

try:
    import requests
except ImportError as e:
    print("Instale: apt install python3-requests", file=sys.stderr)
    raise SystemExit(1) from e

ESTADO_FILE = os.environ.get(
    "FORTALEZA_MONITOR_ESTADO", "/opt/fortaleza-monitor/estado.json"
)
LIMITE_RAM = int(os.environ.get("LIMITE_RAM_PORCENTO", "80"))
LIMITE_DISCO = int(os.environ.get("LIMITE_DISCO_PORCENTO", "80"))
THERMAL_MAX_MC = int(os.environ.get("THERMAL_MAX_MC", "85000"))


def _truthy(name: str, default: bool = True) -> bool:
    v = os.environ.get(name, "").strip().lower()
    if v in ("0", "false", "no", "off"):
        return False
    if v in ("1", "true", "yes", "on"):
        return True
    return default


DIGEST_CROWDSEC = _truthy("DIGEST_CROWDSEC", True)
DIGEST_THERMAL = _truthy("DIGEST_THERMAL", True)
DIGEST_ZFS = _truthy("DIGEST_ZFS", True)


def esc_html(s: object) -> str:
    t = str(s)
    return (
        t.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def require_root() -> None:
    if os.geteuid() != 0:
        print(
            "Aviso: não és root — pvesh e cscli podem falhar. "
            "O manual pvesh(1) restringe pvesh a root.",
            file=sys.stderr,
        )


def env_token_chat() -> tuple[str, str]:
    tok = os.environ.get("TELEGRAM_TOKEN", "").strip()
    cid = os.environ.get("TELEGRAM_CHAT_ID", "").strip()
    if not tok or not cid:
        print(
            "Defina TELEGRAM_TOKEN e TELEGRAM_CHAT_ID (ex.: /etc/fortaleza-monitor.env).",
            file=sys.stderr,
        )
        raise SystemExit(2)
    return tok, cid


def send_message(text: str, parse_mode: str | None = "HTML") -> bool:
    tok, cid = env_token_chat()
    url = f"https://api.telegram.org/bot{tok}/sendMessage"
    payload: dict[str, Any] = {"chat_id": cid, "text": text[:4096]}
    if parse_mode:
        payload["parse_mode"] = parse_mode
    try:
        r = requests.post(url, json=payload, timeout=20)
        if r.status_code != 200:
            print(r.text[:500], file=sys.stderr)
        return r.status_code == 200
    except OSError as e:
        print(f"Telegram: {e}", file=sys.stderr)
        return False


def pvesh_json(path: str) -> Any:
    """Chama pvesh como root; devolve object JSON ou None."""
    try:
        out = subprocess.check_output(
            ["pvesh", "get", path, "--output-format", "json"],
            text=True,
            stderr=subprocess.DEVNULL,
            timeout=60,
        )
        return json.loads(out)
    except (subprocess.CalledProcessError, json.JSONDecodeError, OSError):
        return None


def pve_node_name() -> str:
    forced = os.environ.get("PVE_NODE", "").strip()
    if forced:
        return forced
    data = pvesh_json("/nodes")
    if not data:
        return "localhost"
    if isinstance(data, list) and data:
        name = data[0].get("node")
        if isinstance(name, str) and name:
            return name
    return "localhost"


def ram_info() -> dict[str, float]:
    with open("/proc/meminfo", encoding="utf-8") as f:
        lines = {}
        for line in f:
            if ":" in line:
                k, rest = line.split(":", 1)
                parts = rest.split()
                if parts:
                    lines[k.strip()] = int(parts[0]) * 1024  # kB -> bytes
    total = lines.get("MemTotal", 1)
    avail = lines.get("MemAvailable", 0)
    used = total - avail
    pct = round(100.0 * used / total, 1)
    gb = 1024**3
    return {
        "pct": pct,
        "total_gb": round(total / gb, 1),
        "used_gb": round(used / gb, 1),
        "avail_gb": round(avail / gb, 1),
    }


def disk_root() -> dict[str, float]:
    st = os.statvfs("/")
    total = st.f_blocks * st.f_frsize
    free = st.f_bavail * st.f_frsize
    used = total - free
    pct = round(100.0 * used / total, 1) if total else 0.0
    gb = 1024**3
    return {
        "pct": pct,
        "total_gb": round(total / gb, 1),
        "used_gb": round(used / gb, 1),
        "free_gb": round(free / gb, 1),
    }


def load_state() -> dict[str, Any]:
    try:
        with open(ESTADO_FILE, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return {}


def save_state(data: dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(ESTADO_FILE) or ".", exist_ok=True)
    tmp = ESTADO_FILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=0)
    os.replace(tmp, ESTADO_FILE)


def list_guests() -> list[dict[str, Any]]:
    node = pve_node_name()
    out: list[dict[str, Any]] = []
    base = f"/nodes/{node}"

    qemu = pvesh_json(f"{base}/qemu")
    if isinstance(qemu, list):
        for vm in qemu:
            rawm = vm.get("maxmem") or vm.get("mem") or 0
            try:
                rawm = int(rawm)
            except (TypeError, ValueError):
                rawm = 0
            ram_mb = rawm // (1024 * 1024) if rawm else 0
            cpu = vm.get("cpu")
            cpu_pct = round(float(cpu) * 100, 1) if isinstance(cpu, (int, float)) else 0.0
            out.append(
                {
                    "tipo": "VM",
                    "id": vm.get("vmid"),
                    "nome": vm.get("name") or f"vm{vm.get('vmid')}",
                    "estado": vm.get("status", "?"),
                    "ram_mb": ram_mb,
                    "cpu": cpu_pct,
                }
            )

    lxc = pvesh_json(f"{base}/lxc")
    if isinstance(lxc, list):
        for ct in lxc:
            rawm = ct.get("maxmem") or ct.get("mem") or 0
            try:
                rawm = int(rawm)
            except (TypeError, ValueError):
                rawm = 0
            ram_mb = rawm // (1024 * 1024) if rawm else 0
            cpu = ct.get("cpu")
            cpu_pct = round(float(cpu) * 100, 1) if isinstance(cpu, (int, float)) else 0.0
            out.append(
                {
                    "tipo": "CT",
                    "id": ct.get("vmid"),
                    "nome": ct.get("name") or f"ct{ct.get('vmid')}",
                    "estado": ct.get("status", "?"),
                    "ram_mb": ram_mb,
                    "cpu": cpu_pct,
                }
            )
    return sorted(out, key=lambda x: (x.get("id") is None, x.get("id")))


def pve_version_line() -> str:
    try:
        out = subprocess.check_output(["pveversion"], text=True, timeout=10).strip()
        return out.split("/")[-1] if "/" in out else out
    except (subprocess.CalledProcessError, OSError):
        return "?"


def thermal_summary() -> str:
    lines = []
    base = "/sys/class/thermal"
    try:
        zones = sorted(
            d for d in os.listdir(base) if d.startswith("thermal_zone")
        )
    except OSError:
        return "Thermal: sysfs indisponível."
    for z in zones:
        try:
            with open(os.path.join(base, z, "type"), encoding="utf-8") as f:
                typ = f.read().strip()
            with open(os.path.join(base, z, "temp"), encoding="utf-8") as f:
                mc = int(f.read().strip())
            c = mc / 1000.0
            flag = " (!)" if mc > THERMAL_MAX_MC else ""
            lines.append(f"{z} ({typ}): {c:.1f} °C{flag}")
        except OSError:
            continue
    return "\n".join(lines) if lines else "Thermal: sem zonas lidas."


def zfs_summary() -> str:
    try:
        out = subprocess.check_output(
            ["zpool", "list", "-H", "-o", "name,health,size,free,cap"],
            text=True,
            stderr=subprocess.DEVNULL,
            timeout=20,
        )
    except (subprocess.CalledProcessError, OSError):
        return "ZFS: zpool não disponível ou sem pools."
    rows = [r.strip() for r in out.strip().splitlines() if r.strip()]
    if not rows:
        return "ZFS: sem saída de zpool list."
    return "\n".join(rows)


def crowdsec_decision_count() -> int | None:
    try:
        raw = subprocess.check_output(
            ["cscli", "decisions", "list", "-o", "json"],
            text=True,
            stderr=subprocess.DEVNULL,
            timeout=30,
        )
        data = json.loads(raw)
        if isinstance(data, list):
            return len(data)
        if isinstance(data, dict) and "new" in data:
            return len(data.get("new", []))
    except (subprocess.CalledProcessError, json.JSONDecodeError, OSError, ValueError):
        pass
    return None


def crowdsec_sample_text() -> str:
    try:
        raw = subprocess.check_output(
            ["cscli", "decisions", "list", "--limit", "8"],
            text=True,
            stderr=subprocess.DEVNULL,
            timeout=30,
        )
        return raw.strip()[:3500]
    except (subprocess.CalledProcessError, OSError):
        return "(cscli indisponível)"


def cmd_status() -> str:
    r = ram_info()
    d = disk_root()
    load = os.getloadavg()
    ver = esc_html(pve_version_line())
    node = esc_html(pve_node_name())
    em_r = "🔴" if r["pct"] >= LIMITE_RAM else ("🟡" if r["pct"] >= 70 else "🟢")
    em_d = "🔴" if d["pct"] >= LIMITE_DISCO else ("🟡" if d["pct"] >= 70 else "🟢")
    return (
        "📊 <b>Status host</b>\n"
        f"Nó PVE: <code>{node}</code>\n"
        f"Versão: <code>{ver}</code>\n\n"
        f"{em_r} <b>RAM</b> {r['used_gb']} / {r['total_gb']} GiB ({r['pct']}%)\n"
        f"{em_d} <b>Disco /</b> {d['used_gb']} / {d['total_gb']} GiB ({d['pct']}%)\n\n"
        f"⚙️ Load: {load[0]:.2f} {load[1]:.2f} {load[2]:.2f}"
    )


def cmd_vms() -> str:
    g = list_guests()
    if not g:
        return "⚠️ Sem dados de guests (pvesh falhou ou lista vazia)."
    lines = ["📦 <b>VMs / CTs</b>\n"]
    for i in g:
        ic = "🟢" if i["estado"] == "running" else "🔴"
        nm = esc_html(i["nome"])
        lines.append(
            f"{ic} [{i['tipo']}] <b>{nm}</b> id {i['id']} — {i['estado']} "
            f"RAM {i['ram_mb']} MiB CPU {i['cpu']}%"
        )
    return "\n".join(lines)


def cmd_top() -> str:
    g = [x for x in list_guests() if x["estado"] == "running"]
    g.sort(key=lambda x: x["ram_mb"], reverse=True)
    g = g[:5]
    if not g:
        return "Nenhum guest em <code>running</code>."
    lines = ["🏆 <b>Top 5 RAM (running)</b>\n"]
    for n, i in enumerate(g, 1):
        nm = esc_html(i["nome"])
        lines.append(f"{n}. {nm} ({i['tipo']}) — {i['ram_mb']} MiB")
    return "\n".join(lines)


def cmd_seg() -> str:
    n = crowdsec_decision_count()
    sample = esc_html(crowdsec_sample_text())
    if n is None:
        return "🛡️ <b>CrowdSec</b>\nContagem indisponível.\n<pre>" + sample + "</pre>"
    return f"🛡️ <b>CrowdSec</b>\nDecisões activas (aprox.): <b>{n}</b>\n<pre>{sample}</pre>"


def cmd_hw() -> str:
    th = esc_html(thermal_summary())
    zp = esc_html(zfs_summary())
    return "🌡️ <b>Hardware</b>\n<pre>" + th + "\n\n" + zp + "</pre>"


def cmd_start() -> str:
    return (
        "🛡️ <b>Fortaleza Monitor</b>\n"
        "/status /vms /top /seg /hw\n"
        "/ajuda — esta lista"
    )


def run_command(text: str) -> str:
    t = text.strip().split()[0].lower().split("@")[0]
    if t in ("/start", "/ajuda"):
        return cmd_start()
    if t == "/status":
        return cmd_status()
    if t == "/vms":
        return cmd_vms()
    if t == "/top":
        return cmd_top()
    if t == "/seg":
        return cmd_seg()
    if t == "/hw":
        return cmd_hw()
    return "Comando desconhecido. /ajuda"


def checar_alertas() -> None:
    estado = load_state()
    alertas = dict(estado.get("alertas", {}))
    novos_alert: dict[str, bool] = {}

    # RAM
    r = ram_info()
    key_ram = f"ram_{LIMITE_RAM}"
    if r["pct"] >= LIMITE_RAM:
        if not alertas.get(key_ram):
            send_message(
                "🔴 <b>ALERTA RAM</b>\n"
                f"{r['pct']}% ({r['used_gb']} / {r['total_gb']} GiB)\n"
                "Disponível: "
                f"{r['avail_gb']} GiB\n"
                "/top no bot para ver consumo por guest."
            )
            novos_alert[key_ram] = True
    else:
        novos_alert[key_ram] = False

    # Disco
    d = disk_root()
    key_d = f"disco_{LIMITE_DISCO}"
    if d["pct"] >= LIMITE_DISCO:
        if not alertas.get(key_d):
            send_message(
                "🔴 <b>ALERTA DISCO /</b>\n"
                f"{d['pct']}% usado ({d['used_gb']} / {d['total_gb']} GiB)\n"
                "Livre: "
                f"{d['free_gb']} GiB"
            )
            novos_alert[key_d] = True
    else:
        novos_alert[key_d] = False

    # Guests down/up
    atual = {str(x["id"]): x for x in list_guests()}
    prev_map: dict[str, Any] = estado.get("vms", {})
    for vid, item in atual.items():
        ant = (prev_map.get(vid) or {}).get("estado")
        st = item.get("estado")
        nm = esc_html(item.get("nome", ""))
        if ant == "running" and st != "running":
            send_message(
                "🔴 <b>Guest parado</b>\n"
                f"{item['tipo']} <b>{nm}</b> id {item['id']}\n"
                f"Estado: {esc_html(str(st))}"
            )
        elif ant and ant != "running" and st == "running":
            send_message(
                "🟢 <b>Guest a correr</b>\n"
                f"{item['tipo']} <b>{nm}</b> id {item['id']}"
            )

    # CrowdSec digest — alerta quando o número de decisões aumenta
    if DIGEST_CROWDSEC:
        cnt = crowdsec_decision_count()
        prev_c = estado.get("crowdsec_count")
        if cnt is not None and prev_c is not None and cnt > int(prev_c):
            send_message(
                "🛡️ <b>CrowdSec</b>\n"
                f"Decisões activas subiram: {prev_c} → <b>{cnt}</b>\n"
                "<pre>"
                + esc_html(crowdsec_sample_text()[:3000])
                + "</pre>"
            )
        if cnt is not None:
            estado["crowdsec_count"] = cnt

    # Thermal
    if DIGEST_THERMAL:
        try:
            with open(
                "/sys/class/thermal/thermal_zone0/temp", encoding="utf-8"
            ) as f:
                z0 = int(f.read().strip())
        except OSError:
            z0 = None
        if z0 is not None and z0 > THERMAL_MAX_MC:
            k = "thermal_high"
            if not alertas.get(k):
                send_message(
                    "🌡️ <b>ALERTA TEMPERATURA</b>\n"
                    f"thermal_zone0 ≈ {z0 / 1000.0:.1f} °C "
                    f"(limite {THERMAL_MAX_MC / 1000:.0f} °C)\n"
                    "Verifica poeira, pasta térmica e carga."
                )
                novos_alert[k] = True
        else:
            novos_alert["thermal_high"] = False

    # ZFS health — alerta só em mudança de estado (anti-spam)
    if DIGEST_ZFS:
        prev_zfs: dict[str, str] = dict(estado.get("zfs_health", {}))
        new_zfs: dict[str, str] = {}
        try:
            out = subprocess.check_output(
                ["zpool", "list", "-H", "-o", "name,health"],
                text=True,
                stderr=subprocess.DEVNULL,
                timeout=15,
            )
            for line in out.splitlines():
                parts = line.strip().split("\t")
                if len(parts) >= 2:
                    name, health = parts[0], parts[1]
                    new_zfs[name] = health
                    old = prev_zfs.get(name)
                    if health.upper() != "ONLINE" and old != health:
                        send_message(
                            "💾 <b>ZFS</b>\n"
                            f"Pool <code>{esc_html(name)}</code> health="
                            f"<b>{esc_html(health)}</b>"
                        )
                    if old and old.upper() != "ONLINE" and health.upper() == "ONLINE":
                        send_message(
                            "💾 <b>ZFS recuperado</b>\n"
                            f"Pool <code>{esc_html(name)}</code> voltou a "
                            "<code>ONLINE</code>"
                        )
        except (subprocess.CalledProcessError, OSError):
            new_zfs = prev_zfs
        estado["zfs_health"] = new_zfs

    estado["alertas"] = {**alertas, **novos_alert}
    estado["vms"] = atual
    save_state(estado)


def modo_polling() -> None:
    tok, my_cid = env_token_chat()
    print("Polling Telegram…", flush=True)
    offset = 0
    url = f"https://api.telegram.org/bot{tok}/getUpdates"
    while True:
        try:
            r = requests.get(
                url,
                params={"offset": offset, "timeout": 25},
                timeout=35,
            )
            if r.status_code != 200:
                print(f"getUpdates HTTP {r.status_code}", file=sys.stderr)
                time.sleep(5)
                continue
            data = r.json()
            if not data.get("ok", True):
                print(f"Telegram API: {data}", file=sys.stderr)
                time.sleep(5)
                continue
            for u in data.get("result", []):
                offset = u["update_id"] + 1
                msg = u.get("message") or {}
                chat = msg.get("chat") or {}
                if str(chat.get("id", "")) != str(my_cid):
                    continue
                text = msg.get("text") or ""
                if not text.startswith("/"):
                    continue
                reply = run_command(text)
                send_message(reply)
        except OSError as e:
            print(f"poll: {e}", file=sys.stderr)
            time.sleep(5)


def main() -> None:
    require_root()
    modo = sys.argv[1] if len(sys.argv) > 1 else ""

    if modo == "teste":
        ok = send_message("🛡️ Fortaleza Monitor — teste OK.")
        print("Enviado." if ok else "Falhou.")
        raise SystemExit(0 if ok else 1)

    if modo == "alertas":
        checar_alertas()
        return

    if modo == "polling":
        modo_polling()
        return

    if modo == "status":
        print(cmd_status().replace("<b>", "").replace("</b>", ""))
        return
    if modo == "vms":
        print(cmd_vms().replace("<b>", "").replace("</b>", "").replace("<code>", "").replace("</code>", ""))
        return
    if modo == "top":
        print(cmd_top().replace("<b>", "").replace("</b>", ""))
        return
    if modo == "seg":
        print(cmd_seg())
        return
    if modo == "hw":
        print(cmd_hw())
        return

    print(
        "Uso: fortaleza-telegram-monitor.py "
        "teste|alertas|polling|status|vms|top|seg|hw",
        file=sys.stderr,
    )
    raise SystemExit(2)


if __name__ == "__main__":
    main()
