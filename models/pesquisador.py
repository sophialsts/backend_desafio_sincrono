from dataclasses import dataclass
from typing import Optional
from uuid import UUID

@dataclass
class Pesquisador:
    lattes_id: str
    nome: str
    pesquisadores_id: Optional[UUID] = None
    articles: Optional[int] = 0