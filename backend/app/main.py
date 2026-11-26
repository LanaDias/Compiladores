
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from app.scanner import analisar_lexicamente
from app.parser import analisar_sintaticamente
from app.semantic import analisar_semanticamente
from app.ir import gerar_representacao_intermediaria


app = FastAPI(
    title="CompilaLab API",
    description="Analisador léxico, sintático, semântico e gerador de IR",
    version="5.2.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
        "http://localhost:8081",
        "http://127.0.0.1:8081",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CodigoEntrada(BaseModel):
    codigo: str = Field(max_length=20000)


@app.get("/")
def inicio():
    return {"mensagem": "CompilaLab API funcionando"}


@app.get("/api/hello")
def hello():
    return {"project": "CompilaLab"}


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.post("/api/analisar")
def analisar(entrada: CodigoEntrada):
    codigo = entrada.codigo

    if not codigo.strip():
        raise HTTPException(
            status_code=400,
            detail="O código não pode estar vazio.",
        )

    # 1. ANÁLISE LÉXICA
    resultado_lexico = analisar_lexicamente(codigo)

    tokens = resultado_lexico["tokens"]
    erros_lexicos = resultado_lexico["erros"]

    resultado = {
        "mensagem": "Análise concluída",
        "recebido": True,
        "tamanho": len(codigo),
        "codigo": codigo,

        # Compatibilidade com o frontend atual.
        "sucesso": resultado_lexico["sucesso"],
        "tokens": tokens,
        "erros": erros_lexicos,

        "lexico": resultado_lexico,

        "sintatico": {
            "sucesso": False,
            "ast": None,
            "erros": [],
            "mensagem": "Análise sintática não executada.",
            "ignorada": True,
        },

        "semantico": {
            "sucesso": False,
            "erros": [],
            "tabelaSimbolos": [],
            "mensagem": "Análise semântica não executada.",
            "ignorada": True,
        },

        "ir": {
            "sucesso": False,
            "instrucoes": [],
            "codigo": "",
            "mensagem": "Representação intermediária não gerada.",
            "ignorada": True,
        },
    }

    # Se houver erro léxico, as próximas etapas são interrompidas.
    if erros_lexicos:
        resultado["sintatico"]["mensagem"] = (
            "Análise sintática não executada devido a erros léxicos."
        )

        resultado["semantico"]["mensagem"] = (
            "Análise semântica não executada devido a erros léxicos."
        )

        resultado["ir"]["mensagem"] = (
            "Representação intermediária não gerada devido a erros léxicos."
        )

        return resultado

    # 2. ANÁLISE SINTÁTICA
    try:
        resultado_sintatico = analisar_sintaticamente(tokens)

        erros_sintaticos = resultado_sintatico.get("erros", [])
        sintaxe_valida = resultado_sintatico.get("sucesso", False)

        # A AST só é disponibilizada quando a sintaxe é válida.
        ast = resultado_sintatico.get("ast") if sintaxe_valida else None

        resultado["sintatico"] = {
            "sucesso": sintaxe_valida,
            "ast": ast,
            "erros": erros_sintaticos,
            "mensagem": (
                "Código sintaticamente válido."
                if sintaxe_valida
                else "Foram encontrados erros sintáticos."
            ),
            "ignorada": False,
        }

    except Exception as erro:
        ast = None

        resultado["sintatico"] = {
            "sucesso": False,
            "ast": None,
            "erros": [
                {
                    "tipo": "ERRO_SINTATICO",
                    "regra": "FALHA_ANALISE_SINTATICA",
                    "mensagem": (
                        "Falha durante a análise sintática: "
                        + str(erro)
                    ),
                    "linha": 1,
                    "coluna": 1,
                }
            ],
            "mensagem": "Falha durante a análise sintática.",
            "ignorada": False,
        }

    # Se a sintaxe falhar, a análise semântica e a IR são ignoradas.
    if not resultado["sintatico"]["sucesso"]:
        resultado["semantico"]["mensagem"] = (
            "Análise semântica não executada devido a erros sintáticos."
        )

        resultado["ir"]["mensagem"] = (
            "Representação intermediária não gerada devido a erros sintáticos."
        )

        return resultado

    # 3. ANÁLISE SEMÂNTICA
    try:
        resultado_semantico = analisar_semanticamente(ast)

        resultado["semantico"] = {
            "sucesso": resultado_semantico["sucesso"],
            "erros": resultado_semantico["erros"],
            "tabelaSimbolos": resultado_semantico.get(
                "tabelaSimbolos", []
            ),
            "mensagem": (
                "Código semanticamente válido."
                if resultado_semantico["sucesso"]
                else "Foram encontrados erros semânticos."
            ),
            "ignorada": False,
        }

    except Exception as erro:
        resultado["semantico"] = {
            "sucesso": False,
            "erros": [
                {
                    "tipo": "ERRO_SEMANTICO",
                    "regra": "FALHA_ANALISE_SEMANTICA",
                    "mensagem": (
                        "Falha durante a análise semântica: "
                        + str(erro)
                    ),
                    "linha": 1,
                    "coluna": 1,
                }
            ],
            "tabelaSimbolos": [],
            "mensagem": "Falha durante a análise semântica.",
            "ignorada": False,
        }

    # 4. GERAÇÃO DA REPRESENTAÇÃO INTERMEDIÁRIA
    if resultado["semantico"]["sucesso"]:
        try:
            resultado_ir = gerar_representacao_intermediaria(ast)

            resultado["ir"] = {
                "sucesso": resultado_ir["sucesso"],
                "instrucoes": resultado_ir["instrucoes"],
                "codigo": resultado_ir["codigo"],
                "mensagem": (
                    "Representação intermediária gerada com sucesso."
                    if resultado_ir["sucesso"]
                    else "Não foi possível gerar a representação intermediária."
                ),
                "ignorada": False,
            }

        except Exception as erro:
            resultado["ir"] = {
                "sucesso": False,
                "instrucoes": [],
                "codigo": "",
                "mensagem": (
                    "Falha ao gerar representação intermediária: "
                    + str(erro)
                ),
                "ignorada": False,
            }

    else:
        resultado["ir"]["mensagem"] = (
            "Representação intermediária não gerada devido a erros semânticos."
        )

    return resultado
