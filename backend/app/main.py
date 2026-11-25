from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.scanner import analisar_lexicamente
from app.parser import analisar_sintaticamente


app = FastAPI(
    title="CompilaLab API",
    description="Analisador léxico e sintático",
    version="4.0.0",
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
    codigo: str


@app.get("/")
def inicio():
    return {"mensagem": "CompilaLab API funcionando"}


@app.post("/api/analisar")
def analisar(entrada: CodigoEntrada):
    codigo = entrada.codigo

    resultado_lexico = analisar_lexicamente(codigo)
    tokens = resultado_lexico["tokens"]
    erros_lexicos = resultado_lexico["erros"]

    resultado = {
        "mensagem": "Análise concluída",
        "recebido": True,
        "tamanho": len(codigo),
        "codigo": codigo,
        "sucesso": resultado_lexico["sucesso"],
        "tokens": tokens,
        "erros": erros_lexicos,
        "lexico": resultado_lexico,
        "sintatico": {
            "sucesso": False,
            "ast": None,
            "erros": [],
            "mensagem": "",
            "ignorada": False,
        },
    }

    if erros_lexicos:
        resultado["sintatico"]["mensagem"] = (
            "Análise sintática não executada devido a erros léxicos."
        )
        resultado["sintatico"]["ignorada"] = True
        return resultado

    try:
        resultado_sintatico = analisar_sintaticamente(tokens)

        resultado["sintatico"] = {
            "sucesso": resultado_sintatico["sucesso"],
            "ast": resultado_sintatico["ast"],
            "erros": resultado_sintatico["erros"],
            "mensagem": (
                "Código sintaticamente válido."
                if resultado_sintatico["sucesso"]
                else "Foram encontrados erros sintáticos."
            ),
            "ignorada": False,
        }

    except Exception as erro:
        resultado["sintatico"] = {
            "sucesso": False,
            "ast": None,
            "erros": [str(erro)],
            "mensagem": "Falha durante a análise sintática.",
            "ignorada": False,
        }

    return resultado

@app.get("/api/health")
def health():
    return {"status": "ok"}
