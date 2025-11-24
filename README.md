Este README explica cómo preparar el entorno, importar la base de datos MySQL y ejecutar la aplicación Django sin problemas.

---

Requisitos previos en la máquina del profesor
# Instrucciones rápidas para ejecutar el proyecto

Aquí tienes un README limpio y sencillo con lo mínimo necesario para que el profesor ejecute la aplicación y cargue la base de datos usada por el proyecto.




✅ Requisitos
- Python 3.11+ instalado y en PATH
- MySQL Server (8.x) o MySQL Workbench instalado
- Git instalado

🚀 Preparación APP (pasos mínimos)

1) Clonar el repositorio

```powershell
cd C:\ruta\donde\quieres\trabajar
git clone <URL_DEL_REPO>
cd LogisticaFores
```

2) Crear y activar el entorno virtual

```powershell
python -m venv venv
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process -Force  # si PowerShell bloquea la activación
.\venv\Scripts\Activate.ps1
```

3) Instalar dependencias

```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

🗄️ Preparación DATABASE (solo lo necesario)

- Nombre de la base de datos que usa el proyecto: `logistica_forestal`.

4) Importar la base de datos

- Opción recomendada (MySQL Workbench GUI):

  Server → Data Import → Import from Self-Contained File → seleccionar `db_dump.sql` → Start Import

- Opción línea de comandos (si el archivo está en `C:\ruta\a\db_dump.sql`):

```powershell
"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u root -p < C:\ruta\a\db_dump.sql
```


⚙️ Ajustes

5) Si tu MySQL usa otras credenciales, edita `config/settings.py` y asegúrate de que `DATABASES['default']['NAME']` esté en `logistica_forestal` y que `USER`/`PASSWORD`/`HOST`/`PORT` sean correctos.

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'logistica_forestal',
        'USER': 'root',
        'PASSWORD': 'su_password',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {'charset': 'utf8mb4'},
    }
}
```

🔐 Crear superusuario (opcional)

```powershell
python manage.py createsuperuser
```

▶️ Ejecutar la aplicación

```powershell
python manage.py runserver
# Abrir en: http://127.0.0.1:8000/
```

🔧 Problemas comunes

- Si falta `pymysql`: ejecutar `pip install -r requirements.txt` dentro del venv.
- Si PowerShell bloquea la activación: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process -Force`.
- Si la importación falla por permisos: intentar con `root` o crear la base `logistica_forestal` manualmente antes de importar.

