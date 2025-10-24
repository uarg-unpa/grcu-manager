-- ================================================================================
-- DATOS DE EJEMPLO PARA PRESENTACIÓN - GRCU MANAGER
-- ================================================================================
-- Universidad Nacional de la Patagonia Austral (UNPA)
-- Laboratorio de Desarrollo de Software - 2025
-- Grupo 4Bytes: Abril Alvarez, Martina Gagna, Cristian Carranza, Nicolás Butterfield
-- 
-- Descripción: Carga de datos de ejemplo en las 4 tablas principales del sistema
--              para demostración funcional en presentación académica.
-- 
-- IMPORTANTE: Este script asume que:
--   1. El esquema de base de datos ya fue creado (esquema_grcu_manager_presentacion.sql)
--   2. Las tablas están vacías (sin datos previos)
--   3. Los roles básicos ya fueron creados por el sistema Django
--
-- Tablas incluidas:
--   - accounts_usuario (4 usuarios de ejemplo)
--   - proyectos_proyecto (2 proyectos de ejemplo)
--   - requerimientos_requerimiento (6 requerimientos de ejemplo)
--   - casos_de_uso_casodeuso (4 casos de uso de ejemplo)
-- ================================================================================

-- ================================================================================
-- 1. USUARIOS DE EJEMPLO (accounts_usuario)
-- ================================================================================
-- Nota: El campo 'password' tiene un hash inválido porque estos usuarios usan OAuth2.
--       Solo el superusuario admin necesita un password válido para el panel Django.

INSERT INTO accounts_usuario (
    id, 
    password, 
    last_login, 
    is_superuser, 
    email, 
    nombre, 
    is_staff, 
    is_active, 
    date_joined,
    avatar
) VALUES 
-- Usuario 1: Líder de proyecto (Abril Alvarez)
(
    1,
    'pbkdf2_sha256$600000$invalid_oauth2_hash_1',  -- Hash inválido (OAuth2)
    NULL,
    false,
    'abril.alvarez@unpa.edu.ar',
    'Abril Alvarez',
    false,
    true,
    '2025-01-15 10:00:00+00',
    ''
),

-- Usuario 2: Analista/Desarrollador (Martina Gagna)
(
    2,
    'pbkdf2_sha256$600000$invalid_oauth2_hash_2',  -- Hash inválido (OAuth2)
    NULL,
    false,
    'martina.gagna@unpa.edu.ar',
    'Martina Gagna',
    false,
    true,
    '2025-01-15 11:30:00+00',
    ''
),

-- Usuario 3: Desarrollador (Cristian Carranza)
(
    3,
    'pbkdf2_sha256$600000$invalid_oauth2_hash_3',  -- Hash inválido (OAuth2)
    NULL,
    false,
    'cristian.carranza@unpa.edu.ar',
    'Cristian Carranza',
    false,
    true,
    '2025-01-15 12:00:00+00',
    ''
),

-- Usuario 4: Tester/QA (Nicolás Butterfield)
(
    4,
    'pbkdf2_sha256$600000$invalid_oauth2_hash_4',  -- Hash inválido (OAuth2)
    NULL,
    false,
    'nicolas.butterfield@unpa.edu.ar',
    'Nicolás Butterfield',
    false,
    true,
    '2025-01-15 12:30:00+00',
    ''
);

-- Actualizar la secuencia de IDs
SELECT setval('accounts_usuario_id_seq', 4, true);


-- ================================================================================
-- 2. PROYECTOS DE EJEMPLO (proyectos_proyecto)
-- ================================================================================

