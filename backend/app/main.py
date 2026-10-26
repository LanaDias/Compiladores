
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.scanner import analisar_lexicamente

app = FastAPI(
    title="CompilaLab API",
    description="API educacional para análise léxica de código-fonte.",
    version="0.3.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


class CodigoRequest(BaseModel):
    codigo: str


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/hello")
def hello():
    return {
        "message": "Hello, World!",
        "project": "CompilaLab",
        "stage": "análise léxica",
    }


@app.post("/api/analisar")
def analisar(request: CodigoRequest):
    codigo = request.codigo

    if not codigo.strip():
        raise HTTPException(
            status_code=400,
            detail="O código não pode estar vazio.",
        )

    resultado = analisar_lexicamente(codigo)

    return {
        "mensagem": (
            "Análise léxica concluída."
            if resultado["sucesso"]
            else "Análise léxica concluída com erros."
        ),
        "recebido": True,
        "tamanho": len(codigo),
        "codigo": codigo,
        "sucesso": resultado["sucesso"],
        "tokens": resultado["tokens"],
        "erros": resultado["erros"],
    }
