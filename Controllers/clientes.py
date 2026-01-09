from fastapi import APIRouter, Query
from typing import Optional
from Services import cliente_service
from models import ClienteBase

router = APIRouter()

# Crear cliente 
@router.post("/api/clientes/")
async def crear_cliente(cliente: ClienteBase):
    return await cliente_service.registrar_cliente(cliente)

#Listar clientes 
@router.get("/api/clientes/")
async def listar_clientes(email: Optional[str] = Query(None, description="Filtrar por correo electrónico"),
    documento: Optional[str] = Query(None, description="Filtrar por número de documento"),
    estado_lead: Optional[str] = Query(None, description="Filtrar por estado")):

    return await cliente_service.listar_clientes(email, documento, estado_lead)

# Cliente ID 
@router.get("/api/clientes/{id_cliente}")
async def obtener_cliente(id_cliente: int):
    return await cliente_service.obtener_cliente(id_cliente)

# Actualizar 
@router.put("/api/clientes/{id_cliente}")
async def actualizar_cliente(id_cliente: int, cliente: ClienteBase):
    return await cliente_service.actualizar_cliente(id_cliente, cliente)