INSERT INTO proyectos_proyecto (
    id,
    nombre,
    descripcion,
    fecha_inicio,
    fecha_fin,
    estado,
    metodologia,
    logo,
    grupo_id,
    lider_id,
    creado_por_id,
    fecha_creacion,
    fecha_actualizacion
) VALUES
-- Proyecto 1: Sistema de Gestión Académica (Metodología TRADICIONAL)
(
    1,
    'Sistema de Gestión Académica UNPA',
    'Sistema integral para gestión de alumnos, materias, inscripciones y calificaciones de la Universidad Nacional de la Patagonia Austral. Incluye módulos de seguimiento académico, generación de actas y reportes estadísticos.',
    '2025-02-01',
    '2025-06-30',
    'EN_PROGRESO',
    'TRADICIONAL',  -- Metodología tradicional (cascada)
    '',
    NULL,  -- Sin grupo asignado
    1,     -- Líder: Abril Alvarez
    1,     -- Creado por: Abril Alvarez
    '2025-01-20 09:00:00+00',
    '2025-01-20 09:00:00+00'
),

-- Proyecto 2: App Móvil de Reservas (Metodología ÁGIL)
(
    2,
    'App Móvil de Reservas Biblioteca',
    'Aplicación móvil para Android e iOS que permite a los estudiantes reservar espacios de estudio, computadoras y solicitar préstamos de libros en la biblioteca universitaria. Incluye notificaciones push y sistema de turnos.',
    '2025-03-01',
    '2025-05-15',
    'EN_PROGRESO',
    'AGIL',  -- Metodología ágil (Scrum)
    '',
    NULL,  -- Sin grupo asignado
    2,     -- Líder: Martina Gagna
    2,     -- Creado por: Martina Gagna
    '2025-02-10 10:30:00+00',
    '2025-02-10 10:30:00+00'
);

-- Actualizar la secuencia de IDs
SELECT setval('proyectos_proyecto_id_seq', 2, true);


-- ================================================================================
-- 3. REQUERIMIENTOS DE EJEMPLO (requerimientos_requerimiento)
-- ================================================================================

INSERT INTO requerimientos_requerimiento (
    id,
    nombre,
    descripcion,
    tipo,
    estado,
    proyecto_id,
    creado_por_id,
    fecha_creacion,
    fecha_actualizacion,
    imagen,
    link_externo,
    detalle_tradicional_id,
    detalle_agil_id
) VALUES
-- ========================================
-- REQUERIMIENTOS DEL PROYECTO 1 (TRADICIONAL)
-- ========================================

-- REQ-001: Autenticación de usuarios
(
    1,
    'Autenticación de usuarios con credenciales institucionales',
    'El sistema debe permitir a los usuarios (estudiantes, docentes, administrativos) autenticarse utilizando sus credenciales institucionales de la UNPA. Debe incluir recuperación de contraseña y bloqueo tras 3 intentos fallidos.',
    'FUNCIONAL',
    'APROBADO',
    1,  -- Proyecto: Sistema de Gestión Académica
    2,  -- Creado por: Martina Gagna (Analista)
    '2025-01-22 14:00:00+00',
    '2025-01-23 09:15:00+00',
    '',
    '',
    NULL,  -- Se vinculará con detalle tradicional en otro script
    NULL
),

-- REQ-002: Inscripción a materias
(
    2,
    'Inscripción online a materias del cuatrimestre',
    'Los estudiantes deben poder inscribirse a las materias disponibles para el cuatrimestre actual, verificando correlatividades automáticamente. El sistema debe mostrar horarios y docentes asignados.',
    'FUNCIONAL',
    'EN_DESARROLLO',
    1,  -- Proyecto: Sistema de Gestión Académica
    2,  -- Creado por: Martina Gagna (Analista)
    '2025-01-22 14:30:00+00',
    '2025-02-01 11:00:00+00',
    '',
    '',
    NULL,
    NULL
),

-- REQ-003: Generación de actas
(
    3,
    'Generación automática de actas de examen',
    'Los docentes deben poder generar actas de examen en formato PDF con los datos de los alumnos inscriptos, firmas digitales y formato oficial de la universidad.',
    'FUNCIONAL',
    'PENDIENTE',
    1,  -- Proyecto: Sistema de Gestión Académica
    2,  -- Creado por: Martina Gagna (Analista)
    '2025-01-22 15:00:00+00',
    '2025-01-22 15:00:00+00',
    '',
    '',
    NULL,
    NULL
),

