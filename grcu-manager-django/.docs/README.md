<p align="center">
  <img src="img/unpa_logo.png" alt="Logo UNPA" width="120"/>
</p>

# 📌 GRCU Manager – Gestor de Requerimientos y Casos de Uso  

📊 **Sistema académico desarrollado para la materia _Laboratorio de Desarrollo de Software_ (UNPA)**  
👥 **Team:**

<p align="center">
  <img src="img/4bytes_logo.png" alt="Logo UNPA" width="240"/>
</p>

---

## 📖 Descripción  

**GRCU Manager** es una aplicación web construida con **Django 5.2.6** que permite gestionar de forma ordenada los **requerimientos** y **casos de uso** de un proyecto de software.  

Su propósito principal es ofrecer a equipos de desarrollo una herramienta práctica para documentar, organizar y priorizar la información clave durante la etapa de análisis, manteniendo un historial de cambios y una **matriz de trazabilidad** completa. El sistema soporta tanto metodologías tradicionales como ágiles, proporcionando herramientas especializadas para cada enfoque.

El proyecto incluye dashboards interactivos con métricas detalladas, sistema de autenticación basado en email, roles diferenciados (Administrador, Líder, Desarrollador, Stakeholder, Visitante), y funcionalidades avanzadas como validación de requerimientos, comentarios en hilos, y exportación de reportes en múltiples formatos.  

---

## ✨ Funcionalidades principales  

- ✅ **Sistema de Autenticación**: Autenticación basada en email con roles diferenciados (Administrador, Líder, Desarrollador, Stakeholder, Visitante)
- ✅ **Dashboards Interactivos**: 
  - Dashboard del Líder con métricas completas (requerimientos totales, casos de uso, huérfanos, sin validar, completados, sin completar)
  - Dashboard del Desarrollador personalizado por proyectos asignados
