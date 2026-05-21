# Linux — comandos de fundamentos (cheat sheet)

**Escopo:** uso em **VMs ou CTs Debian de estudo** (laboratório, DMZ, exercícios de aula).  
**Não** substitui nem contradiz o [guia Sentinela Proxmox](../🛡️ Sentinela-Proxmox - Versão 1.0.md): no **host Proxmox** seguem-se as fases do guia (firewall `proxmox-firewall`, CrowdSec, SSH com chave + 2FA, etc.). Coisas como **UFW** ou **fail2ban** no legado "bare metal" fazem sentido **dentro** de guests Debian; **evite** empilhar UFW no nó PVE em paralelo com o firewall do Proxmox sem saber o que está fazendo.

Origem conceitual: projeto anterior **Linux Foundation Lab** (Debian 13 minimal à mão). Este arquivo condensa só a parte **reutilizável** de comandos e hábitos.

---

## Pastas úteis (na VM de estudo ou no seu usuário no PVE)

Você pode organizar assim (ajuste caminhos ao seu usuário):

```bash
mkdir -p ~/lab ~/scripts ~/notes ~/gpg
```

No host Sentinela já existe `~/sentinela-lab/` (README, diário, recuperação) — você pode espelhar a mesma ideia **dentro** de cada VM.

---

## Navegação e arquivos

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
| Recursos | `btop` (moderno) ou `htop`, `free -h`, `df -h` |
| Snapshot do sistema | `fastfetch` |
| Discos / blocos | `lsblk`, `blkid` |
| Auditoria de segurança | `sudo lynis audit system` |

---

## Rede

| Tarefa | Comando |
|--------|---------|
| Interfaces | `ip a`, `ip r` |
| Conexões e portas em escuta | `ss -tuln` (substitui `netstat`) |
| Teste | `ping`, `traceroute` |
| DNS | `dig`, `host`, `resolvectl status` |
| Captura (cuidado em produção) | `tcpdump`, `nmap` (só em lab com permissão) |

---

## Hardware (visão rápida)

```bash
lscpu
lsblk
free -h
df -h
fastfetch          # resumo completo: OS, CPU, RAM, uptime
inxi -Fxz          # inventário detalhado (apt install inxi)
```

---

## SSH (cliente)

```bash
ip a                    # descobrir IP na VM
ssh usuario@IP
```

No **host** Proxmox o guia Sentinela configura **chave Ed25519 + 2FA** — não use esta seção como modelo do servidor PVE.

---

## OpenPGP / GPG (resumo)

Objetivos típicos: chaves pública/privada, assinatura, cifra, identidade.

```bash
gpg --full-generate-key
gpg --list-keys
gpg --armor --export EMAIL
gpg --sign arquivo.txt
gpg --encrypt --recipient EMAIL arquivo.txt
```

Exercício guiado no lab do irmão / GPG: ver **Fase 8** do [guia principal](../🛡️ Sentinela-Proxmox - Versão 1.0.md).

---

## Docker (quando chegar lá)

Instalação oficial em Debian: [Docker Engine — Debian](https://docs.docker.com/engine/install/debian/).

**Não** começar por Kubernetes / Swarm / Compose gigante — primeiro imagens, volumes, redes, um `Dockerfile` simples. No Sentinela, Docker aparece no **CT do ShellHub** (Fase 8); stacks grandes ficam para VMs dedicadas quando tiver RAM disponível.

```bash
docker run hello-world          # teste básico
docker ps -a                    # listar containers
docker images                   # listar imagens locais
docker logs NOME                # ver saída de um container
docker compose up -d            # subir stack (docker-compose.yml)
docker compose down             # parar e remover
docker stats                    # uso de recursos em tempo real
```

---

## UFW / fail2ban (apenas em guests — NÃO no host PVE)

```bash
# UFW — firewall simples para VMs Debian de estudo:
apt install ufw
ufw allow 22/tcp
ufw enable
ufw status verbose

# fail2ban — proteção contra força bruta em VMs expostas:
apt install fail2ban
systemctl enable --now fail2ban
fail2ban-client status sshd
```

> ⚠️ **No host PVE** use o `proxmox-firewall` (Fase 7 do guia). UFW e fail2ban são para **dentro** das VMs/CTs de estudo.

---

## Comandos úteis do dia-a-dia (VM de estudo)

```bash
# Verificar o que está rodando na porta 80:
ss -tuln | grep :80

# Ver processos que mais consomem RAM:
ps aux --sort=-%mem | head -10

# Últimas 50 linhas do kernel log com timestamps:
dmesg -T | tail -50

# Histórico de reboots:
last -x | grep -E "shutdown|reboot" | head -5

# Verificar tempo de resposta DNS:
dig @1.1.1.1 google.com | grep "Query time"
```

---

*Última revisão: 2026-05-13 — alinhado ao Sentinela Proxmox v1.0.*
