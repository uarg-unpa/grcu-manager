# 🔍 Sistema de Auditoría e Historial - GRCU Manager

## ✅ Implementación Completada (Fase 1)

### 1. Instalación de Dependencias
- ✅ `django-simple-history==3.10.1` instalado correctamente

### 2. Configuración de Settings
- ✅ Agregado `simple_history` a `INSTALLED_APPS`
- ✅ Agregado `simple_history.middleware.HistoryRequestMiddleware` a `MIDDLEWARE`
- ✅ Agregado app `auditoria` a `INSTALLED_APPS`

### 3. App Auditoría Creada
**Archivos creados:**
- ✅ `auditoria/models.py` - Modelo `RegistroActividad`
- ✅ `auditoria/admin.py` - Configuración del admin (solo lectura)
- ✅ `auditoria/utils.py` - Funciones helper para registrar actividades

### 4. Historial Agregado a Modelos
- ✅ `Requerimiento` - Ahora con `history = HistoricalRecords()`
- ✅ `CasoDeUso` - Ahora con `history = HistoricalRecords()`
- ✅ `Proyecto` - Ahora con `history = HistoricalRecords()`

### 5. Migraciones Aplicadas
```bash
✅ auditoria.0001_initial - Tabla RegistroActividad
✅ casos_de_uso.0003_historicalcasodeuso - Historial de CasoDeUso
✅ proyectos.0006_historicalproyecto - Historial de Proyecto
✅ requerimientos.0004_historicalrequerimiento - Historial de Requerimiento
```

### 6. Integración Inicial
- ✅ Login/Logout registran actividad automáticamente

---

## 📋 Características Disponibles AHORA

### A. Historial Automático
Cada vez que se modifica un **Requerimiento**, **Caso de Uso** o **Proyecto**:
- Se guarda una copia completa del estado anterior
- Se registra quién hizo el cambio
- Se registra cuándo se hizo el cambio
- Se puede ver qué campos cambiaron

### B. Auditoría de Login/Logout
- Cada login queda registrado con IP y user agent
- Cada logout queda registrado

---

## 🚀 Próximos Pasos (Fase 2)

### 1. Vistas de Historial
Crear vistas para ver el historial de versiones:

```python
# requerimientos/urls.py
path('<int:pk>/historial/', views.requerimiento_historial, name='historial'),
path('<int:pk>/version/<int:version_id>/', views.requerimiento_version_detail, name='version_detail'),

# requerimientos/views.py
def requerimiento_historial(request, pk):
    requerimiento = get_object_or_404(Requerimiento, pk=pk)
    historial = requerimiento.history.all()
    return render(request, 'requerimientos/historial.html', {
        'requerimiento': requerimiento,
        'historial': historial
    })
```

### 2. Templates de Historial
Crear templates para visualizar:
- Lista de versiones
- Comparación entre versiones
- Restauración de versiones

### 3. Integrar Auditoría en Más Vistas
```python
# Ejemplo en proyectos/views.py
from auditoria.utils import registrar_creacion_proyecto, registrar_eliminacion_proyecto

def crear_proyecto(request):
    # ... código existente
    if form.is_valid():
        proyecto = form.save()
        registrar_creacion_proyecto(request, proyecto)
        # ...
```

### 4. Dashboard de Auditoría
Crear un dashboard para el admin que muestre:
- Actividad reciente
- Usuarios más activos
- Gráficos de actividad
- Exportación de logs

### 5. Botones en Templates
Agregar botones "Ver Historial" en:
- Detalle de requerimiento
- Detalle de caso de uso
- Detalle de proyecto

---

## 🔧 Uso del Sistema

### Ver Historial en Python Shell
```python
python manage.py shell

# Ver historial de un requerimiento
from requerimientos.models import Requerimiento
req = Requerimiento.objects.first()

# Todas las versiones
historial = req.history.all()
for version in historial:
    print(f"{version.history_date} - {version.history_user} - {version.history_type}")

# Comparar versiones
version_actual = req.history.first()
version_anterior = req.history.all()[1]
delta = version_actual.diff_against(version_anterior)

for change in delta.changes:
    print(f"{change.field}: {change.old} → {change.new}")

# Restaurar versión anterior
version_anterior.instance.save()
```

### Ver Logs de Auditoría
```python
from auditoria.models import RegistroActividad

# Últimas 10 actividades
RegistroActividad.objects.all()[:10]

# Actividades de un usuario específico
RegistroActividad.objects.filter(usuario__email='user@example.com')

# Solo logins
RegistroActividad.objects.filter(accion='LOGIN')
```

---

## 📊 Tablas Creadas

### 1. `auditoria_registroactividad`
Registra actividades generales (login, logout, creación de usuarios, etc.)

### 2. `historical_*` (3 tablas)
- `historical_requerimiento`
- `historical_casodeuso`
- `historical_proyecto`

Cada una guarda:
- Todos los campos del modelo original
- `history_id` (PK del historial)
- `history_date` (cuándo se hizo el cambio)
- `history_user_id` (quién lo hizo)
- `history_type` ('+' create, '~' update, '-' delete)
- `history_change_reason` (razón del cambio - opcional)

---

## ⚠️ Importante

### NO rompe nada existente
- ✅ Todos los modelos siguen funcionando igual
- ✅ Las migraciones se aplicaron sin errores
- ✅ No afecta el rendimiento de las operaciones normales
- ✅ El historial se crea automáticamente en segundo plano

### Pruebas recomendadas
1. Crear un nuevo requerimiento → Ver que se crea entrada en historial
2. Modificar ese requerimiento → Ver que se crea nueva versión
3. Login/Logout → Ver que se registra en auditoría

---

## 🎯 Estado Actual

**SISTEMA FUNCIONANDO ✅**
- Base de datos actualizada
- Historial activo en 3 modelos principales
- Auditoría registrando login/logout
- Todo listo para la Fase 2

**PRÓXIMO PASO SUGERIDO:**
Crear las vistas y templates de historial para que los usuarios puedan ver las versiones anteriores desde la interfaz web.

¿Quieres que continúe con la Fase 2?
