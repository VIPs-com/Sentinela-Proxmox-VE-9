# Mapa do laboratório — visão geral (v1.0)

**Função:** ponto de entrada único para não te perderes entre o host Proxmox, as VMs de estudo e o curso GPG/OpenPGP.  
**Guia técnico completo do host:** [fortaleza-proxmox-v5.0.md](../fortaleza-proxmox-v5.0.md) (abre no editor e usa `Ctrl+F` / `FASE N` para saltar).

---

## Legenda de trilhas

| Prefixo | Significado |
|---------|-------------|
| **HOST** | Nó Proxmox VE — segue **só** o guia Fortaleza (firewall PVE, CrowdSec, Tailscale no CT100, etc.). |
| **VM** | Debian (ou outro) **dentro** de VM/CT de laboratório — cheat sheet e UFW/`fail2ban` quando fizer sentido. |
| **EXT** | Material **fora** deste repositório (Obsidian, outro Git, PDF do professor). |

---

## O que há dentro de `docs/`

Lista **numerada** (trilhas 0 a 4), categorias **núcleo / complemento / operação** e links estáveis: **[README.md desta pasta](README.md)**. Abre esse ficheiro sempre que entrares na pasta `docs/` no GitHub ou no disco — evita confundir o guia principal com complementos e operação opcional. Relatório meta (o que foi revisto, lacunas P1/P2): [revisao-geral-projeto.md](revisao-geral-projeto.md).

---

## Setor 0 — Onboarding (antes de mexer no host)

**Objetivo:** saber *onde* vais e com *que* contas, sem instalar nada à cega.

