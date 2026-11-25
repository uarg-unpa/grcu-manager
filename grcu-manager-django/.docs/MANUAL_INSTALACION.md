# Manual de Instalación

**Grupo 4Bytes** - Nicolás Butterfield, Abril Alvarez, Martina Gagna, Cristian Carranza

Universidad Nacional de la Patagonia Austral

© Grupo 4Bytes & Universidad Nacional de la Patagonia Austral. Todos los derechos reservados.

Última actualización: 19 de noviembre de 2026

Este manual explica, paso a paso, cómo instalar GRCU Manager en una computadora (Windows, Linux o macOS) y abrirlo en el navegador. No hace falta saber programar: alcanza con copiar los comandos tal como aparecen.

Este manual se probó completo en Windows 11 con Python 3.14. En Linux y macOS los pasos son equivalentes; las diferencias están indicadas donde corresponde.

## Contenido

1. Qué se necesita
2. Instalación
3. Configuración (archivo `.env`)
4. Primer ingreso
5. Datos de demostración (opcional)
6. Problemas frecuentes
7. Para uso avanzado (pruebas y panel de Django)
8. Ejemplo de instalación en un servidor Linux (producción)

## 1. Qué se necesita

- **Python 3.11 o superior.**
- **Git** (solo si el código se baja del repositorio; si se recibió en un archivo ZIP no hace falta).
- **El archivo `.env`** con las credenciales del proyecto. No está en el repositorio porque contiene claves: hay que pedírselo a los docentes o al responsable del proyecto. El ZIP de entrega ya lo trae incluido.
- **Una cuenta de Google real** (`@gmail.com` o `@uarg.unpa.edu.ar`). El sistema no tiene usuario y contraseña propios: solo se entra con Google.
- Conexión a internet.

**Cómo instalar lo que falte**

- *Windows:* Python desde python.org (en el instalador, marcar **"Add Python to PATH"**) y Git desde git-scm.com.
- *Linux:* abrir una terminal y ejecutar el comando de su distribución:
  - Fedora: `sudo dnf install -y git python3 python3-devel gcc`
  - Debian / Ubuntu: `sudo apt update && sudo apt install -y git python3 python3-venv python3-dev build-essential`
  - openSUSE: `sudo zypper install -y git python3 python3-virtualenv python3-devel gcc make`
- *macOS:* con Homebrew (brew.sh): `brew install git python@3.11`.

## 2. Instalación

Los comandos se escriben en una terminal: **PowerShell** en Windows; **Terminal** en Linux y macOS.

**Paso 1. Obtener el proyecto y entrar a su carpeta**

*Si se recibió el código en un archivo ZIP:* descomprimirlo y abrir la terminal dentro de la carpeta `grcu-manager-django` (la que contiene el archivo `manage.py`).

*Si se baja del repositorio:*

```
git clone https://github.com/uarg-unpa/grcu-manager.git
cd grcu-manager/grcu-manager-django
```

**Paso 2. Crear y activar un entorno virtual** (una "caja" que mantiene las librerías del proyecto separadas del resto de la computadora)

Windows (PowerShell):

```
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Si PowerShell bloquea el segundo comando, ejecutar una sola vez `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` y repetirlo.

Linux y macOS:

```
python3 -m venv .venv
source .venv/bin/activate
```

Cuando está activo, la línea de la terminal empieza con `(.venv)`.

**Paso 3. Instalar las librerías**

```
python -m pip install --upgrade pip wheel
pip install -r requirements.txt
```

Si en Linux o macOS aparece un error de compilación (por ejemplo con Pillow), leer el mensaje e instalar la librería de desarrollo que pida (`libjpeg`, `zlib`, etc.). En macOS, además, puede hacer falta `xcode-select --install`.

**Paso 4. Tener el archivo `.env`** en esta misma carpeta, al lado del archivo `manage.py`. Si el código llegó en el ZIP, el `.env` ya está incluido y no hay que hacer nada. Si se bajó del repositorio, hay que copiar el que entregaron los docentes. (Ver la sección 3.)

**Paso 5. Crear la base de datos**

```
python manage.py migrate
```

Esto crea el archivo `db.sqlite3` (la base de datos) y los cinco roles del sistema: Admin, Desarrollador, Líder, Stakeholder y Visitante.

**Paso 6. Iniciar el sistema**

```
python manage.py runserver
```

Dejar esa terminal abierta mientras se usa el sistema. Para apagarlo, presionar `Ctrl + C`. Para volver a iniciarlo otro día, activar el entorno (paso 2, segundo comando) y repetir el paso 6.

## 3. Configuración (archivo `.env`)

El archivo `.env` es un texto con las claves del sistema. Se obtiene de dos maneras:

- **Lo habitual:** usar el que viene en el ZIP de entrega o pedírselo a los docentes o al responsable del proyecto y copiarlo junto a `manage.py`. Ya trae todo cargado, incluidas las credenciales de Google con la dirección de retorno ya registrada.
- **Alternativa:** copiar la plantilla `.env.example` como `.env` y completarla con credenciales propias (ver más abajo).

Contenido mínimo:

```
SECRET_KEY=una-clave-larga-y-secreta
GOOGLE_CLIENT_ID=<client id>
GOOGLE_CLIENT_SECRET=<client secret>
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

