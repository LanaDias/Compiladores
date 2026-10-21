# CompilaLab — Ambiente Educacional de Compiladores

## 1. Objetivo

O CompilaLab é um projeto acadêmico que tem como objetivo apoiar o aprendizado dos conceitos de construção de compiladores por meio de uma aplicação web interativa.

Nesta segunda etapa, o foco é permitir que o usuário insira ou edite código-fonte, selecione exemplos e envie o conteúdo para uma API responsável por receber e validar a entrada.

## 2. Linguagem e escopo

A linguagem definida para o projeto é Python.

O subconjunto planejado para as próximas etapas inclui:

- Números inteiros.
- Identificadores.
- Operadores aritméticos: `+`, `-`, `*` e `/`.
- Parênteses.
- Atribuições simples.

A análise léxica, sintática e semântica ainda não está implementada nesta versão.

## 3. Tecnologias utilizadas

- **Frontend:** HTML, CSS e JavaScript.
- **Backend:** Python e FastAPI.
- **Servidor web:** Nginx.
- **Testes automatizados:** pytest.
- **Ambiente de execução:** Docker e Docker Compose.

## 4. Funcionalidades implementadas

- Interface web com identificação do CompilaLab.
- Editor de código-fonte com fonte monoespaçada.
- Seleção de exemplos de código.
- Botão para solicitar o processamento do código.
- Botão para limpar o editor.
- Comunicação HTTP entre frontend e backend.
- Envio do código em formato JSON.
- Validação de entrada vazia no backend.
- Apresentação do resultado retornado pela API.
- Mensagem de erro em caso de falha de comunicação.

## 5. Exemplos disponíveis

A interface disponibiliza os seguintes exemplos:

1. **Soma de números:** demonstra atribuição e operação aritmética.
2. **Variáveis:** demonstra atribuição de valores e utilização de identificadores.
3. **Expressão matemática:** demonstra operadores aritméticos e parênteses.
4. **Código vazio:** permite verificar o comportamento de validação da entrada.

Os exemplos são enviados como texto para o backend. A aplicação ainda não executa os programas nem realiza sua análise léxica ou sintática.

## 6. Comunicação entre frontend e backend

O frontend envia uma requisição HTTP `POST` para o endpoint `/api/analisar`.

O corpo da requisição utiliza JSON:

```json
{
  "codigo": "valor = 10 + 20\nprint(valor)"
}
```

Quando o código é recebido com sucesso, a API retorna informações sobre o recebimento e o tamanho do conteúdo. Entradas vazias são rejeitadas.

O endpoint `/api/health` permite verificar a saúde do backend, enquanto `/api/hello` fornece uma resposta simples de identificação da API.

## 7. Como executar

### Pré-requisitos

- Git.
- Docker Desktop com Docker Compose.
- Navegador web moderno.

### Iniciar a aplicação

Na pasta raiz do projeto, execute:

```bash
docker compose up --build -d
```

### Acessar a interface

Abra no navegador:

http://localhost:8080

A documentação interativa da API pode ser acessada em:

http://localhost:8000/docs

### Consultar os serviços

```bash
docker compose ps
```

### Encerrar a aplicação

```bash
docker compose down
```

## 8. Testes automatizados

Os testes do backend estão localizados em `backend/tests/test_main.py`.

Para executá-los no Windows PowerShell, entre na pasta `backend` e execute:

```powershell
.\.venv\Scripts\python.exe -m pytest -v
```

Os testes verificam o endpoint de saúde, a resposta de identificação da API, o recebimento de código válido, a rejeição de entradas vazias e outras situações de validação.

Os resultados devem ser registrados conforme as execuções efetivamente realizadas.

## 9. Estrutura do projeto

```text
compiladores/
├── backend/
│   ├── app/
│   │   └── main.py
│   ├── tests/
│   │   └── test_main.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── index.html
│   ├── nginx.conf
│   └── Dockerfile
├── docs/
├── docker-compose.yml
└── README.md
```

## 10. Limitações conhecidas

- O compilador ainda não está implementado.
- O backend recebe e valida o código, mas não executa o programa.
- A análise léxica, sintática e semântica será desenvolvida nas próximas etapas.
- A interface apresenta o resultado do recebimento do código, e não o resultado de uma compilação.

## 11. Próximas etapas

As próximas etapas do projeto deverão desenvolver progressivamente os analisadores léxico, sintático e semântico, além das demais fases previstas para o compilador didático.

O desenvolvimento será acompanhado por testes automatizados para verificar novas funcionalidades e prevenir regressões.
