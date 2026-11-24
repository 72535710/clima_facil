# Clima Fácil

Aplicación web para pequeños agricultores de Huancayo y el Valle del Mantaro, Perú. Muestra las condiciones meteorológicas en tiempo real desde Open-Meteo y recomendaciones agrícolas prácticas almacenadas en SQL Server.

> **Aviso:** Las reglas y umbrales meteorológicos son de carácter orientativo con fines académicos. No constituyen alertas oficiales de SENAMHI.

---

## Descripción

Clima Fácil nació como proyecto académico para acercar información climática útil a agricultores del Valle del Mantaro. Presenta datos reales del clima actual, el pronóstico de siete días, recomendaciones por cultivo y un historial de consultas, todo en un lenguaje sencillo y en una interfaz responsiva.

---

## Objetivo

Facilitar el acceso a información meteorológica comprensible para pequeños productores de Papa, Maíz y Haba de la sierra central del Perú, apoyando la toma de decisiones agrícolas cotidianas.

---

## Tecnologías utilizadas

| Capa | Tecnología |
|---|---|
| Frontend | Angular 22 (modo zoneless, standalone) |
| Backend | FastAPI (Python) |
| Base de datos | SQL Server (ODBC Driver 17 o 18) |
| Datos meteorológicos | Open-Meteo API (libre, sin clave) |
| Estilos | Bootstrap 5.3 + Bootstrap Icons |
| ORM | Sin ORM — pyodbc directo con procedimientos almacenados |
| Tests frontend | Vitest + Angular Testing |
| Tests backend | Script propio con FastAPI TestClient |

---

## Arquitectura

```
Usuario (navegador)
        │
        ▼
  Angular 22 SPA        ← http://localhost:4200
  (ng serve / dist)
        │
        │ HTTP REST (JSON)
        ▼
  FastAPI Backend        ← http://localhost:8000
        │             │
        │             └──► Open-Meteo API (internet)
        │                  (clima actual y pronóstico 7 días)
        │
        ▼
  SQL Server (pyodbc)
  ClimaFacilDB
  (Cultivo, Recomendacion, Ubicacion, Historial)
```

---

## Estructura de carpetas

```
clima_facil/
├── backend/
│   ├── app/
│   │   ├── config.py          # Variables de entorno
│   │   ├── database.py        # Conexión pyodbc a SQL Server
│   │   ├── main.py            # FastAPI app + CORS + lifespan
│   │   ├── routes/            # Endpoints REST
│   │   │   ├── clima.py       # GET /api/clima/actual y /pronostico
│   │   │   ├── cultivos.py    # GET /api/cultivos
│   │   │   ├── recomendaciones.py  # GET /api/recomendaciones
│   │   │   └── historial.py   # GET y POST /api/historial
│   │   ├── schemas/           # Modelos Pydantic (request/response)
│   │   └── services/
│   │       ├── db_service.py      # Lógica de acceso a SQL Server
│   │       ├── open_meteo.py      # Cliente HTTP para Open-Meteo
│   │       └── weather_rules.py   # Umbrales meteorológicos orientativos
│   ├── .env                   # Variables de entorno locales (no subir a Git)
│   ├── .env.example           # Plantilla de configuración
│   ├── .gitignore
│   ├── requirements.txt
│   ├── run.py                 # Punto de entrada con uvicorn
│   └── test_backend.py        # Suite de pruebas del backend
│
├── database/
│   ├── 01_crear_base_datos.sql
│   ├── 02_crear_tablas.sql
│   ├── 03_insertar_datos.sql
│   └── 04_procedimientos.sql
│
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── components/    # Navbar y Footer
│   │   │   ├── config/        # api.config.ts
│   │   │   ├── models/        # Interfaces TypeScript
│   │   │   ├── pages/         # Inicio, Pronóstico, Recomendaciones, Cultivos, Historial
│   │   │   └── services/      # ClimaService, CultivosService, RecomendacionesService
│   │   ├── environments/
│   │   └── styles.css
│   ├── .gitignore
│   ├── angular.json
│   └── package.json
│
└── README.md
```

---

## Requisitos de instalación

### Backend

- Python 3.11 o superior
- SQL Server (Express o superior) con ODBC Driver 17 o 18
- Acceso a internet (para Open-Meteo)

```bash
cd backend
pip install -r requirements.txt
```

### Frontend

- Node.js 20 o superior
- Angular CLI 22

```bash
cd frontend
npm install
```

---

## Configuración de la base de datos

Ejecutar los scripts SQL en orden desde SQL Server Management Studio u otra herramienta compatible:

