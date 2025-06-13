# Desafio de Gerenciamento de Arquivos para Festival de Tecnologia Escolar

## Contexto
Você lidera um festival de tecnologia em uma escola secundária, com equipes apresentando projetos de robótica, aplicativos e experimentos de IA. Organize materiais digitais — planos, códigos-fonte, apresentações, cronogramas e relatórios — em uma estrutura de diretórios sob `/home/user/festival_tecnologia`. Use `vim` para criar/editar conteúdos, simulando um ambiente profissional com prazo apertado.

## Obtendo os arquivos.

Para obter os arquivos, execute a seguinte sequência de comandos:

1. ``` rm -rf * ```
2. ``` apt install git ```
3. ``` git clone --no-checkout https://github.com/charlesfsantos/roteiros-linux.git ```
4. ``` cd roteiros-linux/ ```
5. ``` git sparse-checkout init ```
6. ``` git sparse-checkout set 3-festival-tecnologia ```
7. ``` git checkout main ```
8. ``` mv 3-festival-tecnologia/ ~/festival-tecnologia```
9. ``` cd ~ ```


## Desafio
1. Criar uma estrutura de diretórios para:
  - Planos de projetos (ex.: `plano_robotica.txt`, `plano_app.txt`).
  - Códigos-fonte (ex.: `script_robot.py`, `app_codigo.js`).
  - Apresentações (ex.: `apresentacao_equipe1.txt`, `apresentacao_equipe2.txt`).
  - Cronogramas (ex.: `cronograma_dia1.txt`, `cronograma_dia2.txt`).
  - Relatórios finais (ex.: `relatorio_robotica.txt`, `relatorio_ia.txt`).
2. Organizar arquivos em subdiretórios (ex.: `planos/`, `codigos/`, `apresentacoes/`, `cronogramas/`, `relatorios/`) com `mv`.
3. Criar backups (ex.: `apresentacao_equipe1_backup.txt`, `script_robot_backup.py`) com `cp`.
4. Excluir arquivos obsoletos (ex.: `rascunho_temp.txt`, `teste_errado.py`) com `rm -i`.
- Estrutura final: mínimo de 10 arquivos, 5 subdiretórios, 4 backups, e `resumo_festival.txt` (via `vim`) explicando estrutura, comandos e justificativas.
5. **Verificações**:
  - Usar `wc -w` (word counter) para contar palavras em relatórios.
  - Usar `diff` (ex.: `diff apresentacao_equipe1.txt apresentacao_equipe1_backup.txt`).
  - Criar `README.txt` com instruções para navegar a estrutura.

## Ferramentas
- **Arquivos/Diretórios**: `mkdir`, `touch`, `mv`, `cp`, `rm`, `ls -l`, `cd`.
- **Edição**: `vim` (`i`, `Esc`, `:w`, `:q`, `:wq`, `:q!`, `:e`, `u`, `:%s`, `/`).
- **Auxiliares**: `cat`, `pwd`, `wc`, `diff`, `tree` (se disponível).

## Restrições
- Sem orientações; use conhecimentos prévios de Linux e `vim`.

## Entrega
- Diretório `/home/usuario/festival_tecnologia` com estrutura clara, arquivos editados, backups e `resumo_festival.txt` detalhando escolhas e comandos
- `README.txt` com guia para acessar materiais.
