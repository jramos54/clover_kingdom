# Proyecto FastAPI con MySQL

Este proyecto es una aplicación web construida con FastAPI y SQLAlchemy que utiliza una base de datos MySQL. La aplicación permite el registro de solicitudes de estudiantes y la asignación aleatoria de grimorios.

## Requisitos

- Python 3.12
- MySQL
- pip
- Docker
- Docker Compose

## Ejecución Local

### 1. Configuración del Entorno

#### Variables de Entorno

Crea un archivo `.env` en el directorio raíz del proyecto con el siguiente contenido:

```dotenv
DATABASE_USER=your_db_user
DATABASE_PASSWORD=your_db_password
DATABASE_HOST=localhost
DATABASE_NAME=nativelabs
```
#### Instalación de Dependencias

Crea un entorno virtual:
``` bash
python -m venv venv
```
Activa el entorno virtual:
En Windows:
```bash
venv\Scripts\activate
```
En macOS/Linux:
```bash
source venv/bin/activate
```
Instala las dependencias:
```bash
pip install -r requirements.txt

```
### 2. Configuración de la Base de Datos
Asegúrate de tener MySQL instalado y ejecutándose en tu máquina local.
Crea la base de datos:
```sql
CREATE DATABASE nativelabs;
```
Crea un usuario y otórgale permisos:
```sql
CREATE USER 'your_db_user'@'localhost' IDENTIFIED BY 'your_db_password';
GRANT ALL PRIVILEGES ON nativelabs.* TO 'your_db_user'@'localhost';
FLUSH PRIVILEGES;
```
### 3. Migraciones de la Base de Datos
Ejecuta las migraciones para crear las tablas necesarias:

```bash
alembic upgrade head
```
### 4. Ejecutar la Aplicación
Para iniciar la aplicación:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```
La aplicación estará disponible en http://localhost:8000.

# Ejecución con Docker Compose
### 1. Construir los Contenedores
``` bash
docker-compose build
```
### 2. Iniciar los Contenedores
```bash
docker-compose up
```

La aplicación estará disponible en http://localhost:8000.

Acceder a la Documentación de la API
Puedes acceder a la documentación generada automáticamente por FastAPI en http://localhost:8000/docs.

# Ejecutar las Pruebas
``` bash
pytest
```

# Diagrama de Secuencia

::: mermaid
sequenceDiagram
    participant Client
    participant FastAPI
    participant DB

    Client->>FastAPI: POST /solicitud
    FastAPI->>DB: Insertar solicitud con estado pendiente
    DB-->>FastAPI: Confirmación de inserción
    FastAPI-->>Client: Respuesta con solicitud creada

    Client->>FastAPI: PATCH /solicitud/{id}/estatus
    FastAPI->>DB: Actualizar estado de solicitud
    DB-->>FastAPI: Confirmación de actualización
    alt Solicitud aceptada
        FastAPI->>DB: Asignar grimorio aleatorio
        DB-->>FastAPI: Confirmación de asignación
    end
    FastAPI-->>Client: Respuesta con solicitud actualizada

    Client->>FastAPI: GET /solicitudes
    FastAPI->>DB: Consultar todas las solicitudes
    DB-->>FastAPI: Listado de solicitudes
    FastAPI-->>Client: Respuesta con listado de solicitudes

    Client->>FastAPI: GET /asignaciones
    FastAPI->>DB: Consultar asignaciones de grimorios
    DB-->>FastAPI: Listado de asignaciones
    FastAPI-->>Client: Respuesta con listado de asignaciones

:::

# Diagrama de Clases

::: mermaid

classDiagram
    class Solicitud {
        +int id
        +string nombre
        +string apellido
        +string identificacion
        +int edad
        +string afinidad_magica
        +string status
    }

    class GrimorioAsignacion {
        +int id
        +int solicitud_id
        +string tipo_trebol
    }

    class SolicitudRepositoryInterface {
        <<interface>>
        +create(solicitud: Solicitud): Solicitud
        +update(id: int, solicitud: Solicitud): Solicitud
        +update_status(id: int, status: string): Solicitud
        +list(): List~Solicitud~
    }

    class GrimorioAssignerInterface {
        <<interface>>
        +asignar_grimorio(solicitud: Solicitud): GrimorioAsignacion
    }

    class SolicitudRepository {
        +create(solicitud: Solicitud): Solicitud
        +update(id: int, solicitud: Solicitud): Solicitud
        +update_status(id: int, status: string): Solicitud
        +list(): List~Solicitud~
    }

    class GrimorioAssigner {
        +asignar_grimorio(solicitud: Solicitud): GrimorioAsignacion
    }

    class SolicitudService {
        -SolicitudRepositoryInterface repository
        -GrimorioAssignerInterface assigner
        +create_solicitud(solicitud: Solicitud): Solicitud
        +update_solicitud(id: int, solicitud: Solicitud): Solicitud
        +update_solicitud_status(id: int, status: string): Solicitud
        +list_solicitudes(): List~Solicitud~
    }

    SolicitudService --> SolicitudRepositoryInterface
    SolicitudService --> GrimorioAssignerInterface
    SolicitudRepository --> SolicitudRepositoryInterface
    GrimorioAssigner --> GrimorioAssignerInterface
    Solicitud *-- GrimorioAsignacion

:::