- **Resultados esperados (trilha HOST concluída):** nó PVE com rede estável, repos corretos, SSH com chave + 2FA, painel com `renato@pam` + 2FA, CrowdSec, firewall nftables, acesso remoto sem port forwarding (Tailscale), lab do irmão opcional, backups e documentação viva.
- **Perfil:** mini PC (ex.: N5095, 16 GB RAM), homelab — **não** é roadmap de datacenter no dia 1.
- **Checklist de ferramentas:** Bitwarden, app TOTP, cabo Ethernet, acesso físico ao mini PC — ver **Antes de Começar** e **Apêndice G** no [guia Fortaleza](../fortaleza-proxmox-v5.0.md).
- **Leituras cruzadas:**
  - [audit-matrix.md](audit-matrix.md) — o que foi confrontado com docs oficiais.
  - [roadmap-hardware.md](roadmap-hardware.md) — evolução N5095 → máquinas mais fortes (opcional).
  - [ProxMenux](https://proxmenux.com/) (opcional) — menu shell; ver aviso de fonte no guia.

---

## Setor 1 — Mapa do curso (estás aqui)

1. Lê o **Setor 0** acima.  
2. Percorre o **Setor 2** na **ordem dos blocos A→G** (é a ordem do guia).  
3. Em paralelo ou depois: **Setor 3** (Linux nas VMs) quando tiveres guests de estudo.  
4. **Setor 4** (GPG): curso canónico no teu material **EXT** + prática no homelab na **Fase 8**.

```mermaid
flowchart LR
  mapa[mapa_do_curso]
  host[guia_Fortaleza]
  vm[linux_fundamentos]
  gpg_ext[curso_GPG_EXT]
  mapa --> host
  mapa --> vm
  mapa --> gpg_ext
  host --> f8[Fase8_lab]
  f8 --> gpg_ext
```

---

## Setor 2 — Trilha HOST: Fortaleza Proxmox (blocos A a G)

**Documento:** [fortaleza-proxmox-v5.0.md](../fortaleza-proxmox-v5.0.md) — procura no ficheiro pelo texto **`FASE N`**.

### Tabela rápida (tempo indicativo = ordem de grandeza para quem já tem ISO instalada)

| Bloco | Fases | Tema | Tempo indicativo |
|-------|-------|------|------------------|
| **A** | 0 | Fundação: NTP, IP, hostname, APT, backup, ZFS | 2–4 h |
| **B** | 1–2 | Identidade (`sudo`) e SSH só com chave | 1–2 h |
| **C** | 3–4 | 2FA SSH (TOTP) e CrowdSec | 1–2 h |
| **D** | 5–6 | Tailscale (CT100) e 2FA no painel web | 1–2 h |
| **E** | 7 | Firewall `proxmox-firewall` (nftables) | 1–2 h |
| **F** | 8 | Lab irmão: Docker + ShellHub + exercício GPG | 2–3 h |
| **G** | 9–10 | Manutenção automática, diário, backups, runbook | 1–2 h |

### Bloco A — Fundação e rede **(HOST)**

- **Fase 0** — Preparação do sistema: timezone/NTP, IP fixo, `/etc/hosts`, repos Enterprise → No-Subscription, updates, backup `/etc/pve`, snapshot ZFS (ajusta o dataset ao teu `zfs list`), nota BIOS.

### Bloco B — Identidade e acesso SSH **(HOST)**

- **Fase 1** — Utilizador com `sudo`.  
- **Fase 2** — Chaves Ed25519, `sshd_config.d`, sem password no SSH.

### Bloco C — 2FA e vigilância **(HOST)**

- **Fase 3** — TOTP no SSH (PAM).  
- **Fase 4** — CrowdSec + bouncer nftables + whitelist.

### Bloco D — Acesso remoto e painel **(HOST)**

- **Fase 5** — LXC Tailscale + subnet routes.  
- **Fase 6** — `renato@pam` + TFA na GUI.

### Bloco E — Perímetro **(HOST)**

- **Fase 7** — Regras de firewall, DROP, backend nftables (*tech preview* na wiki).

### Bloco F — Lab partilhado **(HOST + CT)**

- **Fase 8** — CT irmão, ShellHub, GPG introdutório (ponte para Setor 4).

### Bloco G — Operação **(HOST)**

- **Fase 9** — `unattended-upgrades`, `needrestart` (ler 9.1b).  
- **Fase 10** — README local, diário, `backup-fortaleza.sh`, runbook, Git opcional.

**Apêndices do guia:** checklists (A), comandos (B), IDs (C), roadmap serviços (D), FAQ (E), Bitwarden (G), fontes (I) — consulta quando precisares, não precisas de os ler todos antes da Fase 0.

---

## Setor 3 — Trilha VM: Linux na prática **(VM)**

> **Pré-requisito:** Blocos **A** (Fase 0) e **B** (Fases 1–2) do guia Fortaleza concluídos e testados — SSH com chave a funcionar no host antes de abrir VMs de estudo prolongadas. O host seguro é a fundação; não pules para laboratório em VM “em paralelo” sem essa base.

- **Documento:** [linux-comandos-fundamentos.md](linux-comandos-fundamentos.md) — navegação, `systemctl`, rede, GPG resumo, Docker intro, UFW/`fail2ban` **só em guests**.  
- **Laboratório de redes (DMZ/LAN/WAN):** quando montares as VMs da oficina (firewall, DNS, WEB, cliente), podes criar um `notes/rede-lab.md` **dentro** da VM ou no teu `~/fortaleza-lab/` no host — placeholder para não esquecer.

---

## Setor 4 — Trilha OpenPGP / GPG **(EXT + HOST)**

- **Homelab (repo actual):** no guia Fortaleza, procura **`FASE 8`** — CT do irmão / exercício cifrar-assinar.  
- **Curso canónico** (mapa estilo *OpenPGP/GPG do Zero ao Expert*, Módulos 0–1, etc.): o detalhe completo fica no teu **Obsidian / outro repositório** — cola aqui o link quando tiveres:

  - **URL ou caminho do curso GPG:** `SUBSTITUIR_PELO_LINK_OU_CAMINHO` (ex.: `https://github.com/...` ou `obsidian://open?vault=...`)

  - **Como preencher:** edita esta linha em `docs/mapa-do-curso.md` (no repo ou no teu clone), grava o ficheiro e, se usares Git, `git commit -am "docs: link do curso GPG no mapa"` (ou mensagem equivalente). Não precisas de Git se só mantiveres cópia local.

Até lá, usa este ficheiro só para saber **que** o curso EXT existe e **onde** encaixa (depois da base HOST e em paralelo com prática na Fase 8).

---

## Checklist “onde estou?”

- [ ] Setor 0 lido  
- [ ] Bloco A (Fase 0) feito no host  
- [ ] Blocos B→G em sequência, com snapshots antes dos saltos perigosos  
- [ ] Setor 3 aberto quando fores estudar **dentro** de uma VM  
- [ ] Setor 4: link EXT preenchido + Fase 8 feita ou em curso  

---

*Última revisão estrutural: 2026-05-12 — alinhado ao repositório Fortaleza Proxmox.*
