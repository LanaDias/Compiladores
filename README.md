# CompilaLab — ambiente educacional de compiladores

Projeto acadêmico em desenvolvimento para apoiar o ensino de construção de compiladores por meio de uma aplicação web interativa.

## Escopo inicial
- Linguagem-alvo do analisador: subconjunto didático inspirado em Python.
- Primeira entrega: aplicação web mínima com frontend, backend e Docker Compose.
- Próximas etapas previstas: análise léxica, análise sintática, análise semântica, representação intermediária, otimização e geração de código.

> Este repositório é um esqueleto inicial. Ainda não implementa as fases do compilador.

## Tecnologias
- Frontend: HTML, CSS e JavaScript (versão mínima para facilitar a primeira execução).
- Backend: Python e FastAPI.
- Ambiente: Docker e Docker Compose.

## Pré-requisitos
- Git
- Docker Engine ou Docker Desktop com Docker Compose
- Navegador moderno

## Executar
Na raiz do projeto:

```bash
docker compose up --build
```

Abra http://localhost:8080 no navegador.

## Encerrar
```bash
docker compose down
```

## Testar a API diretamente
Abra http://localhost:8000/api/hello ou acesse http://localhost:8000/docs.

## Estrutura
```text
compilalab/
├── backend/
│   ├── app/main.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── tests/
├── frontend/
│   ├── index.html
│   └── Dockerfile
├── docs/
│   └── pesquisa/
├── docker-compose.yml
└── README.md
```

## Subconjunto inicial proposto
O compilador didático será implementado progressivamente. O primeiro subconjunto previsto inclui:
- números inteiros;
- identificadores;
- operadores `+`, `-`, `*`, `/`;
- parênteses;
- atribuições simples.

A gramática e as regras serão documentadas e testadas antes de ampliar o subconjunto. O objetivo não é implementar toda a linguagem Python.

## Pesquisa acadêmica
Os artigos usados para justificar a ferramenta devem ser lidos e fichados antes da versão final do trabalho. Registre as referências, as bases pesquisadas, os termos de busca e a data de acesso em `docs/pesquisa/`.

## Compartilhamento com o professor
Crie um repositório no GitHub sob sua conta e compartilhe o link com o professor conforme as instruções da disciplina. O identificador informado para o professor é `rocha3runo`; confirme no GitHub o perfil correto antes de conceder acesso.

## Limitações atuais
- Não há compilador implementado ainda.
- A página inicial apenas testa a comunicação com o backend.
- A avaliação educacional ainda será planejada e conduzida; não existem resultados experimentais neste repositório.
