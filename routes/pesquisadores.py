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


'''
ESCREVA AQUI A ROTA DE ATUALIZAÇÃO DE PESQUISADOR

Onde fica:
* Neste arquivo, logo abaixo da rota de busca por `lattes_id`.

O que essa rota precisa fazer:
* Usar `@router.put("/{lattes_id}")` para responder no endpoint
  `PUT /pesquisadores/{lattes_id}`.
* Receber o `lattes_id` pela URL.
* Receber no corpo da requisição um `Pesquisador_create_DTO` com os dados atualizados.
* Chamar o método `dao.atualizar(...)` passando os dados necessários.
* Se o DAO retornar erro, responder com HTTP 400.
* Depois da atualização, buscar novamente o pesquisador para devolver os dados atualizados.
* Em caso de sucesso, retornar um `Pesquisador`.

Importante:
* Esta rota depende do `Pesquisador_create_DTO` estar implementado e funcionando corretamente,
  pois ele valida os dados recebidos no corpo da requisição.
* Esta rota também depende do método `dao.atualizar(...)` estar implementado e funcionando.
'''


@router.delete("/{lattes_id}")
def deletar_pesquisador(lattes_id: str):
    resultado = dao.apagar(lattes_id)
    if resultado.get("error") == "inválido":
        raise HTTPException(status_code=400, detail=resultado["message"])
    return {"message": resultado["message"]}
