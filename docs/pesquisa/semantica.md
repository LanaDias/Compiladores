# Etapa 5 — Análise Semântica do CompilaLab

## 1. Objetivo

A análise semântica do CompilaLab verifica se um programa sintaticamente válido respeita as regras de significado definidas para o subconjunto da linguagem implementada.

O analisador recebe a Árvore Sintática Abstrata (AST) produzida pelo parser, verifica declarações, escopos e compatibilidade de tipos, constrói a tabela de símbolos e apresenta diagnósticos quando encontra violações.

## 2. Estratégia utilizada

Foi adotada a estratégia de percorrimento da AST (*tree walk*), em uma passada.

O analisador percorre os nós da árvore e aplica as regras semânticas correspondentes a cada construção da linguagem. Durante esse processo, mantém uma estrutura de escopos e uma tabela de símbolos.

Essa abordagem foi escolhida por ser adequada ao subconjunto implementado e por facilitar a compreensão didática das verificações realizadas.

## 3. Regras semânticas implementadas

O CompilaLab implementa as seguintes verificações:

- **Identificador não declarado:** identifica o uso de variáveis que não foram declaradas em um escopo visível.
- **Redeclaração:** impede que uma variável seja declarada novamente no mesmo escopo.
- **Compatibilidade de tipos:** verifica se o tipo de uma expressão pode ser atribuído ao tipo da variável.
- **Operações aritméticas:** verifica se os operandos são de tipos numéricos compatíveis.
- **Operações relacionais e de igualdade:** verifica a compatibilidade dos operandos nas comparações.
- **Operações lógicas:** verifica o uso de valores booleanos em operações lógicas.
- **Operações unárias:** verifica a compatibilidade do operando com o operador utilizado.
- **Condições:** exige expressões booleanas nas estruturas `if` e `while`.
- **Escopos:** realiza a busca de identificadores do escopo mais interno para os escopos externos.
- **Sombreamento:** permite que uma variável de um escopo interno tenha o mesmo nome de uma variável de um escopo externo.

A linguagem também permite atribuir um valor inteiro a uma variável do tipo `float`, conforme a compatibilidade implementada.

## 4. Regras não implementadas

As seguintes verificações não fazem parte do escopo atual:

- **Uso de variável não inicializada:** embora a tabela registre se a variável possui inicialização, não é realizada uma análise completa para impedir todos os usos antes da inicialização.
- **Análise de fluxo de controle:** não é verificado se uma variável foi inicializada em todos os caminhos possíveis de execução.
- **Funções e parâmetros:** não são verificadas declarações de funções, quantidade ou tipos de argumentos.
- **Compatibilidade de retorno de funções:** não há verificação de tipo de retorno associado a funções, pois declarações de funções não fazem parte do subconjunto atual.
- **Conversões implícitas complexas:** não são implementadas regras avançadas de conversão entre tipos.
- **Sobrecarga de operadores:** não é suportada.

Essas limitações foram definidas considerando o subconjunto da linguagem e o escopo acadêmico do projeto.

## 5. Tabela de símbolos

A tabela de símbolos é construída durante o percurso da AST.

Cada símbolo possui os seguintes atributos:

| Atributo | Descrição |
|---|---|
| `nome` | Nome do identificador |
| `tipo` | Tipo de dado declarado |
| `escopo` | Escopo em que a variável foi declarada |
| `linha` | Linha da declaração |
| `coluna` | Coluna da declaração |
| `inicializado` | Indica se foi declarada com inicialização |
| `usado` | Indica se o identificador foi utilizado |

Os escopos são organizados em uma pilha lógica. Ao entrar em um bloco, um novo escopo é criado; ao sair, ele é encerrado.

A busca por identificadores começa no escopo mais interno e continua em direção aos escopos externos. O sombreamento é permitido, mas a redeclaração dentro do mesmo escopo é rejeitada.

A tabela é retornada pelo backend e apresentada na interface do CompilaLab.

## 6. Diagnósticos semânticos

Os erros semânticos são apresentados com informações que auxiliam o estudante a compreender o problema:

- Regra semântica violada;
- Mensagem explicativa;
- Linha e coluna do problema;
- Sugestão de correção, quando disponível.

Os diagnósticos são apresentados separadamente dos erros léxicos e sintáticos.

## 7. Fluxo de análise

O fluxo implementado é:

1. O usuário informa o código-fonte pela interface.
2. O frontend envia o código ao backend.
3. O scanner realiza a análise léxica.
4. Se não houver erros léxicos, o parser realiza a análise sintática.
5. Se não houver erros sintáticos, o parser disponibiliza a AST.
6. O analisador semântico percorre a AST.
7. A tabela de símbolos é construída e as regras semânticas são verificadas.
8. O backend retorna os resultados para a interface.
9. A interface apresenta tokens, AST, tabela de símbolos e diagnósticos.

A análise semântica não é executada quando existem erros léxicos ou sintáticos. Essa decisão evita diagnósticos semânticos baseados em uma estrutura incompleta ou inválida.

## 8. Integração com a API

A análise é disponibilizada pelo endpoint `POST /api/analisar`.

A resposta mantém os resultados das etapas anteriores e acrescenta o resultado semântico, incluindo:

- Resultado léxico;
- Resultado sintático e AST, quando válida;
- Resultado semântico;
- Tabela de símbolos;
- Diagnósticos semânticos.

Quando uma etapa anterior falha, as etapas seguintes são marcadas como não executadas.

## 9. Diferencial didático

O CompilaLab busca auxiliar o estudante não apenas a identificar erros, mas também a compreender as regras semânticas envolvidas.

Como recurso didático, os diagnósticos apresentam a regra violada, uma explicação em linguagem acessível, a localização do problema e uma sugestão de correção quando possível. A tabela de símbolos também permite visualizar os identificadores declarados, seus tipos e seus respectivos escopos.

A contribuição desse recurso deverá ser avaliada com estudantes e comparada aos recursos apresentados nos trabalhos relacionados, sem pressupor que seja inédito antes dessa comparação.

## 10. Limitações e trabalhos futuros

A análise semântica atual está limitada ao subconjunto de linguagem implementado. Como evolução, podem ser incluídas verificações de inicialização, análise de fluxo de controle, funções, parâmetros e uma representação semântica mais elaborada, prevista para a Etapa 6.