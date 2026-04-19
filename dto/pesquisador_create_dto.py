from pydantic import BaseModel, Field

class Pesquisador_create_DTO(BaseModel):
    lattes_id: str = Field(..., min_length=16, max_length=16)
    nome: str = Field(..., min_length=2, max_length=200)