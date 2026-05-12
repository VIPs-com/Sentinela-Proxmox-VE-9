# 🛡️ Fortaleza Proxmox — Guia Definitivo v5.0

**Autor:** Renato
**Data:** Maio/2026
**Hardware:** Mini PC · 16 GB RAM
**Base:** Proxmox VE 9.x (ex.: 9.1) sobre Debian 13 “Trixie”; kernel e OpenSSH variam com `apt full-upgrade` — confirme com `pveversion`, `uname -r`, `ssh -V`.
**Objetivo:** Construir uma infraestrutura **segura, invisível, documentada e recuperável** antes de começar a estudar.

> **Status da documentação:** guia de homelab **revisado contra fontes oficiais** em 2026-05-12. Não substitui suporte enterprise nem auditoria profissional. Matriz fase × fonte × conclusão: [docs/audit-matrix.md](docs/audit-matrix.md).

> **Perdido nos estudos?** Visão geral por setores (onboarding, blocos A–G, VM, GPG): [docs/mapa-do-curso.md](docs/mapa-do-curso.md).

---

## 📌 O que mudou em relação às versões anteriores

A v4.0 já cobria SSH, 2FA, CrowdSec, Tailscale, nftables e ShellHub. A v5.0 adiciona o que faltava para um **novato** começar do zero sem se trancar fora ou ficar com sistema "torto":

| Adição na v5.0 | Por que é crítico |
|----------------|-------------------|
| **Configurar timezone + NTP** (FASE 0) | TOTP só funciona com relógio sincronizado. Erro silencioso. |
| **Trocar repositório Enterprise por No-Subscription** (FASE 0) | Sem isso, `apt update` falha com `401 Unauthorized` |
| **Configurar IP fixo** (FASE 0) | DHCP do roteador pode trocar o IP e você perde acesso |
| **Hostname + /etc/hosts coerente** (FASE 0) | Proxmox quebra se hostname não resolve |
| **Backup do `/etc/pve`** antes de cada fase | Seu seguro de vida |
| **Remover subscription nag** (opcional, FASE 0) | Qualidade de vida no painel web |
| **FASE 10: Documentação viva** | README local + diário + plano de recuperação |
| **Apêndice G:** lista do que guardar no Bitwarden | Não esquecer nenhum segredo |
| **Apêndice H:** plano de recuperação de desastre | Você vai precisar um dia |

---

## 📖 Como usar este guia

Cada fase segue sempre a mesma estrutura:

> 🎯 **OBJETIVO** — o que você vai conquistar
> 📚 **FUNDAMENTO** — por que estamos fazendo isso
> ⚙️ **COMANDOS** — passo a passo, comentados linha por linha
> ✅ **VERIFIQUE** — como ter certeza de que deu certo
> 🆘 **SE DEU ERRADO** — troubleshooting do erro mais comum

> ⚠️ **Não pule fases.** A ordem foi escolhida para você nunca perder o acesso ao servidor.

Para uma leitura “de cima” antes de mergulhar nas fases, use o [mapa do curso](docs/mapa-do-curso.md). A **ordem dos ficheiros** em `docs/` (núcleo vs complemento vs operação) está em [docs/README.md](docs/README.md).

---

## Dicas para o aluno — como usar este guia (fundamentos)

Estas dicas valem para **todas** as fases. O objectivo é reduzir ansiedade e erros por pressa.

### 1. Leia antes de copiar

- Cada bloco **COMANDOS** mistura linhas que são **comentários** (começam por `#` no shell) com linhas que são **ordens reais** para o terminal.
- Quando o guia mostra **conteúdo de ficheiro** (ex.: `interfaces`, `sshd_config`), o bloco pode ser “cole isto no editor” — não corras isso na shell como se fosse `bash`.
- Se um comando tiver `grep`, `|`, `&&` ou `$(...)`, é **composto**: lê o comentário acima para saber o que o filtro ou a condição fazem.

### 2. Duas sessões SSH (regra de ouro)

A partir do momento em que mexes em **rede** ou **SSH**, mantém **sempre** duas ligações ao servidor (duas janelas de terminal, ou uma janela + consola física / `Shell` no painel web). A primeira sessão é a “corda de segurança”; a segunda serve para testar. Se fechares a única sessão no meio de um `restart` de rede ou SSH, o stress aumenta muito.

### 3. Exemplos não são a tua rede

Endereços como `192.168.1.100`, gateway `192.168.1.1`, interface `vmbr0` / `enp1s0` são **modelos**. Substitui pelos valores **da tua** LAN e pelos nomes que o **teu** `ip addr show` mostrar. Erro típico de novato: copiar IP do guia e depois não bater com o roteador.

### 4. O que é o bloco “Tradução”

Quando aparece **Tradução** (ou glossário inline), o guia está a explicar **o significado** das linhas anteriores (opções do `sshd`, campos do `interfaces`, etc.). Nem todos os passos têm esse rótulo — muitas vezes a explicação está nos **comentários** `#` dentro do `bash`. Se não perceberes uma flag, pesquisa `man comando` no Debian ou a wiki Proxmox ligada na fase.

### 5. Legenda rápida dos rótulos das fases

| Rótulo | Função |
|--------|--------|
| **OBJETIVO** | O que vais ganhar ao terminar o passo. |
| **FUNDAMENTO** | Porque é que isto importa (segurança, rede, relógio…). |
| **COMANDOS** | Passos concretos. |
| **VERIFIQUE** | Provas de que funcionou; não avances sem isto quando a fase for crítica. |
| **SE DEU ERRADO** | O erro mais comum e como sair dele. |

### 6. Ferramentas e contexto

- **Bitwarden** (ou outro gestor): guarda segredos e códigos de recuperação **no momento** em que o guia os gera — ver Apêndice G.
- **Acesso físico** ao mini PC: trata-o como “plano B” sempre que mexeres em rede ou firewall.
- **Documentação satélite** (matriz de auditoria, mapa, cheat sheet Linux): ajudam a **orientar** e a **cruzar fontes**; não substituem executar as fases na ordem no host.

### 7. Se empatares

1. Volta ao [mapa do curso](docs/mapa-do-curso.md) e confirma em que bloco estás.  
2. Relê só o **FUNDAMENTO** e o **SE DEU ERRADO** dessa subsecção.  
3. Consulta a [matriz de auditoria](docs/audit-matrix.md) se a dúvida for “isto ainda bate com a documentação oficial?”.  
4. Apêndice H (recuperação) se perdeste acesso.

---

## Changelog da documentação

| Data | Alteração |
|------|-----------|
| 2026-05 | **v5.0** — rascunho inicial do guia (fases 0–10 e apêndices). |
| 2026-05-12 | Revisão do texto do guia contra fontes oficiais; matriz em [docs/audit-matrix.md](docs/audit-matrix.md). Secção **Dicas para o aluno** (usabilidade); relatório de auditoria pedagógica: [docs/revisao-geral-projeto.md](docs/revisao-geral-projeto.md). **Histórico detalhado** de ficheiros satélites e reorganização da pasta `docs/`: [docs/CHANGELOG-repositorio.md](docs/CHANGELOG-repositorio.md). |

<span id="glossario-completo"></span>

## 📚 Glossário completo

