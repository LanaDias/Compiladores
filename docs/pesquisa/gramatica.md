
# Gramática EBNF do CompilaLab

## 1. Estrutura geral

```ebnf
programa = { instrucao } ;

instrucao =
      declaracao
    | atribuicao
    | comando_print
    | comando_return
    | comando_if
    | comando_while
    | bloco ;

## 2. Declarações

declaracao =
    tipo identificador [ "=" expressao ] fim_instrucao ;

tipo = "int" | "float" ;

## 3. Atribuição

atribuicao =
    identificador "=" expressao fim_instrucao ;

## 4. Comandos

comando_print =
    "print" "(" expressao ")" fim_instrucao ;

comando_return =
    "return" [ expressao ] fim_instrucao ;

comando_if =
    "if" expressao ":" bloco
    [ "else" ":" bloco ] ;

comando_while =
    "while" expressao ":" bloco ;

bloco =
      "{" { instrucao } "}"
    | indentacao { instrucao } dedentacao ;

## 5. Expressões

expressao = expressao_relacional ;

expressao_relacional =
    expressao_soma
    { operador_relacional expressao_soma } ;

expressao_soma =
    expressao_multiplicativa
    { ("+" | "-") expressao_multiplicativa } ;

expressao_multiplicativa =
    expressao_unaria
    { ("*" | "/" | "%") expressao_unaria } ;

expressao_unaria =
      ("+" | "-") expressao_unaria
    | primario ;

primario =
      literal
    | identificador
    | "(" expressao ")" ;

literal =
      inteiro
    | real
    | booleano ;

operador_relacional =
      "=="
    | "!="
    | "<"
    | ">"
    | "<="
    | ">=" ;

fim_instrucao = ";" | quebra_linha | fim_arquivo ;
```

## 6. Precedência

| Operadores | Precedência |
|---|---|
| `==`, `!=`, `<`, `>`, `<=`, `>=` | Menor |
| `+`, `-` | Intermediária |
| `*`, `/`, `%` | Maior |
| `+`, `-` unários | Maior |

A análise sintática é realizada por um parser descendente recursivo.
```
