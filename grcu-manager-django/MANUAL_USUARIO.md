# Manual de Usuario — GRCU Manager

Autores: Nicolás Butterfield, Abril Alvarez, Martina Gagna, Cristian Carranza
Contacto: nicbutter@gmail.com
Versión: 1.0

---

## Contenido
- Introducción
- Público objetivo
- Quickstart (5 minutos)
- Navegación general
- Roles y permisos
- Flujos clave
  - Crear un Requerimiento
  - Editar un Requerimiento
  - Validar / Aprobar / Rechazar
  - Priorizar / Revertir priorización
  - Crear y editar Caso de Uso
  - Añadir comentarios y colaborar
- Historial y comparación de versiones
- Gestión de Fuentes y Categorías
- Gestión de usuarios y grupos
- Paneles y reportes
- Solución de problemas comunes
- FAQ
- Apéndice: capturas y ejemplos

---

## Introducción

Este manual explica cómo usar GRCU Manager desde la perspectiva de usuario (administradores, líderes, desarrolladores y stakeholders/cliente). Aquí encontrarás guías paso a paso, ejemplos y capturas (placeholders) para las tareas más comunes: crear y gestionar requerimientos, casos de uso, validar cambios, priorizar, y revisar el historial de versiones.

## Público objetivo

- Líderes de proyecto
- Desarrolladores
- Stakeholders / Clientes
- Administradores del sistema

## Quickstart (5 minutos)

1. Abrí la URL de la aplicación y accedé con tu cuenta Google o con las credenciales provistas.

2. Caso especial — primer despliegue / creación del administrador:
   - Si la base de datos todavía no tiene usuarios administradores, la aplicación redirigirá automáticamente a la pantalla de configuración inicial (`setup-admin`) para crear el primer administrador del sistema.
   - Este comportamiento está pensado para que uno de los docentes o responsable academico cree el primer usuario administrador. Ese usuario podrá luego gestionar usuarios, proyectos y permisos.

3. Flujo normal de autenticación:
   - Tras autenticación con Google, si el email del usuario ya existe en la base de datos y está registrado (por ejemplo, lo cargó previamente un administrador), el sistema permitirá el acceso y redirigirá al dashboard correspondiente según el rol.
   - Si el email no está registrado en el sistema, el login fallará y mostrará un mensaje indicando que "No estás registrado en el sistema". En ese caso contactá a un administrador para que agregue tu cuenta.

4. Crear tu primer Requerimiento (una vez logueado con una cuenta válida):
   - Ir a la sección "Requerimientos" en la barra de navegación.
   - Pulsar el botón "Crear Requerimiento".
   - Completar el formulario: título, descripción, fuente, categoría y prioridad.
   - Guardar. El requerimiento quedará en estado BORRADOR/VALIDADO según el flujo de tu proyecto.

5. Para ver el historial de un requerimiento:
   - Abrí el Requerimiento → pestaña "Historial" → seleccioná versiones y pulsá "Comparar".

_Nota_: en el manual hay placeholders para capturas: `screenshots/xxx.png`. Podés reemplazarlas por imágenes reales más adelante.

## Navegación general

- Header: acceso a perfil y notificaciones.
- Navbar lateral/ superior: enlaces a `Dashboards`, `Proyectos`, `Requerimientos`, `Casos de Uso`, `Reportes`, `Matriz`.
- Área principal: listado o formulario según la vista.
- Footer: créditos y enlaces institucionales.

![Ejemplo de dashboard](screenshots/dashboard_main.png)

## Roles y permisos

- Admin: todo el acceso (crear/editar/eliminar proyectos, gestionar usuarios, ver reportes).
- Líder: priorizar requerimientos, validar, asignar tareas dentro de su proyecto.
- Stakeholder / Cliente: revisar requerimientos, comentar y aprobar/validar cuando corresponda.
- Desarrollador: ver requerimientos asignados, comentar y marcar tareas como en progreso/completadas según el workflow.
- Visitante: acceso de sólo lectura limitado.

**Reglas importantes sobre edición y validación**

- Solo el creador de un Requerimiento o Caso de Uso, o el Líder del proyecto, pueden editar ese elemento. Esto asegura trazabilidad y control de cambios.
- La validación formal de un Requerimiento solo puede realizarla el Líder del proyecto, y debe hacerse después de una discusión con el cliente (stakeholder) cuyo objetivo es aclarar la interpretación del requerimiento por parte del equipo. Una vez el Líder valida el requerimiento, este entra en el proceso operativo del proyecto (por ejemplo priorización y asignación).

