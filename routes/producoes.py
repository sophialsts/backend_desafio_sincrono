from fastapi import APIRouter, HTTPException, status
from typing import List
from uuid import UUID
from models.producao import Producao
from dto.producao_create_dto import Producao_create_DTO
from dao import ProducaoDAO

router = APIRouter(prefix="/producoes", tags=["Produções"])
dao = ProducaoDAO()


@router.post("", response_model=Producao, status_code=status.HTTP_201_CREATED)
def criar_producao(producao: Producao_create_DTO):
    resultado = dao.salvar(producao)
    if resultado.get("error") == "duplicate":
        raise HTTPException(status_code=409, detail=resultado["message"])
    if not resultado.get("success"):
        raise HTTPException(status_code=400, detail=resultado["message"])
    return Producao(
        issn=producao.issn,
        nomeartigo=producao.nomeartigo,
        anoartigo=producao.anoartigo,
        pesquisadores_id=producao.pesquisadores_id,
        producoes_id=resultado.get("producoes_id")
    )


@router.get("", response_model=List[Producao])
def listar_producoes():
    return dao.listar_todas()


@router.get("/{producoes_id}", response_model=Producao)
def buscar_producao(producoes_id: UUID):
    resultado = dao.buscar_por_id(producoes_id)
    if not resultado:
        raise HTTPException(status_code=404, detail="Produção não encontrada")
    return resultado


'''
ESCREVA AQUI A ROTA DE ATUALIZAÇÃO DE PRODUÇÃO

Onde fica:
* Neste arquivo, logo abaixo da rota de busca por `producoes_id`.

O que essa rota precisa fazer:
* Usar `@router.put("/{producoes_id}")` para responder no endpoint
  `PUT /producoes/{producoes_id}`.
* Receber o `producoes_id` pela URL.
* Receber no corpo da requisição um `Producao_create_DTO` com os dados atualizados.
* Chamar o método `dao.atualizar(...)` passando os dados necessários.
* Se o DAO retornar erro, responder com HTTP 400.
* Depois da atualização, buscar novamente a produção para devolver os dados atualizados.
* Em caso de sucesso, retornar uma `Producao`.

Importante:
* Esta rota depende do `Producao_create_DTO` estar implementado e funcionando corretamente,
  pois ele valida os dados recebidos no corpo da requisição.
* Esta rota também depende do método `dao.atualizar(...)` estar implementado e funcionando.
'''


@router.delete("/{producoes_id}")
def deletar_producao(producoes_id: UUID):
    resultado = dao.apagar(producoes_id)
    if resultado.get("error") == "inválido":
        raise HTTPException(status_code=400, detail=resultado["message"])
    return {"message": resultado["message"]}
