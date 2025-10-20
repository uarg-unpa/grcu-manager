# Gestión de Roles de Integrantes - Caso de Uso 04

## Resumen
Se ha implementado la funcionalidad para que el **Líder del Proyecto** pueda asignar roles a los integrantes de su proyecto.

## Características Implementadas

### 1. **Vista: `gestionar_integrantes`** 
**Archivo:** `proyectos/views.py`

- ✅ Solo el líder del proyecto puede acceder
- ✅ Muestra todos los integrantes del proyecto con sus roles actuales
- ✅ Permite cambiar roles a: **Desarrollador** (default), **Stakeholder** (Cliente) o **Visitante**
- ✅ El líder NO puede cambiar su propio rol
- ✅ Validaciones de seguridad y permisos
- ✅ Creación automática de `ParticipacionProyecto` si no existe (con rol Desarrollador por defecto)

### 2. **Template: `gestionar_integrantes.html`**
**Archivo:** `proyectos/templates/proyectos/gestionar_integrantes.html`

**Secciones:**
- **Breadcrumb de navegación** - Para volver al dashboard
- **Información del proyecto** - Card con logo, nombre y metodología
- **Tabla de integrantes** - Listado con:
  - Avatar circular con inicial del nombre
  - Nombre y email del usuario
  - Select dropdown para cambiar rol (deshabilitado para el líder)
  - Badge indicando si es líder
- **Descripción de roles** - Card informativo con detalles de cada rol
- **Confirmación JavaScript** - Antes de guardar cambios

### 3. **Estilos: `gestionar_integrantes.css`**
**Archivo:** `proyectos/static/proyectos/css/gestionar_integrantes.css`

- ✨ Avatares circulares con gradientes
- ✨ Hover effects en tabla
- ✨ Transiciones suaves
- ✨ Diseño responsive
- ✨ Animaciones de entrada (fadeIn)

### 4. **URL Route**
**Archivo:** `proyectos/urls.py`

```python
path("<int:proyecto_id>/integrantes/", views.gestionar_integrantes, name="gestionar_integrantes")
```

### 5. **Botón en Dashboard del Líder**
**Archivo:** `dashboards/templates/dashboards/lider_dashboard.html`

- 🔵 Nuevo botón **"Gestión de Integrantes"** en el header de cada proyecto
- 🔵 Con icono `bi-people-fill` y tooltip informativo
- 🔵 Ubicado junto al botón de "Asignar Metodología"

## Roles Disponibles

| Rol | Descripción | Por Defecto |
|-----|-------------|-------------|
| **Desarrollador** | Puede crear, editar y gestionar requerimientos y casos de uso | ✅ Sí |
| **Stakeholder** (Cliente) | Representa al cliente. Puede revisar y aprobar requerimientos | ❌ No |
| **Visitante** | Solo lectura. Puede visualizar sin realizar cambios | ❌ No |
| **Líder** | Gestiona el proyecto (asignado automáticamente, NO modificable desde aquí) | ❌ No |

## Flujo de Uso

1. **Líder accede a su dashboard** → Ve sus proyectos
2. **Click en "Gestión de Integrantes"** → Abre página de gestión
3. **Ve tabla con todos los integrantes** → Con sus roles actuales
4. **Cambia roles usando dropdowns** → Selecciona nuevo rol para cada usuario
5. **Click en "Guardar Cambios"** → Confirma y actualiza roles
6. **Mensaje de éxito** → Vuelve a la página de gestión actualizada

## Validaciones de Seguridad

- ✅ Solo el líder del proyecto puede acceder a esta vista
- ✅ No se puede cambiar el rol del líder del proyecto
- ✅ Solo se pueden asignar roles permitidos (Desarrollador, Stakeholder, Visitante)
- ✅ Se valida que el usuario sea participante del proyecto
- ✅ Confirmación JavaScript antes de guardar cambios

## Archivos Modificados/Creados

### Creados:
- ✨ `proyectos/templates/proyectos/gestionar_integrantes.html` (181 líneas)
- ✨ `proyectos/static/proyectos/css/gestionar_integrantes.css` (168 líneas)

### Modificados:
- 📝 `proyectos/views.py` - Añadida vista `gestionar_integrantes` (95 líneas)
- 📝 `proyectos/urls.py` - Añadida ruta para gestión de integrantes
- 📝 `dashboards/templates/dashboards/lider_dashboard.html` - Añadido botón de gestión

## Testing

✅ `python manage.py check` - Sin errores
✅ Sin errores de lint en VS Code

## Próximos Pasos Sugeridos

1. Probar la funcionalidad con usuarios reales
2. Verificar que los permisos funcionan correctamente según el rol asignado
3. Añadir auditoría de cambios de roles (opcional)
4. Considerar añadir un historial de cambios de roles (opcional)
