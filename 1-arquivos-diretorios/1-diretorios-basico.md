# Prática Guiada: Navegando no Sistema de Arquivos do Linux

Neste prática, você deverá navegar pela estrutura hierárquica de diretórios do Linux. Para isso, é necessário entender comandos e conceitos-chave como diretório atual (.), diretório superior (..), diretório home (~) e diretório anterior (-).

## Objetivos
- Compreender a estrutura hierárquica do sistema de arquivos do Linux.
- Usar comandos básicos para navegar em diretórios e visualizar arquivos.
- Aplicar os conceitos de diretório atual (.), diretório superior (..), diretório home (~) e diretório anterior (-).

## Contexto: Sistema de Arquivos do Linux
O sistema de arquivos do Linux é organizado como uma árvore, começando pelo **diretório raiz** (`/`). Todos os outros diretórios e arquivos se ramificam a partir daqui. Diretórios principais incluem:
- `/home`: Contém os diretórios home dos usuários (ex.: `/home/user`).
- `/etc`: Armazena arquivos de configuração do sistema.
- `/var`: Contém dados variáveis, como logs.
- `/bin`: Armazena programas executáveis essenciais.

## Conceitos-Chave
- **Diretório Atual (.)**: Refere-se ao diretório em que você está no momento.
- **Diretório superior (..)**: Refere-se ao diretório um nível acima do diretório atual.
- **Diretório Home (~)**: Seu diretório pessoal, geralmente `/home/user`.
- **Diretório Anterior (-)**: Refere-se ao diretório em que você estava antes do último comando `cd`. O comando `cd -` volta para esse diretório.
- **Caminho**: A localização de um arquivo ou diretório (ex.: `/home/user/documentos`).
  - **Caminho Absoluto**: Caminho completo a partir da raiz (ex.: `/home/user/documentos`).
  - **Caminho Relativo**: Caminho em relação ao diretório atual (ex.: `documentos` se você estiver em `/home/user`).

## Comandos Essenciais
Aqui estão os comandos que você usará:
- `pwd`: Exibe o Diretório Atual (mostra o diretório em que você está).
- `ls`: Lista o conteúdo de um diretório.
- `cd`: Muda de Diretório (move para outro diretório).
- `mkdir`: Cria um novo diretório.
- `touch`: Cria um arquivo vazio.
- `cat`: Exibe o conteúdo de um arquivo.

## Passos da Prática Guiada

### Passo 1: Abrir o Terminal
Realize o login na sua VM Linux com o usuário `user`. Você verá um prompt como `user@debian-fsor:~$`, indicando que está no seu diretório home.

### Passo 2: Descobrir o Diretório Atual
Vamos confirmar onde você está.
1. Digite o seguinte comando e pressione Enter:
   ```
   pwd
   ```
2. A saída será:
   ```
   /home/user
   ```
   Este é o seu **diretório home** (~).

**Pergunta 1**: Qual é o caminho absoluto do seu diretório atual? (responder via formulário)

### Passo 3: Listar o Conteúdo do Diretório
Vamos ver o que há no seu diretório home.
1. Digite:
   ```
   ls -a
   ```
2. Este comando visualiza todos os arquivos dentro deste diretório, incluindo os ocultos (cujos nomes começam com o caractere ponto `.`)

### Passo 4: Criar um Diretório de Trabalho
Vamos criar um diretório para testar os conceitos trabalhados nesta aula.
1. Digite:
   ```
   mkdir pratica
   ```
2. Verifique se foi criado digitando:
   ```
   ls
   ```
   Você deve ver `pratica` na lista.

### Passo 5: Navegar para o Diretório de Prática
Entre no diretório `pratica`.
1. Digite:
   ```
   cd pratica
   ```
2. Confirme sua localização com:
   ```
   pwd
   ```
   A saída deve ser algo como `/home/user/pratica`.

**Pergunta 2**: Qual é o caminho absoluto do seu diretório atual agora?

