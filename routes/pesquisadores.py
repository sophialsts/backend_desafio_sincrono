from fastapi import APIRouter, HTTPException, status
from typing import List
from models.pesquisador import Pesquisador
from dto.pesquisador_create_dto import Pesquisador_create_DTO
from dao import PesquisadorDAO

router = APIRouter(prefix="/pesquisadores", tags=["Pesquisadores"])
dao = PesquisadorDAO()

'''
ESCREVA AQUI A ROTA DE ADIÇÃO DE PESQUISADOR

Onde fica:
* Neste arquivo, logo abaixo da criação do `router` e do `dao`.

O que essa rota precisa fazer:
* Usar `@router.post("")` para responder no endpoint `POST /pesquisadores`.
* Receber no corpo da requisição um `Pesquisador_create_DTO`.
* Chamar o método `dao.salvar(...)` passando os campos necessários do DTO.
* Tratar erro de duplicidade retornando HTTP 409.
* Tratar outros erros de criação retornando HTTP 400.
* Em caso de sucesso, devolver um `Pesquisador` com os dados recebidos e o `pesquisadores_id`
  retornado pelo banco.

Importante:
* Esta rota depende do `Pesquisador_create_DTO` estar implementado e funcionando corretamente,
  porque é ele quem valida a entrada recebida no POST.
'''


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
