
# CompilaLab

Projeto acadêmico de construção de um compilador.

## Funcionalidades

- Análise léxica.
- Identificação de tokens.
- Análise sintática.
- Parser descendente recursivo.
- Construção da Árvore Sintática Abstrata (AST).
- Registro de erros sintáticos.
- API com FastAPI.
- Interface web.
- Execução com Docker Compose.

## Executar com Docker

Na pasta que contém o `docker-compose.yml`:

```powershell
docker compose up --build -d
```

Interface:

http://localhost:8081

Documentação da API:

http://localhost:8000/docs

## Executar testes

```powershell
docker compose exec backend python -m pytest -v
```

## Etapa 4

A Etapa 4 acrescenta análise sintática, construção da AST, registro de posições dos nós e apresentação dos resultados na interface.

A gramática está documentada em:

`docs/pesquisa/gramatica.md`

Os testes estão documentados em:

`docs/pesquisa/testes_etapa4.md`
