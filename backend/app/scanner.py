
import re

PALAVRAS_RESERVADAS = {
    "if", "else", "while", "return", "int", "float",
    "print", "True", "False"
}

PADRAO_TOKEN = re.compile(
    r"""
    (?P<ESPACO>\s+)
    |(?P<COMENTARIO>\#.*)
    |(?P<NUMERO>\d+(?:\.\d+)?)
    |(?P<IDENTIFICADOR>[A-Za-z_][A-Za-z0-9_]*)
    |(?P<OPERADOR>==|!=|<=|>=|[+\-*/%=<>])
    |(?P<DELIMITADOR>[(){}\[\],;:.])
    |(?P<INVALIDO>.)
    """,
    re.VERBOSE
)


def analisar_lexicamente(codigo: str) -> dict:
    tokens = []
    erros = []
    linha = 1
    coluna = 1
    posicao = 0

    while posicao < len(codigo):
        correspondencia = PADRAO_TOKEN.match(codigo, posicao)

        if not correspondencia:
            break

        lexema = correspondencia.group()
        tipo = correspondencia.lastgroup
        linha_token = linha
        coluna_token = coluna

        if tipo == "INVALIDO":
            erros.append({
                "tipo": "ERRO_LEXICO",
                "lexema": lexema,
                "linha": linha_token,
                "coluna": coluna_token,
                "mensagem": f"Caractere não reconhecido: {lexema!r}"
            })

        elif tipo not in {"ESPACO", "COMENTARIO"}:
            if tipo == "IDENTIFICADOR" and lexema in PALAVRAS_RESERVADAS:
                tipo_final = "PALAVRA_RESERVADA"
            elif tipo == "NUMERO":
                tipo_final = (
                    "LITERAL_REAL" if "." in lexema
                    else "LITERAL_INTEIRO"
                )
            elif tipo == "IDENTIFICADOR":
                tipo_final = "IDENTIFICADOR"
            elif tipo == "OPERADOR":
                tipo_final = "OPERADOR"
            else:
                tipo_final = "DELIMITADOR"

            tokens.append({
                "tipo": tipo_final,
                "lexema": lexema,
                "linha": linha_token,
                "coluna": coluna_token
            })

        linhas_consumidas = lexema.split("\n")
        if len(linhas_consumidas) > 1:
            linha += len(linhas_consumidas) - 1
            coluna = len(linhas_consumidas[-1]) + 1
        else:
            coluna += len(lexema)

        posicao = correspondencia.end()

    return {
        "sucesso": len(erros) == 0,
        "tokens": tokens,
        "erros": erros
    }