| Termo | O que é |
|-------|---------|
| **Host** | O Proxmox em si, o sistema "pai" rodando no Mini PC |
| **LXC** | Container Linux leve (compartilha o kernel do host) |
| **CT** | Sigla do Proxmox para container LXC |
| **VM** | Máquina virtual completa (kernel próprio, mais pesada) |
| **PAM** | Sistema de autenticação do Linux ("quem pode logar?") |
| **TOTP** | Código de 6 dígitos que muda a cada 30s (Google Authenticator, Bitwarden) |
| **Bouncer** | Componente que efetivamente bloqueia IPs (o "braço" do CrowdSec) |
| **nftables** | Firewall moderno do kernel Linux (sucessor do iptables) |
| **`proxmox-firewall`** | Serviço do Proxmox VE 9 que aplica o firewall via nftables (backend **tech preview** na [wiki](https://pve.proxmox.com/wiki/Firewall#nftables)) |
| **`pve-firewall`** | Serviço legado (iptables); ainda existe mas é substituído |
| **drop-in config** | Arquivo separado em `/etc/.../conf.d/` que sobrescreve config principal |
| **Snapshot** | Foto do estado do sistema; permite voltar no tempo |
| **Realm** | "Reino" de autenticação do Proxmox (`pam` = Linux, `pve` = interno) |
| **deb822** | Formato moderno do APT para fontes (`.sources` em vez de `.list`) |
| **subnet routing** | Tailscale anunciando uma rede inteira para os peers |
| **TUN device** | Interface virtual de rede usada por VPNs (Tailscale precisa) |
| **`pct`** | Comando CLI do Proxmox para gerenciar containers |
| **`qm`** | Comando CLI do Proxmox para gerenciar VMs |

---

## 🏗️ Diagrama da arquitetura final

```
                    INTERNET
                        │
                        ▼
            ┌───────────────────────┐
            │ Roteador da sua casa  │  ← Sem port forwarding
            └───────────┬───────────┘
                        │ Rede local (192.168.1.0/24)
                        ▼
        ┌────────────────────────────────────────┐
        │  Mini PC — Proxmox VE 9.x              │
        │  ┌──────────────────────────────────┐  │
        │  │ proxmox-firewall (nftables) DROP │  │  ← "Some" da internet
        │  │  ▲ SSH (chave Ed25519 + 2FA)     │  │
        │  │  ▲ Web GUI (senha + 2FA TOTP)    │  │
        │  │  ▲ CrowdSec bouncer (nftables)   │  │  ← Bana IPs maliciosos
        │  └──────────────────────────────────┘  │
        │                                        │
        │  ┌──────────┐    ┌──────────────────┐  │
        │  │ CT 100   │    │ CT 200           │  │
        │  │ Tailscale│    │ lab-irmao        │  │
        │  │ + TUN    │    │ ShellHub Agent   │  │
        │  └──────────┘    └──────────────────┘  │
        └────────────────────────────────────────┘
                ▲                  ▲
                │                  │
        ┌───────┴───────┐  ┌──────┴──────────┐
        │ Tailscale     │  │ ShellHub Cloud  │
        │ (rede privada)│  │ (túnel reverso) │
        └───────┬───────┘  └────────┬────────┘
                │                   │
                ▼                   ▼
            Você (PC,           Seu irmão
            celular,            (acesso só à
            qualquer lugar)     VM dele)
```

---

## ⚠️ Antes de Começar — Leia Tudo

### Sobre o root no Proxmox

No Debian/Ubuntu puro, você costuma deixar o `root` sem senha e usar só sudo. **No Proxmox isso NÃO funciona.** O Proxmox usa o root internamente para vários serviços (cluster, `pveproxy`, `pvedaemon`). Travar a conta root começa a quebrar coisas silenciosamente.

A estratégia correta é **isolar** o root, não eliminá-lo:

| Onde | O que fazer |
|------|-------------|
| Senha root | Manter forte, guardada offline (Bitwarden) |
| SSH (porta 22) | Bloquear: `PermitRootLogin no` |
| Painel web (8006) | Criar `renato@pam` com Administrator + 2FA, nunca usar `root@pam` no dia-a-dia |
| Dia-a-dia | `ssh renato@ip` → `sudo -i` quando precisar |
| Emergência | Console físico (monitor + teclado no Mini PC) |

### Regras de ouro

1. 🔒 **Nunca feche todas as sessões SSH antes de testar a nova.** Mantenha sempre 2 janelas abertas durante mudanças críticas.
2. 📸 **Snapshot antes de cada fase grande.** No painel: `pve → Disks → ZFS → Snapshot`.
3. 📱 **Celular do lado** durante a Fase 3 (2FA). Sem ele, você não loga.
4. 🖥️ **Acesso físico ao Mini PC** funciona como "plano B" se tudo travar.
5. 📝 **Documente cada mudança** num arquivo `~/lab-diario.md` (Fase 10).

### Mini PC, RAM e o que fica ligado 24/7

O **Proxmox (host)** pode ficar **sempre ligado** — agendamentos de backup, rede e endurecimento do guia **não exigem** que todas as VMs/CTs do teu laboratório (oficina, DMZ, etc.) estejam **acesas ao mesmo tempo**. Em hosts com **pouca RAM** (ex.: 16 GB), o uso típico é: **infra leve no host** (e eventualmente um CT como o Tailscale) **+ só as VMs que precisas naquele momento**; desliga ou suspende o resto quando não estiveres a estudar esse módulo. A **segurança do host** (SSH, 2FA, firewall, CrowdSec) protege a plataforma mesmo com poucos guests ligados — não é necessário “encher” o servidor para o guia fazer sentido.

### Pré-requisitos

- [ ] Proxmox VE 9.x instalado (`pveversion` retorna `pve-manager/9.x.x`)
- [ ] Você consegue acessar `https://IP-DO-PROXMOX:8006` no navegador
- [ ] Você consegue fazer `ssh root@IP-DO-PROXMOX` do seu PC
- [ ] Você tem acesso físico ao Mini PC (monitor + teclado) em caso de emergência
- [ ] Bitwarden (ou outro gerenciador de senhas) instalado e funcionando
- [ ] App TOTP no celular (Bitwarden, Aegis, Google Authenticator, 1Password)
- [ ] Cabo de rede conectado (não tente isso por Wi-Fi)

**Substitua nos comandos:** todo `192.168.1.100` pelo IP real do seu Proxmox.

### O que vai pro Bitwarden ANTES de começar

Crie uma pasta "Fortaleza Proxmox" e prepare entradas para:

1. **Senha do root do Proxmox** (definida na instalação)
2. **Senha do usuário `renato`** (vamos criar)
3. **Passphrase da chave SSH** (vamos criar)
4. **QR code/chave secreta do 2FA SSH** (vamos gerar)
5. **Códigos de recuperação 2FA SSH** (5 códigos)
6. **QR code/chave secreta do 2FA painel web** (vamos gerar)
7. **Códigos de recuperação 2FA painel** (vamos gerar)
8. **Conta Tailscale** (Google/GitHub OAuth)
9. **Conta ShellHub Cloud** (email + senha)
10. **Senha do root dos containers** (CT 100, CT 200)
11. **Senha do usuário `irmao`** (no CT 200)

> Apêndice G traz a lista completa para conferir no final.

### (Opcional) ProxMenux — menu interactivo na shell

[ProxMenux](https://proxmenux.com/) é uma ferramenta **de terceiros** (open source, projecto comunitário) que oferece um **menu interactivo** na linha de comandos para tarefas comuns em Proxmox VE (recursos, rede, storage, VM/LXC, manutenção). Documentação introdutória: [Introduction](https://proxmenux.com/docs/introduction).

> **Segurança:** não é produto da Proxmox GmbH. O próprio ProxMenux avisa para **verificar a fonte** antes de executar scripts da Internet — o mesmo princípio do guia sobre `curl|bash`. Revê o [repositório GitHub](https://github.com/MacRimi/proxmenux) e a [instalação](https://proxmenux.com/docs/installation) **antes** de instalar em produção. Usar ProxMenux **não substitui** perceberes o que as Fases 0–7 fazem (rede, repos, SSH, firewall); serve sobretudo para **ganhar tempo** no dia-a-dia depois de dominares o básico.

---

# 🟢 FASE 0 — Preparação do Sistema (FUNDAÇÃO)

🎯 **OBJETIVO:** Deixar o Proxmox saudável **antes** de aplicar qualquer hardening. Atualizar, fixar IP, ajustar relógio, corrigir repositórios.

> **BIOS / firmware (instalação por ISO):** habilite **Intel VT-x** (virtualização). **Intel VT-d** se um dia precisar de *passthrough* de dispositivos. Use **UEFI** conforme a placa e o instalador. **Secure Boot** / *Fast Boot*: depende do firmware e da versão do instalador PVE — veja a documentação da motherboard e a [wiki Proxmox](https://pve.proxmox.com/wiki/Main_Page) para o teu caso; o legado “Linux Foundation Lab” desactivava Secure Boot por simplicidade no Debian minimal, **não** é regra universal no PVE.

> ⚠️ **Esta fase é a mais importante de todas.** Pular ela causa bugs que aparecem só depois (TOTP falhando, `apt update` quebrando, IP mudando). Faça com calma.

### Login inicial

Use SSH normalmente (ainda como root, vamos trocar isso na Fase 1):

```bash
ssh root@192.168.1.100
```

> Não se trancou em nenhum lugar ainda. Tranquilo.

---

## 0.1 Configurar Timezone e NTP

📚 **FUNDAMENTO:** O TOTP (2FA) usa o **relógio do servidor** sincronizado com o **relógio do seu celular**. Se houver diferença de mais de 30s, os códigos não batem e você não consegue logar. Por isso, **antes** de configurar 2FA, garantimos que o relógio está certo via NTP (Network Time Protocol).

### Definir timezone

```bash
# Lista timezones disponíveis
timedatectl list-timezones | grep -i sao_paulo
# Saída: America/Sao_Paulo

# Define o timezone (ajuste se você não for de São Paulo)
timedatectl set-timezone America/Sao_Paulo
```

### Verificar sincronização NTP

```bash
timedatectl status
```

**Saída esperada:**
```
               Local time: Tue 2026-05-12 14:30:15 -03
           Universal time: Tue 2026-05-12 17:30:15 UTC
                 RTC time: Tue 2026-05-12 17:30:15
                Time zone: America/Sao_Paulo (-03, -0300)
System clock synchronized: yes
              NTP service: active
          RTC in local TZ: no
```

> ⚠️ **`System clock synchronized: yes`** e **`NTP service: active`** são obrigatórios. Se aparecer `no`, force a sincronização:

```bash
# Garantir que o systemd-timesyncd está rodando
systemctl enable --now systemd-timesyncd
systemctl status systemd-timesyncd --no-pager
```

### ✅ Verifique

```bash
date
# Saída esperada: data e hora REAL (compare com seu celular)
```

---

## 0.2 Configurar IP Fixo

📚 **FUNDAMENTO:** Por padrão, o Proxmox usa o IP que recebeu durante a instalação. Se ele estiver via DHCP, **pode mudar** quando o roteador reiniciar — e você perde o acesso porque seu firewall (Fase 7) só permite IPs específicos.

Existem duas formas: **(a)** reservar IP no roteador (DHCP reservation) ou **(b)** configurar IP estático no Proxmox.

A forma mais segura é **fazer as duas**.

### Opção A — Reserva no roteador (recomendado fazer ANTES)

No painel do roteador, encontre a seção `DHCP Reservation` (ou `Static Leases`). Adicione:
- MAC address do Mini PC: descubra com `ip addr show` no Proxmox (campo `link/ether`)
- IP desejado: `192.168.1.100`
- Hostname: `pve`

### Opção B — IP estático no Proxmox

⚠️ **Cuidado nesta etapa.** Errar aqui pode te deixar sem rede. Tenha acesso físico ao Mini PC.

```bash
# Ver interfaces atuais
ip addr show

# Identifique o nome da interface (geralmente enp1s0 ou eno1)
# E a bridge do Proxmox (vmbr0)
```

Edite o arquivo de rede:

```bash
nano /etc/network/interfaces
```

Você verá algo como:
```
auto vmbr0
iface vmbr0 inet dhcp
    bridge-ports enp1s0
    bridge-stp off
    bridge-fd 0
```

Mude `dhcp` para `static` e adicione IP/gateway/DNS:

```
auto vmbr0
iface vmbr0 inet static
    address 192.168.1.100/24
    gateway 192.168.1.1
    bridge-ports enp1s0
    bridge-stp off
    bridge-fd 0
    dns-nameservers 1.1.1.1 8.8.8.8
```

> **Tradução:**
> - `address 192.168.1.100/24` — IP do Proxmox / máscara de 24 bits (255.255.255.0)
> - `gateway 192.168.1.1` — IP do seu roteador
> - `dns-nameservers 1.1.1.1 8.8.8.8` — DNS público (Cloudflare + Google)

Salve (`Ctrl+O`, Enter, `Ctrl+X`) e aplique:

```bash
# ifreload vem do pacote ifupdown2 (normalmente já instalado no PVE novo; em upgrades antigos pode faltar)
command -v ifreload >/dev/null || apt install -y ifupdown2

# Aplica a config nova sem reiniciar
ifreload -a
# Saída típica inclui algo como: applying /etc/network/interfaces ...
```

> Se `ifreload` falhar com «command not found» mesmo após instalar `ifupdown2`, usa o caminho mais conservador: `systemctl restart networking` (pode cortar SSH momentaneamente — tenha console físico ou segunda sessão).

```bash
# OU se preferir mais conservador (reinicia stack de rede inteira):
# systemctl restart networking
```

### ✅ Verifique

```bash
ip -4 addr show vmbr0
# Saída esperada: inet 192.168.1.100/24 ...

ping -c 3 1.1.1.1
# Saída esperada: 3 pacotes recebidos

ping -c 3 google.com
# Saída esperada: 3 pacotes recebidos (testa DNS também)
```

### 🆘 Se deu errado

**Erro:** Perdeu conexão SSH ao reiniciar rede
**Solução:** Console físico do Mini PC, logue como root, edite o arquivo de volta para `dhcp` ou corrija a sintaxe.

---

## 0.3 Configurar Hostname e `/etc/hosts`

📚 **FUNDAMENTO:** O Proxmox tem uma quirk importante: o hostname **precisa resolver** para o IP do nó no `/etc/hosts`. Se isso quebra, vários serviços do Proxmox (cluster, pveproxy) começam a falhar de formas estranhas.

### Verificar configuração atual

```bash
hostname              # Geralmente: pve
hostname -i           # Deve retornar o IP correto, NÃO 127.0.1.1
cat /etc/hosts        # Deve ter linha "192.168.1.100 pve.local pve"
```

### Corrigir se necessário

Se `hostname -i` retornou `127.0.1.1` ou erro:

```bash
nano /etc/hosts
```

Garanta que tenha (substitua pelo seu IP):
```
127.0.0.1 localhost
192.168.1.100 pve.local pve

# Linhas IPv6 padrão (mantenha)
::1 localhost ip6-localhost ip6-loopback
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
```

### ✅ Verifique

```bash
hostname -i
# Saída esperada: 192.168.1.100 (NÃO 127.0.1.1)

ping -c 1 pve
# Saída esperada: ping para 192.168.1.100
```

---

## 0.4 Corrigir Repositórios (Enterprise → No-Subscription)

📚 **FUNDAMENTO:** Por padrão, o Proxmox vem configurado para usar o repositório **Enterprise**, que só funciona com subscription paga. Sem subscription, todo `apt update` falha com erro `401 Unauthorized`. Para uso doméstico, trocamos para o repositório **No-Subscription** (gratuito, mesmas atualizações com pequeno atraso).

> ⚠️ **Proxmox VE 9 (Debian 13 Trixie) usa o formato moderno `deb822` (`.sources`).** Não confunda com o formato antigo `.list` — o APT em Trixie avisa sobre formato legacy; veja [Repository formats](https://pve.proxmox.com/wiki/Package_Repositories#sysadmin_apt_repo_formats) na wiki.

### Desabilitar o repositório Enterprise

O método **documentado na wiki** é desactivar a entrada **sem** partir o formato deb822: `Enabled: no` no bloco correcto, ou desligar a entrada no painel.

**Recomendado (menos erro que `sed` em ficheiro `.sources`):**

1. No painel web: **nó (pve) → Updates → Repositories** — seleccione `pve-enterprise` → **Disable** (equivalente a `Enabled: no` no deb822).
2. **Ou** no host: `nano /etc/apt/sources.list.d/pve-enterprise.sources` e acrescente `Enabled: no` ao bloco do repositório enterprise (mantém o ficheiro legível para voltar a `yes` com subscription).

> **Evite** `sed -i 's/^/# /'` em `.sources` deb822: comentar **todas** as linhas (incluindo cabeçalhos de secção) pode deixar o APT com ficheiro malformado. Se **só** tiveres shell, edita manualmente ou usa o painel.

Faça o equivalente para o repositório **Ceph** (não usamos em lab pequeno): no mesmo ecrã **Repositories**, desactive `ceph-enterprise` / entradas Ceph, **ou** `Enabled: no` no ficheiro `ceph.sources` correspondente — **não** uses comentário em massa com `sed` no deb822.

### Adicionar o repositório No-Subscription

Crie o arquivo no formato `deb822` (a wiki sugere o nome [`/etc/apt/sources.list.d/proxmox.sources`](https://pve.proxmox.com/wiki/Package_Repositories); qualquer nome `.sources` em `sources.list.d/` é válido):

```bash
nano /etc/apt/sources.list.d/pve-no-subscription.sources
```

Cole exatamente:

```
Types: deb
URIs: http://download.proxmox.com/debian/pve
Suites: trixie
Components: pve-no-subscription
Signed-By: /usr/share/keyrings/proxmox-archive-keyring.gpg
```

Salve e saia.

### ✅ Verifique

```bash
apt update
```

**Saída esperada:** lista de repos lidos, terminando com `Reading package lists... Done`. **Sem** erros `401 Unauthorized`.

```bash
apt list --upgradable 2>/dev/null | head
# Saída esperada: lista de pacotes a atualizar (ou vazia se já tá tudo)
```

### 🆘 Se deu errado

**Erro:** `The repository 'https://enterprise.proxmox.com/debian/pve trixie InRelease' is not signed`
**Solução:** O repositório enterprise ainda está activo. No painel **Updates → Repositories**, desactive `pve-enterprise`, **ou** em `pve-enterprise.sources` use `Enabled: no` no bloco correcto (evite `sed` que comenta o ficheiro inteiro em deb822).

**Erro:** Chave GPG do Proxmox faltando
**Solução:**
```bash
wget https://enterprise.proxmox.com/debian/proxmox-archive-keyring-trixie.gpg \
  -O /usr/share/keyrings/proxmox-archive-keyring.gpg
```

---

## 0.5 (Opcional) Remover o "Subscription Nag" do Painel Web

📚 **FUNDAMENTO:** Quando você loga no painel web sem subscription, aparece um popup chato "No valid subscription". Isso não afeta segurança nem funcionalidade, é só visual. Você pode:
- **(a)** ignorar e clicar OK toda vez
- **(b)** comprar uma subscription (R$ ~600/ano para Community)
- **(c)** aplicar um patch que remove o popup

Se preferir (c), use o script da comunidade **community-scripts** (amplamente usado em homelab; **não** é da Proxmox GmbH — mesmo tipo de risco de *supply chain* que `curl|sh` ou ProxMenux de terceiros).

> **Cadeia de confiança:** `wget|bash` executa código remoto com os privilégios que o script pedir. Abre o script no GitHub **antes** (compare o URL `raw` com o repositório oficial), lê o que ele altera em `/etc` e no APT, usa só o commit/branch em que confias, e testa primeiro em máquina descartável se possível. Não há substituto «oficial Proxmox» para este patch — ou ignoras o popup ou aceitas o risco com consciência.

```bash
# Versão "tteck" / "community-scripts" — auditar em https://github.com/community-scripts/ProxmoxVE/blob/main/misc/post-pve-install.sh
bash -c "$(wget -qLO - https://github.com/community-scripts/ProxmoxVE/raw/main/misc/post-pve-install.sh)"
```

> Esse script é interativo. Ele pergunta:
> - **Disable the Enterprise Repository?** → **Yes** (já fizemos manualmente, mas confirma)
> - **Enable the No-Subscription Repository?** → **Yes**
> - **Correct ceph.sources?** → **Yes**
> - **Add or correct the test Repository?** → **No**
> - **Disable the subscription nag?** → **Yes**
> - **Update Proxmox VE Now?** → **Yes**

Depois, faça **hard reload** do navegador (`Ctrl+Shift+R`) para limpar o cache do popup.

### ✅ Verifique

Saia do painel web e entre de novo. O popup não deve mais aparecer.

---

## 0.6 Atualizar o Sistema

```bash
apt update && apt full-upgrade -y
apt install sudo curl wget nano gnupg ca-certificates git -y
```

> **O que cada pacote faz:**
> - `sudo` — permite usuário comum executar comandos como root
> - `curl` / `wget` — baixam arquivos da internet (scripts de instalação)
> - `nano` — editor de texto simples
> - `gnupg` / `ca-certificates` — necessários para repositórios externos seguros
> - `git` — vai ser útil para clonar configs/scripts depois

Se kernel foi atualizado, reinicie:

```bash
# Modo interactivo: pergunta o que reiniciar (mais seguro para novatos que a Fase 9.1b ainda não leu)
needrestart -k -r i

# OU reboot total se preferir
reboot
```

> O modo `-r a` (reinício **automático** de serviços) existe mas **não** é «só uma pergunta» — lê a secção **9.1b** antes de usar ou de editar `/etc/needrestart/needrestart.conf`.

### ✅ Verifique

```bash
pveversion
# Saída esperada: pve-manager/9.x.x/xxxxx (running kernel: conforme uname)

uname -r
# Saída esperada: kernel PVE atual (ex.: 6.x.x-pve — varia com updates)

cat /etc/debian_version
# Saída esperada: 13.x (Trixie) ou superior
```

---

## 0.7 Backup Inicial do `/etc/pve`

📚 **FUNDAMENTO:** O diretório `/etc/pve` contém **toda a configuração** do Proxmox (firewall, usuários, VMs, containers, certificates). Se algo corromper, você perdeu tudo. Antes de cada fase grande, faça um tar dessa pasta.

```bash
# Cria pasta de backups
mkdir -p /root/backups

# Backup inicial
tar czf /root/backups/etc-pve-fase0-$(date +%F).tar.gz /etc/pve/

# Verifica
ls -lh /root/backups/
```

> Recomendo copiar esse arquivo para fora do servidor (seu PC, OneDrive, etc.) depois de cada fase importante.

---

## 0.8 Snapshot ZFS Inicial

Se você instalou Proxmox com ZFS (padrão recomendado):

> **Dataset ZFS:** o caminho `rpool/ROOT/pve-1` usado nos comandos deste guia é um **exemplo** comum após instalação pela ISO. O seu pode ser outro — confirme com `zfs list` (dataset montado em `/`) e substitua em **todos** os `zfs snapshot` das fases seguintes.

No painel web:
1. `pve → Disks → ZFS`
2. Selecione o pool root (`rpool`)
3. **Snapshot** → Nome: `snap-fase0-instalacao-limpa`

Pelo terminal (alternativa):

```bash
# Exemplo — ajuste o dataset ao output de: zfs list
zfs snapshot rpool/ROOT/pve-1@snap-fase0-instalacao-limpa
zfs list -t snapshot
```

> Se você usa LVM-Thin (instalação antiga), snapshots de host são limitados. Use o backup `tar` do `/etc/pve` como alternativa principal.

---

## ✅ Checklist da Fase 0

- [ ] Timezone configurado para sua região
- [ ] `timedatectl status` mostra `NTP service: active` e `synchronized: yes`
- [ ] IP fixo configurado (reservado no roteador OU estático no PVE)
- [ ] `hostname -i` retorna o IP correto (não `127.0.1.1`)
- [ ] Repositório Enterprise desabilitado
- [ ] Repositório No-Subscription habilitado
- [ ] `apt update` funciona sem erros
- [ ] Sistema atualizado (`pveversion` mostra última versão)
- [ ] Backup inicial do `/etc/pve` em `/root/backups/`
- [ ] Snapshot ZFS `snap-fase0-instalacao-limpa` criado

---

## Dataset ZFS nos comandos seguintes

Sempre que aparecer `rpool/ROOT/pve-1` num `zfs snapshot`, use o **mesmo** dataset que você confirmou em **0.8** (não copie cegamente se o seu `zfs list` mostrar outro nome).

---

# 🟢 FASE 1 — Identidade e Privilégios

🎯 **OBJETIVO:** Criar `renato` com poder de virar root quando precisar (via `sudo`).

📚 **FUNDAMENTO:** O `root` é o "Deus" do Linux — pode destruir o sistema com um comando errado. Trabalhar com usuário comum + sudo cria uma barreira intencional: quando você digita `sudo`, é como passar a chave do cofre. Você pensa duas vezes antes de fazer algo destrutivo.

### 📸 Snapshot antes de começar

```bash
zfs snapshot rpool/ROOT/pve-1@snap-pre-fase1
```

### ⚙️ Comandos

Logado como root:

```bash
adduser renato
```

> Vai pedir senha. **Forte, e guarde no Bitwarden.** Perguntas extras (Full Name, etc.) podem ficar em branco — só apertar Enter.

```bash
usermod -aG sudo renato
```

> **Tradução:** `usermod` modifica usuário, `-a` append (adiciona, não substitui), `-G sudo` ao grupo sudo, `renato` o alvo.

### ✅ Verifique

**Em um SEGUNDO terminal** (não feche o primeiro!):

```bash
ssh renato@192.168.1.100      # Senha do renato

sudo whoami                    # Pede a senha do renato de novo
# Saída esperada: root
```

✅ Se apareceu `root`, sudo OK. Pode prosseguir.

### 📝 Documente no diário

```bash
# Como renato
mkdir -p ~/fortaleza-lab
echo "## $(date +%F %H:%M) - Fase 1 concluída" >> ~/fortaleza-lab/diario.md
echo "- Criado usuário renato com sudo" >> ~/fortaleza-lab/diario.md
```

### 🆘 Se deu errado

**Erro:** `renato is not in the sudoers file`
**Solução:** Você precisa estar **logado como root** (não como renato com sudo) para executar `usermod`:
```bash
# Pelo terminal do root original:
usermod -aG sudo renato
```
Saia (`exit`) e entre de novo. Grupos só são lidos no login.

---

# 🟢 FASE 2 — Chaves SSH (Adeus Senhas)

🎯 **OBJETIVO:** Substituir senha por chave Ed25519. Só entra quem tem o arquivo da chave privada.

📚 **FUNDAMENTO:** Uma chave Ed25519 tem segurança matemática equivalente a milhares de anos de computação para quebrar. É o padrão atual usado por GitHub, AWS, etc.

> ⚠️ **OpenSSH 10 no Debian 13 REMOVEU suporte a DSA** completamente. Use Ed25519.

### 📸 Snapshot

```bash
zfs snapshot rpool/ROOT/pve-1@snap-pre-fase2
```

### 2.1 Gerar a chave (no SEU PC pessoal)

⚠️ **Esta etapa é no seu computador, não no Proxmox.**

```bash
ssh-keygen -t ed25519 -C "renato-mini-pc" -f "$HOME/.ssh/chave_fortaleza"
```

> **Tradução:**
> - `-t ed25519` — tipo de chave (moderno e seguro)
> - `-C "renato-mini-pc"` — comentário descritivo (fica no final da chave pública)
> - `-f "$HOME/.ssh/chave_fortaleza"` — onde salvar (evita sobrescrever sua chave padrão)

```
Enter passphrase (empty for no passphrase):
```

> 🔐 **Recomendação forte: coloque uma passphrase.** Se alguém roubar o arquivo da chave, ainda precisa dessa senha. **Guarde a passphrase no Bitwarden.**

**Resultado:** dois arquivos criados em `~/.ssh/`:
- `chave_fortaleza` (privada — **NUNCA compartilhe, nunca faça upload**)
- `chave_fortaleza.pub` (pública — pode ser distribuída)

### 2.2 Enviar a chave pública para o Proxmox

```bash
ssh-copy-id -i "$HOME/.ssh/chave_fortaleza.pub" renato@192.168.1.100
```

> Pede a senha do renato uma última vez. Depois disso, a chave está registrada em `/home/renato/.ssh/authorized_keys` no servidor.

### 2.3 Testar o acesso sem senha

```bash
ssh -i "$HOME/.ssh/chave_fortaleza" renato@192.168.1.100
```

> Se entrou direto (pedindo só a passphrase da chave que VOCÊ definiu localmente), sucesso! ✅

### 2.4 (Opcional mas recomendado) Configurar `~/.ssh/config` no seu PC

Cria atalhos para não precisar digitar `-i` e IP todas as vezes:

No seu PC pessoal:

```bash
nano ~/.ssh/config
```

Cole:

```
Host fortaleza
    HostName 192.168.1.100
    User renato
    IdentityFile ~/.ssh/chave_fortaleza
    IdentitiesOnly yes
```

Salve. Agora você acessa só com:

```bash
ssh fortaleza
```

### 2.5 Hardening do SSH via drop-in config

📚 **FUNDAMENTO:** No Debian 13, a melhor prática é criar arquivos em `/etc/ssh/sshd_config.d/` em vez de editar o `sshd_config` principal. Por quê?
- O `sshd_config` principal pode ser sobrescrito em atualizações
- Configs em `sshd_config.d/` têm prioridade e sobrevivem
- Mais fácil de versionar e reverter mudanças

⚠️ **Mantenha 2 sessões SSH abertas durante esta etapa.**

```bash
sudo nano /etc/ssh/sshd_config.d/99-hardening.conf
```

Cole exatamente:

```
# ===========================================
# Hardening SSH - Fortaleza Proxmox
# ===========================================

# Autenticação
PasswordAuthentication no
PubkeyAuthentication yes
PermitRootLogin no
PermitEmptyPasswords no

# Limites e timeouts
MaxAuthTries 3
LoginGraceTime 30
ClientAliveInterval 300
ClientAliveCountMax 2

# Reduzir superfície de ataque
X11Forwarding no
AllowAgentForwarding no
AllowTcpForwarding no

# PAM (necessário pro 2FA da Fase 3)
UsePAM yes
```

> **Tradução de cada linha:**
> - `PasswordAuthentication no` — proíbe login por senha
> - `PubkeyAuthentication yes` — permite login por chave pública
> - `PermitRootLogin no` — bloqueia root via SSH completamente
> - `PermitEmptyPasswords no` — defensive (nunca permite senha vazia)
> - `MaxAuthTries 3` — desconecta após 3 tentativas falhas
> - `LoginGraceTime 30` — só 30s para completar login
> - `ClientAliveInterval 300` — checa se cliente está vivo a cada 5min
> - `ClientAliveCountMax 2` — desconecta após 2 checks sem resposta
> - `X11Forwarding no` — desabilita encaminhamento gráfico
> - `AllowAgentForwarding no` — proíbe forward do ssh-agent
> - `AllowTcpForwarding no` — proíbe túneis TCP locais `ssh -L` / `-D` / `-R` **neste host** (**endurecimento forte**). Se no futuro precisares de port forwarding SSH para debug, o sintoma típico é falha **silenciosa** ou recusa sem mensagem clara — aí comenta temporariamente ou muda para `yes` **só** no drop-in. **Não** afecta o ShellHub no CT do irmão (túnel reverso do *agent* para a cloud ShellHub); afecta **só** o que passa pelo `sshd` do host PVE.
> - `UsePAM yes` — habilita PAM (vamos usar pro 2FA)

Salve (`Ctrl+O`, Enter) e saia (`Ctrl+X`).

### Validar a sintaxe ANTES de reiniciar

```bash
sudo sshd -t
```

> Não deve retornar nada (silêncio = OK). Se retornar erro, **corrija antes** de reiniciar.

```bash
sudo systemctl restart ssh
```

> ⚠️ **No Debian 13 o serviço chama-se `ssh`, não `sshd`.** `systemctl restart sshd` dá erro.

### ✅ Verifique

**Em uma TERCEIRA sessão**:

```bash
ssh fortaleza                      # Deve entrar direto
ssh root@192.168.1.100             # Deve dar: Permission denied (publickey)
```

Verifique configurações ativas:

```bash
sudo sshd -T | grep -E 'passwordauthentication|permitrootlogin|pubkeyauthentication|maxauthtries'
# Saída esperada:
# passwordauthentication no
# pubkeyauthentication yes
# permitrootlogin no
# maxauthtries 3
```

### 🆘 Se deu errado

**Erro:** `Permission denied (publickey)` para renato
**Causa:** Chave não foi instalada corretamente.
**Solução:** Pelo console do Proxmox (físico ou `pve → Shell`):
```bash
cat /home/renato/.ssh/authorized_keys
# Verifique se sua chave pública aparece

ls -la /home/renato/.ssh/
# Permissões devem ser: 700 para .ssh, 600 para authorized_keys
```

**Erro:** Fechou tudo e não consegue mais entrar
**Solução:** Console físico ou `pve → Shell` no painel web. Logue como root, edite o arquivo `/etc/ssh/sshd_config.d/99-hardening.conf`, remova as restrições, `systemctl restart ssh`.

### 📝 Documente

```bash
echo "## $(date +%F %H:%M) - Fase 2 concluída" >> ~/fortaleza-lab/diario.md
echo "- SSH só com chave Ed25519, drop-in em sshd_config.d/" >> ~/fortaleza-lab/diario.md
```

---

# 🟢 FASE 3 — 2FA no SSH (TOTP)

🎯 **OBJETIVO:** Mesmo que sua chave privada seja roubada, sem o código do app autenticador o atacante não entra.

📚 **FUNDAMENTO:** A chave SSH é "algo que você tem" (arquivo). O TOTP é "algo que muda a cada 30s" (gerado pelo celular). Combinação praticamente inquebrável.

> ⚠️ **A partir daqui, perder o celular = perder o acesso.** Guarde os códigos de recuperação no Bitwarden!

> ⚠️ Esta fase só funciona porque você sincronizou o relógio na Fase 0. Sem NTP, o TOTP falha silenciosamente.

### 📸 Snapshot

```bash
sudo zfs snapshot rpool/ROOT/pve-1@snap-pre-fase3
```

### 3.1 Instalar o módulo PAM

```bash
sudo apt install libpam-google-authenticator -y
```

> "Google Authenticator" aqui é só o nome do projeto. Você pode usar qualquer app TOTP (Bitwarden, Aegis, etc.).

### 3.2 Configurar o 2FA para o renato

⚠️ **Logado como `renato`** (não como root, não com sudo):

```bash
google-authenticator
```

Responda:

| Pergunta | Resposta | Por quê |
|----------|----------|---------|
| Time-based tokens? | **y** | Códigos que mudam por tempo (padrão TOTP) |
| Update the file? | **y** | Salva a configuração |
| Disallow multiple uses? | **y** | Cada código só serve uma vez |
| Increase time skew? | **n** | Só ative se seu celular tem relógio errado |
| Enable rate-limiting? | **y** | Limita tentativas (anti-bruteforce) |

**Vai aparecer:**
- Um **QR Code** gigante
- Uma **chave secreta** (`Your new secret key is: XXXXX`)
- Cinco **emergency scratch codes** (recuperação)

> 🔐 **AGORA, sem fechar o terminal:**
> 1. Escaneie o QR Code com seu app de TOTP no celular
> 2. **Salve a chave secreta no Bitwarden** ("2FA SSH renato@pve - chave secreta")
> 3. **Salve TODOS os 5 códigos de recuperação no Bitwarden** ("2FA SSH renato@pve - recovery codes")
> 4. Confirme no app que o código de 6 dígitos está aparecendo

### 3.3 Configurar o PAM

```bash
sudo nano /etc/pam.d/sshd
```

Vá ao **final do arquivo** e adicione:

```
# 2FA TOTP via Google Authenticator
auth required pam_google_authenticator.so nullok
```

> **Tradução:**
> - `auth required` — etapa obrigatória de autenticação
> - `pam_google_authenticator.so` — módulo TOTP
> - `nullok` — permite logar sem 2FA configurado (temporário! removemos depois)

Salve e saia.

### 3.4 Exigir chave + 2FA via drop-in config

Edite o arquivo de hardening que criamos antes:

```bash
sudo nano /etc/ssh/sshd_config.d/99-hardening.conf
```

Adicione no final:

```
# 2FA TOTP - requer chave + código
KbdInteractiveAuthentication yes
AuthenticationMethods publickey,keyboard-interactive
```

> ⚠️ **CRÍTICO no Debian 13:** Use `KbdInteractiveAuthentication`. A diretiva antiga `ChallengeResponseAuthentication` foi **REMOVIDA** no OpenSSH 10 — vai dar erro se você usar.

> **PARA AQUI — não apliques a nova config do `sshd` até confirmares o TOTP (evita ficar trancado fora)**  
> Com `AuthenticationMethods publickey,keyboard-interactive` activo, um `sshd` mal alinhado com o PAM/TOTP pode **rejeitar** o login mesmo com chave correcta. **Checklist obrigatório:**
> 1. Concluíste o §3.2 (`google-authenticator`) e o código de 6 dígitos **já aparece** no telemóvel?
> 2. O §3.3 está gravado em `/etc/pam.d/sshd` com `nullok` (ainda) na linha do `pam_google_authenticator`?
> 3. Mantém **esta** sessão SSH aberta e prepara **outra** janela de terminal (mesmo PC ou outro na LAN).

Valide a sintaxe e **aplica** a configuração (preferir `reload` para manter esta sessão; se falhar, `restart` sem fechar esta janela):

```bash
sudo sshd -t                   # Não deve retornar nada
sudo systemctl reload ssh || sudo systemctl restart ssh
```

> 4. **Na nova janela:** `ssh fortaleza` → deves ver `Verification code:` depois da autenticação por chave. Se **não** pedir código, o código falhar sempre, ou a ligação cair, **não** avances para o §3.5 nem removas o `nullok` — reverifica `/etc/pam.d/sshd`, o drop-in e `sudo sshd -T | grep -iE 'authenticationmethods|kbdinteractiveauthentication'`.

### ✅ Verifique

```bash
ssh fortaleza
```

Deve aparecer:
```
Authenticated using "publickey".
(renato@192.168.1.100) Verification code:
```

Digite o código do app. Se entrou, ✅ 2FA ativo!

### 3.5 Remover o `nullok` (passo CRÍTICO de segurança)

⚠️ **Não pule este passo.** Sem ele, qualquer outro usuário (futuro) pode entrar sem 2FA.

Confirmado que funciona? Remova o `nullok`:

```bash
sudo nano /etc/pam.d/sshd
```

Mude:
```
auth required pam_google_authenticator.so nullok
```
para:
```
auth required pam_google_authenticator.so
```

```bash
sudo systemctl restart ssh
```

### 🆘 Se deu errado

**Erro:** Login não pede código TOTP, entra só com chave
**Causa:** `AuthenticationMethods` não foi aplicado.
**Solução:**
```bash
sudo sshd -T | grep authenticationmethods
# Deve mostrar: authenticationmethods publickey,keyboard-interactive
```

**Erro:** `Bad configuration option: ChallengeResponseAuthentication`
**Causa:** Você usou a diretiva antiga (removida no OpenSSH 10).
**Solução:** Remova essa diretiva do config. Use só `KbdInteractiveAuthentication yes`.

**Erro:** Código TOTP é rejeitado mesmo correto
**Causa:** Relógio dessincronizado (Fase 0 não foi feita direito).
**Solução:**
```bash
sudo timedatectl set-ntp true
sudo systemctl restart systemd-timesyncd
timedatectl status              # Confirme synchronized: yes
```

**Erro:** Perdi o celular
**Solução:** Use um dos 5 códigos de recuperação salvos no Bitwarden.

### 📝 Documente

```bash
echo "## $(date +%F %H:%M) - Fase 3 concluída" >> ~/fortaleza-lab/diario.md
echo "- 2FA TOTP ativo no SSH, nullok removido" >> ~/fortaleza-lab/diario.md
```

---

# 🟢 FASE 4 — CrowdSec (Vigilante Inteligente)

🎯 **OBJETIVO:** Detectar ataques e banir IPs maliciosos automaticamente, usando inteligência coletiva global.

📚 **FUNDAMENTO:** O CrowdSec compartilha dados entre milhares de servidores. Se um IP malicioso ataca outro servidor no mundo, ele chega banido no seu Mini PC.

### 📸 Snapshot

```bash
sudo zfs snapshot rpool/ROOT/pve-1@snap-pre-fase4
```

### 4.1 Instalar o CrowdSec

> **Cadeia de confiança:** o método oficial documentado começa por `curl -s https://install.crowdsec.net | sudo sh`. Se preferir não executar scripts remotos, siga [Manual Repository Installation](https://docs.crowdsec.net/u/getting_started/installation/linux/#manual-repository-installation) na documentação CrowdSec.

```bash
curl -s https://install.crowdsec.net | sudo sh
sudo apt update
sudo apt install crowdsec crowdsec-firewall-bouncer-nftables -y
```

> O pacote `crowdsec-firewall-bouncer-nftables` aplica decisões via **nftables** (adequado quando o host usa firewall nft). A doc de instalação Linux exemplifica muitas vezes o bouncer **iptables**; no Proxmox com `proxmox-firewall`, o variante nftables costuma ser o mais coerente. Em caso de dúvida, veja [Firewall bouncer](https://docs.crowdsec.net/u/bouncers/firewall).

**O que cada componente faz:**

- `crowdsec` — o "cérebro" que lê logs e detecta padrões  
- `crowdsec-firewall-bouncer-nftables` — o "braço" que bloqueia IPs via nftables

### 4.2 Whitelist (CRÍTICO para não se banir)

⚠️ **Sem whitelist, errar a senha algumas vezes te bana do seu próprio servidor.**

```bash
sudo nano /etc/crowdsec/parsers/s02-enrich/whitelists.yaml
```

> **Caminho do ficheiro:** em versões recentes do CrowdSec a árvore sob `/etc/crowdsec/` pode diferir. Se o ficheiro acima não existir, procure `whitelists` com `find /etc/crowdsec -name '*hitelist*' 2>/dev/null` ou consulte a documentação da sua versão (`cscli version`).

Cole exatamente:

```yaml
name: my_whitelist
description: "Trusted internal networks"
whitelist:
  reason: "Rede local e Tailscale são confiáveis"
  ip:
    - "127.0.0.1"
  cidr:
    - "192.168.1.0/24"   # Ajuste para sua rede (confira com 'ip addr')
    - "100.64.0.0/10"    # Faixa completa do Tailscale
```

> **Como descobrir sua faixa local:** `ip -4 addr show vmbr0` → procure `inet 192.168.X.X/24`. Use a rede (`192.168.X.0/24`).

```bash
sudo systemctl restart crowdsec
sudo systemctl enable --now crowdsec-firewall-bouncer
```

### ✅ Verifique

```bash
sudo systemctl status crowdsec --no-pager
sudo systemctl status crowdsec-firewall-bouncer --no-pager
# Ambos: Active: active (running)
```

```bash
sudo cscli bouncers list
# Saída esperada: tabela com cs-firewall-bouncer e status válido
```

```bash
sudo cscli collections list
# Saída esperada: coleções linux, sshd, etc.
```

```bash
sudo cscli decisions list
# Saída esperada: tabela (pode estar vazia ou com bans do feed comunitário)
```

**Confirmar que o nftables tem a chain do CrowdSec:**

```bash
sudo nft list ruleset | grep -i crowdsec
# Saída esperada: pelo menos uma linha mencionando 'crowdsec'
```

> **CrowdSec + `proxmox-firewall` (nftables):** o host pode ter **vários** consumidores de nftables ao mesmo tempo. Os nomes de tabela/chain do bouncer **mudam entre versões**. Se, após a Fase 7, bans ou comportamentos estranhos deixarem de bater com o esperado, inspecione o conjunto completo com `sudo nft list ruleset` e cruze com a [documentação do bouncer](https://docs.crowdsec.net/u/bouncers/firewall) e a [wiki Firewall](https://pve.proxmox.com/wiki/Firewall) — não assumas um único nome de chain fixo copiado da internet.

### 4.3 (Opcional) Conectar ao CrowdSec Console

Para ter um dashboard web bonito:

1. Crie conta gratuita em `https://app.crowdsec.net`
2. Obtenha o enrollment token
3. Execute:
```bash
sudo cscli console enroll <SEU_TOKEN>
sudo systemctl reload crowdsec
```
4. Confirme o device no dashboard web.

### 🆘 Se deu errado

**Erro:** `cscli: command not found`
**Solução:** Instalação não completou. Repita 4.1.

**Erro:** Bouncer com `valid: false`
**Solução:**
```bash
sudo apt reinstall crowdsec-firewall-bouncer-nftables
sudo systemctl restart crowdsec-firewall-bouncer
```

**Erro:** Você foi banido por engano
**Solução:**
```bash
sudo cscli decisions list                          # ver IPs banidos
sudo cscli decisions delete --ip SEU_IP            # remover ban específico
sudo cscli decisions delete --all                  # emergência: remover TODOS
```

### 📝 Documente

```bash
echo "## $(date +%F %H:%M) - Fase 4 concluída" >> ~/fortaleza-lab/diario.md
echo "- CrowdSec + bouncer nftables ativo" >> ~/fortaleza-lab/diario.md
```

---

# 🟢 FASE 5 — Acesso Invisível (Tailscale em LXC)

🎯 **OBJETIVO:** Acessar o Proxmox de qualquer lugar do mundo, sem abrir uma única porta no roteador.

📚 **FUNDAMENTO:** Em vez de "ouvir" conexões da internet (alvo de scanners 24/7), seu servidor faz o caminho contrário: cria um túnel criptografado de SAÍDA até o Tailscale. Vocês se encontram numa "rede privada virtual" que ninguém de fora consegue ver.

### 📸 Snapshot

```bash
sudo zfs snapshot rpool/ROOT/pve-1@snap-pre-fase5
```

### 5.1 Baixar o template Debian 13

No painel web:
1. Árvore lateral → `local (pve)`
2. Aba **CT Templates** → **Templates**
3. Procure `debian-13-standard` → **Download**

### 5.2 Criar o Container LXC

**Create CT** (canto superior direito):

| Aba | Campo | Valor |
|-----|-------|-------|
| General | CT ID | `100` |
| General | Hostname | `vpn-tailscale` |
| General | Password | (senha forte, guarde no Bitwarden como "CT 100 root") |
| General | SSH key | (cole sua chave pública aqui) |
| Template | Template | `debian-13-standard_13.x...` |
| Disks | Disk size | `4` (GB) |
| CPU | Cores | `1` |
| Memory | Memory | `512` (MB) — ⚠️ não use 256 |
| Memory | Swap | `512` (MB) |
| Network | IPv4 | `Static` |
| Network | IPv4/CIDR | `192.168.1.110/24` |
| Network | Gateway | `192.168.1.1` |
| Network | DNS | `1.1.1.1 8.8.8.8` |
| Confirm | Start after created | ✅ |

> 🔍 **Por que IP estático no container?** Para você poder criar regras de firewall específicas depois.

### 5.3 Habilitar TUN e features (método moderno via CLI)

⚠️ **Etapa crítica.** Sem isso, o Tailscale **NÃO** funciona em LXC unprivileged.

No terminal SSH do **Proxmox host** (como renato com sudo):

```bash
# Para o container primeiro
sudo pct stop 100

# Habilita keyctl e nesting (necessários para Tailscale)
sudo pct set 100 --features keyctl=1,nesting=1

# Passa o device /dev/net/tun para o container (método moderno)
sudo pct set 100 --dev0 /dev/net/tun

# Inicia o container
sudo pct start 100
```

> 📚 **O que isso faz:**
> - `keyctl=1` — permite chamadas de sistema para retenção de chaves do kernel
> - `nesting=1` — expõe procfs/sysfs do host (necessário para namespaces aninhados)
> - `--dev0 /dev/net/tun` — passa o dispositivo TUN do host para dentro do container, permitindo modo kernel do Tailscale (sem isso, ele cairia em modo userspace, que tem desempenho ruim)

### 5.4 Instalar o Tailscale dentro do container

Abra o **Console** do CT 100 (`>_ Console` no topo), logue como root:

Antes de instalar o Tailscale, confirme **rede e DNS** dentro do CT (sem isso, `curl`/`install.sh` falham sem diagnóstico claro):

```bash
ping -c 2 1.1.1.1 && echo "Rede IP OK" || echo "Sem reachability IP — verifique gateway/IP estático do CT no Proxmox"
ping -c 1 -W 3 tailscale.com && echo "Resolução DNS OK (tailscale.com)" || echo "Falhou reachability ou DNS — confira /etc/resolv.conf e os dns-nameservers usados na criação do CT"
```

```bash
apt update && apt install curl -y
# Cadeia de confiança: o script oficial de instalação é remoto — reveja https://tailscale.com/install.sh se quiser auditar antes.
curl -fsSL https://tailscale.com/install.sh | sh
```

Verifique se o TUN está acessível dentro do CT:

```bash
ls -l /dev/net/tun
# Deve mostrar: crw-rw-rw- 1 nobody nogroup 10, 200 ...
```

### 5.4b Subnet router — encaminhamento IP no CT

Para o Linux **encaminhar** tráfego entre `tailscale0` e a LAN (`192.168.1.x`), o kernel do CT precisa de `ip_forward` activo. Isto é **dentro do CT 100** (console como root), não no host Proxmox.

> O comando `tailscale up --advertise-routes=...` **aceita sem erro** mesmo com forwarding em `0` — o sintoma é subnet aprovada no admin e **mesmo assim** tráfego que não roteia. Em clientes Tailscale recentes no Debian, o instalador ou o próprio serviço **podem** criar `/etc/sysctl.d/99-tailscale.conf` com forwarding; **não assumas**: confirma no teu CT após o primeiro `tailscale up`. Ver [Subnet routers](https://tailscale.com/kb/1019/subnets/).

Inicie o Tailscale anunciando a rede local como subnet:

```bash
tailscale up --advertise-routes=192.168.1.0/24 --accept-routes
```

> **Tradução:**
> - `--advertise-routes=192.168.1.0/24` — anuncia "eu sei chegar nessa rede" (permite que seus dispositivos cheguem ao IP local do Proxmox via Tailscale)
> - `--accept-routes` — aceita rotas anunciadas por outros peers

Vai aparecer um link `https://login.tailscale.com/a/...`. Abra no navegador, autentique (Google, GitHub, etc.).

Depois de autenticado, **ainda no CT**, verifica se o forwarding já ficou activo:

```bash
sysctl net.ipv4.ip_forward net.ipv6.conf.all.forwarding
```

- Se `net.ipv4.ip_forward = 1` (e `net.ipv6.conf.all.forwarding = 1` se precisares de IPv6 na rota), **não** precisas do bloco manual abaixo — o Tailscale ou o sistema já aplicaram.
- Se `net.ipv4.ip_forward` for **0**, aplica manualmente (ficheiro separado para não sobrescrever um `99-tailscale.conf` eventualmente criado pelo cliente):

```bash
echo 'net.ipv4.ip_forward = 1' | tee /etc/sysctl.d/99-fortaleza-tailscale-forward.conf
echo 'net.ipv6.conf.all.forwarding = 1' | tee -a /etc/sysctl.d/99-fortaleza-tailscale-forward.conf
sysctl -p /etc/sysctl.d/99-fortaleza-tailscale-forward.conf
```

### 5.5 Aprovar a subnet route

`https://login.tailscale.com/admin/machines`:
1. Encontre `vpn-tailscale`
2. **⋯ → Edit route settings**
3. Marque ✅ `192.168.1.0/24`
4. **Save**

### 5.6 Tailscale no seu PC e celular

- **Windows/macOS/Linux:** https://tailscale.com/download
- **Android/iOS:** Play Store / App Store
- Logue com a **mesma conta**

### ✅ Verifique

No console do CT 100:
```bash
tailscale status                 # Lista de peers conectados
tailscale ip                     # IP da VPN (100.x.x.x)

# Confirmar que está em modo kernel (não userspace):
ip addr show tailscale0
# Deve existir interface tailscale0 com IP 100.x.x.x
```

> Se **`tailscale0` não existir**, o TUN/capabilities podem estar incompletos — reveja a Fase 5 (`pct set`, device passthrough) ou a doc [Tailscale em LXC](https://tailscale.com/docs/features/containers/lxc/lxc-unprivileged) (modo userspace só como último recurso, com pior desempenho típico).

No seu PC/celular (Tailscale ativo):
```
https://192.168.1.100:8006
```
Deve carregar o painel mesmo via 4G.

### 🆘 Se deu errado

**Erro:** `tstun.New("tailscale0"): operation not permitted`
**Causa:** Features e/ou device TUN não habilitados.
**Solução:** Repita `sudo pct set 100 --dev0 /dev/net/tun` com container parado.

**Erro:** Conecta no Tailscale mas não enxerga `192.168.1.100`
**Causa:** Subnet route não aprovada, `sysctl` ainda em `0` após `tailscale up`, ou firewall.
**Solução:** Passo 5.5; em 5.4b confirma `sysctl net.ipv4.ip_forward` e aplica o bloco manual se for `0`.

### 📝 Documente

```bash
echo "## $(date +%F %H:%M) - Fase 5 concluída" >> ~/fortaleza-lab/diario.md
echo "- CT 100 vpn-tailscale ativo com subnet routing" >> ~/fortaleza-lab/diario.md
echo "- IP Tailscale do PVE: $(sudo pct exec 100 -- tailscale ip)" >> ~/fortaleza-lab/diario.md
```

---

# 🟢 FASE 6 — 2FA no Painel Web do Proxmox

🎯 **OBJETIVO:** Criar `renato@pam` como administrador com 2FA, nunca mais usar `root@pam` na interface.

📚 **FUNDAMENTO:** O painel web tem dois "realms":
- `pam` — usuários do sistema Linux
- `pve` — usuários internos do Proxmox

Vamos usar `pam`. **O 2FA do painel é separado do 2FA do SSH** — tem que configurar de novo.

### ⚙️ Passo a passo

Acesse `https://192.168.1.100:8006` (via Tailscale ou rede local) e logue como **root@pam** pela última vez.

**1. Criar o usuário no Proxmox:**
- **Datacenter → Permissions → Users → Add**
- User name: `renato`
- Realm: `Linux PAM standard authentication`
- Enabled: ✅
- **Add**

**2. Dar Administrator:**
- **Datacenter → Permissions → Add → User Permission**
- Path: `/`
- User: `renato@pam`
- Role: `Administrator`
- Propagate: ✅
- **Add**

**3. Sair e entrar como renato@pam:**
- **Logout**
- User: `renato`, Realm: `Linux PAM`, Password: (a do renato)

**4. Ativar TOTP:**
- Canto superior direito (`renato@pam`) → **TFA**
- **Add → TOTP**
- Description: `Celular Renato`
- Escaneie o QR Code com o app
- Digite o código de 6 dígitos
- **Add**

> 🔐 **Salve no Bitwarden:**
> - QR code / chave secreta
> - "2FA painel Proxmox - renato@pam"

**5. Adicionar Recovery Keys (importante!):**
- **Add → Recovery Keys**
- Salve TODAS no Bitwarden

### ✅ Verifique

Logout e logue como `renato@pam`. Deve pedir senha + código TOTP.

### 📝 Documente

```bash
echo "## $(date +%F %H:%M) - Fase 6 concluída" >> ~/fortaleza-lab/diario.md
echo "- renato@pam Administrator com 2FA TOTP" >> ~/fortaleza-lab/diario.md
```

---

# 🟢 FASE 7 — Firewall nftables (proxmox-firewall)

🎯 **OBJETIVO:** Migrar para o backend `nftables` moderno do Proxmox 9 e fazer o servidor "sumir" da internet.

📚 **FUNDAMENTO:** O Proxmox VE 9 oferece **proxmox-firewall**, implementação do mesmo modelo de regras da GUI mas sobre **nftables** (em alternativa ao serviço clássico baseado em iptables). A [wiki oficial](https://pve.proxmox.com/wiki/Firewall#nftables) classifica o **nftables backend** como *tech preview*: pode haver bugs ou diferenças face ao firewall “stock”; **não é descrita como adequada para produção** na documentação (homelab com backups e consciência do risco é outra história). Vantagens citadas na wiki: melhor desempenho, regras **forward** e regras a nível de VNet em SDN — funcionalidades ignoradas pelo `pve-firewall` clássico.

### 📸 Snapshot e backup

```bash
sudo zfs snapshot rpool/ROOT/pve-1@snap-pre-fase7
sudo tar czf /root/backups/etc-pve-fase7-$(date +%F).tar.gz /etc/pve/
```

### 7.1 Instalar o pacote proxmox-firewall

```bash
sudo apt install proxmox-firewall -y
```

> Geralmente já vem instalado no PVE 9.x, mas garantia não faz mal.

### 7.2 Criar regras de ACCEPT (ANTES de habilitar DROP)

⚠️ **SEMPRE crie ACCEPT antes de mudar para DROP, senão você se tranca fora.**

**Datacenter → Firewall → Rules → Add** — crie estas 4 regras:

| Direction | Action | Source | Dest. port | Protocol | Comment |
|-----------|--------|--------|------------|----------|---------|
| in | ACCEPT | `100.64.0.0/10` | `22` | tcp | SSH via Tailscale |
| in | ACCEPT | `100.64.0.0/10` | `8006` | tcp | Web GUI via Tailscale |
| in | ACCEPT | `192.168.1.0/24` | `22` | tcp | SSH rede local (emergência) |
| in | ACCEPT | `192.168.1.0/24` | `8006` | tcp | Web GUI rede local (emergência) |

✅ Marque **Enable** em cada regra.

### 7.3 Habilitar o firewall

**Datacenter → Firewall → Options → Edit:**
- Firewall: **Yes**
- Input Policy: **DROP**
- Output Policy: **ACCEPT**
- Log level in: **info**
- Log level out: **nolog**

**No nível do Nó:** `pve → Firewall → Options → Edit:`
- Firewall: **Yes**

### 7.4 Migrar para o backend nftables

📚 **FUNDAMENTO:** Por padrão, o nó pode ainda usar o serviço clássico (`pve-firewall`, iptables). Ativar **nftables: Yes** no host passa o trabalho para o serviço `proxmox-firewall`.

**No painel:** `pve (seu nó) → Firewall → Options → Edit:`
- nftables: **Yes**

> A interface pode mostrar *tech preview* — coincide com a [documentação Proxmox](https://pve.proxmox.com/wiki/Firewall#nftables). Depois de alternar o backend, a wiki recomenda **reiniciar todas as VMs e CTs** para o novo firewall atuar de forma consistente; planeje uma janela curta de manutenção.

### ✅ Verifique

```bash
sudo systemctl status proxmox-firewall --no-pager
# Saída esperada: active (running)
```

```bash
sudo nft list tables
# Deve aparecer, entre outras possíveis:
# table inet proxmox-firewall        ← backend do PVE (nftables)
# table bridge proxmox-firewall-guests
# ... e uma tabela do bouncer CrowdSec (nome típico: contém "crowdsec" — ex.: table inet crowdsec)
```

Se a tabela do CrowdSec **não** aparecer mas a Fase 4 já instalou o bouncer nftables:

```bash
sudo systemctl status crowdsec-firewall-bouncer --no-pager
sudo systemctl restart crowdsec-firewall-bouncer
sudo nft list tables
```

```bash
sudo nft list ruleset | head -50
# Inspeção do ruleset ativo
```

Confirmar que o firewall clássico **não** está a empilhar regras iptables quando esperas só nftables:

```bash
systemctl is-active pve-firewall
```

> **Ler o estado:** com **nftables: Yes** e `proxmox-firewall` a tratar do host, o serviço `pve-firewall` pode aparecer como `inactive` (esperado) **ou** `active` em algumas versões/configurações sem isso significar que ainda estás no backend iptables clássico. O sinal mais útil para “ainda há regras estilo pve-firewall em iptables” são **cadeias PVEFW** em `iptables -L`. Cruza sempre com `sudo systemctl status proxmox-firewall` e a [wiki Firewall](https://pve.proxmox.com/wiki/Firewall).

Se `iptables` existir no host:

```bash
if sudo iptables -L 2>/dev/null | grep -q "PVEFW"; then
  echo "ATENÇÃO: PVEFW detectado — o pve-firewall clássico ainda pode estar a gerar regras iptables."
  echo "          Confirma: systemctl is-active pve-firewall && sudo systemctl status proxmox-firewall --no-pager"
else
  echo "OK: sem chains PVEFW visíveis em iptables (ou iptables vazio / não usado neste nó)."
fi
```

> Em hosts **só nftables**, `iptables -L` pode estar vazio ou mapear para nft — o objectivo é não ficar com **duas** camadas de firewall por engano; se vires PVEFW massivo enquanto esperas nft-only, investiga antes de declarar a fase fechada.

**Teste de conectividade:**

```bash
# Do seu PC (com Tailscale):
ssh fortaleza                 # → deve funcionar

# Do seu PC (na rede local):
ssh renato@192.168.1.100      # → deve funcionar

# Do celular no 4G (sem Tailscale):
# Tente acessar IP_PUBLICO_CASA porta 22 → deve dar timeout
```

### 7.5 Fechar port forwarding no roteador

No painel do roteador, remova qualquer:
- Port Forwarding / NAT
- DMZ
- UPnP apontando para o Mini PC

Especialmente as portas 22 e 8006.

### 🆘 Se deu errado

**Erro:** Você se trancou fora
**Solução:** Console físico ou web:
```bash
# Parar TODOS os firewalls
sudo systemctl stop proxmox-firewall
sudo systemctl stop pve-firewall
sudo pve-firewall stop
```
Edite `/etc/pve/firewall/cluster.fw`, mude `enable: 1` para `enable: 0` na seção `[OPTIONS]`. Reinicie o serviço quando corrigir as regras.

**Erro:** `proxmox-firewall.service: failed`
**Solução:**
```bash
sudo journalctl -u proxmox-firewall -n 50 --no-pager
# Veja os erros e corrija as regras inválidas
# Acompanhar em tempo real (Ctrl+C para sair):
sudo journalctl -u proxmox-firewall -f
```

### 📝 Documente

```bash
echo "## $(date +%F %H:%M) - Fase 7 concluída" >> ~/fortaleza-lab/diario.md
echo "- Firewall nftables com DROP, 4 regras ACCEPT" >> ~/fortaleza-lab/diario.md
echo "- Port forwarding removido do roteador" >> ~/fortaleza-lab/diario.md
```

---

# 🟢 FASE 8 — Laboratório do Irmão (ShellHub + GPG)

🎯 **OBJETIVO:** VM isolada para o irmão estudar GPG, sem expor sua rede e sem entregar acesso ao lab.

📚 **FUNDAMENTO:** ShellHub usa **túnel reverso via Docker**. A VM do irmão "liga" para o ShellHub na nuvem. Quando ele se conecta, o tráfego escorrega pelo túnel até cair na VM. Você não abre porta nenhuma.

> ⚠️ **O método oficial do ShellHub Agent requer Docker.** Por isso vamos habilitar `nesting=1` e instalar Docker no LXC. **Nota:** Docker dentro de LXC usa namespaces aninhados — mais overhead que um CT “só Debian”; para **laboratório isolado** (como o do irmão) é aceitável; não é o padrão típico de produção.

### 📸 Snapshot

```bash
sudo zfs snapshot rpool/ROOT/pve-1@snap-pre-fase8
```

### 8.1 Criar o LXC

**Create CT:**

| Campo | Valor |
|-------|-------|
| CT ID | `200` |
| Hostname | `lab-irmao-gpg` |
| Password | (senha forte do root, Bitwarden) |
| Template | `debian-13-standard...` |
| Disk | `10 GB` |
| Cores | `1` |
| Memory | `1024 MB` |
| Swap | `512 MB` |
| Network | IPv4 Static `192.168.1.120/24`, Gateway `192.168.1.1`, DNS `1.1.1.1` |
| Tags | `lab`, `irmao` |
| Unprivileged | ✅ |

### 8.2 Habilitar features para Docker rodar dentro

```bash
sudo pct stop 200
sudo pct set 200 --features keyctl=1,nesting=1
sudo pct start 200
```

### 8.3 Hardening básico dentro do container

Console do CT 200, logado como root:

```bash
apt update && apt full-upgrade -y
apt install sudo gnupg curl nano ca-certificates -y

# Criar usuário do irmão
adduser irmao
usermod -aG sudo irmao
```

### 8.4 Instalar Docker no container

```bash
# Cadeia de confiança: script remoto da Docker Inc. — alternativa: instalar docker.io dos repos Debian, se preferir pacote só Debian.
curl -fsSL https://get.docker.com | sh
systemctl enable --now docker
docker --version
docker run hello-world
```

### 8.5 Registrar o device no ShellHub Cloud

1. Crie conta gratuita em **https://cloud.shellhub.io**
2. Painel: **Devices → Add Device**
3. Copie o comando de instalação (envolve `curl`/`install.sh` da ShellHub). Confira o procedimento atual em [ShellHub Documentation](https://docs.shellhub.io/).
4. Cole no console do CT 200
5. Volte ao painel ShellHub → device em **Pending** → **Accept**

### 8.6 Como o irmão acessa

No painel ShellHub, **Connect** ao lado do device:

```
ssh irmao@SSHID.shellhub.io
```

Mande esse comando para o irmão. Ele cola no terminal dele e cai direto na VM.

### 8.7 Bônus pedagógico — GPG na prática

Primeiro exercício para ele:

```bash
# Na VM dele (como irmao)
gpg --full-generate-key
# Tipo: 9 (ECC sign and encrypt) → Curva: 1 (Curve 25519)
# Validade: 1y, Nome: dele, Email: dele

gpg --armor --export irmao@email.com > irmao.pub
cat irmao.pub
```

Ele te manda o bloco. Você importa:

```bash
nano irmao.pub      # Cole o conteúdo
gpg --import irmao.pub
gpg --list-keys
```

Criptografa uma mensagem:

```bash
echo "Bem-vindo ao lab, mano!" | gpg --encrypt --armor -r irmao@email.com > msg.asc
cat msg.asc
```

Ele cola e descriptografa:

```bash
nano msg.asc        # cola, salva, sai
gpg --decrypt msg.asc
```

🎉 **Criptografia assimétrica aplicada na prática.**

### 📝 Documente

```bash
echo "## $(date +%F %H:%M) - Fase 8 concluída" >> ~/fortaleza-lab/diario.md
echo "- CT 200 lab-irmao-gpg com Docker + ShellHub agent" >> ~/fortaleza-lab/diario.md
```

---

# 🟢 FASE 9 — Manutenção Automática

🎯 **OBJETIVO:** Atualizações de segurança automáticas + observabilidade.

### 9.1 Atualizações automáticas (Proxmox host)

```bash
sudo apt install unattended-upgrades needrestart apt-listchanges -y
sudo dpkg-reconfigure --priority=low unattended-upgrades
# Responda: Yes
```

Verifique o que será atualizado:

```bash
cat /etc/apt/apt.conf.d/50unattended-upgrades | grep -A 5 "Allowed origins"
# Procure por "Debian-Security" - deve estar ativo
```

### 9.1b `needrestart` e desconexão SSH (leia antes de reclamar do `unattended-upgrades`)

O pacote **needrestart** (instalado na secção anterior) detecta daemons que precisam de reinício após atualização de bibliotecas. No ficheiro de exemplo [upstream](https://github.com/liske/needrestart/blob/master/ex/needrestart.conf), o modo de reinício é: **`l`** = só listar, **`i`** = interactivo, **`a`** = **reinício automático**. Em ambientes **não interactivos** (como o hook do `unattended-upgrades`), o modo interactivo pode fazer **fallback** para “só listar” — ou seja, **não** confundas “passar tudo para automático (`a`)" com “evitar surpresas”: o modo **`a`** pode **reiniciar serviços sem perguntar**, o que em acesso remoto pode ser **pior** se não souberes o que vai ser tocado.

**Recomendações práticas (homelab com SSH remoto):**

- Trate janelas de `full-upgrade` / reinícios como **manutenção**: duas sessões SSH, ou consola física.  
- Leia a documentação Debian sobre [UnattendedUpgrades](https://wiki.debian.org/UnattendedUpgrades) e o projeto [needrestart](https://github.com/liske/needrestart) antes de alterar `/etc/needrestart/needrestart.conf`.  
- **Não copie** da internet receitas `sed` que mudam `$nrconf{restart}` para `'a'` sem entender o efeito — pode aumentar reinícios automáticos.

### 9.2 Ferramentas essenciais

```bash
sudo apt install htop iotop iftop ncdu tree -y
```

| Comando | Para que serve |
|---------|----------------|
| `htop` | CPU/RAM/processos em tempo real |
| `iotop` | Quem está usando o disco |
| `iftop` | Tráfego de rede |
| `ncdu` | Descobrir o que ocupa espaço |
| `tree` | Ver árvore de diretórios |

### 9.3 Repetir em cada CT/VM

Os CTs 100, 200 (e os que você criar depois) também precisam de:

```bash
# Dentro de cada CT
apt update && apt install unattended-upgrades -y
dpkg-reconfigure --priority=low unattended-upgrades
```

### 📝 Documente

```bash
echo "## $(date +%F %H:%M) - Fase 9 concluída" >> ~/fortaleza-lab/diario.md
echo "- unattended-upgrades + ferramentas instaladas" >> ~/fortaleza-lab/diario.md
```

---

# 🟢 FASE 10 — Documentação Viva e Recuperação

🎯 **OBJETIVO:** Garantir que daqui a 6 meses, **mesmo esquecendo tudo**, você consegue recuperar/manter o lab.

📚 **FUNDAMENTO:** Um homelab sem documentação vira lixo eletrônico. Esta fase cria três artefatos vitais:
1. **README local** — visão geral atualizada do estado do lab
2. **Diário de mudanças** — histórico do que você fez
3. **Plano de recuperação** — passos para reconstruir do zero

> **Laboratório descartável (filosofia):** aprender inclui quebrar, reinstalar e documentar. No Proxmox isso traduz-se em **snapshots** antes de mudanças grandes, **`vzdump`** e cópias de `/etc/pve` para disco externo — separar o que é **configuração do nó** do que são **dados das VMs**. Podes ainda manter pastas tipo `~/scripts` e `~/notes` dentro de `~/fortaleza-lab/` ou nas VMs de estudo (ver [docs/linux-comandos-fundamentos.md](docs/linux-comandos-fundamentos.md)).

### 10.1 README local

Como `renato` no Proxmox:

```bash
cat > ~/fortaleza-lab/README.md << 'EOF'
# Fortaleza Proxmox — Estado Atual

## Hardware
- Mini PC, 16 GB RAM, Proxmox VE 9.x (Debian 13 Trixie)

## Rede
- IP local: 192.168.1.100/24
- Gateway: 192.168.1.1
- DNS: 1.1.1.1, 8.8.8.8
- Tailscale IP: (preencher após Fase 5)

## Acesso
- SSH: `ssh fortaleza` (alias no ~/.ssh/config)
- Web GUI: https://192.168.1.100:8006 (renato@pam)
- Emergência: console físico do Mini PC

## Containers Ativos
| ID  | Nome             | IP             | Função                   |
|-----|------------------|----------------|--------------------------|
| 100 | vpn-tailscale    | 192.168.1.110  | VPN Tailscale + subnet   |
| 200 | lab-irmao-gpg    | 192.168.1.120  | Lab GPG do irmão         |

## Segurança Ativa
- SSH: chave Ed25519 + 2FA TOTP (renato)
- root SSH: BLOQUEADO
- Painel web: senha + 2FA TOTP
- CrowdSec + bouncer nftables
- Firewall proxmox-firewall (nftables) em DROP
- Acesso externo: APENAS via Tailscale
- Port forwarding no roteador: DESATIVADO

## Backups
- /root/backups/etc-pve-*.tar.gz (locais)
- Snapshots ZFS: rpool/ROOT/pve-1@snap-*

## Próximos Projetos
- [ ] AdGuard Home (CT 101)
- [ ] Nginx Proxy Manager (CT 102)
- [ ] Vaultwarden (CT 300)
- [ ] Uptime Kuma (CT 301)
EOF

cat ~/fortaleza-lab/README.md
```

### 10.2 Diário de mudanças

Você já vem fazendo isso desde a Fase 1. Continue:

```bash
# Sempre que mudar algo significativo:
echo "## $(date +%F %H:%M) - <Título da mudança>" >> ~/fortaleza-lab/diario.md
echo "- <O que foi feito>" >> ~/fortaleza-lab/diario.md
echo "- <Comando ou config relevante>" >> ~/fortaleza-lab/diario.md
echo "" >> ~/fortaleza-lab/diario.md
```

### 10.3 Backup completo do `/etc/pve`

Crie um script de backup:

```bash
sudo nano /usr/local/bin/backup-fortaleza.sh
```

Cole:

```bash
#!/bin/bash
# Backup do /etc/pve para /root/backups/
set -e

DATE=$(date +%F-%H%M)
BACKUP_DIR="/root/backups"
mkdir -p "$BACKUP_DIR"

# Backup do /etc/pve (configurações Proxmox)
tar czf "$BACKUP_DIR/etc-pve-$DATE.tar.gz" /etc/pve/

# Verificação básica: o tar deve listar sem erro (não extrai)
tar tzf "$BACKUP_DIR/etc-pve-$DATE.tar.gz" >/dev/null && echo "OK: arquivo tar legível"

# Manter só os últimos 30 backups
ls -t "$BACKUP_DIR"/etc-pve-*.tar.gz | tail -n +31 | xargs -r rm

echo "Backup OK: $BACKUP_DIR/etc-pve-$DATE.tar.gz"
ls -lh "$BACKUP_DIR/etc-pve-$DATE.tar.gz"
```

Permissões e teste:

```bash
sudo chmod +x /usr/local/bin/backup-fortaleza.sh
sudo /usr/local/bin/backup-fortaleza.sh
```

Teste manual do último backup (opcional, a qualquer momento):

```bash
LATEST=$(ls -t /root/backups/etc-pve-*.tar.gz | head -1)
tar tzf "$LATEST" >/dev/null && echo "Backup íntegro: $LATEST"
```

### Agendar backup diário via cron

```bash
sudo crontab -e
```

Adicione no final:
```
# Backup diário às 03:00
0 3 * * * /usr/local/bin/backup-fortaleza.sh >> /var/log/backup-fortaleza.log 2>&1
```

### 10.4 Copiar backups para fora do servidor

⚠️ **Backup que fica só no servidor não é backup.** Configure para copiar para seu PC:

No seu PC pessoal, crie um script:

```bash
nano ~/sync-fortaleza-backups.sh
```

```bash
#!/bin/bash
# Sincroniza backups do Proxmox para o PC
rsync -avz --delete \
  fortaleza:/root/backups/ \
  ~/fortaleza-backups/
```

```bash
chmod +x ~/sync-fortaleza-backups.sh
~/sync-fortaleza-backups.sh
```

> Rode esse comando uma vez por semana, manualmente, ou agende um cron no seu PC.

### 10.5 Plano de Recuperação (RUNBOOK)

Crie um runbook para o seu "eu do futuro":

```bash
cat > ~/fortaleza-lab/recuperacao.md << 'EOF'
# Plano de Recuperação — Fortaleza Proxmox

## Cenário 1: Perdi acesso SSH (não consigo logar)

1. Acesso físico ao Mini PC (monitor + teclado)
2. Logue como root (senha no Bitwarden)
3. Verifique:
   - `systemctl status ssh`
   - `cat /etc/ssh/sshd_config.d/99-hardening.conf`
4. Se config quebrada: comente as linhas problemáticas, restart ssh.

## Cenário 2: Perdi o celular do 2FA

1. Use um dos 5 códigos de recuperação salvos no Bitwarden
2. Reconfigure o 2FA imediatamente após logar:
   - `google-authenticator` (gerar novo segredo)
   - Atualizar Bitwarden com novos códigos

## Cenário 3: Mini PC quebrou / disco morreu

1. Compre/recupere hardware
2. Reinstale Proxmox VE 9.x (ISO atual da série 9)
3. Configure rede igual: IP 192.168.1.100/24
4. Restaure `/etc/pve` do último backup:
   - `tar xzf etc-pve-DATE.tar.gz -C /`
5. **TLS / certificado do painel:** após restaurar numa máquina nova ou com hostname/IP diferentes, o browser pode alertar certificado não confiável até alinhares certificados com o nó atual. Consulte a wiki [Certificate Management](https://pve.proxmox.com/wiki/Certificate_Management) e `man pvenode` na tua versão — **não** forces comandos de cluster (`pvecm`) copiados da internet sem ler a doc (contexto *single node* vs *cluster*).
6. Restaure containers (templates + backups VM)
7. Reconfigure Tailscale (re-autenticar device)

## Cenário 4: Me banni acidentalmente no CrowdSec

1. Console físico ou web → terminal local
2. `sudo cscli decisions delete --ip MEU_IP`
3. Ou: `sudo cscli decisions delete --all` (emergência)

## Cenário 5: Firewall me trancou fora

1. Console físico do Mini PC
2. `pve-firewall stop`
3. `systemctl stop proxmox-firewall`
4. Editar `/etc/pve/firewall/cluster.fw` → `enable: 0`
5. Corrigir as regras, depois `enable: 1` e restart

## Senhas e Segredos Críticos
- TODOS no Bitwarden, pasta "Fortaleza Proxmox"
- Console físico do Mini PC: sempre acessível (não trancar a sala!)
- Códigos de recuperação 2FA: impressos e guardados separadamente também

EOF

cat ~/fortaleza-lab/recuperacao.md
```

### 10.6 Versionar no Git (opcional mas recomendado)

```bash
cd ~/fortaleza-lab
git init
git add README.md diario.md recuperacao.md
git config user.email "renato@example.com"
git config user.name "Renato"
git commit -m "Estado inicial da Fortaleza Proxmox v5.0"
```

> Se quiser, depois pode fazer push para um repo privado no GitHub.

### 📝 Documente

```bash
echo "## $(date +%F %H:%M) - Fase 10 concluída" >> ~/fortaleza-lab/diario.md
echo "- README, diário, recuperação criados" >> ~/fortaleza-lab/diario.md
echo "- Backup automático via cron 03:00" >> ~/fortaleza-lab/diario.md
```

---

# 📋 Apêndice A — Checklist Final Consolidado

## FASE 0 — Preparação
- [ ] Timezone correto, NTP ativo (`timedatectl status` → synchronized: yes)
- [ ] IP fixo configurado (estático no PVE OU reserva no roteador)
- [ ] `hostname -i` retorna IP correto (não 127.0.1.1)
- [ ] Repositório Enterprise desabilitado
- [ ] Repositório No-Subscription habilitado
- [ ] `apt update` sem erros
- [ ] Sistema atualizado, reboot se kernel mudou
- [ ] Backup inicial do /etc/pve em /root/backups/
- [ ] Snapshot ZFS `snap-fase0-instalacao-limpa`

## FASE 1 — Identidade
- [ ] Usuário `renato` criado, `sudo whoami` retorna `root`
- [ ] Senha do `renato` no Bitwarden

## FASE 2 — SSH
- [ ] Chave Ed25519 gerada, passphrase no Bitwarden
- [ ] `~/.ssh/config` no PC com alias `fortaleza`
- [ ] `/etc/ssh/sshd_config.d/99-hardening.conf` criado
- [ ] `sshd -T | grep passwordauthentication` retorna `no`
- [ ] Root SSH bloqueado (`ssh root@...` recusado)

## FASE 3 — 2FA SSH
- [ ] 2FA TOTP configurado, QR/chave/recovery no Bitwarden
- [ ] Login SSH pede chave + código
- [ ] **`nullok` REMOVIDO** de `/etc/pam.d/sshd`

## FASE 4 — CrowdSec
- [ ] `cscli bouncers list` mostra bouncer válido
- [ ] Whitelist com 192.168.1.0/24 + 100.64.0.0/10
- [ ] `nft list ruleset | grep crowdsec` retorna resultado

## FASE 5 — Tailscale
- [ ] CT 100 `vpn-tailscale` rodando
- [ ] `tailscale0` aparece em `ip addr` (modo kernel)
- [ ] Subnet route aprovada no admin Tailscale
- [ ] Acesso ao PVE via 100.x.x.x funcionando

## FASE 6 — 2FA painel
- [ ] `renato@pam` Administrator no painel
- [ ] TOTP ativo, recovery keys no Bitwarden
- [ ] `root@pam` não mais usado no dia-a-dia

## FASE 7 — Firewall
- [ ] 4 regras ACCEPT criadas ANTES do DROP
- [ ] Firewall enabled em Datacenter E no Nó
- [ ] nftables: Yes habilitado
- [ ] `systemctl status proxmox-firewall` active
- [ ] `nft list tables` mostra proxmox-firewall e proxmox-firewall-guests
- [ ] Port forwarding removido do roteador
- [ ] Teste de 4G confirma servidor invisível

## FASE 8 — Lab Irmão
- [ ] CT 200 com nesting=1
- [ ] Docker rodando dentro
- [ ] ShellHub device accepted
- [ ] Irmão consegue conectar

## FASE 9 — Manutenção
- [ ] unattended-upgrades ativo no PVE e nos CTs
- [ ] htop/iotop/iftop instalados

## FASE 10 — Documentação
- [ ] README.md em ~/fortaleza-lab/
- [ ] diario.md com histórico
- [ ] recuperacao.md (runbook)
- [ ] Script de backup automático no cron
- [ ] Backups sendo copiados para fora do servidor

---

# 📊 Apêndice B — Comandos de Monitoramento Diário

Cole isso em um arquivo `~/fortaleza-lab/comandos.md`:

| O que verificar | Comando | O que esperar |
|-----------------|---------|---------------|
| IPs banidos | `sudo cscli decisions list` | Tabela de IPs |
| Estatísticas CrowdSec | `sudo cscli metrics` | Logs lidos, detections |
| Tentativas SSH | `sudo journalctl -u ssh -f` | Tempo real |
| Tentativas falhas | `sudo journalctl -u ssh \| grep -i fail` | Lista |
| Status firewall | `sudo systemctl status proxmox-firewall` | active (running) |
| Log firewall em tempo real | `sudo journalctl -u proxmox-firewall -f` | Ctrl+C para sair |
| Ruleset nftables | `sudo nft list ruleset \| less` | Regras ativas |
| Status Tailscale (CT 100) | `sudo pct exec 100 -- tailscale status` | Peers |
| Recursos | `htop` | CPU/RAM/processos |
| Serviços com falha | `systemctl --failed` | 0 listed |
| Atualizações pendentes | `apt list --upgradable 2>/dev/null` | Pacotes |
| Sincronização NTP | `timedatectl status` | synchronized: yes |
| Backups recentes | `ls -lh /root/backups/ \| tail` | Backups recentes |
| Testar leitura do último backup | `L=$(ls -t /root/backups/etc-pve-*.tar.gz \| head -1); tar tzf "$L" >/dev/null && echo OK` | `OK` se o `.tar.gz` não está corrompido |

---

# 🗂️ Apêndice C — Padrão de Organização (IDs, Nomes, Tags)

### Faixas de ID

| Faixa | Função |
|-------|--------|
| 100–199 | Infraestrutura (VPN, DNS, Proxy reverso) |
| 200–299 | Labs isolados (irmão, testes) |
| 300–399 | Serviços (Home Assistant, Jellyfin) |
| 400–499 | Bancos de dados |
| 500–599 | Dev/Build (CI runners, etc) |
| 900+ | Templates limpos |

### Padrão de hostname: `[função]-[sistema]-[ambiente]`

Exemplos:
- `vpn-tailscale-prod`
- `lab-irmao-gpg`
- `net-adguard-dns`
- `srv-jellyfin-prod`
- `db-postgres-prod`

### Padrão de tags

- `infra` — infraestrutura crítica (não desligar)
- `network` — relacionado a rede
- `prod` — produção
- `lab` — laboratório (pode quebrar)
- `irmao` — acesso compartilhado
- `database` — banco de dados
- `critical` — não pode cair

### Snapshots descritivos

- `snap-pre-instalacao-docker`
- `snap-fase4-crowdsec-ok`
- `snap-2026-05-12-funcionando`

---

# 🚀 Apêndice D — Próximos Projetos (Roadmap)

Com a fortaleza de pé, sugiro esta ordem:

1. **AdGuard Home** (CT 101, 256MB) — Bloqueia anúncios na rede inteira via DNS
2. **Nginx Proxy Manager** (CT 102, 512MB) — Reverse proxy + SSL automático Let's Encrypt
3. **Vaultwarden** (CT 300, 256MB) — Servidor de senhas próprio, compatível com Bitwarden
4. **Uptime Kuma** (CT 301, 256MB) — Monitoramento de disponibilidade + alertas
5. **Proxmox Backup Server** (VM 900, 2GB) — Backup centralizado de VMs/CTs
6. **Ansible** (no seu PC) — Automatize a criação de novos CTs

> **Docker / Kubernetes:** não é preciso Kubernetes, Swarm ou Compose enorme para começar — primeiro containers, volumes e redes (ver [instalação Docker em Debian](https://docs.docker.com/engine/install/debian/) e Fase 8 do guia). Orquestração “de empresa” fica para quando os fundamentos estiverem sólidos.

---

# ❓ Apêndice E — FAQ

**P: Por que migrar para nftables se iptables ainda funciona?**
R: No Proxmox VE 9, `proxmox-firewall` (nftables) é onde a equipa investe (regras forward, VNets SDN, etc.). O backend clássico `pve-firewall` (iptables) continua disponível. A wiki descreve o backend nftables como *tech preview* e **não recomendada para produção** — em homelab, com backups e consciência do risco, é uma escolha comum.

**P: Posso usar este guia em outro servidor Debian, sem Proxmox?**
R: Fases 0 (parcial), 1–4, 9 e 10 funcionam em qualquer Debian 13. Fases 5, 7 e 8 envolvem features específicas do Proxmox.

**P: Este guia substitui o plano “Linux Foundation Lab” (Debian bare metal)?**
R: **Evolui** a partir da mesma filosofia (fundamentos, segurança, GPG, redes, sem port forwarding), mas o **caminho actual** é **Proxmox no mini PC**, não Debian minimal como único SO no metal. Comandos de estudo e UFW/`fail2ban` **dentro de VMs** continuam no cheat sheet [docs/linux-comandos-fundamentos.md](docs/linux-comandos-fundamentos.md); o **host** segue as fases Fortaleza (firewall PVE, CrowdSec, etc.). Ver também [docs/roadmap-hardware.md](docs/roadmap-hardware.md).

**P: E se eu errar e me trancar fora?**
R: Console físico do Mini PC sempre funciona. Apêndice H tem o plano de recuperação completo.

**P: Preciso pagar por algo?**
R: Não. Tailscale (até 100 dispositivos), ShellHub Cloud Community, CrowdSec, Proxmox Community — todos gratuitos.

**P: Quanto de RAM isso tudo gasta?**
R: ~600 MB extras com tudo rodando (Proxmox + Tailscale CT + ShellHub CT + CrowdSec + bouncer). Sobra ~14-15 GB para seus labs.

**P: Comandos e versões deste guia vão desatualizar com o tempo?**
R: **Sim.** Nomes de pacotes, menus da GUI e detalhes de `nft`/`sshd` mudam entre *point releases*. Antes de cada `dist-upgrade` ou mudança grande, confirme com `pveversion`, [wiki Proxmox](https://pve.proxmox.com/wiki/Main_Page), [release notes / anúncios](https://forum.proxmox.com/forums/announcements.11/) e a [matriz de auditoria](docs/audit-matrix.md). A **ordem das fases** e a lógica (NTP antes de 2FA, backup antes de firewall) permanecem válidas.

**P: Posso usar ProxMenux para facilitar a administração?**
R: **Sim, como opcional.** O [ProxMenux](https://proxmenux.com/) é um menu interactivo para tarefas no host e em guests — vê a secção no início do guia e a [documentação](https://proxmenux.com/docs/introduction). Trata-o como **terceiro**: revê código e guias de instalação antes de executar; não invalida a ordem nem a segurança das fases Fortaleza.

**P: E se eu perder o celular do 2FA?**
R: Use os códigos de recuperação salvos no Bitwarden. Em última instância, acesse pelo console físico como root e edite `/etc/pam.d/sshd`.

**P: O Proxmox 9.x atualiza entre minor (ex. 9.1 → 9.2) sem quebrar isso?**
R: Em geral, sim: configurações em `sshd_config.d/`, snapshots e regras de firewall na GUI tendem a ser preservadas em *point releases*. Sempre leia as [release notes](https://forum.proxmox.com/forums/announcements.11/) e faça backup de `/etc/pve` antes de subir major/minor.

**P: Devo usar Wi-Fi no Mini PC?**
R: NÃO. Sempre cabo Ethernet. Wi-Fi adiciona instabilidade e complexidade desnecessária.

**P: O `AllowTcpForwarding no` no host impede o meu irmão de usar ShellHub ou `ssh -L` para debug?**
R: **ShellHub (CT do irmão):** não depende de `AllowTcpForwarding` no **sshd** do host Proxmox — o agente fala com a cloud ShellHub por fora do teu endurecimento SSH do PVE. **`ssh -L` / `-D` para o host PVE:** sim, com `AllowTcpForwarding no` o OpenSSH desativa esse encaminhamento; se precisares, ajusta só no drop-in (com consciência do risco) ou faz o túnel **a partir de uma VM/CT** de laboratório, não do host endurecido.

**P: O NTP é mesmo tão importante?**
R: SIM. Sem NTP sincronizado, o 2FA TOTP simplesmente não funciona — os códigos do servidor não batem com os do celular.

**P: Posso usar este guia em produção (empresa)?**
R: Os fundamentos sim. Mas para produção, considere também: backups offsite obrigatórios, monitoring centralizado (Prometheus + Grafana), alertas, gestão de patches mais rigorosa, e Proxmox Subscription Enterprise (suporte oficial).

---

# 📚 Apêndice F — Glossário Expandido

Veja a secção **Glossário completo** no topo do documento (âncora interna `#glossario-completo`), ou o atalho [docs/glossario.md](docs/glossario.md).

---

# 🔐 Apêndice G — O Que Guardar no Bitwarden

Crie a pasta "Fortaleza Proxmox" com:

| # | Item | Onde aparece no guia |
|---|------|----------------------|
| 1 | Senha root Proxmox | Instalação inicial |
| 2 | Senha usuário `renato` | Fase 1 |
| 3 | Passphrase chave SSH `chave_fortaleza` | Fase 2 |
| 4 | Conteúdo da chave privada `chave_fortaleza` | Fase 2 (backup) |
| 5 | 2FA SSH renato — chave secreta TOTP | Fase 3 |
| 6 | 2FA SSH renato — 5 códigos de recuperação | Fase 3 |
| 7 | 2FA painel renato@pam — chave secreta TOTP | Fase 6 |
| 8 | 2FA painel renato@pam — recovery keys | Fase 6 |
| 9 | Senha root CT 100 (vpn-tailscale) | Fase 5 |
| 10 | Conta Tailscale (Google/GitHub OAuth) | Fase 5 |
| 11 | Senha root CT 200 (lab-irmao-gpg) | Fase 8 |
| 12 | Senha usuário `irmao` no CT 200 | Fase 8 |
| 13 | Conta ShellHub Cloud (email/senha) | Fase 8 |
| 14 | CrowdSec Console enroll token (se usar) | Fase 4 |

**Bônus:** imprima os códigos de recuperação 2FA e guarde **fisicamente** em local seguro (cofre, gaveta trancada). Se Bitwarden cair, você ainda tem como entrar.

---

# 🛟 Apêndice H — Plano de Recuperação de Desastre

Já está documentado em `~/fortaleza-lab/recuperacao.md` (criado na Fase 10).

Resumo:

| Cenário | Primeiro passo |
|---------|----------------|
| Não consigo logar SSH | Console físico do Mini PC |
| Perdi celular do 2FA | Códigos de recuperação no Bitwarden |
| Mini PC quebrou | Reinstala PVE, restaura backup de `/etc/pve` |
| Me bani no CrowdSec | Console físico → `cscli decisions delete --ip MEU_IP` |
| Firewall me trancou | Console → `pve-firewall stop` |

---

# 🔗 Apêndice I — Fontes oficiais por fase

Este guia é **pedagógico** e foi confrontado com documentação oficial em 2026-05-12 (detalhe em [docs/audit-matrix.md](docs/audit-matrix.md)). Use sempre as fontes abaixo como verdade final quando houver ambiguidade.

### Fase 0 — SO, rede, APT

| Tópico | Fonte |
|--------|--------|
| Repositórios deb822, enterprise, no-subscription, Ceph, chave GPG Trixie | [Package Repositories](https://pve.proxmox.com/wiki/Package_Repositories) |
| Instalação PVE em Debian 13 | [Install Proxmox VE on Debian 13 Trixie](https://pve.proxmox.com/wiki/Install_Proxmox_VE_on_Debian_13_Trixie) |
| Debian 13 “Trixie” | [Debian Releases — Trixie](https://www.debian.org/releases/trixie/) |
| NTP / relógio | [timedatectl](https://www.freedesktop.org/software/systemd/man/systemd.time.html) (systemd); prática TOTP alinhada a [RFC 6238](https://www.rfc-editor.org/rfc/rfc6238) |

### Fases 1–3 — utilizador, SSH, 2FA

| Tópico | Fonte |
|--------|--------|
| OpenSSH 10 (ex.: remoção DSA) | [OpenSSH 10.0 release notes](https://www.openssh.com/txt/release-10.0) |
| Manual `sshd_config` / `UsePAM` / `AuthenticationMethods` | `man sshd_config` na sua instalação Debian |
| PAM / Google Authenticator | [Debian Wiki — Two-factor authentication with SSH](https://wiki.debian.org/Two-factor_authentication_with_SSH) (referência geral; pacote `libpam-google-authenticator`) |

### Fase 4 — CrowdSec

| Tópico | Fonte |
|--------|--------|
| Instalação Linux (repositório + `apt install`) | [Install on Linux](https://docs.crowdsec.net/u/getting_started/installation/linux/) |
| Bouncers / firewall | [Firewall bouncer](https://docs.crowdsec.net/u/bouncers/firewall) |

### Fase 5 — LXC + Tailscale

| Tópico | Fonte |
|--------|--------|
| Tailscale em LXC não privilegiado | [Tailscale in LXC containers](https://tailscale.com/docs/features/containers/lxc/lxc-unprivileged) |
| `pct` / containers | [Proxmox VE Administration Guide — pct](https://pve.proxmox.com/pve-docs/chapter-pct.html) |

### Fase 6 — utilizador e TFA na GUI

| Tópico | Fonte |
|--------|--------|
| Permissões e utilizadores | [User Management](https://pve.proxmox.com/wiki/User_Management) (wiki PVE) |

### Fase 7 — firewall

| Tópico | Fonte |
|--------|--------|
| Firewall (incl. nftables, `proxmox-firewall`, ficheiros em `/etc/pve/firewall/`) | [Firewall](https://pve.proxmox.com/wiki/Firewall) |

### Fases 8–10 — ShellHub, manutenção, backups

| Tópico | Fonte |
|--------|--------|
| ShellHub | [ShellHub Documentation](https://docs.shellhub.io/) |
| Atualizações não interactivas Debian | [UnattendedUpgrades](https://wiki.debian.org/UnattendedUpgrades) |
| Política de reinício após upgrades (`needrestart`) | [needrestart (GitHub)](https://github.com/liske/needrestart) — ler `needrestart.conf` antes de alterar `$nrconf{restart}` |
| Certificados TLS / GUI após restore ou novo nó | [Certificate Management](https://pve.proxmox.com/wiki/Certificate_Management) |

### Anúncios de versão Proxmox

- [Fórum — anúncios / release notes](https://forum.proxmox.com/forums/announcements.11/) (ex.: tópicos VE 9.1, 9.2, …)

### Ferramentas de terceiros (opcional, não oficiais PVE)

| Ferramenta | Nota |
|-------------|------|
| [ProxMenux](https://proxmenux.com/) | Menu shell para administração; [intro](https://proxmenux.com/docs/introduction). Verificar fonte antes de instalar. |
| [linux-comandos-fundamentos.md](docs/linux-comandos-fundamentos.md) | Cheat sheet Linux (VMs de estudo); ver aviso de âmbito no cabeçalho. |
| [roadmap-hardware.md](docs/roadmap-hardware.md) | Evolução prevista do hardware do lab. |

---

*Repositório: documentação do projeto Fortaleza Proxmox (homelab).*
*Última revisão cruzada com fontes oficiais: 2026-05-12 — ver [docs/audit-matrix.md](docs/audit-matrix.md).*
*Dúvidas, correções ou sugestões? Abra uma Issue no GitHub.*

**Próximo passo:** Quando estiver pronto para executar no laboratório, siga **uma fase de cada vez**, com backup e duas sessões SSH nas alterações críticas. Comece pela **Fase 0**.
