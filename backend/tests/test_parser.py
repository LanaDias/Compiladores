
def test_ast_registra_intervalo_de_posicoes():
    codigo = "int x = 12;"

    scanner = Scanner(codigo)
    tokens, erros = scanner.analisar()

    assert erros == []

    parser = Parser(tokens)
    ast = parser.analisar()

    assert ast is not None
    assert ast.linha == 1
    assert ast.coluna == 1
    assert ast.coluna_fim == 12


def test_ast_precedencia_e_intervalo_da_operacao():
    codigo = "x = 10 + 5 * 2"

    scanner = Scanner(codigo)
    tokens, erros = scanner.analisar()

    assert erros == []

    parser = Parser(tokens)
    ast = parser.analisar()

    assert ast is not None
