
# Testes da Etapa 4

## Objetivo

Validar a análise sintática, a construção da AST e a integração com a API.

## Execução

Na pasta do backend:

```powershell
python -m pytest -v
```

Ou, usando Docker:

```powershell
docker compose exec backend python -m pytest -v
```

## Cenários de validação

- Declaração de variáveis.
- Atribuição de valores.
- Operações aritméticas.
- Precedência de operadores.
- Comandos de impressão.
- Estruturas condicionais.
- Estruturas de repetição.
- Blocos de instruções.
- Erros sintáticos.
- Posições dos nós da AST.
- Retorno da API.

## Validação manual

1. Abrir a interface do CompilaLab.
2. Inserir um programa válido.
3. Executar a análise.
4. Verificar os tokens.
5. Verificar o resultado sintático.
6. Verificar a árvore sintática abstrata.
7. Inserir um programa inválido.
8. Verificar a apresentação dos erros.