`SECRET_KEY`, `GOOGLE_CLIENT_ID` y `GOOGLE_CLIENT_SECRET` son obligatorias; sin ellas el sistema no arranca. `DEBUG=True` se usa en desarrollo y debe ser `False` en producción.

**Importante:** el `.env` no se sube nunca a un repositorio ni se comparte públicamente (ya está excluido en `.gitignore`).

**Credenciales propias de Google (solo si no se tiene el `.env` de los docentes).** En Google Cloud Console → APIs y servicios → Credenciales, crear un "ID de cliente de OAuth 2.0" de tipo aplicación web y, en "URI de redireccionamiento autorizados", agregar exactamente:

```
http://localhost:8000/accounts/google/callback/
```

Copiar el ID y el secreto de cliente al `.env`.

## 4. Primer ingreso

1. Con el sistema iniciado, abrir en el navegador **http://localhost:8000/**. Usar siempre `localhost`; si se entra por `127.0.0.1`, Google rechaza el inicio de sesión (error `redirect_uri_mismatch`).
2. Como todavía no existe ningún administrador, el sistema muestra la pantalla de configuración inicial. Pulsar **"Autenticar con Google"** e iniciar sesión.
3. **La primera cuenta que inicia sesión queda como Administrador del sistema.** Por eso conviene entrar con la cuenta de Google que realmente vaya a administrarlo. Se aceptan solo cuentas `@gmail.com` y `@uarg.unpa.edu.ar`.
4. Google muestra la pantalla "Iniciar sesión en grcu-manager" con el nombre y el correo de la cuenta elegida: pulsar **"Continuar"**.
5. El sistema responde "¡Administrador Configurado!". Pulsar **"Ir al Panel de Administración"**: se abre el panel del Administrador, con el menú Inicio, Usuarios, Grupos, Proyectos y Auditoría.

Para cerrar la sesión, pulsar **"Salir"** (arriba a la derecha); el sistema vuelve a la pantalla de login.

A partir de ahí, **el resto de las personas solo puede entrar si el Administrador cargó antes su correo** en la sección "Usuarios". Si no, el sistema muestra "No estás registrado en el sistema".

## 5. Datos de demostración (opcional)

Para ver el sistema con información de ejemplo, con el entorno activo:

```
python cargar_datos_demo.py
```

Crea 30 usuarios, 4 grupos y 4 proyectos con requerimientos y casos de uso, y asigna el rol Líder a los líderes de cada proyecto. Se puede ejecutar más de una vez: lo que ya existe no se vuelve a cargar.

Los usuarios de demostración **no pueden iniciar sesión**: sus correos son `@unpa.edu.ar`, un dominio que el login no acepta. Para recorrer esos datos, entrar como Administrador (sección 4) y verlos desde los paneles de Usuarios, Grupos y Proyectos.

## 6. Problemas frecuentes

| Qué se ve | Qué hacer |
|---|---|
| Error `SECRET_KEY not found` o `GOOGLE_CLIENT_ID not found` | Falta el `.env` o no está junto a `manage.py`. |
| Google muestra `redirect_uri_mismatch` | Entrar por `http://localhost:8000/`, no por `127.0.0.1`. Si ya se usa `localhost`, la dirección de retorno no está registrada en las credenciales de Google (sección 3). |
| "No estás registrado en el sistema" | El Administrador tiene que cargar ese correo en "Usuarios". |
| "Solo se permiten emails de los dominios…" | Usar una cuenta `@gmail.com` o `@uarg.unpa.edu.ar`. |
| `Activate.ps1` bloqueado en PowerShell | Ver el paso 2 de la sección 2. |
| Error al ejecutar `pip install` | Instalar la librería de desarrollo que indique el mensaje (sección 2, paso 3). |
| Al ejecutar `manage.py` aparece el aviso `staticfiles.W004` (no existe la carpeta `static`) | Es solo un aviso: se puede ignorar, el sistema funciona igual. |
| `unable to open database file` | Revisar que la carpeta del proyecto permita escribir archivos. |
| Los comandos `python` o `pip` no se reconocen | Python no quedó en el PATH: reinstalarlo marcando "Add Python to PATH". |

