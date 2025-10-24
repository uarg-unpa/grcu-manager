# Prompt para Generar Diagrama de Base de Datos - Sistema GRCU Manager

## Información del Proyecto
**Nombre:** GRCU Manager  
**Tipo:** Sistema de Gestión de Proyectos  
**Framework:** Django 5.2.6  
**Base de Datos:** PostgreSQL  
**Arquitectura:** MVC con aplicaciones modulares  

## Estructura de la Base de Datos

### Tablas Principales y sus Campos

#### 1. accounts_usuario (Usuario)
```sql
- id: BIGINT (PK, Auto)
- password: VARCHAR(128)
- last_login: TIMESTAMP
- is_superuser: BOOLEAN
- first_name: VARCHAR(150)
- last_name: VARCHAR(150)
- is_staff: BOOLEAN
- is_active: BOOLEAN
- date_joined: TIMESTAMP
- avatar: VARCHAR(200) (NULL)
- email: VARCHAR(254) (UNIQUE, INDEX)
- nombre: VARCHAR(255) (INDEX)
```

#### 2. roles_rol (Rol)
```sql
- id: BIGINT (PK, Auto)
- nombre: VARCHAR(50) (UNIQUE)
- color: VARCHAR(7)
- icono_url: VARCHAR(200) (NULL)
```

#### 3. permisos_permiso (Permiso)
```sql
- id: BIGINT (PK, Auto)
- nombre: VARCHAR(100) (UNIQUE)
```

#### 4. grupos_grupo (Grupo)
```sql
- id: BIGINT (PK, Auto)
- nombre: VARCHAR(255) (UNIQUE)
- logo: VARCHAR(100) (NULL)
- fecha_creacion: TIMESTAMP
- creado_por_id: BIGINT (FK → accounts_usuario.id) (NULL)
- activo: BOOLEAN
- lider_id: BIGINT (FK → accounts_usuario.id) (NULL)
```

#### 5. proyectos_proyecto (Proyecto)
```sql
- id: BIGINT (PK, Auto)
- nombre: VARCHAR(200) (UNIQUE)
- descripcion: TEXT (NULL)
- metodologia: VARCHAR(20) (NULL)
- fecha_creacion: TIMESTAMP
- activo: BOOLEAN
- logo: VARCHAR(100) (NULL)
- grupo_id: BIGINT (FK → grupos_grupo.id) (NULL)
- lider_id: BIGINT (FK → accounts_usuario.id) (NULL)
- creado_por_id: BIGINT (FK → accounts_usuario.id) (NULL)
```

#### 6. proyectos_participacionproyecto (ParticipacionProyecto)
```sql
- id: BIGINT (PK, Auto)
- usuario_id: BIGINT (FK → accounts_usuario.id)
- proyecto_id: BIGINT (FK → proyectos_proyecto.id)
- rol_id: BIGINT (FK → roles_rol.id)
- fecha_asignacion: TIMESTAMP
```
**UNIQUE:** (usuario_id, proyecto_id)

#### 7. requerimientos_requerimiento (Requerimiento)
```sql
- id: BIGINT (PK, Auto)
- nombre: VARCHAR(255)
- descripcion: TEXT
- tipo: VARCHAR(20)
- estado: VARCHAR(20)
- proyecto_id: BIGINT (FK → proyectos_proyecto.id)
- creado_por_id: BIGINT (FK → accounts_usuario.id) (NULL)
- fecha_creacion: TIMESTAMP
- fecha_actualizacion: TIMESTAMP
- imagen: VARCHAR(100) (NULL)
- link_externo: VARCHAR(500)
- detalle_tradicional_id: BIGINT (FK → requerimientos_detallerequerimientotradicional.id) (NULL)
- detalle_agil_id: BIGINT (FK → requerimientos_detallerequerimientoagil.id) (NULL)
```

