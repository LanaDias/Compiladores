
from app.scanner import analisar_lexicamente
from app.parser import analisar_sintaticamente


def analisar_codigo(codigo):
    resultado_lexico = analisar_lexicamente(codigo)

    assert resultado_lexico["erros"] == []

    resultado_sintatico = analisar_sintaticamente(
        resultado_lexico["tokens"]
    )

    assert resultado_sintatico["sucesso"] is True

    return resultado_sintatico["ast"]


def test_ast_registra_intervalo_de_posicoes():
    codigo = "int x = 12;"

    ast = analisar_codigo(codigo)

    assert ast is not None
    assert ast["tipo"] == "PROGRAMA"
    assert ast["linha"] == 1
    assert ast["coluna"] == 1
    assert ast["colunaFim"] == 12


def test_ast_precedencia_e_intervalo_da_operacao():
    codigo = "x = 10 + 5 * 2"

    ast = analisar_codigo(codigo)

    atribuicao = ast["filhos"][0]

    assert atribuicao["tipo"] == "ATRIBUICAO"

    operacao_soma = atribuicao["filhos"][1]

    assert operacao_soma["tipo"] == "OPERACAO_BINARIA"
    assert operacao_soma["atributos"]["operador"] == "+"

    operacao_multiplicacao = operacao_soma["filhos"][1]

    assert operacao_multiplicacao["tipo"] == "OPERACAO_BINARIA"
    assert operacao_multiplicacao["atributos"]["operador"] == "*"

    # A multiplicação deve estar dentro da soma na AST.
    assert operacao_soma["filhos"][0]["tipo"] == "LITERAL_INTEIRO"
    assert operacao_multiplicacao["filhos"][0]["atributos"]["valor"] == 5
    assert operacao_multiplicacao["filhos"][1]["atributos"]["valor"] == 2

    # Verifica o intervalo da operação.
    assert operacao_soma["linha"] == 1
    assert operacao_soma["coluna"] == 5
    assert operacao_soma["colunaFim"] == 15

    assert operacao_multiplicacao["coluna"] == 10
    assert operacao_multiplicacao["colunaFim"] == 15
