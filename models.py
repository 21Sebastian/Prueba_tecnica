from pydantic import BaseModel, EmailStr, Field
from typing import Optional

#Esquema de la base
class ClienteBase(BaseModel):
    nombre: str
    apellido: str
    email: EmailStr
    documento_numero: str = Field(...,min_length=1)
    telefono: Optional[str] = None

#ID del cliente
class ClienteResponse(ClienteBase):
    id:int