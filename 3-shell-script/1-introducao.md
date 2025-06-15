# Prática Guiada de Shell Script no Linux Debian

Nesta atividade, você aprenderá os conceitos básicos de scripts em shell (bash), incluindo:

1. Sequenciamento de comandos
- O shell script é uma sequência de comandos escrita em um arquivo de texto que pode ser executada pelo interpretador de comandos (shell) de um sistema operacional, como o bash. Ele permite automatizar tarefas, executar operações repetitivas e gerenciar sistemas de forma eficiente, combinando comandos do terminal em scripts reutilizáveis.

2. Variáveis 

- Variáveis são elementos fundamentais em shell scripts, usadas para armazenar dados, como textos ou números, que podem ser manipulados durante a execução. 

    2.1 Variáveis locais e globais (shell e subshell)

    - As variáveis globais são definidas no escopo principal do script e acessíveis em qualquer parte dele, podendo até persistir no ambiente do terminal se o script for executado com o comando  `source`. 
    - Já as variáveis locais, declaradas com a palavra-chave local dentro de um subshell (um ambiente isolado criado por parênteses `()`), existem apenas nesse bloco, evitando conflitos com variáveis globais de mesmo nome. 
    - O propósito do subshell é isolar a execução de comandos, limitando o escopo de variáveis locais e protegendo o ambiente principal do script.

    2.2 Parâmetros (variáveis) posicionais

    - Variáveis posicionais (`$1`, `$2`, `$#`, `$@`) armazenam argumentos passados ao script na linha de comando, permitindo personalizar sua execução com base em entradas externas, como nomes ou valores fornecidos pelo usuário.

De modo a aprender os tópicos pretendidos, realize os passos a seguir:

## Passo 1: Criando o Diretório de Trabalho (certifique-se de estar logado como root)

1. **Objetivo**: Criar um diretório chamado `3-shell-script` para organizar os arquivos desta prática.
2. **Comandos**:
   - Abra o terminal.
   - Execute o comando abaixo para criar o diretório:
     ```bash
     mkdir 3-shell-script
     ```
     - `mkdir`: Cria um novo diretório.
     - `3-shell-script`: Nome do diretório.
   - Entre no diretório criado:
     ```bash
     cd 3-shell-script
     ```
     - `cd`: Muda o diretório atual.
     - `3-shell-script`: Diretório para o qual você está navegando.
3. **Verificação**:
   - Confirme que você está no diretório correto executando:
     ```bash
     pwd
     ```
     - `pwd`: Exibe o caminho completo do diretório atual. Você deve ver algo como `/root/3-shell-script`.


## Passo 2: Primeiro Script - Estrutura Básica com `source`

1. **Objetivo**: Criar um script simples que exibe uma mensagem e usa `source` para demonstrar variáveis globais no terminal.
2. **Tarefa**:
   - Crie um arquivo chamado `ola.sh` usando o Vim:
     ```bash
     vim ola.sh
     ```
   - No Vim, pressione `i` para entrar no modo de inserção e digite o seguinte código:
     ```bash
     #!/bin/bash
     MENSAGEM="Olá, este é meu primeiro script!"
     echo $MENSAGEM
     ```
   - Salve e saia do Vim:
     - Pressione `Esc`.
     - Digite `:wq` e pressione `Enter`.
3. **Explicação do Código**:
   - `#!/bin/bash`: Chamado de "shebang", indica que o script deve ser executado pelo interpretador bash.
   - `MENSAGEM="Olá, este é meu primeiro script!"`: Define uma variável global chamada `MENSAGEM`.
     - **Por que é global?** Variáveis definidas diretamente no script são globais, acessíveis no contexto do terminal executado.
   - `echo $MENSAGEM`: Exibe o valor da variável `MENSAGEM`.
5. **Executar o Script com `source`**:
   - Execute:
     ```bash
     source ola.sh
     ```
     - `source`: Executa o script no shell atual.
     - Alternativamente, você pode usar:
     ```bash
     . ola.sh
     ```
   - **Saída Esperada**:
     ```
     Olá, este é meu primeiro script!
     ```
 **Explicação: Por que usar `source`?**:
   - O comando `source` executa o script no shell atual, permitindo que variáveis globais, como `MENSAGEM`, sejam definidas no ambiente do terminal. Isso é útil nesta etapa inicial para visualizar diretamente no terminal que a variável persiste após a execução.

