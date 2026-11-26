
SEM_CONSTANTE = object()


class GeradorIR:
    def __init__(self):
        self.instrucoes = []
        self.contador_temporario = 0
        self.contador_rotulo = 0

    def novo_temporario(self):
        self.contador_temporario += 1
        return f"t{self.contador_temporario}"

    def novo_rotulo(self):
        self.contador_rotulo += 1
        return f"L{self.contador_rotulo}"

    def emitir(self, instrucao):
        self.instrucoes.append(instrucao)

    def gerar(self, ast):
        if not isinstance(ast, dict) or ast.get("tipo") != "PROGRAMA":
            raise ValueError("A AST fornecida não representa um programa válido.")

        self.visitar(ast)

        return {
            "sucesso": True,
            "instrucoes": self.instrucoes,
            "codigo": "\n".join(self.instrucoes),
        }

    def avaliar_constante(self, no):
        tipo = no.get("tipo")
        atributos = no.get("atributos", {})
        filhos = no.get("filhos", [])

        if tipo == "LITERAL_INTEIRO":
            return atributos["valor"]

        if tipo == "LITERAL_REAL":
            return atributos["valor"]

        if tipo == "LITERAL_BOOLEANO":
            return atributos["valor"]

        if tipo == "AGRUPAMENTO":
            return self.avaliar_constante(filhos[0])

        if tipo == "OPERACAO_UNARIA":
            valor = self.avaliar_constante(filhos[0])

            if valor is SEM_CONSTANTE:
                return SEM_CONSTANTE

            operador = atributos["operador"]

            try:
                if operador == "-":
                    return -valor
                if operador == "+":
                    return +valor
                if operador == "!":
                    return not valor
                if operador == "not":
                    return not valor
            except (TypeError, ValueError):
                return SEM_CONSTANTE

            return SEM_CONSTANTE

        if tipo == "OPERACAO_BINARIA":
            esquerda = self.avaliar_constante(filhos[0])
            direita = self.avaliar_constante(filhos[1])

            if esquerda is SEM_CONSTANTE or direita is SEM_CONSTANTE:
                return SEM_CONSTANTE

            operador = atributos["operador"]

            operacoes = {
                "+": lambda a, b: a + b,
                "-": lambda a, b: a - b,
                "*": lambda a, b: a * b,
                "/": lambda a, b: a / b,
                "%": lambda a, b: a % b,
                "==": lambda a, b: a == b,
                "!=": lambda a, b: a != b,
                "<": lambda a, b: a < b,
                ">": lambda a, b: a > b,
                "<=": lambda a, b: a <= b,
                ">=": lambda a, b: a >= b,
                "and": lambda a, b: a and b,
                "or": lambda a, b: a or b,
            }

            operacao = operacoes.get(operador)

            if operacao is None:
                return SEM_CONSTANTE

            try:
                return operacao(esquerda, direita)
            except (ArithmeticError, TypeError, ValueError):
                return SEM_CONSTANTE

        return SEM_CONSTANTE

    def visitar(self, no):
        tipo = no.get("tipo")
        atributos = no.get("atributos", {})
        filhos = no.get("filhos", [])

        if tipo == "PROGRAMA" or tipo == "BLOCO":
            for filho in filhos:
                self.visitar(filho)

        elif tipo == "DECLARACAO_VARIAVEL":
            identificador = filhos[0]["atributos"]["nome"]
            tipo_dado = atributos["tipoDado"]

            self.emitir(f"DECLARE {identificador} : {tipo_dado}")

            if len(filhos) > 1:
                valor = self.expressao(filhos[1])
                self.emitir(f"{identificador} = {valor}")

        elif tipo == "ATRIBUICAO":
            identificador = filhos[0]["atributos"]["nome"]
            valor = self.expressao(filhos[1])
            self.emitir(f"{identificador} = {valor}")

        elif tipo == "CHAMADA_PRINT":
            for argumento in filhos:
                valor = self.expressao(argumento)
                self.emitir(f"PRINT {valor}")

        elif tipo == "RETORNO":
            if filhos:
                valor = self.expressao(filhos[0])
                self.emitir(f"RETURN {valor}")
            else:
                self.emitir("RETURN")

        elif tipo == "CONDICIONAL":
            condicao = self.expressao(filhos[0])
            rotulo_else = self.novo_rotulo()
            rotulo_fim = self.novo_rotulo()

            if len(filhos) == 3:
                self.emitir(f"IF_FALSE {condicao} GOTO {rotulo_else}")
                self.visitar(filhos[1])
                self.emitir(f"GOTO {rotulo_fim}")
                self.emitir(f"LABEL {rotulo_else}")
                self.visitar(filhos[2])
                self.emitir(f"LABEL {rotulo_fim}")
            else:
                self.emitir(f"IF_FALSE {condicao} GOTO {rotulo_fim}")
                self.visitar(filhos[1])
                self.emitir(f"LABEL {rotulo_fim}")

        elif tipo == "REPETICAO_WHILE":
            rotulo_inicio = self.novo_rotulo()
            rotulo_fim = self.novo_rotulo()

            self.emitir(f"LABEL {rotulo_inicio}")
            condicao = self.expressao(filhos[0])
            self.emitir(f"IF_FALSE {condicao} GOTO {rotulo_fim}")
            self.visitar(filhos[1])
            self.emitir(f"GOTO {rotulo_inicio}")
            self.emitir(f"LABEL {rotulo_fim}")

        else:
            raise ValueError(f"Tipo de nó não suportado na IR: {tipo}")

    def expressao(self, no):
        tipo = no.get("tipo")
        atributos = no.get("atributos", {})
        filhos = no.get("filhos", [])

        if tipo in ("LITERAL_INTEIRO", "LITERAL_REAL", "LITERAL_BOOLEANO"):
            return str(atributos["valor"])

        if tipo == "IDENTIFICADOR":
            return atributos["nome"]

        if tipo == "AGRUPAMENTO":
            return self.expressao(filhos[0])

        if tipo in ("OPERACAO_UNARIA", "OPERACAO_BINARIA"):
            constante = self.avaliar_constante(no)

            if constante is not SEM_CONSTANTE:
                temporario = self.novo_temporario()
                self.emitir(f"{temporario} = {constante}")
                return temporario

        if tipo == "OPERACAO_UNARIA":
            operando = self.expressao(filhos[0])
            temporario = self.novo_temporario()
            operador = atributos["operador"]

            self.emitir(f"{temporario} = {operador}{operando}")
            return temporario

        if tipo == "OPERACAO_BINARIA":
            esquerda = self.expressao(filhos[0])
            direita = self.expressao(filhos[1])
            temporario = self.novo_temporario()
            operador = atributos["operador"]

            self.emitir(
                f"{temporario} = {esquerda} {operador} {direita}"
            )
            return temporario

        raise ValueError(
            f"Tipo de expressão não suportado na IR: {tipo}"
        )


def gerar_representacao_intermediaria(ast):
    gerador = GeradorIR()
    return gerador.gerar(ast)
