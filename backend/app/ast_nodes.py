
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ASTNode:
    tipo: str
    atributos: dict[str, Any] = field(default_factory=dict)
    filhos: list["ASTNode"] = field(default_factory=list)
    linha: int = 1
    coluna: int = 1
    linha_fim: int = 1
    coluna_fim: int = 1

    def to_dict(self) -> dict[str, Any]:
        return {
            "tipo": self.tipo,
            "linha": self.linha,
            "coluna": self.coluna,
            "linhaFim": self.linha_fim,
            "colunaFim": self.coluna_fim,
            "atributos": self.atributos,
            "filhos": [filho.to_dict() for filho in self.filhos],
        }


def valor_token(token, chave, padrao=None):
    if token is None:
        return padrao
    if isinstance(token, dict):
        return token.get(chave, padrao)
    return getattr(token, chave, padrao)


def criar_no(
    tipo,
    atributos=None,
    filhos=None,
    token_inicio=None,
    token_fim=None,
):
    atributos = atributos or {}
    filhos = filhos or []

    linha = valor_token(token_inicio, "linha", 1)
    coluna = valor_token(token_inicio, "coluna", 1)

    linha_fim = valor_token(token_fim, "linha", linha)
    coluna_fim = (
        valor_token(token_fim, "coluna", coluna)
        + len(valor_token(token_fim, "lexema", ""))
    )

    return ASTNode(
        tipo=tipo,
        atributos=atributos,
        filhos=filhos,
        linha=linha,
        coluna=coluna,
        linha_fim=linha_fim,
        coluna_fim=coluna_fim,
    )
