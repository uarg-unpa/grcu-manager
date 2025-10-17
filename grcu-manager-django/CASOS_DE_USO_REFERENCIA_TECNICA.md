# Casos de Uso - GRCU Manager
## Documento Revisado y Corregido

**Fecha de revisión:** 16 de octubre de 2025  
**Proyecto:** GRCU Manager - Sistema de Gestión de Requerimientos y Casos de Uso  
**Versión:** 1.1

---

## Índice de Casos de Uso

1. [CU-00: Creación de usuario administrador inicial](#cu-00-creación-de-usuario-administrador-inicial)
2. [CU-01: Autenticarse](#cu-01-autenticarse)
3. [CU-02: Gestionar usuarios](#cu-02-gestionar-usuarios)
4. [CU-03: Crear proyecto](#cu-03-crear-proyecto)
5. [CU-04: Asignar roles de usuario al proyecto](#cu-04-asignar-roles-de-usuario-al-proyecto)
6. [CU-05: Seleccionar metodología](#cu-05-seleccionar-metodología)
7. [CU-06: Registrar requerimiento](#cu-06-registrar-requerimiento)
8. [CU-07: Priorizar requerimiento](#cu-07-priorizar-requerimiento)
9. [CU-08: Consultar historial de requerimientos](#cu-08-consultar-historial-de-requerimientos)
10. [CU-09: Consultar historial de caso de uso](#cu-09-consultar-historial-de-caso-de-uso)
11. [CU-10: Registrar caso de uso](#cu-10-registrar-caso-de-uso)
12. [CU-11: Definir dependencias](#cu-11-definir-dependencias)
13. [CU-12: Agrupar requerimientos](#cu-12-agrupar-requerimientos)
14. [CU-13: Adjuntar archivo al requerimiento](#cu-13-adjuntar-archivo-al-requerimiento)
15. [CU-14: Adjuntar archivo al caso de uso](#cu-14-adjuntar-archivo-al-caso-de-uso)
16. [CU-15: Generar matriz de trazabilidad](#cu-15-generar-matriz-de-trazabilidad)
17. [CU-16: Listar casos de uso sin requerimiento](#cu-16-listar-casos-de-uso-sin-requerimiento)
18. [CU-17: Listar requerimientos sin caso de uso](#cu-17-listar-requerimientos-sin-caso-de-uso)
19. [CU-18: Comentar requerimiento](#cu-18-comentar-requerimiento)
20. [CU-19: Comentar caso de uso](#cu-19-comentar-caso-de-uso)
21. [CU-20: Validar requerimiento](#cu-20-validar-requerimiento)
22. [CU-21: Generar informe](#cu-21-generar-informe)
23. [CU-22: Visualizar trazabilidad](#cu-22-visualizar-trazabilidad)

---

## CU-00: Creación de usuario administrador inicial

### Descripción
Al iniciarse el sistema por primera vez, se verifica el estado de la base de datos. Si no existe un usuario con rol de administrador registrado, el sistema solicita la creación de uno para completar el despliegue inicial.

La persona que realiza la primera ejecución del sistema debe registrar al usuario administrador inicial mediante autenticación OAuth2 con Google. El proceso requiere:
- Dirección de correo electrónico válida (dominio Gmail)
- Autenticación exitosa mediante Google OAuth2
- Confirmación de datos del usuario (nombre, email)

Una vez validadas las credenciales, el sistema:
1. Crea el usuario administrador inicial
2. Asigna automáticamente el rol "Admin"
3. Habilita todas las funcionalidades de administración
4. Completa el despliegue inicial del sistema

### Actores
- **Instalador del sistema** (primera ejecución)

### Precondiciones
- Sistema desplegado pero sin usuarios administradores en la base de datos
- Configuración de Google OAuth2 completada (CLIENT_ID, CLIENT_SECRET)
- Base de datos inicializada con las tablas correspondientes

### Postcondiciones
- Usuario administrador creado con rol "Admin"
- Sistema listo para uso colaborativo
- Posibilidad de crear nuevos usuarios y proyectos

### Flujo Principal
1. El instalador accede a la URL del sistema
2. El sistema detecta la ausencia de usuarios administradores
3. El sistema redirige a la pantalla de creación de administrador inicial
4. El instalador selecciona "Iniciar sesión con Google"
5. Google solicita autenticación y permisos
6. El instalador autoriza el acceso
7. El sistema recibe los datos del usuario (email, nombre)
8. El sistema crea el usuario y le asigna el rol "Admin"
9. El sistema redirige al dashboard de administración
10. El sistema muestra mensaje de bienvenida

### Flujos Alternativos
**3a. Ya existe un administrador en el sistema**
- El sistema redirige directamente a la pantalla de login estándar

**6a. El usuario cancela la autenticación OAuth2**
- El sistema muestra mensaje explicativo
- Retorna a la pantalla de creación inicial
- Permite reintentar el proceso

**6b. Error en la autenticación con Google**
- El sistema captura el error
- Muestra mensaje de error detallado
- Registra el error en logs del sistema
- Permite reintentar

### Notas Técnicas
- Este caso de uso se ejecuta **una única vez** en el ciclo de vida del sistema
- Implementado en: `accounts/views.py` (lógica de primer uso)
- El rol "Admin" debe existir previamente en la tabla `roles_rol` (fixture o migration)

### Observaciones de Revisión
✅ **Correcciones aplicadas:**
- Especificado que se usa Google OAuth2 (no OAuth2 genérico)
- Clarificado el flujo de autenticación
- Agregados flujos alternativos para errores comunes
- Añadidas notas técnicas sobre implementación

---

## CU-01: Autenticarse

### Descripción
Un usuario accede a la aplicación web mediante autenticación OAuth2 con Google, utilizando exclusivamente una cuenta de Gmail válida. 

Una vez validada la autenticación:
1. El sistema recupera o crea el perfil del usuario en la base de datos local
2. Verifica los roles asignados al usuario
3. Establece la sesión de usuario
4. Redirige al dashboard correspondiente según su rol principal:
   - **Admin**: Dashboard de administración (gestión de usuarios, proyectos, grupos)
   - **Líder**: Dashboard de líder (gestión de proyectos asignados)
   - **Desarrollador/Visitante**: Dashboard limitado según permisos

### Actores
- **Usuario registrado** (cualquier rol: Admin, Líder, Desarrollador, Visitante)

### Precondiciones
- El usuario debe tener una cuenta de Google (Gmail)
- El usuario debe estar registrado en el sistema (excepto primer login donde se auto-registra)
- Configuración OAuth2 activa y funcional

### Postcondiciones
- Sesión de usuario establecida
- Token de acceso almacenado en cookies/sesión
- Usuario redirigido al dashboard correspondiente
- Registro de acceso en log de auditoría

### Flujo Principal
1. El usuario accede a la URL de login del sistema
2. El sistema muestra la pantalla de autenticación
3. El usuario selecciona "Iniciar sesión con Google"
4. El sistema redirige a Google OAuth2
5. Google solicita credenciales y autorización
6. El usuario introduce sus credenciales de Gmail
7. El usuario autoriza el acceso del sistema a su información básica
8. Google redirige de vuelta al sistema con el token
9. El sistema valida el token con Google
10. El sistema busca o crea el usuario en la base de datos local
11. El sistema recupera los roles asignados al usuario
12. El sistema establece la sesión
13. El sistema redirige al dashboard correspondiente

### Flujos Alternativos
**6a. Credenciales incorrectas**
- Google muestra error de autenticación
- El usuario puede reintentar
- Después de 3 intentos fallidos, Google bloquea temporalmente

**7a. El usuario cancela la autorización**
- Google redirige con parámetro de cancelación
- El sistema muestra mensaje: "Autenticación cancelada"
- Permite reintentar el proceso

**9a. Token inválido o expirado**
- El sistema rechaza el token
- Muestra mensaje de error
- Solicita autenticación nuevamente

**11a. Usuario sin roles asignados**
- El sistema asigna rol "Visitante" por defecto
- Registra evento en log
- Notifica al administrador para asignación de roles
- Redirige a vista limitada

### Notas Técnicas
- Implementado con `django-allauth` o biblioteca OAuth2 similar
- Almacenamiento de tokens: cookies HttpOnly con flag Secure
- Tiempo de sesión configurable (default: 7 días con "Remember me")
- Refresh token para renovación automática

### Observaciones de Revisión
✅ **Correcciones aplicadas:**
- Especificado el flujo completo de OAuth2
- Agregado comportamiento de auto-registro en primer login
- Clarificado redireccionamiento según rol
- Añadido caso de usuario sin roles (asignación de Visitante por defecto)
- Añadidas notas de seguridad (tokens, cookies)

---

## CU-02: Gestionar usuarios

### Descripción
El docente con rol de **Administrador** puede realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar) sobre los usuarios del sistema. Las operaciones disponibles son:

**Crear usuario:**
- Ingresar email del nuevo usuario
- Asignar nombre completo
- Seleccionar uno o más roles: Admin, Líder, Visitante (nota: Desarrollador se asigna a nivel de proyecto)
- El usuario recibirá notificación por email para completar su perfil

**Modificar usuario:**
- Cambiar nombre
- Agregar o quitar roles globales
- Activar/desactivar cuenta
- Cambiar estado (activo/inactivo)

**Eliminar usuario:**
- Eliminación lógica (desactivación) o física según configuración
- Confirmación obligatoria mediante modal
- Validación: no permitir eliminar último administrador

**Listar usuarios:**
- Vista tabular con búsqueda y filtros
- Paginación (10 usuarios por página)
- Columnas: Nombre, Email, Roles, Estado, Acciones

### Actores
- **Administrador** (rol requerido)

### Precondiciones
- Usuario autenticado con rol "Admin"
- Acceso a la sección de gestión de usuarios

### Postcondiciones
- Cambios reflejados inmediatamente en la base de datos
- Usuario notificado por email (en caso de creación)
- Logs de auditoría actualizados
- Cache de permisos invalidado para usuarios modificados

### Flujo Principal - Crear Usuario
1. El administrador accede a la sección "Usuarios"
2. El administrador hace clic en "Crear usuario"
3. El sistema muestra el formulario de creación
4. El administrador completa los campos obligatorios:
   - Email (único en el sistema)
   - Nombre completo
   - Roles (selección múltiple: Admin, Líder, Visitante)
5. El administrador hace clic en "Guardar"
6. El sistema valida los datos
7. El sistema crea el usuario en la base de datos
8. El sistema envía email de notificación al nuevo usuario
9. El sistema muestra mensaje de éxito
10. El sistema redirige a la lista de usuarios

### Flujo Principal - Modificar Usuario
1. El administrador accede a la lista de usuarios
2. El administrador hace clic en "Editar" junto al usuario deseado
3. El sistema muestra el formulario pre-llenado con los datos actuales
4. El administrador modifica los campos necesarios
5. El administrador hace clic en "Guardar cambios"
6. El sistema valida los datos
7. El sistema actualiza el usuario en la base de datos
8. El sistema invalida el cache de sesión del usuario modificado
9. El sistema muestra mensaje de confirmación
10. El sistema redirige a la lista de usuarios

### Flujo Principal - Eliminar Usuario
1. El administrador accede a la lista de usuarios
2. El administrador hace clic en "Eliminar" junto al usuario deseado
3. El sistema muestra modal de confirmación con advertencia
4. El administrador confirma la eliminación
5. El sistema valida que no sea el último administrador
6. El sistema desactiva o elimina el usuario (según configuración)
7. El sistema cierra todas las sesiones activas del usuario
8. El sistema muestra mensaje de confirmación
9. El sistema actualiza la lista de usuarios

### Flujos Alternativos
**6a. Email duplicado al crear usuario**
- El sistema muestra error: "El email ya está registrado"
- Mantiene los demás datos en el formulario
- Permite corregir y reintentar

**5a. Intento de eliminar el último administrador**
- El sistema valida el rol antes de eliminar
- Muestra mensaje: "No se puede eliminar el último administrador del sistema"
- Cancela la operación
- Sugiere asignar rol Admin a otro usuario primero

**8a. Error al enviar email de notificación**
- El sistema registra el error en logs
- Crea el usuario de todas formas
- Muestra advertencia: "Usuario creado pero no se pudo enviar email"
- Permite reenviar notificación manualmente

### Reglas de Negocio
- RN-01: Solo usuarios con rol "Admin" pueden gestionar usuarios
- RN-02: No se permite eliminar el último administrador del sistema
- RN-03: Los emails deben ser únicos en todo el sistema
- RN-04: Un usuario puede tener múltiples roles globales
- RN-05: El rol "Desarrollador" solo se asigna a nivel de proyecto (no global)
- RN-06: La desactivación de usuario mantiene integridad referencial en proyectos

### Notas Técnicas
- Vistas: `usuarios/views.py` → `crear_usuario`, `editar_usuario`, `eliminar_usuario`
- Templates: `usuarios/templates/usuarios/`
- Validación de permisos: `@user_passes_test(is_admin)` decorator
- Eliminación: soft-delete mediante campo `activo=False`

### Observaciones de Revisión
✅ **Correcciones aplicadas:**
- Separado en tres flujos principales (Crear, Modificar, Eliminar)
- Especificados roles disponibles para asignación global
- Aclarado que "Desarrollador" se asigna por proyecto, no globalmente
- Agregada regla de validación de último administrador
- Añadido comportamiento de notificación por email
- Clarificada eliminación lógica vs física
- Agregadas reglas de negocio explícitas

---

## CU-03: Crear Proyecto

### Descripción
El docente con rol de **Administrador** crea un nuevo proyecto en el sistema, definiendo su información básica y asignando participantes. Durante la creación:

1. Define datos del proyecto:
   - Nombre (único en el sistema)
   - Descripción
   - Logo/imagen (opcional)
   - Metodología (Tradicional o Ágil) - **puede definirse en este paso o postponerse**
   
2. Asigna participantes:
   - Selecciona usuarios de la lista disponible
   - Designa al **líder del proyecto** (obligatorio)
   - Los demás participantes se asignan con rol "Desarrollador" por defecto
   
3. Resultado:
   - Proyecto creado y visible en la lista de proyectos
   - Participantes notificados por email (opcional)
   - Líder habilitado para gestionar el equipo y asignar roles específicos

El sistema soporta **múltiples proyectos en paralelo**, cada uno independiente con su propio conjunto de usuarios, requerimientos, casos de uso y configuración de metodología.

### Actores
- **Administrador** (crea el proyecto)
- **Líder** (designado durante la creación, gestiona posteriormente)
- **Desarrolladores** (asignados como participantes)

### Precondiciones
- Usuario autenticado con rol "Admin"
- Al menos un usuario disponible para designar como líder
- Sistema con usuarios registrados (para seleccionar participantes)

### Postcondiciones
- Proyecto creado en estado "Activo"
- Registros en tablas: `proyectos_proyecto`, `proyectos_participacionproyecto`
- Líder asignado con permisos de gestión del proyecto
- Participantes asociados con rol "Desarrollador" inicial
- Dashboard del líder actualizado con el nuevo proyecto

### Flujo Principal
1. El administrador accede a la sección "Proyectos"
2. El administrador hace clic en "Crear proyecto"
3. El sistema muestra el formulario de creación con tres secciones:
   - **Información básica**
   - **Selección de líder**
   - **Selección de participantes**
4. El administrador completa la información básica:
   - Nombre del proyecto (obligatorio, único)
   - Descripción (opcional)
   - Logo (archivo de imagen, opcional)
5. El administrador selecciona el líder del proyecto desde un selector
6. El administrador selecciona participantes mediante badges/checkboxes:
   - Búsqueda disponible (por nombre o email)
   - Paginación (10 usuarios por página)
   - Selección múltiple visual
7. El administrador hace clic en "Crear"
8. El sistema valida:
   - Nombre único
   - Líder seleccionado
   - Al menos un participante (incluyendo el líder)
9. El sistema crea el proyecto:
   - Inserta en `proyectos_proyecto`
   - Asigna metodología `NULL` o valor por defecto (puede editarse luego)
   - Registra al creador (`creado_por`)
10. El sistema crea relaciones de participación:
    - Inserta en `proyectos_participacionproyecto` por cada participante
    - Asigna rol "Desarrollador" a todos los participantes
11. El sistema muestra mensaje de éxito
12. El sistema redirige a la lista de proyectos

### Flujos Alternativos
**8a. Nombre de proyecto duplicado**
- El sistema detecta nombre existente
- Muestra error: "Ya existe un proyecto con este nombre"
- Mantiene los datos ingresados en el formulario
- Permite corregir y reintentar

**8b. No se seleccionó líder**
- El sistema valida el campo líder
- Muestra error: "Debe seleccionar un líder para el proyecto"
- Resalta el campo selector de líder
- Permite completar y reintentar

**8c. No se seleccionaron participantes**
- El sistema valida la lista de participantes
- Muestra advertencia: "Debe seleccionar al menos un participante"
- Sugiere agregar participantes o continuar solo con el líder
- Permite confirmar o cancelar

**6a. Búsqueda sin resultados**
- El sistema muestra mensaje: "No se encontraron usuarios"
- Permite limpiar la búsqueda
- Muestra lista completa de usuarios disponibles

**9a. Error al subir logo**
- El sistema captura el error
- Muestra mensaje: "Error al subir la imagen, intente con otro archivo"
- Permite continuar sin logo o reintentar
- Valida tamaño y formato de imagen (PNG, JPG, máx 2MB)

### Reglas de Negocio
- RN-01: Solo usuarios con rol "Admin" pueden crear proyectos
- RN-02: El nombre del proyecto debe ser único en todo el sistema
- RN-03: Todo proyecto debe tener un líder designado
- RN-04: El líder debe ser uno de los participantes del proyecto
- RN-05: Los participantes iniciales reciben rol "Desarrollador" (el líder puede cambiar roles después)
- RN-06: La metodología puede definirse al crear o editarse posteriormente por el líder
- RN-07: Un usuario puede participar en múltiples proyectos simultáneamente
- RN-08: Un usuario puede tener diferentes roles en diferentes proyectos

### Notas Técnicas
- Vista: `proyectos/views.py` → `crear_proyecto`
- Template: `proyectos/templates/proyectos/crear_proyecto.html`
- Modelo: `Proyecto` (con FK a `lider`) y `ParticipacionProyecto` (tabla intermedia)
- Los participantes se envían como `name="participantes"` (checkbox values)
- JavaScript: selección visual de badges con clase `.participante-badge.active`
- Validación de permisos: `@user_passes_test(is_admin)`

### Observaciones de Revisión
✅ **Correcciones aplicadas:**
- Clarificado que la metodología puede definirse al crear o postponerse
- Especificado que participantes inician con rol "Desarrollador"
- Agregado detalle de selección visual (badges/checkboxes con paginación)
- Aclarado que el líder gestiona roles posteriormente (CU-04)
- Añadido flujo alternativo para validación de participantes
- Especificadas las tablas de base de datos involucradas
- Agregadas reglas de negocio sobre roles por proyecto
- Añadidas notas técnicas de implementación actual

---

## CU-04: Asignar roles de usuario al proyecto

### Descripción
El **líder del proyecto** asigna y gestiona los roles específicos de los participantes dentro de su proyecto. 

Los usuarios ya deben estar agregados como participantes del proyecto (ver CU-03). El líder puede:
- Cambiar el rol de cualquier participante
- Ver la lista actual de participantes con sus roles
- Asignar roles según las necesidades del proyecto

**Roles disponibles para asignación por proyecto:**
- **Desarrollador** (rol por defecto al agregar participante)
- **Analista**
- **Tester/Ingeniero de pruebas**
- **Stakeholder/Cliente**
- **Lector** (solo lectura)

El sistema registra los cambios de rol y actualiza los permisos del usuario en el contexto del proyecto inmediatamente.

### Actores
- **Líder del proyecto** (actor principal)
- **Participantes del proyecto** (afectados por la asignación)

### Precondiciones
- Usuario autenticado con rol de líder en el proyecto específico
- Proyecto existente con participantes asignados
- Usuario a modificar debe ser participante del proyecto

### Postcondiciones
- Rol del participante actualizado en tabla `proyectos_participacionproyecto`
- Permisos del usuario actualizados en el contexto del proyecto
- Cache de permisos invalidado para el usuario modificado
- Registro en log de auditoría con la asignación realizada

### Flujo Principal
1. El líder accede a su dashboard
2. El líder selecciona el proyecto a gestionar
3. El líder accede a la sección "Gestión de equipo" o "Participantes"
4. El sistema muestra la lista de participantes con roles actuales:
   - Nombre del usuario
   - Email
   - Rol actual en el proyecto
   - Botón "Cambiar rol"
5. El líder hace clic en "Cambiar rol" junto al participante deseado
6. El sistema muestra modal o selector con roles disponibles:
   - Desarrollador
   - Analista
   - Tester
   - Stakeholder
   - Lector
7. El líder selecciona el nuevo rol
8. El líder confirma el cambio
9. El sistema valida que el líder tenga permisos sobre el proyecto
10. El sistema actualiza el registro en `proyectos_participacionproyecto`:
    - Cambia el campo `rol_id` al nuevo rol
    - Actualiza `fecha_asignacion` (si existe el campo)
11. El sistema invalida el cache de permisos del usuario
12. El sistema muestra mensaje de confirmación: "Rol actualizado exitosamente"
13. El sistema actualiza la lista de participantes con el nuevo rol

### Flujos Alternativos
**9a. Usuario no tiene permisos de líder**
- El sistema valida el rol del usuario solicitante
- Muestra error: "No tienes permisos para modificar roles en este proyecto"
- Registra el intento en log de seguridad
- Redirige al dashboard

**10a. Participante no existe en el proyecto**
- El sistema valida la relación usuario-proyecto
- Muestra error: "El usuario no es participante de este proyecto"
- Cancela la operación
- Permite volver a la lista

**11a. Error al actualizar rol**
- El sistema captura la excepción
- Muestra mensaje: "Error al actualizar el rol, intente nuevamente"
- Registra el error en logs
- Mantiene el rol anterior
- Permite reintentar

### Flujos Opcionales
**Asignación masiva (extensión futura):**
1. El líder selecciona múltiples participantes
2. El líder elige un rol común
3. El sistema aplica el cambio a todos los seleccionados
4. Muestra resumen de cambios realizados

**Historial de cambios de rol (extensión futura):**
1. El líder accede al perfil del participante
2. El sistema muestra historial de roles en el proyecto
3. Incluye fecha, rol anterior, rol nuevo, quién realizó el cambio

### Reglas de Negocio
- RN-01: Solo el líder del proyecto puede asignar roles dentro de ese proyecto
- RN-02: El líder no puede cambiar su propio rol
- RN-03: Solo se pueden asignar roles a usuarios que ya sean participantes
- RN-04: Un participante solo puede tener un rol a la vez en un proyecto
- RN-05: El rol "Admin" es global y no se asigna por proyecto
- RN-06: El rol "Líder" es único por proyecto y se asigna al crear el proyecto
- RN-07: Los permisos asociados al rol se aplican inmediatamente
- RN-08: Un usuario puede tener diferentes roles en diferentes proyectos

### Permisos por Rol (Resumen)
| Rol | Requerimientos | Casos de Uso | Comentarios | Matriz | Informes |
|-----|---------------|--------------|-------------|--------|----------|
| **Desarrollador** | Leer/Crear/Editar | Leer/Crear/Editar | Crear | Ver | Ver |
| **Analista** | Full | Full | Crear | Ver/Generar | Generar |
| **Tester** | Leer | Leer/Editar | Crear | Ver | Ver |
| **Stakeholder** | Leer | Leer | Crear | Ver | Ver |
| **Lector** | Solo lectura | Solo lectura | Solo lectura | Ver | Ver |

### Notas Técnicas
- Vista propuesta: `proyectos/views.py` → `asignar_roles` (pendiente de implementación)
- Template propuesto: `proyectos/templates/proyectos/gestionar_equipo.html`
- Modelo: Actualizar `ParticipacionProyecto.rol`
- Validación: verificar `request.user == proyecto.lider`
- Los roles están definidos en `roles/models.py` → constantes de clase `Rol`

### Estado de Implementación
⚠️ **Pendiente de implementación completa**
- Actualmente los roles se asignan al crear el proyecto (todos como "Desarrollador")
- Se requiere implementar vista y template de gestión de equipo
- Necesario agregar decorador de validación de líder
- Considerar agregar signals para invalidar cache de permisos

### Observaciones de Revisión
✅ **Correcciones aplicadas:**
- Especificados roles disponibles para asignación por proyecto
- Aclarado que Admin y Líder son roles especiales (no se asignan aquí)
- Agregada tabla de permisos por rol
- Clarificado que participante debe existir previamente
- Añadido flujo de cambio individual de rol
- Especificada actualización de tabla intermedia `ParticipacionProyecto`
- Agregadas reglas de negocio sobre restricciones de roles
- Añadida nota sobre estado de implementación actual

---

## CU-05: Seleccionar metodología

### Descripción
Al inicio de un proyecto, el **líder** debe seleccionar la metodología de trabajo que se aplicará: **Tradicional** o **Ágil**.

Esta elección es crucial porque determina:
- Los campos y formularios disponibles para requerimientos
- Los campos y formularios disponibles para casos de uso
- La estructura de los detalles (tablas `DetalleRequerimientoTradicional`/`DetalleRequerimientoAgil`)
- El flujo de trabajo y validaciones aplicables

**Opciones disponibles:**

**Metodología Tradicional:**
- Enfoque en documentación exhaustiva
- Requerimientos con campos formales (fuente, categoría, prioridad)
- Casos de uso con precondiciones, flujos, postcondiciones
- Énfasis en trazabilidad completa

**Metodología Ágil:**
- Enfoque en historias de usuario
- Requerimientos expresados como "Como [rol], quiero [acción] para [beneficio]"
- Casos de uso simplificados con criterios de aceptación
- Énfasis en sprints, puntos de historia, backlog

Una vez seleccionada, la metodología puede cambiarse posteriormente **solo si no hay requerimientos o casos de uso registrados**, para evitar inconsistencias en los datos.

### Actores
- **Líder del proyecto** (selecciona la metodología)
- **Administrador** (puede cambiar metodología si está vacío el proyecto)

### Precondiciones
- Proyecto creado (CU-03)
- Usuario autenticado como líder del proyecto o administrador
- Proyecto sin metodología definida o vacío (sin requerimientos/casos de uso)

### Postcondiciones
- Campo `metodologia` del proyecto actualizado en la base de datos
- Sistema adapta formularios y vistas según metodología seleccionada
- Opciones de creación de requerimientos/casos de uso reflejan la metodología
- Plantillas dinámicas muestran campos específicos de la metodología

### Flujo Principal
1. El líder accede a su proyecto recién creado
2. El sistema detecta que la metodología no está definida
3. El sistema muestra pantalla de selección de metodología con:
   - Título: "Selecciona la metodología para este proyecto"
   - Dos tarjetas descriptivas (Tradicional / Ágil)
   - Descripción de cada metodología
   - Botones de selección
4. El líder revisa las opciones disponibles
5. El líder hace clic en la metodología deseada (Tradicional o Ágil)
6. El sistema muestra modal de confirmación:
   - "¿Estás seguro de seleccionar metodología [X]?"
   - "Esta decisión afecta la estructura de requerimientos y casos de uso"
   - Botones: "Confirmar" / "Cancelar"
7. El líder confirma la selección
8. El sistema actualiza el campo `proyecto.metodologia`:
   - `metodologia = "TRADICIONAL"` o `"AGIL"`
9. El sistema registra el cambio en logs de auditoría
10. El sistema muestra mensaje de éxito: "Metodología seleccionada: [X]"
11. El sistema redirige al dashboard del proyecto
12. El sistema adapta las vistas de creación de requerimientos/casos de uso

### Flujo Alternativo - Cambiar Metodología
1. El líder o administrador accede a la configuración del proyecto
2. El líder hace clic en "Cambiar metodología"
3. El sistema verifica si existen requerimientos o casos de uso
4. **Si el proyecto tiene datos:**
   - El sistema muestra advertencia: "No se puede cambiar la metodología porque ya existen requerimientos o casos de uso registrados"
   - Sugiere eliminar todos los datos primero o crear un nuevo proyecto
   - Cancela la operación
5. **Si el proyecto está vacío:**
   - El sistema muestra las opciones de metodología
   - Permite seleccionar la nueva metodología
   - Actualiza el proyecto
   - Confirma el cambio

### Flujos Alternativos
**3a. Metodología ya definida previamente**
- El sistema detecta que `proyecto.metodologia` no es `NULL`
- No muestra pantalla de selección
- Redirige directamente al dashboard del proyecto
- El líder puede acceder a "Configuración" para ver la metodología actual

**7a. Líder cancela la selección**
- El sistema cierra el modal de confirmación
- Vuelve a mostrar las opciones de metodología
- Permite seleccionar de nuevo

**4a. Intento de cambio con datos existentes**
- Ver "Flujo Alternativo - Cambiar Metodología" paso 4

### Impacto de la Selección de Metodología

**Campos en Requerimientos:**

| Campo | Tradicional | Ágil |
|-------|------------|------|
| Nombre | ✅ | ✅ |
| Descripción | ✅ | ✅ |
| Tipo | ✅ (Funcional/No funcional) | ✅ (Funcional/No funcional) |
| Estado | ✅ (Pendiente/En progreso/Completado) | ✅ (Pendiente/En progreso/Completado) |
| Prioridad MoSCoW | ✅ | ✅ |
| Fuente | ✅ | ❌ |
| Categoría | ✅ | ❌ |
| Fecha compromiso | ✅ | ❌ |
| Estado validación | ✅ | ❌ |
| Historia de usuario | ❌ | ✅ |
| Criterios de aceptación | ❌ | ✅ |
| Puntos estimados | ❌ | ✅ |
| Sprint asignado | ❌ | ✅ |
| Responsable | ❌ | ✅ |
| Estado Scrum | ❌ | ✅ |

**Campos en Casos de Uso:**

| Campo | Tradicional | Ágil |
|-------|------------|------|
| Nombre | ✅ | ✅ |
| Descripción | ✅ | ✅ |
| Actor principal | ✅ | ❌ |
| Precondiciones | ✅ | ❌ |
| Flujo principal | ✅ | ❌ |
| Flujo alternativo | ✅ | ❌ |
| Postcondiciones | ✅ | ❌ |
| Historia de usuario | ❌ | ✅ |
| Criterios de aceptación | ❌ | ✅ |
| Responsable | ❌ | ✅ |
| Estado Scrum | ❌ | ✅ |

### Reglas de Negocio
- RN-01: Solo el líder del proyecto o un administrador pueden seleccionar la metodología
- RN-02: La metodología debe definirse antes de crear requerimientos o casos de uso
- RN-03: No se puede cambiar la metodología si ya existen requerimientos o casos de uso
- RN-04: La metodología aplica a todo el proyecto (no se puede mezclar)
- RN-05: Los formularios se adaptan dinámicamente según la metodología
- RN-06: La metodología se hereda en los reportes y exportaciones

### Notas Técnicas
- Modelo: `proyectos.models.Proyecto` → campo `metodologia`
- Valores posibles: `"TRADICIONAL"`, `"AGIL"`, `NULL` (no definida)
- Vista propuesta: `proyectos/views.py` → `seleccionar_metodologia`
- Template propuesto: `proyectos/templates/proyectos/seleccionar_metodologia.html`
- Validación en formularios: verificar `proyecto.metodologia` antes de renderizar
- Los detalles se guardan en tablas separadas según metodología:
  - `requerimientos_detallerequerimientotradicional`
  - `requerimientos_detallerequerimientoagil`

### Estado de Implementación
⚠️ **Parcialmente implementado**
- El campo `metodologia` existe en el modelo `Proyecto`
- Los modelos de detalle tradicional/ágil están implementados
- **Falta:** Vista y template de selección inicial de metodología
- **Falta:** Validación de cambio de metodología
- **Existe:** Lógica en formularios para adaptar campos según metodología

### Observaciones de Revisión
✅ **Correcciones aplicadas:**
- Especificado que la selección puede ocurrir al crear el proyecto o después
- Clarificado que la metodología afecta campos en requerimientos Y casos de uso
- Agregadas tablas comparativas de campos por metodología
- Añadido flujo para cambiar metodología (con validación de proyecto vacío)
- Especificadas reglas de negocio sobre restricciones de cambio
- Añadido impacto técnico (tablas de detalle separadas)
- Clarificado estado de implementación actual
- Agregada advertencia sobre consistencia de datos

---

## CU-06: Registrar requerimiento

### Descripción
El **analista** o usuario con permisos adecuados registra un nuevo requerimiento en el proyecto. El sistema presenta un formulario con:

**Campos comunes (obligatorios para ambas metodologías):**
- **Nombre:** título breve del requerimiento
- **Descripción:** detalle completo del requerimiento
- **Tipo:** Funcional o No funcional
- **Estado:** Pendiente (valor por defecto)

**Campos específicos según metodología:**

**Metodología Tradicional:**
- **Fuente:** origen del requerimiento (cliente, stakeholder, regulación, etc.)
- **Categoría:** clasificación adicional (sistema, interfaz, rendimiento, etc.)
- **Prioridad MoSCoW:** Must / Should / Could / Won't
- **Fecha compromiso:** fecha esperada de entrega (opcional)
- **Estado de validación:** pendiente/aprobado/rechazado (opcional)
- **Observaciones:** notas adicionales

**Metodología Ágil:**
- **Historia de usuario:** formato "Como [rol], quiero [acción] para [beneficio]"
- **Criterios de aceptación:** condiciones que deben cumplirse para dar por completado
- **Prioridad MoSCoW:** Must / Should / Could / Won't
- **Puntos estimados:** esfuerzo en puntos de historia (opcional)
- **Sprint asignado:** nombre o número del sprint (opcional)
- **Responsable:** miembro del equipo asignado (opcional)
- **Estado Scrum:** To Do / In Progress / Done / Blocked (opcional)

El sistema valida que todos los campos obligatorios estén completos y guarda el requerimiento. Una vez registrado, queda disponible para:
- Consulta
- Edición
- Priorización
- Vinculación con casos de uso
- Comentarios
- Adjuntar archivos
- Generación de matriz de trazabilidad

### Actores
- **Analista** (rol principal para crear requerimientos)
- **Desarrollador** (puede crear según permisos)
- **Líder** (puede crear y aprobar)

### Precondiciones
- Usuario autenticado con rol de analista, desarrollador o líder en el proyecto
- Proyecto existente con metodología definida (CU-05)
- Acceso a la sección de requerimientos del proyecto

### Postcondiciones
- Requerimiento creado en tabla `requerimientos_requerimiento`
- Registro de detalle creado según metodología:
  - `requerimientos_detallerequerimientotradicional` (si tradicional)
  - `requerimientos_detallerequerimientoagil` (si ágil)
- Requerimiento visible en lista de requerimientos del proyecto
- Campos `creado_por`, `fecha_creacion` poblados automáticamente
- Log de auditoría registrado

### Flujo Principal
1. El analista accede al proyecto
2. El analista navega a la sección "Requerimientos"
3. El analista hace clic en "Crear requerimiento"
4. El sistema verifica la metodología del proyecto
5. El sistema muestra el formulario con campos específicos:
   - **Si Tradicional:** campos tradicionales
   - **Si Ágil:** campos ágiles
6. El analista completa los campos obligatorios:
   - Nombre del requerimiento
   - Descripción detallada
   - Tipo (Funcional / No funcional)
7. El analista completa los campos específicos de la metodología:
   - **Tradicional:** fuente, categoría, prioridad
   - **Ágil:** historia de usuario, criterios de aceptación, prioridad
8. El analista hace clic en "Guardar"
9. El sistema valida:
   - Campos obligatorios completos
   - Formato de historia de usuario (si ágil)
   - Valores válidos para campos con opciones
10. El sistema crea el requerimiento:
    - Inserta en `requerimientos_requerimiento`
    - Asigna valores comunes (nombre, descripción, tipo, estado, proyecto, creado_por)
11. El sistema crea el detalle específico:
    - **Si Tradicional:** inserta en `detallerequerimientotradicional`
    - **Si Ágil:** inserta en `detallerequerimientoagil`
    - Vincula con el requerimiento padre mediante FK
12. El sistema muestra mensaje de éxito: "Requerimiento creado exitosamente"
13. El sistema redirige a la vista de detalle del requerimiento o a la lista

### Flujos Alternativos
**9a. Campos obligatorios incompletos**
- El sistema detecta campos vacíos
- Resalta los campos faltantes en rojo
- Muestra mensaje: "Complete todos los campos obligatorios"
- Mantiene los datos ingresados
- Permite corregir y guardar nuevamente

**9b. Historia de usuario con formato incorrecto (Ágil)**
- El sistema valida el formato "Como... quiero... para..."
- Muestra advertencia: "Se recomienda usar el formato: Como [rol], quiero [acción] para [beneficio]"
- Permite guardar de todas formas (es recomendación, no obligatorio)

**10a. Error al guardar en base de datos**
- El sistema captura la excepción
- Muestra mensaje: "Error al guardar el requerimiento, intente nuevamente"
- Registra el error en logs con detalles técnicos
- Mantiene los datos del formulario
- Permite reintentar

**7a. Usuario cancela la creación**
- El analista hace clic en "Cancelar"
- El sistema pregunta: "¿Desea descartar los cambios?"
- Si confirma: redirige a lista de requerimientos
- Si cancela: vuelve al formulario

### Flujo Alternativo - Guardar como Borrador
1. El analista completa parcialmente el formulario
2. El analista hace clic en "Guardar como borrador"
3. El sistema guarda con estado "Borrador" (pendiente)
4. Permite editar posteriormente para completar
5. Muestra en lista con indicador de "Incompleto"

### Reglas de Negocio
- RN-01: Solo usuarios con rol de analista, desarrollador o líder pueden crear requerimientos
- RN-02: El nombre del requerimiento debe ser único dentro del proyecto
- RN-03: La descripción debe tener al menos 10 caracteres
- RN-04: Los campos específicos de metodología son obligatorios según el tipo:
  - Tradicional: prioridad y fuente son obligatorios
  - Ágil: historia de usuario y criterios de aceptación son obligatorios
- RN-05: El estado inicial siempre es "Pendiente"
- RN-06: El creador queda registrado automáticamente (`creado_por`)
- RN-07: La fecha de creación se asigna automáticamente
- RN-08: Los requerimientos sin metodología definida no pueden crearse

### Validaciones Específicas

**Tradicional:**
- Prioridad debe ser uno de: Must, Should, Could, Won't
- Fuente no puede estar vacía
- Fecha compromiso (si se proporciona) debe ser futura

**Ágil:**
- Historia de usuario debe tener al menos 20 caracteres
- Criterios de aceptación deben tener al menos 10 caracteres
- Puntos estimados (si se proporcionan) deben ser > 0
- Estado Scrum debe ser uno de: To Do, In Progress, Done, Blocked

### Notas Técnicas
- Vista: `requerimientos/views.py` → `crear_requerimiento`
- Template: `requerimientos/templates/requerimientos/requerimiento_form.html`
- Formulario: `requerimientos/forms.py` → `RequerimientoForm`
- Lógica de renderizado condicional según `proyecto.metodologia`
- Los detalles se crean automáticamente en el `save()` del formulario
- Transacción atómica: si falla el detalle, rollback del requerimiento

### Ejemplo de Historia de Usuario (Ágil)
```
Como usuario registrado,
quiero poder filtrar requerimientos por prioridad,
para enfocarme en los elementos más importantes del backlog.
```

### Estado de Implementación
✅ **Implementado**
- Formularios con campos condicionales según metodología
- Validación de campos obligatorios
- Creación de detalles tradicional/ágil
- Redirección a lista de requerimientos post-creación

⚠️ **Pendiente:**
- Validación de formato de historia de usuario
- Opción "Guardar como borrador"
- Mejoras en mensajes de error específicos
- Auto-completado de responsables desde participantes del proyecto

### Observaciones de Revisión
✅ **Correcciones aplicadas:**
- Separados claramente los campos comunes vs específicos por metodología
- Agregadas tablas comparativas de campos obligatorios
- Especificada la estructura de tablas (requerimiento + detalle tradicional/ágil)
- Añadido ejemplo de historia de usuario
- Clarificadas validaciones específicas por metodología
- Agregadas reglas de negocio sobre unicidad y longitudes mínimas
- Añadido flujo de "Guardar como borrador" (opcional/futuro)
- Especificado comportamiento de transacciones atómicas
- Actualizado estado de implementación

---

## CU-07: Priorizar requerimiento

### Descripción
El **líder del proyecto** establece y modifica la prioridad de los requerimientos utilizando el método **MoSCoW** (Must have, Should have, Could have, Won't have).

Este proceso permite:
- Asignar o cambiar prioridades de múltiples requerimientos simultáneamente
- Ordenar el backlog según importancia estratégica
- Facilitar la toma de decisiones sobre alcance y fases del proyecto
- Comunicar expectativas claras al equipo y stakeholders

**Niveles de prioridad MoSCoW:**
- **Must have (M):** Esencial para el proyecto, sin él no se puede considerar completo
- **Should have (S):** Importante pero no vital, se puede implementar en una fase posterior
- **Could have (C):** Deseable pero no crítico, se implementa si hay tiempo/recursos
- **Won't have (W):** Descartado para esta iteración, se considera para futuras versiones

La priorización se realiza a nivel de proyecto completo, mostrando todos los requerimientos en una vista consolidada con opciones para actualizar prioridades de forma masiva.

### Actores
- **Líder del proyecto** (prioriza requerimientos)
- **Equipo de desarrollo** (consulta prioridades para planificación)

### Precondiciones
- Usuario autenticado como líder del proyecto
- Proyecto con metodología **Tradicional** (la prioridad se almacena en `DetalleRequerimientoTradicional`)
- Al menos un requerimiento creado en el proyecto
- Requerimientos con detalles tradicionales inicializados

### Postcondiciones
- Prioridades actualizadas en tabla `requerimientos_detallerequerimientotradicional`
- Campo `prioridad` actualizado para los requerimientos modificados
- Cambios reflejados inmediatamente en listados y reportes
- Registro en logs de auditoría (si está implementado)

### Flujo Principal
1. El líder accede a su dashboard de proyectos
2. El líder selecciona el proyecto deseado
3. El líder navega a la sección "Requerimientos"
4. El líder hace clic en "Priorizar requerimientos" o botón equivalente
5. El sistema verifica que el usuario sea el líder del proyecto
6. El sistema recupera todos los requerimientos del proyecto con sus detalles tradicionales
7. El sistema muestra una tabla con:
   - Código/ID del requerimiento
   - Nombre del requerimiento
   - Tipo (Funcional/No funcional)
   - Estado actual
   - Selector de prioridad MoSCoW (dropdown o radio buttons)
8. El líder revisa cada requerimiento
9. El líder selecciona la prioridad MoSCoW para cada requerimiento:
   - Must have
   - Should have
   - Could have
   - Won't have
10. El líder hace clic en "Guardar prioridades"
11. El sistema valida los datos:
    - Valores válidos para prioridad
    - Permisos del usuario
12. El sistema actualiza cada registro en la base de datos:
    - Para cada requerimiento: `detalle_tradicional.prioridad = nueva_prioridad`
    - Ejecuta `save()` en cada detalle modificado
13. El sistema muestra mensaje de éxito: "Prioridades actualizadas correctamente"
14. El sistema recarga la vista con las nuevas prioridades

### Flujos Alternativos
**5a. Usuario no es el líder del proyecto**
- El sistema valida el rol del usuario
- Muestra mensaje: "Solo el líder del proyecto puede priorizar requerimientos"
- Redirige al dashboard
- Registra intento en log de seguridad

**6a. Proyecto sin requerimientos**
- El sistema detecta lista vacía
- Muestra mensaje: "No hay requerimientos para priorizar"
- Muestra botón "Crear requerimiento"
- Permite volver al dashboard del proyecto

**6b. Proyecto con metodología Ágil**
- El sistema detecta metodología ágil
- Muestra advertencia: "La priorización MoSCoW aplica principalmente a metodología tradicional"
- Permite priorizar de todas formas (la prioridad puede existir en ágil también)
- Nota: En ágil, la priorización suele hacerse mediante orden del backlog

**12a. Error al guardar prioridad**
- El sistema captura la excepción
- Muestra mensaje: "Error al actualizar prioridades, intente nuevamente"
- Registra el error en logs con detalles
- No actualiza ninguna prioridad (rollback)
- Mantiene los valores previos

### Flujo Opcional - Priorización por Drag & Drop (Extensión Futura)
1. El sistema muestra requerimientos en lista ordenable
2. El líder arrastra y suelta requerimientos para ordenar por prioridad
3. El sistema asigna prioridades automáticamente según el orden:
   - Primeros 30%: Must have
   - Siguiente 30%: Should have
   - Siguiente 30%: Could have
   - Últimos 10%: Won't have
4. Permite ajustes manuales después del ordenamiento

### Flujo Opcional - Vista Agrupada por Prioridad
1. El líder activa vista "Agrupar por prioridad"
2. El sistema muestra requerimientos agrupados en columnas:
   - Columna "Must have"
   - Columna "Should have"
   - Columna "Could have"
   - Columna "Won't have"
3. El líder arrastra requerimientos entre columnas
4. El sistema actualiza prioridades según la columna destino

### Reglas de Negocio
- RN-01: Solo el líder del proyecto puede modificar prioridades
- RN-02: La prioridad es un campo textual en `DetalleRequerimientoTradicional`
- RN-03: Los valores válidos son: "MUST", "SHOULD", "COULD", "WONT"
- RN-04: Un requerimiento puede existir sin prioridad definida (campo vacío)
- RN-05: Las prioridades pueden cambiarse en cualquier momento
- RN-06: No hay restricciones en la cantidad de requerimientos por nivel
- RN-07: La priorización es independiente del estado del requerimiento
- RN-08: Los requerimientos sin prioridad aparecen al final de las listas ordenadas

### Recomendaciones de Uso MoSCoW
- **Must have:** Máximo 60% de los requerimientos totales
- **Should have:** 20% de los requerimientos
- **Could have:** 15% de los requerimientos
- **Won't have:** 5% (requerimientos descartados para esta versión)

### Notas Técnicas
- Vista: `requerimientos/views.py` → `requerimiento_priorizar`
- Template: `requerimientos/templates/requerimientos/requerimiento_priorizar.html`
- Modelo: `DetalleRequerimientoTradicional.prioridad` (CharField max_length=50)
- Constantes: definidas en la vista como `MOSCOW_CHOICES`
- Validación: verificar `request.user == proyecto.lider`
- Actualización masiva: itera sobre `request.POST.get(f'prioridad_{req.pk}')`
- Redirect POST-Redirect-GET para evitar resubmit

### Ejemplo de Implementación Actual
```python
# En requerimientos/views.py
MOSCOW_CHOICES = [
    ("MUST", "Must have"),
    ("SHOULD", "Should have"),
    ("COULD", "Could have"),
    ("WONT", "Won't have")
]

# Actualización en POST
for req in requerimientos:
    prioridad = request.POST.get(f'prioridad_{req.pk}')
    if req.detalle_tradicional:
        if prioridad and req.detalle_tradicional.prioridad != prioridad:
            req.detalle_tradicional.prioridad = prioridad
            req.detalle_tradicional.save()
```

### Estado de Implementación
✅ **Implementado**
- Vista de priorización con selector MoSCoW
- Actualización masiva de prioridades
- Validación de líder del proyecto
- Redirección POST-Redirect-GET

⚠️ **Pendiente:**
- Ordenamiento visual por prioridad (drag & drop)
- Vista agrupada por columnas MoSCoW
- Validación de límites recomendados (advertencia si >60% son Must)
- Historial de cambios de prioridad
- Exportación de prioridades a CSV/PDF

### Observaciones de Revisión
✅ **Correcciones aplicadas:**
- Clarificado que la priorización es específica de metodología tradicional
- Especificado el método MoSCoW con definiciones claras
- Agregadas recomendaciones de distribución de prioridades
- Añadido comportamiento de actualización masiva
- Clarificada la tabla de almacenamiento (DetalleRequerimientoTradicional)
- Agregadas extensiones futuras (drag & drop, vista agrupada)
- Especificado código de implementación actual

---

## CU-08: Consultar historial de requerimientos

### Descripción
Los usuarios con permisos adecuados pueden consultar el historial completo de cambios realizados sobre un requerimiento específico.

El historial incluye:
- **Cambios de estado:** Pendiente → En progreso → Completado
- **Modificaciones de campos:** nombre, descripción, tipo, prioridad
- **Cambios en detalles específicos:** campos tradicionales/ágiles
- **Vinculaciones/desvinculaciones** con casos de uso
- **Adjuntos** agregados o eliminados
- **Comentarios** registrados
- **Metadatos:** quién realizó el cambio, cuándo, desde qué IP (opcional)

Cada entrada del historial muestra:
- Fecha y hora del cambio
- Usuario que realizó la modificación
- Tipo de cambio (creación, edición, cambio de estado, etc.)
- Valores anteriores y nuevos (para campos modificados)
- Comentario opcional sobre el motivo del cambio

Este registro es fundamental para:
- Auditoría y cumplimiento normativo
- Trazabilidad de decisiones
- Resolución de conflictos
- Análisis retrospectivo

### Actores
- **Líder del proyecto** (acceso completo al historial)
- **Desarrollador/Analista** (visualiza historial de requerimientos que puede editar)
- **Stakeholder** (visualiza historial en modo lectura)
- **Administrador** (acceso completo a todos los historiales)

### Precondiciones
- Usuario autenticado con permisos en el proyecto
- Requerimiento existente
- Sistema de auditoría habilitado (django-simple-history, django-reversion, o custom)
- Al menos un cambio registrado en el requerimiento

### Postcondiciones
- Historial mostrado sin modificar datos
- Registro de consulta en logs (opcional)
- Sin cambios en el requerimiento ni su historial

### Flujo Principal
1. El usuario accede a la lista de requerimientos del proyecto
2. El usuario selecciona un requerimiento específico
3. El usuario hace clic en "Ver detalle" o accede directamente a la vista de requerimiento
4. El sistema muestra la pantalla de detalle del requerimiento con pestañas/secciones:
   - Información actual
   - Casos de uso relacionados
   - Adjuntos
   - Comentarios
   - **Historial de cambios**
5. El usuario hace clic en la pestaña "Historial"
6. El sistema recupera todas las versiones históricas del requerimiento:
   - Desde tabla de auditoría (ej: `requerimientos_requerimiento_history`)
   - Incluye cambios en tablas relacionadas (detalles tradicional/ágil)
7. El sistema muestra una línea de tiempo cronológica inversa (más reciente primero):
   - Fecha y hora del cambio
   - Avatar/nombre del usuario que realizó el cambio
   - Icono según tipo de acción (creación, edición, cambio de estado, etc.)
   - Descripción del cambio en lenguaje natural
   - Botón "Ver detalles" para expandir
8. El usuario puede:
   - Revisar la lista completa de cambios
   - Expandir una entrada para ver detalles campo por campo
   - Comparar dos versiones específicas
   - Filtrar por tipo de cambio o rango de fechas
9. El usuario hace clic en "Ver detalles" de una entrada
10. El sistema muestra un modal/panel expandido con:
    - Tabla comparativa "Antes → Después"
    - Campos modificados destacados
    - Valores anteriores y nuevos
    - Comentario del usuario (si existe)
11. El usuario revisa los detalles
12. El usuario cierra el modal y puede continuar navegando el historial

### Flujos Alternativos
**6a. Requerimiento sin historial (recién creado)**
- El sistema detecta solo la versión inicial
- Muestra mensaje: "Este requerimiento no tiene historial de cambios aún"
- Muestra solo la entrada de creación con fecha, hora y creador

**6b. Sistema de historial no implementado**
- El sistema detecta ausencia de módulo de auditoría
- Muestra mensaje: "El historial de cambios no está disponible en este momento"
- Muestra solo: fecha de creación, creado por, fecha de última actualización
- Sugiere contactar al administrador para habilitar auditoría

**8a. Historial muy extenso (>100 cambios)**
- El sistema implementa paginación
- Muestra 20 entradas por página
- Incluye navegación: "Anterior / Siguiente"
- Opción de filtrar por rango de fechas para reducir resultados

**9a. Usuario sin permisos para ver detalles completos**
- El sistema valida permisos
- Muestra solo resumen: "Campo [X] modificado por [Usuario] el [Fecha]"
- No muestra valores específicos antiguos/nuevos
- Muestra mensaje: "Permisos limitados: contacte al líder para ver detalles completos"

### Flujo Opcional - Comparar Versiones
1. El usuario selecciona dos versiones del historial (checkbox)
2. El usuario hace clic en "Comparar versiones"
3. El sistema muestra vista lado a lado:
   - Columna izquierda: versión más antigua
   - Columna derecha: versión más reciente
   - Campos modificados destacados en amarillo
   - Valores diferentes marcados en rojo/verde
4. El usuario revisa las diferencias
5. El usuario puede exportar la comparación a PDF

### Flujo Opcional - Restaurar Versión Anterior
1. El usuario visualiza una versión histórica
2. El usuario hace clic en "Restaurar esta versión"
3. El sistema muestra advertencia: "¿Desea restaurar el requerimiento a esta versión? Los cambios actuales se perderán"
4. El usuario confirma
5. El sistema crea una nueva entrada de historial: "Restaurado a versión del [Fecha]"
6. El sistema revierte los campos a los valores de la versión seleccionada
7. El sistema muestra mensaje de confirmación
8. El usuario visualiza el requerimiento restaurado

### Información Registrada en el Historial

| Evento | Datos Capturados |
|--------|------------------|
| **Creación** | Fecha, hora, creado_por, valores iniciales |
| **Edición de campo** | Fecha, hora, modificado_por, campo, valor_anterior, valor_nuevo |
| **Cambio de estado** | Fecha, hora, usuario, estado_anterior, estado_nuevo, motivo (opcional) |
| **Cambio de prioridad** | Fecha, hora, usuario, prioridad_anterior, prioridad_nueva |
| **Vinculación con caso de uso** | Fecha, hora, usuario, caso_de_uso_id, nota |
| **Desvinculación de caso de uso** | Fecha, hora, usuario, caso_de_uso_id |
| **Adjunto agregado** | Fecha, hora, usuario, nombre_archivo, tamaño |
| **Adjunto eliminado** | Fecha, hora, usuario, nombre_archivo |
| **Comentario agregado** | Fecha, hora, usuario, texto_comentario (resumen) |

### Reglas de Negocio
- RN-01: El historial es de solo lectura para todos los usuarios
- RN-02: Solo administradores pueden eliminar entradas del historial
- RN-03: El historial se conserva incluso si el requerimiento es eliminado (soft delete)
- RN-04: Cada cambio genera una entrada independiente (granularidad por campo)
- RN-05: Los cambios simultáneos del mismo usuario se agrupan en una transacción
- RN-06: El historial incluye cambios en tablas relacionadas (detalles, vinculaciones)
- RN-07: La fecha/hora se registra en timezone del servidor
- RN-08: Se registra la IP del usuario que realiza el cambio (opcional, configurable)

### Notas Técnicas
**Estado Actual:**
⚠️ **NO IMPLEMENTADO** - El sistema actualmente NO tiene módulo de auditoría/historial

**Opciones de Implementación Recomendadas:**

**Opción 1: django-simple-history**
```python
# En requerimientos/models.py
from simple_history.models import HistoricalRecords

class Requerimiento(models.Model):
    # ... campos existentes ...
    history = HistoricalRecords()
```
- Pros: Fácil implementación, automático, incluye rollback
- Contras: Tablas adicionales por modelo, overhead de storage

**Opción 2: django-reversion**
```python
# En requerimientos/admin.py
from reversion.admin import VersionAdmin

@admin.register(Requerimiento)
class RequerimientoAdmin(VersionAdmin):
    pass
```
- Pros: Versionado completo, comparación de versiones, rollback
- Contras: Requiere serialización, más complejo

**Opción 3: Implementación Custom**
```python
# Tabla personalizada
class RequerimientoHistorial(models.Model):
    requerimiento = models.ForeignKey(Requerimiento, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)
    fecha_cambio = models.DateTimeField(auto_now_add=True)
    tipo_cambio = models.CharField(max_length=50)  # CREACION, EDICION, ESTADO, etc.
    campo_modificado = models.CharField(max_length=100, blank=True)
    valor_anterior = models.TextField(blank=True)
    valor_nuevo = models.TextField(blank=True)
    comentario = models.TextField(blank=True)
```
- Pros: Control total, personalizable, eficiente
- Contras: Requiere mantener manualmente, más código

### Estado de Implementación
❌ **NO IMPLEMENTADO**
- No existe modelo de historial
- No hay signals para capturar cambios
- No hay vista de historial
- Los modelos tienen `fecha_creacion` y `fecha_actualizacion` pero no guardan versiones

**Alternativa Temporal:**
- Mostrar solo: `creado_por`, `fecha_creacion`, `fecha_actualizacion`
- Implementar logging básico en `views.py` para registrar cambios
- Usar logs del servidor para auditoría básica

### Prioridad de Implementación
🔴 **ALTA** - La auditoría y trazabilidad son requisitos críticos en sistemas de gestión de requerimientos, especialmente para proyectos regulados o con múltiples stakeholders.

### Observaciones de Revisión
✅ **Correcciones aplicadas:**
- Reconocido que el historial NO está implementado actualmente
- Especificadas opciones de implementación (django-simple-history, django-reversion, custom)
- Definida la información que DEBERÍA registrarse
- Agregada tabla de eventos y datos a capturar
- Añadidos flujos opcionales (comparar versiones, restaurar)
- Especificadas reglas de negocio para auditoría
- Marcado como caso de uso pendiente de implementación con prioridad alta
- Agregada alternativa temporal con campos existentes (fecha_creacion, fecha_actualizacion)

---

## CU-09: Consultar historial de caso de uso

### Descripción
Los usuarios con permisos adecuados pueden consultar el historial completo de cambios realizados sobre un caso de uso específico.

El historial incluye:
- **Cambios en información básica:** nombre, descripción
- **Modificaciones de detalles específicos:**
  - Tradicional: actor principal, precondiciones, flujos, postcondiciones
  - Ágil: historia de usuario, criterios de aceptación, responsable, estado Scrum
- **Vinculaciones/desvinculaciones** con requerimientos
- **Adjuntos** agregados o eliminados
- **Comentarios** registrados
- **Metadatos:** quién realizó el cambio, cuándo, desde qué IP (opcional)

Cada entrada del historial muestra:
- Fecha y hora del cambio
- Usuario que realizó la modificación
- Tipo de cambio (creación, edición de flujos, vinculación, etc.)
- Valores anteriores y nuevos (para campos modificados)
- Comentario opcional sobre el motivo del cambio

Este registro es fundamental para:
- Rastrear evolución del diseño del sistema
- Auditoría de decisiones de arquitectura
- Resolver disputas sobre especificaciones
- Análisis de impacto de cambios
- Cumplimiento de estándares de calidad

### Actores
- **Líder del proyecto** (acceso completo al historial)
- **Desarrollador/Analista** (visualiza historial de casos de uso que puede editar)
- **Stakeholder** (visualiza historial en modo lectura)
- **Administrador** (acceso completo a todos los historiales)

### Precondiciones
- Usuario autenticado con permisos en el proyecto
- Caso de uso existente
- Sistema de auditoría habilitado (django-simple-history, django-reversion, o custom)
- Al menos un cambio registrado en el caso de uso

### Postcondiciones
- Historial mostrado sin modificar datos
- Registro de consulta en logs (opcional)
- Sin cambios en el caso de uso ni su historial

### Flujo Principal
1. El usuario accede a la lista de casos de uso del proyecto
2. El usuario selecciona un caso de uso específico
3. El usuario hace clic en "Ver detalle" o accede directamente a la vista del caso de uso
4. El sistema muestra la pantalla de detalle del caso de uso con pestañas/secciones:
   - Información actual
   - Requerimientos relacionados
   - Adjuntos
   - Comentarios
   - **Historial de cambios**
5. El usuario hace clic en la pestaña "Historial"
6. El sistema recupera todas las versiones históricas del caso de uso:
   - Desde tabla de auditoría (ej: `casos_de_uso_casodeuso_history`)
   - Incluye cambios en tablas relacionadas (detalles tradicional/ágil)
7. El sistema muestra una línea de tiempo cronológica inversa (más reciente primero):
   - Fecha y hora del cambio
   - Avatar/nombre del usuario que realizó el cambio
   - Icono según tipo de acción (creación, edición, vinculación, etc.)
   - Descripción del cambio en lenguaje natural
   - Botón "Ver detalles" para expandir
8. El usuario puede:
   - Revisar la lista completa de cambios
   - Expandir una entrada para ver detalles campo por campo
   - Comparar dos versiones específicas
   - Filtrar por tipo de cambio o rango de fechas
   - Ver cambios en flujos (diff de texto)
9. El usuario hace clic en "Ver detalles" de una entrada
10. El sistema muestra un modal/panel expandido con:
    - Tabla comparativa "Antes → Después"
    - Campos modificados destacados
    - Valores anteriores y nuevos
    - Para flujos: vista diff con líneas agregadas/eliminadas
    - Comentario del usuario (si existe)
11. El usuario revisa los detalles
12. El usuario cierra el modal y puede continuar navegando el historial

### Flujos Alternativos
**6a. Caso de uso sin historial (recién creado)**
- El sistema detecta solo la versión inicial
- Muestra mensaje: "Este caso de uso no tiene historial de cambios aún"
- Muestra solo la entrada de creación con fecha, hora y creador

**6b. Sistema de historial no implementado**
- El sistema detecta ausencia de módulo de auditoría
- Muestra mensaje: "El historial de cambios no está disponible en este momento"
- Muestra solo: fecha de creación, creado por, fecha de última actualización
- Sugiere contactar al administrador para habilitar auditoría

**8a. Historial muy extenso (>100 cambios)**
- El sistema implementa paginación
- Muestra 20 entradas por página
- Incluye navegación: "Anterior / Siguiente"
- Opción de filtrar por rango de fechas para reducir resultados

**9a. Usuario sin permisos para ver detalles completos**
- El sistema valida permisos
- Muestra solo resumen: "Campo [X] modificado por [Usuario] el [Fecha]"
- No muestra valores específicos antiguos/nuevos
- Muestra mensaje: "Permisos limitados: contacte al líder para ver detalles completos"

### Flujo Opcional - Comparar Versiones de Flujos
1. El usuario selecciona dos versiones del historial
2. El usuario hace clic en "Comparar flujos"
3. El sistema muestra vista diff lado a lado:
   - Panel izquierdo: versión antigua del flujo principal
   - Panel derecho: versión nueva del flujo principal
   - Líneas eliminadas marcadas en rojo
   - Líneas agregadas marcadas en verde
   - Líneas modificadas marcadas en amarillo
4. El usuario revisa las diferencias
5. El usuario puede exportar la comparación a PDF

### Flujo Opcional - Restaurar Versión Anterior
1. El usuario visualiza una versión histórica del caso de uso
2. El usuario hace clic en "Restaurar esta versión"
3. El sistema muestra advertencia: "¿Desea restaurar el caso de uso a esta versión? Los cambios actuales se perderán"
4. El usuario confirma
5. El sistema crea una nueva entrada de historial: "Restaurado a versión del [Fecha]"
6. El sistema revierte los campos a los valores de la versión seleccionada
7. El sistema muestra mensaje de confirmación
8. El usuario visualiza el caso de uso restaurado

### Información Registrada en el Historial

| Evento | Datos Capturados |
|--------|------------------|
| **Creación** | Fecha, hora, creado_por, valores iniciales |
| **Edición de campo** | Fecha, hora, modificado_por, campo, valor_anterior, valor_nuevo |
| **Modificación de flujo principal** | Fecha, hora, usuario, diff del texto |
| **Modificación de flujo alternativo** | Fecha, hora, usuario, diff del texto |
| **Cambio de actor principal** | Fecha, hora, usuario, actor_anterior, actor_nuevo |
| **Actualización de precondiciones** | Fecha, hora, usuario, diff del texto |
| **Actualización de postcondiciones** | Fecha, hora, usuario, diff del texto |
| **Vinculación con requerimiento** | Fecha, hora, usuario, requerimiento_id, nota |
| **Desvinculación de requerimiento** | Fecha, hora, usuario, requerimiento_id |
| **Adjunto agregado** | Fecha, hora, usuario, nombre_archivo, tamaño |
| **Adjunto eliminado** | Fecha, hora, usuario, nombre_archivo |
| **Comentario agregado** | Fecha, hora, usuario, texto_comentario (resumen) |

### Reglas de Negocio
- RN-01: El historial es de solo lectura para todos los usuarios
- RN-02: Solo administradores pueden eliminar entradas del historial
- RN-03: El historial se conserva incluso si el caso de uso es eliminado (soft delete)
- RN-04: Los cambios en campos de texto largo (flujos) se registran como diff
- RN-05: Los cambios simultáneos del mismo usuario se agrupan en una transacción
- RN-06: El historial incluye cambios en tablas relacionadas (detalles, vinculaciones)
- RN-07: La fecha/hora se registra en timezone del servidor
- RN-08: Se registra la IP del usuario que realiza el cambio (opcional, configurable)
- RN-09: Los cambios en flujos se muestran con formato diff (líneas +/-)

### Notas Técnicas
**Estado Actual:**
⚠️ **NO IMPLEMENTADO** - El sistema actualmente NO tiene módulo de auditoría/historial

**Opciones de Implementación Recomendadas:**

**Opción 1: django-simple-history**
```python
# En casos_de_uso/models.py
from simple_history.models import HistoricalRecords

class CasoDeUso(models.Model):
    # ... campos existentes ...
    history = HistoricalRecords()

class DetalleCasoDeUsoTradicional(models.Model):
    # ... campos existentes ...
    history = HistoricalRecords()
```
- Pros: Fácil implementación, automático, incluye rollback
- Contras: Tablas adicionales por modelo, overhead de storage

**Opción 2: django-reversion**
```python
# En casos_de_uso/admin.py
from reversion.admin import VersionAdmin
import reversion

@admin.register(CasoDeUso)
class CasoDeUsoAdmin(VersionAdmin):
    pass

# En vistas, para registrar cambios
with reversion.create_revision():
    caso_de_uso.save()
    reversion.set_user(request.user)
    reversion.set_comment("Actualización de flujos")
```
- Pros: Versionado completo, comparación de versiones, rollback
- Contras: Requiere serialización, más complejo

**Opción 3: Implementación Custom con Diff de Texto**
```python
# Tabla personalizada
class CasoDeUsoHistorial(models.Model):
    caso_de_uso = models.ForeignKey(CasoDeUso, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)
    fecha_cambio = models.DateTimeField(auto_now_add=True)
    tipo_cambio = models.CharField(max_length=50)  # CREACION, EDICION_FLUJO, VINCULACION, etc.
    campo_modificado = models.CharField(max_length=100, blank=True)
    valor_anterior = models.TextField(blank=True)
    valor_nuevo = models.TextField(blank=True)
    diff_texto = models.TextField(blank=True)  # Para campos de texto largo
    comentario = models.TextField(blank=True)

# Generar diff para flujos
from difflib import unified_diff

def generar_diff(texto_anterior, texto_nuevo):
    diff = unified_diff(
        texto_anterior.splitlines(keepends=True),
        texto_nuevo.splitlines(keepends=True),
        fromfile='anterior',
        tofile='nuevo'
    )
    return ''.join(diff)
```
- Pros: Control total, personalizable, diff legible
- Contras: Requiere mantener manualmente, más código

### Visualización de Diff para Flujos
```
Flujo Principal - Versión Anterior (15/10/2025):
1. El usuario ingresa al sistema
2. El usuario selecciona "Crear proyecto"
- 3. El sistema solicita nombre del proyecto
4. El usuario completa el formulario
5. El sistema valida los datos

Flujo Principal - Versión Nueva (16/10/2025):
1. El usuario ingresa al sistema
2. El usuario selecciona "Crear proyecto"
+ 3. El sistema verifica permisos del usuario
+ 4. El sistema solicita nombre del proyecto y líder
- 4. El usuario completa el formulario
+ 5. El usuario completa el formulario con líder designado
- 5. El sistema valida los datos
+ 6. El sistema valida los datos y permisos
```

### Estado de Implementación
❌ **NO IMPLEMENTADO**
- No existe modelo de historial
- No hay signals para capturar cambios
- No hay vista de historial
- Los modelos tienen `fecha_creacion` y `fecha_actualizacion` pero no guardan versiones
- No hay sistema de diff para campos de texto largo

**Alternativa Temporal:**
- Mostrar solo: `creado_por`, `fecha_creacion`, `fecha_actualizacion`
- Implementar logging básico en `views.py` para registrar cambios
- Usar logs del servidor para auditoría básica

### Prioridad de Implementación
🔴 **ALTA** - La auditoría de casos de uso es crítica para:
- Cumplimiento de estándares ISO/IEEE
- Trazabilidad de decisiones de diseño
- Gestión de cambios en especificaciones
- Resolución de conflictos entre stakeholders

### Observaciones de Revisión
✅ **Correcciones aplicadas:**
- Reconocido que el historial NO está implementado actualmente
- Especificadas opciones de implementación (django-simple-history, django-reversion, custom)
- Añadida funcionalidad específica de diff para flujos de texto
- Definida la información que DEBERÍA registrarse
- Agregada tabla de eventos y datos a capturar
- Añadidos flujos opcionales (comparar versiones de flujos, restaurar)
- Especificadas reglas de negocio para auditoría de casos de uso
- Incluido ejemplo visual de diff de flujos
- Marcado como caso de uso pendiente de implementación con prioridad alta
- Agregada alternativa temporal con campos existentes

---

## CU-10: Registrar caso de uso

### Descripción
El **analista** o usuario con permisos adecuados registra un nuevo caso de uso en el proyecto. El sistema presenta un formulario con:

**Campos comunes (obligatorios para ambas metodologías):**
- **Nombre:** identificador breve del caso de uso (ej: "CU-01: Autenticar usuario")
- **Descripción:** resumen del propósito del caso de uso

**Campos específicos según metodología:**

**Metodología Tradicional:**
- **Actor principal:** rol o entidad que inicia el caso de uso
- **Precondiciones:** condiciones que deben cumplirse antes de ejecutar el caso de uso
- **Flujo principal:** secuencia de pasos del escenario exitoso (numerado)
- **Flujo alternativo:** escenarios alternativos, excepciones, errores
- **Postcondiciones:** estado del sistema después de ejecutar el caso de uso exitosamente
- **Observaciones:** notas adicionales, restricciones, consideraciones

**Metodología Ágil:**
- **Historia de usuario:** formato "Como [rol], quiero [acción] para [beneficio]"
- **Criterios de aceptación:** condiciones específicas que deben cumplirse para considerar el caso de uso completo
- **Responsable:** miembro del equipo asignado a implementar el caso de uso
- **Estado Scrum:** To Do / In Progress / Done / Blocked
- **Observaciones:** notas adicionales, dependencias

El sistema valida que todos los campos obligatorios estén completos y guarda el caso de uso. Una vez registrado, queda disponible para:
- Consulta y edición
- Vinculación con requerimientos
- Comentarios
- Adjuntar archivos
- Generación de matriz de trazabilidad

### Actores
- **Analista** (rol principal para crear casos de uso)
- **Desarrollador** (puede crear según permisos)
- **Líder** (puede crear y aprobar)

### Precondiciones
- Usuario autenticado con rol de analista, desarrollador o líder en el proyecto
- Proyecto existente con metodología definida (CU-05)
- Acceso a la sección de casos de uso del proyecto

### Postcondiciones
- Caso de uso creado en tabla `casos_de_uso_casodeuso`
- Registro de detalle creado según metodología:
  - `casos_de_uso_detallecasodeusotradicional` (si tradicional)
  - `casos_de_uso_detallecasodeusoagil` (si ágil)
- Caso de uso visible en lista de casos de uso del proyecto
- Campos `creado_por`, `fecha_creacion` poblados automáticamente
- Log de auditoría registrado (si está implementado)

### Flujo Principal
1. El analista accede al proyecto
2. El analista navega a la sección "Casos de Uso"
3. El analista hace clic en "Crear caso de uso"
4. El sistema verifica la metodología del proyecto
5. El sistema muestra el formulario con campos específicos:
   - **Si Tradicional:** campos tradicionales (actor, precondiciones, flujos, postcondiciones)
   - **Si Ágil:** campos ágiles (historia de usuario, criterios de aceptación, responsable, estado)
6. El analista completa los campos obligatorios:
   - Nombre del caso de uso (ej: "CU-03: Crear proyecto")
   - Descripción breve
7. El analista completa los campos específicos de la metodología:
   - **Tradicional:** actor principal, precondiciones, flujo principal (como mínimo)
   - **Ágil:** historia de usuario, criterios de aceptación
8. El analista hace clic en "Guardar"
9. El sistema valida:
   - Campos obligatorios completos
   - Formato de historia de usuario (si ágil)
   - Unicidad del nombre dentro del proyecto
   - Longitud mínima de flujos (si tradicional)
10. El sistema crea el caso de uso:
    - Inserta en `casos_de_uso_casodeuso`
    - Asigna valores comunes (nombre, descripción, proyecto, creado_por)
11. El sistema crea el detalle específico:
    - **Si Tradicional:** inserta en `detallecasodeusotradicional`
    - **Si Ágil:** inserta en `detallecasodeusoagil`
    - Vincula con el caso de uso padre mediante FK
12. El sistema muestra mensaje de éxito: "Caso de uso creado exitosamente"
13. El sistema redirige a la vista de detalle del caso de uso o a la lista

### Flujos Alternativos
**9a. Campos obligatorios incompletos**
- El sistema detecta campos vacíos
- Resalta los campos faltantes en rojo
- Muestra mensaje: "Complete todos los campos obligatorios"
- Mantiene los datos ingresados
- Permite corregir y guardar nuevamente

**9b. Nombre de caso de uso duplicado**
- El sistema detecta nombre existente en el proyecto
- Muestra error: "Ya existe un caso de uso con este nombre en el proyecto"
- Sugiere nombres alternativos o agregar sufijo numérico
- Mantiene los demás datos del formulario
- Permite corregir y reintentar

**9c. Flujo principal muy corto (Tradicional)**
- El sistema valida longitud del flujo principal
- Muestra advertencia: "El flujo principal debería tener al menos 3 pasos"
- Permite guardar de todas formas (es recomendación, no obligatorio)
- Marca el campo con ícono de advertencia

**10a. Error al guardar en base de datos**
- El sistema captura la excepción
- Muestra mensaje: "Error al guardar el caso de uso, intente nuevamente"
- Registra el error en logs con detalles técnicos
- Mantiene los datos del formulario
- Permite reintentar

**7a. Usuario cancela la creación**
- El analista hace clic en "Cancelar"
- El sistema pregunta: "¿Desea descartar los cambios?"
- Si confirma: redirige a lista de casos de uso
- Si cancela: vuelve al formulario

### Flujo Opcional - Guardar como Borrador
1. El analista completa parcialmente el formulario
2. El analista hace clic en "Guardar como borrador"
3. El sistema guarda con indicador de estado "Borrador" o "Incompleto"
4. Permite editar posteriormente para completar
5. Muestra en lista con indicador visual de "Incompleto"
6. No se incluye en reportes hasta que esté completo

### Flujo Opcional - Crear desde Plantilla
1. El analista hace clic en "Crear desde plantilla"
2. El sistema muestra plantillas predefinidas:
   - Autenticación
   - CRUD básico
   - Registro de entidad
   - Consulta/búsqueda
   - Generación de reporte
3. El analista selecciona una plantilla
4. El sistema pre-llena el formulario con estructura estándar
5. El analista personaliza los campos según el caso específico
6. El analista guarda el caso de uso

### Reglas de Negocio
- RN-01: Solo usuarios con rol de analista, desarrollador o líder pueden crear casos de uso
- RN-02: El nombre del caso de uso debe ser único dentro del proyecto
- RN-03: La descripción debe tener al menos 10 caracteres
- RN-04: Los campos específicos de metodología son obligatorios según el tipo:
  - Tradicional: actor principal y flujo principal son obligatorios
  - Ágil: historia de usuario y criterios de aceptación son obligatorios
- RN-05: El creador queda registrado automáticamente (`creado_por`)
- RN-06: La fecha de creación se asigna automáticamente
- RN-07: Los casos de uso sin metodología definida no pueden crearse
- RN-08: Los flujos se numeran automáticamente (1. 2. 3. ...) o el usuario puede numerarlos manualmente

### Validaciones Específicas

**Tradicional:**
- Actor principal no puede estar vacío
- Flujo principal debe tener al menos 20 caracteres (mínimo 3 pasos)
- Precondiciones recomendadas (advertencia si está vacío)
- Postcondiciones recomendadas (advertencia si está vacío)

**Ágil:**
- Historia de usuario debe seguir formato "Como... quiero... para..." (advertencia, no obligatorio)
- Criterios de aceptación deben tener al menos 15 caracteres
- Estado Scrum debe ser uno de: To Do, In Progress, Done, Blocked
- Responsable debe ser un participante del proyecto (validación opcional)

### Formato Recomendado para Flujos (Tradicional)

**Flujo Principal:**
```
1. El usuario ingresa al sistema
2. El usuario hace clic en "Crear proyecto"
3. El sistema muestra el formulario de creación
4. El usuario completa los campos obligatorios
5. El usuario hace clic en "Guardar"
6. El sistema valida los datos
7. El sistema crea el proyecto
8. El sistema muestra mensaje de confirmación
9. El sistema redirige a la lista de proyectos
```

**Flujo Alternativo:**
```
6a. Datos inválidos:
   6a.1. El sistema muestra mensaje de error
   6a.2. El sistema resalta los campos incorrectos
   6a.3. El usuario corrige los datos
   6a.4. Vuelve al paso 5

7a. Error al guardar:
   7a.1. El sistema muestra mensaje de error técnico
   7a.2. El sistema registra el error en logs
   7a.3. El usuario puede reintentar
```

### Ejemplo de Historia de Usuario (Ágil)
```
Como líder del proyecto,
quiero asignar roles específicos a los participantes,
para definir claramente las responsabilidades de cada miembro del equipo.

Criterios de aceptación:
- Puedo ver la lista completa de participantes del proyecto
- Puedo seleccionar un participante y cambiar su rol
- Los roles disponibles son: Desarrollador, Analista, Tester, Stakeholder, Lector
- El cambio se refleja inmediatamente en el sistema
- Solo el líder puede cambiar roles
```

### Notas Técnicas
- Vista propuesta: `casos_de_uso/views.py` → `crear_caso_de_uso`
- Template propuesto: `casos_de_uso/templates/casos_de_uso/caso_de_uso_form.html`
- Formulario: `casos_de_uso/forms.py` → `CasoDeUsoForm`
- Lógica de renderizado condicional según `proyecto.metodologia`
- Los detalles se crean automáticamente en el `save()` del formulario
- Transacción atómica: si falla el detalle, rollback del caso de uso
- Editor de texto enriquecido recomendado para flujos (ej: TinyMCE, CKEditor)
- Numeración automática de pasos en flujos (JavaScript)

### Estado de Implementación
⚠️ **PARCIALMENTE IMPLEMENTADO**
- El modelo `CasoDeUso` existe con detalles tradicional/ágil
- **Falta:** Vista de creación de casos de uso
- **Falta:** Formulario con campos condicionales según metodología
- **Falta:** Validación de campos obligatorios según metodología
- **Falta:** Editor para flujos con numeración automática
- **Falta:** Plantillas predefinidas
- **Falta:** Opción de guardar como borrador

### Prioridad de Implementación
🔴 **ALTA** - Los casos de uso son fundamentales para:
- Diseño de funcionalidades del sistema
- Comunicación con stakeholders
- Trazabilidad con requerimientos (matriz)
- Documentación técnica
- Pruebas de aceptación

### Observaciones de Revisión
✅ **Correcciones aplicadas:**
- Separados claramente los campos comunes vs específicos por metodología
- Especificada la estructura de tablas (casodeuso + detalle tradicional/ágil)
- Añadido formato recomendado para flujos tradicionales
- Añadido ejemplo de historia de usuario ágil con criterios de aceptación
- Clarificadas validaciones específicas por metodología
- Agregadas reglas de negocio sobre unicidad y longitudes mínimas
- Añadidos flujos opcionales (guardar como borrador, crear desde plantilla)
- Especificado comportamiento de transacciones atómicas
- Marcado como parcialmente implementado (modelo existe, vistas faltan)
- Agregada recomendación de editor de texto enriquecido para flujos
- Prioridad alta debido a importancia en diseño de sistema

---

## CU-11: Definir dependencias

### Descripción
El **analista** o **líder** establece y gestiona relaciones de dependencia entre requerimientos y casos de uso, creando la matriz de trazabilidad bidireccional del proyecto.

Las dependencias permiten:
- **Vincular requerimientos con casos de uso:** un requerimiento puede implementarse mediante uno o más casos de uso
- **Vincular casos de uso con requerimientos:** un caso de uso puede satisfacer uno o más requerimientos
- **Trazabilidad bidireccional:** desde un requerimiento ver qué casos de uso lo implementan, y viceversa
- **Análisis de impacto:** identificar qué casos de uso se ven afectados al modificar un requerimiento
- **Validación de cobertura:** detectar requerimientos sin casos de uso (huérfanos) y casos de uso sin requerimientos

El sistema utiliza una **tabla intermedia** (`RequerimientoCaso`) que permite:
- Registrar la fecha de vinculación
- Agregar notas explicativas sobre la relación
- Mantener la integridad referencial (unique constraint)
- Facilitar consultas eficientes en ambas direcciones

### Actores
- **Analista** (define dependencias durante análisis)
- **Líder del proyecto** (revisa y aprueba trazabilidad)
- **Desarrollador** (consulta dependencias para implementación)

### Precondiciones
- Usuario autenticado con permisos en el proyecto
- Proyecto con al menos un requerimiento creado
- Proyecto con al menos un caso de uso creado
- Acceso a la sección de requerimientos o casos de uso

### Postcondiciones
- Relación registrada en tabla `requerimientos_requerimientocaso`
- Vínculo visible desde ambas entidades (requerimiento ↔ caso de uso)
- Campos `fecha_vinculacion` y `nota` poblados
- Matriz de trazabilidad actualizada
- Contadores de cobertura actualizados

### Flujo Principal - Vincular desde Requerimiento
1. El analista accede a la lista de requerimientos del proyecto
2. El analista selecciona un requerimiento específico
3. El analista hace clic en "Ver detalle" del requerimiento
4. El sistema muestra la pantalla de detalle con secciones/pestañas:
   - Información del requerimiento
   - **Casos de uso relacionados** (lista actual)
   - Comentarios
   - Adjuntos
   - Historial
5. El analista hace clic en "Vincular caso de uso" o botón "+"
6. El sistema muestra un modal/panel con:
   - Lista de casos de uso del proyecto
   - Buscador por nombre/descripción
   - Indicador visual de casos ya vinculados (disabled o marcados)
   - Campo "Nota" (opcional) para explicar la relación
7. El analista busca y selecciona uno o más casos de uso
8. El analista opcionalmente agrega una nota explicativa
9. El analista hace clic en "Vincular"
10. El sistema valida:
    - Casos de uso seleccionados pertenecen al mismo proyecto
    - No existe ya una vinculación duplicada
    - Permisos del usuario
11. El sistema crea registros en `RequerimientoCaso`:
    - `requerimiento_id` = ID del requerimiento actual
    - `caso_de_uso_id` = ID del caso de uso seleccionado
    - `fecha_vinculacion` = timestamp actual
    - `nota` = texto ingresado (opcional)
12. El sistema muestra mensaje de éxito: "Caso(s) de uso vinculado(s) exitosamente"
13. El sistema actualiza la lista de casos de uso relacionados
14. El sistema cierra el modal

### Flujo Principal - Vincular desde Caso de Uso
1. El analista accede a la lista de casos de uso del proyecto
2. El analista selecciona un caso de uso específico
3. El analista hace clic en "Ver detalle" del caso de uso
4. El sistema muestra la pantalla de detalle con sección "Requerimientos relacionados"
5. El analista hace clic en "Vincular requerimiento" o botón "+"
6. El sistema muestra un modal/panel con:
   - Lista de requerimientos del proyecto
   - Buscador por nombre/tipo/prioridad
   - Indicador visual de requerimientos ya vinculados
   - Campo "Nota" (opcional)
7. El analista busca y selecciona uno o más requerimientos
8. El analista opcionalmente agrega una nota explicativa
9. El analista hace clic en "Vincular"
10. El sistema valida y crea los registros en `RequerimientoCaso`
11. El sistema muestra mensaje de éxito
12. El sistema actualiza la lista de requerimientos relacionados

### Flujo Principal - Desvincular
1. El usuario accede al detalle de un requerimiento o caso de uso
2. El usuario ve la lista de elementos vinculados
3. El usuario hace clic en el ícono "Eliminar vínculo" (ej: ✕ o 🗑️) junto a un elemento
4. El sistema muestra modal de confirmación:
   - "¿Desea eliminar el vínculo entre [Req X] y [CU Y]?"
   - "Esta acción no eliminará los elementos, solo la relación"
5. El usuario confirma
6. El sistema elimina el registro de `RequerimientoCaso`
7. El sistema muestra mensaje: "Vínculo eliminado"
8. El sistema actualiza la lista de elementos relacionados

### Flujos Alternativos
**10a. Intento de vincular caso de uso de otro proyecto**
- El sistema valida que `caso_de_uso.proyecto_id == requerimiento.proyecto_id`
- Muestra error: "Solo puede vincular casos de uso del mismo proyecto"
- No crea la vinculación
- Permite seleccionar otro caso de uso

**10b. Vínculo duplicado**
- El sistema detecta que ya existe un registro `RequerimientoCaso` con el mismo par
- Muestra mensaje: "Este caso de uso ya está vinculado a este requerimiento"
- No crea duplicado (unique_together evita duplicados en DB)
- Permite seleccionar otro caso de uso

**6a. No hay casos de uso disponibles para vincular**
- El sistema detecta que todos los casos de uso del proyecto ya están vinculados
- Muestra mensaje: "Todos los casos de uso del proyecto ya están vinculados"
- Sugiere crear un nuevo caso de uso
- Permite cerrar el modal

**6b. Proyecto sin casos de uso**
- El sistema detecta que el proyecto no tiene casos de uso creados
- Muestra mensaje: "No hay casos de uso disponibles. Cree al menos un caso de uso primero"
- Muestra botón "Crear caso de uso"
- Permite cancelar

**11a. Error al guardar vinculación**
- El sistema captura la excepción
- Muestra mensaje: "Error al crear el vínculo, intente nuevamente"
- Registra el error en logs
- No crea la vinculación
- Permite reintentar

### Flujo Opcional - Vinculación Masiva
1. El analista accede a la vista "Matriz de trazabilidad"
2. El sistema muestra tabla bidimensional:
   - Filas: requerimientos del proyecto
   - Columnas: casos de uso del proyecto
   - Celdas: checkboxes indicando vinculación
3. El analista marca/desmarca checkboxes para vincular/desvincular
4. El analista hace clic en "Guardar cambios"
5. El sistema procesa todas las vinculaciones en batch
6. El sistema muestra resumen: "X vínculos creados, Y eliminados"

### Flujo Opcional - Sugerencias Automáticas
1. El analista abre el modal de vinculación
2. El sistema analiza el nombre y descripción del requerimiento
3. El sistema busca casos de uso con palabras clave similares
4. El sistema muestra sección "Sugerencias" con casos de uso relevantes
5. El analista puede aceptar sugerencias o buscar manualmente

### Reglas de Negocio
- RN-01: Un requerimiento puede vincularse con múltiples casos de uso (relación N:M)
- RN-02: Un caso de uso puede vincularse con múltiples requerimientos (relación N:M)
- RN-03: Solo se pueden vincular elementos del mismo proyecto
- RN-04: No se permiten vínculos duplicados (unique_together en DB)
- RN-05: La vinculación es bidireccional (visible desde ambos lados)
- RN-06: Al eliminar un requerimiento o caso de uso, se eliminan sus vinculaciones (cascade)
- RN-07: El campo `nota` es opcional y puede editarse posteriormente
- RN-08: La fecha de vinculación se registra automáticamente y no puede modificarse
- RN-09: Solo usuarios con permisos de edición pueden crear/eliminar vínculos
- RN-10: Los vínculos son independientes del estado del requerimiento o caso de uso

### Modelo de Datos Actual

```python
# En requerimientos/models.py
class Requerimiento(models.Model):
    # ... campos base ...
    casos_relacionados = models.ManyToManyField(
        'casos_de_uso.CasoDeUso',
        through='RequerimientoCaso',
        blank=True,
        related_name='requerimientos_relacionados'
    )

class RequerimientoCaso(models.Model):
    """Tabla intermedia para relación N:M entre Requerimiento y CasoDeUso"""
    requerimiento = models.ForeignKey(
        Requerimiento,
        on_delete=models.CASCADE,
        related_name='relaciones_casos'
    )
    caso_de_uso = models.ForeignKey(
        'casos_de_uso.CasoDeUso',
        on_delete=models.CASCADE,
        related_name='relaciones_requerimientos'
    )
    fecha_vinculacion = models.DateTimeField(auto_now_add=True)
    nota = models.CharField(max_length=255, blank=True)

    class Meta:
        unique_together = ('requerimiento', 'caso_de_uso')

    def __str__(self):
        return f"Req {self.requerimiento.pk} <-> CU {self.caso_de_uso.pk}"
```

### Consultas de Trazabilidad

**Desde Requerimiento a Casos de Uso:**
```python
requerimiento = Requerimiento.objects.get(pk=1)
casos_vinculados = requerimiento.casos_relacionados.all()
# O con detalles de la relación
relaciones = requerimiento.relaciones_casos.select_related('caso_de_uso')
for rel in relaciones:
    print(f"CU: {rel.caso_de_uso.nombre}, Nota: {rel.nota}")
```

**Desde Caso de Uso a Requerimientos:**
```python
caso_de_uso = CasoDeUso.objects.get(pk=1)
reqs_vinculados = caso_de_uso.requerimientos_relacionados.all()
# O con detalles de la relación
relaciones = caso_de_uso.relaciones_requerimientos.select_related('requerimiento')
```

**Requerimientos sin casos de uso (huérfanos):**
```python
reqs_huerfanos = Requerimiento.objects.filter(
    proyecto=proyecto,
    casos_relacionados__isnull=True
)
```

**Casos de uso sin requerimientos (huérfanos):**
```python
casos_huerfanos = CasoDeUso.objects.filter(
    proyecto=proyecto,
    requerimientos_relacionados__isnull=True
)
```

### Notas Técnicas
**Estado Actual:**
✅ **MODELO IMPLEMENTADO** - La tabla intermedia `RequerimientoCaso` existe

⚠️ **VISTAS PENDIENTES:**
- No existe vista para vincular/desvincular desde UI
- No existe modal de selección de casos de uso
- No existe modal de selección de requerimientos
- La vinculación actualmente solo puede hacerse desde admin de Django

**Implementación Recomendada:**

**Vista para vincular:**
```python
# En requerimientos/views.py o casos_de_uso/views.py
@login_required
def vincular_caso_uso(request, requerimiento_id):
    requerimiento = get_object_or_404(Requerimiento, pk=requerimiento_id)
    
    if request.method == 'POST':
        casos_ids = request.POST.getlist('casos_de_uso')
        nota = request.POST.get('nota', '')
        
        for caso_id in casos_ids:
            caso = CasoDeUso.objects.get(pk=caso_id)
            RequerimientoCaso.objects.get_or_create(
                requerimiento=requerimiento,
                caso_de_uso=caso,
                defaults={'nota': nota}
            )
        
        return JsonResponse({'success': True})
    
    # GET: mostrar casos de uso disponibles
    casos_disponibles = CasoDeUso.objects.filter(
        proyecto=requerimiento.proyecto
    ).exclude(
        pk__in=requerimiento.casos_relacionados.values_list('pk', flat=True)
    )
    
    return render(request, 'requerimientos/vincular_modal.html', {
        'requerimiento': requerimiento,
        'casos_disponibles': casos_disponibles
    })
```

**Template modal:**
```html
<!-- requerimientos/templates/requerimientos/vincular_modal.html -->
<div class="modal-body">
    <h5>Vincular casos de uso a: {{ requerimiento.nombre }}</h5>
    <input type="text" id="buscar-caso" placeholder="Buscar caso de uso...">
    <ul class="casos-list">
        {% for caso in casos_disponibles %}
        <li>
            <input type="checkbox" name="casos_de_uso" value="{{ caso.pk }}">
            <label>{{ caso.nombre }}</label>
        </li>
        {% endfor %}
    </ul>
    <textarea name="nota" placeholder="Nota explicativa (opcional)"></textarea>
    <button type="submit">Vincular</button>
</div>
```

### Estado de Implementación
✅ **Modelo implementado** - `RequerimientoCaso` existe en DB

❌ **Vistas NO implementadas:**
- Vista de vinculación desde requerimiento
- Vista de vinculación desde caso de uso
- Modal de selección
- Funcionalidad de desvincular
- Búsqueda de elementos disponibles
- Vinculación masiva desde matriz

⚠️ **Parcialmente visible:**
- Dashboard muestra matriz de trazabilidad básica (solo lectura)
- Código en `dashboards/views.py` genera matriz simple por coincidencia de nombres

### Prioridad de Implementación
🔴 **ALTA** - La trazabilidad es un requisito fundamental en gestión de requerimientos:
- Permite validar cobertura completa
- Facilita análisis de impacto de cambios
- Cumple con estándares de calidad (IEEE 830, ISO 29148)
- Esencial para auditorías y certificaciones

### Observaciones de Revisión
✅ **Correcciones aplicadas:**
- Reconocido que el modelo existe pero las vistas NO
- Especificada la tabla intermedia `RequerimientoCaso` con sus campos
- Agregados flujos para vincular desde requerimiento Y desde caso de uso
- Añadido flujo de desvinculación con confirmación
- Especificadas consultas ORM para trazabilidad bidireccional
- Agregadas consultas para detectar huérfanos (reqs sin casos, casos sin reqs)
- Incluidos flujos opcionales (vinculación masiva, sugerencias automáticas)
- Agregado código de implementación recomendada para vistas
- Clarificado que actualmente solo se puede vincular desde admin de Django
- Marcada como prioridad alta para implementar UI completa

---

## CU-12: Agrupar requerimientos

### Descripción
El **analista** o **líder** organiza y agrupa requerimientos según la metodología del proyecto para facilitar la planificación y seguimiento:

**Metodología Tradicional:**
- Agrupar por **categoría:** Sistema, Interfaz, Rendimiento, Seguridad, Base de datos, Integración, etc.
- Agrupar por **módulo/subsistema:** Autenticación, Gestión de usuarios, Reportes, etc.
- Agrupar por **prioridad MoSCoW:** Must have, Should have, Could have, Won't have
- Agrupar por **fase del proyecto:** Fase 1, Fase 2, Release 1.0, Release 2.0, etc.

**Metodología Ágil:**
- Agrupar por **Sprint:** Sprint 1, Sprint 2, ..., Sprint N
- Agrupar por **Epic/Historia épica:** grandes bloques de funcionalidad
- Agrupar por **Feature/Característica:** conjuntos de historias de usuario relacionadas
- Agrupar por **Estado Scrum:** To Do, In Progress, Done, Blocked

La agrupación permite:
- **Visualización organizada** del backlog
- **Planificación por fases** o iteraciones
- **Estimación de esfuerzo** por grupo
- **Asignación de responsables** por categoría
- **Reportes segmentados** por agrupación
- **Filtrado rápido** en listados

### Actores
- **Analista** (organiza requerimientos por categoría/módulo)
- **Líder del proyecto** (agrupa por sprint/fase, asigna prioridades)
- **Desarrollador** (consulta agrupaciones para planificación)

### Precondiciones
- Usuario autenticado con permisos en el proyecto
- Proyecto con metodología definida (Tradicional o Ágil)
- Al menos un requerimiento creado en el proyecto
- Acceso a la sección de requerimientos

### Postcondiciones
- Campo de agrupación actualizado en requerimientos:
  - Tradicional: `DetalleRequerimientoTradicional.categoria`
  - Ágil: `DetalleRequerimientoAgil.sprint_asignado`
- Requerimientos organizados visualmente por grupos
- Filtros y vistas agrupadas disponibles
- Estadísticas por grupo actualizadas

### Flujo Principal - Agrupar en Metodología Tradicional
1. El analista accede a la lista de requerimientos del proyecto
2. El analista hace clic en "Gestionar categorías" o "Agrupar"
3. El sistema muestra vista de agrupación con:
   - Lista de requerimientos del proyecto
   - Selectores de categoría por cada requerimiento
   - Opciones de categoría predefinidas:
     - Sistema
     - Interfaz de usuario
     - Rendimiento
     - Seguridad
     - Base de datos
     - Integración/API
     - Documentación
     - Testing
     - Otros
   - Opción de crear categoría personalizada
4. El analista selecciona la categoría para cada requerimiento
5. El analista puede usar "Asignación masiva":
   - Selecciona múltiples requerimientos (checkboxes)
   - Elige categoría común
   - Aplica a todos los seleccionados
6. El analista hace clic en "Guardar cambios"
7. El sistema valida las categorías seleccionadas
8. El sistema actualiza el campo `categoria` en `DetalleRequerimientoTradicional`
9. El sistema muestra mensaje: "Categorías actualizadas exitosamente"
10. El sistema reordena la lista agrupada por categoría

### Flujo Principal - Agrupar en Metodología Ágil
1. El líder accede a la lista de requerimientos del proyecto
2. El líder hace clic en "Planificar sprints" o "Agrupar por sprint"
3. El sistema muestra vista de planificación de sprints con:
   - Lista de sprints del proyecto (ej: Sprint 1, Sprint 2, ...)
   - Backlog de requerimientos sin asignar
   - Drag & drop para mover requerimientos a sprints
   - Contador de puntos de historia por sprint
4. El líder arrastra requerimientos desde el backlog a un sprint específico
5. El sistema calcula automáticamente:
   - Total de puntos estimados por sprint
   - Advertencia si se excede la capacidad del equipo
   - Número de historias por sprint
6. El líder puede crear un nuevo sprint:
   - Hace clic en "Nuevo sprint"
   - Ingresa nombre (ej: "Sprint 3")
   - Define duración y capacidad (opcional)
7. El líder hace clic en "Guardar planificación"
8. El sistema actualiza el campo `sprint_asignado` en `DetalleRequerimientoAgil`
9. El sistema muestra mensaje: "Planificación de sprints guardada"
10. El sistema actualiza vista Kanban/Scrum board

### Flujo Principal - Crear Grupo Personalizado
1. El usuario hace clic en "Crear nueva categoría" o "Nuevo sprint"
2. El sistema muestra formulario modal:
   - Nombre del grupo
   - Descripción (opcional)
   - Color de etiqueta (opcional)
   - Ícono (opcional)
3. El usuario completa el nombre
4. El usuario hace clic en "Crear"
5. El sistema valida unicidad del nombre
6. El sistema registra el nuevo grupo
7. El sistema muestra el nuevo grupo en las opciones
8. El usuario puede asignar requerimientos al nuevo grupo

### Flujos Alternativos
**7a. Categoría no válida**
- El sistema detecta categoría vacía o inválida
- Muestra advertencia: "Algunos requerimientos no tienen categoría asignada"
- Permite guardar de todas formas
- Marca requerimientos sin categoría como "Sin clasificar"

**5a. Capacidad del sprint excedida (Ágil)**
- El sistema detecta que puntos de historia exceden capacidad
- Muestra advertencia: "Sprint X tiene Y puntos, capacidad máxima Z"
- Sugiere mover algunos requerimientos a otro sprint
- Permite confirmar de todas formas (es advertencia, no bloqueante)

**8a. Error al guardar agrupación**
- El sistema captura la excepción
- Muestra mensaje: "Error al guardar cambios, intente nuevamente"
- Registra el error en logs
- No actualiza ningún campo
- Permite reintentar

**5b. Nombre de grupo duplicado**
- El sistema detecta nombre existente
- Muestra error: "Ya existe una categoría/sprint con ese nombre"
- Sugiere agregar sufijo (ej: "Sprint 2 - Correcciones")
- Permite corregir y reintentar

### Flujo Opcional - Vista Agrupada
1. El usuario accede a la lista de requerimientos
2. El usuario activa filtro "Agrupar por"
3. El usuario selecciona criterio de agrupación:
   - Categoría (Tradicional)
   - Sprint (Ágil)
   - Prioridad
   - Estado
   - Responsable
4. El sistema reorganiza la vista en secciones colapsables
5. Cada sección muestra:
   - Nombre del grupo
   - Cantidad de requerimientos
   - Total de puntos estimados (si aplica)
   - Lista de requerimientos del grupo
6. El usuario puede expandir/colapsar grupos

### Flujo Opcional - Vista Kanban por Sprint (Ágil)
1. El líder accede a "Vista de sprints"
2. El sistema muestra columnas por sprint:
   - Backlog (sin sprint asignado)
   - Sprint 1
   - Sprint 2
   - Sprint 3
   - ...
3. Cada columna muestra tarjetas de requerimientos
4. El líder arrastra tarjetas entre columnas
5. El sistema actualiza `sprint_asignado` automáticamente

### Reglas de Negocio
- RN-01: Un requerimiento solo puede pertenecer a un grupo a la vez
- RN-02: La agrupación es opcional (requerimientos pueden estar sin grupo)
- RN-03: Los nombres de grupos deben ser únicos dentro del proyecto
- RN-04: En metodología tradicional: el campo `categoria` es texto libre
- RN-05: En metodología ágil: el campo `sprint_asignado` es texto libre
- RN-06: Los grupos pueden crearse dinámicamente (no hay tabla separada)
- RN-07: Al cambiar de metodología, las agrupaciones previas se conservan
- RN-08: Solo líder y analista pueden modificar agrupaciones
- RN-09: Los requerimientos sin grupo aparecen en sección "Sin clasificar"
- RN-10: Las estadísticas se calculan en tiempo real por grupo

### Estructura de Datos Actual

**Metodología Tradicional:**
```python
class DetalleRequerimientoTradicional(models.Model):
    # ... otros campos ...
    categoria = models.CharField(max_length=100, blank=True)
    # Ejemplos de valores: "Sistema", "Interfaz", "Rendimiento", "Seguridad"
```

**Metodología Ágil:**
```python
class DetalleRequerimientoAgil(models.Model):
    # ... otros campos ...
    sprint_asignado = models.CharField(max_length=100, blank=True)
    # Ejemplos de valores: "Sprint 1", "Sprint 2", "Backlog"
```

### Categorías Predefinidas Recomendadas (Tradicional)

| Categoría | Descripción | Ejemplos |
|-----------|-------------|----------|
| **Sistema** | Funcionalidades core del sistema | Lógica de negocio, procesamiento |
| **Interfaz** | Elementos de UI/UX | Pantallas, formularios, navegación |
| **Rendimiento** | Requisitos de performance | Tiempo de respuesta, concurrencia |
| **Seguridad** | Autenticación, autorización, cifrado | Login, permisos, auditoría |
| **Base de datos** | Persistencia y consultas | Modelos, migraciones, queries |
| **Integración** | APIs, servicios externos | REST, OAuth, webhooks |
| **Documentación** | Manuales, ayuda | Guías de usuario, API docs |
| **Testing** | Pruebas y QA | Casos de prueba, cobertura |

### Consultas por Agrupación

**Requerimientos por categoría (Tradicional):**
```python
# Obtener todas las categorías únicas
categorias = DetalleRequerimientoTradicional.objects.filter(
    requerimiento_padre__proyecto=proyecto
).values_list('categoria', flat=True).distinct()

# Requerimientos por categoría específica
reqs_sistema = Requerimiento.objects.filter(
    proyecto=proyecto,
    detalle_tradicional__categoria='Sistema'
)

# Contar por categoría
from django.db.models import Count
stats = Requerimiento.objects.filter(
    proyecto=proyecto
).values('detalle_tradicional__categoria').annotate(
    total=Count('id')
)
```

**Requerimientos por sprint (Ágil):**
```python
# Obtener todos los sprints únicos
sprints = DetalleRequerimientoAgil.objects.filter(
    requerimiento_padre__proyecto=proyecto
).values_list('sprint_asignado', flat=True).distinct()

# Requerimientos de un sprint específico
reqs_sprint1 = Requerimiento.objects.filter(
    proyecto=proyecto,
    detalle_agil__sprint_asignado='Sprint 1'
)

# Puntos por sprint
from django.db.models import Sum
puntos_por_sprint = Requerimiento.objects.filter(
    proyecto=proyecto
).values('detalle_agil__sprint_asignado').annotate(
    total_puntos=Sum('detalle_agil__puntos_estimados')
)
```

### Notas Técnicas
**Estado Actual:**
✅ **CAMPOS IMPLEMENTADOS** - `categoria` y `sprint_asignado` existen en modelos

❌ **VISTAS NO IMPLEMENTADAS:**
- No existe vista de gestión de categorías
- No existe vista de planificación de sprints
- No existe drag & drop para organizar sprints
- No existe vista Kanban por sprint
- No hay selector masivo de categorías
- No hay filtros agrupados en listados

**Implementación Actual:**
- Los campos existen pero solo son editables desde admin de Django
- No hay UI para asignar categoría/sprint desde formulario de requerimiento
- No hay validación de categorías predefinidas
- No hay sugerencias de categorías/sprints existentes

**Implementación Recomendada:**

1. **Agregar selector en formulario de requerimiento:**
```python
# En requerimientos/forms.py
class RequerimientoForm(forms.ModelForm):
    categoria = forms.ChoiceField(
        choices=[],  # Se llena dinámicamente
        required=False
    )
    
    def __init__(self, *args, **kwargs):
        proyecto = kwargs.pop('proyecto', None)
        super().__init__(*args, **kwargs)
        
        if proyecto and proyecto.metodologia == 'TRADICIONAL':
            # Cargar categorías existentes del proyecto
            categorias_existentes = DetalleRequerimientoTradicional.objects.filter(
                requerimiento_padre__proyecto=proyecto
            ).values_list('categoria', flat=True).distinct()
            
            choices = [('', 'Sin categoría')]
            choices += [(c, c) for c in categorias_existentes if c]
            choices += [('__nueva__', '+ Crear nueva categoría')]
            
            self.fields['categoria'].choices = choices
```

2. **Vista de planificación de sprints:**
```python
@login_required
def planificar_sprints(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, pk=proyecto_id)
    
    # Obtener sprints únicos
    sprints = DetalleRequerimientoAgil.objects.filter(
        requerimiento_padre__proyecto=proyecto
    ).values_list('sprint_asignado', flat=True).distinct()
    
    # Backlog: requerimientos sin sprint
    backlog = Requerimiento.objects.filter(
        proyecto=proyecto,
        detalle_agil__sprint_asignado__isnull=True
    )
    
    # Requerimientos por sprint
    reqs_por_sprint = {}
    for sprint in sprints:
        reqs_por_sprint[sprint] = Requerimiento.objects.filter(
            proyecto=proyecto,
            detalle_agil__sprint_asignado=sprint
        )
    
    return render(request, 'requerimientos/planificar_sprints.html', {
        'proyecto': proyecto,
        'sprints': sprints,
        'backlog': backlog,
        'reqs_por_sprint': reqs_por_sprint
    })
```

### Estado de Implementación
✅ **Modelo** - Campos `categoria` y `sprint_asignado` existen

❌ **UI NO implementada:**
- Vista de gestión de categorías
- Selector de categoría en formulario
- Planificación de sprints
- Drag & drop Kanban
- Filtros agrupados
- Estadísticas por grupo

⚠️ **Alternativa actual:**
- Edición manual de campos desde admin
- Categorías/sprints como texto libre (sin validación)

### Prioridad de Implementación
🟡 **MEDIA** - Importante para organización pero no bloqueante:
- Mejora la planificación y seguimiento
- Facilita reportes segmentados
- Esencial para metodología ágil (sprints)
- Puede implementarse gradualmente (primero selector, luego Kanban)

### Observaciones de Revisión
✅ **Correcciones aplicadas:**
- Reconocido que los campos existen pero NO hay UI de gestión
- Separado claramente el comportamiento para metodología Tradicional vs Ágil
- Especificadas categorías predefinidas recomendadas para tradicional
- Agregado flujo de planificación de sprints para ágil
- Incluidas consultas ORM para obtener grupos únicos y estadísticas
- Añadido flujo opcional de vista Kanban por sprint
- Agregado código de implementación recomendada
- Clarificado que actualmente solo es editable desde admin
- Especificadas reglas de negocio sobre unicidad y opcionalidad
- Marcada como prioridad media (importante pero no crítica)

---

## CU-13: Adjuntar archivo al requerimiento

### Descripción
Los usuarios con permisos adecuados pueden adjuntar archivos a un requerimiento para complementar su documentación con:
- **Diagramas:** mockups, wireframes, diagramas de flujo, UML
- **Especificaciones:** documentos Word/PDF con detalles técnicos
- **Imágenes:** capturas de pantalla, ejemplos visuales, referencias
- **Hojas de cálculo:** tablas de datos, cálculos, estimaciones
- **Archivos de diseño:** Figma exports, Sketch files, Adobe XD
- **Videos:** demos, tutoriales, explicaciones

Los adjuntos permiten:
- **Enriquecer la especificación** del requerimiento con material visual
- **Centralizar documentación** relacionada
- **Facilitar comunicación** con stakeholders no técnicos
- **Preservar versiones** de diseños y prototipos
- **Aportar evidencia** para validación y aprobación

El sistema valida:
- Tipos de archivo permitidos (seguridad)
- Tamaño máximo por archivo
- Cuota de almacenamiento del proyecto

### Actores
- **Analista** (adjunta especificaciones técnicas)
- **Diseñador UI/UX** (adjunta mockups, wireframes)
- **Stakeholder** (adjunta documentos de referencia)
- **Líder del proyecto** (adjunta cualquier tipo de documento)

### Precondiciones
- Usuario autenticado con permisos en el proyecto
- Requerimiento existente
- Archivo a subir cumple con restricciones (tipo, tamaño)
- Espacio disponible en el servidor

### Postcondiciones
- Archivo almacenado en sistema de archivos del servidor
- Registro creado vinculando archivo con requerimiento
- Archivo visible en la sección "Adjuntos" del requerimiento
- Metadatos del archivo guardados (nombre, tamaño, tipo, fecha, usuario)
- Cuota de almacenamiento del proyecto actualizada

### Flujo Principal
1. El usuario accede al detalle de un requerimiento
2. El usuario hace clic en la pestaña o sección "Adjuntos"
3. El sistema muestra:
   - Lista de archivos adjuntos existentes (si hay)
   - Botón "Adjuntar archivo" o "Subir archivo"
   - Información de límites (tamaño máx, tipos permitidos)
4. El usuario hace clic en "Adjuntar archivo"
5. El sistema muestra diálogo de selección de archivos
6. El usuario selecciona uno o más archivos desde su dispositivo
7. El usuario opcionalmente agrega:
   - Descripción del archivo
   - Etiquetas/tags
   - Categoría (Diseño, Especificación, Referencia, etc.)
8. El usuario hace clic en "Subir"
9. El sistema valida:
   - Tipo de archivo permitido (extensión y MIME type)
   - Tamaño no excede el límite (ej: 10MB por archivo)
   - Nombre de archivo válido (sin caracteres especiales peligrosos)
   - Espacio disponible en servidor
10. El sistema procesa cada archivo:
    - Genera nombre único para evitar colisiones (UUID + extensión)
    - Almacena en directorio específico (ej: `media/requerimientos/adjuntos/`)
    - Crea registro en tabla de adjuntos:
      - `requerimiento_id`
      - `archivo` (ruta del archivo)
      - `nombre_original`
      - `tamaño` (bytes)
      - `tipo_mime`
      - `descripcion`
      - `subido_por`
      - `fecha_subida`
11. El sistema muestra barra de progreso durante la subida
12. El sistema muestra mensaje de éxito: "Archivo(s) adjuntado(s) exitosamente"
13. El sistema actualiza la lista de adjuntos
14. El sistema muestra el nuevo archivo con opciones:
    - Ver/Descargar
    - Eliminar (si tiene permisos)

### Flujos Alternativos
**9a. Tipo de archivo no permitido**
- El sistema detecta extensión no válida
- Muestra error: "El archivo [nombre] no es válido. Tipos permitidos: PDF, PNG, JPG, DOCX, XLSX, ZIP"
- No sube el archivo
- Permite seleccionar otro archivo
- Muestra lista de tipos permitidos

**9b. Archivo excede tamaño máximo**
- El sistema detecta tamaño > límite (ej: > 10MB)
- Muestra error: "El archivo [nombre] es muy grande. Tamaño máximo: 10MB"
- Muestra tamaño actual del archivo
- Sugiere comprimir o dividir el archivo
- No sube el archivo

**9c. Nombre de archivo con caracteres peligrosos**
- El sistema detecta caracteres no permitidos (ej: `../`, `<script>`)
- Sanitiza el nombre automáticamente
- Reemplaza caracteres especiales por guiones bajos
- Muestra advertencia: "Nombre de archivo modificado para seguridad"
- Continúa con la subida

**10a. Espacio insuficiente en servidor**
- El sistema detecta que no hay espacio disponible
- Muestra error: "Espacio insuficiente en el servidor"
- Notifica al administrador
- Sugiere eliminar archivos antiguos o contactar soporte
- No sube el archivo

**10b. Error durante la subida**
- El sistema captura excepción (conexión interrumpida, permisos, etc.)
- Muestra error: "Error al subir el archivo, intente nuevamente"
- Registra el error en logs
- Limpia archivos parciales si existen
- Permite reintentar

**6a. Usuario cancela la selección**
- El usuario cierra el diálogo sin seleccionar archivos
- El sistema no realiza ninguna acción
- Vuelve a la vista de adjuntos

### Flujo Principal - Descargar Archivo
1. El usuario ve la lista de adjuntos del requerimiento
2. El usuario hace clic en el nombre del archivo o botón "Descargar"
3. El sistema verifica permisos del usuario
4. El sistema registra la descarga en logs
5. El sistema sirve el archivo con headers apropiados:
   - `Content-Disposition: attachment; filename="nombre_original.pdf"`
   - `Content-Type: application/pdf` (según tipo)
6. El navegador del usuario descarga el archivo

### Flujo Principal - Eliminar Archivo
1. El usuario hace clic en el botón "Eliminar" junto a un adjunto
2. El sistema muestra modal de confirmación:
   - "¿Está seguro de eliminar el archivo [nombre]?"
   - "Esta acción no se puede deshacer"
3. El usuario confirma
4. El sistema valida permisos:
   - Solo el usuario que subió el archivo puede eliminarlo
   - O usuarios con rol de líder/administrador
5. El sistema elimina el registro de la base de datos
6. El sistema elimina el archivo físico del servidor
7. El sistema muestra mensaje: "Archivo eliminado"
8. El sistema actualiza la lista de adjuntos

### Reglas de Negocio
- RN-01: Solo usuarios con permisos de edición pueden adjuntar archivos
- RN-02: Tipos de archivo permitidos (configurables):
  - Imágenes: PNG, JPG, JPEG, GIF, SVG
  - Documentos: PDF, DOCX, DOC, XLSX, XLS, TXT
  - Comprimidos: ZIP, RAR
  - Diseño: FIG (Figma), SKETCH, XD
  - Videos: MP4, WEBM (limitados por tamaño)
- RN-03: Tamaño máximo por archivo: 10MB (configurable)
- RN-04: Número máximo de adjuntos por requerimiento: ilimitado (pero sujeto a cuota)
- RN-05: Los nombres de archivo se sanitizan automáticamente
- RN-06: Los archivos se almacenan con nombre único (UUID) pero conservan nombre original en metadata
- RN-07: Solo el usuario que subió el archivo o líder/admin pueden eliminarlo
- RN-08: Al eliminar un requerimiento, sus adjuntos se eliminan también (cascade)
- RN-09: Los adjuntos se sirven con `X-Sendfile` o similar para eficiencia
- RN-10: Se registra log de subidas/descargas/eliminaciones

### Modelo de Datos Propuesto

```python
# En requerimientos/models.py
class AdjuntoRequerimiento(models.Model):
    requerimiento = models.ForeignKey(
        Requerimiento,
        on_delete=models.CASCADE,
        related_name='adjuntos'
    )
    archivo = models.FileField(
        upload_to='requerimientos/adjuntos/%Y/%m/',
        max_length=255
    )
    nombre_original = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)
    tamaño = models.PositiveIntegerField()  # en bytes
    tipo_mime = models.CharField(max_length=100)
    categoria = models.CharField(
        max_length=50,
        choices=[
            ('DISEÑO', 'Diseño/Mockup'),
            ('ESPECIFICACION', 'Especificación'),
            ('REFERENCIA', 'Referencia'),
            ('EVIDENCIA', 'Evidencia'),
            ('OTRO', 'Otro')
        ],
        default='OTRO'
    )
    subido_por = models.ForeignKey(
        'accounts.Usuario',
        on_delete=models.SET_NULL,
        null=True
    )
    fecha_subida = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-fecha_subida']
    
    def __str__(self):
        return f"{self.nombre_original} - {self.requerimiento.nombre}"
    
    def tamaño_legible(self):
        """Retorna tamaño en formato legible (KB, MB)"""
        if self.tamaño < 1024:
            return f"{self.tamaño} bytes"
        elif self.tamaño < 1024 * 1024:
            return f"{self.tamaño / 1024:.1f} KB"
        else:
            return f"{self.tamaño / (1024 * 1024):.1f} MB"
    
    def extension(self):
        """Retorna la extensión del archivo"""
        return self.nombre_original.split('.')[-1].upper()
```

### Validación de Archivos

```python
# En requerimientos/validators.py
import os
from django.core.exceptions import ValidationError

TIPOS_PERMITIDOS = {
    'image/png': '.png',
    'image/jpeg': '.jpg',
    'image/gif': '.gif',
    'application/pdf': '.pdf',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': '.docx',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': '.xlsx',
    'application/zip': '.zip',
}

MAX_TAMAÑO = 10 * 1024 * 1024  # 10MB

def validar_archivo(archivo):
    """Valida tipo y tamaño de archivo"""
    # Validar tamaño
    if archivo.size > MAX_TAMAÑO:
        raise ValidationError(f'El archivo es muy grande. Máximo: 10MB')
    
    # Validar tipo MIME
    if archivo.content_type not in TIPOS_PERMITIDOS:
        raise ValidationError(f'Tipo de archivo no permitido: {archivo.content_type}')
    
    # Validar extensión
    ext = os.path.splitext(archivo.name)[1].lower()
    if ext not in TIPOS_PERMITIDOS.values():
        raise ValidationError(f'Extensión no permitida: {ext}')
    
    return True

def sanitizar_nombre(nombre):
    """Sanitiza nombre de archivo para seguridad"""
    import re
    # Remover caracteres peligrosos
    nombre = re.sub(r'[^\w\s.-]', '_', nombre)
    # Limitar longitud
    if len(nombre) > 100:
        nombre = nombre[:100]
    return nombre
```

### Vista de Subida

```python
# En requerimientos/views.py
from django.core.files.storage import default_storage
import uuid

@login_required
def adjuntar_archivo(request, requerimiento_id):
    requerimiento = get_object_or_404(Requerimiento, pk=requerimiento_id)
    
    # Validar permisos
    if not request.user.tiene_permiso('editar_requerimiento', requerimiento.proyecto):
        return JsonResponse({'error': 'Sin permisos'}, status=403)
    
    if request.method == 'POST' and request.FILES:
        archivo = request.FILES['archivo']
        descripcion = request.POST.get('descripcion', '')
        categoria = request.POST.get('categoria', 'OTRO')
        
        try:
            # Validar archivo
            validar_archivo(archivo)
            
            # Sanitizar nombre
            nombre_original = sanitizar_nombre(archivo.name)
            
            # Crear adjunto
            adjunto = AdjuntoRequerimiento.objects.create(
                requerimiento=requerimiento,
                archivo=archivo,
                nombre_original=nombre_original,
                descripcion=descripcion,
                tamaño=archivo.size,
                tipo_mime=archivo.content_type,
                categoria=categoria,
                subido_por=request.user
            )
            
            return JsonResponse({
                'success': True,
                'adjunto': {
                    'id': adjunto.id,
                    'nombre': adjunto.nombre_original,
                    'tamaño': adjunto.tamaño_legible(),
                    'fecha': adjunto.fecha_subida.strftime('%d/%m/%Y %H:%M')
                }
            })
        
        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)
```

### Notas Técnicas
**Estado Actual:**
❌ **NO IMPLEMENTADO** - No existe modelo de adjuntos ni funcionalidad de subida

**Falta implementar:**
- Modelo `AdjuntoRequerimiento`
- Vista de subida de archivos
- Vista de descarga segura
- Vista de eliminación
- Template con zona de drag & drop
- Validadores de tipo y tamaño
- Sanitización de nombres
- Gestión de cuota de almacenamiento

**Consideraciones de Implementación:**
1. **Seguridad:** Validar tipo MIME Y extensión (doble check)
2. **Performance:** Usar `X-Sendfile` o similar para servir archivos grandes
3. **Escalabilidad:** Considerar almacenamiento en S3/Azure Blob para producción
4. **UX:** Implementar drag & drop, preview de imágenes, barra de progreso
5. **Organización:** Subdirectorios por año/mes en `upload_to`

### Estado de Implementación
❌ **NO IMPLEMENTADO** - Funcionalidad completa pendiente

**Requiere:**
1. Crear modelo `AdjuntoRequerimiento`
2. Crear migración
3. Implementar vistas de upload/download/delete
4. Crear templates con drag & drop
5. Agregar validadores
6. Configurar permisos
7. Implementar mismo sistema para casos de uso (CU-14)

### Prioridad de Implementación
🟡 **MEDIA-ALTA** - Importante para documentación completa:
- Mejora significativa en especificación de requerimientos
- Facilita comunicación con stakeholders
- Permite adjuntar evidencia visual
- Común en sistemas profesionales de gestión de requerimientos
- Puede implementarse gradualmente (primero requerimientos, luego casos de uso)

### Observaciones de Revisión
✅ **Correcciones aplicadas:**
- Reconocido que NO está implementado
- Propuesto modelo completo con metadatos
- Especificadas validaciones de seguridad (tipo MIME + extensión)
- Agregados validadores y sanitización de nombres
- Incluida vista de ejemplo con manejo de errores
- Definidas reglas de negocio sobre permisos y límites
- Listados tipos de archivo permitidos
- Añadido flujo de descarga y eliminación
- Especificadas consideraciones de seguridad y escalabilidad
- Marcada como prioridad media-alta (importante pero no crítica)
- Sugerido almacenamiento cloud para producción (S3, Azure Blob)

---

## CU-14: Adjuntar archivo al caso de uso

### Descripción
Los usuarios con permisos adecuados pueden adjuntar archivos a un caso de uso para complementar su documentación con:
- **Diagramas de flujo:** representaciones visuales del flujo principal y alternativo
- **Diagramas UML:** diagramas de secuencia, actividad, estados
- **Mockups/Wireframes:** diseños de interfaz asociados al caso de uso
- **Prototipos:** demos interactivos, videos de flujos de usuario
- **Especificaciones detalladas:** documentos PDF/Word con detalles técnicos
- **Capturas de pantalla:** ejemplos de interfaces, validaciones, mensajes

Los adjuntos permiten:
- **Enriquecer la especificación** del caso de uso con material visual
- **Documentar escenarios complejos** con diagramas de flujo
- **Facilitar comprensión** para desarrolladores y testers
- **Preservar diseños** y prototipos asociados
- **Aportar evidencia** para validación y aceptación

El sistema valida los mismos criterios que para adjuntos de requerimientos:
- Tipos de archivo permitidos (seguridad)
- Tamaño máximo por archivo
- Cuota de almacenamiento del proyecto

### Actores
- **Analista** (adjunta diagramas UML, especificaciones)
- **Diseñador UI/UX** (adjunta mockups, wireframes, prototipos)
- **Desarrollador** (adjunta diagramas de secuencia, arquitectura)
- **Líder del proyecto** (adjunta cualquier tipo de documento)

### Precondiciones
- Usuario autenticado con permisos en el proyecto
- Caso de uso existente
- Archivo a subir cumple con restricciones (tipo, tamaño)
- Espacio disponible en el servidor

### Postcondiciones
- Archivo almacenado en sistema de archivos del servidor
- Registro creado vinculando archivo con caso de uso
- Archivo visible en la sección "Adjuntos" del caso de uso
- Metadatos del archivo guardados (nombre, tamaño, tipo, fecha, usuario)
- Cuota de almacenamiento del proyecto actualizada

### Flujo Principal
1. El usuario accede al detalle de un caso de uso
2. El usuario hace clic en la pestaña o sección "Adjuntos"
3. El sistema muestra:
   - Lista de archivos adjuntos existentes (si hay)
   - Botón "Adjuntar archivo" o "Subir archivo"
   - Información de límites (tamaño máx, tipos permitidos)
4. El usuario hace clic en "Adjuntar archivo"
5. El sistema muestra diálogo de selección de archivos
6. El usuario selecciona uno o más archivos desde su dispositivo
7. El usuario opcionalmente agrega:
   - Descripción del archivo
   - Etiquetas/tags
   - Categoría (Diagrama de flujo, UML, Mockup, Prototipo, Especificación, etc.)
8. El usuario hace clic en "Subir"
9. El sistema valida:
   - Tipo de archivo permitido (extensión y MIME type)
   - Tamaño no excede el límite (ej: 10MB por archivo)
   - Nombre de archivo válido (sin caracteres especiales peligrosos)
   - Espacio disponible en servidor
10. El sistema procesa cada archivo:
    - Genera nombre único para evitar colisiones (UUID + extensión)
    - Almacena en directorio específico (ej: `media/casos_de_uso/adjuntos/`)
    - Crea registro en tabla de adjuntos:
      - `caso_de_uso_id`
      - `archivo` (ruta del archivo)
      - `nombre_original`
      - `tamaño` (bytes)
      - `tipo_mime`
      - `descripcion`
      - `categoria`
      - `subido_por`
      - `fecha_subida`
11. El sistema muestra barra de progreso durante la subida
12. El sistema muestra mensaje de éxito: "Archivo(s) adjuntado(s) exitosamente"
13. El sistema actualiza la lista de adjuntos
14. El sistema muestra el nuevo archivo con opciones:
    - Ver/Descargar
    - Preview (para imágenes)
    - Eliminar (si tiene permisos)

### Flujos Alternativos
**9a. Tipo de archivo no permitido**
- El sistema detecta extensión no válida
- Muestra error: "El archivo [nombre] no es válido. Tipos permitidos: PDF, PNG, JPG, SVG, DOCX, XLSX, ZIP"
- No sube el archivo
- Permite seleccionar otro archivo

**9b. Archivo excede tamaño máximo**
- El sistema detecta tamaño > límite (ej: > 10MB)
- Muestra error: "El archivo [nombre] es muy grande. Tamaño máximo: 10MB"
- Muestra tamaño actual del archivo
- Sugiere comprimir o dividir el archivo
- No sube el archivo

**9c. Nombre de archivo con caracteres peligrosos**
- El sistema detecta caracteres no permitidos (ej: `../`, `<script>`)
- Sanitiza el nombre automáticamente
- Reemplaza caracteres especiales por guiones bajos
- Muestra advertencia: "Nombre de archivo modificado para seguridad"
- Continúa con la subida

**10a. Espacio insuficiente en servidor**
- El sistema detecta que no hay espacio disponible
- Muestra error: "Espacio insuficiente en el servidor"
- Notifica al administrador
- Sugiere eliminar archivos antiguos o contactar soporte
- No sube el archivo

**10b. Error durante la subida**
- El sistema captura excepción (conexión interrumpida, permisos, etc.)
- Muestra error: "Error al subir el archivo, intente nuevamente"
- Registra el error en logs
- Limpia archivos parciales si existen
- Permite reintentar

### Flujo Principal - Descargar Archivo
1. El usuario ve la lista de adjuntos del caso de uso
2. El usuario hace clic en el nombre del archivo o botón "Descargar"
3. El sistema verifica permisos del usuario
4. El sistema registra la descarga en logs
5. El sistema sirve el archivo con headers apropiados
6. El navegador del usuario descarga el archivo

### Flujo Principal - Eliminar Archivo
1. El usuario hace clic en el botón "Eliminar" junto a un adjunto
2. El sistema muestra modal de confirmación:
   - "¿Está seguro de eliminar el archivo [nombre]?"
   - "Esta acción no se puede deshacer"
3. El usuario confirma
4. El sistema valida permisos:
   - Solo el usuario que subió el archivo puede eliminarlo
   - O usuarios con rol de líder/administrador
5. El sistema elimina el registro de la base de datos
6. El sistema elimina el archivo físico del servidor
7. El sistema muestra mensaje: "Archivo eliminado"
8. El sistema actualiza la lista de adjuntos

### Flujo Opcional - Preview de Imágenes/Diagramas
1. El usuario hace clic en una imagen adjunta (PNG, JPG, SVG)
2. El sistema muestra modal con preview de la imagen a tamaño completo
3. El usuario puede:
   - Hacer zoom
   - Descargar la imagen
   - Ver siguiente/anterior imagen
4. El usuario cierra el modal

### Reglas de Negocio
- RN-01: Solo usuarios con permisos de edición pueden adjuntar archivos
- RN-02: Tipos de archivo permitidos (configurables):
  - Imágenes: PNG, JPG, JPEG, GIF, SVG
  - Documentos: PDF, DOCX, DOC, XLSX, XLS, TXT
  - Diagramas: VSDX (Visio), DRAWIO, SVG
  - Comprimidos: ZIP, RAR
  - Prototipos: FIG (Figma), SKETCH, XD
  - Videos: MP4, WEBM (limitados por tamaño)
- RN-03: Tamaño máximo por archivo: 10MB (configurable)
- RN-04: Número máximo de adjuntos por caso de uso: ilimitado (sujeto a cuota)
- RN-05: Los nombres de archivo se sanitizan automáticamente
- RN-06: Los archivos se almacenan con nombre único (UUID) pero conservan nombre original
- RN-07: Solo el usuario que subió el archivo o líder/admin pueden eliminarlo
- RN-08: Al eliminar un caso de uso, sus adjuntos se eliminan también (cascade)
- RN-09: Los archivos SVG se renderizan inline para preview
- RN-10: Se registra log de subidas/descargas/eliminaciones

### Modelo de Datos Propuesto

```python
# En casos_de_uso/models.py
class AdjuntoCasoDeUso(models.Model):
    caso_de_uso = models.ForeignKey(
        CasoDeUso,
        on_delete=models.CASCADE,
        related_name='adjuntos'
    )
    archivo = models.FileField(
        upload_to='casos_de_uso/adjuntos/%Y/%m/',
        max_length=255
    )
    nombre_original = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)
    tamaño = models.PositiveIntegerField()  # en bytes
    tipo_mime = models.CharField(max_length=100)
    categoria = models.CharField(
        max_length=50,
        choices=[
            ('DIAGRAMA_FLUJO', 'Diagrama de flujo'),
            ('DIAGRAMA_UML', 'Diagrama UML'),
            ('MOCKUP', 'Mockup/Wireframe'),
            ('PROTOTIPO', 'Prototipo'),
            ('ESPECIFICACION', 'Especificación'),
            ('CAPTURA', 'Captura de pantalla'),
            ('OTRO', 'Otro')
        ],
        default='OTRO'
    )
    subido_por = models.ForeignKey(
        'accounts.Usuario',
        on_delete=models.SET_NULL,
        null=True
    )
    fecha_subida = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-fecha_subida']
    
    def __str__(self):
        return f"{self.nombre_original} - {self.caso_de_uso.nombre}"
    
    def tamaño_legible(self):
        """Retorna tamaño en formato legible (KB, MB)"""
        if self.tamaño < 1024:
            return f"{self.tamaño} bytes"
        elif self.tamaño < 1024 * 1024:
            return f"{self.tamaño / 1024:.1f} KB"
        else:
            return f"{self.tamaño / (1024 * 1024):.1f} MB"
    
    def extension(self):
        """Retorna la extensión del archivo"""
        return self.nombre_original.split('.')[-1].upper()
    
    def es_imagen(self):
        """Verifica si es una imagen para mostrar preview"""
        ext = self.extension().lower()
        return ext in ['png', 'jpg', 'jpeg', 'gif', 'svg']
```

### Diferencias con CU-13 (Adjuntos de Requerimientos)

| Aspecto | Requerimientos | Casos de Uso |
|---------|---------------|--------------|
| **Tipos comunes** | Especificaciones, documentos de negocio | Diagramas de flujo, UML, mockups |
| **Categorías** | Diseño, Especificación, Referencia, Evidencia | Diagrama flujo, UML, Mockup, Prototipo |
| **Directorio storage** | `media/requerimientos/adjuntos/` | `media/casos_de_uso/adjuntos/` |
| **Preview inline** | PDF, imágenes | SVG (diagramas), imágenes |
| **Uso principal** | Documentar requisitos de negocio | Documentar diseño e implementación |

### Notas Técnicas
**Estado Actual:**
❌ **NO IMPLEMENTADO** - No existe modelo de adjuntos ni funcionalidad de subida

**Falta implementar:**
- Modelo `AdjuntoCasoDeUso`
- Vista de subida de archivos
- Vista de descarga segura
- Vista de eliminación
- Template con zona de drag & drop
- Validadores de tipo y tamaño (reutilizar de CU-13)
- Sanitización de nombres (reutilizar de CU-13)
- Preview de imágenes/SVG inline

**Implementación Recomendada:**
- Reutilizar validadores y lógica de subida de CU-13
- Crear mixin o clase base para adjuntos (DRY)
- Implementar junto con CU-13 para consistencia

```python
# Clase base para reutilización
class AdjuntoBase(models.Model):
    archivo = models.FileField(max_length=255)
    nombre_original = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)
    tamaño = models.PositiveIntegerField()
    tipo_mime = models.CharField(max_length=100)
    subido_por = models.ForeignKey('accounts.Usuario', on_delete=models.SET_NULL, null=True)
    fecha_subida = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        abstract = True
    
    def tamaño_legible(self):
        # ... implementación común
    
    def extension(self):
        # ... implementación común

class AdjuntoRequerimiento(AdjuntoBase):
    requerimiento = models.ForeignKey(Requerimiento, on_delete=models.CASCADE, related_name='adjuntos')
    categoria = models.CharField(...)  # Categorías específicas

class AdjuntoCasoDeUso(AdjuntoBase):
    caso_de_uso = models.ForeignKey(CasoDeUso, on_delete=models.CASCADE, related_name='adjuntos')
    categoria = models.CharField(...)  # Categorías específicas
```

### Estado de Implementación
❌ **NO IMPLEMENTADO** - Funcionalidad completa pendiente

**Requiere (mismo que CU-13):**
1. Crear modelo `AdjuntoCasoDeUso`
2. Crear migración
3. Implementar vistas de upload/download/delete
4. Crear templates con drag & drop
5. Agregar validadores (reutilizar CU-13)
6. Configurar permisos
7. Implementar preview inline para SVG/imágenes

### Prioridad de Implementación
🟡 **MEDIA-ALTA** - Misma prioridad que CU-13:
- Mejora significativa en especificación de casos de uso
- Permite adjuntar diagramas de flujo (esencial para casos de uso)
- Facilita comunicación visual del diseño
- Debe implementarse junto con CU-13 para consistencia
- Reutilización de código reduce esfuerzo

### Observaciones de Revisión
✅ **Correcciones aplicadas:**
- Reconocido que NO está implementado (igual que CU-13)
- Propuesto modelo similar a `AdjuntoRequerimiento` con categorías específicas
- Especificadas categorías apropiadas para casos de uso (Diagrama flujo, UML, Mockup)
- Agregado flujo de preview inline para SVG/imágenes
- Incluida tabla comparativa con adjuntos de requerimientos
- Propuesta clase base abstracta para reutilización (DRY)
- Especificado que debe implementarse junto con CU-13
- Mismas validaciones de seguridad que CU-13
- Marcada como prioridad media-alta
- Énfasis en diagramas visuales (flujos, UML) característicos de casos de uso

---

## CU-15: Generar matriz de trazabilidad

### Descripción
El sistema genera automáticamente una **matriz de trazabilidad bidireccional** que muestra las relaciones entre requerimientos y casos de uso del proyecto.

La matriz permite:
- **Visualizar cobertura:** qué requerimientos están implementados por casos de uso
- **Detectar huérfanos:** requerimientos sin casos de uso y viceversa
- **Análisis de impacto:** identificar qué casos de uso se ven afectados al modificar un requerimiento
- **Validación de completitud:** verificar que todos los requerimientos tienen al menos un caso de uso
- **Comunicación con stakeholders:** presentar visualmente la trazabilidad del proyecto
- **Auditoría y cumplimiento:** demostrar cobertura completa para certificaciones

**Formatos de salida:**
- **Vista web interactiva:** tabla HTML con filtros, búsqueda, expandir/colapsar
- **Exportación PDF:** documento imprimible con matriz completa
- **Exportación Excel:** hoja de cálculo editable con múltiples hojas
- **Exportación CSV:** datos crudos para análisis personalizado

**Tipos de matriz:**
- **Matriz completa:** todos los requerimientos vs todos los casos de uso (tabla NxM)
- **Matriz compacta:** solo relaciones existentes (lista de pares)
- **Matriz agrupada:** organizada por categoría/sprint/prioridad
- **Matriz inversa:** casos de uso vs requerimientos (perspectiva opuesta)

### Actores
- **Líder del proyecto** (genera matriz para revisión y planificación)
- **Analista** (valida cobertura y trazabilidad)
- **Stakeholder** (consulta estado de implementación de requerimientos)
- **Auditor/QA** (verifica completitud para certificación)

### Precondiciones
- Proyecto existente con metodología definida
- Al menos un requerimiento creado
- Al menos un caso de uso creado
- Usuario autenticado con permisos en el proyecto

### Postcondiciones
- Matriz generada y mostrada en pantalla
- Archivo exportado (si se solicitó exportación)
- Estadísticas de cobertura calculadas
- Registro de generación en logs (opcional)

### Flujo Principal - Vista Web Interactiva
1. El usuario accede al proyecto
2. El usuario navega a la sección "Trazabilidad" o "Matriz"
3. El usuario hace clic en "Generar matriz de trazabilidad"
4. El sistema muestra opciones de configuración:
   - Tipo de vista (Completa / Compacta / Agrupada)
   - Filtros (por prioridad, estado, categoría, sprint)
   - Ordenamiento (por ID, nombre, prioridad)
5. El usuario selecciona las opciones deseadas
6. El usuario hace clic en "Generar"
7. El sistema recupera datos del proyecto:
   - Todos los requerimientos con sus detalles
   - Todos los casos de uso con sus detalles
   - Todas las relaciones `RequerimientoCaso`
8. El sistema construye la matriz según el tipo seleccionado:
   - **Completa:** tabla NxM con checkboxes/iconos indicando relación
   - **Compacta:** lista de pares requerimiento-caso de uso vinculados
   - **Agrupada:** secciones por categoría/sprint con relaciones
9. El sistema calcula estadísticas:
   - Total de requerimientos
   - Total de casos de uso
   - Requerimientos con al menos un caso de uso (cobertura)
   - Requerimientos sin casos de uso (huérfanos)
   - Casos de uso con al menos un requerimiento
   - Casos de uso sin requerimientos (huérfanos)
   - Porcentaje de cobertura: `(reqs_con_casos / total_reqs) * 100`
10. El sistema muestra la matriz con:
    - Encabezados: nombres de requerimientos (filas) y casos de uso (columnas)
    - Celdas: ✓ o ✗ indicando si existe relación
    - Tooltips: mostrar detalles al pasar el mouse
    - Links: hacer clic en nombre para ver detalle
    - Panel de estadísticas en la parte superior
11. El usuario puede:
    - Filtrar filas/columnas
    - Buscar por nombre
    - Expandir/colapsar grupos
    - Hacer clic en celdas para ver detalles de la relación
    - Exportar a PDF/Excel/CSV

### Flujo Principal - Exportar a PDF
1. El usuario visualiza la matriz web
2. El usuario hace clic en "Exportar a PDF"
3. El sistema muestra opciones de exportación:
   - Incluir estadísticas
   - Incluir solo relaciones existentes (compacta)
   - Orientación (horizontal/vertical)
   - Tamaño de papel (A4/Carta/Legal)
4. El usuario selecciona opciones y confirma
5. El sistema genera documento PDF:
   - Encabezado con nombre del proyecto, fecha, generado por
   - Tabla de estadísticas de cobertura
   - Matriz de trazabilidad (tabla)
   - Leyenda explicativa
   - Pie de página con número de página
6. El sistema descarga el PDF: `Matriz_Trazabilidad_[Proyecto]_[Fecha].pdf`
7. El sistema muestra mensaje: "PDF generado exitosamente"

### Flujo Principal - Exportar a Excel
1. El usuario visualiza la matriz web
2. El usuario hace clic en "Exportar a Excel"
3. El sistema genera archivo Excel (.xlsx) con múltiples hojas:
   - **Hoja 1 "Resumen":** estadísticas de cobertura, gráficos
   - **Hoja 2 "Matriz Completa":** tabla NxM con requerimientos vs casos de uso
   - **Hoja 3 "Relaciones":** lista de pares vinculados con detalles
   - **Hoja 4 "Requerimientos Huérfanos":** requerimientos sin casos de uso
   - **Hoja 5 "Casos Huérfanos":** casos de uso sin requerimientos
4. El sistema aplica formato:
   - Celdas con relación: fondo verde, ✓
   - Celdas sin relación: fondo blanco, vacío
   - Encabezados: negrita, fondo gris
   - Filtros automáticos habilitados
5. El sistema descarga el Excel: `Matriz_Trazabilidad_[Proyecto]_[Fecha].xlsx`
6. El sistema muestra mensaje: "Excel generado exitosamente"

### Flujo Principal - Exportar a CSV
1. El usuario hace clic en "Exportar a CSV"
2. El sistema genera archivo CSV con columnas:
   - Requerimiento_ID
   - Requerimiento_Nombre
   - Requerimiento_Tipo
   - Requerimiento_Prioridad
   - CasoDeUso_ID
   - CasoDeUso_Nombre
   - Fecha_Vinculacion
   - Nota
3. El sistema descarga el CSV: `Trazabilidad_[Proyecto]_[Fecha].csv`
4. El usuario puede importar el CSV en Excel, Tableau, Power BI, etc.

### Flujos Alternativos
**7a. Proyecto sin requerimientos**
- El sistema detecta lista vacía
- Muestra mensaje: "No hay requerimientos en el proyecto. Cree al menos un requerimiento primero"
- Muestra botón "Crear requerimiento"
- No genera matriz

**7b. Proyecto sin casos de uso**
- El sistema detecta lista vacía
- Muestra mensaje: "No hay casos de uso en el proyecto. Cree al menos un caso de uso primero"
- Muestra botón "Crear caso de uso"
- No genera matriz

**9a. Todos los requerimientos sin casos de uso (cobertura 0%)**
- El sistema genera matriz vacía (sin relaciones)
- Muestra advertencia destacada: "⚠️ Cobertura 0%: Ningún requerimiento tiene casos de uso vinculados"
- Muestra lista de requerimientos huérfanos
- Sugiere "Crear casos de uso y vincularlos"

**9b. Matriz muy grande (>100 requerimientos o >100 casos de uso)**
- El sistema detecta matriz grande
- Muestra advertencia: "La matriz es muy grande y puede tardar en cargar"
- Sugiere usar filtros o vista compacta
- Permite cancelar o continuar
- Si continúa: muestra barra de progreso

**6a. Error al generar PDF/Excel**
- El sistema captura excepción (librería no instalada, permisos, espacio)
- Muestra error: "Error al generar el archivo, intente nuevamente"
- Registra el error en logs
- Permite reintentar
- Sugiere contactar al administrador si persiste

### Flujo Opcional - Matriz Interactiva con Edición
1. El usuario visualiza la matriz web
2. El usuario hace clic en una celda vacía (sin relación)
3. El sistema muestra tooltip: "Hacer clic para vincular"
4. El usuario hace clic
5. El sistema crea la vinculación inmediatamente
6. El sistema actualiza la celda con ✓
7. El sistema actualiza estadísticas de cobertura
8. El usuario puede desvincular haciendo clic en celda con ✓

### Flujo Opcional - Vista Agrupada por Sprint/Categoría
1. El usuario selecciona "Vista agrupada por sprint"
2. El sistema reorganiza la matriz en secciones:
   - Sprint 1
     - Requerimientos del Sprint 1 vs sus casos de uso
   - Sprint 2
     - Requerimientos del Sprint 2 vs sus casos de uso
   - Backlog
     - Requerimientos sin sprint vs casos de uso
3. Muestra estadísticas por grupo

### Reglas de Negocio
- RN-01: La matriz se genera en tiempo real (no se guarda en DB)
- RN-02: Solo usuarios con permisos de lectura pueden generar la matriz
- RN-03: La matriz muestra todas las relaciones existentes en `RequerimientoCaso`
- RN-04: Los requerimientos huérfanos se destacan visualmente (color rojo/amarillo)
- RN-05: Los casos de uso huérfanos se destacan visualmente
- RN-06: El porcentaje de cobertura debe ser ≥80% para proyectos en producción (recomendación)
- RN-07: Las exportaciones incluyen fecha y hora de generación
- RN-08: Las exportaciones incluyen nombre del usuario que las generó
- RN-09: La matriz respeta los permisos del usuario (solo muestra elementos que puede ver)
- RN-10: Las estadísticas se calculan dinámicamente cada vez

### Cálculo de Cobertura

```python
# Estadísticas de trazabilidad
total_requerimientos = Requerimiento.objects.filter(proyecto=proyecto).count()
total_casos_de_uso = CasoDeUso.objects.filter(proyecto=proyecto).count()

# Requerimientos con al menos un caso de uso
reqs_con_casos = Requerimiento.objects.filter(
    proyecto=proyecto,
    relaciones_casos__isnull=False
).distinct().count()

# Casos de uso con al menos un requerimiento
casos_con_reqs = CasoDeUso.objects.filter(
    proyecto=proyecto,
    relaciones_requerimientos__isnull=False
).distinct().count()

# Huérfanos
reqs_huerfanos = Requerimiento.objects.filter(
    proyecto=proyecto
).annotate(
    rel_count=Count('relaciones_casos')
).filter(rel_count=0)

casos_huerfanos = CasoDeUso.objects.filter(
    proyecto=proyecto
).annotate(
    rel_count=Count('relaciones_requerimientos')
).filter(rel_count=0)

# Porcentajes
cobertura_reqs = (reqs_con_casos / total_requerimientos * 100) if total_requerimientos > 0 else 0
cobertura_casos = (casos_con_reqs / total_casos_de_uso * 100) if total_casos_de_uso > 0 else 0
```

### Estructura de Matriz (Vista Web)

```html
<!-- Ejemplo de tabla matriz -->
<table class="matriz-trazabilidad">
  <thead>
    <tr>
      <th>Requerimiento / Caso de Uso</th>
      <th>CU-01: Autenticar</th>
      <th>CU-02: Crear proyecto</th>
      <th>CU-03: Editar proyecto</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>REQ-01: Login OAuth2</strong></td>
      <td class="vinculado">✓</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td><strong>REQ-02: Gestión proyectos</strong></td>
      <td></td>
      <td class="vinculado">✓</td>
      <td class="vinculado">✓</td>
    </tr>
    <tr class="huerfano">
      <td><strong>REQ-03: Notificaciones</strong></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
  </tbody>
</table>

<!-- Estadísticas -->
<div class="estadisticas">
  <div class="stat">
    <span class="valor">15</span>
    <span class="label">Requerimientos</span>
  </div>
  <div class="stat">
    <span class="valor">22</span>
    <span class="label">Casos de Uso</span>
  </div>
  <div class="stat success">
    <span class="valor">87%</span>
    <span class="label">Cobertura</span>
  </div>
  <div class="stat warning">
    <span class="valor">2</span>
    <span class="label">Huérfanos</span>
  </div>
</div>
```

### Notas Técnicas
**Estado Actual:**
⚠️ **PARCIALMENTE IMPLEMENTADO** - Existe vista básica en dashboard

**Implementado:**
- Vista básica de matriz en `dashboards/views.py` → `admin_proyecto_detail`
- Cálculo de huérfanos con `annotate` y `Count`
- Visualización simple en template

```python
# En dashboards/views.py (líneas 107-116)
reqs_huerfanos = requerimientos.annotate(rel_count=Count('relaciones_casos')).filter(rel_count=0)
casos_huerfanos = casos.annotate(rel_count=Count('relaciones_requerimientos')).filter(rel_count=0)

# Construcción de matriz simple (por coincidencia de nombres)
matriz = []
for req in requerimientos:
    relacionados = [cu for cu in casos if req.nombre.split()[0].lower() in cu.nombre.lower() or req.nombre.lower() in cu.descripcion.lower()]
    matriz.append({'req': req, 'casos': relacionados})
```

**Falta implementar:**
- Matriz completa NxM con TODAS las relaciones (no solo por nombre)
- Exportación a PDF
- Exportación a Excel
- Exportación a CSV
- Filtros avanzados
- Vista agrupada por categoría/sprint
- Edición inline (vincular/desvincular desde matriz)
- Gráficos de cobertura
- Vista compacta (solo relaciones existentes)

**Mejoras Necesarias:**
1. **Usar relaciones reales en lugar de coincidencia de nombres:**
```python
# Correcto: usar relaciones de la tabla intermedia
matriz = []
for req in requerimientos:
    casos_vinculados = req.casos_relacionados.all()  # Relación M2M real
    matriz.append({
        'req': req,
        'casos': casos_vinculados
    })
```

2. **Generar matriz completa NxM:**
```python
def generar_matriz_completa(proyecto):
    requerimientos = Requerimiento.objects.filter(proyecto=proyecto)
    casos_de_uso = CasoDeUso.objects.filter(proyecto=proyecto)
    
    matriz = []
    for req in requerimientos:
        fila = {'requerimiento': req, 'relaciones': {}}
        for caso in casos_de_uso:
            # Verificar si existe relación
            existe = RequerimientoCaso.objects.filter(
                requerimiento=req,
                caso_de_uso=caso
            ).exists()
            fila['relaciones'][caso.id] = existe
        matriz.append(fila)
    
    return {
        'matriz': matriz,
        'casos_de_uso': casos_de_uso,
        'estadisticas': calcular_estadisticas(proyecto)
    }
```

3. **Exportación a PDF con ReportLab:**
```python
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

def exportar_matriz_pdf(proyecto):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(A4))
    
    # Construir datos de tabla
    requerimientos = Requerimiento.objects.filter(proyecto=proyecto)
    casos_de_uso = CasoDeUso.objects.filter(proyecto=proyecto)
    
    # Encabezados
    data = [['Requerimiento'] + [cu.nombre for cu in casos_de_uso]]
    
    # Filas
    for req in requerimientos:
        fila = [req.nombre]
        for caso in casos_de_uso:
            existe = req.casos_relacionados.filter(id=caso.id).exists()
            fila.append('✓' if existe else '')
        data.append(fila)
    
    # Crear tabla
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    doc.build([table])
    buffer.seek(0)
    return buffer
```

4. **Exportación a Excel con openpyxl:**
```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment

def exportar_matriz_excel(proyecto):
    wb = Workbook()
    
    # Hoja 1: Matriz completa
    ws1 = wb.active
    ws1.title = "Matriz Completa"
    
    requerimientos = Requerimiento.objects.filter(proyecto=proyecto)
    casos_de_uso = CasoDeUso.objects.filter(proyecto=proyecto)
    
    # Encabezados
    ws1.cell(1, 1, "Requerimiento")
    for idx, caso in enumerate(casos_de_uso, start=2):
        ws1.cell(1, idx, caso.nombre)
        ws1.cell(1, idx).font = Font(bold=True)
    
    # Filas
    for row_idx, req in enumerate(requerimientos, start=2):
        ws1.cell(row_idx, 1, req.nombre)
        for col_idx, caso in enumerate(casos_de_uso, start=2):
            existe = req.casos_relacionados.filter(id=caso.id).exists()
            cell = ws1.cell(row_idx, col_idx, '✓' if existe else '')
            if existe:
                cell.fill = PatternFill(start_color="90EE90", end_color="90EE90", fill_type="solid")
    
    # Hoja 2: Huérfanos
    ws2 = wb.create_sheet("Huérfanos")
    # ... agregar requerimientos y casos huérfanos
    
    return wb
```

### Estado de Implementación
⚠️ **PARCIALMENTE IMPLEMENTADO**

**✅ Implementado:**
- Vista básica de matriz en dashboard (coincidencia de nombres - NO CORRECTO)
- Cálculo de huérfanos

**❌ NO implementado:**
- Matriz completa NxM con relaciones reales
- Exportación a PDF
- Exportación a Excel
- Exportación a CSV
- Filtros avanzados
- Vista agrupada
- Gráficos de cobertura
- Edición inline

### Prioridad de Implementación
🔴 **ALTA** - Funcionalidad crítica:
- La matriz de trazabilidad es fundamental en gestión de requerimientos
- Requerida para auditorías y certificaciones (ISO, IEEE)
- Permite validar cobertura completa
- Facilita análisis de impacto de cambios
- La implementación actual usa coincidencia de nombres (INCORRECTO)
- Debe corregirse para usar relaciones reales de `RequerimientoCaso`

### Observaciones de Revisión
✅ **Correcciones aplicadas:**
- Reconocido que existe implementación básica PERO usa coincidencia de nombres (incorrecto)
- Especificado que debe usar relaciones reales de `RequerimientoCaso`
- Agregados flujos para exportación PDF/Excel/CSV
- Incluido cálculo de estadísticas de cobertura
- Especificadas reglas de negocio sobre cobertura mínima (80%)
- Agregado código corregido para generar matriz real
- Incluido ejemplo de exportación PDF con ReportLab
- Incluido ejemplo de exportación Excel con openpyxl
- Añadidos flujos opcionales (edición inline, vista agrupada)
- Estructura HTML de ejemplo para matriz web
- Marcada como prioridad alta por ser funcionalidad crítica
- **CRÍTICO:** La implementación actual NO usa las relaciones de la tabla intermedia

---

## CU-16: Listar casos de uso sin requerimiento

### Descripción
El sistema identifica y lista todos los **casos de uso huérfanos** del proyecto, es decir, casos de uso que no están vinculados a ningún requerimiento.

Esta funcionalidad permite:
- **Detectar casos de uso "huérfanos":** casos implementados sin justificación de requerimiento
- **Validar cobertura inversa:** asegurar que todo lo que se diseña tiene un propósito definido
- **Limpieza de especificaciones:** identificar casos de uso obsoletos o innecesarios
- **Auditoría de trazabilidad:** verificar que cada caso de uso satisface al menos un requerimiento
- **Priorización de vinculación:** facilitar el trabajo de vincular casos huérfanos

Los casos de uso sin requerimientos pueden indicar:
- Casos de uso creados prematuramente (antes del requerimiento)
- Casos de uso técnicos/infraestructura sin requerimiento funcional explícito
- Casos de uso obsoletos que ya no se necesitan
- Casos de uso mal documentados que requieren revisión

### Actores
- **Analista** (revisa y vincula casos de uso huérfanos)
- **Líder del proyecto** (valida cobertura y prioriza vinculaciones)
- **Auditor/QA** (verifica que no haya casos huérfanos en producción)

### Precondiciones
- Proyecto existente
- Al menos un caso de uso creado
- Usuario autenticado con permisos en el proyecto

### Postcondiciones
- Lista de casos de uso huérfanos mostrada
- Sin cambios en la base de datos (solo consulta)
- Estadísticas actualizadas

### Flujo Principal
1. El usuario accede al proyecto
2. El usuario navega a la sección "Trazabilidad" o "Casos de Uso"
3. El usuario hace clic en "Ver casos huérfanos" o filtro "Sin requerimiento"
4. El sistema ejecuta consulta:
   ```python
   casos_huerfanos = CasoDeUso.objects.filter(
       proyecto=proyecto
   ).annotate(
       rel_count=Count('relaciones_requerimientos')
   ).filter(rel_count=0)
   ```
5. El sistema calcula estadísticas:
   - Total de casos de uso en el proyecto
   - Cantidad de casos huérfanos
   - Porcentaje de casos huérfanos: `(huerfanos / total) * 100`
6. El sistema muestra lista con:
   - Nombre del caso de uso
   - Descripción breve
   - Fecha de creación
   - Creado por
   - Botón "Vincular requerimiento"
   - Botón "Ver detalle"
7. El usuario puede:
   - Revisar cada caso huérfano
   - Hacer clic en "Vincular requerimiento" para asociarlo
   - Filtrar por fecha de creación, creador
   - Ordenar por nombre, fecha
   - Exportar lista a CSV/Excel
8. El usuario selecciona un caso huérfano
9. El usuario hace clic en "Vincular requerimiento"
10. El sistema muestra modal con lista de requerimientos disponibles
11. El usuario selecciona uno o más requerimientos
12. El usuario confirma la vinculación
13. El sistema crea registros en `RequerimientoCaso`
14. El sistema actualiza la lista (el caso ya no aparece como huérfano)
15. El sistema actualiza estadísticas

### Flujos Alternativos
**4a. No hay casos de uso en el proyecto**
- El sistema detecta lista vacía
- Muestra mensaje: "No hay casos de uso en el proyecto"
- Muestra botón "Crear caso de uso"
- No muestra estadísticas

**4b. Todos los casos de uso tienen al menos un requerimiento (0 huérfanos)**
- El sistema detecta lista vacía de huérfanos
- Muestra mensaje de éxito: "✓ Excelente! Todos los casos de uso están vinculados a requerimientos"
- Muestra estadísticas: "0 casos huérfanos (0%)"
- Muestra gráfico de cobertura 100%

**10a. No hay requerimientos para vincular**
- El sistema detecta que el proyecto no tiene requerimientos
- Muestra mensaje: "No hay requerimientos en el proyecto. Cree al menos un requerimiento primero"
- Muestra botón "Crear requerimiento"
- Permite cancelar

**13a. Error al crear vinculación**
- El sistema captura excepción
- Muestra error: "Error al vincular, intente nuevamente"
- Registra el error en logs
- No crea la vinculación
- Permite reintentar

### Flujo Opcional - Vincular Masivamente
1. El usuario selecciona múltiples casos huérfanos (checkboxes)
2. El usuario hace clic en "Vincular seleccionados"
3. El sistema muestra modal con lista de requerimientos
4. El usuario selecciona un requerimiento común
5. El sistema vincula todos los casos seleccionados con ese requerimiento
6. El sistema muestra resumen: "X casos de uso vinculados exitosamente"
7. El sistema actualiza la lista

### Flujo Opcional - Marcar como Técnico/Infraestructura
1. El usuario identifica un caso de uso técnico sin requerimiento funcional
2. El usuario hace clic en "Marcar como técnico"
3. El sistema agrega etiqueta/tag "Técnico" o "Infraestructura"
4. El caso deja de aparecer en alertas de huérfanos
5. El caso se lista separadamente en "Casos técnicos"

### Flujo Opcional - Eliminar Caso Huérfano Obsoleto
1. El usuario revisa un caso de uso huérfano
2. El usuario determina que es obsoleto y no se necesita
3. El usuario hace clic en "Eliminar"
4. El sistema muestra confirmación:
   - "¿Está seguro de eliminar el caso de uso [nombre]?"
   - "No está vinculado a ningún requerimiento"
   - "Esta acción no se puede deshacer"
5. El usuario confirma
6. El sistema elimina el caso de uso
7. El sistema actualiza estadísticas

### Reglas de Negocio
- RN-01: Un caso de uso es huérfano si no tiene ninguna relación en `RequerimientoCaso`
- RN-02: Los casos huérfanos NO son necesariamente errores (pueden ser casos técnicos)
- RN-03: Se recomienda que <10% de los casos de uso sean huérfanos
- RN-04: Los casos de uso técnicos/infraestructura pueden marcarse para excluirlos de alertas
- RN-05: La lista se actualiza en tiempo real al crear/eliminar vinculaciones
- RN-06: Solo usuarios con permisos de edición pueden vincular casos huérfanos
- RN-07: La lista es de solo lectura pero permite acciones (vincular, eliminar)
- RN-08: Los casos huérfanos se destacan visualmente en listados generales

### Consulta Actual (Implementada)

```python
# En dashboards/views.py (línea 108) y requerimientos/views.py (línea 39)
casos_huerfanos = casos.annotate(
    rel_count=Count('relaciones_requerimientos')
).filter(rel_count=0)

# Uso en template
{% for caso in casos_huerfanos %}
    <tr class="huerfano">
        <td>{{ caso.nombre }}</td>
        <td>{{ caso.descripcion|truncatewords:20 }}</td>
        <td>Sin requerimiento</td>
        <td>
            <a href="#" class="btn-vincular">Vincular</a>
        </td>
    </tr>
{% endfor %}
```

### Visualización Recomendada

```html
<!-- Lista de casos huérfanos -->
<div class="huerfanos-container">
    <div class="estadisticas-huerfanos">
        <div class="stat warning">
            <span class="valor">{{ casos_huerfanos.count }}</span>
            <span class="label">Casos sin requerimiento</span>
        </div>
        <div class="stat">
            <span class="valor">{{ porcentaje_huerfanos }}%</span>
            <span class="label">del total</span>
        </div>
    </div>
    
    {% if casos_huerfanos %}
        <div class="alert alert-warning">
            <i class="bi bi-exclamation-triangle"></i>
            Los siguientes casos de uso no están vinculados a ningún requerimiento.
            Considere vincularlos o marcarlos como técnicos.
        </div>
        
        <table class="table">
            <thead>
                <tr>
                    <th>Caso de Uso</th>
                    <th>Descripción</th>
                    <th>Creado</th>
                    <th>Por</th>
                    <th>Acciones</th>
                </tr>
            </thead>
            <tbody>
                {% for caso in casos_huerfanos %}
                <tr class="huerfano-row">
                    <td>
                        <strong>{{ caso.nombre }}</strong>
                    </td>
                    <td>{{ caso.descripcion|truncatewords:15 }}</td>
                    <td>{{ caso.fecha_creacion|date:"d/m/Y" }}</td>
                    <td>{{ caso.creado_por.nombre }}</td>
                    <td>
                        <button class="btn btn-sm btn-primary" onclick="vincularCaso({{ caso.id }})">
                            <i class="bi bi-link"></i> Vincular
                        </button>
                        <a href="{% url 'casos_de_uso:detalle' caso.id %}" class="btn btn-sm btn-secondary">
                            <i class="bi bi-eye"></i> Ver
                        </a>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    {% else %}
        <div class="alert alert-success">
            <i class="bi bi-check-circle"></i>
            ¡Excelente! Todos los casos de uso están vinculados a requerimientos.
        </div>
    {% endif %}
</div>
```

### Notas Técnicas
**Estado Actual:**
✅ **IMPLEMENTADO PARCIALMENTE** - La consulta existe en el código

**Implementado:**
- Consulta ORM para obtener casos huérfanos: `annotate(rel_count=Count('relaciones_requerimientos')).filter(rel_count=0)`
- Usado en `dashboards/views.py` línea 108
- Usado en `requerimientos/views.py` línea 39

**Falta implementar:**
- Vista dedicada para listar casos huérfanos
- Template específico con listado y acciones
- Funcionalidad de vincular desde la lista
- Exportación de lista a CSV/Excel
- Opción de marcar como técnico/infraestructura
- Filtros y ordenamiento
- Gráficos de estadísticas
- Alertas/notificaciones cuando hay muchos huérfanos

**Mejoras Recomendadas:**

1. **Vista dedicada:**
```python
@login_required
def casos_huerfanos(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, pk=proyecto_id)
    
    casos_huerfanos = CasoDeUso.objects.filter(
        proyecto=proyecto
    ).annotate(
        rel_count=Count('relaciones_requerimientos')
    ).filter(rel_count=0).select_related('creado_por')
    
    total_casos = CasoDeUso.objects.filter(proyecto=proyecto).count()
    porcentaje = (casos_huerfanos.count() / total_casos * 100) if total_casos > 0 else 0
    
    return render(request, 'casos_de_uso/huerfanos.html', {
        'proyecto': proyecto,
        'casos_huerfanos': casos_huerfanos,
        'total_casos': total_casos,
        'porcentaje_huerfanos': round(porcentaje, 1)
    })
```

2. **Exportar a CSV:**
```python
import csv
from django.http import HttpResponse

def exportar_casos_huerfanos_csv(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, pk=proyecto_id)
    casos_huerfanos = CasoDeUso.objects.filter(
        proyecto=proyecto
    ).annotate(rel_count=Count('relaciones_requerimientos')).filter(rel_count=0)
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="casos_huerfanos_{proyecto.nombre}.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['ID', 'Nombre', 'Descripción', 'Creado', 'Por'])
    
    for caso in casos_huerfanos:
        writer.writerow([
            caso.id,
            caso.nombre,
            caso.descripcion,
            caso.fecha_creacion.strftime('%d/%m/%Y'),
            caso.creado_por.nombre if caso.creado_por else 'N/A'
        ])
    
    return response
```

### Estado de Implementación
⚠️ **PARCIALMENTE IMPLEMENTADO**

**✅ Implementado:**
- Consulta de casos huérfanos con `annotate` y `Count`
- Usado en dashboard y vistas de requerimientos

**❌ NO implementado:**
- Vista dedicada para listar huérfanos
- Template específico
- Funcionalidad de vincular desde lista
- Exportación
- Filtros y estadísticas detalladas

### Prioridad de Implementación
🟡 **MEDIA** - Útil pero no crítica:
- La consulta ya existe y funciona
- Mejora la trazabilidad y limpieza del proyecto
- Facilita auditorías de cobertura
- Puede implementarse rápidamente (consulta ya lista)
- Complementa CU-15 (Generar matriz de trazabilidad)

### Observaciones de Revisión
✅ **Correcciones aplicadas:**
- Reconocido que la consulta YA ESTÁ IMPLEMENTADA en el código
- Especificado dónde se usa actualmente (dashboards y requerimientos views)
- Incluida la consulta ORM exacta del código
- Agregados flujos para vista dedicada
- Añadido código de ejemplo para vista y exportación
- Especificadas mejoras necesarias (vista dedicada, filtros, exportación)
- Incluido HTML de ejemplo para visualización
- Aclarado que casos técnicos/infraestructura pueden no necesitar requerimientos
- Marcada como prioridad media (la consulta existe, falta UI dedicada)
- Complementa la matriz de trazabilidad (CU-15)

---

## CU-17: Listar requerimientos sin caso de uso

### Descripción
El sistema identifica y lista todos los **requerimientos huérfanos** del proyecto, es decir, requerimientos que no están vinculados a ningún caso de uso.

Esta funcionalidad permite:
- **Detectar requerimientos "huérfanos":** requisitos definidos pero sin diseño de implementación
- **Validar cobertura de diseño:** asegurar que todos los requerimientos tienen casos de uso que los satisfacen
- **Priorizar diseño:** identificar qué requerimientos necesitan casos de uso urgentemente
- **Auditoría de completitud:** verificar que ningún requerimiento queda sin especificación de implementación
- **Gestión del backlog:** facilitar la planificación de casos de uso faltantes

Los requerimientos sin casos de uso pueden indicar:
- Requerimientos recién creados (pendientes de diseño)
- Requerimientos no funcionales que no requieren casos de uso explícitos
- Requerimientos de alto nivel que se descomponen en sub-requerimientos
- Requerimientos obsoletos o descartados
- Gaps en la especificación del sistema

### Actores
- **Analista** (revisa y crea casos de uso para requerimientos huérfanos)
- **Líder del proyecto** (valida cobertura y prioriza diseño de casos de uso)
- **Auditor/QA** (verifica que todos los requerimientos tienen especificación de implementación)

### Precondiciones
- Proyecto existente
- Al menos un requerimiento creado
- Usuario autenticado con permisos en el proyecto

### Postcondiciones
- Lista de requerimientos huérfanos mostrada
- Sin cambios en la base de datos (solo consulta)
- Estadísticas actualizadas

### Flujo Principal
1. El usuario accede al proyecto
2. El usuario navega a la sección "Trazabilidad" o "Requerimientos"
3. El usuario hace clic en "Ver requerimientos huérfanos" o filtro "Sin caso de uso"
4. El sistema ejecuta consulta:
   ```python
   reqs_huerfanos = Requerimiento.objects.filter(
       proyecto=proyecto
   ).annotate(
       rel_count=Count('relaciones_casos')
   ).filter(rel_count=0)
   ```
5. El sistema calcula estadísticas:
   - Total de requerimientos en el proyecto
   - Cantidad de requerimientos huérfanos
   - Porcentaje de huérfanos: `(huerfanos / total) * 100`
   - Desglose por tipo (Funcional / No funcional)
   - Desglose por prioridad (Must / Should / Could / Won't)
6. El sistema muestra lista con:
   - Código/ID del requerimiento
   - Nombre del requerimiento
   - Tipo (Funcional / No funcional)
   - Prioridad (MoSCoW)
   - Estado (Pendiente / En progreso / Completado)
   - Fecha de creación
   - Creado por
   - Botón "Crear caso de uso"
   - Botón "Vincular caso existente"
   - Botón "Ver detalle"
7. El usuario puede:
   - Revisar cada requerimiento huérfano
   - Filtrar por tipo, prioridad, estado
   - Ordenar por nombre, fecha, prioridad
   - Exportar lista a CSV/Excel
   - Crear caso de uso directamente desde el requerimiento
   - Vincular a caso de uso existente
8. El usuario selecciona un requerimiento huérfano
9. El usuario decide la acción:
   - **Opción A:** Crear caso de uso nuevo
   - **Opción B:** Vincular a caso de uso existente
   - **Opción C:** Marcar como "No requiere caso de uso" (ej: req. no funcional)

### Flujo Alternativo A - Crear Caso de Uso desde Requerimiento
1. El usuario hace clic en "Crear caso de uso" junto a un requerimiento huérfano
2. El sistema abre formulario de creación de caso de uso con:
   - Campo proyecto pre-llenado
   - Nombre sugerido basado en el requerimiento
   - Descripción pre-llenada con referencia al requerimiento
   - Vinculación automática al requerimiento actual
3. El usuario completa los campos del caso de uso
4. El usuario hace clic en "Guardar"
5. El sistema crea el caso de uso
6. El sistema crea automáticamente la vinculación en `RequerimientoCaso`
7. El sistema actualiza la lista (el requerimiento ya no aparece como huérfano)
8. El sistema muestra mensaje: "Caso de uso creado y vinculado exitosamente"

### Flujo Alternativo B - Vincular a Caso de Uso Existente
1. El usuario hace clic en "Vincular caso existente" junto a un requerimiento huérfano
2. El sistema muestra modal con lista de casos de uso del proyecto
3. El sistema destaca casos de uso sin requerimientos (sugerencias)
4. El usuario busca y selecciona uno o más casos de uso
5. El usuario opcionalmente agrega nota explicativa
6. El usuario hace clic en "Vincular"
7. El sistema crea registros en `RequerimientoCaso`
8. El sistema actualiza la lista (el requerimiento ya no aparece como huérfano)
9. El sistema muestra mensaje: "Requerimiento vinculado exitosamente"

### Flujo Alternativo C - Marcar como "No Requiere Caso de Uso"
1. El usuario identifica un requerimiento no funcional (ej: rendimiento, seguridad)
2. El usuario hace clic en "Marcar como no funcional" o checkbox "No requiere caso de uso"
3. El sistema agrega etiqueta/tag o campo especial
4. El requerimiento deja de aparecer en alertas de huérfanos
5. El requerimiento se lista separadamente en "Requisitos no funcionales"

### Flujos Alternativos
**4a. No hay requerimientos en el proyecto**
- El sistema detecta lista vacía
- Muestra mensaje: "No hay requerimientos en el proyecto"
- Muestra botón "Crear requerimiento"
- No muestra estadísticas

**4b. Todos los requerimientos tienen al menos un caso de uso (0 huérfanos)**
- El sistema detecta lista vacía de huérfanos
- Muestra mensaje de éxito: "✓ Excelente! Todos los requerimientos tienen casos de uso vinculados"
- Muestra estadísticas: "0 requerimientos huérfanos (0%)"
- Muestra gráfico de cobertura 100%

**9a. No hay casos de uso para vincular**
- El sistema detecta que el proyecto no tiene casos de uso
- Muestra mensaje: "No hay casos de uso disponibles. Cree un caso de uso primero"
- Ofrece opción "Crear caso de uso ahora"
- Permite cancelar

**7a. Error al crear vinculación**
- El sistema captura excepción
- Muestra error: "Error al vincular, intente nuevamente"
- Registra el error en logs
- No crea la vinculación
- Permite reintentar

### Flujo Opcional - Vincular Masivamente
1. El usuario selecciona múltiples requerimientos huérfanos (checkboxes)
2. El usuario hace clic en "Vincular seleccionados"
3. El sistema muestra modal con lista de casos de uso
4. El usuario selecciona un caso de uso común
5. El sistema vincula todos los requerimientos seleccionados con ese caso de uso
6. El sistema muestra resumen: "X requerimientos vinculados exitosamente"
7. El sistema actualiza la lista

### Flujo Opcional - Generar Casos de Uso Automáticamente
1. El usuario hace clic en "Generar casos de uso para huérfanos"
2. El sistema analiza cada requerimiento huérfano
3. Para cada requerimiento funcional:
   - Crea un caso de uso con nombre "CU-XX: [Nombre del requerimiento]"
   - Copia descripción del requerimiento
   - Vincula automáticamente
   - Si metodología tradicional: inicializa flujo principal vacío
   - Si metodología ágil: copia historia de usuario del requerimiento
4. El sistema muestra resumen: "X casos de uso generados automáticamente"
5. El usuario revisa y completa los casos de uso generados

### Reglas de Negocio
- RN-01: Un requerimiento es huérfano si no tiene ninguna relación en `RequerimientoCaso`
- RN-02: Los requerimientos huérfanos NO son necesariamente errores
- RN-03: Requerimientos no funcionales pueden no necesitar casos de uso explícitos
- RN-04: Se recomienda que <15% de los requerimientos sean huérfanos
- RN-05: Requerimientos Must Have NO deben ser huérfanos en proyectos en producción
- RN-06: La lista se actualiza en tiempo real al crear/eliminar vinculaciones
- RN-07: Solo usuarios con permisos de edición pueden crear/vincular casos de uso
- RN-08: Los requerimientos huérfanos se destacan visualmente en listados generales
- RN-09: Los requerimientos huérfanos de alta prioridad se muestran con alerta
- RN-10: En metodología ágil, las historias sin casos de uso son más comunes (aceptable)

### Consulta Actual (Implementada)

```python
# En dashboards/views.py (línea 107) y requerimientos/views.py (línea 38)
reqs_huerfanos = requerimientos.annotate(
    rel_count=Count('relaciones_casos')
).filter(rel_count=0)

# Uso en template
{% for req in reqs_huerfanos %}
    <tr class="huerfano">
        <td>{{ req.nombre }}</td>
        <td>{{ req.get_tipo_display }}</td>
        <td>{{ req.detalle_tradicional.prioridad }}</td>
        <td>Sin caso de uso</td>
        <td>
            <a href="#" class="btn-crear-caso">Crear caso</a>
            <a href="#" class="btn-vincular">Vincular existente</a>
        </td>
    </tr>
{% endfor %}
```

### Análisis de Prioridad de Huérfanos

```python
# Requerimientos Must Have huérfanos (CRÍTICO)
reqs_must_huerfanos = reqs_huerfanos.filter(
    detalle_tradicional__prioridad='MUST'
)

# Requerimientos funcionales huérfanos (importante)
reqs_funcionales_huerfanos = reqs_huerfanos.filter(
    tipo='FUNCIONAL'
)

# Requerimientos no funcionales huérfanos (puede ser aceptable)
reqs_no_funcionales_huerfanos = reqs_huerfanos.filter(
    tipo='NO_FUNCIONAL'
)

# Estadísticas por prioridad
estadisticas = {
    'must': reqs_huerfanos.filter(detalle_tradicional__prioridad='MUST').count(),
    'should': reqs_huerfanos.filter(detalle_tradicional__prioridad='SHOULD').count(),
    'could': reqs_huerfanos.filter(detalle_tradicional__prioridad='COULD').count(),
    'wont': reqs_huerfanos.filter(detalle_tradicional__prioridad='WONT').count(),
}
```

### Visualización Recomendada

```html
<!-- Lista de requerimientos huérfanos -->
<div class="huerfanos-container">
    <div class="estadisticas-huerfanos">
        <div class="stat danger">
            <span class="valor">{{ reqs_huerfanos.count }}</span>
            <span class="label">Requerimientos sin caso de uso</span>
        </div>
        <div class="stat">
            <span class="valor">{{ porcentaje_huerfanos }}%</span>
            <span class="label">del total</span>
        </div>
        <div class="stat warning">
            <span class="valor">{{ reqs_must_huerfanos.count }}</span>
            <span class="label">Must Have sin caso</span>
        </div>
    </div>
    
    {% if reqs_must_huerfanos %}
        <div class="alert alert-danger">
            <i class="bi bi-exclamation-triangle-fill"></i>
            <strong>¡Atención!</strong> Hay {{ reqs_must_huerfanos.count }} requerimientos 
            de prioridad MUST sin casos de uso. Estos son críticos y deben tener diseño de implementación.
        </div>
    {% endif %}
    
    {% if reqs_huerfanos %}
        <div class="alert alert-warning">
            <i class="bi bi-info-circle"></i>
            Los siguientes requerimientos no tienen casos de uso vinculados.
            Cree casos de uso o vincúlelos a casos existentes.
        </div>
        
        <!-- Filtros -->
        <div class="filters">
            <button class="filter-btn" data-filter="all">Todos</button>
            <button class="filter-btn" data-filter="funcional">Funcionales</button>
            <button class="filter-btn" data-filter="no_funcional">No Funcionales</button>
            <button class="filter-btn" data-filter="must">Must Have</button>
        </div>
        
        <table class="table">
            <thead>
                <tr>
                    <th>
                        <input type="checkbox" id="select-all">
                    </th>
                    <th>Requerimiento</th>
                    <th>Tipo</th>
                    <th>Prioridad</th>
                    <th>Estado</th>
                    <th>Creado</th>
                    <th>Acciones</th>
                </tr>
            </thead>
            <tbody>
                {% for req in reqs_huerfanos %}
                <tr class="huerfano-row" data-tipo="{{ req.tipo }}" data-prioridad="{{ req.detalle_tradicional.prioridad }}">
                    <td>
                        <input type="checkbox" name="req_ids" value="{{ req.id }}">
                    </td>
                    <td>
                        <strong>{{ req.nombre }}</strong>
                        <br>
                        <small class="text-muted">{{ req.descripcion|truncatewords:10 }}</small>
                    </td>
                    <td>
                        <span class="badge bg-{{ req.tipo == 'FUNCIONAL' and 'primary' or 'secondary' }}">
                            {{ req.get_tipo_display }}
                        </span>
                    </td>
                    <td>
                        <span class="badge bg-{{ req.detalle_tradicional.prioridad == 'MUST' and 'danger' or 'warning' }}">
                            {{ req.detalle_tradicional.prioridad }}
                        </span>
                    </td>
                    <td>{{ req.get_estado_display }}</td>
                    <td>{{ req.fecha_creacion|date:"d/m/Y" }}</td>
                    <td>
                        <div class="btn-group">
                            <button class="btn btn-sm btn-success" onclick="crearCaso({{ req.id }})">
                                <i class="bi bi-plus-circle"></i> Crear caso
                            </button>
                            <button class="btn btn-sm btn-primary" onclick="vincularCaso({{ req.id }})">
                                <i class="bi bi-link"></i> Vincular
                            </button>
                            <a href="{% url 'requerimientos:detalle' req.id %}" class="btn btn-sm btn-secondary">
                                <i class="bi bi-eye"></i> Ver
                            </a>
                        </div>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
        
        <!-- Acciones masivas -->
        <div class="acciones-masivas">
            <button class="btn btn-primary" onclick="vincularSeleccionados()">
                <i class="bi bi-link"></i> Vincular seleccionados
            </button>
            <button class="btn btn-success" onclick="generarCasosAutomaticos()">
                <i class="bi bi-magic"></i> Generar casos automáticamente
            </button>
        </div>
    {% else %}
        <div class="alert alert-success">
            <i class="bi bi-check-circle-fill"></i>
            ¡Excelente! Todos los requerimientos tienen al menos un caso de uso vinculado.
        </div>
    {% endif %}
</div>
```

### Indicadores de Calidad

| Porcentaje Huérfanos | Nivel | Acción Recomendada |
|---------------------|-------|-------------------|
| 0% - 5% | ✅ Excelente | Mantener |
| 6% - 15% | 🟡 Aceptable | Revisar periódicamente |
| 16% - 30% | 🟠 Preocupante | Priorizar creación de casos de uso |
| >30% | 🔴 Crítico | Acción inmediata requerida |

**Criterio especial:**
- **Must Have huérfanos:** 0% aceptable (todos deben tener casos de uso)
- **No funcionales huérfanos:** hasta 50% puede ser aceptable

### Notas Técnicas
**Estado Actual:**
✅ **IMPLEMENTADO PARCIALMENTE** - La consulta existe en el código

**Implementado:**
- Consulta ORM para obtener requerimientos huérfanos: `annotate(rel_count=Count('relaciones_casos')).filter(rel_count=0)`
- Usado en `dashboards/views.py` línea 107
- Usado en `requerimientos/views.py` línea 38

**Falta implementar:**
- Vista dedicada para listar requerimientos huérfanos
- Template específico con listado y acciones
- Funcionalidad de crear caso de uso desde requerimiento
- Funcionalidad de vincular desde la lista
- Filtros por tipo, prioridad, estado
- Estadísticas detalladas por prioridad
- Exportación de lista a CSV/Excel
- Alertas para requerimientos Must Have huérfanos
- Generación automática de casos de uso
- Vinculación masiva

**Mejoras Recomendadas:**

1. **Vista dedicada:**
```python
@login_required
def requerimientos_huerfanos(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, pk=proyecto_id)
    
    reqs_huerfanos = Requerimiento.objects.filter(
        proyecto=proyecto
    ).annotate(
        rel_count=Count('relaciones_casos')
    ).filter(rel_count=0).select_related('creado_por', 'detalle_tradicional')
    
    total_reqs = Requerimiento.objects.filter(proyecto=proyecto).count()
    porcentaje = (reqs_huerfanos.count() / total_reqs * 100) if total_reqs > 0 else 0
    
    # Estadísticas por prioridad
    reqs_must = reqs_huerfanos.filter(detalle_tradicional__prioridad='MUST').count()
    reqs_funcionales = reqs_huerfanos.filter(tipo='FUNCIONAL').count()
    
    # Nivel de alerta
    nivel_alerta = 'success' if porcentaje < 5 else 'warning' if porcentaje < 15 else 'danger'
    
    return render(request, 'requerimientos/huerfanos.html', {
        'proyecto': proyecto,
        'reqs_huerfanos': reqs_huerfanos,
        'total_reqs': total_reqs,
        'porcentaje_huerfanos': round(porcentaje, 1),
        'reqs_must_huerfanos': reqs_must,
        'reqs_funcionales_huerfanos': reqs_funcionales,
        'nivel_alerta': nivel_alerta
    })
```

2. **Crear caso de uso desde requerimiento:**
```python
@login_required
def crear_caso_desde_req(request, requerimiento_id):
    req = get_object_or_404(Requerimiento, pk=requerimiento_id)
    
    if request.method == 'POST':
        form = CasoDeUsoForm(request.POST)
        if form.is_valid():
            caso = form.save(commit=False)
            caso.proyecto = req.proyecto
            caso.creado_por = request.user
            caso.save()
            
            # Crear detalle según metodología
            if req.proyecto.metodologia == 'TRADICIONAL':
                DetalleCasoDeUsoTradicional.objects.create(caso_de_uso_padre=caso)
            elif req.proyecto.metodologia == 'AGIL':
                DetalleCasoDeUsoAgil.objects.create(caso_de_uso_padre=caso)
            
            # Vincular automáticamente
            RequerimientoCaso.objects.create(
                requerimiento=req,
                caso_de_uso=caso,
                nota=f"Creado desde requerimiento {req.nombre}"
            )
            
            messages.success(request, f"Caso de uso creado y vinculado a {req.nombre}")
            return redirect('requerimientos:detalle', pk=req.id)
    else:
        # Pre-llenar formulario
        initial = {
            'nombre': f"CU: {req.nombre}",
            'descripcion': f"Implementa el requerimiento: {req.descripcion}"
        }
        form = CasoDeUsoForm(initial=initial)
    
    return render(request, 'casos_de_uso/crear_desde_req.html', {
        'form': form,
        'requerimiento': req
    })
```

3. **Exportar a CSV:**
```python
def exportar_reqs_huerfanos_csv(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, pk=proyecto_id)
    reqs_huerfanos = Requerimiento.objects.filter(
        proyecto=proyecto
    ).annotate(rel_count=Count('relaciones_casos')).filter(rel_count=0)
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="requerimientos_huerfanos_{proyecto.nombre}.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['ID', 'Nombre', 'Tipo', 'Prioridad', 'Estado', 'Creado', 'Por'])
    
    for req in reqs_huerfanos:
        writer.writerow([
            req.id,
            req.nombre,
            req.get_tipo_display(),
            req.detalle_tradicional.prioridad if req.detalle_tradicional else 'N/A',
            req.get_estado_display(),
            req.fecha_creacion.strftime('%d/%m/%Y'),
            req.creado_por.nombre if req.creado_por else 'N/A'
        ])
    
    return response
```

### Estado de Implementación
⚠️ **PARCIALMENTE IMPLEMENTADO**

**✅ Implementado:**
- Consulta de requerimientos huérfanos con `annotate` y `Count`
- Usado en dashboard y vistas de requerimientos

**❌ NO implementado:**
- Vista dedicada para listar huérfanos
- Template específico con filtros
- Crear caso de uso desde requerimiento
- Vincular desde lista
- Alertas para Must Have huérfanos
- Estadísticas por prioridad
- Exportación
- Generación automática de casos

### Prioridad de Implementación
🟡 **MEDIA-ALTA** - Más crítico que CU-16:
- Los requerimientos sin casos de uso son más problemáticos que casos sin requerimientos
- Requerimientos Must Have huérfanos son críticos para el proyecto
- La consulta ya existe y funciona
- Facilita completitud de la especificación
- Complementa CU-15 (Generar matriz de trazabilidad) y CU-16
- Debe priorizar requerimientos de alta prioridad (Must Have)

### Observaciones de Revisión
✅ **Correcciones aplicadas:**
- Reconocido que la consulta YA ESTÁ IMPLEMENTADA (igual que CU-16)
- Especificado dónde se usa actualmente (dashboards y requerimientos views)
- Añadido análisis por prioridad (Must/Should/Could/Won't)
- Agregados flujos para crear caso de uso desde requerimiento
- Incluido código de ejemplo para vista dedicada y creación de casos
- Especificadas alertas críticas para Must Have huérfanos
- Tabla de indicadores de calidad según porcentaje
- Flujo de generación automática de casos de uso
- HTML de ejemplo con filtros y acciones masivas
- Marcada como prioridad media-alta (más crítica que CU-16)
- Los requerimientos sin casos son más problemáticos que casos sin requerimientos
- Complementa CU-15 y CU-16

---

## CU-18: Comentar requerimiento

### Descripción
El sistema permite a los usuarios agregar **comentarios colaborativos** a un requerimiento específico para facilitar:
- **Discusión y aclaraciones:** preguntas, respuestas, aclaraciones sobre el alcance del requerimiento
- **Seguimiento de decisiones:** registro de decisiones de diseño, cambios de alcance, justificaciones
- **Comunicación asíncrona:** equipo distribuido puede discutir sin reuniones
- **Historial de conversaciones:** todas las discusiones quedan registradas con fecha, autor y contexto
- **Trazabilidad de cambios:** por qué se modificó el requerimiento, quién lo solicitó, cuándo
- **Colaboración multidisciplinaria:** stakeholders, desarrolladores, testers pueden participar
- **Resolución de dudas:** evitar interpretaciones incorrectas del requerimiento

Los comentarios deben ser:
- **Auditables:** fecha, hora, autor registrados automáticamente
- **Editables:** el autor puede editar su comentario (con marca de edición)
- **Eliminables:** autor o admin pueden eliminar comentarios (soft delete recomendado)
- **Anidables (opcional):** respuestas a comentarios específicos (hilos de conversación)
- **Notificables:** alertar a usuarios mencionados o suscritos al requerimiento

### Actores
- **Todos los usuarios del proyecto** (stakeholders, analistas, desarrolladores, testers, PO, SM)

### Precondiciones
- Requerimiento existente
- Usuario autenticado con acceso al proyecto
- Usuario con permisos de lectura mínimo

### Postcondiciones
- Comentario guardado en la base de datos
- Comentario visible para todos los usuarios del proyecto
- Notificaciones enviadas (opcional)
- Fecha y autor registrados

### Flujo Principal
1. El usuario navega al detalle de un requerimiento
2. El sistema muestra la sección "Comentarios" al final de la página
3. El sistema lista comentarios existentes ordenados por fecha (más reciente primero o último)
4. El usuario lee los comentarios anteriores (si existen)
5. El usuario hace clic en "Agregar comentario" o en el campo de texto
6. El sistema muestra editor de texto (textarea con formateo básico opcional)
7. El usuario escribe el comentario (texto plano o Markdown)
8. El usuario opcionalmente:
   - Menciona otros usuarios con `@usuario` (notificación automática)
   - Adjunta archivos pequeños (imágenes, PDFs)
   - Marca como "importante" o "pregunta"
9. El usuario hace clic en "Publicar comentario"
10. El sistema valida:
    - Comentario no vacío (mínimo 3 caracteres)
    - Usuario autenticado
    - Permisos de escritura
11. El sistema crea registro en tabla `ComentarioRequerimiento`:
    ```python
    ComentarioRequerimiento.objects.create(
        requerimiento=requerimiento,
        autor=request.user,
        contenido=comentario_texto,
        fecha_creacion=now()
    )
    ```
12. El sistema renderiza Markdown a HTML (si aplica)
13. El sistema envía notificaciones:
    - A usuarios mencionados con @
    - A usuarios suscritos al requerimiento
    - Al creador del requerimiento (opcional)
14. El sistema recarga la sección de comentarios
15. El sistema muestra mensaje: "Comentario publicado exitosamente"
16. El nuevo comentario aparece en la lista
17. El usuario puede editar/eliminar su comentario (botones solo visibles para él)

### Flujo Alternativo A - Editar Comentario
1. El usuario ve su propio comentario
2. El usuario hace clic en "Editar" (ícono lápiz)
3. El sistema muestra el contenido en modo edición
4. El usuario modifica el texto
5. El usuario hace clic en "Guardar cambios"
6. El sistema valida (no vacío)
7. El sistema actualiza el comentario:
    ```python
    comentario.contenido = nuevo_texto
    comentario.editado = True
    comentario.fecha_ultima_edicion = now()
    comentario.save()
    ```
8. El sistema muestra marca "(editado)" junto a la fecha
9. El comentario actualizado se muestra

### Flujo Alternativo B - Eliminar Comentario
1. El usuario hace clic en "Eliminar" (ícono papelera) en su comentario
2. El sistema muestra confirmación: "¿Eliminar este comentario?"
3. El usuario confirma
4. El sistema marca el comentario como eliminado (soft delete):
    ```python
    comentario.eliminado = True
    comentario.fecha_eliminacion = now()
    comentario.save()
    ```
5. El comentario se oculta (o muestra "[Comentario eliminado]")
6. El sistema muestra mensaje: "Comentario eliminado"

### Flujo Alternativo C - Responder a Comentario (hilos)
1. El usuario hace clic en "Responder" bajo un comentario específico
2. El sistema muestra editor de respuesta anidado
3. El sistema cita automáticamente al autor original: "@usuario dijo..."
4. El usuario escribe su respuesta
5. El usuario hace clic en "Publicar respuesta"
6. El sistema crea comentario con `comentario_padre_id` apuntando al original
7. La respuesta se muestra indentada bajo el comentario padre
8. Se envía notificación al autor del comentario padre

### Flujo Alternativo D - Mencionar Usuario
1. El usuario escribe `@` en el comentario
2. El sistema muestra autocompletado con usuarios del proyecto
3. El usuario selecciona un usuario de la lista
4. El sistema inserta `@nombre_usuario` en el texto
5. Al publicar, el sistema detecta menciones con regex
6. El sistema envía notificación al usuario mencionado:
    ```python
    Notificacion.objects.create(
        usuario=usuario_mencionado,
        tipo='MENCION_COMENTARIO',
        contenido=f"{autor.nombre} te mencionó en {requerimiento.nombre}",
        url=comentario.get_absolute_url()
    )
    ```
7. El usuario mencionado recibe alerta en tiempo real (WebSocket o polling)

### Flujos Alternativos
**10a. Comentario vacío o muy corto**
- El sistema detecta `len(comentario.strip()) < 3`
- Muestra error: "El comentario debe tener al menos 3 caracteres"
- No guarda nada
- Mantiene el foco en el editor

**10b. Usuario sin permisos de escritura**
- El sistema detecta que el usuario solo tiene permisos de lectura
- Muestra mensaje: "No tienes permisos para comentar en este proyecto"
- El campo de comentario aparece deshabilitado o no se muestra

**10c. Requerimiento bloqueado o archivado**
- El sistema detecta que el requerimiento está en estado "ARCHIVADO" o "BLOQUEADO"
- Muestra advertencia: "Este requerimiento está bloqueado. Los comentarios están deshabilitados"
- El campo de comentario se deshabilita

**13a. Error al enviar notificaciones**
- El sistema captura excepción al enviar notificación
- Registra error en logs
- **NO falla** la publicación del comentario
- El comentario se guarda exitosamente
- Muestra advertencia: "Comentario publicado, pero algunas notificaciones no se pudieron enviar"

### Flujo Opcional - Suscribirse a Comentarios
1. El usuario hace clic en "Suscribirse a notificaciones" en el requerimiento
2. El sistema crea registro: `SuscripcionRequerimiento(usuario=user, requerimiento=req)`
3. El usuario recibe notificaciones de todos los comentarios nuevos
4. El usuario puede hacer clic en "Desuscribirse" en cualquier momento

### Flujo Opcional - Filtrar Comentarios
1. El usuario hace clic en "Filtros"
2. El sistema muestra opciones:
   - Solo mis comentarios
   - Solo preguntas
   - Solo comentarios importantes
   - Por autor específico
3. El usuario selecciona un filtro
4. El sistema filtra la lista de comentarios en tiempo real (JavaScript)

### Reglas de Negocio
- RN-01: Los comentarios son visibles para todos los miembros del proyecto
- RN-02: Solo el autor puede editar su propio comentario (o admin)
- RN-03: Solo el autor puede eliminar su propio comentario (o admin del proyecto)
- RN-04: Los comentarios editados deben mostrar marca "(editado)" y fecha de última edición
- RN-05: Los comentarios eliminados se ocultan pero se conservan en BD (soft delete)
- RN-06: Comentarios deben registrar autor, fecha, contenido mínimo
- RN-07: Se recomienda soporte de Markdown básico (negritas, cursivas, listas, links)
- RN-08: Menciones con @ deben generar notificaciones automáticas
- RN-09: Comentarios no pueden ser vacíos (mínimo 3 caracteres)
- RN-10: Límite recomendado de 5000 caracteres por comentario
- RN-11: Comentarios se ordenan cronológicamente (más reciente al final o al principio según preferencia)
- RN-12: Respuestas anidadas (opcional) máximo 2 niveles de profundidad
- RN-13: Admin puede eliminar cualquier comentario (moderar contenido inapropiado)

### Modelo Propuesto

```python
# En requerimientos/models.py
class ComentarioRequerimiento(models.Model):
    """Comentarios colaborativos en requerimientos."""
    requerimiento = models.ForeignKey(
        Requerimiento, 
        on_delete=models.CASCADE, 
        related_name='comentarios'
    )
    autor = models.ForeignKey(
        Usuario, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='comentarios_requerimientos'
    )
    contenido = models.TextField(
        max_length=5000,
        help_text="Soporta Markdown básico"
    )
    
    # Comentarios anidados (opcional)
    comentario_padre = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='respuestas'
    )
    
    # Metadatos
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_ultima_edicion = models.DateTimeField(null=True, blank=True)
    editado = models.BooleanField(default=False)
    
    # Soft delete
    eliminado = models.BooleanField(default=False)
    fecha_eliminacion = models.DateTimeField(null=True, blank=True)
    
    # Clasificación (opcional)
    tipo = models.CharField(
        max_length=20,
        choices=[
            ('NORMAL', 'Normal'),
            ('PREGUNTA', 'Pregunta'),
            ('IMPORTANTE', 'Importante'),
            ('DECISION', 'Decisión'),
        ],
        default='NORMAL'
    )
    
    class Meta:
        ordering = ['fecha_creacion']  # o ['-fecha_creacion'] para descendente
        verbose_name = 'Comentario de Requerimiento'
        verbose_name_plural = 'Comentarios de Requerimientos'
    
    def __str__(self):
        return f"Comentario de {self.autor} en {self.requerimiento.nombre}"
    
    def get_absolute_url(self):
        return f"{self.requerimiento.get_absolute_url()}#comentario-{self.id}"
    
    def contenido_html(self):
        """Convierte Markdown a HTML."""
        import markdown
        return markdown.markdown(self.contenido, safe_mode='escape')
```

### Vista Propuesta

```python
# En requerimientos/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone

@login_required
def agregar_comentario_requerimiento(request, requerimiento_id):
    """Agregar comentario a un requerimiento."""
    requerimiento = get_object_or_404(Requerimiento, pk=requerimiento_id)
    
    # Verificar permisos de escritura en el proyecto
    if not request.user.tiene_permiso_escritura(requerimiento.proyecto):
        messages.error(request, "No tienes permisos para comentar en este proyecto")
        return redirect('requerimientos:detalle', pk=requerimiento.id)
    
    if request.method == 'POST':
        contenido = request.POST.get('contenido', '').strip()
        tipo = request.POST.get('tipo', 'NORMAL')
        comentario_padre_id = request.POST.get('comentario_padre_id')
        
        # Validar contenido
        if len(contenido) < 3:
            messages.error(request, "El comentario debe tener al menos 3 caracteres")
            return redirect('requerimientos:detalle', pk=requerimiento.id)
        
        if len(contenido) > 5000:
            messages.error(request, "El comentario no puede exceder 5000 caracteres")
            return redirect('requerimientos:detalle', pk=requerimiento.id)
        
        # Crear comentario
        comentario = ComentarioRequerimiento.objects.create(
            requerimiento=requerimiento,
            autor=request.user,
            contenido=contenido,
            tipo=tipo,
            comentario_padre_id=comentario_padre_id if comentario_padre_id else None
        )
        
        # Procesar menciones y enviar notificaciones
        enviar_notificaciones_menciones(comentario)
        
        messages.success(request, "Comentario publicado exitosamente")
        return redirect(f"{requerimiento.get_absolute_url()}#comentario-{comentario.id}")
    
    return redirect('requerimientos:detalle', pk=requerimiento.id)


@login_required
def editar_comentario_requerimiento(request, comentario_id):
    """Editar un comentario propio."""
    comentario = get_object_or_404(ComentarioRequerimiento, pk=comentario_id)
    
    # Solo el autor o admin puede editar
    if comentario.autor != request.user and not request.user.es_admin_proyecto(comentario.requerimiento.proyecto):
        messages.error(request, "No tienes permisos para editar este comentario")
        return redirect('requerimientos:detalle', pk=comentario.requerimiento.id)
    
    if request.method == 'POST':
        nuevo_contenido = request.POST.get('contenido', '').strip()
        
        if len(nuevo_contenido) < 3:
            messages.error(request, "El comentario debe tener al menos 3 caracteres")
            return redirect('requerimientos:detalle', pk=comentario.requerimiento.id)
        
        # Actualizar comentario
        comentario.contenido = nuevo_contenido
        comentario.editado = True
        comentario.fecha_ultima_edicion = timezone.now()
        comentario.save()
        
        messages.success(request, "Comentario actualizado exitosamente")
        return redirect(f"{comentario.requerimiento.get_absolute_url()}#comentario-{comentario.id}")
    
    return redirect('requerimientos:detalle', pk=comentario.requerimiento.id)


@login_required
def eliminar_comentario_requerimiento(request, comentario_id):
    """Eliminar (soft delete) un comentario."""
    comentario = get_object_or_404(ComentarioRequerimiento, pk=comentario_id)
    
    # Solo el autor o admin puede eliminar
    if comentario.autor != request.user and not request.user.es_admin_proyecto(comentario.requerimiento.proyecto):
        messages.error(request, "No tienes permisos para eliminar este comentario")
        return redirect('requerimientos:detalle', pk=comentario.requerimiento.id)
    
    if request.method == 'POST':
        # Soft delete
        comentario.eliminado = True
        comentario.fecha_eliminacion = timezone.now()
        comentario.save()
        
        messages.success(request, "Comentario eliminado exitosamente")
        return redirect('requerimientos:detalle', pk=comentario.requerimiento.id)
    
    # Mostrar confirmación
    return render(request, 'requerimientos/confirmar_eliminar_comentario.html', {
        'comentario': comentario
    })


def enviar_notificaciones_menciones(comentario):
    """Detecta menciones (@usuario) y envía notificaciones."""
    import re
    
    # Regex para detectar @usuario
    menciones = re.findall(r'@(\w+)', comentario.contenido)
    
    for username in menciones:
        try:
            usuario = Usuario.objects.get(username=username)
            # Crear notificación (requiere modelo de notificaciones)
            # Notificacion.objects.create(...)
            # O enviar email
            # send_mail(...)
        except Usuario.DoesNotExist:
            pass  # Usuario no existe, ignorar
```

### Template Propuesto

```html
<!-- En requerimientos/templates/requerimientos/detalle.html -->
<div class="comentarios-section">
    <h3>
        <i class="bi bi-chat-left-text"></i> 
        Comentarios 
        <span class="badge bg-secondary">{{ requerimiento.comentarios.filter(eliminado=False).count }}</span>
    </h3>
    
    <!-- Lista de comentarios -->
    <div class="comentarios-list">
        {% for comentario in requerimiento.comentarios.filter(eliminado=False, comentario_padre__isnull=True) %}
        <div class="comentario" id="comentario-{{ comentario.id }}">
            <div class="comentario-header">
                <img src="{{ comentario.autor.avatar_url }}" alt="{{ comentario.autor.nombre }}" class="avatar-sm">
                <strong>{{ comentario.autor.nombre }}</strong>
                <span class="text-muted">{{ comentario.fecha_creacion|date:"d/m/Y H:i" }}</span>
                {% if comentario.editado %}
                    <span class="badge bg-info">(editado)</span>
                {% endif %}
                {% if comentario.tipo != 'NORMAL' %}
                    <span class="badge bg-{{ comentario.tipo == 'PREGUNTA' and 'warning' or 'danger' }}">
                        {{ comentario.get_tipo_display }}
                    </span>
                {% endif %}
            </div>
            
            <div class="comentario-body">
                {{ comentario.contenido_html|safe }}
            </div>
            
            <div class="comentario-actions">
                <button class="btn btn-sm btn-link" onclick="responder({{ comentario.id }})">
                    <i class="bi bi-reply"></i> Responder
                </button>
                
                {% if comentario.autor == request.user %}
                    <button class="btn btn-sm btn-link" onclick="editarComentario({{ comentario.id }})">
                        <i class="bi bi-pencil"></i> Editar
                    </button>
                    <form method="post" action="{% url 'requerimientos:eliminar_comentario' comentario.id %}" style="display:inline;">
                        {% csrf_token %}
                        <button type="submit" class="btn btn-sm btn-link text-danger" onclick="return confirm('¿Eliminar este comentario?')">
                            <i class="bi bi-trash"></i> Eliminar
                        </button>
                    </form>
                {% endif %}
            </div>
            
            <!-- Respuestas anidadas -->
            {% if comentario.respuestas.filter(eliminado=False).exists %}
            <div class="respuestas">
                {% for respuesta in comentario.respuestas.filter(eliminado=False) %}
                <div class="comentario comentario-respuesta" id="comentario-{{ respuesta.id }}">
                    <div class="comentario-header">
                        <img src="{{ respuesta.autor.avatar_url }}" alt="{{ respuesta.autor.nombre }}" class="avatar-xs">
                        <strong>{{ respuesta.autor.nombre }}</strong>
                        <span class="text-muted">{{ respuesta.fecha_creacion|date:"d/m/Y H:i" }}</span>
                    </div>
                    <div class="comentario-body">
                        {{ respuesta.contenido_html|safe }}
                    </div>
                </div>
                {% endfor %}
            </div>
            {% endif %}
        </div>
        {% empty %}
        <p class="text-muted">No hay comentarios aún. Sé el primero en comentar.</p>
        {% endfor %}
    </div>
    
    <!-- Formulario para agregar comentario -->
    {% if user.tiene_permiso_escritura %}
    <div class="agregar-comentario">
        <h4>Agregar comentario</h4>
        <form method="post" action="{% url 'requerimientos:agregar_comentario' requerimiento.id %}">
            {% csrf_token %}
            <div class="mb-3">
                <textarea 
                    name="contenido" 
                    class="form-control" 
                    rows="4" 
                    placeholder="Escribe tu comentario... (Soporta Markdown básico)"
                    required
                    minlength="3"
                    maxlength="5000"
                ></textarea>
                <small class="text-muted">
                    Puedes mencionar usuarios con @usuario. 
                    Soporta **negritas**, *cursivas*, [enlaces](url)
                </small>
            </div>
            
            <div class="mb-3">
                <label>Tipo de comentario:</label>
                <div class="btn-group" role="group">
                    <input type="radio" class="btn-check" name="tipo" value="NORMAL" id="tipo-normal" checked>
                    <label class="btn btn-outline-secondary" for="tipo-normal">Normal</label>
                    
                    <input type="radio" class="btn-check" name="tipo" value="PREGUNTA" id="tipo-pregunta">
                    <label class="btn btn-outline-warning" for="tipo-pregunta">❓ Pregunta</label>
                    
                    <input type="radio" class="btn-check" name="tipo" value="IMPORTANTE" id="tipo-importante">
                    <label class="btn btn-outline-danger" for="tipo-importante">⚠️ Importante</label>
                    
                    <input type="radio" class="btn-check" name="tipo" value="DECISION" id="tipo-decision">
                    <label class="btn btn-outline-info" for="tipo-decision">✓ Decisión</label>
                </div>
            </div>
            
            <button type="submit" class="btn btn-primary">
                <i class="bi bi-send"></i> Publicar comentario
            </button>
        </form>
    </div>
    {% else %}
    <div class="alert alert-warning">
        No tienes permisos para comentar en este proyecto.
    </div>
    {% endif %}
</div>
```

### JavaScript para Respuestas y Edición

```javascript
// En requerimientos/static/requerimientos/js/comentarios.js
function responder(comentarioId) {
    // Mostrar formulario de respuesta anidado bajo el comentario
    const comentario = document.getElementById(`comentario-${comentarioId}`);
    const form = document.querySelector('.agregar-comentario form');
    
    // Clonar formulario y modificar para respuesta
    const formRespuesta = form.cloneNode(true);
    formRespuesta.querySelector('textarea').value = `@${comentario.dataset.autor} `;
    formRespuesta.querySelector('input[name="comentario_padre_id"]').value = comentarioId;
    
    // Insertar después del comentario
    comentario.appendChild(formRespuesta);
}

function editarComentario(comentarioId) {
    const comentario = document.getElementById(`comentario-${comentarioId}`);
    const contenidoDiv = comentario.querySelector('.comentario-body');
    const contenidoOriginal = contenidoDiv.dataset.original;
    
    // Reemplazar con textarea
    contenidoDiv.innerHTML = `
        <form method="post" action="/requerimientos/comentario/${comentarioId}/editar/">
            <textarea class="form-control" name="contenido">${contenidoOriginal}</textarea>
            <button type="submit" class="btn btn-sm btn-success mt-2">Guardar</button>
            <button type="button" class="btn btn-sm btn-secondary mt-2" onclick="cancelarEdicion(${comentarioId})">Cancelar</button>
        </form>
    `;
}

function cancelarEdicion(comentarioId) {
    location.reload();  // O restaurar contenido sin recargar
}
```

### Estado de Implementación
⏳ **PLANIFICADO PARA IMPLEMENTACIÓN PRÓXIMA**

**Análisis del código actual:**
- ❌ NO existe modelo `ComentarioRequerimiento` (aún)
- ❌ Solo existe campo `observaciones` en `DetalleRequerimientoTradicional` y `DetalleRequerimientoAgil` (no es lo mismo)
- ❌ Campo `observaciones` es un `TextField` simple, NO soporta múltiples comentarios colaborativos
- ❌ Campo `observaciones` NO registra autor, fecha, ni permite edición/eliminación
- ❌ NO hay vistas para agregar/editar/eliminar comentarios (pendiente)
- ❌ NO hay templates con sección de comentarios (pendiente)
- ❌ NO hay sistema de notificaciones para menciones (pendiente)

**📋 Funcionalidad planificada:**
- ✅ Se implementará sistema de comentarios completo
- ✅ Disponible para requerimientos (CU-18) y casos de uso (CU-19)
- ✅ Todos los usuarios del proyecto podrán comentar
- ✅ Incluirá autor, fecha, edición, eliminación
- ✅ Soporte de respuestas anidadas (hilos de conversación)
- ✅ Notificaciones para menciones con @usuario

**Campo actual `observaciones` vs Comentarios:**
```python
# Campo actual (NO es lo mismo que comentarios)
observaciones = models.TextField(blank=True)
# - Es un campo de texto simple
# - NO registra autor ni fecha
# - NO permite múltiples comentarios
# - NO es colaborativo (solo el que edita el requerimiento puede modificarlo)
# - NO tiene historial de cambios
```

**Diferencias clave:**
| Característica | `observaciones` (actual) | Comentarios (propuesto) |
|---------------|-------------------------|-------------------------|
| Múltiples entradas | ❌ No | ✅ Sí (tabla separada) |
| Autor registrado | ❌ No | ✅ Sí (FK a Usuario) |
| Fecha registrada | ❌ No | ✅ Sí (auto_now_add) |
| Edición con historial | ❌ No | ✅ Sí (con marca editado) |
| Eliminación | ❌ Sobrescritura | ✅ Soft delete |
| Colaborativo | ❌ No | ✅ Sí (todos pueden comentar) |
| Notificaciones | ❌ No | ✅ Sí (menciones @) |
| Respuestas anidadas | ❌ No | ✅ Sí (comentario_padre) |

### Prioridad de Implementación
🟢 **ALTA - EN PLANIFICACIÓN** - Funcionalidad de colaboración crítica:
- Facilita comunicación asíncrona en equipos distribuidos
- Registra decisiones y aclaraciones con trazabilidad completa
- Mejora la calidad de especificación de requerimientos
- Reduce malentendidos y ambigüedades
- Complementa CU-19 (Comentar caso de uso)
- Similar a sistemas issue tracking (GitHub Issues, Jira, etc.)
- Campo `observaciones` actual es insuficiente para colaboración real
- **Se implementará próximamente para requerimientos y casos de uso**

### Observaciones de Revisión
✅ **Análisis realizado:**
- Confirmado que NO existen comentarios como entidad separada
- Campo `observaciones` actual es simple TextField sin metadatos
- Propuesto modelo completo `ComentarioRequerimiento` con:
  - Relación FK a requerimiento y autor
  - Soporte de respuestas anidadas (comentario_padre)
  - Soft delete para auditabilidad
  - Marcas de edición con fecha
  - Tipos de comentario (Normal, Pregunta, Importante, Decisión)
- Incluidas vistas para agregar, editar, eliminar comentarios
- Template completo con formulario y listado
- JavaScript para respuestas y edición inline
- Sistema de menciones con @ y notificaciones
- Soporte de Markdown para formateo
- **CRÍTICO:** Esto NO es lo mismo que el campo `observaciones` actual

---

## CU-19: Comentar caso de uso

### Descripción
El sistema permite a los usuarios agregar **comentarios colaborativos** a un caso de uso específico. Esta funcionalidad es **idéntica a CU-18 (Comentar requerimiento)** pero aplicada a casos de uso.

Los comentarios en casos de uso facilitan:
- **Discusión sobre diseño:** preguntas sobre flujos alternativos, excepciones, precondiciones
- **Aclaraciones de implementación:** desarrolladores consultan detalles técnicos
- **Revisión por pares:** feedback de otros analistas sobre la especificación
- **Decisiones de diseño:** registro de por qué se eligió un enfoque específico
- **Cambios de alcance:** documentar modificaciones al caso de uso original
- **Comunicación con stakeholders:** respuestas a dudas sobre el comportamiento esperado
- **Trazabilidad de conversaciones:** historial completo de discusiones sobre cada caso

### Actores
- **Todos los usuarios del proyecto** (analistas, desarrolladores, testers, arquitectos, PO, SM, stakeholders)

### Precondiciones
- Caso de uso existente
- Usuario autenticado con acceso al proyecto
- Usuario con permisos de lectura mínimo

### Postcondiciones
- Comentario guardado en la base de datos
- Comentario visible para todos los usuarios del proyecto
- Notificaciones enviadas a usuarios mencionados (opcional)
- Fecha y autor registrados

### Flujo Principal
1. El usuario navega al detalle de un caso de uso
2. El sistema muestra la sección "Comentarios" al final de la página
3. El sistema lista comentarios existentes ordenados cronológicamente
4. El usuario lee los comentarios anteriores (si existen)
5. El usuario hace clic en "Agregar comentario" o en el campo de texto
6. El sistema muestra editor de texto (textarea con formateo básico opcional)
7. El usuario escribe el comentario (texto plano o Markdown)
8. El usuario opcionalmente:
   - Menciona otros usuarios con `@usuario` (notificación automática)
   - Marca como "importante" o "pregunta"
   - Adjunta imágenes o archivos pequeños (opcional)
9. El usuario hace clic en "Publicar comentario"
10. El sistema valida:
    - Comentario no vacío (mínimo 3 caracteres)
    - Usuario autenticado
    - Permisos de escritura en el proyecto
11. El sistema crea registro en tabla `ComentarioCasoDeUso`:
    ```python
    ComentarioCasoDeUso.objects.create(
        caso_de_uso=caso,
        autor=request.user,
        contenido=comentario_texto,
        fecha_creacion=now()
    )
    ```
12. El sistema renderiza Markdown a HTML (si aplica)
13. El sistema envía notificaciones a usuarios mencionados
14. El sistema recarga la sección de comentarios
15. El sistema muestra mensaje: "Comentario publicado exitosamente"
16. El nuevo comentario aparece en la lista
17. El usuario puede editar/eliminar su comentario

### Flujos Alternativos
**Idénticos a CU-18:**
- **Flujo A:** Editar comentario (solo autor o admin)
- **Flujo B:** Eliminar comentario (soft delete)
- **Flujo C:** Responder a comentario (hilos anidados)
- **Flujo D:** Mencionar usuario con @usuario

Ver CU-18 para detalles completos de estos flujos.

### Reglas de Negocio
**Idénticas a CU-18:**
- RN-01: Los comentarios son visibles para todos los miembros del proyecto
- RN-02: Solo el autor puede editar su propio comentario (o admin)
- RN-03: Solo el autor puede eliminar su propio comentario (o admin del proyecto)
- RN-04: Los comentarios editados deben mostrar marca "(editado)" y fecha de última edición
- RN-05: Los comentarios eliminados se ocultan pero se conservan en BD (soft delete)
- RN-06: Comentarios deben registrar autor, fecha, contenido mínimo
- RN-07: Se recomienda soporte de Markdown básico (negritas, cursivas, listas, links)
- RN-08: Menciones con @ deben generar notificaciones automáticas
- RN-09: Comentarios no pueden ser vacíos (mínimo 3 caracteres)
- RN-10: Límite recomendado de 5000 caracteres por comentario
- RN-11: Comentarios se ordenan cronológicamente
- RN-12: Respuestas anidadas (opcional) máximo 2 niveles de profundidad
- RN-13: Admin puede eliminar cualquier comentario

### Modelo Propuesto

```python
# En casos_de_uso/models.py
class ComentarioCasoDeUso(models.Model):
    """Comentarios colaborativos en casos de uso."""
    caso_de_uso = models.ForeignKey(
        CasoDeUso, 
        on_delete=models.CASCADE, 
        related_name='comentarios'
    )
    autor = models.ForeignKey(
        Usuario, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='comentarios_casos_uso'
    )
    contenido = models.TextField(
        max_length=5000,
        help_text="Soporta Markdown básico"
    )
    
    # Comentarios anidados (opcional)
    comentario_padre = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='respuestas'
    )
    
    # Metadatos
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_ultima_edicion = models.DateTimeField(null=True, blank=True)
    editado = models.BooleanField(default=False)
    
    # Soft delete
    eliminado = models.BooleanField(default=False)
    fecha_eliminacion = models.DateTimeField(null=True, blank=True)
    
    # Clasificación (opcional)
    tipo = models.CharField(
        max_length=20,
        choices=[
            ('NORMAL', 'Normal'),
            ('PREGUNTA', 'Pregunta'),
            ('IMPORTANTE', 'Importante'),
            ('DECISION', 'Decisión'),
        ],
        default='NORMAL'
    )
    
    class Meta:
        ordering = ['fecha_creacion']
        verbose_name = 'Comentario de Caso de Uso'
        verbose_name_plural = 'Comentarios de Casos de Uso'
    
    def __str__(self):
        return f"Comentario de {self.autor} en {self.caso_de_uso.nombre}"
    
    def get_absolute_url(self):
        return f"{self.caso_de_uso.get_absolute_url()}#comentario-{self.id}"
    
    def contenido_html(self):
        """Convierte Markdown a HTML."""
        import markdown
        return markdown.markdown(self.contenido, safe_mode='escape')
```

### Vistas Propuestas

```python
# En casos_de_uso/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone

@login_required
def agregar_comentario_caso(request, caso_id):
    """Agregar comentario a un caso de uso."""
    caso = get_object_or_404(CasoDeUso, pk=caso_id)
    
    if not request.user.tiene_permiso_escritura(caso.proyecto):
        messages.error(request, "No tienes permisos para comentar en este proyecto")
        return redirect('casos_de_uso:detalle', pk=caso.id)
    
    if request.method == 'POST':
        contenido = request.POST.get('contenido', '').strip()
        tipo = request.POST.get('tipo', 'NORMAL')
        comentario_padre_id = request.POST.get('comentario_padre_id')
        
        if len(contenido) < 3:
            messages.error(request, "El comentario debe tener al menos 3 caracteres")
            return redirect('casos_de_uso:detalle', pk=caso.id)
        
        if len(contenido) > 5000:
            messages.error(request, "El comentario no puede exceder 5000 caracteres")
            return redirect('casos_de_uso:detalle', pk=caso.id)
        
        comentario = ComentarioCasoDeUso.objects.create(
            caso_de_uso=caso,
            autor=request.user,
            contenido=contenido,
            tipo=tipo,
            comentario_padre_id=comentario_padre_id if comentario_padre_id else None
        )
        
        # Procesar menciones y enviar notificaciones
        enviar_notificaciones_menciones(comentario)
        
        messages.success(request, "Comentario publicado exitosamente")
        return redirect(f"{caso.get_absolute_url()}#comentario-{comentario.id}")
    
    return redirect('casos_de_uso:detalle', pk=caso.id)


@login_required
def editar_comentario_caso(request, comentario_id):
    """Editar un comentario propio."""
    comentario = get_object_or_404(ComentarioCasoDeUso, pk=comentario_id)
    
    if comentario.autor != request.user and not request.user.es_admin_proyecto(comentario.caso_de_uso.proyecto):
        messages.error(request, "No tienes permisos para editar este comentario")
        return redirect('casos_de_uso:detalle', pk=comentario.caso_de_uso.id)
    
    if request.method == 'POST':
        nuevo_contenido = request.POST.get('contenido', '').strip()
        
        if len(nuevo_contenido) < 3:
            messages.error(request, "El comentario debe tener al menos 3 caracteres")
            return redirect('casos_de_uso:detalle', pk=comentario.caso_de_uso.id)
        
        comentario.contenido = nuevo_contenido
        comentario.editado = True
        comentario.fecha_ultima_edicion = timezone.now()
        comentario.save()
        
        messages.success(request, "Comentario actualizado exitosamente")
        return redirect(f"{comentario.caso_de_uso.get_absolute_url()}#comentario-{comentario.id}")
    
    return redirect('casos_de_uso:detalle', pk=comentario.caso_de_uso.id)


@login_required
def eliminar_comentario_caso(request, comentario_id):
    """Eliminar (soft delete) un comentario."""
    comentario = get_object_or_404(ComentarioCasoDeUso, pk=comentario_id)
    
    if comentario.autor != request.user and not request.user.es_admin_proyecto(comentario.caso_de_uso.proyecto):
        messages.error(request, "No tienes permisos para eliminar este comentario")
        return redirect('casos_de_uso:detalle', pk=comentario.caso_de_uso.id)
    
    if request.method == 'POST':
        comentario.eliminado = True
        comentario.fecha_eliminacion = timezone.now()
        comentario.save()
        
        messages.success(request, "Comentario eliminado exitosamente")
        return redirect('casos_de_uso:detalle', pk=comentario.caso_de_uso.id)
    
    return render(request, 'casos_de_uso/confirmar_eliminar_comentario.html', {
        'comentario': comentario
    })
```

### Template Propuesto

```html
<!-- En casos_de_uso/templates/casos_de_uso/detalle.html -->
<div class="comentarios-section">
    <h3>
        <i class="bi bi-chat-left-text"></i> 
        Comentarios 
        <span class="badge bg-secondary">{{ caso_de_uso.comentarios.filter(eliminado=False).count }}</span>
    </h3>
    
    <!-- Lista de comentarios -->
    <div class="comentarios-list">
        {% for comentario in caso_de_uso.comentarios.filter(eliminado=False, comentario_padre__isnull=True) %}
        <div class="comentario" id="comentario-{{ comentario.id }}" data-autor="{{ comentario.autor.username }}">
            <div class="comentario-header">
                <img src="{{ comentario.autor.avatar_url }}" alt="{{ comentario.autor.nombre }}" class="avatar-sm">
                <strong>{{ comentario.autor.nombre }}</strong>
                <span class="text-muted">{{ comentario.fecha_creacion|date:"d/m/Y H:i" }}</span>
                {% if comentario.editado %}
                    <span class="badge bg-info">(editado {{ comentario.fecha_ultima_edicion|date:"d/m/Y H:i" }})</span>
                {% endif %}
                {% if comentario.tipo != 'NORMAL' %}
                    <span class="badge bg-{{ comentario.tipo == 'PREGUNTA' and 'warning' or comentario.tipo == 'IMPORTANTE' and 'danger' or 'info' }}">
                        {{ comentario.get_tipo_display }}
                    </span>
                {% endif %}
            </div>
            
            <div class="comentario-body" data-original="{{ comentario.contenido }}">
                {{ comentario.contenido_html|safe }}
            </div>
            
            <div class="comentario-actions">
                <button class="btn btn-sm btn-link" onclick="responder({{ comentario.id }})">
                    <i class="bi bi-reply"></i> Responder
                </button>
                
                {% if comentario.autor == request.user %}
                    <button class="btn btn-sm btn-link" onclick="editarComentario({{ comentario.id }})">
                        <i class="bi bi-pencil"></i> Editar
                    </button>
                    <form method="post" action="{% url 'casos_de_uso:eliminar_comentario' comentario.id %}" style="display:inline;">
                        {% csrf_token %}
                        <button type="submit" class="btn btn-sm btn-link text-danger" onclick="return confirm('¿Eliminar este comentario?')">
                            <i class="bi bi-trash"></i> Eliminar
                        </button>
                    </form>
                {% endif %}
            </div>
            
            <!-- Respuestas anidadas -->
            {% if comentario.respuestas.filter(eliminado=False).exists %}
            <div class="respuestas">
                {% for respuesta in comentario.respuestas.filter(eliminado=False) %}
                <div class="comentario comentario-respuesta" id="comentario-{{ respuesta.id }}">
                    <div class="comentario-header">
                        <img src="{{ respuesta.autor.avatar_url }}" alt="{{ respuesta.autor.nombre }}" class="avatar-xs">
                        <strong>{{ respuesta.autor.nombre }}</strong>
                        <span class="text-muted">{{ respuesta.fecha_creacion|date:"d/m/Y H:i" }}</span>
                    </div>
                    <div class="comentario-body">
                        {{ respuesta.contenido_html|safe }}
                    </div>
                </div>
                {% endfor %}
            </div>
            {% endif %}
        </div>
        {% empty %}
        <p class="text-muted">
            <i class="bi bi-chat"></i> No hay comentarios aún. Sé el primero en comentar sobre este caso de uso.
        </p>
        {% endfor %}
    </div>
    
    <!-- Formulario para agregar comentario -->
    {% if user.tiene_permiso_escritura %}
    <div class="agregar-comentario">
        <h4>Agregar comentario</h4>
        <form method="post" action="{% url 'casos_de_uso:agregar_comentario' caso_de_uso.id %}">
            {% csrf_token %}
            <input type="hidden" name="comentario_padre_id" id="comentario_padre_id">
            
            <div class="mb-3">
                <textarea 
                    name="contenido" 
                    class="form-control" 
                    rows="4" 
                    placeholder="Escribe tu comentario sobre este caso de uso... (Soporta Markdown básico)"
                    required
                    minlength="3"
                    maxlength="5000"
                ></textarea>
                <small class="text-muted">
                    💡 Puedes mencionar usuarios con @usuario. 
                    Soporta **negritas**, *cursivas*, [enlaces](url), `código`
                </small>
            </div>
            
            <div class="mb-3">
                <label>Tipo de comentario:</label>
                <div class="btn-group" role="group">
                    <input type="radio" class="btn-check" name="tipo" value="NORMAL" id="tipo-normal" checked>
                    <label class="btn btn-outline-secondary" for="tipo-normal">
                        <i class="bi bi-chat"></i> Normal
                    </label>
                    
                    <input type="radio" class="btn-check" name="tipo" value="PREGUNTA" id="tipo-pregunta">
                    <label class="btn btn-outline-warning" for="tipo-pregunta">
                        <i class="bi bi-question-circle"></i> Pregunta
                    </label>
                    
                    <input type="radio" class="btn-check" name="tipo" value="IMPORTANTE" id="tipo-importante">
                    <label class="btn btn-outline-danger" for="tipo-importante">
                        <i class="bi bi-exclamation-triangle"></i> Importante
                    </label>
                    
                    <input type="radio" class="btn-check" name="tipo" value="DECISION" id="tipo-decision">
                    <label class="btn btn-outline-info" for="tipo-decision">
                        <i class="bi bi-check-circle"></i> Decisión
                    </label>
                </div>
            </div>
            
            <button type="submit" class="btn btn-primary">
                <i class="bi bi-send"></i> Publicar comentario
            </button>
        </form>
    </div>
    {% else %}
    <div class="alert alert-warning">
        <i class="bi bi-lock"></i> No tienes permisos para comentar en este proyecto.
    </div>
    {% endif %}
</div>

<style>
/* Estilos para comentarios */
.comentarios-section {
    margin-top: 3rem;
    padding-top: 2rem;
    border-top: 2px solid #dee2e6;
}

.comentario {
    background-color: #f8f9fa;
    border-left: 3px solid #007bff;
    padding: 1rem;
    margin-bottom: 1rem;
    border-radius: 0.25rem;
}

.comentario-respuesta {
    margin-left: 2rem;
    border-left-color: #6c757d;
    background-color: #e9ecef;
}

.comentario-header {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 0.5rem;
}

.avatar-sm {
    width: 32px;
    height: 32px;
    border-radius: 50%;
}

.avatar-xs {
    width: 24px;
    height: 24px;
    border-radius: 50%;
}

.comentario-actions {
    margin-top: 0.5rem;
    display: flex;
    gap: 0.5rem;
}

.agregar-comentario {
    margin-top: 2rem;
    padding: 1.5rem;
    background-color: #ffffff;
    border: 1px solid #dee2e6;
    border-radius: 0.5rem;
}
</style>
```

### Casos de Uso Típicos de Comentarios en Casos de Uso

**Ejemplo 1: Pregunta sobre flujo alternativo**
```
@maria_dev: En el flujo alternativo 2a, ¿qué pasa si el usuario cancela la operación? 
¿Debemos volver al paso 3 o al inicio?

Tipo: PREGUNTA
```

**Ejemplo 2: Decisión de diseño**
```
Decidimos usar paginación de 20 elementos en lugar de 50 para mejorar el rendimiento. 
Se actualizó el paso 5 del flujo principal en consecuencia.

Tipo: DECISION
```

**Ejemplo 3: Aclaración técnica**
```
Nota para implementación: La validación del campo "email" debe usar regex según RFC 5322. 
No solo verificar presencia de @.

Tipo: IMPORTANTE
```

**Ejemplo 4: Feedback de revisión**
```
@juan_analista: Sugiero agregar un flujo alternativo para cuando el servicio externo no responde 
(timeout). Es un caso común que debemos manejar.

Tipo: NORMAL
```

### Estado de Implementación
⏳ **PLANIFICADO PARA IMPLEMENTACIÓN PRÓXIMA**

**Análisis del código actual:**
- ❌ NO existe modelo `ComentarioCasoDeUso` (aún)
- ❌ Solo existe campo `observaciones` en `DetalleCasoDeUsoTradicional` y `DetalleCasoDeUsoAgil` (no es lo mismo)
- ❌ Campo `observaciones` es un `TextField` simple, NO soporta múltiples comentarios colaborativos
- ❌ NO hay vistas para agregar/editar/eliminar comentarios (pendiente)
- ❌ NO hay templates con sección de comentarios (pendiente)
- ❌ NO hay sistema de notificaciones (pendiente)

**📋 Funcionalidad planificada:**
- ✅ Se implementará sistema de comentarios completo
- ✅ **Idéntico a CU-18** pero para casos de uso
- ✅ Todos los usuarios del proyecto podrán comentar
- ✅ Incluirá autor, fecha, edición, eliminación, respuestas anidadas
- ✅ Soporte de Markdown y menciones con @usuario
- ✅ Tipos de comentario: Normal, Pregunta, Importante, Decisión

**Diferencia clave:**
- `observaciones` (campo actual) = TextField simple sin metadatos ni colaboración
- Comentarios (planificado) = sistema colaborativo completo con trazabilidad

### Prioridad de Implementación
🟢 **ALTA - EN PLANIFICACIÓN** - Funcionalidad de colaboración crítica:
- Idéntica importancia a CU-18 (Comentar requerimiento)
- Facilita discusión sobre diseño e implementación
- Los casos de uso requieren más aclaraciones técnicas que los requerimientos
- Desarrolladores necesitan clarificar detalles de flujos y excepciones
- Permite feedback de revisión por pares
- **Se implementará junto con CU-18 (misma infraestructura, diferentes modelos)**
- Reduce malentendidos en la etapa de implementación

### Observaciones de Revisión
✅ **Correcciones aplicadas:**
- Reconocido que es funcionalidad planificada (no implementada aún)
- Especificado que es **idéntica a CU-18** pero para casos de uso
- Confirmado que todos los usuarios del proyecto podrán comentar
- Modelo `ComentarioCasoDeUso` paralelo a `ComentarioRequerimiento`
- Vistas y templates similares a CU-18 pero en app `casos_de_uso`
- Incluidos ejemplos de uso típico en casos de uso (preguntas técnicas, decisiones de diseño)
- **NOTA CRÍTICA:** El campo `observaciones` actual NO es lo mismo que comentarios colaborativos
- Se implementará próximamente con la misma infraestructura que CU-18

---

## CU-20: Validar requerimiento

### Descripción
El sistema permite a los usuarios con permisos apropiados (analistas senior, líderes de proyecto, PO) **validar o rechazar requerimientos** mediante un proceso de revisión formal.

La validación de requerimientos asegura que:
- **Completitud:** el requerimiento está completamente especificado
- **Claridad:** es comprensible para todos los stakeholders
- **Consistencia:** no contradice otros requerimientos
- **Viabilidad:** es técnicamente factible y económicamente viable
- **Trazabilidad:** está correctamente vinculado a objetivos del negocio
- **Verificabilidad:** se puede comprobar su cumplimiento (criterios de aceptación claros)

Estados de validación típicos:
- **Pendiente validación:** estado inicial, requiere revisión
- **En revisión:** está siendo evaluado por el validador
- **Aprobado:** cumple todos los criterios, listo para implementación
- **Rechazado:** no cumple criterios, requiere correcciones
- **Aprobado con observaciones:** aceptado pero con comentarios para mejorar
- **Revalidación requerida:** aprobado previamente pero modificado, requiere nueva validación

### Actores
- **Validador principal:** Analista senior, Líder del proyecto, Product Owner
- **Solicitante:** Usuario que creó el requerimiento (recibe notificación del resultado)
- **Stakeholders:** Pueden ser consultados durante la validación

### Precondiciones
- Requerimiento existente en estado "Pendiente" o "En progreso"
- Usuario autenticado con permisos de validación
- Requerimiento con información mínima completa (nombre, descripción, tipo)
- Proyecto en metodología TRADICIONAL (el campo `estado_validacion` solo existe en `DetalleRequerimientoTradicional`)

### Postcondiciones
- Campo `estado_validacion` actualizado en `DetalleRequerimientoTradicional`
- Fecha de validación registrada
- Observaciones de validación guardadas (opcional)
- Notificación enviada al creador del requerimiento
- Si es aprobado: requerimiento puede pasar a diseño (creación de casos de uso)
- Si es rechazado: requerimiento vuelve a estado "Pendiente" para corrección

### Flujo Principal
1. El validador accede al proyecto
2. El validador navega a la lista de requerimientos
3. El sistema muestra filtro "Requerimientos pendientes de validación"
4. El validador selecciona un requerimiento sin validar o con `estado_validacion` vacío/pendiente
5. El validador hace clic en "Validar requerimiento" o accede al detalle
6. El sistema muestra formulario de validación con:
   - Datos completos del requerimiento (nombre, descripción, tipo, prioridad, fuente, etc.)
   - Casos de uso vinculados (si existen)
   - Historial de cambios (si existe CU-08)
   - Comentarios existentes (si existe CU-18)
   - Checklist de validación:
     * ✓ ¿El requerimiento es claro y comprensible?
     * ✓ ¿Está completo (todos los campos obligatorios)?
     * ✓ ¿Es consistente con otros requerimientos?
     * ✓ ¿Es viable técnica y económicamente?
     * ✓ ¿Tiene criterios de aceptación claros?
     * ✓ ¿La prioridad es correcta?
   - Opciones de decisión:
     * 🟢 Aprobar
     * 🟡 Aprobar con observaciones
     * 🔴 Rechazar
   - Campo de observaciones (obligatorio si rechaza)
7. El validador revisa el requerimiento completo
8. El validador marca los ítems del checklist (opcional)
9. El validador selecciona una decisión (Aprobar / Aprobar con observaciones / Rechazar)
10. Si rechaza o aprueba con observaciones, el validador escribe justificación en "Observaciones"
11. El validador hace clic en "Confirmar validación"
12. El sistema valida:
    - Decisión seleccionada
    - Si rechazó: observaciones no vacías (mínimo 10 caracteres)
    - Usuario tiene permisos de validación
13. El sistema actualiza el requerimiento:
    ```python
    detalle = requerimiento.detalle_tradicional
    detalle.estado_validacion = estado_seleccionado  # 'APROBADO', 'RECHAZADO', etc.
    # Agregar campos adicionales (si se agregan al modelo):
    # detalle.validado_por = request.user
    # detalle.fecha_validacion = now()
    # detalle.observaciones_validacion = observaciones
    detalle.save()
    ```
14. Si rechazado:
    - El sistema cambia `requerimiento.estado` a "PENDIENTE"
    - El sistema crea comentario automático (si existe CU-18):
      ```
      "❌ Requerimiento rechazado en validación por [Validador]
      Motivo: [observaciones]
      Requiere correcciones antes de continuar."
      ```
15. Si aprobado:
    - El sistema permite cambiar `requerimiento.estado` a "COMPLETADO" (opcional)
    - El sistema crea comentario automático:
      ```
      "✅ Requerimiento aprobado por [Validador]"
      ```
16. El sistema envía notificación al creador del requerimiento:
    - Email: "Tu requerimiento [nombre] ha sido [aprobado/rechazado]"
    - Notificación en plataforma con enlace al requerimiento
17. El sistema registra la validación en historial (si existe CU-08)
18. El sistema muestra mensaje: "Requerimiento validado exitosamente"
19. El sistema redirige a la lista de requerimientos

### Flujo Alternativo A - Aprobar con Observaciones
1. El validador selecciona "Aprobar con observaciones"
2. El validador escribe comentarios/sugerencias de mejora
3. El validador hace clic en "Confirmar validación"
4. El sistema actualiza `estado_validacion = "APROBADO_CON_OBSERVACIONES"`
5. El sistema crea comentario con las observaciones
6. El sistema envía notificación al creador:
   - "Tu requerimiento ha sido aprobado con observaciones. Revisa los comentarios del validador."
7. El requerimiento puede continuar a diseño (casos de uso)
8. El creador puede opcionalmente aplicar las mejoras sugeridas

### Flujo Alternativo B - Solicitar Revalidación
1. Un requerimiento previamente aprobado es modificado significativamente
2. El sistema detecta cambios en campos críticos (nombre, descripción, tipo)
3. El sistema cambia automáticamente `estado_validacion = "REVALIDACION_REQUERIDA"`
4. El sistema envía notificación al validador original (si se registró):
   - "El requerimiento [nombre] que validaste ha sido modificado y requiere revalidación"
5. El validador revisa los cambios (diff)
6. El validador revalida siguiendo el flujo principal

### Flujo Alternativo C - Validación Colaborativa
1. El validador principal inicia la validación
2. El validador hace clic en "Solicitar revisión adicional"
3. El sistema muestra lista de otros validadores del proyecto
4. El validador selecciona uno o más revisores
5. El sistema envía notificaciones a los revisores
6. Cada revisor agrega sus comentarios/observaciones
7. El validador principal toma la decisión final considerando los comentarios
8. El validador principal confirma la validación

### Flujos Alternativos de Error
**12a. Usuario sin permisos de validación**
- El sistema detecta que el usuario no tiene rol de validador
- Muestra error: "No tienes permisos para validar requerimientos"
- No muestra formulario de validación
- Muestra solo botón "Solicitar validación a un líder"

**12b. Observaciones vacías al rechazar**
- El sistema detecta rechazo sin justificación
- Muestra error: "Debes proporcionar motivos de rechazo (mínimo 10 caracteres)"
- No guarda la validación
- Mantiene el foco en el campo de observaciones
- Destaca el campo en rojo

**13a. Requerimiento ya validado**
- El sistema detecta que `estado_validacion` ya tiene un valor aprobado
- Muestra advertencia: "Este requerimiento ya fue validado por [usuario] el [fecha]"
- Pregunta: "¿Deseas revalidar? Esto sobrescribirá la validación anterior"
- Usuario confirma o cancela

**13b. Requerimiento incompleto**
- El sistema detecta campos obligatorios vacíos (nombre, descripción, tipo)
- Muestra error: "El requerimiento está incompleto. Campos faltantes: [lista]"
- Sugiere: "Completa el requerimiento antes de validar"
- No permite validar hasta que esté completo

**17a. Error al enviar notificación**
- El sistema captura excepción al enviar notificación
- Registra error en logs
- La validación se guarda exitosamente (no falla)
- Muestra advertencia: "Validación guardada, pero no se pudo notificar al creador"

### Flujo Opcional - Validación en Lote
1. El validador selecciona múltiples requerimientos (checkboxes)
2. El validador hace clic en "Validar seleccionados"
3. El sistema muestra modal con decisión única para todos:
   - Aprobar todos
   - Rechazar todos (con observaciones comunes)
4. El validador selecciona decisión y escribe observaciones (si aplica)
5. El validador confirma
6. El sistema valida todos los requerimientos seleccionados
7. El sistema muestra resumen: "X requerimientos aprobados, Y rechazados"

### Flujo Opcional - Exportar Informe de Validación
1. El validador hace clic en "Exportar informe de validación"
2. El sistema genera PDF con:
   - Lista de requerimientos validados
   - Estado de cada uno (Aprobado/Rechazado)
   - Observaciones de validación
   - Fecha y validador
   - Estadísticas: % aprobados, % rechazados
3. El sistema descarga el PDF

### Reglas de Negocio
- RN-01: Solo usuarios con rol de "Validador", "Líder de Proyecto" o "Product Owner" pueden validar
- RN-02: Campo `estado_validacion` solo existe en metodología TRADICIONAL
- RN-03: Requerimientos rechazados deben incluir observaciones (mínimo 10 caracteres)
- RN-04: Requerimientos aprobados pueden pasar directamente a diseño (creación de casos de uso)
- RN-05: Modificar un requerimiento aprobado debe marcar "Revalidación requerida"
- RN-06: Solo campos críticos (nombre, descripción, tipo) requieren revalidación al cambiar
- RN-07: Cambios menores (observaciones, categoría) NO requieren revalidación
- RN-08: Se recomienda validar antes de crear casos de uso (evitar diseño de req. inválidos)
- RN-09: Un requerimiento puede ser revalidado múltiples veces
- RN-10: Historial de validaciones debe conservarse (no sobrescribir, agregar registro)
- RN-11: Notificación al creador es obligatoria (éxito o fallo debe informarse)
- RN-12: Estados sugeridos: PENDIENTE, EN_REVISION, APROBADO, RECHAZADO, APROBADO_CON_OBSERVACIONES, REVALIDACION_REQUERIDA
- RN-13: En metodología ÁGIL, la validación es más informal (PO en daily standup o sprint planning)

### Modelo Actual y Propuestas de Mejora

**Modelo actual:**
```python
# En requerimientos/models.py - DetalleRequerimientoTradicional
estado_validacion = models.CharField(max_length=100, blank=True)
# ✅ Campo existe
# ❌ Es CharField genérico sin choices
# ❌ No registra quién validó ni cuándo
# ❌ No tiene campo separado para observaciones de validación
```

**Mejoras propuestas:**
```python
# En requerimientos/models.py - DetalleRequerimientoTradicional
class DetalleRequerimientoTradicional(models.Model):
    # ... campos existentes ...
    
    # Validación mejorada
    ESTADO_VALIDACION_CHOICES = [
        ('PENDIENTE', 'Pendiente validación'),
        ('EN_REVISION', 'En revisión'),
        ('APROBADO', 'Aprobado'),
        ('RECHAZADO', 'Rechazado'),
        ('APROBADO_CON_OBSERVACIONES', 'Aprobado con observaciones'),
        ('REVALIDACION_REQUERIDA', 'Revalidación requerida'),
    ]
    
    estado_validacion = models.CharField(
        max_length=100,
        choices=ESTADO_VALIDACION_CHOICES,
        default='PENDIENTE',
        blank=True
    )
    
    # Campos adicionales recomendados
    validado_por = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='requerimientos_validados',
        verbose_name="Validado por"
    )
    fecha_validacion = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Fecha de validación"
    )
    observaciones_validacion = models.TextField(
        blank=True,
        verbose_name="Observaciones del validador",
        help_text="Motivos de rechazo o comentarios de aprobación"
    )
    
    # Campo existente (para observaciones generales, no solo validación)
    observaciones = models.TextField(blank=True)
```

**Modelo de Historial de Validaciones (recomendado):**
```python
# En requerimientos/models.py
class HistorialValidacion(models.Model):
    """Registra todas las validaciones de un requerimiento."""
    requerimiento = models.ForeignKey(
        Requerimiento,
        on_delete=models.CASCADE,
        related_name='historial_validaciones'
    )
    validador = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        related_name='validaciones_realizadas'
    )
    fecha = models.DateTimeField(auto_now_add=True)
    
    DECISION_CHOICES = [
        ('APROBADO', 'Aprobado'),
        ('RECHAZADO', 'Rechazado'),
        ('APROBADO_CON_OBSERVACIONES', 'Aprobado con observaciones'),
    ]
    decision = models.CharField(max_length=50, choices=DECISION_CHOICES)
    observaciones = models.TextField(blank=True)
    
    # Checklist (opcional, como JSONField)
    checklist = models.JSONField(
        default=dict,
        blank=True,
        help_text="Checklist de validación completado"
    )
    
    class Meta:
        ordering = ['-fecha']
        verbose_name = 'Historial de Validación'
        verbose_name_plural = 'Historiales de Validación'
    
    def __str__(self):
        return f"{self.decision} por {self.validador} - {self.fecha.strftime('%d/%m/%Y')}"
```

### Vista Propuesta

```python
# En requerimientos/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.utils import timezone

@login_required
def validar_requerimiento(request, requerimiento_id):
    """Vista para validar un requerimiento."""
    requerimiento = get_object_or_404(Requerimiento, pk=requerimiento_id)
    
    # Verificar permisos de validación
    if not request.user.puede_validar_requerimientos(requerimiento.proyecto):
        messages.error(request, "No tienes permisos para validar requerimientos")
        return redirect('requerimientos:detalle', pk=requerimiento.id)
    
    # Verificar metodología (solo TRADICIONAL tiene estado_validacion)
    if requerimiento.proyecto.metodologia != 'TRADICIONAL':
        messages.warning(request, "La validación formal solo aplica en metodología tradicional")
        return redirect('requerimientos:detalle', pk=requerimiento.id)
    
    # Verificar que existe detalle tradicional
    if not requerimiento.detalle_tradicional:
        messages.error(request, "Este requerimiento no tiene detalle tradicional")
        return redirect('requerimientos:detalle', pk=requerimiento.id)
    
    if request.method == 'POST':
        decision = request.POST.get('decision')  # APROBADO, RECHAZADO, APROBADO_CON_OBSERVACIONES
        observaciones = request.POST.get('observaciones', '').strip()
        
        # Validaciones
        if not decision:
            messages.error(request, "Debes seleccionar una decisión (Aprobar o Rechazar)")
            return redirect('requerimientos:validar', requerimiento_id=requerimiento.id)
        
        if decision == 'RECHAZADO' and len(observaciones) < 10:
            messages.error(request, "Debes proporcionar motivos de rechazo (mínimo 10 caracteres)")
            return redirect('requerimientos:validar', requerimiento_id=requerimiento.id)
        
        # Actualizar estado de validación
        detalle = requerimiento.detalle_tradicional
        detalle.estado_validacion = decision
        
        # Si se agregaron campos adicionales al modelo:
        # detalle.validado_por = request.user
        # detalle.fecha_validacion = timezone.now()
        # detalle.observaciones_validacion = observaciones
        
        detalle.save()
        
        # Si se implementó HistorialValidacion:
        # HistorialValidacion.objects.create(
        #     requerimiento=requerimiento,
        #     validador=request.user,
        #     decision=decision,
        #     observaciones=observaciones
        # )
        
        # Cambiar estado del requerimiento si rechazado
        if decision == 'RECHAZADO':
            requerimiento.estado = 'PENDIENTE'
            requerimiento.save()
            
            # Crear comentario automático (si existe CU-18)
            # ComentarioRequerimiento.objects.create(...)
        
        elif decision == 'APROBADO':
            # Opcional: cambiar a COMPLETADO
            # requerimiento.estado = 'COMPLETADO'
            # requerimiento.save()
            pass
        
        # Enviar notificación al creador
        enviar_notificacion_validacion(requerimiento, decision, observaciones, request.user)
        
        messages.success(request, f"Requerimiento {decision.lower()} exitosamente")
        return redirect('requerimientos:detalle', pk=requerimiento.id)
    
    # GET: mostrar formulario de validación
    detalle = requerimiento.detalle_tradicional
    
    # Checklist de validación
    checklist = [
        {'id': 'claro', 'texto': '¿El requerimiento es claro y comprensible?'},
        {'id': 'completo', 'texto': '¿Está completo (todos los campos necesarios)?'},
        {'id': 'consistente', 'texto': '¿Es consistente con otros requerimientos?'},
        {'id': 'viable', 'texto': '¿Es viable técnica y económicamente?'},
        {'id': 'verificable', 'texto': '¿Tiene criterios de aceptación claros?'},
        {'id': 'prioridad', 'texto': '¿La prioridad es correcta?'},
    ]
    
    return render(request, 'requerimientos/validar.html', {
        'requerimiento': requerimiento,
        'detalle': detalle,
        'checklist': checklist,
        'casos_vinculados': requerimiento.casos_relacionados.all(),
        'ya_validado': bool(detalle.estado_validacion and detalle.estado_validacion != 'PENDIENTE')
    })


def enviar_notificacion_validacion(requerimiento, decision, observaciones, validador):
    """Envía notificación al creador del requerimiento."""
    if not requerimiento.creado_por:
        return
    
    creador = requerimiento.creado_por
    
    # Email
    asunto = f"Requerimiento {requerimiento.nombre} - {decision}"
    
    if decision == 'APROBADO':
        mensaje = f"Tu requerimiento '{requerimiento.nombre}' ha sido aprobado por {validador.nombre}."
    elif decision == 'RECHAZADO':
        mensaje = f"Tu requerimiento '{requerimiento.nombre}' ha sido rechazado por {validador.nombre}.\n\nMotivo: {observaciones}\n\nPor favor, realiza las correcciones necesarias."
    else:  # APROBADO_CON_OBSERVACIONES
        mensaje = f"Tu requerimiento '{requerimiento.nombre}' ha sido aprobado con observaciones por {validador.nombre}.\n\nObservaciones: {observaciones}"
    
    # Enviar email (si está configurado)
    try:
        from django.core.mail import send_mail
        send_mail(
            subject=asunto,
            message=mensaje,
            from_email='noreply@grcu-manager.com',
            recipient_list=[creador.email],
            fail_silently=True
        )
    except Exception as e:
        print(f"Error al enviar email: {e}")
    
    # Crear notificación en plataforma (si existe modelo de notificaciones)
    # Notificacion.objects.create(...)
```

### Template Propuesto

```html
<!-- En requerimientos/templates/requerimientos/validar.html -->
{% extends "base.html" %}

{% block title %}Validar Requerimiento - {{ requerimiento.nombre }}{% endblock %}

{% block content %}
<div class="container mt-4">
    <h2>
        <i class="bi bi-check-circle"></i> Validar Requerimiento
    </h2>
    
    {% if ya_validado %}
    <div class="alert alert-warning">
        <i class="bi bi-exclamation-triangle"></i>
        <strong>Atención:</strong> Este requerimiento ya fue validado anteriormente.
        Estado actual: <strong>{{ detalle.estado_validacion }}</strong>
        {% if detalle.fecha_validacion %}
        el {{ detalle.fecha_validacion|date:"d/m/Y H:i" }}
        {% endif %}
        <br>
        Si continúas, se sobrescribirá la validación anterior.
    </div>
    {% endif %}
    
    <!-- Información del requerimiento -->
    <div class="card mb-4">
        <div class="card-header bg-primary text-white">
            <h4 class="mb-0">{{ requerimiento.nombre }}</h4>
        </div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-6">
                    <p><strong>Tipo:</strong> {{ requerimiento.get_tipo_display }}</p>
                    <p><strong>Estado:</strong> {{ requerimiento.get_estado_display }}</p>
                    <p><strong>Prioridad:</strong> {{ detalle.prioridad|default:"Sin prioridad" }}</p>
                </div>
                <div class="col-md-6">
                    <p><strong>Fuente:</strong> {{ detalle.fuente|default:"No especificada" }}</p>
                    <p><strong>Categoría:</strong> {{ detalle.categoria|default:"Sin categoría" }}</p>
                    <p><strong>Creado por:</strong> {{ requerimiento.creado_por.nombre|default:"Desconocido" }}</p>
                </div>
            </div>
            
            <hr>
            
            <h5>Descripción:</h5>
            <p>{{ requerimiento.descripcion|default:"Sin descripción" }}</p>
            
            {% if casos_vinculados %}
            <hr>
            <h5>Casos de Uso Vinculados:</h5>
            <ul>
                {% for caso in casos_vinculados %}
                <li>
                    <a href="{% url 'casos_de_uso:detalle' caso.id %}" target="_blank">
                        {{ caso.nombre }}
                    </a>
                </li>
                {% endfor %}
            </ul>
            {% endif %}
            
            {% if detalle.observaciones %}
            <hr>
            <h5>Observaciones:</h5>
            <p>{{ detalle.observaciones }}</p>
            {% endif %}
        </div>
    </div>
    
    <!-- Formulario de validación -->
    <div class="card">
        <div class="card-header bg-info text-white">
            <h4 class="mb-0">
                <i class="bi bi-clipboard-check"></i> Checklist de Validación
            </h4>
        </div>
        <div class="card-body">
            <form method="post">
                {% csrf_token %}
                
                <!-- Checklist -->
                <div class="mb-4">
                    <p class="text-muted">
                        Revisa los siguientes aspectos antes de validar:
                    </p>
                    {% for item in checklist %}
                    <div class="form-check">
                        <input 
                            class="form-check-input" 
                            type="checkbox" 
                            id="check-{{ item.id }}"
                            name="checklist_{{ item.id }}"
                        >
                        <label class="form-check-label" for="check-{{ item.id }}">
                            {{ item.texto }}
                        </label>
                    </div>
                    {% endfor %}
                </div>
                
                <hr>
                
                <!-- Decisión -->
                <div class="mb-4">
                    <h5>Decisión de Validación <span class="text-danger">*</span></h5>
                    <div class="btn-group w-100" role="group">
                        <input 
                            type="radio" 
                            class="btn-check" 
                            name="decision" 
                            value="APROBADO" 
                            id="decision-aprobado"
                            required
                        >
                        <label class="btn btn-outline-success" for="decision-aprobado">
                            <i class="bi bi-check-circle"></i> Aprobar
                        </label>
                        
                        <input 
                            type="radio" 
                            class="btn-check" 
                            name="decision" 
                            value="APROBADO_CON_OBSERVACIONES" 
                            id="decision-obs"
                        >
                        <label class="btn btn-outline-warning" for="decision-obs">
                            <i class="bi bi-check-circle-fill"></i> Aprobar con observaciones
                        </label>
                        
                        <input 
                            type="radio" 
                            class="btn-check" 
                            name="decision" 
                            value="RECHAZADO" 
                            id="decision-rechazado"
                        >
                        <label class="btn btn-outline-danger" for="decision-rechazado">
                            <i class="bi bi-x-circle"></i> Rechazar
                        </label>
                    </div>
                </div>
                
                <!-- Observaciones -->
                <div class="mb-4">
                    <label for="observaciones" class="form-label">
                        <h5>
                            Observaciones / Motivos 
                            <span class="text-danger" id="obs-requerido" style="display:none;">*</span>
                        </h5>
                    </label>
                    <textarea 
                        class="form-control" 
                        id="observaciones" 
                        name="observaciones" 
                        rows="5"
                        placeholder="Escribe aquí los motivos de rechazo o comentarios/sugerencias de mejora..."
                    ></textarea>
                    <small class="text-muted">
                        <span id="help-rechazar" style="display:none;">
                            <i class="bi bi-exclamation-circle text-danger"></i>
                            <strong>Obligatorio al rechazar:</strong> Explica claramente qué debe corregirse (mínimo 10 caracteres)
                        </span>
                        <span id="help-aprobar-obs" style="display:none;">
                            <i class="bi bi-info-circle text-warning"></i>
                            <strong>Opcional pero recomendado:</strong> Sugerencias para mejorar el requerimiento
                        </span>
                    </small>
                </div>
                
                <!-- Botones -->
                <div class="d-flex justify-content-between">
                    <a href="{% url 'requerimientos:detalle' requerimiento.id %}" class="btn btn-secondary">
                        <i class="bi bi-arrow-left"></i> Cancelar
                    </a>
                    <button type="submit" class="btn btn-primary btn-lg">
                        <i class="bi bi-save"></i> Confirmar Validación
                    </button>
                </div>
            </form>
        </div>
    </div>
</div>

<script>
// Mostrar/ocultar ayuda según decisión seleccionada
document.querySelectorAll('input[name="decision"]').forEach(radio => {
    radio.addEventListener('change', function() {
        const decision = this.value;
        
        // Ocultar todos los mensajes
        document.getElementById('help-rechazar').style.display = 'none';
        document.getElementById('help-aprobar-obs').style.display = 'none';
        document.getElementById('obs-requerido').style.display = 'none';
        
        // Mostrar el mensaje correspondiente
        if (decision === 'RECHAZADO') {
            document.getElementById('help-rechazar').style.display = 'inline';
            document.getElementById('obs-requerido').style.display = 'inline';
            document.getElementById('observaciones').required = true;
        } else if (decision === 'APROBADO_CON_OBSERVACIONES') {
            document.getElementById('help-aprobar-obs').style.display = 'inline';
            document.getElementById('observaciones').required = false;
        } else {
            document.getElementById('observaciones').required = false;
        }
    });
});

// Validación de formulario
document.querySelector('form').addEventListener('submit', function(e) {
    const decision = document.querySelector('input[name="decision"]:checked');
    
    if (!decision) {
        e.preventDefault();
        alert('Debes seleccionar una decisión (Aprobar o Rechazar)');
        return false;
    }
    
    if (decision.value === 'RECHAZADO') {
        const observaciones = document.getElementById('observaciones').value.trim();
        if (observaciones.length < 10) {
            e.preventDefault();
            alert('Debes proporcionar motivos de rechazo (mínimo 10 caracteres)');
            document.getElementById('observaciones').focus();
            return false;
        }
    }
});
</script>
{% endblock %}
```

### Flujo de Validación Visual

```
┌─────────────────────────────────────────────────────────┐
│ REQUERIMIENTO CREADO                                    │
│ estado_validacion = "PENDIENTE" (o vacío)              │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
         ┌────────────────┐
         │   VALIDADOR    │
         │    REVISA      │
         └────────┬───────┘
                  │
        ┌─────────┴─────────┐
        │                   │
        ▼                   ▼
┌───────────────┐   ┌───────────────┐
│   APROBAR     │   │   RECHAZAR    │
└───────┬───────┘   └───────┬───────┘
        │                   │
        ▼                   ▼
estado_validacion    estado_validacion
= "APROBADO"        = "RECHAZADO"
        │            requerimiento.estado
        │            = "PENDIENTE"
        │                   │
        ▼                   ▼
  Puede pasar          Requiere
  a diseño            correcciones
  (crear CU)               │
        │                   │
        │                   ▼
        │            ┌─────────────┐
        │            │  CORRECCIONES│
        │            └──────┬───────┘
        │                   │
        │                   ▼
        │            estado_validacion
        │            = "REVALIDACION_REQUERIDA"
        │                   │
        └───────────────────┘
                    │
                    ▼
            CICLO SE REPITE
```

### Estado de Implementación
⚠️ **PARCIALMENTE IMPLEMENTADO**

**✅ Implementado:**
- Campo `estado_validacion` en `DetalleRequerimientoTradicional`
- Es CharField de 100 caracteres, blank=True

**❌ NO implementado:**
- No tiene choices definidos (es CharField genérico)
- NO registra quién validó (`validado_por`)
- NO registra cuándo se validó (`fecha_validacion`)
- NO tiene campo separado para observaciones de validación
- NO hay vista para validar requerimientos
- NO hay template de validación
- NO hay checklist de validación
- NO hay notificaciones al creador
- NO hay historial de validaciones
- NO hay validación en lote
- Solo existe en metodología TRADICIONAL (correcto según diseño)

**Mejoras recomendadas:**
1. Agregar choices al campo `estado_validacion`
2. Agregar campos `validado_por`, `fecha_validacion`, `observaciones_validacion`
3. Crear modelo `HistorialValidacion` para trazabilidad completa
4. Implementar vista y template de validación
5. Implementar notificaciones
6. Agregar permisos específicos para validadores

### Prioridad de Implementación
🟡 **MEDIA** - Importante para calidad pero no crítico:
- Mejora significativamente la calidad de requerimientos
- Previene diseño e implementación de requisitos incorrectos
- El campo ya existe (solo necesita lógica de negocio)
- Común en metodologías tradicionales y procesos formales
- No es crítico en proyectos pequeños o metodología ágil
- En ágil, PO valida informalmente en grooming/planning
- Complementa CU-01 (Registrar requerimiento) y CU-18 (Comentar)

### Observaciones de Revisión
✅ **Correcciones aplicadas:**
- Reconocido que el campo `estado_validacion` YA EXISTE en el modelo
- Es CharField simple sin choices ni metadatos de validación
- Propuestas mejoras: choices, validado_por, fecha_validacion
- Propuesto modelo `HistorialValidacion` para trazabilidad completa
- Vista y template completos con checklist
- Flujo de notificaciones al creador
- JavaScript para validación de formulario
- Solo aplica a metodología TRADICIONAL (correcto)
- Incluido flujo de revalidación cuando se modifica un req. aprobado
- Validación en lote como funcionalidad opcional
- Diagrama de flujo visual del proceso de validación

---

## CU-21: Generar informe

### Descripción
El sistema permite a los usuarios generar **informes profesionales** sobre diferentes aspectos del proyecto de gestión de requerimientos y casos de uso, exportables en múltiples formatos (PDF, Excel, CSV).

Los informes disponibles incluyen:
- **Informe de Requerimientos:** listado completo con prioridades, estados, validación, trazabilidad
- **Informe de Casos de Uso:** listado con criticidad, actores, complejidad, comentarios
- **Matriz de Trazabilidad:** relaciones entre requerimientos y casos de uso con cobertura
- **Informe de Validación:** requerimientos aprobados/rechazados con estadísticas
- **Informe de Progreso:** avance del proyecto por estados y completitud
- **Informe de Actividades:** historial de cambios y acciones de usuarios
- **Informe de Huérfanos:** requerimientos sin casos de uso y casos sin requerimientos
- **Informe Ejecutivo:** resumen de alto nivel para stakeholders

Objetivos de los informes:
- **Comunicación con stakeholders:** presentar avances de forma profesional
- **Toma de decisiones:** datos y métricas para planificación
- **Auditoría y cumplimiento:** evidencia documental del proceso
- **Análisis de calidad:** identificar gaps, huérfanos, inconsistencias
- **Documentación del proyecto:** registros formales para archivo
- **Presentaciones:** material para reuniones y revisiones

### Actores
- **Líder del proyecto** (genera informes ejecutivos y de progreso)
- **Analista** (genera informes técnicos de requerimientos y casos de uso)
- **Auditor/QA** (genera informes de validación y trazabilidad)
- **Product Owner** (genera informes de priorización y progreso)
- **Stakeholders** (reciben informes ejecutivos)

### Precondiciones
- Proyecto existente con al menos un requerimiento o caso de uso
- Usuario autenticado con permisos de lectura en el proyecto
- Datos suficientes para generar el informe solicitado

### Postcondiciones
- Informe generado en el formato solicitado (PDF/Excel/CSV)
- Archivo descargado al dispositivo del usuario
- Registro de generación de informe en logs (opcional)
- Sin cambios en la base de datos (solo lectura)

### Flujo Principal
1. El usuario navega al proyecto
2. El usuario hace clic en "Reportes" o "Generar informe" en el menú
3. El sistema muestra la página de reportes con opciones disponibles
4. El sistema lista los tipos de informes:
   - 📊 Informe de Requerimientos
   - 📋 Informe de Casos de Uso
   - 🔗 Matriz de Trazabilidad
   - ✅ Informe de Validación
   - 📈 Informe de Progreso
   - 🕒 Informe de Actividades
   - 👻 Informe de Huérfanos
   - 📄 Informe Ejecutivo
5. El usuario selecciona un tipo de informe
6. El sistema muestra opciones de configuración:
   - **Formato:** PDF, Excel, CSV
   - **Filtros:** estado, tipo, prioridad, fecha
   - **Orden:** nombre, fecha, prioridad
   - **Inclusiones:** comentarios, historial, estadísticas
   - **Idioma:** español, inglés (opcional)
7. El usuario configura las opciones según sus necesidades
8. El usuario hace clic en "Generar informe"
9. El sistema valida:
   - Formato seleccionado
   - Hay datos para incluir en el informe
   - Usuario tiene permisos de lectura
10. El sistema muestra mensaje: "Generando informe..."
11. El sistema ejecuta consultas según el tipo de informe:
    ```python
    if tipo == 'requerimientos':
        datos = Requerimiento.objects.filter(proyecto=proyecto).select_related(...)
    elif tipo == 'casos_uso':
        datos = CasoDeUso.objects.filter(proyecto=proyecto).select_related(...)
    elif tipo == 'matriz':
        # Consultas complejas de trazabilidad
        datos = generar_matriz_trazabilidad(proyecto)
    # etc.
    ```
12. El sistema genera el informe en el formato seleccionado:
    - **PDF:** usando ReportLab o WeasyPrint
    - **Excel:** usando openpyxl o xlsxwriter
    - **CSV:** usando módulo csv de Python
13. El sistema agrega:
    - Encabezado con logo del proyecto (si existe)
    - Nombre del proyecto
    - Fecha de generación
    - Usuario que generó
    - Pie de página con numeración
14. El sistema descarga el archivo al navegador
15. El sistema muestra mensaje: "Informe generado exitosamente"
16. El usuario abre/guarda el archivo descargado

### Flujo Alternativo A - Informe de Requerimientos
1. El usuario selecciona "Informe de Requerimientos"
2. El sistema permite filtrar por:
   - Estado (Pendiente/En progreso/Completado)
   - Tipo (Funcional/No funcional)
   - Prioridad (Must/Should/Could/Won't)
   - Validación (Aprobado/Rechazado/Pendiente)
3. El usuario configura filtros y formato
4. El usuario genera el informe
5. El sistema incluye en el informe:
   - Resumen ejecutivo (total, por tipo, por estado)
   - Tabla de requerimientos con columnas:
     * ID/Código
     * Nombre
     * Descripción
     * Tipo
     * Prioridad
     * Estado
     * Estado validación
     * Casos de uso vinculados (cantidad)
     * Creado por
     * Fecha creación
   - Gráficos (si es PDF):
     * Distribución por tipo (pie chart)
     * Distribución por prioridad (bar chart)
     * Distribución por estado (pie chart)
   - Estadísticas:
     * Total de requerimientos
     * % funcionales vs no funcionales
     * % por prioridad
     * % validados
     * % con casos de uso vinculados
6. El sistema descarga el archivo

### Flujo Alternativo B - Matriz de Trazabilidad
1. El usuario selecciona "Matriz de Trazabilidad"
2. El sistema genera matriz bidireccional:
   ```
   ┌──────────────┬──────┬──────┬──────┬──────┐
   │ Req/Caso     │ CU-01│ CU-02│ CU-03│ CU-04│
   ├──────────────┼──────┼──────┼──────┼──────┤
   │ REQ-001      │  X   │      │  X   │      │
   │ REQ-002      │      │  X   │      │      │
   │ REQ-003      │  X   │  X   │  X   │      │
   │ REQ-004      │      │      │      │  X   │
   └──────────────┴──────┴──────┴──────┴──────┘
   ```
3. El sistema calcula métricas:
   - Cobertura de requerimientos: % con al menos un CU
   - Cobertura de casos de uso: % con al menos un req
   - Requerimientos huérfanos (sin CU)
   - Casos huérfanos (sin req)
4. El sistema genera el archivo
5. En Excel: matriz interactiva con filtros
6. En PDF: matriz visual con resumen de cobertura

### Flujo Alternativo C - Informe Ejecutivo
1. El usuario selecciona "Informe Ejecutivo"
2. El sistema genera resumen de alto nivel:
   - **Portada:** nombre proyecto, logo, fecha, autor
   - **Resumen ejecutivo:** 
     * Objetivo del proyecto
     * Estado general (% completado)
     * Métricas clave
   - **Requerimientos:**
     * Total: X requerimientos
     * Aprobados: X (Y%)
     * En progreso: X (Y%)
   - **Casos de Uso:**
     * Total: X casos
     * Completados: X (Y%)
   - **Trazabilidad:**
     * Cobertura de requerimientos: X%
     * Cobertura de casos de uso: X%
   - **Alertas:**
     * Requerimientos Must Have sin validar
     * Requerimientos huérfanos
     * Casos huérfanos
   - **Próximos pasos:** recomendaciones automáticas
3. El sistema genera PDF profesional con gráficos
4. Ideal para presentaciones a stakeholders

### Flujo Alternativo D - Programar Informe Periódico
1. El usuario hace clic en "Programar informe"
2. El sistema muestra formulario:
   - Tipo de informe
   - Frecuencia (Diario/Semanal/Mensual)
   - Formato
   - Destinatarios (emails)
3. El usuario configura la programación
4. El usuario hace clic en "Guardar programación"
5. El sistema crea tarea programada (Celery/Cron)
6. El sistema envía informes automáticamente según configuración

### Flujos Alternativos de Error
**9a. No hay datos para el informe**
- El sistema detecta que no hay requerimientos ni casos de uso
- Muestra mensaje: "No hay datos suficientes para generar este informe"
- Sugiere: "Crea al menos un requerimiento o caso de uso primero"
- No genera el archivo
- Ofrece volver a reportes

**9b. Usuario sin permisos de lectura**
- El sistema detecta que el usuario no tiene acceso al proyecto
- Muestra error: "No tienes permisos para generar informes de este proyecto"
- Redirige a la lista de proyectos

**12a. Error al generar PDF**
- El sistema captura excepción durante generación
- Muestra error: "Error al generar PDF. Intenta con formato Excel o CSV"
- Registra error en logs
- Ofrece formatos alternativos
- Permite reintentar

**12b. Archivo muy grande**
- El sistema detecta que el informe superaría 50MB
- Muestra advertencia: "Este informe es muy grande. Considera aplicar filtros"
- Sugiere limitar por fechas o estados
- Permite continuar bajo responsabilidad del usuario

**14a. Navegador bloquea descarga**
- El sistema detecta que el navegador bloqueó la descarga
- Muestra instrucciones: "Permite descargas de este sitio en tu navegador"
- Ofrece enlace directo al archivo generado
- Archivo disponible temporalmente (24 horas)

### Flujo Opcional - Vista Previa
1. El usuario hace clic en "Vista previa" en lugar de "Generar"
2. El sistema genera HTML del informe
3. El sistema muestra en modal o nueva pestaña
4. El usuario revisa el contenido
5. Si está satisfecho, hace clic en "Descargar PDF/Excel"
6. Si quiere cambios, cierra y modifica filtros

### Reglas de Negocio
- RN-01: Solo usuarios con permisos de lectura pueden generar informes
- RN-02: Los informes son instantáneos (snapshot) del momento de generación
- RN-03: Los informes NO modifican datos (solo lectura)
- RN-04: Formatos soportados: PDF, Excel (.xlsx), CSV
- RN-05: Todos los informes incluyen metadatos: fecha, usuario, proyecto
- RN-06: Límite de tamaño: 50MB por informe (configurable)
- RN-07: Los informes deben ser profesionales (con logo, formato corporativo)
- RN-08: Datos sensibles se pueden ocultar según configuración
- RN-09: Los informes pueden incluir gráficos solo en PDF
- RN-10: CSV es ideal para análisis en herramientas externas (Excel, R, Python)
- RN-11: Excel permite filtros interactivos y formato condicional
- RN-12: PDF es ideal para presentaciones e impresión
- RN-13: Los informes programados se envían por email automáticamente
- RN-14: Se recomienda incluir pie de página con "Generado por GRCU Manager"

### Tipos de Informes Detallados

#### 1. Informe de Requerimientos
**Contenido:**
- Resumen: total, por tipo, por estado, por prioridad
- Tabla detallada: ID, nombre, descripción, tipo, prioridad, estado, validación, CU vinculados
- Gráficos: distribución por tipo, prioridad, estado
- Requerimientos críticos (Must Have) destacados
- Requerimientos sin validar (alerta)
- Requerimientos huérfanos (alerta)

#### 2. Informe de Casos de Uso
**Contenido:**
- Resumen: total casos, por complejidad, por estado
- Tabla: ID, nombre, descripción, actores, precondiciones, flujos, reqs vinculados
- Casos críticos destacados
- Casos huérfanos (sin requerimientos)
- Distribución por complejidad (alta/media/baja)

#### 3. Matriz de Trazabilidad
**Contenido:**
- Tabla bidireccional: requerimientos × casos de uso
- Marca X donde hay vinculación
- Resumen de cobertura: % reqs cubiertos, % casos cubiertos
- Lista de requerimientos huérfanos
- Lista de casos huérfanos
- Recomendaciones de vinculación

#### 4. Informe de Validación
**Contenido:**
- Solo metodología TRADICIONAL
- Estadísticas: aprobados, rechazados, pendientes
- Lista de requerimientos por estado de validación
- Observaciones de validadores
- Requerimientos rechazados con motivos
- Timeline de validaciones

#### 5. Informe de Progreso
**Contenido:**
- % de completitud del proyecto
- Requerimientos: X% completados
- Casos de uso: Y% completados
- Gráfico de burn-down (si aplica)
- Velocidad del equipo (reqs/casos por semana)
- Estimación de finalización

#### 6. Informe de Actividades
**Contenido:**
- Log de cambios recientes (últimos 30 días)
- Quién hizo qué y cuándo
- Requerimientos creados/modificados
- Casos creados/modificados
- Validaciones realizadas
- Comentarios agregados
- Actividad por usuario

#### 7. Informe de Huérfanos
**Contenido:**
- Requerimientos sin casos de uso
- Casos de uso sin requerimientos
- Análisis de impacto
- Priorización de huérfanos (Must Have primero)
- Recomendaciones de vinculación automática

#### 8. Informe Ejecutivo
**Contenido:**
- Portada profesional
- Resumen ejecutivo (1-2 páginas)
- Métricas clave con iconos/gráficos
- Estado general del proyecto
- Alertas y riesgos
- Próximos hitos
- Recomendaciones

### Implementación de Generación de PDF

```python
# En dashboards/views.py o requerimientos/views.py
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.units import inch
from io import BytesIO
from datetime import datetime

@login_required
def generar_informe_requerimientos_pdf(request, proyecto_id):
    """Genera informe de requerimientos en PDF."""
    proyecto = get_object_or_404(Proyecto, pk=proyecto_id)
    
    # Verificar permisos
    if not request.user.tiene_permiso_lectura(proyecto):
        messages.error(request, "No tienes permisos para generar informes")
        return redirect('proyectos:detalle', pk=proyecto.id)
    
    # Obtener datos
    requerimientos = Requerimiento.objects.filter(
        proyecto=proyecto
    ).select_related('detalle_tradicional', 'detalle_agil', 'creado_por')
    
    # Calcular estadísticas
    total = requerimientos.count()
    funcionales = requerimientos.filter(tipo='FUNCIONAL').count()
    no_funcionales = requerimientos.filter(tipo='NO_FUNCIONAL').count()
    pendientes = requerimientos.filter(estado='PENDIENTE').count()
    en_progreso = requerimientos.filter(estado='EN_PROGRESO').count()
    completados = requerimientos.filter(estado='COMPLETADO').count()
    
    # Crear PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    
    # Estilos
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#003366'),
        spaceAfter=30
    )
    
    # Título
    title = Paragraph(f"Informe de Requerimientos<br/>{proyecto.nombre}", title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.2*inch))
    
    # Metadatos
    fecha_generacion = datetime.now().strftime('%d/%m/%Y %H:%M')
    meta = Paragraph(
        f"<b>Generado por:</b> {request.user.nombre}<br/>"
        f"<b>Fecha:</b> {fecha_generacion}<br/>"
        f"<b>Total de requerimientos:</b> {total}",
        styles['Normal']
    )
    elements.append(meta)
    elements.append(Spacer(1, 0.3*inch))
    
    # Resumen estadístico
    resumen_title = Paragraph("<b>Resumen Estadístico</b>", styles['Heading2'])
    elements.append(resumen_title)
    
    stats_data = [
        ['Métrica', 'Cantidad', 'Porcentaje'],
        ['Requerimientos Funcionales', str(funcionales), f"{(funcionales/total*100):.1f}%"],
        ['Requerimientos No Funcionales', str(no_funcionales), f"{(no_funcionales/total*100):.1f}%"],
        ['Pendientes', str(pendientes), f"{(pendientes/total*100):.1f}%"],
        ['En Progreso', str(en_progreso), f"{(en_progreso/total*100):.1f}%"],
        ['Completados', str(completados), f"{(completados/total*100):.1f}%"],
    ]
    
    stats_table = Table(stats_data)
    stats_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(stats_table)
    elements.append(Spacer(1, 0.5*inch))
    
    # Tabla de requerimientos
    req_title = Paragraph("<b>Detalle de Requerimientos</b>", styles['Heading2'])
    elements.append(req_title)
    
    req_data = [['ID', 'Nombre', 'Tipo', 'Estado', 'Prioridad']]
    for req in requerimientos:
        prioridad = 'N/A'
        if proyecto.metodologia == 'TRADICIONAL' and req.detalle_tradicional:
            prioridad = req.detalle_tradicional.prioridad or 'N/A'
        
        req_data.append([
            str(req.id),
            req.nombre[:40] + '...' if len(req.nombre) > 40 else req.nombre,
            req.get_tipo_display(),
            req.get_estado_display(),
            prioridad
        ])
    
    req_table = Table(req_data, colWidths=[0.8*inch, 3*inch, 1.2*inch, 1.2*inch, 1*inch])
    req_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003366')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
    ]))
    elements.append(req_table)
    
    # Pie de página
    elements.append(Spacer(1, 0.5*inch))
    footer = Paragraph(
        f"<i>Generado por GRCU Manager - {fecha_generacion}</i>",
        styles['Normal']
    )
    elements.append(footer)
    
    # Construir PDF
    doc.build(elements)
    
    # Retornar respuesta
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="informe_requerimientos_{proyecto.nombre}_{datetime.now().strftime("%Y%m%d")}.pdf"'
    
    return response
```

### Implementación de Generación de Excel

```python
# En dashboards/views.py o requerimientos/views.py
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.chart import PieChart, Reference

@login_required
def generar_informe_requerimientos_excel(request, proyecto_id):
    """Genera informe de requerimientos en Excel."""
    proyecto = get_object_or_404(Proyecto, pk=proyecto_id)
    
    # Verificar permisos
    if not request.user.tiene_permiso_lectura(proyecto):
        messages.error(request, "No tienes permisos para generar informes")
        return redirect('proyectos:detalle', pk=proyecto.id)
    
    # Obtener datos
    requerimientos = Requerimiento.objects.filter(
        proyecto=proyecto
    ).select_related('detalle_tradicional', 'detalle_agil', 'creado_por')
    
    # Crear workbook
    wb = Workbook()
    
    # Hoja 1: Resumen
    ws_resumen = wb.active
    ws_resumen.title = "Resumen"
    
    # Título
    ws_resumen['A1'] = f"Informe de Requerimientos - {proyecto.nombre}"
    ws_resumen['A1'].font = Font(size=16, bold=True, color="003366")
    ws_resumen.merge_cells('A1:E1')
    
    # Metadatos
    ws_resumen['A3'] = "Generado por:"
    ws_resumen['B3'] = request.user.nombre
    ws_resumen['A4'] = "Fecha:"
    ws_resumen['B4'] = datetime.now().strftime('%d/%m/%Y %H:%M')
    ws_resumen['A5'] = "Total requerimientos:"
    ws_resumen['B5'] = requerimientos.count()
    
    # Estadísticas
    ws_resumen['A7'] = "Estadísticas por Tipo"
    ws_resumen['A7'].font = Font(bold=True)
    ws_resumen['A8'] = "Funcionales"
    ws_resumen['B8'] = requerimientos.filter(tipo='FUNCIONAL').count()
    ws_resumen['A9'] = "No Funcionales"
    ws_resumen['B9'] = requerimientos.filter(tipo='NO_FUNCIONAL').count()
    
    ws_resumen['D7'] = "Estadísticas por Estado"
    ws_resumen['D7'].font = Font(bold=True)
    ws_resumen['D8'] = "Pendientes"
    ws_resumen['E8'] = requerimientos.filter(estado='PENDIENTE').count()
    ws_resumen['D9'] = "En Progreso"
    ws_resumen['E9'] = requerimientos.filter(estado='EN_PROGRESO').count()
    ws_resumen['D10'] = "Completados"
    ws_resumen['E10'] = requerimientos.filter(estado='COMPLETADO').count()
    
    # Hoja 2: Detalle de Requerimientos
    ws_detalle = wb.create_sheet(title="Requerimientos")
    
    # Encabezados
    headers = ['ID', 'Nombre', 'Descripción', 'Tipo', 'Estado', 'Prioridad', 'Creado Por', 'Fecha Creación']
    ws_detalle.append(headers)
    
    # Estilo de encabezado
    header_fill = PatternFill(start_color="003366", end_color="003366", fill_type="solid")
    header_font = Font(color="FFFFFF", bold=True)
    
    for cell in ws_detalle[1]:
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal='center', vertical='center')
    
    # Datos
    for req in requerimientos:
        prioridad = 'N/A'
        if proyecto.metodologia == 'TRADICIONAL' and req.detalle_tradicional:
            prioridad = req.detalle_tradicional.prioridad or 'N/A'
        
        ws_detalle.append([
            req.id,
            req.nombre,
            req.descripcion,
            req.get_tipo_display(),
            req.get_estado_display(),
            prioridad,
            req.creado_por.nombre if req.creado_por else 'N/A',
            req.fecha_creacion.strftime('%d/%m/%Y')
        ])
    
    # Ajustar anchos de columna
    ws_detalle.column_dimensions['A'].width = 8
    ws_detalle.column_dimensions['B'].width = 40
    ws_detalle.column_dimensions['C'].width = 60
    ws_detalle.column_dimensions['D'].width = 15
    ws_detalle.column_dimensions['E'].width = 15
    ws_detalle.column_dimensions['F'].width = 12
    ws_detalle.column_dimensions['G'].width = 20
    ws_detalle.column_dimensions['H'].width = 15
    
    # Filtros automáticos
    ws_detalle.auto_filter.ref = ws_detalle.dimensions
    
    # Guardar en buffer
    buffer = BytesIO()
    wb.save(buffer)
    buffer.seek(0)
    
    # Retornar respuesta
    response = HttpResponse(
        buffer,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="informe_requerimientos_{proyecto.nombre}_{datetime.now().strftime("%Y%m%d")}.xlsx"'
    
    return response
```

### Template de Página de Reportes

```html
<!-- En dashboards/templates/dashboards/lider_reportes.html (mejorado) -->
{% extends "core/base.html" %}
{% load static %}

{% block extra_css %}
<link rel="stylesheet" href="{% static 'dashboards/css/lider_reportes_styles.css' %}">
{% endblock %}

{% block content %}
<div class="reportes-container">
    <h2>
        <i class="bi bi-file-earmark-bar-graph"></i> 
        Reportes del Proyecto
    </h2>
    <p class="text-muted">
        Genera informes profesionales sobre requerimientos, casos de uso y trazabilidad
    </p>
    
    <!-- Selector de proyecto -->
    <div class="proyecto-selector mb-4">
        <label for="proyecto">Proyecto:</label>
        <select id="proyecto" class="form-select">
            {% for p in proyectos %}
            <option value="{{ p.id }}">{{ p.nombre }}</option>
            {% endfor %}
        </select>
    </div>

    <div class="reportes-grid">
        <!-- Informe de Requerimientos -->
        <div class="reporte-card">
            <div class="reporte-icon">
                <i class="bi bi-list-check"></i>
            </div>
            <h4>Reporte de Requerimientos</h4>
            <p>Resumen completo de todos los requerimientos con priorización, validación y estado de avance.</p>
            <div class="stats">
                <span class="badge bg-primary">{{ total_requerimientos }} requerimientos</span>
            </div>
            <div class="botones-export">
                <a href="{% url 'dashboards:generar_informe_pdf' proyecto.id 'requerimientos' %}" 
                   class="btn btn-danger btn-sm">
                    <i class="bi bi-file-pdf"></i> PDF
                </a>
                <a href="{% url 'dashboards:generar_informe_excel' proyecto.id 'requerimientos' %}" 
                   class="btn btn-success btn-sm">
                    <i class="bi bi-file-excel"></i> Excel
                </a>
                <a href="{% url 'dashboards:generar_informe_csv' proyecto.id 'requerimientos' %}" 
                   class="btn btn-secondary btn-sm">
                    <i class="bi bi-filetype-csv"></i> CSV
                </a>
            </div>
        </div>

        <!-- Informe de Casos de Uso -->
        <div class="reporte-card">
            <div class="reporte-icon">
                <i class="bi bi-diagram-3"></i>
            </div>
            <h4>Reporte de Casos de Uso</h4>
            <p>Listado de casos de uso con actores, complejidad, flujos y comentarios asociados.</p>
            <div class="stats">
                <span class="badge bg-info">{{ total_casos_uso }} casos de uso</span>
            </div>
            <div class="botones-export">
                <a href="{% url 'dashboards:generar_informe_pdf' proyecto.id 'casos_uso' %}" 
                   class="btn btn-danger btn-sm">
                    <i class="bi bi-file-pdf"></i> PDF
                </a>
                <a href="{% url 'dashboards:generar_informe_excel' proyecto.id 'casos_uso' %}" 
                   class="btn btn-success btn-sm">
                    <i class="bi bi-file-excel"></i> Excel
                </a>
                <a href="{% url 'dashboards:generar_informe_csv' proyecto.id 'casos_uso' %}" 
                   class="btn btn-secondary btn-sm">
                    <i class="bi bi-filetype-csv"></i> CSV
                </a>
            </div>
        </div>

        <!-- Matriz de Trazabilidad -->
        <div class="reporte-card">
            <div class="reporte-icon">
                <i class="bi bi-grid-3x3-gap"></i>
            </div>
            <h4>Matriz de Trazabilidad</h4>
            <p>Muestra la relación entre requerimientos y casos de uso con análisis de cobertura.</p>
            <div class="stats">
                <span class="badge bg-warning">{{ cobertura_porcentaje }}% cobertura</span>
            </div>
            <div class="botones-export">
                <a href="{% url 'dashboards:generar_informe_pdf' proyecto.id 'matriz' %}" 
                   class="btn btn-danger btn-sm">
                    <i class="bi bi-file-pdf"></i> PDF
                </a>
                <a href="{% url 'dashboards:generar_informe_excel' proyecto.id 'matriz' %}" 
                   class="btn btn-success btn-sm">
                    <i class="bi bi-file-excel"></i> Excel
                </a>
            </div>
        </div>

        <!-- Informe de Validación -->
        <div class="reporte-card">
            <div class="reporte-icon">
                <i class="bi bi-check-circle"></i>
            </div>
            <h4>Informe de Validación</h4>
            <p>Requerimientos aprobados, rechazados y pendientes con observaciones de validadores.</p>
            <div class="stats">
                <span class="badge bg-success">{{ reqs_aprobados }} aprobados</span>
                <span class="badge bg-danger">{{ reqs_rechazados }} rechazados</span>
            </div>
            <div class="botones-export">
                <a href="{% url 'dashboards:generar_informe_pdf' proyecto.id 'validacion' %}" 
                   class="btn btn-danger btn-sm">
                    <i class="bi bi-file-pdf"></i> PDF
                </a>
                <a href="{% url 'dashboards:generar_informe_excel' proyecto.id 'validacion' %}" 
                   class="btn btn-success btn-sm">
                    <i class="bi bi-file-excel"></i> Excel
                </a>
            </div>
        </div>
        
        <!-- Informe de Huérfanos -->
        <div class="reporte-card">
            <div class="reporte-icon">
                <i class="bi bi-exclamation-triangle"></i>
            </div>
            <h4>Informe de Huérfanos</h4>
            <p>Requerimientos sin casos de uso y casos de uso sin requerimientos vinculados.</p>
            <div class="stats">
                <span class="badge bg-danger">{{ reqs_huerfanos }} req. huérfanos</span>
                <span class="badge bg-warning">{{ casos_huerfanos }} casos huérfanos</span>
            </div>
            <div class="botones-export">
                <a href="{% url 'dashboards:generar_informe_pdf' proyecto.id 'huerfanos' %}" 
                   class="btn btn-danger btn-sm">
                    <i class="bi bi-file-pdf"></i> PDF
                </a>
                <a href="{% url 'dashboards:generar_informe_excel' proyecto.id 'huerfanos' %}" 
                   class="btn btn-success btn-sm">
                    <i class="bi bi-file-excel"></i> Excel
                </a>
            </div>
        </div>
        
        <!-- Informe Ejecutivo -->
        <div class="reporte-card destacado">
            <div class="reporte-icon">
                <i class="bi bi-briefcase"></i>
            </div>
            <h4>Informe Ejecutivo</h4>
            <p>Resumen de alto nivel para stakeholders con métricas clave y estado del proyecto.</p>
            <div class="stats">
                <span class="badge bg-primary">{{ progreso_porcentaje }}% completado</span>
            </div>
            <div class="botones-export">
                <a href="{% url 'dashboards:generar_informe_pdf' proyecto.id 'ejecutivo' %}" 
                   class="btn btn-danger btn-lg">
                    <i class="bi bi-file-pdf"></i> Generar PDF
                </a>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### Estado de Implementación
⚠️ **PARCIALMENTE IMPLEMENTADO**

**✅ Implementado:**
- Vista `lider_reportes` en `dashboards/views.py`
- Template `lider_reportes.html` con estructura básica de reportes
- URL `/dashboards/lider/reportes/` funcional

**❌ NO implementado:**
- Botones de exportación NO tienen funcionalidad (solo HTML estático)
- NO existen vistas para generar PDF, Excel, CSV
- NO hay integración con ReportLab, openpyxl o csv
- NO hay consultas de datos para los informes
- NO hay cálculo de estadísticas
- NO hay generación real de archivos
- NO hay descarga de informes
- NO hay filtros ni configuración de informes
- NO hay informes programados/automáticos
- NO hay gráficos en PDF
- Template solo muestra botones sin funcionalidad

**Librerías necesarias (no instaladas):**
```bash
pip install reportlab  # Para generar PDF
pip install openpyxl   # Para generar Excel
pip install pillow     # Para imágenes en PDF (opcional)
pip install matplotlib # Para gráficos (opcional)
```

### Prioridad de Implementación
🟡 **MEDIA** - Útil pero no crítico para funcionalidad básica:
- Facilita comunicación con stakeholders
- Mejora profesionalismo del sistema
- Útil para auditorías y presentaciones
- No es crítico para la gestión día a día
- Se puede trabajar inicialmente sin informes (exportar datos manualmente)
- Alta prioridad para proyectos formales o regulados
- Baja prioridad para proyectos internos o startups
- Complementa todos los demás casos de uso (CU-01 a CU-20)

### Observaciones de Revisión
✅ **Correcciones aplicadas:**
- Reconocido que existe página de reportes pero SIN funcionalidad real
- Template `lider_reportes.html` solo tiene HTML estático
- Botones "Exportar PDF/Excel" NO tienen URLs ni vistas asociadas
- Propuestos 8 tipos de informes diferentes con contenido específico
- Código completo para generar PDF con ReportLab
- Código completo para generar Excel con openpyxl
- Template mejorado con badges de estadísticas
- Incluidos filtros, configuración, vista previa
- Flujos alternativos para cada tipo de informe
- Manejo de errores (sin datos, archivo grande, permisos)
- Informes programados/periódicos (funcionalidad avanzada)
- Listadas librerías necesarias para implementación

---

## CU-22: Visualizar trazabilidad

### Descripción
El sistema permite a los usuarios **visualizar la matriz de trazabilidad** entre requerimientos y casos de uso de forma interactiva, facilitando el análisis de cobertura, identificación de gaps y gestión de relaciones.

La visualización de trazabilidad permite:
- **Ver relaciones bidireccionales:** qué casos de uso implementan cada requerimiento y viceversa
- **Identificar cobertura:** qué % de requerimientos tienen casos de uso vinculados
- **Detectar huérfanos:** requerimientos sin casos de uso y casos sin requerimientos
- **Análisis de impacto:** qué casos se afectan al cambiar un requerimiento
- **Navegación intuitiva:** hacer clic en las relaciones para ir al detalle
- **Filtros dinámicos:** filtrar por tipo, estado, prioridad
- **Búsqueda rápida:** encontrar requerimientos o casos específicos
- **Exportación:** guardar matriz en PDF/Excel (relacionado con CU-21)
- **Visualización gráfica:** diagramas de red o grafos de dependencias (opcional)

La matriz de trazabilidad es **crítica** para:
- Validar que todos los requerimientos tienen diseño de implementación
- Asegurar que no hay casos de uso huérfanos (sin propósito de negocio)
- Análisis de impacto ante cambios
- Auditorías y cumplimiento de estándares
- Presentaciones a stakeholders

### Actores
- **Todos los usuarios del proyecto** (lectura)
- **Analista** (navega y analiza trazabilidad)
- **Líder del proyecto** (revisa cobertura y gaps)
- **Auditor/QA** (verifica completitud)
- **Product Owner** (valida que requerimientos estén cubiertos)

### Precondiciones
- Proyecto existente
- Al menos un requerimiento o caso de uso creado
- Usuario autenticado con acceso al proyecto

### Postcondiciones
- Matriz de trazabilidad visualizada
- Sin cambios en la base de datos (solo lectura)
- Usuario puede navegar a detalles de requerimientos/casos
- Estadísticas de cobertura calculadas

### Flujo Principal
1. El usuario navega al proyecto
2. El usuario hace clic en "Trazabilidad" o "Matriz de trazabilidad" en el menú
3. El sistema consulta datos:
   ```python
   # Obtener todos los requerimientos y casos del proyecto
   requerimientos = Requerimiento.objects.filter(proyecto=proyecto)
   casos = CasoDeUso.objects.filter(proyecto=proyecto)
   
   # Obtener relaciones desde tabla intermedia
   relaciones = RequerimientoCaso.objects.filter(
       requerimiento__proyecto=proyecto
   ).select_related('requerimiento', 'caso_de_uso')
   ```
4. El sistema construye la matriz de trazabilidad:
   ```python
   # Crear matriz bidireccional
   matriz = {}
   for req in requerimientos:
       matriz[req.id] = {
           'requerimiento': req,
           'casos_vinculados': req.casos_relacionados.all(),
           'tiene_casos': req.casos_relacionados.exists()
       }
   ```
5. El sistema calcula estadísticas:
   - Total de requerimientos: X
   - Total de casos de uso: Y
   - Requerimientos con casos: Z (Z/X%)
   - Casos con requerimientos: W (W/Y%)
   - Requerimientos huérfanos: X - Z
   - Casos huérfanos: Y - W
6. El sistema muestra la matriz en formato tabla bidireccional:
   - Filas: requerimientos
   - Columnas: casos de uso
   - Celdas: marca ✓ si hay vinculación
7. El sistema destaca visualmente:
   - Requerimientos sin casos: fila en rojo/amarillo
   - Casos sin requerimientos: columna en rojo/amarillo
   - Requerimientos Must Have sin casos: alerta crítica
8. El usuario puede:
   - Hacer clic en un requerimiento para ver su detalle
   - Hacer clic en un caso de uso para ver su detalle
   - Hacer clic en una celda marcada para ver/editar la vinculación
   - Filtrar por estado, tipo, prioridad
   - Buscar requerimientos o casos específicos
   - Ver solo huérfanos
   - Exportar a PDF/Excel
   - Cambiar entre vista tabla y vista gráfica
9. El usuario navega por la matriz según sus necesidades
10. El sistema actualiza la visualización dinámicamente (AJAX/JavaScript)

### Flujo Alternativo A - Vista de Tabla Interactiva
1. El usuario accede a la matriz
2. El sistema muestra tabla HTML con:
   - Encabezado fijo (scroll horizontal)
   - Primera columna fija (requerimientos)
   - Celdas con checkmark ✓ donde hay vinculación
   - Tooltip al pasar mouse: "REQ-001 → CU-003: [nota de vinculación]"
3. El usuario puede:
   - Ordenar por nombre, prioridad, estado
   - Filtrar columnas (casos) y filas (requerimientos)
   - Hacer clic en celda para ir al detalle de la vinculación
4. Ejemplo visual:
   ```
   ┌─────────────────┬────────┬────────┬────────┬────────┬────────┐
   │ Requerimiento   │ CU-001 │ CU-002 │ CU-003 │ CU-004 │ CU-005 │
   ├─────────────────┼────────┼────────┼────────┼────────┼────────┤
   │ REQ-001 (MUST)  │   ✓    │        │   ✓    │        │        │
   │ REQ-002 (SHOULD)│        │   ✓    │        │        │   ✓    │
   │ REQ-003 (MUST)  │   ✓    │   ✓    │   ✓    │        │        │
   │ REQ-004 (COULD) │        │        │        │   ✓    │        │
   │ REQ-005 ⚠️      │        │        │        │        │        │ ← Huérfano
   └─────────────────┴────────┴────────┴────────┴────────┴────────┘
                                                             ↑
                                                         Huérfano
   ```

### Flujo Alternativo B - Vista de Lista con Agrupación
1. El usuario cambia a "Vista de lista"
2. El sistema muestra lista agrupada:
   - **Requerimientos con casos vinculados:**
     * REQ-001: Login seguro → CU-001, CU-003
     * REQ-002: Registro → CU-002, CU-005
   - **Requerimientos sin casos (huérfanos):**
     * REQ-005: Validación de datos ⚠️
   - **Casos de uso con requerimientos:**
     * CU-001: Login de usuario → REQ-001, REQ-003
   - **Casos sin requerimientos (huérfanos):**
     * CU-006: Exportar datos ⚠️
3. El usuario puede expandir/colapsar secciones
4. Vista más legible para proyectos grandes

### Flujo Alternativo C - Vista de Grafo/Red (Visualización Avanzada)
1. El usuario selecciona "Vista de grafo"
2. El sistema genera visualización con librería D3.js o Vis.js:
   - Nodos azules: requerimientos
   - Nodos verdes: casos de uso
   - Líneas/aristas: vinculaciones
   - Nodos sin conexiones: destacados en rojo (huérfanos)
3. El usuario puede:
   - Hacer zoom in/out
   - Arrastrar nodos para reposicionar
   - Hacer clic en nodo para ver detalles
   - Hacer clic en arista para ver/editar vinculación
4. Visualización ideal para análisis de dependencias complejas
5. Ejemplo visual:
   ```
      REQ-001 ──────────── CU-001
         │                   │
         │                   │
         └──────── CU-003 ───┘
                     │
      REQ-002 ──────┘
   
      REQ-004 (huérfano, sin conexiones)
      CU-005 (huérfano, sin conexiones)
   ```

### Flujo Alternativo D - Filtros Dinámicos
1. El usuario hace clic en "Filtros"
2. El sistema muestra panel de filtros:
   - **Requerimientos:**
     * Tipo: Funcional / No funcional
     * Estado: Pendiente / En progreso / Completado
     * Prioridad: Must / Should / Could / Won't
     * Validación: Aprobado / Rechazado / Pendiente
   - **Casos de uso:**
     * Estado: Pendiente / En progreso / Completado
     * Complejidad: Alta / Media / Baja
   - **Trazabilidad:**
     * Solo requerimientos con casos
     * Solo requerimientos huérfanos
     * Solo casos con requerimientos
     * Solo casos huérfanos
     * Must Have sin casos (crítico)
3. El usuario selecciona filtros
4. El sistema actualiza la matriz en tiempo real (JavaScript)
5. El usuario puede guardar combinaciones de filtros favoritas

### Flujo Alternativo E - Búsqueda Rápida
1. El usuario escribe en el campo de búsqueda
2. El sistema filtra en tiempo real:
   - Por nombre de requerimiento
   - Por nombre de caso de uso
   - Por descripción
   - Por ID/código
3. La matriz muestra solo las filas/columnas que coinciden
4. El usuario puede limpiar búsqueda para volver a vista completa

### Flujo Alternativo F - Crear Vinculación desde Matriz
1. El usuario hace clic en una celda vacía (sin ✓)
2. El sistema muestra modal: "¿Vincular REQ-001 con CU-003?"
3. El usuario opcionalmente agrega nota explicativa
4. El usuario confirma
5. El sistema crea vinculación en `RequerimientoCaso`:
   ```python
   RequerimientoCaso.objects.create(
       requerimiento=req,
       caso_de_uso=caso,
       nota=nota_usuario
   )
   ```
6. La celda se actualiza mostrando ✓
7. Las estadísticas se recalculan automáticamente

### Flujo Alternativo G - Eliminar Vinculación desde Matriz
1. El usuario hace clic en una celda con ✓
2. El sistema muestra detalle de la vinculación:
   - Fecha de vinculación
   - Nota (si existe)
   - Botón "Desvincular"
3. El usuario hace clic en "Desvincular"
4. El sistema pide confirmación: "¿Eliminar vinculación?"
5. El usuario confirma
6. El sistema elimina el registro de `RequerimientoCaso`
7. La celda se actualiza (vacía, sin ✓)
8. Las estadísticas se recalculan

### Flujos Alternativos de Error
**3a. No hay requerimientos ni casos de uso**
- El sistema detecta proyecto vacío
- Muestra mensaje: "No hay requerimientos ni casos de uso en este proyecto"
- Muestra botones: "Crear requerimiento" / "Crear caso de uso"
- No muestra matriz vacía

**3b. Solo hay requerimientos (sin casos de uso)**
- El sistema detecta casos = 0
- Muestra advertencia: "No hay casos de uso. Todos los requerimientos son huérfanos"
- Muestra lista de requerimientos con alerta
- Sugiere: "Crea casos de uso para implementar estos requerimientos"

**3c. Solo hay casos de uso (sin requerimientos)**
- El sistema detecta requerimientos = 0
- Muestra advertencia: "No hay requerimientos. Todos los casos son huérfanos"
- Sugiere: "Los casos de uso deben implementar requerimientos de negocio"

**10a. Error al cargar matriz (proyecto muy grande)**
- El sistema detecta >500 requerimientos o >500 casos
- Muestra advertencia: "Proyecto muy grande. Aplica filtros para mejor rendimiento"
- Carga vista paginada o con scroll virtual
- Sugiere usar filtros o búsqueda

**6a. Usuario sin permisos**
- El sistema detecta usuario sin acceso al proyecto
- Muestra error: "No tienes permisos para ver este proyecto"
- Redirige a lista de proyectos

### Flujo Opcional - Análisis de Impacto
1. El usuario hace clic derecho en un requerimiento
2. El usuario selecciona "Análisis de impacto"
3. El sistema muestra:
   - Casos de uso que implementan este requerimiento
   - Otros requerimientos relacionados (mismo caso de uso)
   - Usuarios asignados a los casos vinculados
   - Estimación de esfuerzo total
4. El usuario puede generar informe de impacto (PDF)
5. Útil para evaluar cambios en requerimientos

### Flujo Opcional - Sugerencias Automáticas de Vinculación
1. El usuario hace clic en "Sugerir vinculaciones"
2. El sistema analiza:
   - Similitud de nombres (Levenshtein distance)
   - Palabras clave comunes
   - Descripción vs flujos de casos
3. El sistema muestra lista de sugerencias:
   - "REQ-001 podría vincularse con CU-003 (75% similitud)"
   - "REQ-005 podría vincularse con CU-007 (palabras clave: login, autenticación)"
4. El usuario puede aceptar/rechazar cada sugerencia
5. Sugerencias aceptadas se vinculan automáticamente

### Reglas de Negocio
- RN-01: La matriz usa las relaciones reales de la tabla `RequerimientoCaso`
- RN-02: **NO** se deben usar coincidencias de nombres (heurísticas poco confiables)
- RN-03: Un requerimiento puede estar vinculado a múltiples casos de uso (N:M)
- RN-04: Un caso de uso puede implementar múltiples requerimientos (N:M)
- RN-05: Requerimientos Must Have sin casos de uso son alertas críticas
- RN-06: Se recomienda cobertura >95% (menos de 5% huérfanos)
- RN-07: La matriz debe actualizarse en tiempo real al crear/eliminar vinculaciones
- RN-08: Los huérfanos se destacan visualmente (color rojo/amarillo)
- RN-09: Solo usuarios con permisos de edición pueden crear/eliminar vinculaciones desde matriz
- RN-10: La matriz debe ser exportable (PDF/Excel) para auditorías
- RN-11: Tooltips deben mostrar información adicional al pasar mouse
- RN-12: La matriz debe soportar búsqueda y filtros dinámicos
- RN-13: En proyectos grandes (>100 req o >100 casos) usar paginación o scroll virtual
- RN-14: Cada vinculación puede tener nota explicativa (campo `nota` en `RequerimientoCaso`)

### Implementación Actual (INCORRECTA)

**Código actual en `dashboards/views.py` (líneas 112-116):**
```python
# ❌ INCORRECTO: Usa heurística de coincidencia de nombres
# Matriz de trazabilidad simple: relacionar requerimientos y casos por nombre parcial (heurística)
matriz = []
for req in requerimientos:
    relacionados = [cu for cu in casos if req.nombre.split()[0].lower() in cu.nombre.lower() or req.nombre.lower() in cu.descripcion.lower()]
    matriz.append({'req': req, 'casos': relacionados})
```

**Problemas:**
1. ❌ NO usa la tabla intermedia `RequerimientoCaso`
2. ❌ Usa coincidencia de nombres (poco confiable)
3. ❌ No respeta las vinculaciones reales creadas por usuarios
4. ❌ Genera "falsos positivos" (vinculaciones que no existen)
5. ❌ Puede perder vinculaciones reales si los nombres no coinciden

### Implementación Correcta Propuesta

```python
# En dashboards/views.py
@login_required
def lider_matriz(request, proyecto_id):
    """Vista de matriz de trazabilidad CORRECTA usando relaciones reales."""
    proyecto = get_object_or_404(Proyecto, pk=proyecto_id)
    
    # Verificar permisos
    if not request.user.tiene_permiso_lectura(proyecto):
        messages.error(request, "No tienes permisos para ver este proyecto")
        return redirect('proyectos:lista')
    
    # ✅ CORRECTO: Obtener datos con relaciones
    requerimientos = Requerimiento.objects.filter(
        proyecto=proyecto
    ).prefetch_related('casos_relacionados')
    
    casos = CasoDeUso.objects.filter(
        proyecto=proyecto
    ).prefetch_related('requerimientos_relacionados')
    
    # ✅ Construir matriz usando relaciones REALES de la tabla intermedia
    matriz_data = []
    for req in requerimientos:
        casos_vinculados = req.casos_relacionados.all()  # Usa la relación M2M real
        matriz_data.append({
            'requerimiento': req,
            'casos_vinculados': casos_vinculados,
            'tiene_casos': casos_vinculados.exists(),
            'es_must_have': (
                req.detalle_tradicional.prioridad == 'MUST' 
                if req.detalle_tradicional else False
            )
        })
    
    # Calcular estadísticas
    total_reqs = requerimientos.count()
    total_casos = casos.count()
    
    # Requerimientos con al menos un caso
    reqs_con_casos = requerimientos.annotate(
        num_casos=Count('casos_relacionados')
    ).filter(num_casos__gt=0).count()
    
    # Casos con al menos un requerimiento
    casos_con_reqs = casos.annotate(
        num_reqs=Count('requerimientos_relacionados')
    ).filter(num_reqs__gt=0).count()
    
    # Huérfanos
    reqs_huerfanos = requerimientos.annotate(
        num_casos=Count('casos_relacionados')
    ).filter(num_casos=0)
    
    casos_huerfanos = casos.annotate(
        num_reqs=Count('requerimientos_relacionados')
    ).filter(num_reqs=0)
    
    # Must Have sin casos (CRÍTICO)
    reqs_must_sin_casos = requerimientos.filter(
        detalle_tradicional__prioridad='MUST'
    ).annotate(
        num_casos=Count('casos_relacionados')
    ).filter(num_casos=0)
    
    # Porcentajes de cobertura
    cobertura_reqs = (reqs_con_casos / total_reqs * 100) if total_reqs > 0 else 0
    cobertura_casos = (casos_con_reqs / total_casos * 100) if total_casos > 0 else 0
    
    # Nivel de alerta
    if reqs_must_sin_casos.exists():
        nivel_alerta = 'danger'  # Crítico: Must Have sin casos
    elif cobertura_reqs < 80:
        nivel_alerta = 'warning'  # Advertencia: baja cobertura
    else:
        nivel_alerta = 'success'  # OK
    
    return render(request, 'dashboards/lider_matriz.html', {
        'proyecto': proyecto,
        'requerimientos': requerimientos,
        'casos': casos,
        'matriz_data': matriz_data,
        'total_reqs': total_reqs,
        'total_casos': total_casos,
        'reqs_con_casos': reqs_con_casos,
        'casos_con_reqs': casos_con_reqs,
        'reqs_huerfanos': reqs_huerfanos,
        'casos_huerfanos': casos_huerfanos,
        'reqs_must_sin_casos': reqs_must_sin_casos,
        'cobertura_reqs': round(cobertura_reqs, 1),
        'cobertura_casos': round(cobertura_casos, 1),
        'nivel_alerta': nivel_alerta,
    })
```

### Template Propuesto (Matriz Interactiva)

```html
<!-- En dashboards/templates/dashboards/lider_matriz.html (MEJORADO) -->
{% extends "core/base.html" %}
{% load static %}

{% block extra_css %}
<link rel="stylesheet" href="{% static 'dashboards/css/lider_matriz_styles.css' %}">
<style>
.matriz-container {
    overflow-x: auto;
    margin: 2rem 0;
}

.matriz-table {
    border-collapse: collapse;
    min-width: 100%;
    background: white;
}

.matriz-table th {
    background: #003366;
    color: white;
    padding: 12px;
    text-align: center;
    position: sticky;
    top: 0;
    z-index: 10;
}

.matriz-table th:first-child {
    background: #004080;
    text-align: left;
    min-width: 300px;
    position: sticky;
    left: 0;
    z-index: 11;
}

.matriz-table td {
    border: 1px solid #ddd;
    padding: 10px;
    text-align: center;
}

.matriz-table td:first-child {
    background: #f8f9fa;
    font-weight: 500;
    text-align: left;
    position: sticky;
    left: 0;
    z-index: 9;
}

.matriz-table tr.huerfano td:first-child {
    background: #fff3cd;
    border-left: 4px solid #ffc107;
}

.matriz-table tr.must-huerfano td:first-child {
    background: #f8d7da;
    border-left: 4px solid #dc3545;
}

.celda-vinculada {
    background: #d1ecf1;
    cursor: pointer;
    font-size: 1.5rem;
    color: #0c5460;
}

.celda-vinculada:hover {
    background: #bee5eb;
}

.celda-vacia {
    background: #f8f9fa;
    cursor: pointer;
}

.celda-vacia:hover {
    background: #e9ecef;
}

.stats-panel {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
    margin-bottom: 2rem;
}

.stat-card {
    background: white;
    padding: 1.5rem;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    text-align: center;
}

.stat-value {
    font-size: 2rem;
    font-weight: bold;
    color: #003366;
}

.stat-label {
    color: #6c757d;
    margin-top: 0.5rem;
}
</style>
{% endblock %}

{% block content %}
<div class="container-fluid mt-4">
    <h2>
        <i class="bi bi-grid-3x3-gap"></i> 
        Matriz de Trazabilidad - {{ proyecto.nombre }}
    </h2>
    
    <!-- Panel de estadísticas -->
    <div class="stats-panel">
        <div class="stat-card">
            <div class="stat-value">{{ total_reqs }}</div>
            <div class="stat-label">Requerimientos</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{{ total_casos }}</div>
            <div class="stat-label">Casos de Uso</div>
        </div>
        <div class="stat-card">
            <div class="stat-value text-success">{{ cobertura_reqs }}%</div>
            <div class="stat-label">Cobertura Requerimientos</div>
        </div>
        <div class="stat-card">
            <div class="stat-value text-info">{{ cobertura_casos }}%</div>
            <div class="stat-label">Cobertura Casos de Uso</div>
        </div>
        <div class="stat-card">
            <div class="stat-value text-warning">{{ reqs_huerfanos.count }}</div>
            <div class="stat-label">Req. Huérfanos</div>
        </div>
        <div class="stat-card">
            <div class="stat-value text-warning">{{ casos_huerfanos.count }}</div>
            <div class="stat-label">Casos Huérfanos</div>
        </div>
    </div>
    
    <!-- Alertas críticas -->
    {% if reqs_must_sin_casos %}
    <div class="alert alert-danger">
        <i class="bi bi-exclamation-triangle-fill"></i>
        <strong>¡Atención crítica!</strong> Hay {{ reqs_must_sin_casos.count }} requerimientos 
        Must Have sin casos de uso vinculados. Estos son críticos y requieren diseño de implementación urgente.
        <ul class="mb-0 mt-2">
            {% for req in reqs_must_sin_casos %}
            <li>
                <a href="{% url 'requerimientos:detalle' req.id %}" class="text-danger">
                    {{ req.nombre }}
                </a>
            </li>
            {% endfor %}
        </ul>
    </div>
    {% endif %}
    
    {% if cobertura_reqs < 80 %}
    <div class="alert alert-warning">
        <i class="bi bi-exclamation-circle"></i>
        La cobertura de requerimientos es {{ cobertura_reqs }}% (recomendado: >95%).
        Revisa los requerimientos huérfanos y vincúlalos con casos de uso.
    </div>
    {% endif %}
    
    <!-- Filtros -->
    <div class="filters mb-3">
        <button class="btn btn-sm btn-outline-primary" onclick="filtrarVista('todos')">
            Todos
        </button>
        <button class="btn btn-sm btn-outline-warning" onclick="filtrarVista('huerfanos')">
            Solo Huérfanos
        </button>
        <button class="btn btn-sm btn-outline-success" onclick="filtrarVista('vinculados')">
            Solo Vinculados
        </button>
        <button class="btn btn-sm btn-outline-danger" onclick="filtrarVista('must')">
            Must Have
        </button>
        <input type="text" id="busqueda" class="form-control d-inline-block" 
               style="width: 300px; margin-left: 1rem;" 
               placeholder="Buscar requerimiento o caso...">
    </div>
    
    <!-- Matriz bidireccional -->
    {% if requerimientos and casos %}
    <div class="matriz-container">
        <table class="matriz-table">
            <thead>
                <tr>
                    <th>Requerimiento / Caso de Uso</th>
                    {% for caso in casos %}
                    <th title="{{ caso.descripcion }}">
                        <a href="{% url 'casos_de_uso:detalle' caso.id %}" class="text-white">
                            {{ caso.nombre|truncatewords:3 }}
                        </a>
                    </th>
                    {% endfor %}
                </tr>
            </thead>
            <tbody>
                {% for item in matriz_data %}
                <tr class="{% if not item.tiene_casos %}{% if item.es_must_have %}must-huerfano{% else %}huerfano{% endif %}{% endif %}">
                    <td>
                        <a href="{% url 'requerimientos:detalle' item.requerimiento.id %}">
                            {{ item.requerimiento.nombre }}
                        </a>
                        {% if item.es_must_have %}
                            <span class="badge bg-danger">MUST</span>
                        {% endif %}
                        {% if not item.tiene_casos %}
                            <span class="badge bg-warning">⚠️ Sin casos</span>
                        {% endif %}
                    </td>
                    {% for caso in casos %}
                    <td class="{% if caso in item.casos_vinculados %}celda-vinculada{% else %}celda-vacia{% endif %}"
                        onclick="toggleVinculacion({{ item.requerimiento.id }}, {{ caso.id }})"
                        title="{% if caso in item.casos_vinculados %}Vinculado - Click para desvincular{% else %}No vinculado - Click para vincular{% endif %}">
                        {% if caso in item.casos_vinculados %}
                            ✓
                        {% endif %}
                    </td>
                    {% endfor %}
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
    {% else %}
    <div class="alert alert-info">
        <i class="bi bi-info-circle"></i>
        No hay datos suficientes para mostrar la matriz de trazabilidad.
        {% if not requerimientos %}
        <a href="{% url 'requerimientos:crear' proyecto.id %}" class="btn btn-sm btn-primary">
            Crear Requerimiento
        </a>
        {% endif %}
        {% if not casos %}
        <a href="{% url 'casos_de_uso:crear' proyecto.id %}" class="btn btn-sm btn-success">
            Crear Caso de Uso
        </a>
        {% endif %}
    </div>
    {% endif %}
    
    <!-- Botones de exportación -->
    <div class="mt-4">
        <a href="{% url 'dashboards:exportar_matriz_pdf' proyecto.id %}" class="btn btn-danger">
            <i class="bi bi-file-pdf"></i> Exportar Matriz (PDF)
        </a>
        <a href="{% url 'dashboards:exportar_matriz_excel' proyecto.id %}" class="btn btn-success">
            <i class="bi bi-file-excel"></i> Exportar Matriz (Excel)
        </a>
    </div>
</div>

<script>
function toggleVinculacion(reqId, casoId) {
    // AJAX para crear/eliminar vinculación
    fetch(`/api/trazabilidad/toggle/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            requerimiento_id: reqId,
            caso_id: casoId
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            location.reload();  // Recargar para actualizar matriz
        } else {
            alert('Error: ' + data.error);
        }
    });
}

function filtrarVista(filtro) {
    // Implementar filtrado de filas según filtro seleccionado
    const filas = document.querySelectorAll('.matriz-table tbody tr');
    
    filas.forEach(fila => {
        if (filtro === 'todos') {
            fila.style.display = '';
        } else if (filtro === 'huerfanos') {
            fila.style.display = fila.classList.contains('huerfano') || fila.classList.contains('must-huerfano') ? '' : 'none';
        } else if (filtro === 'vinculados') {
            fila.style.display = !fila.classList.contains('huerfano') && !fila.classList.contains('must-huerfano') ? '' : 'none';
        } else if (filtro === 'must') {
            fila.style.display = fila.querySelector('.badge-danger') ? '' : 'none';
        }
    });
}

// Búsqueda en tiempo real
document.getElementById('busqueda').addEventListener('input', function(e) {
    const termino = e.target.value.toLowerCase();
    const filas = document.querySelectorAll('.matriz-table tbody tr');
    
    filas.forEach(fila => {
        const texto = fila.textContent.toLowerCase();
        fila.style.display = texto.includes(termino) ? '' : 'none';
    });
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
</script>
{% endblock %}
```

### Estado de Implementación
⚠️ **IMPLEMENTADO PERO INCORRECTO**

**✅ Implementado:**
- Vista `lider_matriz` en `dashboards/views.py`
- Template `lider_matriz.html`
- URL `/dashboards/lider/matriz/` funcional

**❌ IMPLEMENTACIÓN INCORRECTA:**
- **Código actual usa heurística de coincidencia de nombres** (líneas 112-116)
- NO usa la tabla intermedia `RequerimientoCaso`
- NO respeta las vinculaciones reales creadas por usuarios
- Genera falsos positivos y puede perder vinculaciones reales
- Template actual solo muestra datos estáticos (HTML hardcodeado)

**✅ Modelo correcto YA EXISTE:**
- Tabla intermedia `RequerimientoCaso` con relación M2M
- Relación `casos_relacionados` en `Requerimiento`
- Relación `requerimientos_relacionados` en `CasoDeUso`

**❌ NO implementado:**
- Vista correcta usando relaciones reales
- Estadísticas de cobertura
- Detección de huérfanos usando relaciones
- Alertas para Must Have sin casos
- Filtros dinámicos
- Búsqueda en tiempo real
- Crear/eliminar vinculaciones desde matriz
- Exportación de matriz a PDF/Excel
- Vista de grafo/red
- Sugerencias automáticas

### Corrección Crítica Necesaria

**ANTES (INCORRECTO):**
```python
# ❌ NO hacer esto
relacionados = [cu for cu in casos if req.nombre.split()[0].lower() in cu.nombre.lower()]
```

**DESPUÉS (CORRECTO):**
```python
# ✅ Hacer esto
casos_vinculados = req.casos_relacionados.all()  # Usa la relación M2M real
```

### Prioridad de Implementación
🔴 **ALTA - CORRECCIÓN URGENTE**:
- **Código actual es INCORRECTO** y genera datos erróneos
- La matriz muestra vinculaciones que NO existen en la BD
- Puede confundir a usuarios sobre qué está realmente vinculado
- El modelo correcto YA EXISTE (solo hay que usarlo)
- Corrección es simple: reemplazar heurística por relaciones reales
- Es una de las vistas más importantes del sistema (trazabilidad)
- Complementa TODOS los casos de uso (CU-01 a CU-21)
- Crítico para auditorías y validación de completitud

### Observaciones de Revisión
✅ **Correcciones aplicadas:**
- **IDENTIFICADO ERROR CRÍTICO:** código usa coincidencia de nombres en lugar de relaciones reales
- Explicado por qué el código actual es incorrecto
- Propuesto código correcto usando `casos_relacionados.all()`
- Template completo con matriz interactiva y estadísticas
- Filtros dinámicos (todos, huérfanos, vinculados, Must Have)
- Búsqueda en tiempo real con JavaScript
- Crear/eliminar vinculaciones desde la matriz
- Alertas críticas para Must Have sin casos
- Panel de estadísticas de cobertura
- Vista de lista como alternativa
- Vista de grafo para análisis de dependencias
- Exportación a PDF/Excel
- Sugerencias automáticas de vinculación
- **PRIORIDAD ALTA** porque el código actual genera datos erróneos

---

## 🎉 RESUMEN FINAL - TODOS LOS CASOS DE USO COMPLETADOS

**Total de casos de uso documentados: 23 (CU-00 a CU-22)**

### Estado de Implementación General

| Estado | Cantidad | Casos de Uso |
|--------|----------|--------------|
| ✅ **Implementado** | 7 | CU-00, CU-01, CU-02, CU-03, CU-04, CU-05, CU-07 |
| ⚠️ **Parcialmente Implementado** | 7 | CU-06, CU-10, CU-11, CU-12, CU-15, CU-16, CU-17, CU-20, CU-21 |
| 🔴 **Implementado INCORRECTO** | 1 | **CU-22** (usa heurística, no relaciones reales) |
| ⏳ **Planificado** | 2 | CU-18, CU-19 (comentarios) |
| ❌ **NO Implementado** | 6 | CU-08, CU-09, CU-13, CU-14 |

### Hallazgos Críticos

1. **🔴 CU-22 (Matriz de Trazabilidad) - ERROR CRÍTICO**
   - Código actual usa coincidencia de nombres
   - NO usa tabla intermedia `RequerimientoCaso`
   - Genera datos erróneos
   - **Corrección urgente necesaria**

2. **⚠️ CU-15 (Generar Matriz) - MISMO ERROR**
   - Usa misma lógica incorrecta que CU-22
   - Debe corregirse junto con CU-22

3. **✅ Modelo de Trazabilidad CORRECTO**
   - Tabla `RequerimientoCaso` existe y funciona
   - Relaciones M2M implementadas correctamente
   - Solo falta usar en vistas

4. **⏳ Sistema de Comentarios PLANIFICADO**
   - CU-18 y CU-19 se implementarán pronto
   - Todos los usuarios podrán comentar
   - Infraestructura completa propuesta

5. **❌ Funcionalidades Mayores Faltantes**
   - Historial de cambios (CU-08, CU-09)
   - Adjuntos en requerimientos/casos (CU-13, CU-14)
   - Generación real de informes PDF/Excel (CU-21 parcial)

### Próximos Pasos Recomendados

**Prioridad CRÍTICA:**
1. 🔴 Corregir CU-22 (matriz de trazabilidad) - usar relaciones reales
2. 🔴 Corregir CU-15 (generar matriz) - mismo fix

**Prioridad ALTA:**
3. 🟢 Implementar CU-18 y CU-19 (sistema de comentarios planificado)
4. 🟡 Completar CU-20 (validación) - agregar choices y metadatos
5. 🟡 Implementar vistas reales de informes PDF/Excel (CU-21)

**Prioridad MEDIA:**
6. Implementar CU-13 y CU-14 (adjuntos)
7. Completar CU-06 (eliminar req/caso con validación)
8. Implementar CU-08 y CU-09 (historial)

### Documentación Completa ✅

Todos los 23 casos de uso han sido:
- ✅ Revisados según implementación real
- ✅ Corregidos con flujos detallados
- ✅ Documentados con código de ejemplo
- ✅ Marcados con estado actual de implementación
- ✅ Priorizados según importancia
- ✅ Incluidos con observaciones técnicas

**¡Documento CASOS_DE_USO_REVISADOS.md completado!** 🎊

