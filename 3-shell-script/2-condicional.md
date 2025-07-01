
# Elementos condicionais em shell scripting

## Contexto

Nesta prática, utlizaremos os comandos de teste (`test`, `[ ]`) do `bash`, que são a base para as estruturas `if`, que verificam de afirmações condicionadas. Por fim, usaremos tais comandos em scripts de gerenciamento básico do sistema.

Antes de iniciar esta prática, vá até o diretório `~/3-shell-script/exercicios`. Então, crie e entre no diretório `condicionais`. 

---

## Tarefa 1. Fundamentos do comando `test` e retorno `$?`

### Tarefa 1.1 — Testes numéricos simples

Na linha de comando, forneça os seguintes comandos:

```bash
test 5 -eq 5; echo $?
test 8 -gt 3; echo $?
test 2 -lt 1; echo $?
```

Saída esperada: 
```
0
0
1
```

Considerações:
1. A variável `$?` verifica o status final (código de retorno) do último comando executado. O símbolo `;` indica uma sequência de comandos, ou seja, `echo $?` é executado após `test 5 -eq 5`. 

2. Deste modo, o comando `echo $?` testa se o comando foi executado com sucesso ou não. Um código retorno igual a 0 indica que o comando obteve êxito. Qualquer código de retorno diferente denota algum tipo de falha na execução do comando. 

3. O comando `test` possui um conjunto de utilidades que comparam dois valores e realizam verificações em arquivos e diretórios. Os comandos que você forneceu testam igualdade (`-eq`), maior que (`-gt`, do inglês "greater than") e menor que (`-lt`, do inglês "less than") entre dois números.  


Pergunta: **O que significa o retorno `0` e `1`**?

---

### Tarefa 1.2 — Testes com arquivos

Execute os seguintes comandos no terminal:

```bash
touch teste.txt
mkdir pasta

test -f teste.txt; echo $?
test -d pasta; echo $?
test -r teste.txt; echo $?
```

Saída esperada: 
```
0
0
0
```

A opção `-f` do comando verifica a existência de um arquivo (do inglês "file"). Em seguida, a opção `-d` verifica a existência de um diretório (do inglês "directory"). Por fim, o teste que verifica se o arquivo possui permissão de leitura é realizado com a opção `-r` (do inglês "read"). 

---

## Tarefa 2 — Teste de estrutura `if` com `test` e `[ ]`

### Tarefa 2.1 — Comparar números

Certifique-se de estar no diretório `~/3-shell-script/exercicios/condicionais`. 

Agora, faça um script que usa o comando `test` para realizar uma comparação entre dois números. O script deverá ler um número para uma variável, verificando se é maior ou menor que 100. 

Crie e edite o arquivo `maiorque.sh`.

```bash
#!/bin/bash
echo "Digite um número:"
read NUM

if test "$NUM" -gt 100
then
    echo "Maior que 100"
else
    echo "Menor ou igual a 100"
fi
```

**Conceda permissão de execução para o arquivo e o execute com alguns valores:** 

```bash
root@debian-fsor:~$ chmod +x maiorque.sh
root@debian-fsor:~$ ./maiorque.sh
Digite um número: 
100
Menor ou igual a 100;
```

---

### Tarefa 2.2 — Verificar arquivo e exibir conteúdo

Nesta etapa, será utilizada a versão encurtada do comando `test`, que inclui o uso de colchetes. Verifique o exemplo a seguir.

Edite o arquivo `conteudo.sh`. 

```bash
#!/bin/bash
echo "Informe um arquivo:"
read ARQ

if [ -f "$ARQ" ]
then
    echo "Arquivo encontrado. Conteúdo:"
    cat "$ARQ"
else
    echo "Arquivo não encontrado!"
fi
```

**Conceda permissão de execução para o arquivo e o execute com alguns valores:** 

```bash
root@debian-fsor:~$ chmod +x conteudo.sh
root@debian-fsor:~$ ./conteudo.sh
Informe um arquivo: 
maiorque.sh
Arquivo encontrado. Conteúdo: [...]
```


---

## Tarefa 3 — Trabalhando com permissões

### Tarefa 3.1 — Verificar permissões de leitura, escrita e execução

Crie o arquivo `permissoes.sh`. 

```bash
#!/bin/bash
read -p "Arquivo: " ARQ

if [ -r "$ARQ" ]; then echo "Pode ler"; fi
if [ -w "$ARQ" ]; then echo "Pode escrever"; fi
if [ -x "$ARQ" ]; then echo "Pode executar"; fi
```

**Conceda permissão de execução para o arquivo e o execute com alguns valores:** 

```bash
root@debian-fsor:~$ chmod +x permissoes.sh
root@debian-fsor:~$ ./permissoes.sh
Arquivo: conteudo.sh
Pode ler
Pode escrever
Pode executar
```


---

### Tarefa 3.2 — Oferecer edição apenas se tiver permissão de escrita

Crie o arquivo `edicao.sh`.

```bash
#!/bin/bash
read -p "Arquivo: " ARQ

if [ -w "$ARQ" ]
then
    vim "$ARQ"
else
    echo "Sem permissão de escrita."
fi
```

Conceda permissão de execução do arquivo e teste-o com algum script já existente. 

---

## Tarefa 4 — Verificando e manipulando usuários

### Tarefa 4.1 — Verificar se um usuário existe

Edite o arquivo `usuario.sh`.

```bash
#!/bin/bash
read -p "Usuário: " USR

if id "$USR" >/dev/null 2>&1
then
    echo "Usuário existe"
else
    echo "Usuário não existe"
fi
```

