import httpx
import os
from dotenv import load_dotenv

load_dotenv()
ORDS_BASE_URL = os.getenv("ORDS_URL")

#lista de clientes
async def get_clients_all():

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{ORDS_BASE_URL}/")
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            print("Error 502: No se pudo conectar con ORDS")
            return {"items": []} 
        except httpx.HTTPStatusError as e:
            print(f"Error 500 interno de ORDS: {e}")
            return {"items": []}
        
#Cliente por ID
async def get_cliente_by_id(id_cliente: int):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{ORDS_BASE_URL}/{id_cliente}")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return None
            print(f"Error ORDS GET ID: {e}")
            return None

#Actualizar cliente
async def update_cliente(id_cliente: int, data: dict):
    async with httpx.AsyncClient() as client:
        response = await client.put(f"{ORDS_BASE_URL}/{id_cliente}", json=data)
        response.raise_for_status()
        return response.json()
    
#Crear cliente
async def create_cliente(data:dict):

    async with httpx.AsyncClient() as client:
        response = await client.post(f"{ORDS_BASE_URL}/", json=data)
        response.raise_for_status()
        return response.json