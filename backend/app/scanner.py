
import re

# Palavras que possuem significado especial na linguagem.
PALAVRAS_RESERVADAS = {
    "if",
    "else",
    "while",
    "return",
    "int",
    "float",
    "print",
    "True",
    "False",
    "and",
    "or",
    "not",
}

# Operadores reconhecidos pela linguagem.
OPERADORES = (
    "==",
    "!=",
    "<=",
    ">=",
    "+",
    "-",
    "*",
    "/",
    "%",
    "=",
    "<",
    ">",
    "!",
)

# Símbolos utilizados para organizar o código.
DELIMITADORES = {
    "(", ")",
    "{", "}",
    "[", "]",
    ",", ";",
    ":", ".",
}


def analisar_lexicamente(codigo: str) -> dict:
    tokens = []
    erros = []

    posicao = 0
    linha = 1
    coluna = 1

    def avancar(texto):
        nonlocal linha, coluna

        linhas = texto.split("\n")

        if len(linhas) > 1:
            linha += len(linhas) - 1
            coluna = len(linhas[-1]) + 1
        else:
            coluna += len(texto)

    def registrar_erro(lexema, linha_erro, coluna_erro, mensagem):
        erros.append({
            "tipo": "ERRO_LEXICO",
            "lexema": lexema,
            "linha": linha_erro,
            "coluna": coluna_erro,
            "mensagem": mensagem,
        })

    while posicao < len(codigo):
        caractere = codigo[posicao]

        # Ignorar espaços, tabulações e quebras de linha.
        if caractere.isspace():
            avancar(caractere)
            posicao += 1
            continue

        linha_token = linha
        coluna_token = coluna

        # Ignorar comentários iniciados por #.
        if caractere == "#":
            inicio = posicao

            while posicao < len(codigo) and codigo[posicao] != "\n":
                posicao += 1

            lexema = codigo[inicio:posicao]
            avancar(lexema)
            continue

        # Reconhecer números inteiros e reais.
        if caractere.isdigit():
            inicio = posicao

            while posicao < len(codigo) and (
                codigo[posicao].isdigit()
                or codigo[posicao] == "."
            ):
                posicao += 1

            # Verificar se existe uma letra ou "_" logo após o número.
            if posicao < len(codigo) and (
                codigo[posicao].isalpha()
                or codigo[posicao] == "_"
            ):
                while posicao < len(codigo) and (
                    codigo[posicao].isalnum()
                    or codigo[posicao] == "_"
                    or codigo[posicao] == "."
                ):
                    posicao += 1

                lexema = codigo[inicio:posicao]

                registrar_erro(
                    lexema,
                    linha_token,
                    coluna_token,
                    f"Número malformado: {lexema!r}",
                )

                avancar(lexema)
                continue

            lexema = codigo[inicio:posicao]

            if lexema.count(".") > 1:
                registrar_erro(
                    lexema,
                    linha_token,
                    coluna_token,
                    f"Número malformado: {lexema!r}",
                )
            else:
                tipo = (
                    "LITERAL_REAL"
                    if "." in lexema
                    else "LITERAL_INTEIRO"
                )

                tokens.append({
                    "tipo": tipo,
                    "lexema": lexema,
                    "linha": linha_token,
                    "coluna": coluna_token,
                })

            avancar(lexema)
            continue

        # Reconhecer identificadores e palavras reservadas.
        if caractere.isalpha() or caractere == "_":
            inicio = posicao

            while posicao < len(codigo) and (
                codigo[posicao].isalnum()
                or codigo[posicao] == "_"
            ):
                posicao += 1

            lexema = codigo[inicio:posicao]

            tipo = (
                "PALAVRA_RESERVADA"
                if lexema in PALAVRAS_RESERVADAS
                else "IDENTIFICADOR"
            )

            tokens.append({
                "tipo": tipo,
                "lexema": lexema,
                "linha": linha_token,
                "coluna": coluna_token,
            })

            avancar(lexema)
            continue

        # Reconhecer operadores, priorizando os maiores.
        operador_encontrado = None

        for operador in OPERADORES:
            if codigo.startswith(operador, posicao):
                operador_encontrado = operador
                break

        if operador_encontrado is not None:
            tokens.append({
                "tipo": "OPERADOR",
                "lexema": operador_encontrado,
                "linha": linha_token,
                "coluna": coluna_token,
            })

            avancar(operador_encontrado)
            posicao += len(operador_encontrado)
            continue

        # Reconhecer delimitadores.
        if caractere in DELIMITADORES:
            tokens.append({
                "tipo": "DELIMITADOR",
                "lexema": caractere,
                "linha": linha_token,
                "coluna": coluna_token,
            })

            avancar(caractere)
            posicao += 1
            continue

        # Caracteres não reconhecidos.
        registrar_erro(
            caractere,
            linha_token,
            coluna_token,
            f"Caractere não reconhecido: {caractere!r}",
        )

        avancar(caractere)
        posicao += 1

    return {
        "sucesso": len(erros) == 0,
        "tokens": tokens,
        "erros": erros,
    }
    
    