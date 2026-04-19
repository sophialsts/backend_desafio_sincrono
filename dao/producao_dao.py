from database import Conexao
from dto.producao_create_dto import Producao_create_DTO
from typing import List, Optional, Dict, Any
from uuid import UUID

class ProducaoDAO:
    def __init__(self):
        self._conexao = Conexao()

    def _get_cursor(self):
        return self._conexao.get_conexao().cursor()

    def _normalizar_uuid(self, valor: str | UUID) -> str:
        return str(valor)

    def salvar(self, producao: Producao_create_DTO) -> Dict[str, Any]:
        sql = """
            INSERT INTO producoes (nomeartigo, anoartigo, pesquisadores_id, issn)
            VALUES (%s, %s, %s, %s)
            RETURNING producoes_id
        """
        try:
            with self._get_cursor() as cursor:
                cursor.execute(sql, (
                    producao.nomeartigo,
                    producao.anoartigo,
                    self._normalizar_uuid(producao.pesquisadores_id),
                    producao.issn
                ))
                result = cursor.fetchone()
                self._conexao.get_conexao().commit()
                return {"success": True, "producoes_id": str(result[0]) if result else None}
        except Exception as e:
            self._conexao.get_conexao().rollback()
            error_msg = str(e)
            if "foreign key" in error_msg.lower():
                return {"success": False, "error": "Erro", "message": "Pesquisador não encontrado"}
            if "duplicate key" in error_msg.lower() or "unique constraint" in error_msg.lower():
                return {"success": False, "error": "duplicate", "message": error_msg}
            return {"success": False, "error": "Erro", "message": error_msg}

    def listar_todos(self) -> List[Dict[str, Any]]:
        sql = """
            SELECT producoes_id, pesquisadores_id, issn, nomeartigo, anoartigo 
            FROM producoes 
            ORDER BY anoartigo DESC, nomeartigo
        """
        with self._get_cursor() as cursor:
            cursor.execute(sql)
            colunas = [desc[0] for desc in cursor.description]
            return [dict(zip(colunas, linha)) for linha in cursor.fetchall()]

    def buscar_por_id(self, producoes_id: str | UUID) -> Optional[Dict[str, Any]]:
        sql = """
            SELECT producoes_id, pesquisadores_id, issn, nomeartigo, anoartigo 
            FROM producoes 
            WHERE producoes_id = %s
        """
        with self._get_cursor() as cursor:
            cursor.execute(sql, (self._normalizar_uuid(producoes_id),))
            resultado = cursor.fetchone()
            if resultado:
                colunas = [desc[0] for desc in cursor.description]
                return dict(zip(colunas, resultado))
            return None

    def atualizar(self, producao: Producao_create_DTO, producoes_id: str | UUID) -> Dict[str, Any]:
        sql = """
            UPDATE producoes
            SET nomeartigo = %s, issn = %s, anoartigo = %s, pesquisadores_id = %s
            WHERE producoes_id = %s
            RETURNING producoes_id
        """
        try:
            with self._get_cursor() as cursor:
                cursor.execute(sql, (
                    producao.nomeartigo,
                    producao.issn,
                    producao.anoartigo,
                    self._normalizar_uuid(producao.pesquisadores_id),
                    self._normalizar_uuid(producoes_id)
                ))
                result = cursor.fetchone()
                self._conexao.get_conexao().commit()
                if result:
                    return {"success": True, "message": "Produção atualizada com sucesso!"}
                return {"success": False, "error": "Erro", "message": "Produção não encontrada"}
        except Exception as e:
            self._conexao.get_conexao().rollback()
            return {"success": False, "error": "Erro", "message": str(e)}

    def apagar(self, producoes_id: str | UUID) -> Dict[str, Any]:
        sql = "DELETE FROM producoes WHERE producoes_id = %s"
        try:
            with self._get_cursor() as cursor:
                cursor.execute(sql, (self._normalizar_uuid(producoes_id),))
                if cursor.rowcount > 0:
                    self._conexao.get_conexao().commit()
                    return {"success": True, "message": "Produção apagada com sucesso!"}
                return {"success": False, "error": "inválido", "message": "Produção não encontrada ou ID inválido"}
        except Exception as e:
            self._conexao.get_conexao().rollback()
            return {"success": False, "error": "inválido", "message": str(e)}
