# Roadmap de hardware (narrativa)

Este documento **não** obriga a compras nem a fases rígidas: descreve a **evolução pensada** do laboratório, do projecto anterior *Linux Foundation Lab* para o caminho actual **Fortaleza Proxmox**.

## Fase actual — Mini PC (Proxmox no N5095)

| Componente | Papel |
|--------------|--------|
| Intel Jasper Lake **N5095** | CPU do homelab principal |
| **16 GB** RAM | Orçamento apertado: VMs por turnos, host 24/7 com poucos guests ligados |
| **WD Red SN700 500 GB** (NVMe) | Disco principal do nó PVE (dados de CT/VM conforme escolha ZFS/LVM-thin) |
| **Samsung 870 EVO** (SATA) | ISO, templates, destino de `vzdump` / cópias (recomendado) |

**Papel:** hypervisor Proxmox + rede segura (guia Fortaleza) + VMs/CTs de estudo (firewall, DMZ, GPG, etc.).

---

## Fase intermédia (quando fizer sentido) — estação mais forte

| Componente | Papel pensado |
|--------------|----------------|
| **i7-4790K**, **32 GB** RAM, **GTX 1050 Ti** | Mais RAM e CPU para **KVM/libvirt** pesado, Docker avançado, labs que não cabem confortavelmente no N5095 |

Não é obrigatório: podes ficar só no mini PC até dominares o percurso do guia.

---

## Fase avançada (opcional, longo prazo) — “enterprise de brincar”

| Componente | Papel pensado |
|--------------|----------------|
| **Xeon E5-2650L**, **128 GB** ECC | Clustering, ZFS a maior escala, mais VMs em paralelo |

Isto é **horizonte** de aprendizagem (Proxmox cluster, storage avançado), não requisito do guia v5.0.

---

## Filosofia comum a todas as fases

- Fundamentos antes da escala; documentar antes de “crescer”.  
- **Sem port forwarding** na Internet para expor o lab (alinhado ao Fortaleza: Tailscale / acesso controlado).  
- O laboratório pode ser **reinstalado** — backups e snapshots existem para isso.

---

*Ver também [fortaleza-proxmox-v5.0.md](../fortaleza-proxmox-v5.0.md) e [linux-comandos-fundamentos.md](linux-comandos-fundamentos.md).*
