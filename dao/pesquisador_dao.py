from database import Conexao
from typing import List, Optional, Dict, Any
from dto.pesquisador_create_dto import Pesquisador_create_DTO


class PesquisadorDAO:
    def __init__(self):
        self._conexao = Conexao()

    def _get_cursor(self):
        return self._conexao.get_conexao().cursor()

    '''
    ESCREVA AQUI A FUNÇÃO DAO PARA ADICIONAR UM PESQUISADOR

    Onde fica:
    * Neste arquivo, logo abaixo de `_get_cursor`.

    O que essa função precisa fazer:
    * Receber os dados necessários para criar um pesquisador, como `nome` e `lattes_id`.
    * Executar um `INSERT INTO pesquisadores (...) VALUES (...)`.
    * Usar `RETURNING pesquisadores_id` para devolver o identificador gerado.
    * Fazer `commit()` em caso de sucesso.
    * Fazer `rollback()` em caso de erro.
    * Retornar um dicionário com `success`, e quando existir, `pesquisadores_id`.
    * Tratar duplicidade para a rota conseguir responder com erro apropriado.

    Importante:
    * Essa função será chamada pela rota de `POST /pesquisadores`.
    * O DTO de criação do pesquisador precisa estar implementado e funcionando, pois a rota
      depende dele para validar os dados antes de chamar este DAO.
    '''

    def listar_todos(self) -> List[Dict[str, Any]]:
        sql = """
            SELECT p.pesquisadores_id, p.lattes_id, p.nome, COUNT(prod.producoes_id) as articles
            FROM pesquisadores p
            LEFT JOIN producoes prod ON p.pesquisadores_id = prod.pesquisadores_id
            GROUP BY p.pesquisadores_id, p.lattes_id, p.nome
            ORDER BY p.nome
        """
        with self._get_cursor() as cursor:
            cursor.execute(sql)
            colunas = [desc[0] for desc in cursor.description]
            return [dict(zip(colunas, linha)) for linha in cursor.fetchall()]

    def buscar_por_lattes_id(self, lattes_id: str) -> Optional[Dict[str, Any]]:
        sql = """
            SELECT p.pesquisadores_id, p.lattes_id, p.nome, COUNT(prod.producoes_id) as articles
            FROM pesquisadores p
            LEFT JOIN producoes prod ON p.pesquisadores_id = prod.pesquisadores_id
            WHERE p.lattes_id = %s
            GROUP BY p.pesquisadores_id, p.lattes_id, p.nome
        """
        with self._get_cursor() as cursor:
            cursor.execute(sql, (lattes_id,))
            resultado = cursor.fetchone()
            if resultado:
                colunas = [desc[0] for desc in cursor.description]
                return dict(zip(colunas, resultado))
            return None

    '''
    ESCREVA AQUI A FUNÇÃO DAO PARA ATUALIZAR UM PESQUISADOR

    Onde fica:
    * Neste arquivo, logo abaixo de `buscar_por_lattes_id`.

    O que essa função precisa fazer:
    * Receber os dados necessários para atualizar o pesquisador.
    * Executar um `UPDATE pesquisadores SET ... WHERE lattes_id = %s`.
    * Usar `RETURNING pesquisadores_id` para confirmar que o registro foi atualizado.
    * Fazer `commit()` em caso de sucesso.
    * Fazer `rollback()` em caso de erro.
    * Retornar um dicionário com `success` e uma `message`.
    * Se nenhum registro for encontrado, retornar erro informando que o pesquisador não existe.

    Importante:
    * Essa função será chamada pela rota de `PUT /pesquisadores/{lattes_id}`.
    * A rota de atualização também depende do DTO de criação/edição do pesquisador estar
      funcionando para validar os dados antes de chamar este DAO.
    '''

    def atualizar(self, lattes_id: str, pesquisador: Pesquisador_create_DTO) -> Dict[str, Any]:
        sql = """
            UPDATE pesquisadores
            SET lattes_id = %s, nome = %s
            WHERE lattes_id = %s
            RETURNING pesquisadores_id
        """
        try:
            with self._get_cursor() as cursor:
                cursor.execute(sql, (
                    pesquisador.lattes_id,
                    pesquisador.nome,
                    lattes_id
                ))
                resultado = cursor.fetchone()
                if resultado:
                    self._conexao.get_conexao().commit()
                    return {"success": True, "message": "Pesquisador atualizado com sucesso!"}

                self._conexao.get_conexao().rollback()
                return {"success": False, "error": "Erro", "message": "Pesquisador não encontrado"}
        except Exception as e:
            self._conexao.get_conexao().rollback()
            error_msg = str(e)
            if "duplicate key" in error_msg.lower() or "unique constraint" in error_msg.lower():
                return {"success": False, "error": "duplicate", "message": error_msg}
            return {"success": False, "error": "Erro", "message": error_msg}

    '''
    ESCREVA AQUI A FUNÇÃO DAO PARA APAGAR UM PESQUISADOR

    Onde fica:
    * Neste arquivo, logo abaixo da função de atualização do pesquisador.

    O que essa função precisa fazer:
    * Receber o `lattes_id` do pesquisador que será apagado.
    * Executar um `DELETE FROM pesquisadores WHERE lattes_id = %s`.
    * Fazer `commit()` em caso de sucesso.
    * Fazer `rollback()` em caso de erro.
    * Retornar um dicionário com `success` e uma `message`.
    * Se nenhum registro for apagado, retornar erro informando que o pesquisador não existe
      ou que o identificador é inválido.

    Importante:
    * Essa função será chamada pela rota de `DELETE /pesquisadores/{lattes_id}`.
    * A rota depende desse retorno para decidir se responde sucesso ou HTTP 400.
    '''
