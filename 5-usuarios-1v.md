# Prática Guiada: Gerenciamento de Usuários e Grupos no Linux para a Expotec 2025 no IFRN Campus Macau

## Contextualização
Você é um administrador de sistemas do **IFRN Campus Macau**, configurando um servidor Linux para a **Expotec 2025**, um evento de tecnologia e inovação integrado à **Secitex** (Semana de Ciência, Tecnologia e Extensão) do IFRN. O Campus Macau gerencia uma **sala de servidores** para projetos de robótica, aplicativos móveis e multimídia. Você criará contas de usuário para estudantes e professores, configurará grupos para equipes, gerenciará permissões e auditará os acessos ao servidor, usando comandos de terminal e inspecionando `/etc/passwd`, `/etc/shadow`, `/etc/group`, e `/etc/gshadow`.

## Objetivos
- Criar e gerenciar contas de usuários e grupos.
- Configurar permissões e senhas.
- Adicionar usuários a grupos e alternar contas.
- Inspecionar arquivos de configuração.
- Simular administração real para a Expotec.

## Cenário
A Expotec 2025 tem três equipes:
1. **Robótica**: Robô autônomo.
2. **App**: Aplicativo para eventos do IFRN.
3. **Multimídia**: Vídeos e apresentações.

Cada equipe precisa de contas para membros (estudantes e professor orientador) e um grupo para permissões. Um grupo `professores` será criado para administradores. Você auditará os usuários e grupos após sua criação.

## Passos da Prática

### Passo 1: Configurando o Ambiente
Logado como `root` (ou com `sudo`), verifique privilégios.

**Tarefa**:
1. Abra um terminal.
2. Verifique quem você é:
   ```bash
   whoami
   ```
   **Saída esperada**: `root` (ou seu usuário com `sudo`).
3. Se não for `root`, alterne:
   ```bash
   su -
   ```
   Digite a senha do `root`.
4. Confirme o diretório:
   ```bash
   pwd
   ```
   **Saída esperada**: `/root`.

**Explicação**: `su -` inicia uma sessão `root` com privilégios totais. O `-` carrega o ambiente do `root`.

---

### Passo 2: Criando Grupos para Equipes
Crie grupos `robotica`, `app`, `multimidia`, e `professores` para gerenciar permissões.

**Tarefa**:
1. Crie `robotica` com GID 1100:
   ```bash
   addgroup --gid 1100 robotica
   ```
2. Crie `app` (GID 1101) e `multimidia` (GID 1102):
   ```bash
   addgroup --gid 1101 app
   addgroup --gid 1102 multimidia
   ```
3. Crie `professores` (sem GID específico):
   ```bash
   addgroup professores
   ```
4. Verifique em `/etc/group`:
   ```bash
   tail -4 /etc/group
   ```
   **Saída esperada** (GID de `professores` pode variar):
   ```
   robotica:x:1100:
   app:x:1101:
   multimidia:x:1102:
   professores:x:1103:
   ```

**Explicação**: `addgroup` cria grupos, atualizando `/etc/group`. O `--gid` define IDs únicos. `/etc/group` lista nome, senha (`x` para `/etc/gshadow`), GID, e membros.

### Passo 3: Criando Usuários e Adicionando aos Grupos
Crie contas para:
- **Robótica**: Estudantes `leticia`, `juan`; professor `prof_joao`.
- **App**: Estudantes `clara`, `juliana`.
- **Multimídia**: Estudantes `naiara`, `isaac`.

Use `adduser` sem grupo primário, criando automaticamente um diretório home. Adicione usuários aos grupos com `gpasswd` and defina o grupo primário com `usermod`. Senhas: **expotec2025** para estudantes, **ifrn2025** para `prof_joao`. Grupos não terão senhas nesta etapa (sem `newgrp`).

**Tarefa**:
1. Crie o usuário `leticia` com UID 1201:
   ```bash
   adduser --uid 1201 leticia
   ```
   - Senha: **expotec2025**.
   - **Explicação**: `adduser` cria `leticia`, seu diretório home (`/home/leticia`), e um grupo padrão (e.g., `leticia` ou `users`). Cada usuário tem um **UID** (ID único, aqui 1201) e um **GID padrão** (grupo primário, definido em `/etc/passwd`), que determina o grupo de novos arquivos. Adiciona entradas em `/etc/passwd` (dados do usuário) e `/etc/shadow` (senha criptografada).
2. Verifique o GID inicial de `leticia`:
   ```bash
   id leticia
   ```
   **Saída esperada** (exemplo):
   ```
   uid=1201(leticia) gid=1201(leticia) groups=1201(leticia)
   ```
   - **Explicação**: O `id` mostra o UID (1201), o GID primário (1201, grupo `leticia`), e grupos suplementares (atualmente apenas `leticia`). O GID primário é o grupo padrão criado por `adduser`.
3. Adicione `leticia` ao grupo `robotica`:
   ```bash
   gpasswd -a leticia robotica
   ```
   - **Explicação**: `gpasswd -a` adiciona `leticia` a `robotica` como grupo suplementar, atualizando a lista de membros em `/etc/group`. Sem senha para o grupo, pois não usamos `newgrp`.
