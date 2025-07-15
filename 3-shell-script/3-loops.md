
# Estruturas de Repetição em Shell Script (`for` e `while`)

Em linhas de comando como o `bash`, existem comandos internos que representam as estruturas básicas de repetição que conhecemos da programação, nomeadamente `for` e `while`.

Neste guia prático, iremos entender quais são os formatos necessários para declarar tais *loops*, assim como aplicá-los em alguns exemplos de tarefas de administração do sistema. 

Para iniciar esta aula, vá ao diretório `~/3-shell-script/exercicios` e crie (e entre n)a pasta `loops`. 

## Pré-requisitos

- Uso básico da linha de comando e de editores de texto
- Saber como executar scripts

---

## Seção 1: Laço `for`

### Sintaxe 1: Laço sobre uma lista

- `frutas.sh`
```bash
#!/bin/bash
for item in maçã banana cereja
do
  echo "Fruta: $item"
done
```

**Explicação**:
- Percorre cada item da lista.
- A variável `item` armazena cada valor da vez.

**Pratique**:
Digite o script acima em `frutas.sh`, torne-o executável e execute-o.

---

### Sintaxe 2: Laço sobre arquivos

- `arquivos.sh`
```bash
#!/bin/bash
for arquivo in *.txt
do
  echo "Processando $arquivo"
done
```

**Explicação**:
- O padrão `*.txt` lista todos os arquivos `.txt` no diretório.

**Pratique**:
1. Crie 3 arquivos `.txt`: `touch a.txt b.txt c.txt`
2. Execute o script e veja o processamento.

---

### Sintaxe 3: Laço estilo C

- `for_contador.sh`
```bash
for ((i=1; i<=5; i++))
do
  echo "Número $i"
done
```

**Explicação**:
- Funciona como um laço `for` em C.
- Bom para sequências numéricas.

**Pratique**:
Altere o limite para `i<=10` e execute novamente.

---

## Seção 2: Laço `while`

### Sintaxe básica do `while`

- `while_contador.sh`
```bash
contador=1
while [ $contador -le 5 ]
do
  echo "Contador: $contador"
  contador=$((contador + 1))
done
```

**Explicação**:
- Executa enquanto a condição for verdadeira. Isto é, enquanto a varável contador for menor ou igual a 5. 
- É necessário atualizar a variável (`contador`) manualmente (feito na linha `contador=$((contador + 1))`).

**Pratique**:
Altere a condição para parar no 10.

---

### Laço `while` infinito com `break`

- `interativo.sh`
```bash
while true
do
  read -p "Digite 'sair' para encerrar: " entrada
  if [ "$entrada" = "sair" ]; then
    break
  fi
  echo "Você digitou: $entrada"
done
```

**Explicação**:
- Útil quando o script espera uma condição específica do usuário.

**Pratique**:
Substitua `"sair"` por `"parar"` e teste novamente.

---

## Seção 3: Combinando Laços e Condições

- `paridade.sh`
```bash
for numero in {1..10}
do
  if [ $((numero % 2)) -eq 0 ]; then
    echo "$numero é par"
  else
    echo "$numero é ímpar"
  fi
done
```

**Pratique**:
- Altere o intervalo para `{1..20}`
- Exiba "divisível por 5" quando apropriado.

---

## Desafio Final

**Script: "`soma_pares.sh`"**

### Objetivo:
Criar um script que:

1. Solicite ao usuário um **número inicial** e um **número final**.
2. Percorra todos os números no intervalo.
3. Identifique os números **pares** e os exiba.
4. Calcule e exiba a **soma total dos pares**.

### Execução:

```
Digite o número inicial: 3
Digite o número final: 10

Números pares:
4
6
8
10

Soma = 28
```

### Dicas:
- Use `read` para obter os valores digitados.
- Utilize `for` ou `while` para iterar.
- Use `%` (módulo) para verificar se o número é par.
- Some os valores com: `soma=$((soma + numero))`

---