### Passo 6: Criar Arquivos e Subdiretórios
Vamos adicionar algum conteúdo.
1. Crie um arquivo:
   ```
   touch meu_arquivo.txt
   ```
2. Crie um subdiretório:
   ```
   mkdir subdiretorio
   ```
3. Liste o conteúdo:
   ```
   ls
   ```
   Você deve ver `meu_arquivo.txt` e `subdiretorio`.

### Passo 7: Explorar os Diretórios Atual e superior
1. Use o **diretório atual (.)** para listar conteúdos:
   ```
   ls .
   ```
   Isso é o mesmo que `ls`, já que `.` significa “aqui”.
2. Entre na `subdiretorio`:
   ```
   cd subdiretorio
   ```
3. Use o **diretório superior (..)** para voltar:
   ```
   cd ..
   ```
4. Verifique se voltou para `pratica` com `pwd`.

**Pergunta 3**: O que `cd ..` faz? O que aconteceria se você executasse novamente?

### Passo 8: Usar o Diretório Home (~)
Vamos voltar para o diretório home.
1. Digite:
   ```
   cd ~
   ```
2. Verifique sua localização:
   ```
   pwd
   ```
   Você está de volta em `/home/user`.

**Pergunta 4**: A partir do diretório home, entre em `pratica/subdiretorio` usando o **caminho relativo**. Qual comando utilizado?

### Passo 9: Usar o Diretório Anterior (-)
Vamos explorar o conceito de **diretório anterior**.
1. Certifique-se de estar em `~/pratica` (use `cd ~/pratica` se necessário).
2. Navegue para `/etc`:
   ```
   cd /etc
   ```
3. Volte para o diretório anterior (`~/pratica`) usando:
   ```
   cd -
   ```
4. Verifique sua localização com `pwd`. A saída deve ser `/home/user/pratica`.
5. Experimente novamente: volte para `/etc` com `cd -` e observe como você alterna entre os dois diretórios.

**Pergunta**: O que `cd -` faz? Como ele é diferente de `cd ..`?

### Passo 10: Experimentar Caminhos Absolutos e Relativos
1. De qualquer lugar, vá para `/etc` usando um **caminho absoluto**:
   ```
   cd /etc
   ```
2. Liste seu conteúdo:
   ```
   ls
   ```
   Você verá arquivos e diretórios de configuração.
3. Volte para o diretório `pratica` usando um **caminho absoluto**:
   ```
   cd ~/pratica
   ```
   Note que `~` é um atalho para o diretório home.

**Pergunta 6**: Qual é a diferença entre `cd /etc` e `cd etc` se você estiver no diretório home?

### Passo 11: Criar e Visualizar um Arquivo
Vamos criar um arquivo com algum conteúdo.
1. Certifique-se de estar em `~/pratica` (use `cd ~/pratica` se necessário).
2. Crie um arquivo com texto:
   ```
   echo "Olá, Linux!" > saudacao.txt
   ```
3. Veja seu conteúdo:
   ```
   cat saudacao.txt
   ```

**Experimente**: Crie outro arquivo chamado `notas.txt` usando `touch`, depois adicione texto com `echo "Minhas notas" > notas.txt`. Use `cat` para verificar.

### Passo 12: Desafio
1. A partir do diretório home (~), crie um diretório chamado `escola`.
2. Dentro de `escola`, crie dois subdiretórios: `matematica` e `historia`.
3. Em `matematica`, crie um arquivo chamado `tarefa.txt`.
4. Navegue para `historia` usando um **caminho relativo** a partir de `matematica`.
5. Volte para o diretório home usando `~`.
6. Liste todo o conteúdo de `escola` usando um **caminho absoluto** (ex.: `ls ~/escola`).

**Dica**: Use `mkdir`, `touch`, `cd` e `ls`. Se ficar preso, use `pwd` para verificar sua localização.
