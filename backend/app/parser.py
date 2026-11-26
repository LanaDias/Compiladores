
from app.ast_nodes import criar_no


class ErroSintatico(Exception):
    def __init__(
        self,
        mensagem: str,
        token: dict | None,
        esperado: list[str] | None = None,
    ):
        self.mensagem = mensagem
        self.token = token
        self.esperado = esperado or []
        super().__init__(mensagem)


class Parser:
    PRECEDENCIA = {
        "or": 1,
        "and": 2,
        "==": 3,
        "!=": 3,
        "<": 3,
        ">": 3,
        "<=": 3,
        ">=": 3,
        "+": 4,
        "-": 4,
        "*": 5,
        "/": 5,
        "%": 5,
    }

    def __init__(self, tokens: list[dict]):
        self.tokens = tokens
        self.posicao = 0
        self.erros = []

    def atual(self):
        if self.posicao < len(self.tokens):
            return self.tokens[self.posicao]
        return None

    def anterior(self):
        if self.posicao > 0:
            return self.tokens[self.posicao - 1]
        return None

    def avancar(self):
        token = self.atual()

        if token is not None:
            self.posicao += 1

        return token

    def verificar(self, lexema: str):
        token = self.atual()

        return (
            token is not None
            and token["lexema"] == lexema
        )

    def aceitar(self, lexema: str):
        if self.verificar(lexema):
            return self.avancar()

        return None

    def exigir(self, lexema: str):
        token = self.aceitar(lexema)

        if token is None:
            atual = self.atual()
            encontrado = (
                atual["lexema"]
                if atual
                else "fim do código"
            )

            raise ErroSintatico(
                f"Era esperado {lexema!r}, "
                f"mas foi encontrado {encontrado!r}.",
                atual,
                [lexema],
            )

        return token

    def erro(self, mensagem, esperado=None):
        raise ErroSintatico(
            mensagem,
            self.atual(),
            esperado,
        )

    def consumir_fim_instrucao(self, inicio):
        if self.aceitar(";"):
            return

        atual = self.atual()

        if atual is None or atual["lexema"] == "}":
            return

        if atual.get("linha", 0) > inicio.get("linha", 0):
            return

        self.erro(
            "Há um elemento inesperado depois do fim da instrução. "
            "Separe instruções com uma nova linha ou ponto e vírgula.",
            ["nova linha", ";"],
        )

    def analisar(self):
        inicio = self.tokens[0] if self.tokens else None
        comandos = []

        while self.atual() is not None:
            if self.aceitar(";"):
                continue

            posicao_anterior = self.posicao

            try:
                comandos.append(
                    self.declaracao_ou_comando()
                )

            except ErroSintatico as erro:
                self.registrar_erro(erro)
                self.recuperar()

            if self.posicao == posicao_anterior:
                self.avancar()

        raiz = criar_no(
            "PROGRAMA",
            filhos=comandos,
            token_inicio=inicio,
            token_fim=self.anterior(),
        )

        return {
            "sucesso": len(self.erros) == 0,
            "ast": raiz.to_dict(),
            "erros": self.erros,
        }

    def registrar_erro(self, erro):
        token = erro.token or self.anterior() or {}

        encontrado = token.get(
            "lexema",
            "fim do código",
        )

        linha = token.get("linha", 1)
        coluna = token.get("coluna", 1)

        self.erros.append({
            "tipo": "ERRO_SINTATICO",
            "linha": linha,
            "coluna": coluna,
            "encontrado": encontrado,
            "esperado": erro.esperado,
            "mensagem": (
                f"Erro sintático na linha {linha}, "
                f"coluna {coluna}: {erro.mensagem}"
            ),
        })

    def recuperar(self):
        if self.atual() is None:
            return

        linha_inicial = self.atual().get("linha", 1)

        while self.atual() is not None:
            token = self.atual()

            if token["lexema"] in (";", "}"):
                self.avancar()
                return

            if token.get("linha", 1) > linha_inicial:
                return

            self.avancar()

    def recuperar_bloco(self):
        if self.atual() is None:
            return

        linha_inicial = self.atual().get("linha", 1)

        while self.atual() is not None:
            token = self.atual()

            # Preserva o fechamento do bloco.
            if token["lexema"] == "}":
                return

            # Consome o ponto e vírgula.
            if token["lexema"] == ";":
                self.avancar()
                return

            # Permite tentar o próximo comando.
            if token.get("linha", 1) > linha_inicial:
                return

            self.avancar()

    def declaracao_ou_comando(self):
        token = self.atual()

        if token is None:
            self.erro("Era esperado um comando.")

        lexema = token["lexema"]

        if lexema in ("int", "float"):
            return self.declaracao_variavel()

        if lexema == "if":
            return self.condicional()

        if lexema == "while":
            return self.repeticao_while()

        if lexema == "print":
            return self.chamada_print()

        if lexema == "return":
            return self.retorno()

        if token["tipo"] == "IDENTIFICADOR":
            return self.atribuicao()

        self.erro(
            f"Não é possível iniciar uma instrução com {lexema!r}.",
            [
                "int",
                "float",
                "if",
                "while",
                "print",
                "return",
                "identificador",
            ],
        )

    def declaracao_variavel(self):
        inicio = self.avancar()
        tipo_dado = inicio["lexema"]

        identificador = self.atual()

        if (
            identificador is None
            or identificador["tipo"] != "IDENTIFICADOR"
        ):
            self.erro(
                "Era esperado um identificador depois "
                "do tipo da variável.",
                ["identificador"],
            )

        self.avancar()

        filhos = [
            criar_no(
                "IDENTIFICADOR",
                atributos={
                    "nome": identificador["lexema"]
                },
                token_inicio=identificador,
                token_fim=identificador,
            )
        ]

        if self.aceitar("="):
            filhos.append(self.expressao())

        fim = self.anterior()
        self.consumir_fim_instrucao(inicio)

        if self.anterior() is not None:
            fim = self.anterior()

        return criar_no(
            "DECLARACAO_VARIAVEL",
            atributos={"tipoDado": tipo_dado},
            filhos=filhos,
            token_inicio=inicio,
            token_fim=fim,
        )

    def atribuicao(self):
        inicio = self.avancar()
        nome = inicio["lexema"]

        self.exigir("=")
        valor = self.expressao()

        fim = self.anterior()
        self.consumir_fim_instrucao(inicio)

        if self.anterior() is not None:
            fim = self.anterior()

        identificador = criar_no(
            "IDENTIFICADOR",
            atributos={"nome": nome},
            token_inicio=inicio,
            token_fim=inicio,
        )

        return criar_no(
            "ATRIBUICAO",
            filhos=[identificador, valor],
            token_inicio=inicio,
            token_fim=fim,
        )

    def chamada_print(self):
        inicio = self.avancar()
        self.exigir("(")

        argumentos = []

        if not self.verificar(")"):
            argumentos.append(self.expressao())

            while self.aceitar(","):
                argumentos.append(self.expressao())

        fim = self.exigir(")")
        self.consumir_fim_instrucao(inicio)

        return criar_no(
            "CHAMADA_PRINT",
            filhos=argumentos,
            token_inicio=inicio,
            token_fim=fim,
        )

    def retorno(self):
        inicio = self.avancar()
        filhos = []

        atual = self.atual()

        if (
            atual is not None
            and atual["lexema"] not in (";", "}")
            and atual.get("linha") == inicio.get("linha")
        ):
            filhos.append(self.expressao())

        fim = self.anterior()
        self.consumir_fim_instrucao(inicio)

        if self.anterior() is not None:
            fim = self.anterior()

        return criar_no(
            "RETORNO",
            filhos=filhos,
            token_inicio=inicio,
            token_fim=fim,
        )

    def condicional(self):
        inicio = self.avancar()
        condicao = self.expressao()

        self.exigir(":")
        bloco_if = self.bloco_indentado(inicio)

        filhos = [condicao, bloco_if]

        atual = self.atual()

        if (
            atual is not None
            and atual["lexema"] == "else"
            and atual.get("coluna") == inicio.get("coluna")
        ):
            self.avancar()
            self.exigir(":")
            bloco_else = self.bloco_indentado(inicio)
            filhos.append(bloco_else)

        return criar_no(
            "CONDICIONAL",
            atributos={
                "possuiElse": len(filhos) == 3
            },
            filhos=filhos,
            token_inicio=inicio,
            token_fim=self.anterior(),
        )

    def repeticao_while(self):
        inicio = self.avancar()

        condicao = self.expressao()

        self.exigir(":")
        bloco = self.bloco_indentado(inicio)

        return criar_no(
            "REPETICAO_WHILE",
            filhos=[condicao, bloco],
            token_inicio=inicio,
            token_fim=self.anterior(),
        )

    def bloco_indentado(self, cabecalho):
        if self.aceitar("{"):
            inicio_bloco = self.anterior()
            comandos = []

            while (
                self.atual() is not None
                and not self.verificar("}")
            ):
                if self.aceitar(";"):
                    continue

                posicao_anterior = self.posicao

                try:
                    comandos.append(
                        self.declaracao_ou_comando()
                    )

                except ErroSintatico as erro:
                    self.registrar_erro(erro)
                    self.recuperar_bloco()

                if self.posicao == posicao_anterior:
                    self.avancar()

            fim_bloco = self.exigir("}")

            return criar_no(
                "BLOCO",
                filhos=comandos,
                token_inicio=inicio_bloco,
                token_fim=fim_bloco,
            )

        primeiro = self.atual()

        if primeiro is None:
            self.erro(
                "Era esperado um bloco depois de ':'.",
                ["indentação"],
            )

        if primeiro.get("linha", 0) <= cabecalho.get("linha", 0):
            self.erro(
                "Era esperado um bloco indentado na linha seguinte.",
                ["bloco indentado"],
            )

        indentacao = primeiro.get("coluna", 1)
        comandos = []

        while self.atual() is not None:
            atual = self.atual()

            if atual.get("coluna", 1) < indentacao:
                break

            if atual["lexema"] == "else":
                break

            posicao_anterior = self.posicao

            try:
                comandos.append(
                    self.declaracao_ou_comando()
                )

            except ErroSintatico as erro:
                self.registrar_erro(erro)
                self.recuperar_bloco()

            if self.posicao == posicao_anterior:
                self.avancar()

        if not comandos:
            self.erro(
                "O bloco precisa conter pelo menos um comando."
            )

        return criar_no(
            "BLOCO",
            filhos=comandos,
            token_inicio=primeiro,
            token_fim=self.anterior(),
        )

    def expressao(self, nivel_minimo=1):
        esquerda = self.fator()

        while self.atual() is not None:
            operador = self.atual()["lexema"]
            precedencia = self.PRECEDENCIA.get(
                operador,
                0,
            )

            if precedencia < nivel_minimo:
                break

            token_operador = self.avancar()
            direita = self.expressao(precedencia + 1)

            inicio_operacao = {
                "linha": esquerda.linha,
                "coluna": esquerda.coluna,
                "lexema": "",
            }

            esquerda = criar_no(
                "OPERACAO_BINARIA",
                atributos={
                    "operador": token_operador["lexema"]
                },
                filhos=[esquerda, direita],
                token_inicio=inicio_operacao,
                token_fim=self.anterior(),
            )

        return esquerda

    def fator(self):
        token = self.atual()

        if token is None:
            self.erro(
                "A expressão terminou antes de receber "
                "um operando.",
                [
                    "identificador",
                    "número",
                    "(",
                ],
            )

        # Operadores unários.
        if token["lexema"] in (
            "+",
            "-",
            "!",
            "not",
        ):
            operador = self.avancar()
            operando = self.fator()

            return criar_no(
                "OPERACAO_UNARIA",
                atributos={
                    "operador": (
                        "not"
                        if operador["lexema"] == "!"
                        else operador["lexema"]
                    )
                },
                filhos=[operando],
                token_inicio=operador,
                token_fim=self.anterior(),
            )

        # Expressões entre parênteses.
        if token["lexema"] == "(":
            inicio = self.avancar()
            expressao = self.expressao()
            fim = self.exigir(")")

            return criar_no(
                "AGRUPAMENTO",
                filhos=[expressao],
                token_inicio=inicio,
                token_fim=fim,
            )

        # Números inteiros.
        if token["tipo"] == "LITERAL_INTEIRO":
            self.avancar()

            return criar_no(
                "LITERAL_INTEIRO",
                atributos={
                    "valor": int(token["lexema"])
                },
                token_inicio=token,
                token_fim=token,
            )

        # Números reais.
        if token["tipo"] == "LITERAL_REAL":
            self.avancar()

            return criar_no(
                "LITERAL_REAL",
                atributos={
                    "valor": float(token["lexema"])
                },
                token_inicio=token,
                token_fim=token,
            )

        # Valores booleanos.
        if token["lexema"] in (
            "True",
            "False",
        ):
            self.avancar()

            return criar_no(
                "LITERAL_BOOLEANO",
                atributos={
                    "valor": token["lexema"] == "True"
                },
                token_inicio=token,
                token_fim=token,
            )

        # Identificadores.
        if token["tipo"] == "IDENTIFICADOR":
            self.avancar()

            return criar_no(
                "IDENTIFICADOR",
                atributos={
                    "nome": token["lexema"]
                },
                token_inicio=token,
                token_fim=token,
            )

        self.erro(
            f"Era esperado um operando, mas foi encontrado "
            f"{token['lexema']!r}.",
            [
                "identificador",
                "número",
                "True",
                "False",
                "(",
            ],
        )


def analisar_sintaticamente(tokens: list[dict]) -> dict:
    return Parser(tokens).analisar()