## Flujos clave

### Crear un Requerimiento

1. Ir a `Requerimientos` → `Crear Requerimiento`.
2. Completar campos obligatorios (título, descripción).
3. Seleccionar `Fuente` y `Categoría` (o crear nueva fuente/categoría si el permiso lo permite).
4. Guardar.

Placeholder imagen: `screenshots/requerimiento_create.png`

### Editar un Requerimiento

- Seleccionar el requerimiento desde la lista y pulsar `Editar`.
- Realizar cambios y guardar. Si existiera control de permisos, la acción podría estar limitada a creador o líder.

### Validar / Aprobar / Rechazar


- Desde la vista de detalle, únicamente el Líder podrá ejecutar la acción de `Validar` (previa discusión con el Cliente). Los stakeholders pueden proponer la validación y dejar comentarios, pero la acción final de validar la toma el Líder.

- Discusión y adjuntos: cada Requerimiento incluye un sistema de discusión donde Líder y Cliente (y otros participantes autorizados) pueden intercambiar mensajes. En los comentarios se pueden:
   - Adjuntar imágenes (capturas, mockups).
   - Pegar URLs relevantes (documentación externa, prototipos, tickets relacionados).

- Los comentarios y adjuntos quedan registrados como parte del historial del Requerimiento y se conservan para trazabilidad.

- Añadir comentario al validar/rechazar para dejar registro de decisiones y la razón de la aprobación o rechazo.

Flujo tras la validación:

- Cuando el Líder valida un Requerimiento después de la discusión con el Cliente, el Requerimiento pasa a formar parte del flujo operativo del proyecto: será priorizado, planificado, ejecutado y finalmente cerrado una vez completado.

- Durante todo el ciclo, los comentarios y adjuntos permanecen asociados al Requerimiento para facilitar revisiones, auditorías y comparaciones.

### Estados del Requerimiento

Los estados del ciclo de vida de un Requerimiento en la aplicación son:

- BORRADOR: el Requerimiento ha sido creado pero aún no fue validado por el Líder.
- VALIDADO: el Líder confirmó la interpretación del Requerimiento tras la discusión con el Cliente; el Requerimiento está listo para priorizarse.
- PRIORIZADO: el Requerimiento fue clasificado por prioridad (por ejemplo usando MoSCoW) y está listo para ser planificado.
- EN PROCESO: el Requerimiento está siendo trabajado por el equipo (implementación, pruebas, etc.).
- TERMINADO: el trabajo asociado al Requerimiento se completó y fue marcado como finalizado.

Dependiendo del flujo de tu proyecto puede haber estados intermedios o adicionales (por ejemplo 'En revisión' o 'En pruebas'), pero la secuencia habitual en la aplicación es:

BORRADOR → VALIDADO → PRIORIZADO → EN PROCESO → TERMINADO

Notas:

- Tras la validación, las herramientas de priorización y planificación lo incorporan al backlog del proyecto.
- Los adjuntos y comentarios en la discusión quedan asociados al Requerimiento y se conservan en el historial para trazabilidad.

### Cobertura por Casos de Uso

Un Requerimiento solo puede declararse como "cubierto" por uno o más Casos de Uso cuando el Requerimiento ha alcanzado el estado VALIDADO. Esto garantiza que los Casos de Uso reflejen requisitos ya consensuados y reduce el riesgo de que trabajo se base en especificaciones incompletas o equivocadas.

Flujo recomendado:

- Crear el Requerimiento (BORRADOR).
- Discutir el Requerimiento con stakeholders y equipo.
- El Líder valida el Requerimiento (pasa a VALIDADO).
- A partir de ese momento, se pueden crear Casos de Uso que referencien y cubran el Requerimiento validado.

Si un Caso de Uso intenta cubrir un Requerimiento no validado, la aplicación mostrará una advertencia y no permitirá la asociación hasta que el Requerimiento sea VALIDADO.

### Dependencias entre Requerimientos

Los Requerimientos pueden declararse dependientes de otros Requerimientos del mismo proyecto. Esto permite modelar restricciones de orden (por ejemplo: "Requerimiento B depende de A" significa que B no debería ser implementado antes de A).

Buenas prácticas para gestionar dependencias:

- Declara las dependencias claramente en el Requerimiento (uno o varios dependencias posibles).
- Evita ciclos de dependencia (A depende de B y B depende de A). El sistema advertirá si detecta referencias circulares.
- Usa las dependencias para orientar la priorización y la planificación: un Requerimiento con dependencias pendientes normalmente debe esperar a que sus predecesores estén VALIDADOS y/o PRIORIZADOS.

