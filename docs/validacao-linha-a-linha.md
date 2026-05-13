# Validação linha-a-linha — Fortaleza Proxmox

Este arquivo registra a **revisão manual** do conteúdo, **por partes**, com calma. Não substitui a [matriz de auditoria](audit-matrix.md) (fontes oficiais por fase).

**Como usar:** cada parte indica o intervalo de linhas do arquivo [fortaleza-proxmox-v5.0.md](../fortaleza-proxmox-v5.0.md) (ou outro). O estado **Concluída** significa leitura + notas; **Correções** lista alterações já aplicadas no repo.

---

## Convenções

| Estado | Significado |
|--------|-------------|
| Concluída | Texto relido; problemas anotados ou "nenhum bloqueante". |
| Pendente | Ainda não revisto nesta sessão. |
| Correção aplicada | Commit / diff associado (referência breve no texto da parte). |

---

## Parte 1 — Linhas 1–305 (cabeçalho, Dicas, Changelog, Antes de Começar, início Fase 0 até fim §0.1 NTP)

**Arquivo:** `fortaleza-proxmox-v5.0.md`  
**Estado:** Concluída (2026-05-12)

### Verificações feitas

- Links relativos `docs/audit-matrix.md`, `docs/mapa-do-curso.md`, `docs/README.md`, `docs/revisao-geral-projeto.md`, `docs/CHANGELOG-repositorio.md` — coerentes com a árvore do repo.
- Seção **Dicas para o aluno** — coerente com a estrutura anunciada em "Como usar este guia".
- **Pré-requisitos** — checklist alinhada ao fluxo (PVE 9, web, SSH root, físico, Bitwarden, TOTP, cabo).
- **§0.1 Timezone/NTP** — `timedatectl list-timezones | grep -i sao_paulo` e `set-timezone` corretos; bloco de saída esperada é ilustrativo (data de exemplo); nota de `systemd-timesyncd` adequada a Debian/PVE típico.

### Problemas encontrados e correções

| Linha (aprox.) | Problema | Ação |
|----------------|----------|------|
| Diagrama (~L144) | Texto `← "Some" da internet` — erro tipográfico / inglês ambíguo. | Substituído por texto claro em PT: tráfego da internet barrado (DROP). |
| ~L193 | `~/lab-diario.md` inconsistente com o resto do guia (`~/fortaleza-lab/diario.md` a partir da Fase 1). | Unificado com explicação: pasta na Fase 1 ou `mkdir` antecipado. |

### Observações não bloqueantes (P2)

- ✅ **PT-BR puro concluído** (2026-05-13) — mistura você/tu/perceberes eliminada em todo o guia.
- Diagrama: "Roteador da sua casa" com espaços duplos antes do `│` — cosmético.
- **§0.2 em diante:** coberto na **Parte 2** (ver abaixo).

---

## Parte 2 — Linhas 306–647 (Fase 0: §0.2 IP fixo até checklist e nota ZFS)

**Arquivo:** `fortaleza-proxmox-v5.0.md`  
**Estado:** Concluída (2026-05-12)

> **Nota:** o intervalo foi alargado em relação ao rascunho inicial (306–620) para incluir o **fecho completo da Fase 0** (checklist, lembrete do dataset), evitando cortar a §0.8 a meio.

### Verificações feitas

