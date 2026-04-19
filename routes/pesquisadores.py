from fastapi import APIRouter, HTTPException, status
from typing import List
from models.pesquisador import Pesquisador
from dto.pesquisador_create_dto import Pesquisador_create_DTO
from dao import PesquisadorDAO

router = APIRouter(prefix="/pesquisadores", tags=["Pesquisadores"])
dao = PesquisadorDAO()

@router.post("", response_model=Pesquisador, status_code=status.HTTP_201_CREATED)
def criar_pesquisador(pesquisador: Pesquisador_create_DTO):
    resultado = dao.salvar(nome=pesquisador.nome, lattes_id=pesquisador.lattes_id)
    if resultado.get("error") == "duplicate":
        raise HTTPException(status_code=409, detail=resultado["message"])
    if not resultado.get("success"):
        raise HTTPException(status_code=400, detail=resultado["message"])
    return Pesquisador(
        lattes_id=pesquisador.lattes_id,
        nome=pesquisador.nome,
        pesquisadores_id=resultado.get("pesquisadores_id"),
        articles=0
    )


@router.get("", response_model=List[Pesquisador])
def listar_pesquisadores():
    return dao.listar_todos()


@router.get("/{lattes_id}", response_model=Pesquisador)
def buscar_pesquisador(lattes_id: str):
    resultado = dao.buscar_por_lattes_id(lattes_id)
    if not resultado:
        raise HTTPException(status_code=404, detail="Pesquisador não encontrado")
    return resultado


@router.put("/{lattes_id}", response_model=Pesquisador)
def atualizar_pesquisador(lattes_id: str, pesquisador: Pesquisador_create_DTO):
    resultado = dao.atualizar(
        nome=pesquisador.nome,
        pesquisadores_id=pesquisador.lattes_id,
        lattes_id=lattes_id
    )
    if resultado.get("error"):
        raise HTTPException(status_code=400, detail=resultado["message"])
    pesquisador_atualizado = dao.buscar_por_lattes_id(lattes_id)
    if pesquisador_atualizado:
        return Pesquisador(**pesquisador_atualizado)
    return Pesquisador(
        lattes_id=lattes_id,
        nome=pesquisador.nome,
        pesquisadores_id=pesquisador.lattes_id,
        articles=0
    )


@router.delete("/{lattes_id}")
def deletar_pesquisador(lattes_id: str):
    resultado = dao.apagar(lattes_id)
    if resultado.get("error") == "inválido":
        raise HTTPException(status_code=400, detail=resultado["message"])
    return {"message": resultado["message"]}
