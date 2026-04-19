import os

import psycopg2
from dotenv import load_dotenv
from psycopg2 import OperationalError


class Conexao:
    _instancia_bd = None
    _dotenv_carregado = False

    def __new__(cls, *args, **kwargs):
        if cls._instancia_bd is None:
            cls._instancia_bd = super(Conexao, cls).__new__(cls)
        return cls._instancia_bd

    @classmethod
    def _carregar_variaveis_ambiente(cls):
        if not cls._dotenv_carregado:
            load_dotenv()
            cls._dotenv_carregado = True

    def __init__(
        self,
        host: str = None,
        database: str = None,
        user: str = None,
        password: str = None,
        port: int = None,
    ):
        if not hasattr(self, "_inicializado"):
            self._carregar_variaveis_ambiente()
            self._host = host or os.getenv("DB_HOST", "localhost")
            self._database = database or os.getenv("DB_NAME", "postgres")
            self._user = user or os.getenv("DB_USER", "postgres")
            self._password = password or os.getenv("DB_PASSWORD", "root")
            self._port = port or int(os.getenv("DB_PORT", "5432"))
            self._conexao = None
            self._inicializado = True

    def conectar_ao_banco(self):
        if self._conexao is None or self._conexao.closed:
            try:
                self._conexao = psycopg2.connect(
                    host=self._host,
                    database=self._database,
                    user=self._user,
                    password=self._password,
                    port=self._port,
                )
            except OperationalError as erro:
                raise Exception(f"Erro ao conectar ao banco: {erro}")

    def get_conexao(self):
        if self._conexao is None or self._conexao.closed:
            self.conectar_ao_banco()
        return self._conexao

    def fechar_conexao(self):
        if self._conexao and not self._conexao.closed:
            self._conexao.close()
            self._conexao = None