- **§0.2** — `ifreload` / `ifupdown2`, aviso de `restart networking`, exemplos `vmbr0` / `enp1s0` coerentes com o guia; lembrete de IP de exemplo.
- **§0.3** — `/etc/hosts` e `hostname -i` alinhados à [wiki](https://pve.proxmox.com/wiki/Network_Configuration) e quebras típicas de cluster.
- **§0.4** — deb822, painel vs `Enabled: no`, aviso contra `sed` em massa; arquivo `pve-no-subscription.sources` com `Suites: trixie` coerente com PVE 9.
- **§0.5** — risco *supply chain* explícito; URL `community-scripts/ProxmoxVE` como referência auditável.
- **§0.6** — `apt full-upgrade` como root; `needrestart -k -r i` com comentário sobre o significado de `-k`.
- **§0.7** — `tar czf` de `/etc/pve` com data no nome; verificação `ls`.
- **§0.8** — snapshot ZFS com aviso de dataset; alternativa LVM-Thin.
- **Checklist Fase 0** — itens alinhados aos passos anteriores.

### Problemas encontrados e correções

| Seção | Problema | Ação |
|-------|----------|------|
| §0.3 | `ping -c 1 pve` assume hostname `pve`; quem tem `mini` ou outro nome falha o teste. | `ping -c 1 "$(hostname)"` + comentário; comandos `hostname` / `cat` com texto que exige consistência nome/IP. |
| Checklist Fase 0 | Item ZFS obrigatório mesmo sem pool ZFS. | Texto **ou N/A** com ênfase no backup `tar` quando não há ZFS. |

### Observações P2 (não corrigidas agora)

- ✅ **PT-BR puro concluído** (2026-05-13) — mistura você/tu/ativo eliminada em todo o guia.
- `wget` da chave GPG a partir de `enterprise.proxmox.com` na seção "Se deu errado" — funcional para obter keyring; quem bloqueia DNS a enterprise pode precisar de espelho (caso raro em homelab).

---

## Parte 3 — Linhas 648–1088 (Fases 1 a 3 — fim da documentação da Fase 3)

**Arquivo:** `fortaleza-proxmox-v5.0.md`  
**Estado:** Concluída (2026-05-12)

> **Nota:** o intervalo final foi alargado em relação ao rascunho (648–1050) para incluir o **§3.5 completo** e o bloco **Documente** da Fase 3, terminando antes da Fase 4.

### Verificações feitas

- **Fase 1** — `adduser` / `usermod -aG sudo`; verificação em segundo terminal; diário em `~/fortaleza-lab/`; troubleshooting `sudoers`.
- **Fase 2** — chave no PC local, `ssh-copy-id`, `~/.ssh/config`, drop-in `99-hardening.conf` alinhado a OpenSSH 10 / Debian 13; `sshd -T` para validar.
- **Fase 3** — PAM `nullok` → remoção; `KbdInteractiveAuthentication`; bloco **PARA AQUI** + `reload||restart`; instalação `libpam-google-authenticator`; snapshot com `sudo` explícito para sessão `renato`.

### Problemas encontrados e correções

| Seção | Problema | Ação |
|-------|----------|------|
| §2.5 | Aviso "serviço `ssh` não `sshd`" vinha **depois** do `systemctl restart ssh` — fácil de não ler a tempo. | Aviso movido para **antes** do `restart`. |
| §3 **Verifique** | Assume sempre `ssh fortaleza`; quem saltou o §2.4 fica preso. | Alternativa `ssh -i … renato@IP` no bloco e no passo 4 do checklist TOTP. |
| Snapshots Fase 1–3 | Fase 1–2: `zfs` sem `sudo` (root implícito); Fase 3: `sudo zfs` — ambíguo para o novato. | Comentários `# Como root` nos snapshots 1 e 2; Fase 3: nota "como renato (sudo)" + dataset Fase 0.8. |
| §3.5 | Só `restart ssh` após remover `nullok`; §3.4 já ensina `reload` preferencial. | `sshd -t` + `reload \|\| restart` + lembrete da unidade `ssh`. |

### Observações P2

- ✅ **PT-BR puro concluído** (2026-05-13) — mistura você/tu/ativo eliminada em todo o guia.
- Linha de exemplo `(renato@192.168.1.100)` na saída esperada do TOTP — IP de modelo (já coberto nas Dicas).

---

## Parte 4 — Linhas 1089–1402 (Fases 4 e 5 — CrowdSec e Tailscale em LXC)

**Arquivo:** `fortaleza-proxmox-v5.0.md`  
**Estado:** Concluída (2026-05-12)

> **Nota:** o intervalo **não** inclui a Fase 6 (2FA no painel): termina no `---` imediatamente antes de `# FASE 6`, para coincidir com o título «CrowdSec / Tailscale».

### Verificações feitas

- **Fase 4** — `curl|sh` com remissão a instalação manual; pacote `crowdsec-firewall-bouncer-nftables` e nota iptables vs nft; whitelist com CIDR local + Tailscale `100.64.0.0/10`; `systemctl` em `crowdsec` e bouncer; comandos `cscli` e `nft`; troubleshooting `cscli decisions`.
- **Fase 5** — CT 100, template Debian 13, rede estática; `pct set` (`keyctl`, `nesting`, `/dev/net/tun`); pings de pré-checagem; `tailscale up` + subnet + `sysctl` forwarding; aprovação de rotas no admin; verificação `tailscale0`; doc CrowdSec + PVE na Fase 7 referenciada onde relevante.

### Problemas encontrados e correções

| Seção | Problema | Ação |
|-------|----------|------|
| Snapshots Fase 4 e 5 | Sem contexto de *quem* corre nem remissão ao dataset da §0.8 (inconsistente com Fases 1–3). | Comentários no bloco: host Proxmox, dataset §0.8, `renato` com `sudo`. |
| §4.2 | O nome da unidade systemd do bouncer não era óbvio para quem só vê o nome do pacote `…-nftables`. | Comentário: em Debian a unidade costuma ser `crowdsec-firewall-bouncer`. |
| §5.4 | Mensagem de erro do `ping tailscale.com` misturava ICMP bloqueado com falha de DNS. | Texto separado + `curl -fsSI` opcional se ICMP falhar com rede OK. |
| §5 **Documente** | «IP Tailscale do PVE» — o comando obtém o IP do **CT 100**, não do hipervisor. | Texto e comando: IPv4 do CT com `tailscale ip -4`. |

### Observações P2

- ✅ **PT-BR puro concluído** (2026-05-13) — mistura você/tu eliminada em todo o guia.
- Tabela do CT (IP `192.168.1.110`) e subnet `192.168.1.0/24` são exemplos; já alinhados às Dicas em outras fases.

---

## Parte 5 — Linhas 1404–1761 (Fases 6 a 8 — painel 2FA, proxmox-firewall, ShellHub)

**Arquivo:** `fortaleza-proxmox-v5.0.md`  
**Estado:** Concluída (2026-05-12)

> **Nota:** termina no `---` imediatamente antes da **Fase 9**.

### Verificações feitas

- **Fase 6** — usuário `renato@pam`, permissão Administrator, TOTP + recovery keys; remissão a IP de exemplo e acesso via Tailscale/LAN; alinhamento com realms `pam` vs `pve`.
- **Fase 7** — snapshot + `tar` de `/etc/pve`; instalação `proxmox-firewall`; quatro ACCEPT antes de DROP; opções Datacenter e nó; backend nftables e *tech preview*; `systemctl` / `nft` / `iptables` PVEFW; CrowdSec + coexistência nft; testes de conectividade e fecho de port forwarding; troubleshooting com paragem de serviços e `cluster.fw`.
- **Fase 8** — CT 200, `nesting`/`keyctl`, Docker `get.docker.com`, ShellHub cloud, fluxo SSH do irmão; exercício GPG com `gpg --full-generate-key`.

### Problemas encontrados e correções

| Seção | Problema | Ação |
|-------|----------|------|
| Fase 6 | Sem snapshot ZFS antes de alterações sensíveis ao acesso web — inconsistente com fases vizinhas. | Bloco **📸 Snapshot (recomendado)** com `snap-pre-fase6` + comentário §0.8 / `sudo`. |
| Fase 7 | Snapshot `zfs` sem contexto de dataset/usuário; teste SSH só com `ssh fortaleza`. | Comentário no bloco ZFS; testes com fallback `ssh -i … renato@IP` e nota para trocar IP. |
| Fase 7 **Se deu errado** | «Edite `/etc/pve/firewall/cluster.fw`» sem indicar privilégios de root. | Texto: `sudo nano` (ou equivalente) como root. |
| Fase 8 | Objetivo e texto falavam em **VM** mas o guia cria **LXC** (`pct`, CT 200). | Wording: container/LXC/CT; comentário no snapshot Fase 8; §8.6 «cai no CT»; §8.7 comentário GnuPG e menus variáveis. |

### Observações P2

- ✅ **PT-BR puro concluído** (2026-05-13) — exercício GPG e mistura você/tu eliminados em todo o guia.

---

## Parte 6 — Linhas 1763–2079 (Fases 9 e 10 — manutenção automática e documentação viva)

**Arquivo:** `fortaleza-proxmox-v5.0.md`  
**Estado:** Concluída (2026-05-12)

> **Nota:** termina no `---` imediatamente antes do **Apêndice A**.

### Verificações feitas

- **Fase 9** — `unattended-upgrades`, `needrestart`, `apt-listchanges`; seção 9.1b (modos `l`/`i`/`a`, aviso contra `sed` cego); ferramentas `htop`/`iotop`/etc.; repetição nos CTs 100/200.
- **Fase 10** — README heredoc, diário, script `backup-fortaleza.sh`, `tar tzf`, `crontab`, `rsync` off-site, runbook `recuperacao.md`, Git opcional.

### Problemas encontrados e correções

| Seção | Problema | Ação |
|-------|----------|------|
| §9.1 | `grep "Allowed origins"` não bate com a chave real `Unattended-Upgrade::Allowed-Origins` do `50unattended-upgrades`. | `grep -A 12 'Unattended-Upgrade::Allowed-Origins'` + nota sobre `Origins-Pattern` / wiki. |
| §9.1b | Frase com `` `a` `` e aspas misturadas — risco de renderização confusa. | Reformulação sem crases aninhadas no modo **a**. |
| Fases 9–10 | Sem snapshot ZFS antes de automatizar upgrades / cron de backups — desalinhado das fases 4–8. | Blocos **📸 Snapshot** `snap-pre-fase9` e `snap-pre-fase10` + itens no Apêndice A. |
| §9.3 | Quem entra no CT sem `root` pode não perceber o contexto. | Comentário: console como root ou `sudo -i`. |
| §10.4 | `rsync fortaleza:` assume `Host fortaleza` no PC sem o dizer. | Comentário no script: Host §2.4 ou `renato@IP`. |
| Runbook §10.5 | «restart ssh» genérico; cenário 3 sem `sudo` no `tar`; cenário 5 sem `sudo` / editor. | `systemctl restart ssh` + unidade `ssh`; `sudo tar`; `sudo` nos stops e `sudo nano` + remissão wiki Firewall. |

### Observações P2

- O `grep` das origens ainda pode variar entre versões Debian/Proxmox — o aluno pode precisar de abrir o arquivo à mão.
- ✅ **PT-BR puro concluído** (2026-05-13) — mistura você/tu eliminada em todo o guia.

---

## Parte 7 — Linhas 2081–2404 (Apêndices A–I, FAQ, fontes, rodapé)

**Arquivo:** `fortaleza-proxmox-v5.0.md`  
**Estado:** Concluída (2026-05-12)

> **Nota:** o número da última linha pode crescer com edições futuras; o bloco cobre desde `# Apêndice A` até ao parágrafo **Próximo passo** no fim do arquivo.

### Verificações feitas

- **Apêndice A** — checklist por fase alinhada ao corpo do guia (incl. snapshots fases 6–10).
- **Apêndice B** — tabela de comandos de rotina; escapes `\|` nas células para tabelas Markdown.
- **Apêndices C–D** — convenções de IDs, roadmap opcional.
- **Apêndice E (FAQ)** — nftables/tech preview, escopo Debian vs Proxmox, ProxMenux, 2FA, ShellHub vs `AllowTcpForwarding`, NTP/TOTP.
- **Apêndices F–I** — glossário, Bitwarden, resumo recuperação, fontes oficiais e links internos `docs/`.

### Problemas encontrados e correções

| Seção | Problema | Ação |
|-------|----------|------|
| FAQ (Ap. E) | «Apêndice H tem o plano **completo**» — o detalhe está na Fase 10 (`recuperacao.md`); H é resumo. | Texto corrigido: arquivo na Fase 10 + H como resumo. |
| FAQ (Ap. E) | Perda 2FA: editar `sshd` PAM sem mencionar `sudo`/editor. | `sudo nano` explícito. |
| Ap. H (tabela) | `cscli` e `pve-firewall` sem `sudo` (inconsistente com Fases 4 e 7). | Prefixo `sudo` nos exemplos. |
| Ap. B (tabela) | `apt list --upgradable` sem `sudo` no host onde `renato` é típico. | `sudo apt list …` |
| Ap. B (tabela) | `systemctl --failed` como usuário pode omitir falhas de sistema. | `sudo systemctl --failed` |
| Ap. A (checklist) | Snapshots ZFS das fases 6–8 no guia principal mas não refletidos no checklist. | Linhas de verificação `snap-pre-fase6` … `snap-pre-fase8` + tar fase 7. |

### Observações P2

- Estimativa de RAM no FAQ (~600 MB) é ordem de grandeza — depende de versões e serviços extra.
- Tabela Ap. B: alguns comandos assumem sessão no **host** (não no CT); não está explicitado em cada linha.

---

## Outros arquivos (validação separada)

| Arquivo | Estado |
|---------|--------|
| [README.md](../README.md) raiz | ✅ Concluído (2026-05-13) — reescrito para lançamento público; PT-BR puro. |
| [docs/mapa-do-curso.md](mapa-do-curso.md) | ✅ Concluído (2026-05-13) — PT-BR puro; apêndices A–N; Fases -1/10b/VM-01. |
| [docs/monitoramento-telegram-fortaleza-proxmox.md](monitoramento-telegram-fortaleza-proxmox.md) | ✅ Concluído (2026-05-13) — PT-BR puro. |
| [scripts/fortaleza-telegram-monitor.py](../scripts/fortaleza-telegram-monitor.py) | ✅ Concluído (2026-05-13) — PT-BR puro nas strings de saída. |

---

*Última atualização: Partes 1–7 + arquivos satélite — 2026-05-13. PT-BR puro em todo o repositório.*
