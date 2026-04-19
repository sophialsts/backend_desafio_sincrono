try:
    from database import Conexao
except ModuleNotFoundError:
    from conexao import Conexao

banco = Conexao().get_conexao()

script_sql = """
    DROP TABLE IF EXISTS producoes;
    DROP TABLE IF EXISTS pesquisadores;
    DROP EXTENSION IF EXISTS "uuid-ossp";
"""

try:
    with banco.cursor() as cursor:
        print("Removendo tabelas...")
        cursor.execute(script_sql)
        banco.commit()
        print("Tabelas e extensões removidas com sucesso!")
except Exception as e:
    banco.rollback()
    print(f"Erro: {e}")
finally:
    Conexao().fechar_conexao()
    print("Conexão encerrada.")
