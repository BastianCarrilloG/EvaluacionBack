# Sistema de Gestión de Logística Forestal

## Descripción del Sistema

LogísticaFores es una aplicación web desarrollada en Django para la gestión operativa de transporte y movimientos de carga en operaciones forestales. Permite registrar vehículos (camiones, camionetas, maquinaria) y llevar un registro detallado de cada movimiento de carga (ingresos/salidas), con información temporal, origen, destino y descripción.

**Características principales:**
- Autenticación de usuarios con sesiones seguras
- CRUD completo de vehículos con validación de patentes chilenas
- Registro de movimientos de carga con validaciones de fechas
- Interfaz responsiva con Bootstrap 5
- Base de datos MySQL 8.0 para persistencia de datos

---

## Modelo de Datos

El sistema utiliza dos modelos principales con relación One-to-Many:

```
┌─────────────────────────────────┐
│         VEHÍCULOS               │
├─────────────────────────────────┤
│ id (PK)                         │
│ patente (unique, AAAA11)        │◄─────────┐
│ marca (varchar)                 │          │
│ modelo (varchar)                │          │ 1 a Muchos
│ tipo (CAMIÓN/CAMIONETA/MAQUIN)  │          │ (relación)
│ año (PositiveInteger)           │          │
└─────────────────────────────────┘          │
                                             │
        ┌──────────────────────────────────────────┐
        │     MOVIMIENTOS DE CARGA                 │
        ├──────────────────────────────────────────┤
        │ id (PK)                                  │
        │ vehiculo_id (FK → Vehículos)             │
        │ tipo_movimiento (INGRESO/SALIDA)         │
        │ fecha_hora (DateTime)                    │
        │ origen (varchar)                         │
        │ destino (varchar)                        │
        │ descripcion (TextField)                  │
        └──────────────────────────────────────────┘
```

**Relaciones:**
- Cada Vehículo puede tener múltiples MovimientosCarga
- Al eliminar un Vehículo, sus movimientos se eliminan automáticamente (CASCADE)

---

## Requisitos previos en la máquina del profesor

✅ **Necesario tener instalado:**
- Python 3.11+ en PATH
- MySQL Server (8.x) o MySQL Workbench
- Git

---

## 🚀 Guía de Instalación Rápida

### 1) Clonar el repositorio

```powershell
cd C:\ruta\donde\quieres\trabajar
git clone <URL_DEL_REPO>
cd LogisticaFores
```

### 2) Crear y activar el entorno virtual

```powershell
python -m venv venv
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process -Force
.\venv\Scripts\Activate.ps1
```

### 3) Instalar dependencias

```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

### 4) Importar la base de datos

**Opción A: MySQL Workbench (recomendado):**
1. Abrir MySQL Workbench
2. Server → Data Import → Import from Self-Contained File
3. Seleccionar `db_dump.sql` de la carpeta `data/`
4. Clic en "Start Import"

**Opción B: Línea de comandos:**

```powershell
"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u root -p < C:\ruta\a\db_dump.sql
```

### 5) Configurar credenciales (si es necesario)

Editar `config/settings.py` y ajustar `DATABASES`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'logistica_forestal',
        'USER': 'root',
        'PASSWORD': 'tu_contraseña',  # Cambiar si es distinto
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {'charset': 'utf8mb4'},
    }
}
```

### 6) Crear superusuario (opcional)

```powershell
python manage.py createsuperuser
```

### 7) Ejecutar la aplicación

```powershell
python manage.py runserver
```

Abrir navegador en: **http://127.0.0.1:8000/**

---

## 🔧 Solución de Problemas

| Problema | Solución |
|----------|----------|
| `pymysql not found` | `pip install -r requirements.txt` dentro del venv |
| PowerShell bloquea activación | `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process -Force` |
| Error al importar BD | Crear base manualmente: `CREATE DATABASE logistica_forestal;` |
| Conexión a MySQL fallida | Verificar que MySQL Server está corriendo; revisar USER/PASSWORD en settings.py |

---

## 📁 Estructura del Proyecto

```
LogisticaFores/
├── config/                  # Configuración Django
│   ├── settings.py         # Configuración de aplicación
│   ├── urls.py             # URLs principales
│   └── wsgi.py             # Configuración para producción
├── gestion/                # Aplicación principal
│   ├── models.py           # Modelos Vehiculo, MovimientoCarga
│   ├── views.py            # Vistas CRUD
│   ├── forms.py            # Formularios con validaciones
│   ├── urls.py             # URLs de la aplicación
│   ├── templates/          # Plantillas HTML
│   │   ├── base.html       # Base con navbar
│   │   ├── login.html      # Login con Bootstrap
│   │   ├── vehiculos/      # Templates CRUD vehículos
│   │   └── movimientos/    # Templates CRUD movimientos
│   └── migrations/         # Migraciones de BD
├── manage.py              # Script de gestión Django
├── requirements.txt       # Dependencias Python
└── README.md             # Este archivo
```

---

## 📊 Validaciones Implementadas

| Campo | Validación |
|-------|-----------|
| **Patente** | Formato: AAAA11 (4 letras + 2 números), Único en BD |
| **Año** | Rango: 1900 - año_actual + 1 |
| **Fecha/Hora** | No puede ser en el futuro |
| **Autenticación** | Requerida en todas las vistas operacionales |

---

## 🔐 Seguridad

- ✅ Contraseñas hasheadas con PBKDF2-SHA256
- ✅ Protección CSRF en todos los formularios
- ✅ Sesiones seguras con Django
- ✅ Acceso restringido con `@login_required`

---

## 📝 Notas Finales

- Base de datos recomendada: `logistica_forestal`
- Archivo de volcado: `data/db_dump.sql`
- Variables de entorno: Se recomienda usar `.env` para credenciales en producción
- Documentación de código: Todas las funciones incluyen docstrings descriptivos

¿Preguntas? Revisar logs en terminal o contactar al desarrollador.