#### 8. requerimientos_detallerequerimientotradicional (DetalleRequerimientoTradicional)
```sql
- id: BIGINT (PK, Auto)
- requerimiento_padre_id: BIGINT (FK → requerimientos_requerimiento.id) (UNIQUE)
- prioridad: VARCHAR(50)
- fuente: VARCHAR(255)
- categoria: VARCHAR(100)
- fecha_compromiso: DATE (NULL)
- estado_validacion: VARCHAR(100)
- observaciones: TEXT
```

#### 9. requerimientos_detallerequerimientoagil (DetalleRequerimientoAgil)
```sql
- id: BIGINT (PK, Auto)
- requerimiento_padre_id: BIGINT (FK → requerimientos_requerimiento.id) (UNIQUE)
- historia_usuario: TEXT
- criterio_aceptacion: TEXT
- puntos_estimados: INTEGER (NULL)
- sprint_asignado: VARCHAR(100)
- responsable: VARCHAR(100)
- estado_scrum: VARCHAR(100)
- observaciones: TEXT
```

#### 10. casos_de_uso_casodeuso (CasoDeUso)
```sql
- id: BIGINT (PK, Auto)
- nombre: VARCHAR(255)
- descripcion: TEXT
- proyecto_id: BIGINT (FK → proyectos_proyecto.id)
- creado_por_id: BIGINT (FK → accounts_usuario.id) (NULL)
- fecha_creacion: TIMESTAMP
- fecha_actualizacion: TIMESTAMP
- imagen: VARCHAR(100) (NULL)
- link_externo: VARCHAR(500)
- detalle_tradicional_id: BIGINT (FK → casos_de_uso_detallecasodeusotradicional.id) (NULL)
- detalle_agil_id: BIGINT (FK → casos_de_uso_detallecasodeusoagil.id) (NULL)
```

#### 11. casos_de_uso_detallecasodeusotradicional (DetalleCasoDeUsoTradicional)
```sql
- id: BIGINT (PK, Auto)
- caso_de_uso_padre_id: BIGINT (FK → casos_de_uso_casodeuso.id) (UNIQUE)
- actor_principal: VARCHAR(255)
- precondiciones: TEXT
- flujo_principal: TEXT
- flujo_alternativo: TEXT
- postcondiciones: TEXT
- observaciones: TEXT
```

#### 12. casos_de_uso_detallecasodeusoagil (DetalleCasoDeUsoAgil)
```sql
- id: BIGINT (PK, Auto)
- caso_de_uso_padre_id: BIGINT (FK → casos_de_uso_casodeuso.id) (UNIQUE)
- historia_usuario: TEXT
- criterio_aceptacion: TEXT
- responsable: VARCHAR(100)
- estado_scrum: VARCHAR(100)
- observaciones: TEXT
```

#### 13. requerimientos_requerimientocaso (RequerimientoCaso)
```sql
- id: BIGINT (PK, Auto)
- requerimiento_id: BIGINT (FK → requerimientos_requerimiento.id)
- caso_de_uso_id: BIGINT (FK → casos_de_uso_casodeuso.id)
- fecha_vinculacion: TIMESTAMP
- nota: VARCHAR(255)
```
**UNIQUE:** (requerimiento_id, caso_de_uso_id)

#### 14. auditoria_registroactividad (RegistroActividad)
```sql
- id: BIGINT (PK, Auto)
- usuario_id: BIGINT (FK → accounts_usuario.id) (NULL)
- accion: VARCHAR(20)
- descripcion: TEXT
- detalles: JSON (NULL)
- ip_address: INET (NULL)
- user_agent: TEXT
- fecha: TIMESTAMP
```

## Relaciones Many-to-Many (Tablas Intermedias)

#### 15. accounts_usuario_roles (Usuario ↔ Rol)
```sql
- id: BIGINT (PK, Auto)
- usuario_id: BIGINT (FK → accounts_usuario.id)
- rol_id: BIGINT (FK → roles_rol.id)
```

