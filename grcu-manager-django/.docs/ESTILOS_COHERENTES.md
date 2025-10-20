# 🎨 Guía de Estilos Coherentes - GRCU Manager

## 📋 Esquema de Colores Institucionales

### Requerimientos (Verde)
- **Color Principal**: `#28A745` (Verde Bootstrap Success)
- **Color Secundario**: `#20C997` (Verde Teal)
- **Gradiente**: `linear-gradient(135deg, #28A745 0%, #20C997 100%)`
- **Uso**: Headers, botones principales, cards de requerimientos

### Casos de Uso (Azul Cian)
- **Color Principal**: `#17A2B8` (Azul Info)
- **Color Secundario**: `#138496` (Azul Info Oscuro)
- **Gradiente**: `linear-gradient(135deg, #17A2B8 0%, #138496 100%)`
- **Uso**: Headers, botones principales, cards de casos de uso

### Estados de Requerimientos
- **Pendiente**: `#FFC107` (Amarillo Warning)
- **En Desarrollo**: `#17A2B8` (Azul Info)
- **Aprobado**: `#28A745` (Verde Success)

### Tipos de Requerimientos
- **Funcional**: `#007BFF` (Azul Primary)
- **No Funcional**: `#6C757D` (Gris Secondary)

### Tipos de Casos de Uso
- **Tradicional**: `#6F42C1` (Morado)
- **Ágil**: `#FD7E14` (Naranja)

### Alertas y Estados Especiales
- **Huérfano**: `#DC3545` (Rojo Danger)
- **Enlace a Caso de Uso**: `#17A2B8` (Azul Info)

---

## 🎯 Componentes Estandarizados

### 1. Headers de Página

**Estructura HTML:**
```html
<div class="page-header-[tipo] d-flex justify-content-between align-items-center">
  <div class="header-title">
    <i class="bi bi-[icono]"></i>
    <span class="fs-4 fw-bold">[Título]</span>
  </div>
  <a href="#" class="btn btn-crear-[tipo]">
    <i class="bi bi-plus-circle-fill me-2"></i>
    Nuevo [Elemento]
  </a>
</div>
```

**CSS Común:**
- Padding: `20px`
- Border radius: `8px`
- Margin bottom: `24px`
- Font size icono: `2rem`
- Box shadow: `0 4px 8px rgba([color], 0.2)`

### 2. Cards de Listado

**Estructura:**
```html
<div class="card [tipo]-list-card">
  <div class="table-responsive mb-0">
    <table class="table table-bordered table-hover align-middle mb-0">
      <!-- contenido -->
    </table>
  </div>
</div>
```

**CSS Común:**
- Border: `1.5px solid [color-principal]`
- Border radius: `8px`
- Box shadow: `0 2px 8px rgba([color], 0.08)`
- Overflow: `hidden`

### 3. Headers de Tabla

**CSS Común:**
- Background: `linear-gradient(135deg, [color1] 0%, [color2] 100%)`
- Color: `#fff`
- Padding: `14px 12px`
- Font weight: `600`
- Text transform: `uppercase`
- Font size: `0.85rem`
- Letter spacing: `0.5px`

### 4. Filas de Tabla

**CSS Común:**
- Transition: `all 0.2s ease`
- Hover background: `rgba([color], 0.05)`
- Hover transform: `translateY(-1px)`
- Hover box shadow: `0 2px 4px rgba(0, 0, 0, 0.05)`
- Padding: `12px`

### 5. Botones Principales

**Clases:**
- `.btn-crear-requerimiento` (Verde)
- `.btn-crear-caso-uso` (Azul)

**CSS Común:**
- Background: `linear-gradient(135deg, [color1] 0%, [color2] 100%)`
- Border: `none`
- Color: `white`
- Font weight: `600`
- Padding: `10px 24px`
- Border radius: `8px`
- Transition: `all 0.3s ease`
- Box shadow: `0 3px 6px rgba([color], 0.3)`

**Hover:**
- Background: `linear-gradient(135deg, [color2] 0%, [color1] 100%)` (invertido)
- Transform: `translateY(-2px)`
- Box shadow: `0 6px 12px rgba([color], 0.4)`

### 6. Botones de Acción

**Clases:**
- `.btn-action-req` (Requerimientos)
- `.btn-action-caso` (Casos de Uso)

**CSS Común:**
- Padding: `6px 12px`
- Border radius: `6px`
- Transition: `all 0.2s ease`
- Font size: `0.9rem`

**Hover:**
- Transform: `translateY(-2px)`
- Box shadow: `0 4px 8px rgba(0, 0, 0, 0.15)`

### 7. Badges

#### Badge Huérfano
```css
.badge-huerfano {
    background: linear-gradient(135deg, #dc3545 0%, #c82333 100%);
    color: white;
    padding: 6px 12px;
    border-radius: 6px;
}
```

