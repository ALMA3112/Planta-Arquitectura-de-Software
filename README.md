# Planta 

 Arquitectura de Software · Universidad Sergio Arboleda · 2026-03.
Equipo: Carlos Cardona, Francisco Morales, Andres (cuyo compañero no sabemos el apellido)

## Estructura

```
PLANTA/
├── backend/                     API en Python + Flask (solo JSON)
│   ├── app.py                   raíz de composición: crea la app y registra rutas
│   ├── presentacion/            controlador REST, DTO, mapper (RA6), manejo de errores (RF6)
│   ├── aplicacion/              casos de uso: DiagnosticarPlanta, ListarEspecies
│   ├── dominio/                 entidades, reglas de negocio, puerto RepositorioRangos (RA5)
│   ├── infraestructura/         capa de abastecimiento: repositorio CSV, CORS, ensamblaje
│   ├── tests/                   pruebas unitarias del dominio (sin servidor ni CSV)
│   └── requirements.txt
├── front/                       cliente web estático (HTML + CSS + JS, `fetch`)
└── docs/                        documento de arquitectura, diagramas, bitácora de IA
```

Las dependencias van siempre hacia el dominio; el dominio solo importa `abc` y `enum`.
Detalle completo en [`docs/arquitectura.docx`](docs/arquitectura.docx).

## Requisitos

- Python 3.10 o superior
- `pip`
- Un navegador moderno

## Ejecutar el backend

Desde la carpeta `backend/`:

```bash
# 1. Entorno virtual (recomendado)
python -m venv .venv
source .venv/bin/activate        # Windows (PowerShell): .venv\Scripts\Activate.ps1

# 2. Dependencias
pip install -r requirements.txt

# 3. Levantar la API
python app.py
```

La API queda en `http://127.0.0.1:5000`.
Comprobación rápida: abrir `http://127.0.0.1:5000/api/v1/especies` (debe devolver un JSON con 17 especies).

## Ejecutar el front

El front es un sitio estático **servido por separado** del backend (RA2). Con el backend ya corriendo, abrir **otra terminal** y desde la carpeta `front/`:

```bash
python -m http.server 5500
```

Luego abrir `http://localhost:5500` en el navegador.

> Sirva el front por HTTP (no abriendo `index.html` con doble clic): CORS solo admite orígenes `http://localhost` / `http://127.0.0.1` en los puertos **5500** y **8000**. Con la extensión *Live Server* de VS Code (puerto 5500 por defecto) también funciona.

El front llama a `http://127.0.0.1:5000/api/v1` (constante `URL_BASE` al inicio de `front/app.js`).

## Ejecutar las pruebas

Desde la carpeta `backend/`:

```bash
python -m pytest -v
```

Las pruebas ejercitan el dominio y los casos de uso con un doble de prueba de `RepositorioRangos`: no levantan Flask ni leen `especies.csv`.

## API

### `POST /api/v1/diagnosticos`

```json
{ "especie": "sansevieria", "humedad": 32.5, "luz": 850, "temperatura": 21.0 }
```

`200 OK`: `especie`, `estado` (índice de vitalidad), `parametros[]` (nombre, valor, unidad, rangoOptimo, estado) y `recomendaciones[]`.

### `GET /api/v1/especies`

`200 OK`: lista de `{ "nombre": ..., "rangos": { "humedad": {"min", "max"}, "luz": {...}, "temperatura": {...} } }`.

### Errores (cuerpo uniforme `{ "error", "mensaje", "detalle" }`)

| Situación | HTTP | `error` |
|---|---|---|
| Especie desconocida | 404 | `ESPECIE_NO_SOPORTADA` |
| Parámetro ausente, no numérico o fuera del rango físico posible | 400 | `PARAMETRO_INVALIDO` |

Rangos físicos aceptados: humedad 0–100 %, luz 0–200 000 lux, temperatura −50–80 °C.

## CORS

`infraestructura/configuracion_cors.py` permite únicamente los orígenes del front local (puertos 5500 y 8000 en `localhost` y `127.0.0.1`) y solo sobre `/api/*`. Para otro origen (por ejemplo, un despliegue) no hace falta tocar código:

```bash
CORS_ORIGINS="https://mi-front.example.com" python app.py
# Windows (PowerShell):  $env:CORS_ORIGINS="https://mi-front.example.com"; python app.py
```

## Tabla de referencia

`backend/infraestructura/datos/especies.csv` (17 especies). Fuentes de los valores en [`docs/fuentes_rangos.md`](docs/fuentes_rangos.md).
Migrar a base de datos implica **una clase nueva** en `infraestructura/` que implemente `RepositorioRangos` y cambiar las líneas de `infraestructura/configuracion.py` que nombran la clase concreta (import, tipo de retorno y construcción); el dominio no cambia.

## Documentación

- [`docs/arquitectura.docx`](docs/arquitectura.docx) — documento de arquitectura
- [`docs/diagramas/`](docs/diagramas/) — diagramas de clases y de secuencia (fuente editable: `PROYECTO.mdj`)
- [`docs/bitacora_ia.md`](docs/bitacora_ia.md) — bitácora de uso de IA
