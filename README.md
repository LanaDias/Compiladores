# CompilaLab — Ambiente Educacional de Compiladores

## 1. Objetivo

O CompilaLab é um projeto acadêmico que tem como objetivo apoiar o aprendizado dos conceitos de construção de compiladores por meio de uma aplicação web interativa.

Nesta terceira etapa, o foco é implementar a análise léxica (Scanner), responsável por percorrer o código-fonte e identificar os tokens que compõem a linguagem.

## 2. Linguagem e escopo

A linguagem definida como referência para o projeto é Python, considerando um subconjunto simplificado.

O scanner identifica as seguintes categorias:

- Palavras reservadas, como `if`, `else`, `while`, `return`, `int`, `float` e `print`.
- Identificadores, como `numero` e `valor`.
- Números inteiros, como `10` e `20`.
- Números reais, como `2.5` e `10.75`.
- Operadores aritméticos e relacionais, como `+`, `-`, `*`, `/`, `=`, `==`, `!=`, `<` e `>`.
- Delimitadores, como parênteses, chaves, colchetes, vírgulas e ponto e vírgula.
- Comentários iniciados pelo caractere `#`.

O scanner também identifica caracteres não reconhecidos e informa suas posições no código-fonte.

A análise sintática e semântica ainda não está implementada nesta versão.

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
- Botão para solicitar a análise do código.
- Botão para limpar o editor.
- Comunicação HTTP entre frontend e backend.
- Envio do código em formato JSON.
- Validação de entrada vazia no backend.
- Análise léxica do código-fonte.
- Identificação e classificação dos tokens.
- Registro do tipo, lexema, linha e coluna de cada token.
- Ignoração de espaços em branco e comentários.
- Identificação de caracteres inválidos com indicação de posição.
- Exibição dos tokens em uma tabela na interface.
- Exibição dos erros léxicos encontrados.
- Testes automatizados para o scanner e para a API.

## 5. Exemplos disponíveis

A interface disponibiliza exemplos para demonstrar o funcionamento da aplicação:

1. **Código básico:** demonstra atribuições e operações aritméticas.
2. **Variáveis:** demonstra a utilização de identificadores.
3. **Expressão matemática:** demonstra operadores e números.
4. **Condição:** demonstra palavras reservadas e operadores relacionais.
5. **Caractere inválido:** permite verificar a identificação de erros léxicos.
6. **Código vazio:** permite verificar a validação da entrada.

Os exemplos são enviados como texto para o backend. A aplicação realiza a análise léxica, mas ainda não executa os programas nem realiza a análise sintática ou semântica.

## 6. Comunicação entre frontend e backend

O frontend envia uma requisição HTTP `POST` para o endpoint `/api/analisar`.

O corpo da requisição utiliza JSON:

```
{
  "codigo": "valor = 10 + 20\nprint(valor)"
}
```

A API recebe o código-fonte e executa a análise léxica. A resposta contém informações sobre o recebimento do código, os tokens identificados e os erros encontrados.

Cada token apresenta os seguintes campos:

- `tipo`: categoria do token.
- `lexema`: trecho do código identificado.
- `linha`: linha em que o token aparece.
- `coluna`: coluna inicial do token.

Os erros léxicos apresentam o tipo do erro, o lexema, a linha, a coluna e uma mensagem explicativa.

O campo `sucesso` indica se a análise foi concluída sem erros léxicos. Entradas vazias são rejeitadas pela API.

O endpoint `/api/health` permite verificar a saúde do backend, enquanto `/api/hello` fornece uma resposta simples de identificação da API.

## 7. Como executar

### Pré-requisitos

- Git.
- Docker Desktop com Docker Compose.
- Navegador web moderno.

### Iniciar a aplicação

Na pasta raiz do projeto, execute:

```
docker compose up --build -d
```

### Acessar a interface

Abra no navegador:

[http://localhost:8080](http://localhost:8080)

A documentação interativa da API pode ser acessada em:

[http://localhost:8000/docs](http://localhost:8000/docs)

### Consultar os serviços

```
docker compose ps
```

### Encerrar a aplicação

```
docker compose down
```

## 8. Testes automatizados

Os testes do backend estão localizados em `backend/tests/`.

Para executá-los no Windows PowerShell, entre na pasta `backend` e execute:

```
.\.venv\Scripts\python.exe -m pytest -v
```

Os testes verificam funcionalidades da API e do scanner, incluindo:

- Identificação de identificadores e números.
- Classificação de palavras reservadas.
- Ignoração de espaços em branco e comentários.
- Registro de linhas e colunas.
- Identificação de caracteres inválidos.
- Identificação de delimitadores.
- Funcionamento dos endpoints da API.
- Validação de entradas vazias.

Na execução realizada durante o desenvolvimento, foram aprovados 12 testes (`12 passed`).

## 9. Estrutura do projeto

```
compiladores/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   └── scanner.py
│   ├── tests/
│   │   ├── test_main.py
│   │   └── test_scanner.py
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

- O scanner reconhece apenas um subconjunto simplificado de construções da linguagem Python.
- Nem todas as palavras reservadas e construções da linguagem Python são contempladas.
- A análise léxica identifica tokens, mas não garante que o código esteja sintaticamente correto.
- A análise sintática e semântica ainda não foi implementada.
- O backend não executa os programas recebidos.
- A validação léxica não cobre todas as situações possíveis da linguagem Python.

## 11. Próximas etapas

As próximas etapas do projeto deverão desenvolver progressivamente a análise sintática e a análise semântica, além das demais funcionalidades previstas para o compilador didático.

O desenvolvimento continuará acompanhado por testes automatizados para verificar as funcionalidades implementadas e prevenir regressões.
