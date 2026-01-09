Proxy ORDS - Backend API

DESCRIPCIÓN DEL PROYECTO

Este proyecto es un servicio backend intermedio (Proxy) desarrollado en Python con FastAPI.
Su propósito es actuar como una capa de lógica de negocio entre los consumidores del API y una base de datos Oracle expuesta mediante ORDS (Oracle REST Data Services).

El sistema valida datos, previene duplicados y maneja errores antes de persistir la información en la base de datos, garantizando integridad y estabilidad del servicio.


TECNOLOGÍAS UTILIZADAS

- Lenguaje: Python 3.9+
- Framework Web: FastAPI
- Servidor ASGI: Uvicorn
- Cliente HTTP Asíncrono: HTTPX
- Validación de Datos: Pydantic, Email-Validator
- Variables de Entorno: Python-dotenv
- Base de Datos: Oracle (expuesta vía ORDS)


CARACTERÍSTICAS Y REGLAS DE NEGOCIO

Prevención de duplicados:
- No permite crear ni actualizar clientes con un documento o email que ya exista en otro registro.
- Retorna error 409 Conflict en caso de duplicidad.

Validación de datos:
- Normalización de correos electrónicos (no sensible a mayúsculas/minúsculas).
- Validación de formato de email.
- Validación de campos obligatorios mediante Pydantic.

Manejo de errores:
- 200 OK: Operación exitosa.
- 404 Not Found: Cliente no encontrado.
- 409 Conflict: Documento o email duplicado.
- 502 Bad Gateway: Error de comunicación con ORDS.
- 500 Internal Server Error: Error inesperado controlado.

Nota:
El servidor captura y gestiona internamente errores inesperados para evitar la caída del servicio.

Filtrado:
- Búsqueda por email.
- Búsqueda por documento.
- Búsqueda por estado del lead.


INSTALACIÓN Y CONFIGURACIÓN

1. Clonar el repositorio
Clona el proyecto en tu máquina local.

2. Crear un entorno virtual (recomendado)

python -m venv venv

Activación del entorno virtual:

Windows:
.\venv\Scripts\activate

Mac / Linux:
source venv/bin/activate

3. Instalar dependencias

pip install fastapi uvicorn httpx python-dotenv pydantic email-validator

4. Configurar variables de entorno

Crear un archivo .env en la raíz del proyecto con el siguiente contenido:

ORDS_URL=https://gabdddcba32cc06-agenteaidb.adb.us-ashburn-1.oraclecloudapps.com/ords/admin/clientes_seguros


EJECUCIÓN DEL PROYECTO

Para iniciar el servidor en modo desarrollo:

python -m uvicorn main:app --reload

El servicio quedará disponible en:
http://127.0.0.1:8000


DOCUMENTACIÓN Y PRUEBAS

FastAPI genera documentación automática mediante Swagger UI.

Accede desde tu navegador a:
http://127.0.0.1:8000

Desde allí podrás probar todos los endpoints disponibles.


ENDPOINTS DISPONIBLES

POST /api/clientes
- Crear un nuevo cliente.

GET /api/clientes
- Listar clientes con filtros opcionales por email, documento o estado_lead.

GET /api/clientes/{id}
- Obtener el detalle de un cliente por su ID.

PUT /api/clientes/{id}
- Actualizar un cliente existente validando duplicados.


EJEMPLOS DE USO CON CURL 

Crear un cliente:

curl -X POST ^
  http://127.0.0.1:8000/api/clientes ^
  -H "Content-Type: application/json" ^
  -d "{
    \"nombre\": \"Juan\",
    \"apellido\": \"Perez\",
    \"email\": \"juan.perez@example.com\",
    \"documento_numero\": \"100200300\",
    \"telefono\": \"555-0199\",
    \"estado_lead\": \"Nuevo\"
  }"

Listar clientes por estado:

curl -X GET ^
  http://127.0.0.1:8000/api/clientes?estado_lead=Nuevo ^
  -H "accept: application/json"

Obtener cliente por ID:

curl -X GET ^
  http://127.0.0.1:8000/api/clientes/21 ^
  -H "accept: application/json"

Actualizar cliente:

curl -X PUT ^
  http://127.0.0.1:8000/api/clientes/21 ^
  -H "Content-Type: application/json" ^
  -d "{
    \"nombre\": \"Juan\",
    \"apellido\": \"Perez\",
    \"email\": \"juan.perez@example.com\",
    \"documento_numero\": \"100200300\",
    \"telefono\": \"555-9999\",
    \"estado_lead\": \"Contactado\"
  }"

PRUEBAS CON POSTMAN

Para facilitar la validación de los endpoints, se incluye en el repositorio el archivo postman_ejemplos.json. Este archivo contiene una colección preconfigurada con todas las peticiones listas para usar.

¿Cómo importar la colección?
1. Abre Postman.
2. Haz clic en el botón "Import" (ubicado en la esquina superior izquierda).
3. Arrastra el archivo postman_ejemplos.json o selecciónalo desde tu carpeta del proyecto.
4. Una vez importado, verás una carpeta llamada "Proxy ORDS Seguros" en tu panel de colecciones.
5. Asegúrate de que tu servidor esté corriendo (python -m uvicorn main:app --reload) y ejecuta las peticiones.


ESTRUCTURA DEL PROYECTO

/
├── Controllers/
│   └── clientes.py        Definición de endpoints
├── ORDS/
│   └── cliente_ords.py    Cliente HTTP para ORDS
├── Services/
│   └── cliente_service.py Lógica de negocio
├── models.py              Modelos Pydantic
├── main.py                Punto de entrada
├── .env                   Variables de entorno
└── README.txt             Documentación del proyecto


NOTAS FINALES

Este proyecto está diseñado como una capa intermedia segura y robusta entre los consumidores del API y una base de datos Oracle, asegurando validaciones, control de errores y estabilidad del servicio.
