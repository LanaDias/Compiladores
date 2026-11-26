
from app.scanner import analisar_lexicamente


def test_identifica_identificador_e_numeros():
    resultado = analisar_lexicamente("numero = 10 + 2.5")

    assert resultado["sucesso"] is True
    assert [t["tipo"] for t in resultado["tokens"]] == [
        "IDENTIFICADOR",
        "OPERADOR",
        "LITERAL_INTEIRO",
        "OPERADOR",
        "LITERAL_REAL",
    ]


def test_identifica_palavra_reservada():
    resultado = analisar_lexicamente("if")

    assert resultado["tokens"][0]["tipo"] == "PALAVRA_RESERVADA"


def test_ignora_espacos_e_comentarios():
    resultado = analisar_lexicamente("x = 1  # comentario\n y = 2")

    lexemas = [t["lexema"] for t in resultado["tokens"]]

    assert lexemas == ["x", "=", "1", "y", "=", "2"]
    assert resultado["erros"] == []


def test_registra_linha_e_coluna():
    resultado = analisar_lexicamente("x = 1\ny = 2")

    segundo_identificador = resultado["tokens"][3]

    assert segundo_identificador["lexema"] == "y"
    assert segundo_identificador["linha"] == 2
    assert segundo_identificador["coluna"] == 1


def test_identifica_caractere_invalido():
    resultado = analisar_lexicamente("x = 10 @ 20")

    assert resultado["sucesso"] is False
    assert len(resultado["erros"]) == 1
    assert resultado["erros"][0]["lexema"] == "@"
    assert resultado["erros"][0]["linha"] == 1
    assert resultado["erros"][0]["coluna"] == 8


def test_identifica_delimitadores():
    resultado = analisar_lexicamente("(x, y);")

    lexemas = [t["lexema"] for t in resultado["tokens"]]

    assert lexemas == ["(", "x", ",", "y", ")", ";"]
    assert all(
        t["tipo"] == "DELIMITADOR"
        for t in [
            resultado["tokens"][0],
            resultado["tokens"][2],
            resultado["tokens"][4],
            resultado["tokens"][5],
        ]
    )


def test_identifica_operadores_logicos():
    resultado = analisar_lexicamente("a and b or not c")

    assert resultado["sucesso"] is True
    assert [t["lexema"] for t in resultado["tokens"]] == [
        "a", "and", "b", "or", "not", "c"
    ]
    assert resultado["tokens"][1]["tipo"] == "PALAVRA_RESERVADA"
    assert resultado["tokens"][3]["tipo"] == "PALAVRA_RESERVADA"
    assert resultado["tokens"][4]["tipo"] == "PALAVRA_RESERVADA"


def test_identifica_operadores_compostos():
    resultado = analisar_lexicamente("a == b != c <= d >= e")

    assert resultado["sucesso"] is True
    assert [t["lexema"] for t in resultado["tokens"]] == [
        "a", "==", "b", "!=", "c", "<=", "d", ">=", "e"
    ]


def test_identifica_identificadores_com_underscore():
    resultado = analisar_lexicamente("meu_numero = valor2")

    assert resultado["sucesso"] is True
    assert [t["tipo"] for t in resultado["tokens"]] == [
        "IDENTIFICADOR",
        "OPERADOR",
        "IDENTIFICADOR",
    ]


def test_identifica_numero_malformado():
    resultado = analisar_lexicamente("numero = 12.3.4")

    assert resultado["sucesso"] is False
    assert len(resultado["erros"]) >= 1
