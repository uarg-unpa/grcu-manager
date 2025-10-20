# Refactorización: admin_proyecto_detail → proyectos app

## Resumen
Se ha movido la funcionalidad `admin_proyecto_detail` desde la app **dashboards** a la app **proyectos**, donde corresponde arquitectónicamente.

## Motivación
La vista de detalle de un proyecto es responsabilidad de la app `proyectos`, no de `dashboards`. Los dashboards deben ser agregadores de información, mientras que las vistas específicas de entidades pertenecen a sus respectivas apps.

## Cambios Realizados

### 1. **Vista Movida**

**Desde:** `dashboards/views.py` → `admin_proyecto_detail()`  
**Hacia:** `proyectos/views.py` → `proyecto_detail_admin()`

**Mejoras aplicadas:**
- ✅ Renombrada a `proyecto_detail_admin` para mayor claridad
- ✅ Agregado `page_title` al contexto para título dinámico
- ✅ Corregidos estados de requerimientos: `EN_PROGRESO` → `EN_DESARROLLO`, `COMPLETADO` → `APROBADO`
- ✅ Documentación mejorada con docstring

**Código:**
```python
@login_required
def proyecto_detail_admin(request, proyecto_id):
    """
    Vista detallada de un proyecto para administradores.
    Muestra toda la información del proyecto incluyendo integrantes, requerimientos,
    casos de uso, métricas y gráficos.
    """
    # ... implementación ...
    context = {
        'page_title': f'Detalle del Proyecto - {proyecto.nombre}',
        # ... resto del contexto ...
    }
    return render(request, 'proyectos/proyecto_detail_admin.html', context)
```

### 2. **Template Movido**

**Desde:** `dashboards/templates/dashboards/admin_project_detail.html`  
**Hacia:** `proyectos/templates/proyectos/proyecto_detail_admin.html`

**Mejoras aplicadas:**
- ✅ Agregado `{% block title %}{{ page_title }}{% endblock %}`
- ✅ Eliminado el título `<h3>{{ proyecto.nombre }}</h3>` del cuerpo (ya aparece en el header)
- ✅ Template ahora sigue el patrón de título dinámico del resto del sistema

### 3. **URL Añadida en proyectos**

**Archivo:** `proyectos/urls.py`

```python
path("<int:proyecto_id>/detail/", views.proyecto_detail_admin, name="proyecto_detail_admin"),
```

### 4. **Retrocompatibilidad en dashboards**

**Archivo:** `dashboards/views.py`

La vista antigua ahora redirige a la nueva ubicación para mantener compatibilidad:

```python
@login_required
def admin_proyecto_detail(request, project_id):
    """
    Redirige a la vista de detalle del proyecto en la app proyectos.
    Mantiene compatibilidad con URLs antiguas.
    """
    return redirect('proyectos:proyecto_detail_admin', proyecto_id=project_id)
```

### 5. **Referencias Actualizadas**

**Archivo:** `proyectos/templates/proyectos/lista_proyectos.html`

```html
<!-- ANTES -->
<a href="{% url 'dashboards:admin_proyecto_detail' proyecto.id %}" ...>

<!-- DESPUÉS -->
<a href="{% url 'proyectos:proyecto_detail_admin' proyecto.id %}" ...>
```

## Estructura de URLs

### Antes:
```
/dashboard/admin/proyecto/<id>/  → dashboards:admin_proyecto_detail
```

### Ahora:
```
/proyectos/<id>/detail/           → proyectos:proyecto_detail_admin (nueva ubicación)
/dashboard/admin/proyecto/<id>/  → Redirige a la nueva ubicación (retrocompatibilidad)
```

## Beneficios de la Refactorización

### ✅ **Arquitectura Limpia:**
- Cada app maneja sus propias responsabilidades
- `proyectos` gestiona todo lo relacionado con proyectos
- `dashboards` solo agrega información

### ✅ **Consistencia:**
- Todas las vistas de proyectos en un solo lugar
- URLs organizadas bajo el namespace `proyectos:`
- Patrón de nombres coherente: `proyecto_<accion>`

### ✅ **Mantenibilidad:**
- Más fácil encontrar código relacionado
- Imports más lógicos
- Reducción de dependencias cruzadas

### ✅ **Título Dinámico:**
- Sigue el patrón del resto del sistema
- El título aparece en el header, no duplicado en el cuerpo
- Contexto más limpio

## Archivos Modificados

### Modificados:
- 📝 `proyectos/views.py` - Añadida vista `proyecto_detail_admin` (90 líneas)
- 📝 `proyectos/urls.py` - Añadida ruta para detalle de proyecto
- 📝 `dashboards/views.py` - Convertida vista antigua en redirect (10 líneas)
- 📝 `proyectos/templates/proyectos/lista_proyectos.html` - Actualizada referencia de URL
- 📝 `proyectos/templates/proyectos/proyecto_detail_admin.html` - Añadido título dinámico, eliminado título duplicado

### Movidos:
- 🔄 `dashboards/templates/dashboards/admin_project_detail.html` → `proyectos/templates/proyectos/proyecto_detail_admin.html`

## Testing

✅ `python manage.py check` - Sin errores  
✅ Sin errores de lint en VS Code  
✅ Retrocompatibilidad mantenida (URLs antiguas redirigen)  
✅ Referencias actualizadas

## Patrón de Organización

Esta refactorización establece el patrón para futuras vistas:

| Vista | App Correcta | Razón |
|-------|--------------|-------|
| Detalle de proyecto | `proyectos` | Pertenece a la entidad Proyecto |
| Lista de proyectos | `proyectos` | Pertenece a la entidad Proyecto |
| Matriz de trazabilidad | `proyectos` | Relacionado con proyectos |
| Reportes de proyecto | `proyectos` | Relacionado con proyectos |
| Dashboard del líder | `dashboards` | Agrega información de múltiples fuentes |
| Dashboard del desarrollador | `dashboards` | Agrega información de múltiples fuentes |
| Dashboard del admin | `dashboards` | Agrega información de múltiples fuentes |

## Próximos Pasos Sugeridos

1. Verificar que todos los links funcionan correctamente
2. Probar la vista con usuarios administradores
3. Considerar eliminar el redirect después de un período de transición
4. Documentar el nuevo patrón en guías de desarrollo

## Notas

- La vista antigua en dashboards se mantiene solo como redirect para retrocompatibilidad
- Se puede eliminar después de verificar que no hay enlaces externos o bookmarks
- El template ahora sigue el patrón de título dinámico del resto del sistema
- Los estados de requerimientos fueron corregidos para coincidir con el modelo actual
