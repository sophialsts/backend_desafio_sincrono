from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field

class Pesquisador_response_DTO(BaseModel):
    pesquisadores_id: Optional[UUID] = None
    lattes_id: str = Field(..., min_length=16, max_length=16)
    nome: str = Field(..., min_length=2, max_length=200)
    articles: Optional[int] = Field(0, ge=0)

    class Config:
        from_attributes = True