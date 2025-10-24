# 📋 INSTRUCCIONES PARA IMPORTAR EL ESQUEMA DE BASE DE DATOS

## Información del Proyecto
- **Universidad:** Universidad Nacional de la Patagonia Austral (UNPA)
- **Materia:** Laboratorio de Desarrollo de Software
- **Año:** 2025
- **Grupo:** 4Bytes
- **Proyecto:** GRCU Manager - Herramienta de Gestión de Requerimientos y Casos de Uso

## Integrantes
- Abril Alvarez
- Martina Gagna
- Cristian Carranza
- Nicolás Butterfield

---

## 🗄️ Archivo del Esquema

**Archivo:** `esquema_grcu_manager_presentacion.sql`

**Características:**
- ✅ Esquema completo de 29 tablas
- ✅ Definiciones de columnas, tipos de datos
- ✅ Primary Keys, Foreign Keys, Constraints
- ✅ Índices optimizados
- ✅ Documentación técnica completa
- ✅ Sin datos (schema-only)
- ✅ 100% ejecutable

**Estadísticas:**
- Líneas: 2,201
- Tamaño: 72 KB
- Tablas: 29
- Primary Keys: 29
- Foreign Keys: 41
- Índices: 65
- Constraints UNIQUE: 24

---

## 🚀 Cómo Importar el Esquema

### Requisitos Previos
- PostgreSQL 17.x instalado (o versión 12+)
- Acceso a una base de datos PostgreSQL

### Opción 1: Desde línea de comandos (psql)

```bash
# 1. Crear la base de datos (opcional)
createdb -U postgres grcu_db_test

# 2. Importar el esquema
psql -U postgres -d grcu_db_test -f esquema_grcu_manager_presentacion.sql

# 3. Verificar que se crearon las tablas
psql -U postgres -d grcu_db_test -c "\dt"
```

### Opción 2: Desde pgAdmin

1. **Crear base de datos:**
   - Click derecho en "Databases" → "Create" → "Database"
   - Nombre: `grcu_db_test`
   - Owner: tu usuario
   - Click "Save"

2. **Ejecutar el script:**
   - Click derecho en la base de datos → "Query Tool"
   - Menu: File → Open
   - Seleccionar: `esquema_grcu_manager_presentacion.sql`
   - Click en "Execute/Run" (⚡ o F5)

3. **Verificar:**
   - Expandir: Databases → grcu_db_test → Schemas → public → Tables
   - Deberías ver 29 tablas

### Opción 3: Desde DBeaver / DataGrip

1. **Crear conexión a PostgreSQL**
2. **Crear base de datos:**
   ```sql
   CREATE DATABASE grcu_db_test;
   ```
3. **Abrir SQL Console**
4. **Ejecutar el archivo:**
   - Menu: File → Open → Seleccionar `esquema_grcu_manager_presentacion.sql`
   - Click en "Execute Script" (Ctrl+Alt+X)

---

## 📊 Estructura de la Base de Datos

### Módulos Funcionales (8)

1. **AUTENTICACIÓN Y USUARIOS** (4 tablas)
   - `accounts_usuario` - Usuarios con OAuth2/tradicional
   - `accounts_usuario_groups` - Relación usuarios-grupos
   - `accounts_usuario_roles` - Relación usuarios-roles
   - `accounts_usuario_user_permissions` - Permisos por usuario

2. **AUDITORÍA** (1 tabla)
   - `auditoria_registroactividad` - Registro de todas las acciones

3. **CASOS DE USO** (4 tablas)
   - `casos_de_uso_casodeuso` - Casos de uso base
   - `casos_de_uso_detallecasodeusoagil` - Detalles metodología Ágil
   - `casos_de_uso_detallecasodeusotradicional` - Detalles metodología Tradicional
   - `casos_de_uso_historicalcasodeuso` - Historial de versiones

4. **GRUPOS** (2 tablas)
   - `grupos_grupo` - Grupos de trabajo
   - `grupos_grupo_integrantes` - Relación grupos-usuarios

5. **PERMISOS** (1 tabla)
   - `permisos_permiso` - Definición de permisos

6. **PROYECTOS** (3 tablas)
   - `proyectos_proyecto` - Proyectos del sistema
   - `proyectos_participacionproyecto` - Participación usuarios-proyectos
   - `proyectos_historicalproyecto` - Historial de versiones

7. **REQUERIMIENTOS** (5 tablas)
   - `requerimientos_requerimiento` - Requerimientos base
   - `requerimientos_detallerequerimientoagil` - Detalles metodología Ágil
   - `requerimientos_detallerequerimientotradicional` - Detalles metodología Tradicional
   - `requerimientos_requerimientocaso` - Relación requerimientos-casos
   - `requerimientos_historicalrequerimiento` - Historial de versiones

8. **ROLES** (2 tablas)
   - `roles_rol` - Roles del sistema
   - `roles_rol_permisos` - Relación roles-permisos

9. **DJANGO FRAMEWORK** (7 tablas)
   - Tablas estándar de Django para administración

---

## 🔍 Consultas de Verificación

Después de importar, puedes ejecutar estas consultas para verificar:

```sql
-- Ver todas las tablas
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
ORDER BY table_name;

-- Contar registros (debería ser 0)
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY tablename;

-- Ver las relaciones (Foreign Keys)
SELECT
    tc.table_name, 
    kcu.column_name, 
    ccu.table_name AS foreign_table_name,
    ccu.column_name AS foreign_column_name 
FROM information_schema.table_constraints AS tc 
JOIN information_schema.key_column_usage AS kcu
  ON tc.constraint_name = kcu.constraint_name
JOIN information_schema.constraint_column_usage AS ccu
  ON ccu.constraint_name = tc.constraint_name
WHERE tc.constraint_type = 'FOREIGN KEY' 
ORDER BY tc.table_name;
```

---

## ⚠️ Notas Importantes

### Sobre la Metodología
- **Cada proyecto debe elegir UNA metodología** al momento de su creación
- Opciones: **TRADICIONAL** o **ÁGIL** (mutuamente excluyente)
- **NO se permite uso híbrido** en un mismo proyecto
- La metodología define qué tablas de detalle se utilizan

### Sobre la Autenticación
- **Campo `password` en `accounts_usuario`:**
  - Requerido por Django (modelo AbstractUser)
  - Usado SOLO para superusuario del panel admin (`/admin/`)
  - Usuarios finales usan OAuth2 (Google) sin contraseña
  - Los usuarios OAuth2 tienen hash inválido en este campo

### Sobre el Versionamiento
- Tablas con prefijo `historical*` usan `django-simple-history`
- Capturan todos los cambios automáticamente
- Incluyen: usuario, fecha, tipo de cambio, motivo

---

## 📞 Contacto

Para consultas sobre el esquema o el proyecto:

**Grupo 4Bytes - UNPA 2025**
- Materia: Laboratorio de Desarrollo de Software
- Docentes: [Completar con nombres de profesores]

---

## 📄 Licencia

Este esquema es parte del proyecto académico GRCU Manager desarrollado para la 
Universidad Nacional de la Patagonia Austral.
