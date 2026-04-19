from dataclasses import dataclass
from typing import Optional
from uuid import UUID

@dataclass
class Producao:
    issn: str
    nomeartigo: str
    anoartigo: int
    pesquisadores_id: UUID
    producoes_id: Optional[UUID] = None