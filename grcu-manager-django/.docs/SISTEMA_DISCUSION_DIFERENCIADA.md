# Sistema de Discusión Diferenciada para Requerimientos

## 📋 Descripción General

Se ha implementado un sistema de discusión diferenciada que permite tres tipos de conversaciones en los requerimientos:

### 1. **DISCUSION_INTERNA** 🔵
- **Visibilidad**: Solo líder y desarrolladores
- **Quién puede comentar**: Líder y desarrolladores
- **Propósito**: Coordinar implementación técnica, resolver dudas del equipo
- **Uso**: Discusiones técnicas internas sin involucrar al cliente

### 2. **VALIDACION_CLIENTE** 🟢
- **Visibilidad**: Todos (líder, desarrolladores, cliente)
- **Quién puede comentar**: Solo líder y cliente
- **Propósito**: Negociar y validar requerimientos con el cliente
- **Uso**: Los desarrolladores pueden ver la conversación pero no intervenir
- **Nota**: Los desarrolladores observan pero no comentan para evitar confusión

### 3. **IMPLEMENTACION** 🔵
- **Visibilidad**: Líder y desarrolladores
- **Quién puede comentar**: Líder y desarrolladores
- **Propósito**: Discusión post-validación sobre la implementación
- **Uso**: Después de que el cliente valida, se discute cómo implementar

---

## 🏗️ Cambios Implementados

### 1. Modelo `ComentarioValidacion`

**Archivo**: `requerimientos/models.py`

```python
TIPO_COMENTARIO_CHOICES = [
    ("DISCUSION_INTERNA", "Discusión Interna"),
    ("VALIDACION_CLIENTE", "Validación con Cliente"),
    ("IMPLEMENTACION", "Implementación"),
]

tipo_comentario = models.CharField(
    max_length=20,
    choices=TIPO_COMENTARIO_CHOICES,
    default="DISCUSION_INTERNA",
    help_text="Tipo de comentario: interno del equipo, con cliente, o implementación"
)
```

**Migración aplicada**: `0012_agregar_tipo_comentario.py`

---

### 2. Vista `requerimiento_discusion`

**Archivo**: `requerimientos/views.py`

#### Permisos implementados:
```python
# Determinar roles del usuario
es_lider = usuario == proyecto.lider
es_participante = proyecto.participantes.filter(pk=usuario.pk).exists()
es_stakeholder = proyecto.stakeholders.filter(pk=usuario.pk).exists()

# Validación de permisos por tipo de comentario
if tipo_comentario_seleccionado == 'DISCUSION_INTERNA':
    puede_comentar = es_lider or es_participante
elif tipo_comentario_seleccionado == 'VALIDACION_CLIENTE':
    puede_comentar = es_lider or es_stakeholder
elif tipo_comentario_seleccionado == 'IMPLEMENTACION':
    puede_comentar = es_lider or es_participante
```

#### Filtrado de comentarios por visibilidad:
```python
# Filtrar comentarios según tipo y rol
comentarios_visibles = []

if es_lider or es_participante:
    # Líder y devs ven DISCUSION_INTERNA, VALIDACION_CLIENTE, IMPLEMENTACION
    for comentario in todos_comentarios:
        if comentario.tipo_comentario in ['DISCUSION_INTERNA', 'VALIDACION_CLIENTE', 'IMPLEMENTACION']:
            comentarios_visibles.append(comentario)
elif es_stakeholder:
    # Cliente solo ve VALIDACION_CLIENTE
    for comentario in todos_comentarios:
        if comentario.tipo_comentario == 'VALIDACION_CLIENTE':
            comentarios_visibles.append(comentario)
```

---

### 3. Template `requerimiento_discusion.html`

**Archivo**: `requerimientos/templates/requerimientos/requerimiento_discusion.html`

#### Selector de tipo de comentario:
- Cards interactivos para seleccionar tipo de discusión
- Descripción clara de cada tipo
- Validación JavaScript antes de enviar
- Hereda tipo del comentario padre en respuestas

#### Badges de identificación:
```html
<!-- Badge del tipo de comentario -->
{% if hilo.tipo_comentario == 'DISCUSION_INTERNA' %}
    <span class="badge bg-primary ms-1">
        <i class="bi bi-people"></i> Interna
    </span>
{% elif hilo.tipo_comentario == 'VALIDACION_CLIENTE' %}
    <span class="badge bg-success ms-1">
        <i class="bi bi-chat-square-quote"></i> Cliente
    </span>
{% elif hilo.tipo_comentario == 'IMPLEMENTACION' %}
    <span class="badge bg-info ms-1">
        <i class="bi bi-code-slash"></i> Implementación
    </span>
{% endif %}
```

#### Variables de contexto adicionales:
```python
context = {
    'es_lider': es_lider,
    'es_participante': es_participante,
    'es_stakeholder': es_stakeholder,
    'puede_comentar_interno': es_lider or es_participante,
    'puede_comentar_cliente': es_lider or es_stakeholder,
}
```

---

### 4. Estilos CSS

**Archivo**: `requerimientos/static/requerimientos/css/discusion_styles.css`

