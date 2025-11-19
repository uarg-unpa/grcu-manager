# Manual de instalación — GRCU Manager

Última actualización: 19 de noviembre de 2025

Este documento describe los pasos para instalar y poner en marcha el proyecto GRCU Manager (Django) en distintos sistemas operativos: Windows, Linux (Fedora, Debian/Ubuntu, openSUSE) y macOS. Está pensado para entornos de desarrollo y contiene notas para despliegue en producción.

Aunque el proyecto usa SQLite por defecto (archivo `db.sqlite3` incluido en el repo para desarrollo), también describimos los pasos básicos para usar PostgreSQL en producción.

## Contenido
- Introducción
- Requisitos generales
- Preparación del entorno
- Instalación en Windows
- Instalación en Linux
  - Fedora
  - Debian
  - openSUSE
- Instalación en macOS
- Configuración del proyecto
  - Variables de entorno y `.env` de ejemplo
  - Base de datos
  - Migraciones y datos iniciales
- Ejecutar la aplicación en local
- Despliegue (notas rápidas)
- Solución de problemas comunes
- Pruebas y verificación
- Preguntas frecuentes (FAQ)
- Apéndice: comandos útiles y referencias

---

## Introducción

GRCU Manager es una herramienta web diseñada para que los desarrolladores de software puedan gestionar requisitos y casos de uso de una manera profesional y clara. Provee historial de cambios por elemento y un sistema de discusión que permite al cliente participar activamente en el proceso de validación de los requerimientos. Este manual te guía desde la instalación de dependencias del sistema operativo, la creación de un entorno virtual Python, la configuración del proyecto y su ejecución local, hasta recomendaciones básicas para desplegar en producción.

## Requisitos generales

- Git
- Python 3.11+ (se ha probado con 3.11.x)
- pip
- Virtual environment (venv) o una alternativa como `virtualenv` o `pyenv-virtualenv`
- Node/npm (opcional, sólo si querés compilar activos frontend adicionales)
- En producción: servidor WSGI (Gunicorn/uvicorn) y servidor HTTP (nginx) o plataforma hosting (Render, Heroku, etc.)

Requerimientos Python del proyecto están en `requirements.txt`.

## Preparación del entorno

Pasos comunes (se repiten en todas las plataformas):

1. Clonar el repositorio:

```bash
git clone https://github.com/uarg-unpa/grcu-manager.git
cd grcu-manager/grcu-manager-django
```

