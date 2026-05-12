# Linux — comandos de fundamentos (cheat sheet)

**Âmbito:** uso em **VMs ou CTs Debian de estudo** (laboratório, DMZ, exercícios de aula).  
**Não** substitui nem contradiz o [guia Fortaleza Proxmox](../fortaleza-proxmox-v5.0.md): no **host Proxmox** seguem-se as fases do guia (firewall `proxmox-firewall`, CrowdSec, SSH com chave + 2FA, etc.). Coisas como **UFW** ou **fail2ban** no legado “bare metal” fazem sentido **dentro** de guests Debian; **evita** empilhar UFW no nó PVE em paralelo com o firewall do Proxmox sem saber o que estás a fazer.

Origem conceptual: projecto anterior **Linux Foundation Lab** (Debian 13 minimal à mão). Este ficheiro condensa só a parte **reutilizável** de comandos e hábitos.

---

## Pastas úteis (na VM de estudo ou no teu utilizador no PVE)

Podes organizar assim (ajusta caminhos ao teu utilizador):

```bash
mkdir -p ~/lab ~/scripts ~/notes ~/gpg
```

No host Fortaleza já existe `~/fortaleza-lab/` (README, diário, recuperação) — podes espelhar a mesma ideia **dentro** de cada VM.

---

## Navegação e ficheiros

| Área | Comandos |
|------|----------|
| Onde estou / listar | `pwd`, `ls`, `ls -la` |
| Mudar pasta | `cd`, `cd -` |
| Procurar | `find`, `locate` (requer `plocate`/`mlocate`) |
| Copiar / mover / apagar | `cp`, `mv`, `rm`, `mkdir`, `touch` |
| Ver conteúdo | `cat`, `less`, `head`, `tail` |
| Editar | `nano`, `vim` |

---

## Sistema e serviços

| Tarefa | Comando |
|--------|---------|
| Serviços (systemd) | `systemctl status NOME`, `systemctl list-units --failed` |
| Logs | `journalctl -xe`, `journalctl -u ssh -f` |
| Recursos | `htop` ou `btop`, `free -h`, `df -h` |
| Discos / blocos | `lsblk` |

---

## Rede

| Tarefa | Comando |
|--------|---------|
| Interfaces | `ip a`, `ip r` |
| Ligações e portas | `ss -tulpen` |
| Teste | `ping`, `traceroute` |
| DNS | `dig`, `host` |
| Captura (cuidado em produção) | `tcpdump`, `nmap` (só em lab com permissão) |

---

## Hardware (visão rápida)

```bash
lscpu
lsblk
free -h
df -h
```

---

## SSH (cliente)

```bash
ip a                    # descobrir IP na VM
ssh utilizador@IP
```

No **host** Proxmox o guia Fortaleza configura **chave Ed25519 + 2FA** — não uses esta secção como modelo do servidor PVE.

---

## OpenPGP / GPG (resumo)

Objectivos típicos: chaves pública/privada, assinatura, cifra, identidade.

```bash
gpg --full-generate-key
gpg --list-keys
gpg --armor --export EMAIL
gpg --sign ficheiro.txt
gpg --encrypt --recipient EMAIL ficheiro.txt
```

Exercício guiado no lab do irmão / GPG: ver **Fase 8** do [guia principal](../fortaleza-proxmox-v5.0.md).

---

## Docker (quando chegares lá)

Instalação oficial em Debian: [Docker Engine — Debian](https://docs.docker.com/engine/install/debian/).

**Não** começar por Kubernetes / Swarm / Compose gigante — primeiro imagens, volumes, redes, um `Dockerfile` simples. No Fortaleza, Docker aparece no **CT do ShellHub** (Fase 8); stacks grandes ficam para VMs dedicadas quando tiveres RAM.

---

## Segurança mínima **dentro** de uma VM Debian (legado)

Isto **não** é o checklist do host PVE.

- Firewall tipo **UFW**: `ufw default deny incoming`, `ufw allow from LAN to any port 22`, `ufw enable`, `ufw status verbose`.
- **fail2ban**: `systemctl enable --now fail2ban`, `fail2ban-client status`.

No host Proxmox usa-se **CrowdSec** + regras do guia, não misturar à ligeira com UFW no mesmo nó.

---

## Primeira actualização (guest)

```bash
sudo apt update && sudo apt full-upgrade -y
```

Firmware (`intel-microcode`, `firmware-linux`, etc.) aplica-se sobretudo ao **metal** ou a VMs com pass-through; num CT típico o kernel é o do host.

---

## Pacotes úteis em VM de lab (lista curta)

```bash
sudo apt install -y sudo curl wget git vim nano htop tree zip unzip tar rsync \
  dnsutils traceroute ca-certificates gnupg gpg
```

Pacotes como `nmap`, `tcpdump`, `iftop`, `iotop` — instala só quando fore à aula que precisa deles.

---

*Documento complementar ao repositório Fortaleza Proxmox — não auditado linha a linha contra man pages; usa `man comando` quando tiveres dúvida.*
