from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="CompilaLab API",
    description="API inicial do ambiente educacional de compiladores.",
    version="0.1.0",
)

# Na primeira etapa, o frontend está em outro serviço/porta.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)

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
