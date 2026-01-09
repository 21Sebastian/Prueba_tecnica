from fastapi import HTTPException, status
from ORDS import cliente_ords
from models import ClienteBase

#Crear cliente 
async def registrar_cliente(cliente: ClienteBase):
    data = await cliente_ords.get_clients_all()
    items = data.get("items",[])

    for item in items:
        if item.get("documento_numero") == cliente.documento_numero:
            raise HTTPException(status_code=409, detail="Documento duplicado")
        if item.get("email") == cliente.email:
            raise HTTPException(status_code=409, detail="Email duplicado")
        
    nuevo_cliente = await cliente_ords.create_cliente(cliente.dict())
    return nuevo_cliente

#Listar cliente 
async def listar_clientes(email: str = None, documento: str = None, estado_lead: str = None):
    data = await cliente_ords.get_clients_all()
    items = data.get("items", [])

    if email:
        items = [i for i in items if i.get("email") == email]
    if documento:
        items = [i for i in items if i.get("documento_numero") == documento]
    if estado_lead:
        items = [c for c in items if c.get("estado_lead") == estado_lead]
    
    return {"items": items}

# Cliente por ID 
async def obtener_cliente(id_cliente: int):
    cliente = await cliente_ords.get_cliente_by_id(id_cliente)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente

#Actualizar cliente 
async def actualizar_cliente(id_cliente: int, cliente_update: ClienteBase):

    existe = await cliente_ords.get_cliente_by_id(id_cliente)
    if not existe:
        raise HTTPException(status_code=404, detail="Cliente no existe")

    data = await cliente_ords.get_clients_all()
    items = data.get("items", [])

    for item in items:
        item_id = item.get("id") 
        
        if item_id != id_cliente:
            if item.get("documento_numero") == cliente_update.documento_numero:
                raise HTTPException(status_code=409, detail="Documento ya existe en otro cliente")
            if item.get("email") == cliente_update.email:
                raise HTTPException(status_code=409, detail="Email ya existe en otro cliente")

    try:
        resultado = await cliente_ords.update_cliente(id_cliente, cliente_update.dict())
        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error actualizando en ORDS: {str(e)}")