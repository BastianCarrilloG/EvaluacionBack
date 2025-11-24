Este README explica cómo preparar el entorno, importar la base de datos MySQL y ejecutar la aplicación Django sin problemas.

---

Requisitos previos en la máquina del profesor
- Python 3.11+ instalado y en PATH
- MySQL Server (8.x) o MySQL Workbench instalado y funcionando
- Git instalado

Archivos en este repo relevantes
- `requirements.txt` — dependencias Python

1) Clonar el repositorio

Abra PowerShell y ejecute:
```powershell
cd C:\ruta\donde\quieres\trabajar
git clone <URL_DEL_REPO>
cd LogisticaFores
```

2) Preparar un entorno virtual (recomendado)

```powershell
python -m venv venv
# Si tu política de ejecución bloquea los scripts de PowerShell (activación):
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process -Force
.\venv\Scripts\Activate.ps1
# ahora el prompt debería mostrar (venv)
```

3) Instalar dependencias

```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

4) Preparar la base de datos MySQL

Opción A — Usar MySQL Workbench (GUI) (recomendado si no quieres usar línea de comandos)

- Abrir MySQL Workbench → Server → Data Import
- Seleccionar "Import from Self-Contained File" y elegir el archivo SQL que te entregaron (ej. `db_dump.sql`)
- En "Default Target Schema" puedes seleccionar "New" para crear la base con el nombre deseado o dejar que el script cree la base (si el dump incluye `CREATE DATABASE`).
- Click en "Start Import".

Opción B — Usar línea de comandos (si el archivo es `db_dump.sql` en `C:\ruta`)

Abre PowerShell y ejecuta (ajusta ruta a `mysql.exe` y credenciales):

```powershell
"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u root -p < C:\ruta\a\db_dump.sql
```

El comando pedirá la contraseña del usuario MySQL.

Opción C — Usar el script incluido `scripts\import_db.ps1`

```powershell
cd .\scripts
.\import_db.ps1 -User root -Password TU_PASS -Host 127.0.0.1 -SqlFile ..\data\db_dump.sql
```

Nota: Si el dump incluye `CREATE DATABASE` y `USE nombre_db`, la importación creará la base de datos automáticamente.

5) Ajustar las credenciales en `config/settings.py` (si es necesario)

El proyecto trae una configuración por defecto en `config/settings.py` que usa MySQL. Antes de ejecutar la app, verifica que los valores de `DATABASES['default']` coincidan con los de la máquina del profesor (usuario/contraseña/host/port). Si prefieres, reemplaza los valores por los del entorno del profesor.

Ejemplo (editar `config/settings.py`):

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'logistica_forestal',  # cambia si el profesor importó con otro nombre
        'USER': 'root',
        'PASSWORD': 'su_password',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {'charset': 'utf8mb4'},
    }
}
```

Alternativa (recomendada para producción/seguridad): usar variables de entorno y `django-environ`. Para este entregable no es obligatorio.

6) Ejecutar migraciones (opcional/seguro)

Si el dump ya incluye `django_migrations`, no es estrictamente necesario correr `migrate`, pero no hace daño y garantizará que el esquema esté actualizado:

```powershell
cd D:\ruta\LogisticaFores
python manage.py migrate
```

7) Crear un superusuario (si quieres acceder al admin)

Si el dump no incluye un admin válido, crea uno:

```powershell
python manage.py createsuperuser
# Sigue las instrucciones (username, email, password)
```

Si el dump ya contiene un usuario admin (por ejemplo `AdminUser`), puedes usar esas credenciales si las conoces; de lo contrario crear un nuevo superuser es la opción más simple.

8) Ejecutar la aplicación

```powershell
python manage.py runserver

# Abrir en el navegador:
http://127.0.0.1:8000/
```

Acceder al admin:
```
http://127.0.0.1:8000/admin/
```

9) Consejos finales y resolución de problemas

- Si aparece error `ModuleNotFoundError: No module named 'pymysql'`, asegúrate de haber ejecutado `pip install -r requirements.txt` dentro del venv.
- Si MySQL no está en PATH, usa la ruta completa a `mysql.exe` / `mysqldump.exe` como en los ejemplos.
- Si PowerShell impide activar el venv por políticas, ejecuta:
  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process -Force
  .\venv\Scripts\Activate.ps1
  ```
- Si al importar el dump aparece error por user/privilegios, intenta importar como `root` o pide al profesor que cree la base manualmente y luego ejecute el `.sql` sobre esa base.

10) (Opcional) Echar un vistazo rápido a este repo

- Carpeta `gestion/` contiene la app principal con modelos `Vehiculo` y `MovimientoCarga`.
- `manage.py` es el entrypoint para comandos Django.
- `scripts/` contiene utilidades para export/import de la base.
- `README_DB.md` tiene instrucciones adicionales sobre export/import.

---

Si quieres, puedo:
- Mover el `db_dump.sql` al repo bajo `data/db_dump.sql` y añadir un `data/.gitkeep`.
- Añadir instrucciones más cortas en la raíz `README.md`.

Si te parece bien, indícame si quieres que mueva/commitee el SQL (yo puedo tomar el archivo si lo subes aquí), o si prefieres subirlo tú mismo.
