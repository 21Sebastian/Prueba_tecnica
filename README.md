Proxy ORDS - Backend API 

Descripción del Proyecto 

Este proyecto es un servicio backend intermedio (Proxy) desarrollado en Python con FastAPI. Su objetivo es interactuar con una base de datos Oracle, expuesta vía ORDS (Oracle REST Data Services). 

El sistema actúa como una capa de lógica de negocio que valida datos, previene duplicados y gestiona errores antes de persistir la información en la base de datos. 

 

Tecnologías Utilizadas 

Lenguaje: Python 3.9+ 

Framework Web: FastAPI 

Servidor: Uvicorn 

Cliente HTTP Asíncrono: HTTPX 

Validación de Datos: Pydantic & Email-Validator 

Variables de Entorno: Python-dotenv 

 

Características y Reglas de Negocio 

El API implementa las siguientes validaciones: 

Prevención de Duplicados: 

No permite crear ni actualizar clientes con un Documento o Email que ya exista en otro registro. 

Devuelve error 409 Conflict en caso de duplicidad. 

Validación de Datos: 

Normalización de emails (insensible a mayúsculas/minúsculas). 

Validación de formato de correo electrónico. 

Validación de campos obligatorios. 

Manejo de Errores: 

404 Not Found: Si el cliente a consultar o actualizar no existe. 

502 Bad Gateway: Si falla la conexión con ORDS. 

500 Internal Server Error: Errores inesperados controlados. 
Nota:(El servidor captura, arregla y gestiona internamente cualquier fallo inesperado para evitar la caída del servicio.)

200 OK: Proceso existoso. 

Filtrado: 

Búsqueda por email, documento y estado. 



Instalación y Configuración 

1. Clonar el repositorio 

Descarga el código fuente en tu máquina local. 

2. Crear un entorno virtual (Recomendado) 

En tu terminal (PowerShell o Bash): 

python -m venv venv 
# Activar en Windows: 
.\venv\Scripts\activate 
# Activar en Mac/Linux: 
source venv/bin/activate 

3. Instalar dependencias 

Ejecuta el siguiente comando para instalar todas las librerías necesarias: 

pip install fastapi uvicorn httpx python-dotenv pydantic email-validator 

4. Configurar Variables de Entorno 

Crea un archivo llamado .env en la raíz del proyecto y agrega la URL base de ORDS: 

ORDS_URL=https://gabdddcba32cc06-agenteaidb.adb.us-ashburn-1.oraclecloudapps.com/ords/admin/clientes_seguros 



Ejecución del Proyecto 

Para iniciar el servidor de desarrollo, ejecuta el siguiente comando en la terminal: 

python -m uvicorn main:app --reload 

Si todo es correcto, verás un mensaje indicando que el servidor corre en: http://127.0.0.1:8000 



Documentación y Pruebas (Swagger UI) 

El proyecto incluye documentación interactiva automática. 

Abre tu navegador web. 

Ingresa a: http://127.0.0.1:8000 

Serás redirigido automáticamente a la interfaz de Swagger UI. 

Desde allí podrás probar todos los endpoints directamente: 

Endpoints Disponibles 

POST /api/clientes: Crear un nuevo cliente. 

GET /api/clientes: Listar clientes (permite filtros por email, documento, estado_lead). 

GET /api/clientes/{id}: Obtener el detalle de un cliente específico. 

PUT /api/clientes/{id}: Actualizar un cliente existente (valida duplicados excluyendo al propio usuario). 

Ejemplos de Uso de Endpoints

A continuación se detallan ejemplos prácticos de cómo consumir los servicios del API utilizando curl. También puedes probarlos directamente desde la interfaz de Swagger (/docs). 

1. Crear un Cliente (POST) 

Crea un nuevo registro validando que el email y el documento no existan previamente. 

URL: /api/clientes 

curl -X 'POST' \ 
 'http://127.0.0.1:8000/api/clientes' \ 
 -H 'Content-Type: application/json' \ 
 -d '{ 
 "nombre": "Juan", 
 "apellido": "Perez", 
 "email": "juan.perez@example.com", 
 "documento_numero": "100200300", 
 "telefono": "555-0199", 
 "estado_lead": "Nuevo" 
}' 

2. Listar Clientes con Filtros (GET) 

Obtiene la lista de clientes. Puedes filtrar por email, documento o estado_lead. 

URL: /api/clientes 
Ejemplo: Filtrar por estado "Nuevo" 

curl -X 'GET' \ 
 'http://127.0.0.1:8000/api/clientes?estado_lead=Nuevo' \ 
 -H 'accept: application/json' 

3. Obtener Cliente por ID (GET) 

Busca un cliente específico por su identificador único. 

URL: /api/clientes/{id} 
Ejemplo: Buscar el ID 21 

curl -X 'GET' \ 
 'http://127.0.0.1:8000/api/clientes/21' \ 
 -H 'accept: application/json' 

4. Actualizar Cliente (PUT) 

Actualiza los datos de un cliente existente. El sistema validará que, si cambias el email o documento, estos no pertenezcan a otro usuario diferente. 

URL: /api/clientes/{id} 
Ejemplo: Actualizar el teléfono y estado del ID 21 

curl -X 'PUT' \ 
 'http://127.0.0.1:8000/api/clientes/21' \ 
 -H 'Content-Type: application/json' \ 
 -d '{ 
 "nombre": "Juan", 
 "apellido": "Perez", 
 "email": "juan.perez@example.com", 
 "documento_numero": "100200300", 
 "telefono": "555-9999", 
 "estado_lead": "Contactado" 
}' 



Estructura del Proyecto 
/ 
├── Controllers/ 
│   └── clientes.py       # Definición de rutas (endpoints) y documentación 
├── ORDS/ 
│   └── cliente_ords.py   # Cliente HTTP para comunicarse con Oracle 
├── Services/ 
│   └── cliente_service.py # Lógica de negocio y validaciones 
├── models.py             # Esquemas Pydantic (Validación de datos) 
├── main.py               # Punto de entrada de la aplicación 
├── .env                  # Variables de entorno (No incluido en repo) 
└── README.md             # Este archivo 