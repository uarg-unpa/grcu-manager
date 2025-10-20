# 🔗 Matriz de Trazabilidad - Documentación Completa

## 📋 Descripción General

La **Matriz de Trazabilidad** es una herramienta fundamental para la gestión de requerimientos que permite visualizar y analizar las relaciones entre **Requerimientos** y **Casos de Uso** de un proyecto en tiempo real.

### ✨ Características Principales

#### 🎯 Live Traceability
- **Actualización en tiempo real**: La matriz refleja el estado actual de todos los requerimientos y casos de uso
- **Indicadores visuales**: Codificación por colores según estado y tipo
- **Métricas dinámicas**: Cálculo automático de coberturas y elementos huérfanos

#### �� Visualización Avanzada
- **Tabla interactiva**: Scroll horizontal y vertical con headers fijos
- **Heat map de cobertura**: Identificación rápida de relaciones
- **Badges informativos**: Estado, tipo y prioridad de cada elemento
- **Tooltips**: Información adicional al pasar el mouse

#### 🔍 Filtros Dinámicos
- **Por tipo**: Funcional / No Funcional
- **Por estado**: Pendiente / En Progreso / Completado
- **Huérfanos**: Solo elementos sin relaciones
- **Sin cubrir**: Solo casos de uso sin requerimientos

#### 📤 Herramientas de Exportación
- **CSV**: Para análisis en hojas de cálculo
- **Excel**: Con formato y estilos (requiere `openpyxl`)
- **PDF**: Para reportes formales (requiere `reportlab`)

---

## 🏗️ Arquitectura

### Responsabilidad por App

```
proyectos/
├── views.py
│   ├── matriz_trazabilidad()    ← Vista principal
│   └── exportar_matriz()         ← Exportación en múltiples formatos
├── urls.py
│   ├── <proyecto_id>/matriz/
│   └── <proyecto_id>/matriz/exportar/<formato>/
└── templates/
    └── proyectos/
        └── matriz_trazabilidad.html

dashboards/
└── views.py
    └── lider_matriz()            ← Redirige a proyectos
```

### Flujo de Datos

```
Usuario → Dashboard → Redirige a → Proyectos/Matriz
                                         ↓
                                  Calcula métricas
                                         ↓
                                  Construye matriz
                                         ↓
                                  Renderiza template
```

---

## 📊 Métricas Calculadas

### 1. Totales
- **Total de Requerimientos**: Cuenta todos los requerimientos del proyecto
- **Total de Casos de Uso**: Cuenta todos los casos del proyecto
- **Total de Relaciones**: Cuenta vínculos en `RequerimientoCaso`

### 2. Coberturas
- **Cobertura de Requerimientos**: % de requerimientos con al menos un caso de uso
- **Cobertura de Casos**: % de casos de uso con al menos un requerimiento

### 3. Análisis por Categoría
- **Por Estado**: Distribución (Pendiente/En Progreso/Completado)
- **Por Tipo**: Distribución (Funcional/No Funcional)

### 4. Identificación de Gaps
- **Requerimientos Huérfanos**: Sin casos de uso asociados
- **Casos Huérfanos**: Sin requerimientos asociados

---

## 🎨 Interfaz de Usuario

### Estructura Visual

```
╔═══════════════════════════════════════════════════════════╗
║  Matriz de Trazabilidad - [Nombre del Proyecto]         ║
║  [Exportar ▼] [Gestionar Requerimientos]                ║
╠═══════════════════════════════════════════════════════════╣
║  MÉTRICAS (6 Cards)                                      ║
║  • Total Reqs    • Total CUs    • Cobertura Reqs        ║
║  • Cobertura CUs • Huérfanos R  • Huérfanos CU          ║
╠═══════════════════════════════════════════════════════════╣
║  FILTROS                                                 ║
║  [Tipo ▼] [Estado ▼] [☐ Huérfanos] [☐ Sin cubrir]     ║
╠═══════════════════════════════════════════════════════════╣
║  TABLA DE MATRIZ                                         ║
║  ┌─────────────┬──────┬────────┬───┬───┬───┬───┐      ║
║  │ Requerimiento│ Tipo │ Estado │CU1│CU2│CU3│...│      ║
║  ├─────────────┼──────┼────────┼───┼───┼───┼───┤      ║
║  │ REQ-1: ...  │ Func │ Pend.  │ ✓ │ - │ ✓ │   │      ║
║  │ REQ-2: ...  │ NoF  │ Prog.  │ - │ ✓ │ - │   │      ║
║  └─────────────┴──────┴────────┴───┴───┴───┴───┘      ║
╚═══════════════════════════════════════════════════════════╝
```

