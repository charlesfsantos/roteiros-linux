# Prática Guiada: Gerenciamento de Permissões de Arquivos e Diretórios no Linux para a Expotec 2025 no IFRN Campus Macau

## Contextualização
Você é administrador de sistemas do **IFRN Campus Macau**, configurando um servidor Linux para a **Expotec 2025**, integrada à **Secitex**. Contas de usuários (`prof_joao`, `leticia`, `juan`, `clara`, `juliana`, `naiara`, `isaac`) e grupos (`robotica`, `app`, `multimidia`, `professores`) foram criados. Esta prática configura a estrutura de diretórios em `/expotec2025` com permissões, donos, e grupos para as equipes de robótica, aplicativos móveis, e multimídia, garantindo que `prof_joao` tenha controle total como supervisor.

## Objetivos
- Criar estrutura de diretórios para a Expotec 2025.
- Configurar permissões de acesso, donos, e grupos.
- Aplicar permissões especiais (`setgid`) e `umask`.
- Auditar permissões para colaboração e segurança.

## Cenário
As equipes (`robotica`, `app`, `multimidia`) precisam de diretórios em `/expotec2025`:
- **Robótica**: `leticia` e `juan` criam/editam arquivos; `prof_joao` tem acesso total.
- **App**: `clara` e `juliana` compartilham arquivos; `prof_joao` supervisiona.
- **Multimídia**: `naiara` e `isaac` editam vídeos; `leticia` e `juan` têm leitura.
- **Professores**: `prof_joao` gerencia todos os projetos com privilégios administrativos.

Estrutura: `/expotec2025/{robotica,app,multimidia}`. `prof_joao` será o dono de todos os diretórios.

## Passos da Prática

### Passo 1: Configurando o Ambiente
Logado como `root` ou com `sudo`, crie a estrutura de diretórios.

**Tarefa**:
1. Confirme privilégios:
   ```bash
   whoami
   ```
   **Saída esperada**: `root` (ou use `sudo`).
2. Crie diretórios:
   ```bash
   mkdir -p /expotec2025/{robotica,app,multimidia}
   ```
3. Defina `prof_joao` como dono:
   ```bash
   chown prof_joao /expotec2025 /expotec2025/*
   ```
4. Verifique:
   ```bash
   ls -ld /expotec2025 /expotec2025/*
   ```
   **Saída esperada** (exemplo):
   ```
   drwxr-xr-x 5 prof_joao root       4096 Jun 11 2025 /expotec2025
   drwxr-xr-x 2 prof_joao root       4096 Jun 11 2025 /expotec2025/app
   drwxr-xr-x 2 prof_joao root       4096 Jun 11 2025 /expotec2025/multimidia
   drwxr-xr-x 2 prof_joao root       4096 Jun 11 2025 /expotec2025/robotica
   ```

**Explicação**: `mkdir -p` cria a estrutura desejada. `chown` define `prof_joao` como dono de todos os diretórios, alinhando com seu papel de supervisor.

**Pergunta**: Qual é o dono de `/expotec2025/robotica`?

---

### Passo 2: Configurando Grupos e Permissões
Configure grupos e permissões para colaboração.

**Tarefa**:
1. Altere grupos dos subdiretórios:
   ```bash
   chgrp robotica /expotec2025/robotica
   chgrp app /expotec2025/app
   chgrp multimidia /expotec2025/multimidia
   ```
2. Defina permissões:
   - `/expotec2025/robotica`: Dono (`prof_joao`) e grupo (`robotica`): `rwx`; outros: sem acesso.
   - `/expotec2025/app`: Dono (`prof_joao`) e grupo (`app`): `rwx`; outros: sem acesso.
   - `/expotec2025/multimidia`: Dono (`prof_joao`) e grupo (`multimidia`): `rwx`; outros: `rx`.
   ```bash
   chmod 770 /expotec2025/robotica
   chmod 770 /expotec2025/app
   chmod 775 /expotec2025/multimidia
   ```
3. Verifique:
   ```bash
   ls -ld /expotec2025/*
   ```
   **Saída esperada** (exemplo):
   ```
   drwxrwx--- 2 prof_joao app        4096 Jun 11 2025 /expotec2025/app
   drwxrwxr-x 2 prof_joao multimidia 4096 Jun 11 2025 /expotec2025/multimidia
   drwxrwx--- 2 prof_joao robotica   4096 Jun 11 2025 /expotec2025/robotica
   ```

**Explicação**: `chgrp` define grupos para colaboração. `770` (`rwxrwx---`) restringe acesso ao dono e grupo; `775` (`rwxrwxr-x`) permite leitura/execução para outros (`leticia` e `juan` em `multimidia`).

**Pergunta**: Por que `/expotec2025/multimidia` teria permissões `775`?

---

### Passo 3: Testando Acesso
Teste permissões para usuários.

**Tarefa**:
1. Como `leticia`, acesse `/expotec2025/robotica`:
   ```bash
   su - leticia
   cd /expotec2025/robotica
   touch projeto_robotica.txt
   ```
2. Verifique:
   ```bash
   ls -l /expotec2025/robotica
   ```
   **Saída esperada**:
   ```
   -rw-rw-r-- 1 leticia robotica 0 Jun 11 2025 projeto_robotica.txt
   ```
3. Como `clara`, tente acessar `/expotec2025/robotica`:
   ```bash
   exit
   su - clara
   cd /expotec2025/robotica
   ```
   **Saída esperada**: `Permission denied`.

**Explicação**: `leticia` (grupo `robotica`) tem acesso (`770`); `clara` (grupo `app`) não.

**Pergunta**: Por que `clara` não acessou `/expotec2025/robotica`?

