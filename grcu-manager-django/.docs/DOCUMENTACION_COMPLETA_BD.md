# 📊 Documentación Completa de la Base de Datos - GRCU Manager

**Última actualización:** 23 de octubre de 2025  
**Versión Django:** 5.2.6  
**Base de Datos:** PostgreSQL  
**Total de Tablas:** 29

---

## 📖 Índice

1. [Estructura General](#estructura-general)
2. [Grupo 1: Autenticación y Permisos](#grupo-1-autenticación-y-permisos)
3. [Grupo 2: Organización](#grupo-2-organización)
4. [Grupo 3: Requerimientos](#grupo-3-requerimientos)
5. [Grupo 4: Casos de Uso](#grupo-4-casos-de-uso)
6. [Grupo 5: Auditoría](#grupo-5-auditoría)
7. [Grupo 6: Sistema Django](#grupo-6-sistema-django)
8. [Relaciones Principales](#relaciones-principales)
9. [Características Clave](#características-clave)

---

## 🏗️ Estructura General

El sistema GRCU Manager gestiona requerimientos y casos de uso con soporte para **metodologías tradicionales y ágiles**. La base de datos se organiza en **6 grupos funcionales** con **29 tablas** interconectadas.

### **Resumen por Grupo:**
- 🔐 **Autenticación y Permisos:** 3 tablas principales + 5 de Django
- 🏢 **Organización:** 4 tablas (grupos, proyectos, participación)
- 📋 **Requerimientos:** 5 tablas (base + detalles + historial)
- 🎯 **Casos de Uso:** 4 tablas (base + detalles + historial)
- 📊 **Auditoría:** 1 tabla (registro completo)
- ⚙️ **Sistema Django:** 7 tablas (sesiones, migraciones, admin)

---

## 🔐 Grupo 1: Autenticación y Permisos

### **1.1 `accounts_usuario`** (Usuario Principal)

**Propósito:** Usuario del sistema, extiende `AbstractUser` de Django

**Autenticación:**
- **Primaria:** Google OAuth2 (vía `allauth`)
- **Secundaria:** Password (para admin/superusers)

**Campos Clave:**
```sql
id                BIGSERIAL PRIMARY KEY
email             VARCHAR(254) UNIQUE NOT NULL  -- Login principal
password          VARCHAR(128)                   -- Hash (bcrypt/argon2)
nombre            VARCHAR(255)                   -- Nombre completo
avatar            VARCHAR(200)                   -- URL de Google OAuth2
is_superuser      BOOLEAN DEFAULT FALSE
is_staff          BOOLEAN DEFAULT FALSE
is_active         BOOLEAN DEFAULT TRUE
date_joined       TIMESTAMP DEFAULT NOW()
last_login        TIMESTAMP NULL
```

**Índices:**
- `email` (UNIQUE INDEX) - Login rápido
- `nombre` (INDEX) - Búsquedas por nombre

**Relaciones:**
- → `grupos_grupo` (creador, líder)
- → `proyectos_proyecto` (creador, líder)
- → `requerimientos_requerimiento` (creador)
- → `casos_de_uso_casodeuso` (creador)
- → `auditoria_registroactividad` (actor)
- ↔ `roles_rol` (M2M via `accounts_usuario_roles`)
- ↔ `auth_group` (M2M via `accounts_usuario_groups`)

**Flujo OAuth2:**
```
Usuario → Google Login → Callback → 
  idinfo.get("email") → usuario.email
  idinfo.get("name") → usuario.nombre  
  idinfo.get("picture") → usuario.avatar (URL)
```

---

### **1.2 `roles_rol`** (Roles del Sistema)

**Propósito:** Define roles de usuario en proyectos (Líder, Analista, Desarrollador, etc.)

**Campos:**
```sql
id          BIGSERIAL PRIMARY KEY
nombre      VARCHAR(50) UNIQUE NOT NULL
color       VARCHAR(7) DEFAULT '#444c8a'  -- Hex color para UI
icono_url   VARCHAR(200) NULL              -- Ícono del rol
```

**Uso:**
- Asignación de roles **por proyecto** via `proyectos_participacionproyecto`
- Asignación de roles **globales** via `accounts_usuario_roles`
- Control de permisos via `roles_rol_permisos`

**Ejemplos de Roles:**
- `Líder de Proyecto`
- `Analista de Requerimientos`
- `Desarrollador`
- `Tester`
- `Stakeholder`

---

### **1.3 `permisos_permiso`** (Permisos Granulares)

**Propósito:** Permisos específicos del sistema (custom, no Django)

**Campos:**
```sql
id      BIGSERIAL PRIMARY KEY
nombre  VARCHAR(100) UNIQUE NOT NULL
```

**Ejemplos de Permisos:**
- `crear_proyecto`
- `editar_requerimiento`
- `eliminar_caso_uso`
- `ver_dashboard_admin`
- `exportar_matriz_trazabilidad`

**Asignación:** Se asignan a roles via `roles_rol_permisos` (M2M)

---

### **1.4 Tablas M2M:**

#### **`accounts_usuario_roles`**
Asigna roles globales a usuarios (fuera del contexto de proyecto)

```sql
id          BIGSERIAL PRIMARY KEY
usuario_id  BIGINT FK → accounts_usuario
rol_id      BIGINT FK → roles_rol
```

---

## 🏢 Grupo 2: Organización

### **2.1 `grupos_grupo`** (Grupos/Departamentos)

**Propósito:** Organización o departamento que agrupa proyectos

**Campos:**
```sql
id              BIGSERIAL PRIMARY KEY
nombre          VARCHAR(255) UNIQUE NOT NULL
logo            VARCHAR(100) NULL               -- ImageField: media/grupos/logos/
fecha_creacion  TIMESTAMP DEFAULT NOW()
activo          BOOLEAN DEFAULT TRUE            -- Soft delete
creado_por_id   BIGINT FK → accounts_usuario (SET_NULL)
lider_id        BIGINT FK → accounts_usuario (SET_NULL)
```

**Soft Delete:** 
- Usar `activo=False` en lugar de `DELETE`
- Preserva historial y relaciones

**Relaciones:**
- ← `proyectos_proyecto` (grupo contiene proyectos)
- ↔ `accounts_usuario` (M2M via `grupos_grupo_integrantes`)

---

### **2.2 `grupos_grupo_integrantes`** (M2M)

**Propósito:** Usuarios miembros de un grupo

```sql
id          BIGSERIAL PRIMARY KEY
grupo_id    BIGINT FK → grupos_grupo
usuario_id  BIGINT FK → accounts_usuario
```

---

### **2.3 `proyectos_proyecto`** (Proyectos)

**Propósito:** Proyecto de desarrollo (sistema/aplicación a construir)

**Campos:**
```sql
id              BIGSERIAL PRIMARY KEY
nombre          VARCHAR(200) UNIQUE NOT NULL
descripcion     TEXT NULL
metodologia     VARCHAR(20) NULL                 -- CHOICES: TRADICIONAL/AGIL
fecha_creacion  TIMESTAMP DEFAULT NOW()
activo          BOOLEAN DEFAULT TRUE             -- Soft delete
logo            VARCHAR(100) NULL                -- ImageField: media/proyectos/logos/
grupo_id        BIGINT FK → grupos_grupo (SET_NULL)
lider_id        BIGINT FK → accounts_usuario (SET_NULL)
creado_por_id   BIGINT FK → accounts_usuario (SET_NULL)
```

**Metodologías:**
- `TRADICIONAL`: Usa `DetalleRequerimientoTradicional` y `DetalleCasoDeUsoTradicional`
- `AGIL`: Usa `DetalleRequerimientoAgil` y `DetalleCasoDeUsoAgil`
- `NULL`: Mixto o sin definir

**Relaciones:**
- ← `requerimientos_requerimiento` (proyecto contiene requerimientos)
- ← `casos_de_uso_casodeuso` (proyecto contiene casos de uso)
- ← `proyectos_participacionproyecto` (asignación de usuarios con roles)
- ← `proyectos_historicalproyecto` (historial de versiones)

---

### **2.4 `proyectos_participacionproyecto`** (Participación)

**Propósito:** Asigna usuarios a proyectos con un rol específico

**Campos:**
```sql
id                BIGSERIAL PRIMARY KEY
usuario_id        BIGINT FK → accounts_usuario (CASCADE)
proyecto_id       BIGINT FK → proyectos_proyecto (CASCADE)
rol_id            BIGINT FK → roles_rol (PROTECT)
fecha_asignacion  TIMESTAMP DEFAULT NOW()
```

**Constraint:** `UNIQUE(usuario_id, proyecto_id)`  
→ Un usuario no puede estar duplicado en el mismo proyecto

**on_delete:**
- `CASCADE`: Si se borra usuario/proyecto, se borra la participación
- `PROTECT`: No se puede borrar un rol si está en uso

---

### **2.5 `proyectos_historicalproyecto`** (Historial)

**Propósito:** Versiones históricas del proyecto (django-simple-history)

**Campos Adicionales:**
```sql
history_id        BIGSERIAL PRIMARY KEY
history_type      VARCHAR(1)                     -- '+' create, '~' update, '-' delete
history_date      TIMESTAMP DEFAULT NOW()
history_user_id   BIGINT FK → accounts_usuario NULL
```

**Uso:**
- Ver quién modificó qué y cuándo
- Recuperar versiones anteriores
- Auditoría de cambios

---

## 📋 Grupo 3: Requerimientos

### **3.1 `requerimientos_requerimiento`** (Requerimiento Base)

**Propósito:** Requerimiento funcional o no funcional del sistema

**Campos:**
```sql
id                      BIGSERIAL PRIMARY KEY
nombre                  VARCHAR(255) NOT NULL
descripcion             TEXT
tipo                    VARCHAR(20) NOT NULL         -- FUNCIONAL/NO_FUNCIONAL
estado                  VARCHAR(20) DEFAULT 'PENDIENTE'
proyecto_id             BIGINT FK → proyectos_proyecto (CASCADE)
creado_por_id           BIGINT FK → accounts_usuario (SET_NULL)
fecha_creacion          TIMESTAMP DEFAULT NOW()
fecha_actualizacion     TIMESTAMP DEFAULT NOW()
imagen                  VARCHAR(100) NULL            -- ImageField: media/requerimientos/imagenes/
link_externo            VARCHAR(500)                 -- URL a Jira, Trello, etc.
detalle_tradicional_id  BIGINT FK → detallerequerimientotradicional (SET_NULL) OneToOne
detalle_agil_id         BIGINT FK → detallerequerimientoagil (SET_NULL) OneToOne
```

**Estados Posibles:**
- `PENDIENTE`
- `EN_PROGRESO`
- `COMPLETADO`
- `CANCELADO`
- `BLOQUEADO`

**Flexibilidad Metodológica:**
- Puede tener detalle tradicional, ágil, ambos o ninguno
- Permite transición entre metodologías

**Relaciones:**
- ↔ `casos_de_uso_casodeuso` (M2M via `requerimientos_requerimientocaso`)
- → `requerimientos_historicalrequerimiento` (historial)

---

### **3.2 `requerimientos_detallerequerimientotradicional`**

**Propósito:** Campos adicionales para metodología tradicional

**Campos:**
```sql
id                     BIGSERIAL PRIMARY KEY
requerimiento_padre_id BIGINT FK → requerimientos_requerimiento (CASCADE) UNIQUE
prioridad              VARCHAR(50)                  -- Alta, Media, Baja
fuente                 VARCHAR(255)                 -- Cliente, Stakeholder, etc.
categoria              VARCHAR(100)                 -- Seguridad, Performance, etc.
fecha_compromiso       DATE NULL
estado_validacion      VARCHAR(100)                 -- Validado, Pendiente, Rechazado
observaciones          TEXT
```

**OneToOne Reverse:** `requerimiento.detalle_tradicional_reverse`

---

### **3.3 `requerimientos_detallerequerimientoagil`**

**Propósito:** Campos adicionales para metodología ágil (Scrum)

**Campos:**
```sql
id                     BIGSERIAL PRIMARY KEY
requerimiento_padre_id BIGINT FK → requerimientos_requerimiento (CASCADE) UNIQUE
historia_usuario       TEXT                         -- User Story
criterio_aceptacion    TEXT                         -- Acceptance Criteria
puntos_estimados       INTEGER POSITIVE NULL         -- Story Points
sprint_asignado        VARCHAR(100)                 -- Sprint 1, Sprint 2, etc.
responsable            VARCHAR(100)                 -- Product Owner, Dev Team
estado_scrum           VARCHAR(100)                 -- Backlog, In Progress, Done
observaciones          TEXT
```

**OneToOne Reverse:** `requerimiento.detalle_agil_reverse`

---

### **3.4 `requerimientos_requerimientocaso`** (Trazabilidad)

**Propósito:** Vincula requerimientos con casos de uso (tabla intermedia M2M)

**Campos:**
```sql
id                BIGSERIAL PRIMARY KEY
requerimiento_id  BIGINT FK → requerimientos_requerimiento (CASCADE)
caso_de_uso_id    BIGINT FK → casos_de_uso_casodeuso (CASCADE)
fecha_vinculacion TIMESTAMP DEFAULT NOW()
nota              VARCHAR(255)                     -- Contexto de la relación
```

**Constraint:** `UNIQUE(requerimiento_id, caso_de_uso_id)`  
→ Evita duplicados

**Uso:**
- Matriz de trazabilidad
- Detectar requerimientos/casos huérfanos
- Análisis de cobertura

---

### **3.5 `requerimientos_historicalrequerimiento`**

**Propósito:** Historial de versiones de requerimientos

**Campos:** Igual que `requerimientos_requerimiento` + campos history

---

## 🎯 Grupo 4: Casos de Uso

### **4.1 `casos_de_uso_casodeuso`** (Caso de Uso Base)

**Propósito:** Casos de uso del sistema (interacciones usuario-sistema)

**Campos:**
```sql
id                      BIGSERIAL PRIMARY KEY
nombre                  VARCHAR(255) NOT NULL
descripcion             TEXT
proyecto_id             BIGINT FK → proyectos_proyecto (CASCADE)
creado_por_id           BIGINT FK → accounts_usuario (SET_NULL)
fecha_creacion          TIMESTAMP DEFAULT NOW()
fecha_actualizacion     TIMESTAMP DEFAULT NOW()
imagen                  VARCHAR(100) NULL            -- ImageField: media/casos_de_uso/imagenes/
link_externo            VARCHAR(500)
detalle_tradicional_id  BIGINT FK → detallecasodeusotradicional (SET_NULL) OneToOne
detalle_agil_id         BIGINT FK → detallecasodeusoagil (SET_NULL) OneToOne
```

**Estructura:** Análoga a `requerimientos_requerimiento`

---

### **4.2 `casos_de_uso_detallecasodeusotradicional`**

**Propósito:** Detalles tradicionales del caso de uso

**Campos:**
```sql
id                     BIGSERIAL PRIMARY KEY
caso_de_uso_padre_id   BIGINT FK → casos_de_uso_casodeuso (CASCADE) UNIQUE
actor_principal        VARCHAR(255)                 -- Usuario, Administrador, etc.
precondiciones         TEXT                         -- Condiciones iniciales
flujo_principal        TEXT                         -- Flujo normal
flujo_alternativo      TEXT                         -- Excepciones
postcondiciones        TEXT                         -- Resultado final
observaciones          TEXT
```

---

### **4.3 `casos_de_uso_detallecasodeusoagil`**

**Propósito:** Detalles ágiles del caso de uso

**Campos:**
```sql
id                     BIGSERIAL PRIMARY KEY
caso_de_uso_padre_id   BIGINT FK → casos_de_uso_casodeuso (CASCADE) UNIQUE
historia_usuario       TEXT
criterio_aceptacion    TEXT
responsable            VARCHAR(100)
estado_scrum           VARCHAR(100)
observaciones          TEXT
```

---

### **4.4 `casos_de_uso_historicalcasodeuso`**

**Propósito:** Historial de versiones de casos de uso

---

## 📊 Grupo 5: Auditoría

### **5.1 `auditoria_registroactividad`** (Auditoría Completa)

**Propósito:** Log de todas las acciones del sistema

**Campos:**
```sql
id           BIGSERIAL PRIMARY KEY
usuario_id   BIGINT FK → accounts_usuario (SET_NULL)
accion       VARCHAR(20) NOT NULL                -- CHOICES (ver abajo)
descripcion  TEXT                                -- Texto descriptivo
detalles     JSON NULL                           -- Metadata adicional
ip_address   INET NULL                           -- IP del usuario
user_agent   TEXT                                -- Navegador/dispositivo
fecha        TIMESTAMP DEFAULT NOW()
```

**Acciones Disponibles:**
- `LOGIN` / `LOGOUT`
- `CREATE` / `UPDATE` / `DELETE`
- `EXPORT`
- `ASSIGN_ROL`
- `CHANGE_STATUS`
- etc.

**Índices Optimizados:**
- `fecha DESC` - Queries por fecha
- `(usuario_id, fecha) DESC` - Actividad por usuario
- `accion` - Filtros por tipo

**Ejemplo de uso:**
```python
RegistroActividad.objects.create(
    usuario=request.user,
    accion='CREATE',
    descripcion=f'Creó requerimiento: {req.nombre}',
    detalles={'requerimiento_id': req.id, 'tipo': req.tipo},
    ip_address=get_client_ip(request),
    user_agent=request.META.get('HTTP_USER_AGENT')
)
```

---

## ⚙️ Grupo 6: Sistema Django

### **6.1 `auth_group`** (Grupos Django)
Sistema nativo de permisos de Django (usado principalmente para admin panel)

### **6.2 `auth_permission`** (Permisos Django)
Permisos generados automáticamente por Django para cada modelo

### **6.3 `auth_group_permissions`** (M2M)
Relación entre grupos y permisos Django

### **6.4 `accounts_usuario_groups`** (M2M)
Asigna grupos Django a usuarios

### **6.5 `accounts_usuario_user_permissions`** (M2M)
Permisos directos a usuarios (sin pasar por grupos)

### **6.6 `django_content_type`**
Metadatos de modelos Django (para permisos y admin)

### **6.7 `django_admin_log`**
Log de acciones en el panel de administración de Django

```sql
id              BIGSERIAL PRIMARY KEY
action_time     TIMESTAMP DEFAULT NOW()
user_id         BIGINT FK → accounts_usuario
content_type_id BIGINT FK → django_content_type (SET_NULL)
object_id       TEXT NULL
object_repr     VARCHAR(200)
action_flag     SMALLINT                         -- 1=add, 2=change, 3=delete
change_message  TEXT
```

### **6.8 `django_session`**
Sesiones de usuario

```sql
session_key   VARCHAR(40) PRIMARY KEY
session_data  TEXT
expire_date   TIMESTAMP                         -- INDEX
```

**⚠️ Sin relaciones FK:** Las sesiones NO tienen ForeignKey a usuarios porque:
- Django guarda sesiones **antes** de la autenticación
- La relación usuario-sesión está **dentro** del campo `session_data` (serializado)
- No hay FK en la estructura de la tabla

### **6.9 `django_migrations`**
Historial de migraciones aplicadas

```sql
id       BIGSERIAL PRIMARY KEY
app      VARCHAR(255)           -- Nombre de la app
name     VARCHAR(255)           -- Nombre de la migración
applied  TIMESTAMP              -- Cuándo se aplicó
```

**⚠️ Sin relaciones FK:** Tabla de control standalone que registra qué migraciones se han aplicado. No necesita relaciones con otras tablas del sistema.

---

## 🔗 Relaciones Principales

### **Flujo Completo:**

```
Usuario (accounts_usuario)
  ↓
  ├─ Crea Grupo (grupos_grupo)
  │    ↓
  │    └─ Grupo contiene Proyectos (proyectos_proyecto)
  │
  └─ Participa en Proyecto con Rol (proyectos_participacionproyecto)
       ↓
       ├─ Proyecto tiene Requerimientos (requerimientos_requerimiento)
       │    ↓
       │    ├─ Detalle Tradicional (detallerequerimientotradicional)
       │    ├─ Detalle Ágil (detallerequerimientoagil)
       │    └─ Vinculado a Casos de Uso (requerimientos_requerimientocaso)
       │
       └─ Proyecto tiene Casos de Uso (casos_de_uso_casodeuso)
            ↓
            ├─ Detalle Tradicional (detallecasodeusotradicional)
            └─ Detalle Ágil (detallecasodeusoagil)

Toda actividad → auditoria_registroactividad
Todo cambio → *_historical* (django-simple-history)
```

---

## 💡 Características Clave del Diseño

### **1. Flexibilidad Metodológica**
✅ Soporta metodología tradicional, ágil o mixta  
✅ Transición sin pérdida de datos  
✅ Detalles opcionales (OneToOne nullable)

### **2. Auditoría Completa**
✅ Historial automático con `django-simple-history`  
✅ Log de actividades con `auditoria_registroactividad`  
✅ Timestamps en todas las entidades

### **3. Soft Deletes**
✅ Grupos y proyectos usan `activo=False`  
✅ Preserva historial y relaciones  
✅ Recuperación posible

### **4. Trazabilidad**
✅ Múltiples formas de relacionar requerimientos con casos de uso  
✅ Detección de huérfanos  
✅ Matriz de trazabilidad

### **5. Seguridad Granular**
✅ Sistema dual de permisos (Django + Custom)  
✅ Permisos por rol  
✅ Roles por proyecto

### **6. Multimedia**
✅ Imágenes en requerimientos y casos de uso  
✅ Links externos a herramientas (Jira, Trello)  
✅ Logos en grupos y proyectos

### **7. on_delete Inteligente**
✅ `CASCADE`: Dependencias fuertes (proyecto → requerimientos)  
✅ `SET_NULL`: Referencias opcionales (creador, líder)  
✅ `PROTECT`: Datos críticos (roles en uso)

---

## 🚀 Optimizaciones

### **Índices Clave:**
- `accounts_usuario.email` (UNIQUE, INDEX) - Login
- `accounts_usuario.nombre` (INDEX) - Búsquedas
- `auditoria_registroactividad.fecha` (INDEX) - Queries temporales
- `django_session.expire_date` (INDEX) - Limpieza de sesiones

### **Constraints:**
- `UNIQUE(usuario_id, proyecto_id)` en `proyectos_participacionproyecto`
- `UNIQUE(requerimiento_id, caso_de_uso_id)` en `requerimientos_requerimientocaso`
- `UNIQUE` en emails, nombres de roles, permisos

---

## 📚 Archivos Relacionados

- **Diagrama Mermaid:** `.docs/diagrama_bd_mermaid.txt`
- **Migración Limpieza:** `.docs/MIGRACION_LIMPIEZA_BD.md`
- **Casos de Prueba:** `.docs/casos_prueba_funcionalidades.txt`

---

**Documentación generada por:** GitHub Copilot  
**Mantenida por:** Equipo GRCU Manager