```css
/* Tarjetas interactivas de tipo de comentario */
.tipo-comentario-card {
    cursor: pointer;
    transition: all 0.3s ease;
    border: 2px solid transparent;
}

.tipo-comentario-card:hover {
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    transform: translateY(-2px);
}

.tipo-comentario-card.selected {
    border-color: #007bff;
    background-color: #f0f8ff;
}
```

---

### 5. JavaScript

**Funcionalidades**:
- ✅ Auto-expansión de textareas
- ✅ Selección visual de tipo de comentario (cards interactivos)
- ✅ Validación antes de enviar (requiere tipo seleccionado)
- ✅ Heredar tipo en respuestas automáticamente

---

## 🔄 Flujo de Trabajo

### Escenario 1: Líder comenta con cliente
1. Líder crea requerimiento (estado: BORRADOR)
2. Líder selecciona **VALIDACION_CLIENTE** y comenta
3. Cliente ve el comentario y responde
4. Desarrolladores ven toda la conversación (no comentan)
5. Se negocia hasta llegar a acuerdo
6. Líder marca requerimiento como VALIDADO

### Escenario 2: Equipo discute implementación
1. Desarrollador tiene duda técnica
2. Selecciona **DISCUSION_INTERNA** y pregunta
3. Solo el equipo (líder + devs) ve esta conversación
4. Cliente NO ve estas discusiones técnicas
5. Se resuelve internamente

### Escenario 3: Post-validación
1. Requerimiento VALIDADO
2. Se usa **IMPLEMENTACION** para discutir cómo codificar
3. Solo líder y desarrolladores participan
4. Cliente no ve estas discusiones técnicas

---

## 🎯 Próximos Pasos Sugeridos

### Pendiente por implementar:

1. **Dashboard del Cliente** 📊
   - Vista exclusiva para stakeholders/clientes
   - Lista de requerimientos pendientes de validación
   - Solo muestra comentarios tipo VALIDACION_CLIENTE
   - Botones de Validar/Rechazar requerimiento

2. **Notificaciones** 🔔
   - Email cuando cliente recibe comentario de validación
   - Notificación a líder cuando cliente responde
   - Alertas para desarrolladores en discusiones internas

3. **Transiciones de Estado** 🔄
   - BORRADOR → DISCUSION_INTERNA (equipo revisa)
   - BORRADOR → VALIDACION_CLIENTE (enviar a cliente)
   - VALIDADO → IMPLEMENTACION (iniciar desarrollo)

4. **Filtros en Lista de Requerimientos** 🔍
   - Filtrar por tipo de discusión activa
   - Ver requerimientos pendientes de validación cliente
   - Ver requerimientos con discusiones internas abiertas

5. **Estadísticas** 📈
   - Tiempo promedio de validación con cliente
   - Número de comentarios por tipo
   - Requerimientos bloqueados por discusión

---

## ✅ Testing Recomendado

### Casos de prueba:

1. **Líder comenta tipo VALIDACION_CLIENTE**
   - ✅ Líder puede crear comentario
   - ✅ Cliente ve el comentario
   - ✅ Desarrollador ve pero no puede comentar
   - ✅ Badge verde se muestra correctamente

2. **Desarrollador comenta tipo DISCUSION_INTERNA**
   - ✅ Desarrollador puede crear comentario
   - ✅ Líder ve el comentario
   - ✅ Cliente NO ve el comentario
   - ✅ Badge azul se muestra correctamente

3. **Cliente intenta comentar DISCUSION_INTERNA**
   - ✅ No ve la opción en el selector
   - ✅ Solo ve opción VALIDACION_CLIENTE
   - ✅ Mensaje de error si intenta bypass

4. **Respuestas heredan tipo del padre**
   - ✅ Respuesta a VALIDACION_CLIENTE es VALIDACION_CLIENTE
   - ✅ Respuesta a DISCUSION_INTERNA es DISCUSION_INTERNA
   - ✅ No se puede cambiar tipo en respuestas

---

## 🐛 Problemas Resueltos

### Bug #1: QuerySet convertido a lista
**Problema**: Al filtrar comentarios por visibilidad, se convertía QuerySet a lista, rompiendo `.filter()` downstream.

**Solución**: 
- Usar list comprehensions para filtrar
- Cambiar `.count()` por `len()`
- Cambiar `.filter()` por list comprehensions

**Código antes**:
```python
comentarios = ComentarioValidacion.objects.filter(...)
comentarios_visibles = [...]  # Convertido a lista
comentarios_raiz = comentarios.filter(...)  # ❌ Error
```

**Código después**:
```python
comentarios_visibles = [...]  # Lista filtrada
comentarios_raiz = [c for c in comentarios if c.comentario_padre is None]  # ✅ OK
```

---

## 📚 Referencias

- Modelo: `requerimientos/models.py` línea 155-165
- Vista: `requerimientos/views.py` línea 1179-1350
- Template: `requerimientos/templates/requerimientos/requerimiento_discusion.html`
- Estilos: `requerimientos/static/requerimientos/css/discusion_styles.css`
- Migración: `requerimientos/migrations/0012_agregar_tipo_comentario.py`

---

**Fecha de implementación**: 2025
**Desarrollado por**: GitHub Copilot
**Estado**: ✅ Implementado y funcional