6. **Visualizar a Variável Global**:
   - Verifique se a variável `MENSAGEM` está definida no terminal:
     ```bash
     echo $MENSAGEM
     ```
     - **Saída Esperada**:
       ```
       Olá, este é meu primeiro script!
       ```
     - **Explicação**: Como `source` executa o script no shell atual, a variável global `MENSAGEM` permanece no ambiente do terminal.

## Passo 3: Variáveis Globais com `source`

1. **Objetivo**: Criar um script que usa uma variável global para armazenar um nome.
2. **Tarefa**:
   - Crie um arquivo chamado `nome.sh`:
     ```bash
     vim nome.sh
     ```
   - Insira o seguinte código:
     ```bash
     #!/bin/bash
     NOME="Maria"
     echo "Olá, $NOME!"
     echo "Bem-vindo, $NOME!"
     ```
   - Salve e saia (`:wq`).
3. **Explicação do Código**:
   - `NOME="Maria"`: Define uma variável global chamada `NOME`.
     - **Por que é global?** Como não está em um subshell ou marcada como `local`, esta é acessível em todo o script. Ao executá-lo com o comando `source`, a variável também será visível no ambiente do terminal.
   - `echo "Olá, $NOME!"`: Exibe uma mensagem usando o valor da variável `NOME`.
   - `echo "Bem-vindo, $NOME!"`: Usa a variável global novamente, mostrando sua persistência no script.
4. **Executar o Script com `source`**:
   - Execute:
     ```bash
     source nome.sh
     ```
   - **Saída Esperada**:
     ```
     Olá, Maria!
     Bem-vindo, Maria!
     ```
5. **Visualizar a Variável Global**:
   - Verifique se a variável `NOME` está definida no terminal. Digite:
     ```bash
     echo $NOME
     ```
     - **Saída Esperada**:
       ```
       Maria
       ```
     - **Explicação**: A variável `NOME` persiste no terminal porque `source` executa o script no mesmo ambiente do shell.

## Passo 4: Variáveis Locals em Subshells e Introdução ao `./`

1. **Objetivo**: Criar um script que demonstra variáveis locais em um subshell e variáveis globais, usando `./` para mostrar isolamento do ambiente do terminal.
2. **Tarefa**:
   - Crie um arquivo chamado `local.sh`:
     ```bash
     vim local.sh
     ```
   - Insira o seguinte código:
     ```bash
     #!/bin/bash
     NOME="João"
     echo "Fora do subshell: Olá, $NOME!"
     (
         NOME="Ana"
         echo "Dentro do subshell: Olá, $NOME!"
     )
     echo "Fora do subshell, após o subshell: Olá, $NOME!"
     ```
   - Salve e saia (`:wq`).
3. **Explicação do Código**:
   - `NOME="João"`: Define uma variável global chamada `NOME`.
     - **Por que é global?** Está definida diretamente no script e é acessível em todo o script. No entanto, ao executar com `./` essa variável não afetará o ambiente do terminal, como nos passos anteriores.
   - `echo "Fora do subshell: Olá, $NOME!"`: Exibe o valor da variável global antes de definir o subshell.
   - `(` e `)`: Delimita um subshell, criando um ambiente separado para execução de comandos.
   - `NOME="Ana"`: Define uma variável local dentro do subshell, acessível apenas nesse bloco.
     - **Por que é local?** A variável que contém "Ana" é restrito ao subshell, não afetando a variável global de mesmo nome fora dele.
   - `echo "Dentro do subshell: Olá, $NOME!"`: Exibe o valor da variável local dentro do subshell.
   - `echo "Fora do subshell, após o subshell: Olá, $NOME!"`: Exibe o valor da variável global após o subshell, mostrando que, apesar da variável local ter o mesmo nome, a variável global não é afetada.
4. **Por que usar `./`?**:
   - Diferentemente do `source`, que executa o script no shell atual e altera o ambiente do terminal, o `./` executa o script em um novo processo, isolando as variáveis globais do ambiente do terminal. Isso é preferido para a maioria dos scripts porque:
     - **Segurança**: Evita alterações indesejadas no ambiente do terminal, como sobrescrever variáveis existentes (por exemplo, `NOME` definida como `Maria`).
     **Tarefa**: execute `export` e verifique as variáveis já declaradas para o seu shell.
     - **Previsibilidade**: Garante que o script não deixe "resíduos" (como variáveis) no terminal após a execução.
     - **Boas práticas**: Scripts geralmente são projetados para serem independentes do ambiente do usuário, e `./` suporta essa abordagem.
   - Usar `./` a partir deste ponto ajuda a entender a diferença prática entre os dois métodos de execução.