2. Crear y activar un entorno virtual Python:

Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows (PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Actualizar pip y wheel

```bash
pip install --upgrade pip wheel
```

4. Instalar dependencias del proyecto

```bash
pip install -r requirements.txt
```

5. Copiar archivo de ejemplo de variables de entorno (ver sección de configuración abajo) y editar según corresponda.

---

## Instalación en Windows

1. Instalar Python 3.11+ desde python.org o usar Windows Store. Asegurate de marcar "Add Python to PATH".
2. Instalar Git para Windows (Git Bash) si no lo tenés.
3. Abrir PowerShell o Git Bash y seguir los pasos de "Preparación del entorno".
4. Variables de entorno en Windows: podés crear un archivo `.env` en la raíz del proyecto o definir variables de entorno del sistema. Recomendamos usar un `.env` y una librería como `python-dotenv` si el proyecto la carga (si no, exportar variables en el PowerShell antes de ejecutar).

Ejecutar servidor en desarrollo:

```powershell
# Activar entorno
.\.venv\Scripts\Activate.ps1

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Ejecutar servidor
python manage.py runserver
```

---

## Instalación en Linux

Recomendación general: usar el gestor de paquetes de la distribución para instalar Python y herramientas (git, build-essential si es necesario).

### Fedora

```bash
sudo dnf update -y
sudo dnf install -y git python3 python3-venv python3-devel gcc redhat-rpm-config
```

Luego seguir los pasos de "Preparación del entorno".

### Debian

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y git python3 python3-venv python3-dev build-essential
```

Luego seguir los pasos de "Preparación del entorno".

### openSUSE

```bash
sudo zypper refresh
sudo zypper install -y git python3 python3-virtualenv python3-devel gcc make
```

Luego seguir los pasos de "Preparación del entorno".

Notas sobre dependencias del sistema: algunas dependencias Python (por ejemplo, si usás Pillow o dependencias que compilan extensiones) pueden requerir librerías de sistema adicionales (`libjpeg-devel`, `zlib`, etc.). Si durante `pip install -r requirements.txt` ves errores de compilación revisá el mensaje (por ejemplo `libjpeg` o `freetype`) y añadí los paquetes de desarrollo correspondientes.

---

## Instalación en macOS

1. Instalar Homebrew (si no lo tenés):

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

2. Instalar Python y Git:

```bash
brew update
brew install git python@3.11
```

3. Verificar `python3` apunta a la versión correcta o usar el path completo. Crear entorno virtual y seguir los pasos de "Preparación del entorno".

4. Si necesitás compilación de paquetes nativos instalá las herramientas de línea de comandos Xcode:

```bash
xcode-select --install
```

---

## Configuración del proyecto

### Variables de entorno (archivo `.env`)

Para desarrollo puedes crear un archivo `.env` en la raíz del proyecto con las variables mínimas. Ejemplo de `.env`:

```
DEBUG=True
SECRET_KEY=django-insecure-REEMPLAZAR_POR_UNA_LLAVE_SECRETA
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
# Si usas PostgreSQL en producción:
# DATABASE_URL=postgres://usuario:password@host:5432/dbname

# Google OAuth (opcional para login)
GOOGLE_CLIENT_ID=tu_google_client_id
GOOGLE_CLIENT_SECRET=tu_google_client_secret

# Email (si usas envíos de email en la app)
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_HOST_USER=usuario@example.com
EMAIL_HOST_PASSWORD=secreto
EMAIL_USE_TLS=True

```

Nota: dependiendo de cómo el proyecto cargue variables, puede ser necesario exportarlas en el shell antes de ejecutar Django (por ejemplo `export SECRET_KEY=...`) o usar una librería que cargue `.env` automáticamente. Si el proyecto ya incluye manejo de `.env` revisá `manage.py` o `settings.py` para ver cómo se cargan.

### Autenticación OAuth2 (Google)

Este sistema utiliza OAuth2 (Google) para la validación de credenciales y el login de usuarios. Eso implica que, además de configurar las variables de entorno `GOOGLE_CLIENT_ID` y `GOOGLE_CLIENT_SECRET`, es imprescindible registrar correctamente las rutas de redirección (Authorized redirect URIs) en la consola de Google Cloud del proyecto de OAuth.

Puntos importantes:

- Las "Authorized redirect URIs" deben coincidir exactamente con la URL a la que Google enviará el código de autorización. En este proyecto la ruta de callback por defecto es `/accounts/google/callback/`.
- Si en producción el servidor va a escuchas en un puerto distinto al 80/443 (por ejemplo `https://mi-dominio:8443`), ese puerto debe aparecer en la URL registrada en Google Cloud. Google exige coincidencia exacta (incluido protocolo, dominio y puerto si aplica).
- En desarrollo es común registrar `http://localhost:8000/accounts/google/callback/`. Yo (el autor/validador) validé las URLs y el callback para `localhost:8000`. Quien despliegue en producción debe **añadir las URLs de producción** (ej. `https://mi-dominio/accounts/google/callback/`) en la configuración de credenciales de Google antes de usar el login con Google en producción.
- Si el despliegue se realiza detrás de un proxy (nginx) que sirve en HTTPS en el puerto 443 y proxy_pass hacia Gunicorn en otro puerto, la URL que debe registrarse en Google debe ser la pública (HTTPS) que el navegador usa. Es decir, registrar `https://mi-dominio/accounts/google/callback/` aunque internamente el tráfico vaya a `http://127.0.0.1:8000`.
- Para entornos con subdominios o múltiples ambientes (staging/production), registrar todas las URIs necesarias o crear credenciales separadas por ambiente.

Cómo configurarlo (pasos rápidos):

1. Ir a Google Cloud Console → APIs & Services → Credentials.
2. Crear un OAuth 2.0 Client ID (o editar uno existente).
3. En "Authorized redirect URIs" añadir la ruta completa, por ejemplo:

```
http://localhost:8000/accounts/google/callback/
https://mi-dominio/accounts/google/callback/
```

4. Copiar los valores `Client ID` y `Client secret` al `.env` (`GOOGLE_CLIENT_ID` y `GOOGLE_CLIENT_SECRET`).

Recomendaciones de seguridad:

- Usar siempre HTTPS en producción y registrar la URI con `https://...` en Google Cloud.
- No publicar `GOOGLE_CLIENT_SECRET` en repositorios ni compartirlo públicamente.
- Si cambiás el dominio o puerto de producción, actualizar las URIs en Google Cloud antes de poner en producción el flujo de login.

Si querés, puedo agregar un checklist y comandos detallados para crear las credenciales paso a paso con capturas de ejemplo.

### Base de datos

Por defecto el proyecto incluye `db.sqlite3` para desarrollo. Para producción usar PostgreSQL u otro motor relacional.


Ejemplo mínimo para PostgreSQL (instalación rápida en Debian):

```bash
sudo apt install -y postgresql postgresql-contrib libpq-dev
sudo -u postgres createuser --interactive  # crea usuario
sudo -u postgres createdb grcu_db
# luego configurar DATABASE_URL con el usuario/contraseña
```

### Migraciones y datos iniciales

```bash
python manage.py makemigrations
python manage.py migrate

# Cargar datos demo si existe un fixture o script (por ejemplo cargar_datos_demo.py)
python cargar_datos_demo.py

python manage.py collectstatic --noinput
```

Crear superusuario (sigue prompts):

```bash
python manage.py createsuperuser
```

---

## Ejecutar la aplicación en local

```bash
# Activar entorno
source .venv/bin/activate  # o en Windows: .\.venv\Scripts\Activate.ps1

python manage.py runserver

# Visitar:
http://127.0.0.1:8000/
http://127.0.0.1:8000/accounts/login/
```

Para entornos de producción, usá Gunicorn + nginx o la plataforma que prefieras (Render, Heroku, etc.).

### Ejemplo mínimo con Gunicorn

```bash
pip install gunicorn
gunicorn grcu_manager.wsgi:application --bind 0.0.0.0:8000
```

---

## Despliegue (notas rápidas)

- Recomendamos usar PostgreSQL en producción.
- Asegurar `DEBUG=False`, `SECRET_KEY` complejo, `ALLOWED_HOSTS` correctamente configurado y HTTPS (TLS).
- Configurar servidor web (nginx) como proxy inverso hacia Gunicorn/uvicorn.
- Asegurar archivos estáticos (`collectstatic`) y media (configurar `MEDIA_ROOT` y un bucket S3 si fuera necesario).
- En plataformas PaaS (Render, Heroku) configurá variables de entorno por el panel de la plataforma.

---

## Solución de problemas comunes

- Error: "OperationalError: unable to open database file" (SQLite)
  - Verificar permisos de escritura del archivo `db.sqlite3` y del directorio.

- Error durante `pip install` con compilación de paquetes:
  - Instalar headers/devel packages del sistema (`python3-dev`, `libjpeg-dev`, `zlib1g-dev`, etc.) según el error.

- La página de login aparece aunque estoy logueado:
  - Asegurate de haber desplegado la versión del código que redirige usuarios autenticados desde `/accounts/login/`. Reinicia la app y limpia la caché del navegador.

- Variables de entorno no aplicadas:
  - Verificar si el proyecto usa `python-dotenv` o `django-environ`. Si no, exportar variables con `export` (Linux/macOS) o establecer variables en Windows.

---

## Pruebas y verificación

- Tests unitarios (si el repo tiene):

```bash
pytest -q
```

- Prueba manual básica:
  1. Iniciar servidor: `python manage.py runserver`
  2. Crear superuser y loguear
  3. Intentar acceder a `/accounts/login/` estando logueado: deberías ser redirigido al dashboard

---

## Preguntas frecuentes (FAQ)

- ¿Puedo usar Conda en lugar de venv? Sí, mientras actives el entorno y uses la versión de Python compatible.
- ¿Debo usar SQLite en producción? No. SQLite es conveniente para desarrollo; para producción elegí PostgreSQL u otro servidor SQL.
- ¿Dónde configuro Google OAuth? En el archivo de variables de entorno (`GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`) y en la consola de Google Cloud configurá los redirect URIs (ej. `https://tu-dominio/accounts/google/callback/`).

---

## Apéndice: comandos útiles

- Activar venv (Linux/macOS): `source .venv/bin/activate`
- Activar venv (Windows PS): `.\.venv\Scripts\Activate.ps1`
- Migraciones: `python manage.py migrate`
- Crear superuser: `python manage.py createsuperuser`
- Ejecutar servidor: `python manage.py runserver`
- Instalar dependencias: `pip install -r requirements.txt`

---

Si querés, puedo:

- Añadir instrucciones específicas para PostgreSQL (creación de usuario, bases y ajuste en `DATABASES` en `settings.py`).
- Crear un `README-DEPLOYMENT.md` con un ejemplo completo de `systemd` + `nginx` + `gunicorn` para un VPS.
- Generar un archivo `.env.example` listo para commit (sin las claves reales).

Decime qué más querés incluir y lo agrego.
