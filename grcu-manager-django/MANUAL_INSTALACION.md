# Manual de Instalación - GRCU Manager

## Tabla de Contenidos
1. Introducción
2. Requisitos del Sistema
3. Instalación para Desarrollo
4. Instalación para Producción
5. Configuración Inicial
6. Solución de Problemas
7. Recursos Adicionales
8. Licencia

---

## Introducción

**GRCU Manager** es una aplicación web desarrollada con Django 5.2.6 para la gestión de requerimientos y casos de uso en proyectos de software. Este manual describe el proceso completo de instalación tanto para entornos de desarrollo como de producción.

### ¿Qué incluye este manual?
- Configuración del entorno de desarrollo local
- Instalación de dependencias
- Configuración de base de datos
- Configuración de variables de entorno
- Preparación para producción
- Troubleshooting común

---

## Requisitos del Sistema

### Software Requerido

#### Obligatorio
- **Python**: 3.10 o superior (recomendado 3.13.9)
- **pip**: Gestor de paquetes de Python (incluido con Python)
- **Git**: Sistema de control de versiones
- **Navegador web**: Chrome, Firefox, Edge o Safari (actualizado)



#### Opcional (según configuración)
- **PostgreSQL**: 14 o superior (para producción)
- **SQLite**: Incluido con Python (para desarrollo)

### Requisitos de Hardware Mínimos
- **Procesador**: Dual-core 2.0 GHz o superior
- **RAM**: 4 GB mínimo (8 GB recomendado)
- **Disco**: 500 MB de espacio libre
- **Conexión a Internet**: Para descargar dependencias

### Sistemas Operativos Soportados
- Linux (Ubuntu 20.04+, Debian, CentOS, etc.)
- macOS 11+
- Windows 10/11

---

## Instalación para Desarrollo

### Paso 1: Instalación de Python

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3.13 python3.13-venv python3-pip git
```


#### Linux (OpenSUSE)
```bash
sudo zypper refresh
sudo zypper install python3 python3-pip python3-venv git
# Si necesitas una versión específica de Python:
sudo zypper install python3.13
```

#### macOS
```bash
# Usando Homebrew
brew install python@3.13 git
```

#### Windows
1. Descargar Python desde [python.org](https://www.python.org/downloads/)
2. Durante la instalación, marcar "Add Python to PATH"
3. Instalar Git desde [git-scm.com](https://git-scm.com/)

#### Linux (OpenSUSE) Nota
> Los comandos específicos de despliegue (permisos, servicios y PostgreSQL) se detallan en las secciones de Base de Datos y Producción más adelante.
### Paso 2: Clonar el Repositorio

```bash
# Clonar el proyecto
git clone https://github.com/uarg-unpa/grcu-manager.git

# Navegar al directorio del proyecto
cd grcu-manager/grcu-manager-django
```

### Paso 3: Crear Entorno Virtual

El entorno virtual aísla las dependencias del proyecto del sistema.

```bash
# Crear entorno virtual
python3 -m venv venv

# Activar el entorno virtual (Linux/macOS)
source venv/bin/activate
```

En Windows (PowerShell):
```powershell
venv\Scripts\Activate.ps1
```

**Nota**: Verás `(venv)` al inicio de tu línea de comandos cuando esté activo.

### Paso 4: Instalar Dependencias

```bash
# Actualizar pip a la última versión
pip install --upgrade pip

# Instalar todas las dependencias del proyecto
pip install -r requirements.txt
```

**Dependencias principales incluidas:**
- Django 5.2.6 - Framework web
- reportlab 4.0.7 - Generación de PDFs
- pillow 11.3.0 - Procesamiento de imágenes
- python-decouple 3.8 - Gestión de configuración
- django-simple-history 3.10.1 - Auditoría
- openpyxl 3.1.2 - Exportación Excel
- psycopg2-binary 2.9.10 - Conector PostgreSQL (opcional)

### Paso 5: Configurar Variables de Entorno

Crear archivo `.env` en la raíz del proyecto:

```bash
# Copiar el archivo de ejemplo (si existe)
# O crear uno nuevo
touch .env
```

Editar el archivo `.env` con el siguiente contenido:

```env
# Configuración básica de Django
SECRET_KEY='django-insecure-bu0!u5+)!ac&of*_q*6ew12%h)voiu^1_^@i9^0b+$qeum#cvl'
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,localhost:8000

# Base de datos PostgreSQL (opcional - comentar si usas SQLite)
# DB_NAME=grcu_db
# DB_USER=grcu
# DB_PASSWORD=grcu010203
# DB_HOST=localhost
# DB_PORT=5432

# Google OAuth (opcional - solo si usas autenticación con Google)
GOOGLE_CLIENT_ID=tu-client-id-aqui
GOOGLE_CLIENT_SECRET=tu-client-secret-aqui
```

**IMPORTANTE**: 
- En producción, cambia `SECRET_KEY` por una clave única y segura
- Nunca compartas el archivo `.env` en repositorios públicos
- El `.env` debe estar en `.gitignore`

### Paso 6: Configurar Base de Datos

#### Opción A: SQLite (Recomendado para Desarrollo)

Por defecto, el proyecto usa SQLite. No requiere configuración adicional.

```python
# En settings.py está configurado así:
        'NAME': BASE_DIR / 'db.sqlite3',
}
```

#### Opción B: PostgreSQL (Recomendado para Producción)

1. **Instalar PostgreSQL**:

```bash
# Ubuntu/Debian
sudo apt install postgresql postgresql-contrib