#### 16. grupos_grupo_integrantes (Grupo ↔ Usuario - Integrantes)
```sql
- id: BIGINT (PK, Auto)
- grupo_id: BIGINT (FK → grupos_grupo.id)
- usuario_id: BIGINT (FK → accounts_usuario.id)
```

#### 17. roles_rol_permisos (Rol ↔ Permiso)
```sql
- id: BIGINT (PK, Auto)
- rol_id: BIGINT (FK → roles_rol.id)
- permiso_id: BIGINT (FK → permisos_permiso.id)
```

#### 18. requerimientos_requerimiento_casos_relacionados (Requerimiento ↔ CasoDeUso)
```sql
- id: BIGINT (PK, Auto)
- requerimiento_id: BIGINT (FK → requerimientos_requerimiento.id)
- casodeuso_id: BIGINT (FK → casos_de_uso_casodeuso.id)
```

## Tablas de Historial (Django Simple History)

#### 19. proyectos_historicalproyecto
#### 20. requerimientos_historicalrequerimiento
#### 21. casos_de_uso_historicalcasodeuso

*(Tablas automáticas generadas por django-simple-history para tracking de cambios)*

## Instrucciones para Generar el Diagrama

### Formato Preferido
**Utiliza Mermaid.js** para generar el diagrama ERD (Entity Relationship Diagram).

### Estructura del Diagrama
1. **Entidades Principales** (rectángulos azules):
   - Usuario, Rol, Permiso, Grupo, Proyecto, Requerimiento, CasoDeUso, RegistroActividad

2. **Entidades de Detalle** (rectángulos verdes):
   - DetalleRequerimientoTradicional, DetalleRequerimientoAgil
   - DetalleCasoDeUsoTradicional, DetalleCasoDeUsoAgil
   - ParticipacionProyecto, RequerimientoCaso

3. **Relaciones**:
   - **One-to-One**: Línea continua con `|o--||o`
   - **One-to-Many**: Línea continua con `||--o{`
   - **Many-to-Many**: Línea discontinua con `}o--o{`

### Campos a Mostrar
- **Campos PK**: En negrita con `*`
- **Campos FK**: Con sufijo `_id`
- **Campos únicos**: Con subrayado
- **Campos opcionales**: Con `(NULL)` al final

### Agrupación Lógica
- **Grupo de Autenticación**: Usuario, Rol, Permiso
- **Grupo de Organización**: Grupo, Proyecto, ParticipacionProyecto
- **Grupo de Requerimientos**: Requerimiento, DetalleRequerimiento*, RequerimientoCaso
- **Grupo de Casos de Uso**: CasoDeUso, DetalleCasoDeUso*
- **Grupo de Auditoría**: RegistroActividad

### Colores y Estilos
- **Entidades principales**: `fill:#e1f5fe`
- **Entidades de detalle**: `fill:#f3e5f5`
- **Relaciones One-to-One**: `stroke:#4caf50,stroke-width:2px`
- **Relaciones One-to-Many**: `stroke:#2196f3,stroke-width:2px`
- **Relaciones Many-to-Many**: `stroke:#ff9800,stroke-width:2px,stroke-dasharray:5`

### Output Esperado
1. **Código Mermaid completo** para el diagrama
2. **Descripción textual** de las relaciones principales
3. **Notas sobre integridad referencial** y constraints importantes
4. **Recomendaciones de optimización** si las hay

### Consideraciones Especiales
- **Herencia Django**: Usuario hereda de AbstractUser
- **Campos JSON**: Para detalles flexibles en auditoría
- **Constraints únicos**: En ParticipacionProyecto y RequerimientoCaso
- **Soft deletes**: No implementados (se usan campos `activo`)
- **Historial**: django-simple-history para tracking automático

Genera el diagrama completo con todas las entidades, relaciones y campos especificados.