from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field

class Producao_response_DTO(BaseModel):
    producoes_id: Optional[UUID] = None
    issn: str = Field(..., min_length=8, max_length=8, pattern=r"^\d{8}$")
    nomeartigo: str = Field(..., min_length=2, max_length=200)
    anoartigo: int = Field(..., ge=1900, le=2100)
    pesquisadores_id: UUID

    class Config:
        from_attributes = True