## 7. Para uso avanzado

**Pruebas automáticas:** `pytest -q`. Todas las pruebas deben pasar.

**Panel de Django (`/admin/`):** requiere un superusuario (`python manage.py createsuperuser`). Es independiente del rol Administrador de GRCU Manager y no reemplaza el primer ingreso de la sección 4.

## 8. Ejemplo de instalación en un servidor Linux (producción)

Ejemplo para Ubuntu o Debian con PostgreSQL, Gunicorn y nginx. Los nombres (`grcu`, `mi-dominio.com`, rutas) se ajustan a cada servidor. Se ejecuta con un usuario que tenga `sudo`.

**Importante:** la carpeta `.venv` de otra computadora no se copia al servidor; se crea una nueva en el servidor (paso 3). Tampoco se suben `db.sqlite3` ni `staticfiles`.

**Paso 1. Instalar los programas**

```
sudo apt update
sudo apt install -y git python3 python3-venv python3-dev build-essential libpq-dev postgresql nginx
```

**Paso 2. Crear la base de datos** (cambiar la contraseña)

```
sudo -u postgres psql -c "CREATE USER grcu WITH PASSWORD 'cambiar-esta-clave';"
sudo -u postgres psql -c "CREATE DATABASE grcu_db OWNER grcu;"
```

**Paso 3. Descargar el proyecto e instalar las librerías**

```
sudo mkdir -p /opt/grcu && sudo chown $USER /opt/grcu
cd /opt/grcu
git clone https://github.com/uarg-unpa/grcu-manager.git
cd grcu-manager/grcu-manager-django
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip wheel
pip install -r requirements.txt
pip install gunicorn psycopg2-binary
```

**Paso 4. Configurar el `.env`.** Copiar al servidor el `.env` entregado por los docentes (por ejemplo con `scp`, no por Git) y ajustar estos valores:

```
DEBUG=False
SECRET_KEY=una-clave-larga-y-propia
ALLOWED_HOSTS=mi-dominio.com
DB_NAME=grcu_db
DB_USER=grcu
DB_PASSWORD=cambiar-esta-clave
DB_HOST=localhost
DB_PORT=5432
```

**Paso 5. Activar PostgreSQL.** Editar `grcu_manager/settings.py` (con `nano grcu_manager/settings.py`): comentar el bloque `DATABASES` de SQLite y descomentar el bloque "PostgreSQL configuration". No hace falta tocar nada más: con `DEBUG=False`, el archivo ya está preparado para funcionar detrás de nginx con HTTPS.

**Paso 6. Preparar la base y los archivos**

```
python manage.py migrate
python manage.py collectstatic --noinput
```

**Paso 7. Dejar la aplicación funcionando como servicio.** Crear el archivo `/etc/systemd/system/grcu.service` (`sudo nano /etc/systemd/system/grcu.service`) con este contenido, cambiando `TU_USUARIO` por el usuario del servidor:

```
[Unit]
Description=GRCU Manager
After=network.target postgresql.service

[Service]
User=TU_USUARIO
WorkingDirectory=/opt/grcu/grcu-manager/grcu-manager-django
ExecStart=/opt/grcu/grcu-manager/grcu-manager-django/.venv/bin/gunicorn grcu_manager.wsgi:application --bind 127.0.0.1:8000
Restart=always

[Install]
WantedBy=multi-user.target
```

Activarlo:

```
sudo systemctl daemon-reload
sudo systemctl enable --now grcu
```

**Paso 8. Configurar nginx.** Crear `/etc/nginx/sites-available/grcu` con este contenido:

```
server {
    listen 80;
    server_name mi-dominio.com;

    location /static/ {
        alias /opt/grcu/grcu-manager/grcu-manager-django/staticfiles/;
    }

    location /media/ {
        alias /opt/grcu/grcu-manager/grcu-manager-django/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Activarlo:

```
sudo ln -s /etc/nginx/sites-available/grcu /etc/nginx/sites-enabled/grcu
sudo nginx -t
sudo systemctl reload nginx
```

**Paso 9. Activar HTTPS** con un certificado gratuito de Let's Encrypt:

```
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d mi-dominio.com
```

**Paso 10. Registrar la dirección en Google.** En las credenciales de Google Cloud agregar la URI de retorno de producción (la misma que en la sección 3, con el dominio real):

```
https://mi-dominio.com/accounts/google/callback/
```

Después, abrir `https://mi-dominio.com/` y hacer el primer ingreso como en la sección 4.

**Para actualizar el sistema más adelante:**

```
cd /opt/grcu/grcu-manager/grcu-manager-django
git pull
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart grcu
```
