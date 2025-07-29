## Shell Scripting: Funções

Assim como em outras linguagens de programação, funções são blocos reutilizáveis de código que executam uma tarefa específica. 

<!-- Em shell script, elas ajudam a organizar melhor os comandos, evitando repetições e facilitando a manutenção do código. Você pode definir uma função uma única vez e chamá-la quantas vezes quiser ao longo do script. -->

Uma vez definido, uma função pode ser chamada como um comando comum do shell. Desse modo, é possível fornecer parâmetros de entrada para uso interno na função. 

Ao final deste guia prático, você será capaz de definir e interagir com funções, realizando tarefas distintas no sistema operacional. 

---

### Requisitos

* Compreensão sobre navegar na estrutura de diretórios do Linux (usando comandos como `cd` e `ls`)
* Entendimento básico de comandos de shell e execução de scripts (`chmod +x` e `./script.sh`).

---

### Preparação do Arquivo

Em `~/3-shell-script/exercicios`, crie o diretórios `funcoes`. 

No diretório `funcoes`, crie um arquivo de script de trabalho:

```bash
touch pratica_funcoes.sh
chmod +x pratica_funcoes.sh
vim pratica_funcoes.sh
```

---

## Passo 1: Estrutura basica de uma função

Adicione isso ao seu script:

```bash
#!/bin/bash

olamundo() {
  echo "Olá, mundo!"
}

olamundo
```

✅ **Teste**: Execute o script. Você verá uma mensagem de saudação.

---

### Passo 2: Função com Parâmetros

Crie e modifique o script `ola_usuario.sh`:

```bash
#!/bin/bash

olausuario() {
  echo "Olá, $1! Hoje é $(date +%A)."
}

olausuario "Carlos"
olausuario "Ana"
```

✅ **Explicação**: A função imprime saudações personalizadas usando o primeiro parâmetro posicional **local** `$1`.

---

### Passo 3: Função que Retorna um Valor

Funções Bash não "retornam" valores como outras linguagens, mas podemos usar `echo` ou o valor especial `return`.

Exemplo com `echo`:

Crie e edite `quadrado.sh`:
```bash
#!/bin/bash

quadrado() {
  result=$(( $1 * $1 ))
  echo "$result"
}

valor=`quadrado 5`
echo "O quadrado de 5 é: $valor"
```

✅ **Teste**: Ao executar, você verá "O quadrado de 5 é: 25".

---

### Passo 4: Usando `return` para Código de Saída

Entretanto, o comando `return` pode indicar sucesso ou falha na execução da função. Para isso, você deve explicitar em quais momentos os códigos serão retornados. 

Para indicar sucesso, use o código `0`. Valores diferentes de zero podem ser usados para informar diferentes tipos de falhas:

Crie e edite `paridade.sh`

```bash
#!/bin/bash

verificar_paridade() {
  if (( $1 % 2 == 0 )); then
    return 0
  else
    return 1
  fi
}

number=4

if verificar_paridade $number; then
  echo "$number é par"
else
  echo "$number é ímpar"
fi
```

✅ **Teste**: Altere o valor de `number` para testar diferentes saídas.

---

### Passo 5: Chamando Funções Dentro de Outras

Você pode chamar uma função dentro de outra:

Crie e edite `dobrar.sh`

```bash
dobrar() {
  echo $(( $1 * 2 ))
}

processar_numero() {
  original=$1
  dobrado=$(dobrar $original)
  echo "Original: $original - Dobrado: $dobrado"
}

processar_numero 7
```

✅ **Teste**: Irá imprimir o número original e seu dobro. Teste outros números. 

---

## Desafio 1

1. Tendo em vista que as variáveis definidas posicionais das funções são do tipo local, modifique os scripts `dobrar.sh` e `paridade.sh` para que sejam realizem suas tarefas de forma parametrizada. Como resultado, os scripts devem ser executados de acordo com os exemplos a seguir:
- `./dobrar.sh 5`
- `./paridade.sh 3`

2. Os scripts `quadrado.sh` e `ola_usuario.sh`, ao serem executados, devem solicitar, de forma interativa com o comando `read`, as informações necessárias para realizar as suas respectivas tarefas. Por exemplo
- `./quadrado.sh`

```
Informe o número para ser elevado ao quadrado: 5
O quadrado de 5 é: 25
```

## Desafio 2

Crie um script chamado `verifica_arquivo.sh` baseado em funções que:

1. Solicite ao usuário que digite o nome de um arquivo via entrada do teclado (`read`).
2. Verifique se o arquivo informado existe e é um arquivo comum usando `[ -f "$nome" ]`.
3. Caso o arquivo exista:
   - Mostre o caminho absoluto do arquivo com `realpath`.
   - Conte e exiba o número de linhas com `wc -l`.
4. Caso o arquivo não exista, exiba uma mensagem de erro amigável.

Seu script deve conter *pelo menos* duas funções:

- `check_file`: responsável por verificar a existência do arquivo.
- `count_lines`: responsável por contar e mostrar o número de linhas do arquivo, caso ele exista.