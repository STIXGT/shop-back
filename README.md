# Tienda API (Backend)

Una API REST construida con FastAPI para gestionar productos y órdenes de compra. Incluye persistencia en PostgreSQL, validación con Pydantic y documentación automática con Swagger.

## Arquitectura

- FastAPI para el servidor HTTP ([app/main.py](app/main.py)).
- SQLAlchemy ORM con modelos `Product` y `Order` ([app/models](app/models)).
- Esquemas Pydantic para entradas/salidas ([app/schemas](app/schemas)).
- Rutas separadas por dominio: productos y órdenes ([app/routes](app/routes)).
- Base de datos PostgreSQL con conexión gestionada en [app/database.py](app/database.py).
- Contenedores Docker orquestados con Compose ([docker-compose.yml](docker-compose.yml)).

## Requisitos

- Docker y Docker Compose (recomendado)
- Opcional: Python 3.11 si deseas correr local sin Docker

## Variables de entorno

Crea un archivo `.env` en la raíz del backend. Ejemplo:

```env
# Variables usadas por el contenedor de Postgres
POSTGRES_DB=tienda
POSTGRES_USER=tienda_user
POSTGRES_PASSWORD=supersecret

# Variables usadas por la API (SQLAlchemy)
DB_NAME=${POSTGRES_DB}
DB_USER=${POSTGRES_USER}
DB_PASSWORD=${POSTGRES_PASSWORD}
DB_HOST=db
DB_PORT=5432
```

- La API construye `DATABASE_URL` como `postgresql://DB_USER:DB_PASSWORD@DB_HOST:DB_PORT/DB_NAME`.
- En Docker, `DB_HOST` debe ser `db` (nombre del servicio en Compose).

## Ejecutar con Docker

```bash
# Construir y levantar servicios (API + DB)
docker compose up --build

# Detener y remover contenedores
docker compose down
```

- API expone `http://localhost:8000`.
- Postgres expone `localhost:5432`.
- Swagger UI: `http://localhost:8000/docs`

Las tablas se crean automáticamente al iniciar la API gracias a `Base.metadata.create_all(bind=engine)` en [app/main.py](app/main.py).

## Ejecutar local (sin Docker)

1. Crea y activa un entorno virtual, instala dependencias:

```bash
python -m venv .venv
. .venv/Scripts/activate  # Windows PowerShell
pip install -r requirements.txt
```

2. Asegura que tu Postgres local está corriendo y que `.env` tiene las credenciales correctas.

3. Ejecuta la API:

```bash
uvicorn app.main:app --reload --port 8000
```

## Endpoints principales

### Productos (`/products`)

- POST `/products/` — Crear producto

  - Body (JSON):
    ```json
    {
      "name": "Laptop",
      "description": "14 pulgadas",
      "price": 999.99,
      "stock": 10
    }
    ```
  - Respuesta: objeto `ProductResponse` con `id`.

- GET `/products/` — Listar productos
  - Respuesta: lista de `ProductResponse`.

### Órdenes (`/orders`)

- POST `/orders/` — Crear orden

  - Reglas:
    - 404 si `product_id` no existe.
    - 400 si `quantity` > `product.stock`.
    - Reduce el `stock` del producto en la cantidad ordenada.
  - Body (JSON):
    ```json
    {
      "product_id": 1,
      "customer_name": "Juan Pérez",
      "customer_address": "Calle 123",
      "customer_phone": "+51 999 999 999",
      "quantity": 2
    }
    ```
  - Respuesta: objeto `OrderResponse` con `id` y `created_at` (campo gestionado en modelo).

- GET `/orders/` — Listar órdenes
  - Respuesta: lista de `OrderResponse`.

## Ejemplos rápidos (curl)

```bash
# Crear producto
curl -X POST http://localhost:8000/products/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Mouse",
    "description": "Inalámbrico",
    "price": 25.5,
    "stock": 50
  }'

# Listar productos
curl http://localhost:8000/products/

# Crear orden (usa un id de producto válido)
curl -X POST http://localhost:8000/orders/ \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": 1,
    "customer_name": "Ana",
    "customer_address": "Av. Principal",
    "customer_phone": "+51 988 888 888",
    "quantity": 3
  }'

# Listar órdenes
curl http://localhost:8000/orders/
```

## Estructura del proyecto

```
backend/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models/
│   │   ├── product.py
│   │   └── order.py
│   ├── routes/
│   │   ├── product_routes.py
│   │   └── order_routes.py
│   └── schemas/
│       ├── product.py
│       └── order.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Notas

- CORS está abierto (`*`) para facilitar desarrollo local.
- Pydantic `Config.from_attributes = True` habilita conversión desde objetos SQLAlchemy en respuestas.
- La conexión a DB usa variables separadas para el contenedor de Postgres (`POSTGRES_*`) y la API (`DB_*`) para mayor claridad.
- Documentación interactiva disponible en `/docs` (Swagger) y `/redoc`.

## Licencia

Proyecto para fines académicos. Ajusta según tus necesidades.
