# 🧹 Migración y Limpieza de Base de Datos

**Fecha:** 23 de octubre de 2025  
**Estado:** ✅ COMPLETADO

---

## 📋 Resumen de Cambios

### ❌ **Tablas Eliminadas**

#### 1. `usuarios_accionusuario` 
- **Razón:** Funcionalidad duplicada con `auditoria_registroactividad`
- **Estado anterior:** 0 registros (vacía)
- **Acción:** Eliminada mediante migración `usuarios/0002_delete_accionusuario.py`

#### 2. `requerimientos_requerimiento_casos_relacionados`
- **Razón:** Tabla automática duplicada, se usa `requerimientos_requerimientocaso` (through model)
- **Estado anterior:** No existía en la base de datos
- **Acción:** Ya había sido eliminada previamente

---

## 🔧 Cambios en el Código

### **Modelo Eliminado**
```python
# usuarios/models.py - ANTES
class AccionUsuario(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    accion = models.CharField(max_length=255)
    fecha = models.DateTimeField(auto_now_add=True)
```

**AHORA:** Se usa `auditoria.RegistroActividad` que tiene más funcionalidad:
- Campo `accion` con choices (LOGIN, LOGOUT, CREATE, UPDATE, DELETE, etc.)
- Campo `detalles` (JSONField) para metadata
- Campos `ip_address` y `user_agent` para auditoría completa
- Índices optimizados para queries

---

### **Archivos Actualizados**

#### 1. `usuarios/models.py`
```python
# Modelo AccionUsuario eliminado
# Agregado comentario explicativo
```

#### 2. `usuarios/forms.py`
```python
# ANTES:
from .models import Usuario

# AHORA:
from accounts.models import Usuario
```

#### 3. `proyectos/views.py`
```python
# ANTES:
from usuarios.models import AccionUsuario
acciones = AccionUsuario.objects.filter(...)

# AHORA:
from auditoria.models import RegistroActividad
acciones = RegistroActividad.objects.filter(...)
```

#### 4. `dashboards/views.py`
```python
# ANTES:
from usuarios.models import AccionUsuario
acciones = AccionUsuario.objects.filter(...)

# AHORA:
from auditoria.models import RegistroActividad
acciones = RegistroActividad.objects.filter(...)
```

#### 5. `usuarios/tests/test_usuario.py`
```python
# ANTES:
from usuarios.models import AccionUsuario
accion = AccionUsuario.objects.create(usuario=user, accion='login')

# AHORA:
from auditoria.models import RegistroActividad
registro = RegistroActividad.objects.create(
    usuario=user, 
    accion='LOGIN', 
    descripcion='Usuario inició sesión'
)
```

---

## 📊 Estado Final de la Base de Datos

### **Total de Tablas:** 29 (antes: 30)

```
✅ accounts_usuario
✅ accounts_usuario_groups
✅ accounts_usuario_roles
✅ accounts_usuario_user_permissions
✅ auditoria_registroactividad
✅ auth_group
✅ auth_group_permissions
✅ auth_permission
✅ casos_de_uso_casodeuso
✅ casos_de_uso_detallecasodeusoagil
✅ casos_de_uso_detallecasodeusotradicional
✅ casos_de_uso_historicalcasodeuso
✅ django_admin_log
✅ django_content_type
✅ django_migrations
✅ django_session
✅ grupos_grupo
✅ grupos_grupo_integrantes
✅ permisos_permiso
✅ proyectos_historicalproyecto
✅ proyectos_participacionproyecto
✅ proyectos_proyecto
✅ requerimientos_detallerequerimientoagil
✅ requerimientos_detallerequerimientotradicional
✅ requerimientos_historicalrequerimiento
✅ requerimientos_requerimiento
✅ requerimientos_requerimientocaso
✅ roles_rol
✅ roles_rol_permisos
```

### **Tablas Eliminadas:**
```
❌ usuarios_accionusuario (eliminada)
❌ requerimientos_requerimiento_casos_relacionados (nunca existió en BD)
```

---

## ✅ Verificaciones Realizadas

1. **Migración aplicada correctamente:**
   ```bash
   python manage.py migrate usuarios
   # Applying usuarios.0002_delete_accionusuario... OK
   ```

2. **Sistema sin errores:**
   ```bash
   python manage.py check
   # System check identified no issues (0 silenced)
   ```

3. **Todas las importaciones actualizadas** en:
   - `proyectos/views.py`
   - `dashboards/views.py`
   - `usuarios/tests/test_usuario.py`
   - `usuarios/forms.py`

4. **Diagrama Mermaid actualizado** en `.docs/diagrama_bd_mermaid.txt`

---

## 🎯 Beneficios de la Limpieza

1. ✅ **Menos duplicación:** Un solo sistema de auditoría (`auditoria_registroactividad`)
2. ✅ **Mejor estructura:** Separación clara entre apps (Usuario en `accounts`, no en `usuarios`)
3. ✅ **Código más limpio:** Sin modelos obsoletos o sin usar
4. ✅ **Base de datos optimizada:** Solo 29 tablas necesarias
5. ✅ **Mejor auditoría:** `RegistroActividad` tiene más campos y funcionalidad

---

## 📝 Notas Importantes

### **Sistema Dual de Permisos**
El proyecto mantiene dos sistemas de permisos (esto es normal):
1. **Sistema Django nativo:** `auth_group`, `auth_permission` (para admin panel)
2. **Sistema custom:** `roles_rol`, `permisos_permiso` (para la aplicación)

### **Tabla `requerimientos_requerimientocaso`**
Es la tabla intermedia correcta para la relación M2M entre Requerimiento y CasoDeUso:
```python
casos_relacionados = models.ManyToManyField(
    'casos_de_uso.CasoDeUso', 
    through='RequerimientoCaso',  # ← Usa esta tabla
    blank=True
)
```

---

## 🚀 Próximos Pasos

1. ✅ Migración aplicada
2. ✅ Código actualizado
3. ✅ Tests actualizados
4. ✅ Diagrama Mermaid actualizado
5. ⏭️ Ejecutar tests para validar: `pytest`
6. ⏭️ Verificar dashboards en desarrollo

---

**Migración realizada por:** GitHub Copilot  
**Revisada y aprobada por:** Usuario
