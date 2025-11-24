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

Usar MySQL Workbench (GUI)

- Abrir MySQL Workbench → Server → Data Import
- Seleccionar "Import from Self-Contained File" y elegir el archivo SQL que te entregaron 
- Click en "Start Import".



5) Ajustar las credenciales en `config/settings.py` (si es necesario)
 

Ejemplo (editar `config/settings.py`):

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'logistica_forestal',  # cnombre por defecto de la base de datos
        'USER': 'root',
        'PASSWORD': 'su_password',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {'charset': 'utf8mb4'},
    }
}
```

6) Ejecutar migraciones (opcional/seguro)

Si el dump ya incluye `django_migrations`, no es estrictamente necesario correr `migrate`, pero no hace daño y garantizará que el esquema esté actualizado:

```powershell
cd D:\ruta\LogisticaFores
python manage.py migrate
```

7) Crear un superusuario (si quieres acceder al admin)

En la terminal debera ejecutar los siguientes comandos (email es opcional)

```powershell
python manage.py createsuperuser
# Sigue las instrucciones (username, email, password)
```

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
- Si al importar el dump aparece error por user/privilegios, intenta importar como `root`.

10) (Opcional) Echar un vistazo rápido a este repo

- Carpeta `gestion/` contiene la app principal con modelos `Vehiculo` y `MovimientoCarga`.
- `manage.py` es el entrypoint para comandos Django.
- `scripts/` contiene utilidades para export/import de la base.
---