```sql
-- 1. Crear la base de datos
-- database/01_crear_base_datos.sql

-- 2. Crear las cuatro tablas con sus restricciones
-- database/02_crear_tablas.sql

-- 3. Insertar datos iniciales (Ubicacion, Cultivos, Recomendaciones)
-- database/03_insertar_datos.sql

-- 4. Crear los cuatro procedimientos almacenados
-- database/04_procedimientos.sql
```

Los scripts son **idempotentes**: pueden ejecutarse sobre una base de datos existente sin duplicar datos ni romper la estructura.
Los scripts usan `ClimaFacilDB` por defecto. Para reconstruir una base temporal independiente, sustituir todas las apariciones de `ClimaFacilDB` por el nombre temporal elegido antes de ejecutar los cuatro scripts en orden.

---

## Configuración del backend

Copiar el archivo de ejemplo y ajustar los valores:

```bash
cd backend
copy .env.example .env   # Windows
# cp .env.example .env   # Linux/Mac
```

Editar `backend/.env`:

```env
# Servidor SQL Server
DB_SERVER=localhost\SQLEXPRESS
DB_NAME=ClimaFacilDB
DB_DRIVER=ODBC Driver 17 for SQL Server
DB_TRUSTED_CONNECTION=yes

# Si se usa autenticación SQL en lugar de Windows:
# DB_USER=tu_usuario
# DB_PASSWORD=tu_contraseña

# Coordenadas de Huancayo (no modificar salvo necesidad)
HUANCAYO_LATITUDE=-12.0651
HUANCAYO_LONGITUDE=-75.2049

# Puerto y CORS
API_PORT=8000
CORS_ORIGIN=http://localhost:4200
```

---

## Configuración del frontend

El frontend apunta al backend mediante `frontend/src/environments/environment.ts`:

```typescript
export const environment = {
  production: false,
  apiUrl: 'http://localhost:8000'
};
```

No se requiere ninguna clave de API adicional. Open-Meteo es un servicio abierto y gratuito.

---

## Ejecución

### Iniciar el backend

```bash
cd backend
python run.py
# Disponible en: http://localhost:8000
# Documentación Swagger: http://localhost:8000/docs
```

### Iniciar el frontend (desarrollo)

```bash
cd frontend
npm start
# Disponible en: http://localhost:4200
```

### Compilar el frontend (producción)

```bash
cd frontend
npm run build
# Resultado en: frontend/dist/clima-facil/
```

### Pruebas

```bash
# Pruebas del backend (requiere SQL Server activo)
cd backend
python test_backend.py

# Pruebas unitarias del frontend
cd frontend
npm test
```

---

## Funcionalidades principales

| Página | Descripción |
|---|---|
| **Inicio** | Clima actual (temperatura, humedad, lluvia, viento) desde Open-Meteo y recomendación destacada desde SQL Server. Permite guardar la consulta en el historial. |
| **Pronóstico** | Pronóstico de 7 días con temperatura máxima/mínima, probabilidad de lluvia, precipitación esperada y descripción del cielo. |
| **Recomendaciones** | Lista completa de consejos agrícolas desde SQL Server con filtro por cultivo (Papa, Maíz, Haba). |
| **Cultivos** | Catálogo de los tres cultivos del Valle del Mantaro con descripción desde SQL Server. |
| **Historial** | Tabla de consultas registradas en SQL Server. Permite registrar nuevas consultas con los datos climáticos actuales. |

---

## Endpoints REST

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/` | Estado del backend |
| GET | `/api/clima/actual` | Clima actual desde Open-Meteo |
| GET | `/api/clima/pronostico` | Pronóstico de 7 días desde Open-Meteo |
| GET | `/api/cultivos` | Lista de cultivos desde SQL Server |
| GET | `/api/recomendaciones` | Recomendaciones (filtrable por `?id_cultivo=N`) |
| GET | `/api/historial` | Historial (filtrable por `?id_ubicacion=N`) |
| POST | `/api/historial` | Registrar nueva consulta en el historial |
| GET | `/docs` | Documentación interactiva Swagger UI |

---

## Notas de desarrollo

- El frontend usa **Angular zoneless** (`provideZonelessChangeDetection`). Todas las suscripciones HTTP utilizan `ChangeDetectorRef.markForCheck()` para actualizar la vista.
- La conexión a SQL Server utiliza **pyodbc** con procedimientos almacenados, sin ORM.
- Los datos meteorológicos provienen de **Open-Meteo** (latitud -12.0651, longitud -75.2049 — Huancayo).
- El proyecto no usa autenticación de usuarios ni sesiones.