-- REQ-004: Tiempo de respuesta (No funcional)
(
    4,
    'Tiempo de respuesta menor a 2 segundos',
    'Todas las operaciones críticas (login, consultas, inscripciones) deben responder en menos de 2 segundos bajo carga normal (hasta 500 usuarios concurrentes).',
    'NO_FUNCIONAL',
    'APROBADO',
    1,  -- Proyecto: Sistema de Gestión Académica
    3,  -- Creado por: Cristian Carranza (Desarrollador)
    '2025-01-23 10:00:00+00',
    '2025-01-23 10:00:00+00',
    '',
    '',
    NULL,
    NULL
),

-- ========================================
-- REQUERIMIENTOS DEL PROYECTO 2 (ÁGIL)
-- ========================================

-- REQ-005: Búsqueda de libros
(
    5,
    'Como estudiante, quiero buscar libros disponibles para reservarlos',
    'El usuario debe poder buscar libros por título, autor o ISBN, ver disponibilidad en tiempo real y realizar reservas directamente desde la app móvil.',
    'FUNCIONAL',
    'COMPLETADO',
    2,  -- Proyecto: App Móvil de Reservas
    2,  -- Creado por: Martina Gagna (Product Owner)
    '2025-02-12 09:00:00+00',
    '2025-02-20 16:30:00+00',
    '',
    '',
    NULL,
    NULL  -- Se vinculará con detalle ágil en otro script
),

-- REQ-006: Notificaciones push
(
    6,
    'Como estudiante, quiero recibir notificaciones cuando mi turno esté próximo',
    'La app debe enviar notificaciones push 15 minutos antes del turno reservado y permitir cancelar o posponer el turno desde la notificación.',
    'FUNCIONAL',
    'EN_DESARROLLO',
    2,  -- Proyecto: App Móvil de Reservas
    2,  -- Creado por: Martina Gagna (Product Owner)
    '2025-02-12 09:30:00+00',
    '2025-02-15 14:00:00+00',
    '',
    '',
    NULL,
    NULL
);

-- Actualizar la secuencia de IDs
SELECT setval('requerimientos_requerimiento_id_seq', 6, true);


-- ================================================================================
-- 4. CASOS DE USO DE EJEMPLO (casos_de_uso_casodeuso)
-- ================================================================================

INSERT INTO casos_de_uso_casodeuso (
    id,
    nombre,
    descripcion,
    proyecto_id,
    creado_por_id,
    fecha_creacion,
    fecha_actualizacion,
    imagen,
    link_externo,
    detalle_tradicional_id,
    detalle_agil_id
) VALUES
-- ========================================
-- CASOS DE USO DEL PROYECTO 1 (TRADICIONAL)
-- ========================================

-- CU-001: Login al sistema
(
    1,
    'CU-001: Autenticarse en el sistema',
    'El usuario ingresa sus credenciales institucionales (email y contraseña) para acceder al sistema. El sistema valida las credenciales contra el directorio LDAP de la UNPA y registra el acceso en la auditoría.',
    1,  -- Proyecto: Sistema de Gestión Académica
    2,  -- Creado por: Martina Gagna
    '2025-01-24 10:00:00+00',
    '2025-01-24 10:00:00+00',
    '',
    '',
    NULL,  -- Se vinculará con detalle tradicional en otro script
    NULL
),

-- CU-002: Consultar materias disponibles
(
    2,
    'CU-002: Consultar materias disponibles para inscripción',
    'El estudiante consulta la oferta académica del cuatrimestre actual, filtrando por carrera y año. El sistema muestra horarios, docentes, cupos disponibles y correlatividades cumplidas.',
    1,  -- Proyecto: Sistema de Gestión Académica
    2,  -- Creado por: Martina Gagna
    '2025-01-24 11:00:00+00',
    '2025-01-24 11:00:00+00',
    '',
    '',
    NULL,
    NULL
),