# OpenSUSE
sudo zypper install postgresql-server postgresql-contrib
# Para inicializar la base de datos en OpenSUSE:
sudo systemctl enable postgresql
sudo systemctl start postgresql
sudo -u postgres initdb --locale=en_US.UTF-8 -D /var/lib/pgsql/data
sudo systemctl restart postgresql

# macOS
brew install postgresql

# Windows: Descargar desde postgresql.org
```

2. **Crear base de datos**:

```bash
# Acceder a PostgreSQL
sudo -u postgres psql

# Crear usuario y base de datos
CREATE DATABASE grcu_db;
CREATE USER grcu WITH PASSWORD 'grcu010203';
ALTER ROLE grcu SET client_encoding TO 'utf8';
ALTER ROLE grcu SET default_transaction_isolation TO 'read committed';
ALTER ROLE grcu SET timezone TO 'America/Argentina/Rio_Gallegos';
GRANT ALL PRIVILEGES ON DATABASE grcu_db TO grcu;
\q
```

3. **Descomentar configuración PostgreSQL en `settings.py`**:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
    }
}
```

4. **Actualizar `.env`** con las credenciales de PostgreSQL.

### Paso 7: Aplicar Migraciones

Las migraciones crean las tablas en la base de datos:

```bash
# Verificar migraciones pendientes
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate
```

**Salida esperada:**
```
Operations to perform:
  Apply all migrations: accounts, admin, auditoria, auth, casos_de_uso, 
  contenttypes, grupos, permisos, proyectos, requerimientos, roles, 
  sessions, usuarios
Running migrations:
  Applying permisos.0001_initial... OK
  Applying roles.0001_initial... OK
  ...
Rol 'Admin' creado
Rol 'Desarrollador' creado
Rol 'Líder' creado
Rol 'Stakeholder' creado
Rol 'Visitante' creado
```

### Paso 8: Crear Directorios de Medios

```bash
# Crear directorio para archivos subidos
mkdir -p media/grupos/logos
mkdir -p media/proyectos/logos
```

### Paso 9: Ejecutar el Servidor de Desarrollo

```bash
# Iniciar el servidor
python manage.py runserver

# O en un puerto específico
python manage.py runserver 8080
```

**Salida esperada:**
```
System check identified no issues (0 silenced).
Django version 5.2.6, using settings 'grcu_manager.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

### Paso 10: Acceder a la Aplicación

1. Abrir navegador en: `http://localhost:8000/`
2. Primera vez: Serás redirigido a configurar el administrador
3. Autenticarse con Google usando el correo autorizado
4. El sistema creará automáticamente el usuario administrador

**URLs importantes:**
- Página principal: `http://localhost:8000/`
- Panel de administración Django: `http://localhost:8000/admin/`

---

## Instalación para Producción

### Consideraciones de Producción

1. **Nunca usar `DEBUG=True` en producción**
2. **Configurar un servidor WSGI** (Gunicorn, uWSGI)
3. **Usar un servidor web** como proxy reverso (Nginx, Apache)
4. **Configurar HTTPS** con certificados SSL
5. **Usar PostgreSQL** en lugar de SQLite
6. **Configurar backups automáticos** de la base de datos

### Configuración Básica de Producción

#### 1. Actualizar `.env` para producción:

```env
SECRET_KEY='GENERAR-UNA-CLAVE-SEGURA-UNICA-AQUI'
DEBUG=False
ALLOWED_HOSTS=tudominio.com,www.tudominio.com

# PostgreSQL (obligatorio en producción)
DB_NAME=grcu_db_prod
DB_USER=grcu_prod
DB_PASSWORD=contraseña-segura-aqui
DB_HOST=localhost
DB_PORT=5432
```

#### 2. Generar SECRET_KEY segura:

