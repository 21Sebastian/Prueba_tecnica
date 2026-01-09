from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from Controllers import clientes

app = FastAPI(title="Proxy_Prueba_Tecnica")

app.include_router(clientes.router)

@app.get("/")
def root():
    return RedirectResponse(url="/docs")


