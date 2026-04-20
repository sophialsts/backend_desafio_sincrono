from pydantic import BaseModel

class Pesquisador_create_DTO(BaseModel):
    '''
    IMPLEMENTE AQUI O DTO DE CRIAÇÃO DE PESQUISADOR

    Onde este DTO é usado:
    * Na rota de `POST /pesquisadores`.
    * Atualmente ele também é reutilizado na rota de atualização de pesquisador.

    O que precisa existir aqui:
    * Os campos necessários para receber os dados de criação do pesquisador.
    * As validações desses campos com Pydantic.

    Importante:
    * Este DTO precisa estar funcionando corretamente para que a rota de adição de pesquisador
      consiga validar o corpo da requisição antes de chamar o DAO.
    * Este DTO também é dependência da rota de atualização de pesquisador caso ele seja
      reutilizado no `PUT /pesquisadores/{lattes_id}`.
    '''
    pass