4. Verifique o GID após `gpasswd`:
   ```bash
   id leticia
   ```
   **Saída esperada** (exemplo):
   ```
   uid=1201(leticia) gid=1201(leticia) groups=1201(leticia),1100(robotica)
   ```
   - **Explicação**: O GID primário permanece `leticia` (1201), mas `robotica` (1100) agora é um grupo suplementar. O `gpasswd -a` não altera o GID primário.
5. Defina `robotica` como grupo primário:
   ```bash
   usermod -g robotica leticia
   ```
   - **Explicação**: `usermod -g` altera o GID primário para `robotica` (1100), atualizando `/etc/passwd`. Isso garante que novos arquivos de `leticia` pertençam ao grupo `robotica`, essencial para permissões da equipe.
6. Verifique o GID final:
   ```bash
   id leticia
   ```
   **Saída esperada** (exemplo):
   ```
   uid=1201(leticia) gid=1100(robotica) groups=1100(robotica)
   ```
   - **Explicação**: O GID primário agora é `robotica` (1100), e `leticia` não está mais no grupo `leticia` como suplementar, pois `usermod -g` substitui o GID primário.
7. Verifique a criação de `leticia` em `/etc/passwd`:
   ```bash
   cat /etc/passwd | grep leticia
   ```
   **Saída esperada** (exemplo):
   ```
   leticia:x:1201:1100:leticia:/home/leticia:/bin/bash
   ```
   - **Explicação dos campos**:
     - **leticia**: Nome do usuário (login).
     - **x**: Placeholder para senha (em `/etc/shadow`).
     - **1201**: UID (ID único).
     - **1100**: GID (grupo primário, `robotica`).
     - **leticia**: GECOS (nome completo, editável).
     - **/home/leticia**: Diretório home.
     - **/bin/bash**: Shell padrão.

8. Crie `juan` com UID 1202:
   ```bash
   adduser --uid 1202 juan
   ```
   - Senha: **expotec2025**.
   - **Explicação**: Cria `juan` com home (`/home/juan`) e grupo padrão.
   ```bash
   gpasswd -a juan robotica
   usermod -g robotica juan
   ```
   - **Explicação**: Adiciona `juan` a `robotica` e define como grupo primário.

9. Crie `prof_joao` com UID 1200:
   ```bash
   adduser --uid 1200 prof_joao
   ```
   - Senha: **ifrn2025**.
   - **Explicação**: Cria `prof_joao` com home (`/home/prof_joao`).
   ```bash
   gpasswd -a prof_joao professores
   usermod -g professores prof_joao
   ```
   - **Explicação**: Adiciona `prof_joao` a `professores` e define como grupo primário.

10. Crie usuários da equipe `app`:
    ```bash
    adduser --uid 1203 clara
    ```
    - Senha: **expotec2025**.
    ```bash
    gpasswd -a clara app
    usermod -g app clara
    ```
    ```bash
    adduser --uid 1204 juliana
    ```
    - Senha: **expotec2025**.
    ```bash
    gpasswd -a juliana app
    usermod -g app juliana
    ```
    - **Explicação**: Cria `clara` e `juliana`, adiciona a `app`, define `app` como grupo primário.

11. Crie usuários da equipe `multimidia`:
    ```bash
    adduser --uid 1205 naiara
    ```
    - Senha: **expotec2025**.
    ```bash
    gpasswd -a naiara multimidia
    usermod -g multimidia naiara
    ```
    ```bash
    adduser --uid 1206 isaac
    ```
    - Senha: **expotec2025**.
    ```bash
    gpasswd -a isaac multimidia
    usermod -g multimidia isaac
    ```
    - **Explicação**: Cria `naiara` e `isaac`, adiciona a `multimidia`, define `multimidia` como grupo primário.

12. Verifique todas as contas em `/etc/passwd`:
    ```bash
    cat /etc/passwd | grep -E 'leticia|juan|prof_joao|clara|juliana|naiara|isaac'
    ```
    **Saída esperada** (exemplo):
    ```
    prof_joao:x:1200:1103:Professor Joao:/home/prof_joao:/bin/bash
    leticia:x:1201:1100:leticia:/home/leticia:/bin/bash
    juan:x:1202:1100:juan:/home/juan:/bin/bash
    clara:x:1203:1101:clara:/home/clara:/bin/bash
    juliana:x:1204:1101:juliana:/home/juliana:/bin/bash
    naiara:x:1205:1102:naiara:/home/naiara:/bin/bash
    isaac:x:1206:1102:isaac:/home/isaac:/bin/bash
    ```
    - **Explicação**: Confirma a criação de usuários com UIDs e GIDs corretos.

13. Verifique senhas em `/etc/shadow`:
    ```bash
    tail -7 /etc/shadow
    ```
    - **Explicação**: Garante que senhas (`expotec2025`, `ifrn2025`) estão criptografadas (`$6$`).

