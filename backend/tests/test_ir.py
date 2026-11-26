
from app.ir import gerar_representacao_intermediaria


def criar_ast(tipo, atributos=None, filhos=None):
    return {
        "tipo": tipo,
        "atributos": atributos or {},
        "filhos": filhos or [],
    }


# TESTES ANTERIORES DA IR

def test_gerar_ir_declaracao_variavel():
    ast = criar_ast("PROGRAMA", filhos=[
        criar_ast("DECLARACAO_VARIAVEL", {"tipoDado": "int"}, [
            criar_ast("IDENTIFICADOR", {"nome": "a"}),
            criar_ast("LITERAL_INTEIRO", {"valor": 10}),
        ])
    ])

    resultado = gerar_representacao_intermediaria(ast)

    assert resultado["sucesso"] is True
    assert "DECLARE a : int" in resultado["instrucoes"]
    assert "a = 10" in resultado["instrucoes"]


def test_gerar_ir_operacao_aritmetica():
    expressao = criar_ast("OPERACAO_BINARIA", {"operador": "+"}, [
        criar_ast("LITERAL_INTEIRO", {"valor": 5}),
        criar_ast("LITERAL_INTEIRO", {"valor": 3}),
    ])

    ast = criar_ast("PROGRAMA", filhos=[
        criar_ast("CHAMADA_PRINT", filhos=[expressao])
    ])

    resultado = gerar_representacao_intermediaria(ast)

    assert resultado["sucesso"] is True
    assert "t1 = 8" in resultado["instrucoes"]
    assert "PRINT t1" in resultado["instrucoes"]


def test_gerar_ir_condicional():
    condicao = criar_ast("LITERAL_BOOLEANO", {"valor": True})
    bloco = criar_ast("BLOCO")

    ast = criar_ast("PROGRAMA", filhos=[
        criar_ast("CONDICIONAL", filhos=[condicao, bloco])
    ])

    resultado = gerar_representacao_intermediaria(ast)

    assert resultado["sucesso"] is True
    assert any(item.startswith("IF_FALSE") for item in resultado["instrucoes"])
    assert any(item.startswith("LABEL") for item in resultado["instrucoes"])


def test_rejeitar_ast_invalida():
    try:
        gerar_representacao_intermediaria({})
        assert False, "Era esperado um ValueError"
    except ValueError:
        pass


# NOVOS TESTES DE DOBRA DE CONSTANTES

def test_dobra_constantes_soma():
    expressao = criar_ast("OPERACAO_BINARIA", {"operador": "+"}, [
        criar_ast("LITERAL_INTEIRO", {"valor": 5}),
        criar_ast("LITERAL_INTEIRO", {"valor": 3}),
    ])

    ast = criar_ast("PROGRAMA", filhos=[
        criar_ast("CHAMADA_PRINT", filhos=[expressao])
    ])

    resultado = gerar_representacao_intermediaria(ast)

    assert "t1 = 8" in resultado["instrucoes"]
    assert "t1 = 5 + 3" not in resultado["instrucoes"]


def test_dobra_constantes_operacao_aninhada():
    multiplicacao = criar_ast("OPERACAO_BINARIA", {"operador": "*"}, [
        criar_ast("LITERAL_INTEIRO", {"valor": 3}),
        criar_ast("LITERAL_INTEIRO", {"valor": 2}),
    ])

    expressao = criar_ast("OPERACAO_BINARIA", {"operador": "+"}, [
        criar_ast("LITERAL_INTEIRO", {"valor": 5}),
        multiplicacao,
    ])

    ast = criar_ast("PROGRAMA", filhos=[
        criar_ast("CHAMADA_PRINT", filhos=[expressao])
    ])

    resultado = gerar_representacao_intermediaria(ast)

    assert "t1 = 11" in resultado["instrucoes"]


def test_nao_dobra_expressao_com_variavel():
    expressao = criar_ast("OPERACAO_BINARIA", {"operador": "+"}, [
        criar_ast("IDENTIFICADOR", {"nome": "a"}),
        criar_ast("LITERAL_INTEIRO", {"valor": 3}),
    ])

    ast = criar_ast("PROGRAMA", filhos=[
        criar_ast("CHAMADA_PRINT", filhos=[expressao])
    ])

    resultado = gerar_representacao_intermediaria(ast)

    assert "t1 = a + 3" in resultado["instrucoes"]


def test_dobra_constantes_multiplicacao():
    expressao = criar_ast("OPERACAO_BINARIA", {"operador": "*"}, [
        criar_ast("LITERAL_INTEIRO", {"valor": 10}),
        criar_ast("LITERAL_INTEIRO", {"valor": 2}),
    ])

    ast = criar_ast("PROGRAMA", filhos=[
        criar_ast("CHAMADA_PRINT", filhos=[expressao])
    ])

    resultado = gerar_representacao_intermediaria(ast)

    assert "t1 = 20" in resultado["instrucoes"]


def test_divisao_por_zero_nao_interrompe_geracao():
    expressao = criar_ast("OPERACAO_BINARIA", {"operador": "/"}, [
        criar_ast("LITERAL_INTEIRO", {"valor": 10}),
        criar_ast("LITERAL_INTEIRO", {"valor": 0}),
    ])

    ast = criar_ast("PROGRAMA", filhos=[
        criar_ast("CHAMADA_PRINT", filhos=[expressao])
    ])

    resultado = gerar_representacao_intermediaria(ast)

    assert resultado["sucesso"] is True
    assert "t1 = 10 / 0" in resultado["instrucoes"]
