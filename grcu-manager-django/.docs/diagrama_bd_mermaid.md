erDiagram
    %% Grupo de Autenticacion
    USUARIO {
        BIGINT id PK
        VARCHAR(128) password
        TIMESTAMP last_login
        BOOLEAN is_superuser
        VARCHAR(150) first_name
        VARCHAR(150) last_name
        BOOLEAN is_staff
        BOOLEAN is_active
        TIMESTAMP date_joined
        VARCHAR(200) avatar
        VARCHAR(254) email UK
        VARCHAR(255) nombre
    }

    ROL {
        BIGINT id PK
        VARCHAR(50) nombre UK
        VARCHAR(7) color
        VARCHAR(200) icono_url
    }

    PERMISO {
        BIGINT id PK
        VARCHAR(100) nombre UK
    }

    %% Grupo de Organizacion
    GRUPO {
        BIGINT id PK
        VARCHAR(255) nombre UK
        VARCHAR(100) logo
        TIMESTAMP fecha_creacion
        BIGINT creado_por_id FK
        BOOLEAN activo
        BIGINT lider_id FK
    }

    PROYECTO {
        BIGINT id PK
        VARCHAR(200) nombre UK
        TEXT descripcion
        VARCHAR(20) metodologia
        TIMESTAMP fecha_creacion
        BOOLEAN activo
        VARCHAR(100) logo
        BIGINT grupo_id FK
        BIGINT lider_id FK
        BIGINT creado_por_id FK
    }

    PARTICIPACION_PROYECTO {
        BIGINT id PK
        BIGINT usuario_id FK
        BIGINT proyecto_id FK
        BIGINT rol_id FK
        TIMESTAMP fecha_asignacion
    }

    %% Grupo de Requerimientos
    REQUERIMIENTO {
        BIGINT id PK
        VARCHAR(255) nombre
        TEXT descripcion
        VARCHAR(20) tipo
        VARCHAR(20) estado
        BIGINT proyecto_id FK
        BIGINT creado_por_id FK
        TIMESTAMP fecha_creacion
        TIMESTAMP fecha_actualizacion
        VARCHAR(100) imagen
        VARCHAR(500) link_externo
        BIGINT detalle_tradicional_id FK
        BIGINT detalle_agil_id FK
    }

    DETALLETRADICIONALREQ {
        BIGINT id PK
        BIGINT requerimiento_padre_id FK
        VARCHAR(50) prioridad
        VARCHAR(255) fuente
        VARCHAR(100) categoria
        DATE fecha_compromiso
        VARCHAR(100) estado_validacion
        TEXT observaciones
    }

    DETALLEAGILREQ {
        BIGINT id PK
        BIGINT requerimiento_padre_id FK
        TEXT historia_usuario
        TEXT criterio_aceptacion
        INTEGER puntos_estimados
        VARCHAR(100) sprint_asignado
        VARCHAR(100) responsable
        VARCHAR(100) estado_scrum
        TEXT observaciones
    }

    REQUERIMIENTO_CASO {
        BIGINT id PK
        BIGINT requerimiento_id FK
        BIGINT caso_de_uso_id FK
        TIMESTAMP fecha_vinculacion
        VARCHAR(255) nota
    }

    %% Grupo de Casos de Uso
    CASO_DE_USO {
        BIGINT id PK
        VARCHAR(255) nombre
        TEXT descripcion
        BIGINT proyecto_id FK
        BIGINT creado_por_id FK
        TIMESTAMP fecha_creacion
        TIMESTAMP fecha_actualizacion
        VARCHAR(100) imagen
        VARCHAR(500) link_externo
        BIGINT detalle_tradicional_id FK
        BIGINT detalle_agil_id FK
    }

    DETALLETRADICIONALCU {
        BIGINT id PK
        BIGINT caso_de_uso_padre_id FK
        VARCHAR(255) actor_principal
        TEXT precondiciones
        TEXT flujo_principal
        TEXT flujo_alternativo
        TEXT postcondiciones
        TEXT observaciones
    }

    DETALLEAGILCU {
        BIGINT id PK
        BIGINT caso_de_uso_padre_id FK
        TEXT historia_usuario
        TEXT criterio_aceptacion
        VARCHAR(100) responsable
        VARCHAR(100) estado_scrum
        TEXT observaciones
    }

    %% Grupo de Auditoria
    REGISTRO_ACTIVIDAD {
        BIGINT id PK
        BIGINT usuario_id FK
        VARCHAR(20) accion
        TEXT descripcion
        JSON detalles
        INET ip_address
        TEXT user_agent
        TIMESTAMP fecha
    }

    %% Tablas Intermedias Many-to-Many
    USUARIO_ROLES {
        BIGINT id PK
        BIGINT usuario_id FK
        BIGINT rol_id FK
    }

    GRUPO_INTEGRANTES {
        BIGINT id PK
        BIGINT grupo_id FK
        BIGINT usuario_id FK
    }

    ROL_PERMISOS {
        BIGINT id PK
        BIGINT rol_id FK
        BIGINT permiso_id FK
    }

    REQ_CASOS_RELACIONADOS {
        BIGINT id PK
        BIGINT requerimiento_id FK
        BIGINT casodeuso_id FK
    }

    %% Relaciones One-to-Many
    USUARIO ||--o{ GRUPO : creado_por_id
    USUARIO ||--o{ GRUPO : lider_id
    USUARIO ||--o{ PROYECTO : lider_id
    USUARIO ||--o{ PROYECTO : creado_por_id
    USUARIO ||--o{ REQUERIMIENTO : creado_por_id
    USUARIO ||--o{ CASO_DE_USO : creado_por_id
    USUARIO ||--o{ REGISTRO_ACTIVIDAD : usuario_id

    GRUPO ||--o{ PROYECTO : grupo_id

    PROYECTO ||--o{ REQUERIMIENTO : proyecto_id
    PROYECTO ||--o{ CASO_DE_USO : proyecto_id

    REQUERIMIENTO ||--o{ DETALLETRADICIONALREQ : detalle_tradicional_id
    REQUERIMIENTO ||--o{ DETALLEAGILREQ : detalle_agil_id

    CASO_DE_USO ||--o{ DETALLETRADICIONALCU : detalle_tradicional_id
    CASO_DE_USO ||--o{ DETALLEAGILCU : detalle_agil_id

    %% Relaciones Many-to-Many (a traves de tablas intermedias)
    USUARIO }o--o{ ROL : USUARIO_ROLES
    GRUPO }o--o{ USUARIO : GRUPO_INTEGRANTES
    ROL }o--o{ PERMISO : ROL_PERMISOS
    REQUERIMIENTO }o--o{ CASO_DE_USO : REQ_CASOS_RELACIONADOS

    %% Relaciones Many-to-Many directas
    PROYECTO }o--o{ USUARIO : PARTICIPACION_PROYECTO
    REQUERIMIENTO }o--o{ CASO_DE_USO : REQUERIMIENTO_CASO

    %% Relaciones One-to-One
    REQUERIMIENTO |o--||o DETALLETRADICIONALREQ : detalle_tradicional_id
    REQUERIMIENTO |o--||o DETALLEAGILREQ : detalle_agil_id
    CASO_DE_USO |o--||o DETALLETRADICIONALCU : detalle_tradicional_id
    CASO_DE_USO |o--||o DETALLEAGILCU : detalle_agil_id