14. Verifique grupos em `/etc/group`:
    ```bash
    tail -4 /etc/group
    ```
    **Saída esperada** (exemplo):
    ```
    robotica:x:1100:leticia,juan
    app:x:1101:clara,juliana
    multimidia:x:1102:naiara,isaac
    professores:x:1103:prof_joao
    ```
    - **Explicação**: Confirma que usuários estão nos grupos corretos.

**Explicação (Resumo)**: Cada usuário tem um UID e um GID primário, definido em `/etc/passwd`. O `adduser` cria usuários com um grupo padrão, `gpasswd -a` adiciona a grupos suplementares, e `usermod -g` altera o GID primário, atualizando `/etc/passwd`, `/etc/shadow`, e `/etc/group`. A verificação de `leticia` com `id` e `/etc/passwd` demonstra essas mudanças.

**Desafio**:
- Compare `id leticia` antes e depois de `usermod -g robotica leticia`.
  - **Dica**: O GID primário muda de `leticia` (1201) para `robotica` (1100).

---

### Passo 4: Adicionando Usuários a Grupos Extras
A equipe `robotica` acessará arquivos da `multimidia`. O `prof_joao` será adicionado a `robotica`.

**Tarefa**:
1. Adicione `leticia` e `juan` a `multimidia`:
   ```bash
   gpasswd -a leticia multimidia
   gpasswd -a juan multimidia
   ```
2. Adicione `prof_joao` a `robotica`:
   ```bash
   gpasswd -a prof_joao robotica
   ```
3. Verifique com `id`:
   ```bash
   id leticia
   id juan
   id prof_joao
   ```
   **Saída esperada** (exemplo):
   ```
   uid=1201(leticia) gid=1100(robotica) groups=1100(robotica),1102(multimidia)
   uid=1202(juan) gid=1100(robotica) groups=1100(robotica),1102(multimidia)
   uid=1200(prof_joao) gid=1103(professores) groups=1103(professores),1100(robotica)
   ```
4. Confirme grupos de `leticia`:
   ```bash
   groups leticia
   ```
   **Saída esperada**: `robotica multimidia`.

**Explicação**: `gpasswd -a` adiciona a grupos suplementares, atualizando `/etc/group`. O `id` mostra UID, GID, e grupos; `groups` lista grupos.

**Desafio**:
- Verifique `multimidia` em `/etc/group`:
  ```bash
  grep multimidia /etc/group
  ```
  **Saída esperada**: `multimidia:x:1102:leticia,juan`.

---

### Passo 5: Gerenciando Senhas e Grupos
Configure uma senha para `professores` e teste `newgrp`. Altere a senha de `leticia`.

**Tarefa**:
1. Defina senha para `professores`:
   ```bash
   gpasswd professores
   ```
   - Senha: **ifrn2025**.
2. Teste `newgrp` como `leticia`:
   ```bash
   su - leticia
   newgrp professores
   ```
   - Senha: **ifrn2025**.
   - Verifique:
     ```bash
     id
     ```
   - Saia:
     ```bash
     exit
     exit
     ```
3. Altere a senha de `leticia` para **macau2025**:
   ```bash
   passwd leticia
   ```
4. Verifique `/etc/shadow`:
   ```bash
   grep leticia /etc/shadow
   ```

**Explicação**: `gpasswd` define senha em `/etc/gshadow`. O `newgrp` altera GID efetivo. O `passwd` atualiza `/etc/shadow`.

**Desafio**:
- Por que `/etc/gshadow` pode ter `!` ou vazio?
  - **Dica**: Grupo bloqueado ou sem senha.

---

### Passo 6: Configurando Acesso Administrativo com `sudo`
O `prof_joao` precisa de privilégios.

**Tarefa**:
1. Instale o pacote `sudo` (lembre-se de registrar-se na rede com `elinks`):
   ```bash
   apt update
   apt install sudo
   ```
1. Adicione `prof_joao` a `sudo`:
   ```bash
   gpasswd -a prof_joao sudo
   ```
2. Teste `sudo`:
   ```bash
   su - prof_joao
   sudo whoami
   ```
   - Senha: **ifrn2025**. **Saída esperada**: `root`.
3. Saia:
   ```bash
   exit
   ```

**Explicação**: O grupo `sudo` concede privilégios. O `sudo` executa como `root`.

---

### Passo 7: Auditoria de Usuários e Grupos
Audite contas e grupos.

**Tarefa**:
1. Liste usuários logados:
   ```bash
   users
   ```
2. Verifique usuário atual:
   ```bash
   logname
   ```
3. Liste grupos:
   ```bash
   getent group
   ```
4. Verifique `/etc/passwd` e `/etc/shadow`:
   ```bash
   pwck
   ```
5. Verifique `/etc/group` e `/etc/gshadow`:
   ```bash
   grpck
   ```

**Explicação**: `users` mostra logins, `logname` a sessão original, `getent group` lista grupos. `pwck` e `grpck` verificam inconsistências.

**Desafio**:
- Compare `id clara` e `groups clara`.
  - **Dica**: `id` mostra UID, GID, grupos suplementares.

---

**Parabéns!** Você gerenciou o servidor da Expotec 2025 com sucesso!