### Codificación de Colores

#### Estados
- 🟨 **Pendiente**: Amarillo (`#fff3cd`)
- 🟦 **En Progreso**: Azul (`#cfe2ff`)
- 🟩 **Completado**: Verde (`#d1e7dd`)

#### Tipos
- 🔵 **Funcional**: Azul claro (`#e3f2fd`)
- 🔴 **No Funcional**: Rosa (`#fce4ec`)

#### Relaciones
- ✅ **Relacionado**: Verde (`#d5f4e6`) con ✓
- ⬜ **No Relacionado**: Gris (`#fef5f5`) con -

---

## 🔐 Control de Acceso

### Permisos

```python
# Pueden acceder:
- Líder del proyecto
- Participantes del proyecto

# Validación en la vista:
es_lider = proyecto.lider == request.user
es_participante = proyecto.participantes.filter(id=request.user.id).exists()

if not (es_lider or es_participante):
    messages.error(request, "No tienes permiso...")
    return redirect(...)
```

### Acciones Permitidas

| Rol           | Ver Matriz | Exportar | Filtrar | Gestionar Reqs |
|---------------|------------|----------|---------|----------------|
| Líder         | ✅         | ✅       | ✅      | ✅             |
| Participante  | ✅         | ✅       | ✅      | ❌             |
| Otros         | ❌         | ❌       | ❌      | ❌             |

---

## 📤 Formatos de Exportación

### 1. CSV
```python
# Formato:
Requerimiento, Tipo, Estado, CU-1, CU-2, ...
REQ-1: Login, Funcional, Completado, ✓, -, ...
```

**Características**:
- ✅ No requiere dependencias adicionales
- ✅ Compatible con Excel y Google Sheets
- ✅ Encoding UTF-8 con BOM
- ✅ Tamaño ligero

### 2. Excel (.xlsx)
```python
# Requiere: pip install openpyxl

# Características:
- Headers con fondo azul
- Checkmarks con fondo verde
- Anchos de columna ajustados
- Alineación centrada
```

**Ventajas**:
- ✨ Formato profesional
- ✨ Estilos y colores
- ✨ Fácil de compartir

### 3. PDF
```python
# Requiere: pip install reportlab

# Características:
- Orientación horizontal (landscape)
- Tabla con estilos
- Encabezado con título del proyecto
- Formato A4
```

**Ventajas**:
- 📄 Ideal para reportes formales
- 📄 No editable (protección)
- 📄 Presentaciones profesionales

---

## 🔧 Optimizaciones Implementadas

### 1. Queries Eficientes
```python
# Prefetch para evitar N+1 queries
requerimientos = requerimientos_qs.prefetch_related(
    Prefetch('relaciones_casos',
            queryset=RequerimientoCaso.objects.select_related('caso_de_uso'))
)

casos = CasoDeUso.objects.filter(proyecto=proyecto).prefetch_related(
    Prefetch('relaciones_requerimientos',
            queryset=RequerimientoCaso.objects.select_related('requerimiento'))
)
```

### 2. Anotaciones para Conteo
```python
# Evita queries repetitivas
requerimientos.annotate(rel_count=Count('relaciones_casos'))
```

### 3. Cálculo en Python
```python
# Métricas calculadas una sola vez
cobertura_reqs = (reqs_con_casos / total_requerimientos * 100) if total_requerimientos > 0 else 0
```

---

## 🚀 Uso

### Acceder a la Matriz

#### Opción 1: Desde el Dashboard del Líder
```
Dashboard Líder → Card del Proyecto → "Ver Matriz de Trazabilidad"
```

#### Opción 2: URL Directa
```
/proyectos/<proyecto_id>/matriz/
```

#### Opción 3: Desde el Menú del Proyecto
```
Gestión de Proyecto → Matriz de Trazabilidad
```

### Aplicar Filtros

1. **Seleccionar filtros** en el panel superior
2. Los filtros se aplican automáticamente (auto-submit)
3. La URL se actualiza con los parámetros GET

Ejemplo:
```
/proyectos/19/matriz/?tipo_req=FUNCIONAL&estado_req=COMPLETADO
```

### Exportar Matriz

1. Click en **"Exportar"**
2. Seleccionar formato (CSV/Excel/PDF)
3. El archivo se descarga automáticamente

---

## 📦 Dependencias Opcionales

### Para Exportación Excel
```bash
pip install openpyxl
```

### Para Exportación PDF
```bash
pip install reportlab
```

> ⚠️ Si no están instaladas, se mostrará un mensaje de error y se sugerirá usar CSV.

---

## 🎯 Casos de Uso

### 1. Auditoría de Cobertura
**Objetivo**: Verificar que todos los requerimientos tienen casos de uso