5. **Tornar Executável e Executar com `./`**:
   - Torne o script executável:
     ```bash
     chmod +x local.sh
     ```
     - `chmod +x`: Adiciona permissão de execução ao arquivo.
   - Execute:
     ```bash
     ./local.sh
     ```
   - **Saída Esperada**:
     ```
     Fora do subshell: Olá, João!
     Dentro do subshell: Olá, Ana!
     Fora do subshell, após o subshell: Olá, João!
     ```
6. **Visualizar a Variável Global**:
   - Verifique se a variável `NOME` foi alterada no terminal:
     ```bash
     echo $NOME
     ```
     - **Saída Esperada**:
       ```
       Maria
       ```
     - **Explicação**: A variável `NOME` mantém o valor `Maria` (definido por `source nome.sh`), pois `./local.sh` executa em um processo separado e não afeta o ambiente do terminal.

## Passo 5: Variáveis Posicionais

1. **Objetivo**: Criar um script que usa variáveis posicionais para processar argumentos passados na linha de comando.
2. **Tarefa**:
   - Crie um arquivo chamado `argumentos.sh`:
     ```bash
     vim argumentos.sh
     ```
   - Insira o seguinte código:
     ```bash
     #!/bin/bash
     NOME="$1"
     echo "Primeiro argumento: $NOME"
     echo "Segundo argumento: $2"
     echo "Número total de argumentos: $#"
     echo "Todos os argumentos: $@"
     ```
   - Salve e saia (`:wq`).
3. **Explicação do Código**:
   - `NOME="$1"`: Define uma variável global `NOME` com o valor do primeiro argumento posicional.
   - `echo "Primeiro argumento: $NOME"`: Exibe o valor da variável `NOME` (primeiro argumento).
   - `echo "Segundo argumento: $2"`: Exibe o segundo argumento posicional diretamente no comando `echo`.
   - `echo "Número total de argumentos: $#"`: Exibe o número total de argumentos passados.
   - `echo "Todos os argumentos: $@"`: Exibe todos os argumentos como uma lista.
   - **O que são variáveis posicionais?** São variáveis automáticas (`$1`, `$2`, etc.) que armazenam os argumentos passados ao script na ordem em que são fornecidos.
4. **Tornar Executável e Executar com `./`**:
   - Torne o script executável:
     ```bash
     chmod +x argumentos.sh
     ```
   - Execute com argumentos:
     ```bash
     ./argumentos.sh Ana 25
     ```
   - **Saída Esperada**:
     ```
     Primeiro argumento: Ana
     Segundo argumento: 25
     Número total de argumentos: 2
     Todos os argumentos: Ana 25
     ```
5. **Visualizar a Variável Global**:
   - Verifique se a variável `NOME` foi alterada no terminal:
     ```bash
     echo $NOME
     ```
     - **Saída Esperada**:
       ```
       Maria
       ```
     - **Explicação**: A variável `NOME` definida no script não afeta o terminal, pois `./` executa em um processo separado.

## Passo 6: Script com Entrada de Usuário

1. **Objetivo**: Criar um script que solicita entrada do usuário e armazena em variáveis globais.
2. **Tarefa**:
   - Crie um arquivo chamado `interativo.sh`:
     ```bash
     vim interativo.sh
     ```
   - Insira o seguinte código:
     ```bash
     #!/bin/bash
     echo "Digite seu nome:"
     read NOME
     echo "Digite sua idade:"
     read IDADE
     MENSAGEM="Bem-vindo, $NOME! Você tem $IDADE anos."
     echo $MENSAGEM
     ```
   - Salve e saia (`:wq`).
3. **Explicação do Código**:
   - `echo "Digite seu nome:"`: Exibe uma mensagem pedindo o nome do usuário.
   - `read NOME`: Lê a entrada do usuário e armazena na variável global `NOME`.
   - `echo "Digite sua idade:"`: Exibe uma mensagem pedindo a idade.
   - `read IDADE`: Lê a entrada do usuário e armazena na variável global `IDADE`.
   - `MENSAGEM="Bem-vindo, $NOME! Você tem $IDADE anos."`: Cria uma variável global `MENSAGEM` com uma string formatada.
   - `echo $MENSAGEM`: Exibe o valor da variável `MENSAGEM`.