#### Badge Caso de Uso
```css
.badge-caso-uso {
    background: linear-gradient(135deg, #17A2B8 0%, #138496 100%);
    color: white;
    padding: 5px 10px;
    border-radius: 6px;
    text-decoration: none;
}
```

#### Badge Tradicional/Ágil
```css
.badge-tradicional {
    background: linear-gradient(135deg, #6f42c1 0%, #5a32a3 100%);
}

.badge-agil {
    background: linear-gradient(135deg, #fd7e14 0%, #e8590c 100%);
}
```

### 8. Contenedor de Filtros

**HTML:**
```html
<div class="filtros-container">
  <div class="d-flex gap-2 align-items-center flex-wrap">
    <!-- inputs y selects -->
  </div>
</div>
```

**CSS:**
- Background: `#f8f9fa`
- Padding: `16px`
- Border radius: `8px`
- Border: `1px solid #e9ecef`
- Margin bottom: `20px`

### 9. Empty States

**HTML:**
```html
<div class="empty-state-[tipo]">
  <i class="bi bi-inbox"></i>
  <p class="mb-0">No hay [elementos] disponibles.</p>
</div>
```

**CSS:**
- Text align: `center`
- Padding: `60px 20px`
- Color: `#6c757d`
- Icono font size: `4rem`
- Icono color: `[color-principal]`
- Icono opacity: `0.3`

---

## 📱 Responsivo

### Breakpoint Mobile (max-width: 768px)

```css
@media (max-width: 768px) {
    /* Cards */
    .[tipo]-list-card {
        font-size: 0.9rem;
    }
    
    /* Botones principales */
    .btn-crear-[tipo] {
        padding: 8px 16px;
        font-size: 0.9rem;
    }
    
    /* Filtros */
    .filtros-container {
        padding: 12px;
    }
}
```

---

## ✨ Animaciones

### Fade In (Filas de tabla)
```css
@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.[tipo]-list-card tbody tr {
    animation: fadeIn 0.3s ease;
}
```

---

## 🎨 Iconos Bootstrap Icons

### Requerimientos
- Lista: `bi-list-task`
- Nombre: `bi-file-earmark-text`
- Tipo: `bi-tag`
- Estado: `bi-flag`
- Descripción: `bi-card-text`
- Fecha: `bi-calendar`
- Relación: `bi-link-45deg`
- Acciones: `bi-gear`
- Ver: `bi-eye`
- Crear: `bi-plus-circle-fill`
- Huérfano: `bi-exclamation-triangle`

### Casos de Uso
- Lista: `bi-diagram-3`
- ID: `bi-hash`
- Tipo Tradicional: `bi-book`
- Tipo Ágil: `bi-lightning`
- Detalles: `bi-eye` / `bi-chevron-down`
- Vacío: `bi-inbox`

---

## 📦 Archivos CSS

### Requerimientos
**Ubicación:** `/requerimientos/static/requerimientos/css/requerimiento_list_styles.css`

**Carga en template:**
```django
{% block extra_css %}
  <link rel="stylesheet" href="{% static 'requerimientos/css/requerimiento_list_styles.css' %}?v=1.0">
{% endblock %}
```

### Casos de Uso
**Ubicación:** `/casos_de_uso/static/casos_de_uso/css/casos_de_uso_styles.css`

**Carga en template:**
```django
{% block extra_css %}
  <link rel="stylesheet" href="{% static 'casos_de_uso/css/casos_de_uso_styles.css' %}?v=1.0">
{% endblock %}
```

---

## 🎯 Checklist de Coherencia

Al crear nuevos listados, verificar:

- [ ] Header con gradiente del color institucional
- [ ] Botón "Crear" con gradiente y hover animado
- [ ] Card con borde del color institucional (1.5px)
- [ ] Tabla con header gradiente y uppercase
- [ ] Filas con hover effect (transform y background)
- [ ] Botones de acción con clases `.btn-action-[tipo]`
- [ ] Badges con gradientes coherentes
- [ ] Empty state con icono grande y opacidad 0.3
- [ ] Animación fadeIn en las filas
- [ ] Filtros en contenedor con fondo gris claro
- [ ] Iconos Bootstrap en todos los headers de columna
- [ ] Responsivo para mobile (media query 768px)

---

## 🚀 Próximas Implementaciones

Para mantener la coherencia en futuros módulos:

1. **Proyectos**: Color institucional `#FFC107` (Amarillo)
2. **Usuarios**: Color institucional `#6C757D` (Gris)
3. **Grupos**: Color institucional `#6F42C1` (Morado)
4. **Dashboard**: Usar colores mixtos con las cards respectivas

---

**Fecha de creación:** 19 de octubre de 2025
**Versión:** 1.0
**Autor:** Sistema GRCU Manager