```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

#### 3. Instalar servidor WSGI (Gunicorn):

```bash
pip install gunicorn
```

#### 4. Crear archivo de configuración `gunicorn_config.py`:

```python
bind = "127.0.0.1:8000"
workers = 3
worker_class = "sync"
timeout = 120
accesslog = "/var/log/grcu/access.log"
errorlog = "/var/log/grcu/error.log"
```

#### 5. Ejecutar con Gunicorn:

```bash
gunicorn grcu_manager.wsgi:application -c gunicorn_config.py
```

#### 6. Configurar Nginx como proxy reverso:

```nginx
server {
    listen 80;
    server_name tudominio.com www.tudominio.com;

    location = /favicon.ico { access_log off; log_not_found off; }

    location /static/ {
        alias /ruta/a/grcu-manager-django/staticfiles/;
    }

    location /media/ {
        alias /ruta/a/grcu-manager-django/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

#### 7. Recolectar archivos estáticos:

```bash
python manage.py collectstatic --noinput
```
#### 8. Crear servicio systemd (Linux):

Archivo: `/etc/systemd/system/grcu.service`
```ini
[Unit]
Description=GRCU Manager Gunicorn Service
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/ruta/a/grcu-manager-django
Environment="PATH=/ruta/a/grcu-manager-django/venv/bin"
ExecStart=/ruta/a/grcu-manager-django/venv/bin/gunicorn -c /ruta/a/grcu-manager-django/gunicorn_config.py grcu_manager.wsgi:application
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now grcu.service
sudo systemctl status grcu.service --no-pager
```

---

## Configuración Inicial

### Primera Ejecución

1. **Acceder a la aplicación** por primera vez
2. Serás redirigido a `/accounts/setup-admin/`
3. **Hacer clic en "Autenticar con Google"**
4. Iniciar sesión con tu cuenta de Google
5. El sistema creará automáticamente:
   - Usuario administrador con tu email
   - Rol de "Admin" asignado
   - Permisos completos

### Configuración de Google OAuth (Opcional)

Si deseas usar autenticación con Google:

1. Ir a [Google Cloud Console](https://console.cloud.google.com/)
2. Crear un nuevo proyecto
3. Habilitar "Google+ API"
4. Crear credenciales OAuth 2.0
5. Configurar URIs de redireccionamiento:
   - `http://localhost:8000/accounts/google/callback/` (desarrollo)
   - `https://tudominio.com/accounts/google/callback/` (producción)
6. Copiar Client ID y Client Secret al `.env`

### Cargar Datos de Demostración

```bash
# Cargar datos de ejemplo (opcional)
python cargar_datos_demo.py

# O cargar datos específicos de GRCU
python cargar_datos_grcu.py
```

---

## Solución de Problemas

### Error: "ModuleNotFoundError: No module named 'django'"

**Causa**: Entorno virtual no activado o dependencias no instaladas.

**Solución**:
```bash
source venv/bin/activate  # Activar entorno virtual
pip install -r requirements.txt  # Reinstalar dependencias
```

### Error: "django.db.utils.OperationalError: no such table"

**Causa**: Migraciones no aplicadas.

**Solución**:
```bash
python manage.py migrate
```

### Error: "CSRF verification failed"

**Causa**: Configuración de `ALLOWED_HOSTS` incorrecta.

**Solución**: Verificar que tu dominio/IP esté en `ALLOWED_HOSTS` del `.env`.

### Error: "ConnectionRefusedError: [Errno 111] Connection refused" (PostgreSQL)

**Causa**: PostgreSQL no está corriendo o credenciales incorrectas.

**Solución**:
```bash
# Verificar si PostgreSQL está corriendo
sudo systemctl status postgresql

# Iniciar PostgreSQL
sudo systemctl start postgresql

# Verificar credenciales en .env
```

### Advertencia: "The directory '/path/to/static' in STATICFILES_DIRS does not exist"

**Causa**: Directorio de archivos estáticos no creado.

**Solución**:
```bash
mkdir -p static
```

### Error: "reportlab not found" al exportar PDF

**Causa**: Librería reportlab no instalada.

**Solución**:
```bash
pip install reportlab==4.0.7
```

### Puerto 8000 ya en uso

**Solución**: Usar otro puerto:
```bash
python manage.py runserver 8080
```

### Problemas con permisos en Linux

**Solución**:
```bash
# Dar permisos al directorio de medios
chmod -R 755 media/

# Asegurar propiedad correcta
sudo chown -R $USER:$USER .
```

---

## Recursos Adicionales

### Documentación Oficial
- [Documentación de Django](https://docs.djangoproject.com/en/5.2/)
- [Python Documentation](https://docs.python.org/3/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

### Archivos de Configuración Importantes
- `grcu_manager/settings.py` - Configuración principal de Django
- `grcu_manager/urls.py` - Rutas URL principales
- `.env` - Variables de entorno
- `requirements.txt` - Dependencias del proyecto

### Comandos Útiles de Django

```bash
# Ver migraciones pendientes
python manage.py showmigrations

# Crear superusuario (alternativo)
python manage.py createsuperuser

# Shell interactivo de Django
python manage.py shell

# Recolectar archivos estáticos
python manage.py collectstatic

# Verificar proyecto
python manage.py check

# Ver rutas disponibles
python manage.py show_urls  # Requiere django-extensions
```

---

## Soporte

Para problemas, consultas o sugerencias:

- **Repositorio**: [https://github.com/uarg-unpa/grcu-manager](https://github.com/uarg-unpa/grcu-manager)
- **Issues**: [https://github.com/uarg-unpa/grcu-manager/issues](https://github.com/uarg-unpa/grcu-manager/issues)
- **Universidad**: UNPA - Laboratorio de Desarrollo de Software

---

## Licencia

Este proyecto es de uso académico para la materia Laboratorio de Desarrollo de Software de la Universidad Nacional de la Patagonia Austral (UNPA).

---

**Última actualización**: Noviembre 2025  
**Versión del manual**: 1.0  
**Versión de Django**: 5.2.6