- ✅ Registrar y administrar requerimientos y casos de uso de software
- ✅ Asignar prioridades con la técnica **MoSCoW** (_Must, Should, Could, Won't_)
- ✅ Mantener historial de cambios y versiones en cada requerimiento
- ✅ Definir dependencias entre requerimientos
- ✅ Agrupar requerimientos mediante categorías o etiquetas
- ✅ Generar una **matriz de trazabilidad** que vincule requerimientos con casos de uso
- ✅ Validación de requerimientos por líderes y stakeholders
- ✅ Añadir comentarios y discusiones en hilos
- ✅ Adjuntar documentos o enlaces externos
- ✅ Reportes y estadísticas con gráficos de distribución
- ✅ Exportación de datos en CSV, Excel y PDF
- ✅ Panel de administración completo con auditoría de actividades
- ✅ Inspirado en funcionalidades de herramientas profesionales (con un enfoque académico)

---

## 🖥 Capturas de pantalla  

> *Dashboard inicial de Administración*  

<p align="center">
  <img src="img/captura_1.png" width="600" alt="Captura 1"/>
</p>  

> *Pantalla de administración de usuarios y Roles*

<p align="center">
  <img src="img/captura_2.png" width="600" alt="Captura 2"/>
</p>  

---

## 🚀 Instalación  

### Prerrequisitos
- Python 3.13.9
- PostgreSQL
- Git

### Pasos de Instalación

1. **Clonar el repositorio**:  
   ```bash
   git clone https://github.com/uarg-unpa/grcu-manager.git
   cd grcu-manager
   ```

2. **Crear entorno virtual**:  
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instalar dependencias**:  
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar base de datos**:  
   - Crear una base de datos PostgreSQL
   - Configurar las credenciales en `grcu_manager/settings.py`

5. **Aplicar migraciones**:  
   ```bash
   python manage.py migrate
   ```

6. **Crear superusuario**:  
   ```bash
   python manage.py createsuperuser
   ```

7. **Ejecutar servidor**:  
   ```bash
   python manage.py runserver
   ```

8. **Acceder en el navegador**:  
   ```
   http://localhost:8000
   ```

---

## 🛠 Tecnologías  

- **Backend**: Django 5.2.6 (Python 3.13.9)
- **Base de Datos**: PostgreSQL
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript
- **Gráficos**: Chart.js
- **Autenticación**: Sistema personalizado con email
- **ORM**: Django ORM con relaciones complejas
- **Historial**: Django Simple History
- **Control de versiones**: Git + GitHub  

---

## 🎯 Uso  

### Para Administradores
- Gestionar usuarios, roles y permisos
- Configurar proyectos y equipos
- Monitorear auditoría de actividades
- Realizar limpieza y reseteo de base de datos

### Para Líderes de Proyecto
- Acceder al dashboard con métricas completas
- Gestionar integrantes del proyecto
- Asignar metodología (tradicional o ágil)
- Validar requerimientos pendientes
- Monitorear progreso y generar reportes

### Para Desarrolladores
- Ver proyectos asignados en dashboard personalizado
- Crear y gestionar requerimientos
- Desarrollar casos de uso
- Participar en validaciones y discusiones

### Para Stakeholders
- Validar requerimientos asignados
- Participar en discusiones y comentarios
- Revisar progreso del proyecto

### Funcionalidades Generales
- Ingresar al panel de administración
- Crear, editar y eliminar requerimientos y casos de uso
- Asignar prioridades y categorías con MoSCoW
- Visualizar la **matriz de trazabilidad**
- Comentar, adjuntar documentos y enlaces
- Exportar reportes en CSV, Excel y PDF  

---

## 🛣 Roadmap  

### ✅ Implementado
- 🔐 Sistema de autenticación con roles (Administrador, Líder, Desarrollador, Stakeholder, Visitante)
- � Dashboards interactivos con métricas detalladas y gráficos
- 🕒 Historial completo de cambios en requerimientos
- � Exportación de matriz de trazabilidad en CSV, Excel y PDF
- 🎨 Interfaz mejorada con Bootstrap 5 y Chart.js
- ✅ Validación de requerimientos por roles
- 💬 Sistema de comentarios y discusiones en hilos
- 📋 Soporte para metodologías tradicionales y ágiles

### 🔄 En Desarrollo / Pendiente
- 📱 Mejoras en la experiencia móvil
- 🔍 Búsqueda avanzada y filtros
- 📧 Notificaciones por email
- 🔄 Integración con herramientas externas (Jira, GitHub)
- 📊 Análisis predictivo de requerimientos  

## 📁 Estructura del Proyecto

```
grcu-manager/
├── accounts/              # Gestión de usuarios y autenticación
├── casos_de_uso/          # Módulo de casos de uso
├── core/                  # Configuraciones core y utilidades
├── dashboards/            # Dashboards para líderes y desarrolladores
├── grupos/                # Gestión de grupos
├── permisos/              # Sistema de permisos
├── proyectos/             # Gestión de proyectos
├── requerimientos/        # Gestión de requerimientos
├── roles/                 # Definición de roles
├── static/                # Archivos estáticos (CSS, JS, imágenes)
├── templates/             # Plantillas HTML
├── media/                 # Archivos multimedia subidos
├── grcu_manager/          # Configuración principal de Django
├── conftest.py            # Configuración de pruebas
├── manage.py              # Script de gestión de Django
├── pytest.ini             # Configuración de pytest
├── requirements.txt       # Dependencias del proyecto
└── README.md
```

---

## 🔧 Configuración Adicional

### Variables de Entorno
Crear un archivo `.env` en la raíz del proyecto:

```env
DEBUG=True
SECRET_KEY=tu_clave_secreta_aqui
DATABASE_URL=postgresql://usuario:password@localhost:5432/grcu_manager
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu_email@gmail.com
EMAIL_HOST_PASSWORD=tu_password
```

### Base de Datos
El sistema utiliza PostgreSQL con:
- Relaciones complejas (muchos-a-muchos)
- Historial de versiones con django-simple-history
- Índices optimizados para consultas frecuentes
- Triggers para auditoría automática

---

## 🖼️ Diagramas del Sistema

### Diagrama de Entidad-Relación
![Diagrama Entidad-Relación](diagrama_entidad_relacion.png)

### Diagrama de Base de Datos
![Diagrama Base de Datos](grcu_db%20_DER.png)  

1. Forkear el repositorio.  
2. Crear tu rama: `git checkout -b feature/nueva-funcionalidad`.  
3. Hacer commit: `git commit -m "Añadir nueva funcionalidad"`.  
4. Push a la rama: `git push origin feature/nueva-funcionalidad`.  
5. Abrir un Pull Request.  

---

## 👩‍💻 Equipo  

| ![Martina](img/martina.png) | ![Abril](img/abril.png) | ![Nico](img/nico.png) | ![Cristian](img/cristian.png) |
|:------------------------------:|:--------------------------:|:------------------------:|:--------------------------------:|
| **Martina Gagna**              | **Abril Alvarez**          | **Nicolás Butterfield**  | **Cristian Carranza**            |

**Dev Team:**

<p align="center">
  <img src="img/4bytes_logo.png" alt="Logo UNPA" width="150"/>
</p>

---

## 📄 Licencia  

Este proyecto está bajo la licencia **MIT**.  

---

## 🔗 Links útiles  
 
- 💻 [Repositorio en GitHub](https://github.com/uarg-unpa/grcu-manager)  