-- ========================================
-- CASOS DE USO DEL PROYECTO 2 (ÁGIL)
-- ========================================

-- CU-003: Realizar reserva de libro
(
    3,
    'CU-003: Realizar reserva de libro desde la app',
    'El estudiante selecciona un libro de los resultados de búsqueda, elige fecha y hora de retiro, confirma la reserva y recibe un código QR de confirmación.',
    2,  -- Proyecto: App Móvil de Reservas
    3,  -- Creado por: Cristian Carranza
    '2025-02-13 14:00:00+00',
    '2025-02-13 14:00:00+00',
    '',
    '',
    NULL,
    NULL  -- Se vinculará con detalle ágil en otro script
),

-- CU-004: Cancelar reserva
(
    4,
    'CU-004: Cancelar una reserva existente',
    'El estudiante accede a "Mis reservas", selecciona la reserva que desea cancelar y confirma la cancelación. El sistema libera el turno y envía notificación de confirmación.',
    2,  -- Proyecto: App Móvil de Reservas
    3,  -- Creado por: Cristian Carranza
    '2025-02-13 14:30:00+00',
    '2025-02-13 14:30:00+00',
    '',
    '',
    NULL,
    NULL
);

-- Actualizar la secuencia de IDs
SELECT setval('casos_de_uso_casodeuso_id_seq', 4, true);


-- ================================================================================
-- VERIFICACIÓN DE DATOS CARGADOS
-- ================================================================================

-- Contar usuarios insertados (debería ser 4):
SELECT COUNT(*) AS total_usuarios FROM accounts_usuario;

-- Contar proyectos insertados (debería ser 2):
SELECT COUNT(*) AS total_proyectos FROM proyectos_proyecto;

-- Contar requerimientos insertados (debería ser 6):
SELECT COUNT(*) AS total_requerimientos FROM requerimientos_requerimiento;

-- Contar casos de uso insertados (debería ser 4):
SELECT COUNT(*) AS total_casos_uso FROM casos_de_uso_casodeuso;

-- Mostrar resumen por proyecto:
SELECT 
    p.id,
    p.nombre AS proyecto,
    p.metodologia,
    p.estado,
    COUNT(DISTINCT r.id) AS total_requerimientos,
    COUNT(DISTINCT cu.id) AS total_casos_uso
FROM proyectos_proyecto p
LEFT JOIN requerimientos_requerimiento r ON r.proyecto_id = p.id
LEFT JOIN casos_de_uso_casodeuso cu ON cu.proyecto_id = p.id
GROUP BY p.id, p.nombre, p.metodologia, p.estado
ORDER BY p.id;


-- ================================================================================
-- NOTAS IMPORTANTES
-- ================================================================================

-- 1. SOBRE LOS PASSWORDS:
--    Los usuarios tienen hashes inválidos porque usan OAuth2 (Google) para autenticarse.
--    Solo el superusuario admin necesita un password válido para el panel Django.

-- 2. SOBRE LAS RELACIONES:
--    Este script carga solo las 4 tablas principales.
--    Las tablas de detalles (tradicional/ágil) se pueden cargar en un script separado.

-- 3. SOBRE LOS IDs:
--    Los IDs están explícitamente definidos para mantener coherencia en presentaciones.
--    En producción, Django asignaría IDs automáticamente.

-- 4. SOBRE LA METODOLOGÍA:
--    - Proyecto 1 usa metodología TRADICIONAL (campos como prioridad MoSCoW)
--    - Proyecto 2 usa metodología ÁGIL (campos como historia de usuario, sprint)

-- 5. DATOS ACADÉMICOS:
--    Todos los nombres de usuarios corresponden a los integrantes del Grupo 4Bytes
--    Los emails usan dominio @unpa.edu.ar (Universidad Nacional de la Patagonia Austral)

-- ================================================================================
-- FIN DEL SCRIPT DE CARGA DE DATOS
-- Grupo 4Bytes - UNPA 2025
-- ================================================================================
