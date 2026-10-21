from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(
    title="CompilaLab API",
    description="API educacional para receber e validar código-fonte.",
    version="0.2.0",
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
        "stage": "estrutura inicial",
    }


@app.post("/api/analisar")
def analisar(request: CodigoRequest):
    codigo = request.codigo

    if not codigo.strip():
        raise HTTPException(
            status_code=400,
            detail="O código não pode estar vazio.",
        )

    return {
        "mensagem": "Código recebido com sucesso.",
        "recebido": True,
        "tamanho": len(codigo),
        "codigo": codigo,
        "observacao": (
            "A análise léxica e sintática ainda não foi implementada."
        ),
    }