4. **Tornar Executável e Executar com `./`**:
   - Torne o script executável:
     ```bash
     chmod +x interativo.sh
     ```
   - Execute:
     ```bash
     ./interativo.sh
     ```
   - **Exemplo de Interação**:
     ```
     Digite seu nome:
     Carlos
     Digite sua idade:
     25
     Bem-vindo, Carlos! Você tem 25 anos.
     ```
5. **Visualizar a Variável Global**:
   - Verifique se a variável `NOME` foi alterada no terminal:
     ```bash
     echo $NOME
     ```
     - **Saída Esperada**:
       ```
       Maria
       ```
     - **Explicação**: As variáveis do script não afetam o terminal, pois `./` usa um processo separado.

## Passo 7: Tarefa Final - Script de Organização de Diretórios com Variáveis Posicionais

1. **Objetivo**: Criar um script que organiza vários de shell script (que foram criados durante esta prática) arquivos em um diretório fixo.
- Entrada: o script deve ser acionado com um argumento. Este argumento é o nome do diretório a ser criado.
- Comportamento e saída esperada: o script deve informar a criação do diretório. Após isso, deve mover todos os arquivos de extensão `.sh` para o diretório informado na entrada. Por fim, o script deve confirmar a remoção dos arquivos para o diretório. 
2. **Tarefa**:
   - Crie um arquivo chamado `organizador.sh`:
     ```bash
     vim organizador.sh
     ```
   - Insira o seguinte código:
     ```bash
     #!/bin/bash
     DIRETORIO="$1"
     mkdir $DIRETORIO
     echo "Diretório $DIRETORIO criado ou já existente."
     echo "Organizando arquivos para $DIRETORIO..."
     mv *.sh $DIRETORIO/
     echo "Arquivos shell movidos para $DIRETORIO."
     ```
   - Salve e saia (`:wq`).
3. **Explicação do Código**:
   - `DIRETORIO="$1"`: Define uma variável global `DIRETORIO` com o parâmetro posicional $1.
   - `mkdir $DIRETORIO`: Cria o diretório de acordo com o nome informado no parâmetro.
   - `echo "Diretório $DIRETORIO criado ou já existente."`: Exibe uma mensagem confirmando a tentativa de criação do diretório.
   - `echo "Organizando arquivos para $DIRETORIO..."`: Exibe uma mensagem informando o início do processo de organização.
   - `mv scripts/*.sh $DIRETORIO/`: Move todos os arquivos cujos nomes finalizam com `.sh` para o subdiretório informado.
     - `*.sh`: Corresponde a todos os arquivos com extensão `.sh`.
   - `echo "Arquivos movidos para $DIRETORIO."`: Confirma que os arquivos foram movidos.
4. **Tornar Executável e Executar com `./`**:
   - Torne o script executável:
     ```bash
     chmod +x organizador.sh
     ```
   - Execute com o argumento que representa o nome do diretório desejado:
     ```bash
     ./organizador.sh scripts
     ```
   - **Saída Esperada** (exemplo):
     ```
     Diretório scripts criado ou já existente.
     Organizando arquivos shell (.sh) para scripts...
     Arquivos shell movidos para scripts.
     ```
     - **Nota**: Se o diretório já existir, uma mensagem de erro do `mkdir` pode aparecer, mas o script continuará funcionando. Se não houver arquivos `.sh` para mover, o `mv` pode gerar um erro, mas a execução prossegue.
5. **Visualizar a Variável Global**:
   - Verifique se a variável `NOME` foi alterada no terminal:
     ```bash
     echo $NOME
     ```
     - **Saída Esperada**:
       ```
       Maria
       ```
     - **Explicação**: A variável `NOME` definida no script não afeta o terminal, pois `./` isola a execução.
6. **Tarefa de Gerenciamento**:
   - Verifique o conteúdo do diretório `backup`:
     ```bash
     ls
     ls scripts
     ```
     - Você verá os arquivos `.sh` movidos (por exemplo, `nome.sh`, `local.sh`, `argumentos.sh`, `interativo.sh`).

