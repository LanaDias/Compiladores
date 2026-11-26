
class AnalisadorSemantico:
    def __init__(self):
        self.escopos = [{}]
        self.nomes_escopos = ["global"]
        self.erros = []
        self.tabela_simbolos = []
        self.contador_escopos = 0

    def erro(self, mensagem, no, regra, sugestao=None):
        diagnostico = {
            "tipo": "ERRO_SEMANTICO",
            "regra": regra,
            "mensagem": mensagem,
            "linha": no.get("linha", 1),
            "coluna": no.get("coluna", 1),
        }

        if sugestao:
            diagnostico["sugestao"] = sugestao

        self.erros.append(diagnostico)

    def buscar_variavel(self, nome):
        for escopo in reversed(self.escopos):
            if nome in escopo:
                return escopo[nome]

        return None

    def abrir_escopo(self, no):
        self.contador_escopos += 1

        nome = (
            f"bloco_{self.contador_escopos}"
            f"_linha_{no.get('linha', 1)}"
        )

        caminho = f"{self.nomes_escopos[-1]}/{nome}"

        self.escopos.append({})
        self.nomes_escopos.append(caminho)

    def fechar_escopo(self):
        self.escopos.pop()
        self.nomes_escopos.pop()

    def analisar(self, ast):
        if ast is not None:
            self.analisar_no(ast)

        return {
            "sucesso": len(self.erros) == 0,
            "erros": self.erros,
            "tabelaSimbolos": self.tabela_simbolos,
        }

    def analisar_no(self, no):
        if not isinstance(no, dict):
            return

        tipo = no.get("tipo")
        filhos = no.get("filhos", [])
        atributos = no.get("atributos", {})

        if tipo == "PROGRAMA":
            for filho in filhos:
                self.analisar_no(filho)

        elif tipo == "BLOCO":
            self.abrir_escopo(no)

            for filho in filhos:
                self.analisar_no(filho)

            self.fechar_escopo()

        elif tipo == "DECLARACAO_VARIAVEL":
            if not filhos:
                return

            identificador = filhos[0]
            nome = identificador["atributos"]["nome"]
            tipo_dado = atributos.get("tipoDado")

            escopo_atual = self.escopos[-1]

            if nome in escopo_atual:
                self.erro(
                    f"A variável '{nome}' já foi declarada neste escopo.",
                    identificador,
                    "IDENTIFICADOR_REDECLARADO",
                    "Escolha outro nome ou utilize a variável já declarada.",
                )
                return

            simbolo = {
                "nome": nome,
                "tipo": tipo_dado,
                "escopo": self.nomes_escopos[-1],
                "linha": identificador.get("linha", 1),
                "coluna": identificador.get("coluna", 1),
                "inicializado": len(filhos) > 1,
                "usado": False,
            }

            escopo_atual[nome] = simbolo
            self.tabela_simbolos.append(simbolo)

            if len(filhos) > 1:
                tipo_expressao = self.analisar_expressao(filhos[1])

                if not self.tipo_compativel(tipo_dado, tipo_expressao):
                    self.erro(
                        f"Não é possível inicializar a variável "
                        f"'{nome}' do tipo {tipo_dado} "
                        f"com um valor do tipo {tipo_expressao}.",
                        no,
                        "TIPO_INCOMPATIVEL_INICIALIZACAO",
                        "Utilize um valor compatível com o tipo declarado.",
                    )

        elif tipo == "ATRIBUICAO":
            if len(filhos) < 2:
                return

            identificador = filhos[0]
            nome = identificador["atributos"]["nome"]

            simbolo = self.buscar_variavel(nome)

            if simbolo is None:
                self.erro(
                    f"A variável '{nome}' não foi declarada.",
                    identificador,
                    "IDENTIFICADOR_NAO_DECLARADO",
                    "Declare a variável antes de utilizá-la.",
                )

                self.analisar_expressao(filhos[1])
                return

            tipo_expressao = self.analisar_expressao(filhos[1])

            if not self.tipo_compativel(
                simbolo["tipo"], tipo_expressao
            ):
                self.erro(
                    f"Não é possível atribuir um valor do tipo "
                    f"{tipo_expressao} à variável '{nome}' "
                    f"do tipo {simbolo['tipo']}.",
                    no,
                    "TIPO_INCOMPATIVEL_ATRIBUICAO",
                    "Atribua um valor compatível com o tipo da variável.",
                )

            elif tipo_expressao is not None:
                simbolo["inicializado"] = True

        elif tipo == "CHAMADA_PRINT":
            for filho in filhos:
                self.analisar_expressao(filho)

        elif tipo == "RETORNO":
            for filho in filhos:
                self.analisar_expressao(filho)

        elif tipo == "CONDICIONAL":
            if not filhos:
                return

            tipo_condicao = self.analisar_expressao(filhos[0])
            self.verificar_condicao(tipo_condicao, filhos[0])

            if len(filhos) > 1:
                self.analisar_no(filhos[1])

            if len(filhos) > 2:
                self.analisar_no(filhos[2])

        elif tipo == "REPETICAO_WHILE":
            if not filhos:
                return

            tipo_condicao = self.analisar_expressao(filhos[0])
            self.verificar_condicao(tipo_condicao, filhos[0])

            if len(filhos) > 1:
                self.analisar_no(filhos[1])

    def verificar_condicao(self, tipo_condicao, no):
        if tipo_condicao is None:
            return

        if tipo_condicao != "bool":
            self.erro(
                "A condição deve resultar em um valor booleano.",
                no,
                "CONDICAO_NAO_BOOLEANA",
                "Utilize uma expressão lógica ou uma comparação.",
            )

    def analisar_expressao(self, no):
        if not isinstance(no, dict):
            return None

        tipo = no.get("tipo")
        filhos = no.get("filhos", [])
        atributos = no.get("atributos", {})

        if tipo == "LITERAL_INTEIRO":
            return "int"

        if tipo == "LITERAL_REAL":
            return "float"

        if tipo == "LITERAL_BOOLEANO":
            return "bool"

        if tipo == "IDENTIFICADOR":
            nome = atributos.get("nome")
            simbolo = self.buscar_variavel(nome)

            if simbolo is None:
                self.erro(
                    f"A variável '{nome}' não foi declarada.",
                    no,
                    "IDENTIFICADOR_NAO_DECLARADO",
                    "Declare a variável antes de utilizá-la.",
                )
                return None

            simbolo["usado"] = True
            return simbolo["tipo"]

        if tipo == "AGRUPAMENTO":
            if filhos:
                return self.analisar_expressao(filhos[0])

            return None

        if tipo == "OPERACAO_UNARIA":
            if not filhos:
                return None

            operador = atributos.get("operador")
            tipo_operando = self.analisar_expressao(filhos[0])

            if tipo_operando is None:
                return None

            if operador in ("not", "!"):
                if tipo_operando != "bool":
                    self.erro(
                        "O operador lógico 'not' exige um valor booleano.",
                        no,
                        "OPERADOR_LOGICO_TIPO_INVALIDO",
                        "Utilize uma expressão booleana com 'not'.",
                    )
                    return None

                return "bool"

            if operador in ("+", "-"):
                if tipo_operando not in ("int", "float"):
                    self.erro(
                        "O operador unário exige um valor numérico.",
                        no,
                        "OPERADOR_UNARIO_TIPO_INVALIDO",
                        "Utilize um operando do tipo int ou float.",
                    )
                    return None

                return tipo_operando

        if tipo == "OPERACAO_BINARIA":
            if len(filhos) < 2:
                return None

            operador = atributos.get("operador")

            tipo_esquerda = self.analisar_expressao(filhos[0])
            tipo_direita = self.analisar_expressao(filhos[1])

            if tipo_esquerda is None or tipo_direita is None:
                return None

            numericos = ("int", "float")

            if operador in ("+", "-", "*", "/", "%"):
                if (
                    tipo_esquerda not in numericos
                    or tipo_direita not in numericos
                ):
                    self.erro(
                        f"O operador '{operador}' exige operandos numéricos.",
                        no,
                        "OPERACAO_ARITMETICA_TIPO_INVALIDO",
                        "Utilize operandos do tipo int ou float.",
                    )
                    return None

                if operador == "/" or "float" in (
                    tipo_esquerda, tipo_direita
                ):
                    return "float"

                return "int"

            if operador in ("<", ">", "<=", ">="):
                if (
                    tipo_esquerda not in numericos
                    or tipo_direita not in numericos
                ):
                    self.erro(
                        f"O operador '{operador}' exige operandos numéricos.",
                        no,
                        "COMPARACAO_TIPO_INVALIDO",
                        "Compare valores numéricos.",
                    )
                    return None

                return "bool"

            if operador in ("==", "!="):
                tipos_compativeis = (
                    tipo_esquerda == tipo_direita
                    or (
                        tipo_esquerda in numericos
                        and tipo_direita in numericos
                    )
                )

                if not tipos_compativeis:
                    self.erro(
                        "A comparação exige operandos de tipos compatíveis.",
                        no,
                        "COMPARACAO_TIPO_INVALIDO",
                        "Compare valores de tipos compatíveis.",
                    )
                    return None

                return "bool"

            if operador in ("and", "or"):
                if (
                    tipo_esquerda != "bool"
                    or tipo_direita != "bool"
                ):
                    self.erro(
                        f"O operador lógico '{operador}' exige "
                        "operandos booleanos.",
                        no,
                        "OPERADOR_LOGICO_TIPO_INVALIDO",
                        "Utilize expressões que resultem em valores booleanos.",
                    )
                    return None

                return "bool"

        return None

    def tipo_compativel(self, tipo_variavel, tipo_valor):
        if tipo_valor is None:
            return True

        if tipo_variavel == tipo_valor:
            return True

        # Um inteiro pode ser atribuído a uma variável real.
        if tipo_variavel == "float" and tipo_valor == "int":
            return True

        return False


def analisar_semanticamente(ast):
    analisador = AnalisadorSemantico()
    return analisador.analisar(ast)
