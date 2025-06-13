# Prática de Navegação no Sistema de Arquivos do Linux

**Objetivo**: Familiarizar-se com a hierarquia do sistema de arquivos do Linux, navegando por diretórios, explorando diretórios importantes do sistema e usando comandos comuns como `cd`, `ls`, `pwd` e `tree`.

**Pré-requisitos**:
- Acesso a um sistema Linux (por exemplo, Ubuntu, Fedora ou uma máquina virtual).
- Uma janela de terminal.
- Familiaridade básica com comandos como `cd`, `ls` e `pwd`.

## Passos do Exercício

1. **Abrir um Terminal e Verificar Sua Posição Inicial**
   - Abra seu terminal.
   - Execute `pwd` para exibir o diretório de trabalho atual. Provavelmente, você estará no diretório home (`/home/nome_do_usuario`).
   - **Tarefa**: Anote o caminho completo exibido pelo `pwd`.

2. **Navegar para o Diretório Raiz**
   - Use o comando:
     ```bash
     cd /
     ```
   - Execute `pwd` novamente para confirmar que você está em `/`.
   - **Tarefa**: Qual é a saída do `pwd` agora?

3. **Listar o Conteúdo do Diretório Raiz**
   - Execute:
     ```bash
     ls -l
     ```
   - Isso lista o conteúdo de `/` com detalhes (permissões, proprietário, etc.).

     **Diretórios Raiz Comuns**:
     | Diretório | Propósito |
     |-----------|-----------|
     | `/bin`    | Executáveis binários essenciais (por exemplo, `ls`, `cat`). |
     | `/etc`    | Arquivos de configuração do sistema. |
     | `/home`   | Diretórios home dos usuários. |
     | `/var`    | Dados variáveis, como logs ou arquivos temporários. |
     | `/usr`    | Software e utilitários instalados pelo usuário. |

4. **Explorar Diretórios Importantes**
   - Navegue para `/etc`:
     ```bash
     cd /etc
     ```
   - Liste seu conteúdo com `ls`. Procure pelos arquivos `passwd` e `fstab`.
   - **Tarefa**: Execute `ls | wc -l` para contar quantos arquivos e diretórios estão em `/etc`.
   - Retorne ao diretório raiz:
     ```bash
     cd /
     ```

5. **Navegar Usando Caminhos Absolutos e Relativos**
   - **Caminho Absoluto**: Navegue para `/usr/local` usando o caminho completo:
     ```bash
     cd /usr/local
     ```
     Execute `ls` para ver o que está lá.
   - **Caminho Relativo**: De `/usr/local`, navegue para `/usr` (um nível acima):
     ```bash
     cd ..
     ```
     Verifique com `pwd`.
   - **Pergunta**: Qual é o caminho completo do seu diretório atual após `cd ..`?

6. **Explorar o Diretório Home**
   - Navegue para o diretório home usando o atalho:
     ```bash
     cd ~
     ```
   - Alternativamente, use o caminho absoluto (por exemplo, `cd /home/nome_do_usuario`).
   - Execute `ls -a` para mostrar arquivos ocultos (aqueles que começam com `.`).

7. **Usar `tree` para Visualizar a Estrutura de Diretórios** (se `tree` estiver instalado)
   - Instale o `tree` se não estiver presente (`apt install tree`).
   - No diretório home, execute:
     ```bash
     tree -L 1
     ```
     Isso mostra a estrutura de diretórios em um nível de profundidade.
   - **Tarefa**: Execute `tree -L 2` a partir de `/` (como root, se necessário: `sudo tree -L 2 /`). Quantos diretórios estão diretamente sob `/`?

8. **Desafio: Navegação Aninhada**
   - Navegue para `/var/log`:
     ```bash
     cd /var/log
     ```
   - Liste os arquivos com `ls -l`. Procure por logs como `syslog` e/ou `auth.log`.
   - **Tarefa**: Use `less` para visualizar uma pequena parte de um arquivo de log (por exemplo, `less syslog`). Que tipo de informação está armazenada lá? Pressione `q` para sair do less.
   - Navegue de volta para o diretório home em um comando:
     ```bash
     cd ~
     ```

9. **Criar e Navegar em uma Estrutura de Diretórios Personalizada**
   - No diretório home, crie um diretório de prática:
     ```bash
     mkdir -p ~/pratica/dir1/dir2
     ```
   - Navegue para `dir2`:
     ```bash
     cd ~/pratica/dir1/dir2
     ```
   - Verifique com `pwd`.
   - **Tarefa**: Crie um arquivo em `dir2` chamado `teste.txt`:
     ```bash
     touch teste.txt
     ```
   - Navegue de volta para `~/pratica` usando um caminho relativo:
     ```bash
     cd ../..
     ```
   - Confirme com `ls` que `dir1` existe.