**Pasos**:
1. Acceder a la matriz
2. Observar la métrica "Cobertura de Requerimientos"
3. Si < 100%, ver "Requerimientos Huérfanos"
4. Activar filtro "Solo huérfanos"
5. Asignar casos de uso a los huérfanos

### 2. Análisis de Completitud
**Objetivo**: Identificar qué casos no están respaldados por requerimientos

**Pasos**:
1. Observar "Casos Huérfanos"
2. Activar "Solo sin cubrir"
3. Revisar casos huérfanos
4. Crear requerimientos faltantes o eliminar casos innecesarios

### 3. Reportes para Stakeholders
**Objetivo**: Generar reporte visual del estado del proyecto

**Pasos**:
1. Aplicar filtros según necesidad
2. Exportar a PDF
3. Adjuntar a email o presentación
4. Las métricas se reflejan automáticamente

### 4. Seguimiento de Progreso
**Objetivo**: Ver evolución de requerimientos completados

**Pasos**:
1. Filtrar por "Estado: Completado"
2. Ver cobertura actual
3. Comparar con sprints anteriores
4. Exportar para registro histórico

---

## 🐛 Solución de Problemas

### Problema: "No tienes proyectos asignados como líder"
**Solución**: Contactar al administrador para ser asignado como líder de un proyecto.

### Problema: Matriz vacía
**Causas posibles**:
1. El proyecto no tiene requerimientos cargados
2. Filtros muy restrictivos
3. No hay casos de uso

**Solución**:
- Cargar requerimientos desde "Gestionar Requerimientos"
- Quitar filtros
- Crear casos de uso

### Problema: Error al exportar Excel/PDF
**Causa**: Dependencias no instaladas

**Solución**:
```bash
# Para Excel
pip install openpyxl

# Para PDF
pip install reportlab
```

### Problema: La tabla se ve cortada en móvil
**Solución**: Hacer scroll horizontal en la tabla. La interfaz es responsive pero la matriz requiere espacio horizontal.

---

## 🔮 Mejoras Futuras

### v2.0 - Edición en Línea
- ✏️ Vincular/desvincular requerimientos y casos directamente desde la matriz
- 🔄 Drag & drop para crear relaciones
- ⚡ Actualización AJAX sin recargar

### v3.0 - Análisis Avanzado
- 📊 Gráficos de tendencias
- 🎯 Análisis de impacto de cambios
- 🔍 Búsqueda de requerimientos en la matriz
- 📈 Comparación entre sprints

### v4.0 - Inteligencia Artificial
- 🤖 Sugerencias automáticas de relaciones
- 🧠 Detección de inconsistencias
- 📝 Generación automática de reportes con insights

---

## 📚 Referencias

### Modelos Relacionados
- `proyectos.models.Proyecto`
- `requerimientos.models.Requerimiento`
- `requerimientos.models.RequerimientoCaso` (tabla intermedia)
- `casos_de_uso.models.CasoDeUso`

### Vistas Relacionadas
- `proyectos.views.matriz_trazabilidad`
- `proyectos.views.exportar_matriz`
- `dashboards.views.lider_dashboard`

### URLs
```python
# En proyectos/urls.py
path("<int:proyecto_id>/matriz/", views.matriz_trazabilidad, name="matriz_trazabilidad")
path("<int:proyecto_id>/matriz/exportar/<str:formato>/", views.exportar_matriz, name="exportar_matriz")
```

---

## ✅ Checklist de Implementación

- [x] Vista de matriz en `proyectos/views.py`
- [x] Template con diseño responsive
- [x] Filtros dinámicos con auto-submit
- [x] Cálculo de métricas en tiempo real
- [x] Exportación a CSV
- [x] Exportación a Excel (con openpyxl)
- [x] Exportación a PDF (con reportlab)
- [x] Control de acceso (líder/participante)
- [x] Redirección desde dashboard
- [x] Optimización de queries (prefetch)
- [x] Documentación completa
- [x] Tooltips informativos
- [x] Headers fijos en scroll
- [x] Codificación de colores
- [x] Empty states para datos vacíos

---

## 🎉 Conclusión

La Matriz de Trazabilidad es una herramienta completa y profesional que permite:

✅ **Visualizar** relaciones entre requerimientos y casos de uso
✅ **Analizar** cobertura y completitud del proyecto
✅ **Identificar** gaps y elementos huérfanos
✅ **Exportar** reportes en múltiples formatos
✅ **Filtrar** datos según necesidades específicas
✅ **Compartir** información con stakeholders

---

**Desarrollado para GRCU Manager** | Versión 1.0 | Octubre 2025