### Priorización — técnica MoSCoW

La priorización en la aplicación se realiza usando la técnica MoSCoW (Must / Should / Could / Won't). Esta clasificación ayuda a tomar decisiones prácticas sobre qué entregar en cada iteración:

- Must: requisitos que son imprescindibles para el éxito del proyecto en la entrega objetivo.
- Should: requisitos importantes, pero no críticos; se implementan si el tiempo/recursos lo permiten.
- Could: requisitos deseables pero de bajo impacto; se consideran solo si hay capacidad.
- Won't (this time): requisitos que se descartan de la entrega actual (pueden reconsiderarse en futuras versiones).

Cómo usar MoSCoW en la app:

- Al validar un Requerimiento, el Líder puede asignarle una categoría MoSCoW.
- La priorización global del backlog mostrará las categorías MoSCoW para ayudar en la toma de decisiones.
- Revisa dependencias: un "Must" que depende de un elemento no priorizado puede requerir que su dependencia también se eleve en la prioridad.

Con estas reglas el equipo mantiene mejor control sobre qué se implementa primero y evita comenzar Casos de Uso que cubran Requerimientos no consensuados o bloqueados por dependencias.

### Priorizar / Revertir priorización

- Los líderes pueden priorizar requerimientos (paso a PRIORIZADO). Si se necesita revertir hay un control específico `Revertir a VALIDADO`.

### Crear y editar Caso de Uso

- Los casos de uso se crean desde `Casos de Uso` → `Crear Caso de Uso`.
- Incluir los pasos principales, actores, precondiciones y resultados esperados.

### Añadir comentarios y colaborar

- En cada Requerimiento y Caso de Uso existe un área de comentarios para discusión entre desarrolladores y clientes.
- Los comentarios quedan registrados y forman parte del historial de la entidad.

El sistema de discusión soporta dos canales distintos:

1. Discusión pública (Líder ↔ Cliente / Stakeholders):
   - Diseñada para la comunicación entre el Líder y el Cliente y para dejar registro visible de las decisiones.
   - Estos hilos y sus comentarios son visibles para todos los participantes del proyecto (administradores, líderes, desarrolladores asignados, stakeholders con acceso).
   - En esta modalidad se permite adjuntar imágenes y pegar URLs relevantes; los archivos y enlaces quedan asociados al requerimiento.

2. Discusión interna (Equipo de desarrollo):
   - Pensada para conversaciones técnicas internas (sugerencias, código, detalles de implementación) que no deben ser visibles para el Cliente.
   - Solo los miembros del equipo de desarrollo y administradores con permisos verán estos comentarios.
   - Al crear un comentario, la UI incluye una opción para marcarlo como "Interno"; por defecto los comentarios son públicos (no internos).

Comportamiento y buenas prácticas:

- El Líder puede iniciar ambos tipos de hilos según la naturaleza del intercambio. Si la conversación implica decisiones con el Cliente, preferir el canal público.
- Los comentarios internos no aparecen en los reportes compartidos con el Cliente y no se indexan en vistas públicas del proyecto.
- Mantener limpias las discusiones públicas: usar comentarios públicos para acuerdos y decisiones, y usar las internas para notas de implementación o comunicaciones sensibles.

## Historial y comparación de versiones

- Cada Requerimiento y Caso de Uso mantiene un historial (simple-history). Podés ver versiones anteriores, quién las modificó y comparar campos.
- En la vista `Historial` seleccionar dos versiones y pulsar `Comparar` para ver sólo los campos que cambiaron.

Placeholder imagen: `screenshots/historial_compare.png`

## Gestión de Fuentes y Categorías

- Fuentes y Categorías se administran desde `Requerimientos` → `Fuentes/Categorías`.
- Se soporta la creación automática al crear proyectos si corresponde.

## Gestión de usuarios y grupos

Los administradores pueden asignar roles a usuarios y gestionar la creación masiva de cuentas; los líderes pueden gestionar integrantes de su proyecto y asignaciones internas.

### Flujo docente — creación de usuarios, grupos y proyectos

1. Recolección de emails por parte del docente:
   - El docente solicita a los alumnos de la cátedra sus emails institucionales. Estos emails serán las cuentas que usarán en el sistema.

2. Envío de información al administrador del sistema:
   - El docente remite al administrador (usuario con rol Admin) la lista de emails, además de los nombres de los grupos que se formarán y, si corresponde, un logo por grupo.

3. Creación de usuarios por el administrador:
   - El administrador crea las cuentas de usuario usando los emails provistos. Estas cuentas pueden crearse individualmente o mediante una carga masiva (según la funcionalidad disponible en la administración).

4. Creación de grupos y asignación de integrantes:
   - El administrador crea los grupos en la sección `Grupos` (nombre del grupo, logo opcional) y asigna a cada grupo los alumnos correspondientes como integrantes.

5. Creación del proyecto y asignación del grupo:
   - El administrador o docente crea el Proyecto correspondiente y asigna el grupo asociado al proyecto. Cada proyecto definido por el cuerpo docente debe tener un grupo asignado que lo represente en el sistema.

6. Selección del Líder de proyecto:
   - Al asignar el grupo al proyecto, se debe seleccionar uno de los integrantes del grupo como Líder del proyecto. El Líder recibe permisos adicionales (priorizar, validar dentro del proyecto, gestionar asignaciones internas).

7. Asignación de usuario Cliente y Visitante (opcionales):
   - Se pueden asignar además un usuario con rol Cliente y otro con rol Visitante al proyecto.
   - Importante: los usuarios Cliente y Visitante deben existir previamente y no pertenecer a ningún grupo del proyecto (son cuentas externas o de stakeholders que no forman parte de los equipos estudiantiles).

Notas y buenas prácticas:

- Verificá que los emails estén correctamente escritos antes de crear cuentas para evitar problemas de acceso con Google OAuth.
- Si la aplicación soporta carga masiva, preferila para evitar errores manuales al crear muchas cuentas.
- Documentá quién es responsable de la carga (docente o administrador) para mantener trazabilidad.
- Controlá que el Líder asignado efectivamente pertenezca al grupo seleccionado; la UI mostrará solo integrantes válidos al seleccionar el líder.

## Paneles y reportes

- `Matriz` y `Reportes` ofrecen vistas para rastrear trazabilidad y generar reportes resumidos.

### Generar reportes personalizados

Los Líderes, Clientes (stakeholders con acceso) y Desarrolladores pueden generar reportes PDF personalizados desde la sección `Reportes`. La interfaz permite seleccionar qué secciones incluir en el reporte mediante casillas de verificación, de forma similar al modal de selección que aparece en la aplicación.

Secciones típicas que se pueden seleccionar:

- Equipo del Proyecto: lista de participantes con roles y avatares.
- Resumen Ejecutivo: métricas, cobertura y estadísticas del proyecto.
- Matriz de Trazabilidad: relación entre Requerimientos y Casos de Uso.
- Listado Detallado de Requerimientos: descripción completa de cada requerimiento.
- Listado Detallado de Casos de Uso: descripción completa de cada caso de uso.
- Recomendaciones: sugerencias de mejora basadas en el análisis.
- Información del Grupo: detalles del grupo asociado al proyecto.

Uso del modal de generación:

1. Abrí `Reportes` → `Generar Reporte`.
2. Marcá las casillas de las secciones que querés incluir.
3. Pulsá `Generar Reporte`. El sistema preparará un PDF con las secciones seleccionadas y te ofrecerá descargarlo o, según la configuración, te lo enviará por email cuando esté listo.

Notas importantes:

- Los comentarios marcados como "Internos" (discusión interna) no se incluirán en los reportes públicos o en los PDFs generados para el Cliente.
- Si seleccionás la Matriz de Trazabilidad, el reporte incluirá las relaciones entre Requerimientos y Casos de Uso, útil para auditorías y revisión de cobertura.
- El proceso de generación puede tardar en proyectos grandes; el sistema puede notificar por email cuando el reporte esté disponible.

Placeholder imagen modal: `screenshots/report_modal.png`

## Solución de problemas comunes

- No puedo ver el botón de editar: verificá tu rol y si sos creador o líder del elemento.
- Al comparar versiones no hay diferencias: confirmá que las versiones seleccionadas sean distintas; de lo contrario no habrá cambios.

## FAQ

- ¿Cómo se registra quién modificó? — El sistema guarda `history_user` en cada cambio si la acción pasa por la vista que establece `_history_user`.

## Apéndice: capturas y ejemplos


- `screenshots/dashboard_main.png` — Vista principal del dashboard.
- `screenshots/requerimiento_create.png` — Formulario de creación de requerimiento.
- `screenshots/historial_compare.png` — Comparación de versiones.

---

Fin del manual (esqueleto).
