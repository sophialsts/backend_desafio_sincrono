from database import Conexao
from typing import List, Optional, Dict, Any


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

    def atualizar(self, nome: str, pesquisadores_id: str, lattes_id: str) -> Dict[str, Any]:
        sql = """
            UPDATE pesquisadores
            SET nome = %s
            WHERE lattes_id = %s
            RETURNING pesquisadores_id
        """
        try:
            with self._get_cursor() as cursor:
                cursor.execute(sql, (nome, lattes_id))
                result = cursor.fetchone()
                self._conexao.get_conexao().commit()
                if result:
                    return {"success": True, "message": "Pesquisador atualizado com sucesso!"}
                return {"success": False, "error": "Erro", "message": "Pesquisador não encontrado"}
        except Exception as e:
            self._conexao.get_conexao().rollback()
            return {"success": False, "error": "Erro", "message": str(e)}

    def apagar(self, lattes_id: str) -> Dict[str, Any]:
        sql = "DELETE FROM pesquisadores WHERE lattes_id = %s"
        try:
            with self._get_cursor() as cursor:
                cursor.execute(sql, (lattes_id,))
                if cursor.rowcount > 0:
                    self._conexao.get_conexao().commit()
                    return {"success": True, "message": "Pesquisador apagado com sucesso!"}
                return {"success": False, "error": "inválido", "message": "Pesquisador não encontrado ou ID inválido"}
        except Exception as e:
            self._conexao.get_conexao().rollback()
            return {"success": False, "error": "inválido", "message": str(e)}
