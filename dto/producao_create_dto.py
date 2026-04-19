from pydantic import BaseModel, Field
from uuid import UUID

class Producao_create_DTO(BaseModel):
    issn: str = Field(..., min_length=8, max_length=8, pattern=r"^\d{8}$")
    nomeartigo: str = Field(..., min_length=2, max_length=200)
    anoartigo: int = Field(..., ge=1900, le=2100)
    pesquisadores_id: UUID