---

### Passo 4: Permissões em Arquivos
Teste permissões em arquivos.

**Tarefa**:
1. Como `naiara`, crie um arquivo em `/expotec2025/multimidia`:
   ```bash
   exit
   su - naiara
   echo "Video promocional" > /expotec2025/multimidia/video.txt
   chmod 660 /expotec2025/multimidia/video.txt
   ```
2. Verifique:
   ```bash
   ls -l /expotec2025/multimidia/video.txt
   ```
   **Saída esperada**:
   ```
   -rw-rw---- 1 naiara multimidia 17 Jun 11 2025 video.txt
   ```
3. Como `leticia`, tente ler:
   ```bash
   exit
   su - leticia
   cat /expotec2025/multimidia/video.txt
   exit
   ```
   **Saída esperada**: `Permission denied`.

**Explicação**: `660` (`rw-rw----`) restringe acesso ao dono (`naiara`) e grupo (`multimidia`). `leticia` acessa o diretório (`775`), mas não o arquivo.

**Desafio**: Como `juliana`, crie `/expotec2025/app/config.txt` com permissões `640`. Verifique.

---

### Passo 5: Permissões Especiais (setgid)
Configure `setgid` para herança de grupo.

**Tarefa**:
1. Aplique `setgid` em `/expotec2025/robotica`:
   ```bash
   chmod g+s /expotec2025/robotica
   ```
2. Como `juan`, crie um arquivo:
   ```bash
   su - juan
   touch /expotec2025/robotica/novo_projeto.txt
   ```
3. Verifique:
   ```bash
   ls -ld /expotec2025/robotica /expotec2025/robotica/*
   exit
   ```
   **Saída esperada**:
   ```
   drwxrws--- 2 prof_joao robotica 4096 Jun 11 2025 robotica
   -rw-rw-r-- 1 juan robotica 0 Jun 11 2025 novo_projeto.txt
   ```

**Explicação**: `setgid` (`g+s`) faz novos arquivos herdarem o grupo `robotica`. O `s` aparece em `drwxrws---`.

**Pergunta**: Por que `novo_projeto.txt` pertence ao grupo `robotica`?

---

### Passo 6: Privilégios de Root e prof_joao
Teste privilégios.

**Tarefa**:
1. Como `prof_joao`, crie um arquivo:
   ```bash
   su - prof_joao
   touch /expotec2025/robotica/admin.txt
   exit
   ```
2. Como `leticia`, tente excluir:
   ```bash
   su - leticia
   rm /expotec2025/robotica/admin.txt
   exit
   ```
   **Saída esperada**: `Permission denied`.
3. Como `root`, crie outro arquivo:
   ```bash
   su -
   touch /expotec2025/robotica/root_file.txt
   exit
   ```
4. Como `prof_joao`, tente excluir:
   ```bash
   su - prof_joao
   rm /expotec2025/robotica/root_file.txt
   exit
   ```

**Explicação**: `prof_joao` (dono) tem `rwx` em `/expotec2025/robotica`, permitindo a criação e exclusão de arquivos no diretório. `leticia` (grupo `robotica`) não pode excluir arquivos que possuem outro dono. `root` ignora as permissões.

**Pergunta**: Por que `prof_joao` pode excluir `root_file.txt`?

---

### Passo 7: Ajustando Permissões
Ajuste permissões e donos.

**Tarefa**:
1. Mude o dono de `video.txt` para `isaac`:
   ```bash
   chown isaac /expotec2025/multimidia/video.txt
   ```
2. Adicione leitura para outros:
   ```bash
   chmod o+r /expotec2025/multimidia/video.txt
   ```
3. Verifique:
   ```bash
   ls -l /expotec2025/multimidia/video.txt
   ```
   **Saída esperada**:
   ```
   -rw-rw-r-- 1 isaac multimidia 17 Jun 11 2025 video.txt
   ```
4. Como `leticia`, leia:
   ```bash
   exit
   su - leticia
   cat /expotec2025/multimidia/video.txt
   exit
   ```

**Explicação**: `chown` altera o dono; `o+r` permite leitura para outros. `leticia` lê devido a `775` no diretório e `r` no arquivo.

**Tarefa**: Configure `/expotec2025/app/app.py` com permissões `750`.

---

### Passo 8: Permissões em modo Octal
Use modo octal.

**Tarefa**:
1. Como `clara`, crie um arquivo:
   ```bash
   su - clara
   touch /expotec2025/app/config.txt
   chmod 640 /expotec2025/app/config.txt
   ```
2. Verifique:
   ```bash
   ls -l /expotec2025/app/config.txt
   ```
   **Saída esperada**:
   ```
   -rw-r----- 1 clara app 0 Jun 11 2025 config.txt
   ```

**Explicação**: `640` = `rw-r-----` (dono: `rw`; grupo: `r`; outros: nenhum).

**Pergunta**: O que significa `750` em permissões?

---

### Passo 9: Configurando umask
Ajuste `umask` para novos arquivos.

**Tarefa**:
1. Como `juliana`, defina `umask`:
   ```bash
   exit
   su - juliana
   umask 027
   touch /expotec2025/app/teste.txt
   ```
2. Verifique:
   ```bash
   ls -l /expotec2025/app/teste.txt
   ```
   **Saída esperada**:
   ```
   -rw-r----- 1 juliana app 0 Jun 11 2025 teste.txt
   ```

**Explicação**: `umask 027` subtrai permissões de novos arquivos, resultando em `640` (`rw-r-----`).

**Pergunta**: Seguindo esta lógica, qual `umask` resulta em permissões `660` para novos arquivos?

---