Conceda permissão de execução e realize os testes apropriados. 

---

### Tarefa 4.2 — Criar diretório para usuário, se não existir

Crie o arquivo `diretorio.sh`.

```bash
#!/bin/bash
read -p "Diretório: " DIR

if [ ! -d "$DIR" ]
then
    echo "Criando diretório home..."
    mkdir "$DIR"
else
    echo "Diretório $DIR já existe."
fi
```

Conceda permissão de execução e realize os testes apropriados. 

---

### Tarefa 4.3 — Adicionar usuário a um grupo se ele existir

Crie o arquivo `grupos.sh`.

```bash
#!/bin/bash
read -p "Usuário: " USR
read -p "Grupo: " GRP

if id "$USR" >/dev/null 2>&1
then
    usermod -aG "$GRP" "$USR"
    echo "Usuário adicionado ao grupo."
else
    echo "Usuário inexistente."
fi
```

Em seguida, verifique os usuários e grupos criados usando os comandos `getent passwd` e `getent group`. Conceda permissão de execução para o arquivo e execute os testes para adicionar um usuário a um grupo qualuquer. 

---

### Tarefa 4.4 — Verificar quem está usando um arquivo

Escreva no arquivo `uso_arquivo.sh`. 

```bash
#!/bin/bash
read -p "Arquivo: " ARQ

if [ -f "$ARQ" ]
then
    echo "Usuários que estão acessando o arquivo:"
    lsof "$ARQ"
else
    echo "Arquivo não encontrado"
fi
```

O comando `lsof` lista os arquivos em uso no sistema operacional. Ao mesmo tempo, o comando identifica qual usuário está realizando operações sobre o arquivo em uso. 

Para testar o script, abra um novo terminal (ex. `Alt + F2`) e abra algum arquivo em `~/3-shell-script/exercicios/condicional` com o comando `vim`. Em seguida, volte ao terminal anterior (ex. `Alt + F1`), conceda permissão de execução ao arquivo `uso_arquivo.sh`, execute-o e forneça o nome do arquivo que foi aberto no outro terminal. Verifique o retorno do script. 

---


## Tarefa 5 — Escrevendo scripts com múltiplos testes

### Tarefa 5.1 — Menu de verificação de arquivo

Edite o arquivo `e_permissoes.sh` e insira o novo conteúdo conforme a seguir: 

```bash
#!/bin/bash
read -p "Arquivo: " ARQ

if [ ! -e "$ARQ" ]; then
    echo "Arquivo não existe"
    exit 1
fi

echo "Arquivo existe."
echo "Escolha: (1) Exibir, (2) Editar, (3) Executar"

read OPCAO

if [ "$OPCAO" = "1" ] && [ -r "$ARQ" ]; then
    cat "$ARQ"
elif [ "$OPCAO" = "2" ] && [ -w "$ARQ" ]; then
    vim "$ARQ"
elif [ "$OPCAO" = "3" ] && [ -x "$ARQ" ]; then
    ./"$ARQ"
else
    echo "Operação não permitida ou inválida."
fi
```

Aqui, o sinal de exclamação `!` indica uma afirmação negativa. Em outras palavras, o primeiro condicional `if` testa se o arquivo informado não existe para, então, mostrar o informe com o comando `echo` e, em seguida, interromper a execução do script com o comando `exit` junto ao código de retorno `1`. 

Após ler a opção escolhida, o script realiza dois testes em cada condição. Cada condição só será satisfeita se ambos testes forem bem sucedidos. 
- Por exemplo, ao escolher a opção **Exibir**, o script testará, na primeira condição, se a opção `1` foi fornecida. Se sim, é necessário realizar o teste de leitura no arquivo. Se a leitura for possível, o script chamará o comando de leitura do arquivo `cat $ARQ`.

Com a permissão de execução do arquivo `permissoes.sh`, teste o script sobre os arquivos existentes no diretório. 

---

### Tarefa 5.2 — Verificar se o arquivo é legível **ou** executável

Escreva o arquivo `ou_permissoes.sh`.

```bash
#!/bin/bash
read -p "Arquivo: " ARQ

if [ -r "$ARQ" ] || [ -x "$ARQ" ]
then
    echo "Você pode ler ou executar este arquivo."
else
    echo "Você NÃO tem permissão de leitura nem de execução."
fi
```

A análise condicional deste script testa se um arquivo é legível **ou** executável. Portanto, basta que o arquivo possua uma das duas permissões para que a verificação seja bem sucedida. 

Com a permissão de execução do arquivo `ou_permissoes.sh`, teste o script sobre os arquivos existentes no diretório. 


---


## Tarefa 6 — Testes finais

### Desafio 6.1 — Criar usuário e grupo se necessário

Escreva o script a seguir em `criar_contas.sh` de termine como se dá a sequência das lógicas aplicadas. 

```bash
#!/bin/bash
read -p "Usuário: " USR
read -p "Grupo: " GRP

# Verifica e cria grupo
if ! getent group "$GRP" >/dev/null
then
    groupadd "$GRP"
    echo "Grupo $GRP criado."
else
    echo "Grupo já existente."
fi

# Verifica e cria usuário
if ! id "$USR" >/dev/null 2>&1
then
    useradd -m -G "$GRP" "$USR"
    echo "Usuário $USR criado no grupo $GRP."
else
    echo "Usuário já existe."
fi
```

---

## Conclusão

Você praticou:

- Testes com `test` e `[ ]`
- Estruturas `if`, `else`, `&&`, `||`
- Permissões (r, w, x)
- Manipulação de arquivos e usuários
- Scripts utilitários com lógica condicional real