from app.scanner import analisar_lexicamente
from app.parser import analisar_sintaticamente
from app.semantic import analisar_semanticamente


def analisar_codigo(codigo):
    lexico = analisar_lexicamente(codigo)
    assert lexico["erros"] == []

    sintatico = analisar_sintaticamente(lexico["tokens"])
    assert sintatico["sucesso"] is True, sintatico["erros"]

    return analisar_semanticamente(sintatico["ast"])


def test_variavel_declarada_sem_erros():
    resultado = analisar_codigo("int x = 10;")

    assert resultado["sucesso"] is True
    assert resultado["erros"] == []


def test_identifica_variavel_nao_declarada():
    resultado = analisar_codigo("print(x);")

    assert resultado["sucesso"] is False
    assert any(
        "não foi declarada" in erro["mensagem"]
        for erro in resultado["erros"]
    )


def test_identifica_declaracao_duplicada():
    resultado = analisar_codigo(
        "int x = 10;\nint x = 20;"
    )

    assert resultado["sucesso"] is False
    assert any(
        "já foi declarada" in erro["mensagem"]
        for erro in resultado["erros"]
    )


def test_identifica_tipo_incompativel():
    resultado = analisar_codigo("int x = 10.5;")

    assert resultado["sucesso"] is False
    assert any(
        "Não é possível inicializar" in erro["mensagem"]
        for erro in resultado["erros"]
    )


def test_identifica_variavel_nao_declarada_em_expressao():
    resultado = analisar_codigo(
        "int x = 10;\nint y = x + z;"
    )

    assert resultado["sucesso"] is False
    assert any(
        "'z' não foi declarada" in erro["mensagem"]
        for erro in resultado["erros"]
    )


def test_aceita_atribuicao_compativel():
    resultado = analisar_codigo(
        "int x = 10;\nx = 20;"
    )

    assert resultado["sucesso"] is True
    assert resultado["erros"] == []


def test_rejeita_condicao_if_nao_booleana():
    resultado = analisar_codigo(
        "if (10): {\n"
        "    print(10);\n"
        "}"
    )

    assert resultado["sucesso"] is False
    assert len(resultado["erros"]) > 0


def test_rejeita_condicao_while_nao_booleana():
    resultado = analisar_codigo(
        "while (10): {\n"
        "    print(10);\n"
        "}"
    )

    assert resultado["sucesso"] is False
    assert len(resultado["erros"]) > 0


def test_aceita_sombreamento_em_bloco_interno():
    resultado = analisar_codigo(
        "int x = 10;\n"
        "if (True): {\n"
        "    int x = 20;\n"
        "    print(x);\n"
        "}\n"
        "print(x);"
    )

    assert resultado["sucesso"] is True
    assert resultado["erros"] == []


def test_tabela_de_simbolos_contem_dados_da_variavel():
    resultado = analisar_codigo("int numero = 10;")

    assert resultado["sucesso"] is True

    simbolo = resultado["tabelaSimbolos"][0]

    assert simbolo["nome"] == "numero"
    assert simbolo["tipo"] == "int"
    assert simbolo["escopo"] == "global"
    assert simbolo["linha"] == 1
    assert simbolo["coluna"] > 0
    assert simbolo["inicializado"] is True