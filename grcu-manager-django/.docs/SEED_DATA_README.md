# 📋 Datos de Prueba Cargados - GRCU Manager

## ✅ Resumen de Carga

Se han cargado **20 requerimientos** en el proyecto **"GRCU Manager - Sistema de Gestión de Requerimientos"** con metodología **TRADICIONAL**.

---

## 🎯 Proyecto Creado

- **Nombre**: GRCU Manager - Sistema de Gestión de Requerimientos
- **Descripción**: Sistema web para gestionar requerimientos y casos de uso de proyectos de software
- **Metodología**: Tradicional (MoSCoW)
- **ID**: 24
- **Estado**: Activo

---

## 📊 Estadísticas de Requerimientos

### Por Tipo
- **Funcionales**: 15 (75%)
- **No Funcionales**: 5 (25%)

### Por Estado
- **Aprobado**: 9 (45%)
- **En Desarrollo**: 6 (30%)
- **Pendiente**: 5 (25%)

### Por Prioridad MoSCoW
- **MUST have** (Crítico): 12 (60%)
- **SHOULD have** (Importante): 6 (30%)
- **COULD have** (Deseable): 2 (10%)
- **WON'T have** (Fuera de alcance): 0 (0%)

---

## 📝 Requerimientos Cargados

### 🔐 Gestión de Usuarios (5)

1. **Autenticación de usuarios** [MUST] - APROBADO
   - Categoría: Seguridad
   - Estado de Validación: VALIDADO

2. **Registro de nuevos usuarios** [MUST] - EN DESARROLLO
   - Categoría: Gestión de Usuarios
   - Estado de Validación: EN REVISIÓN

3. **Gestión de roles y permisos** [MUST] - APROBADO
   - Categoría: Seguridad
   - Estado de Validación: VALIDADO

4. **Recuperación de contraseña** [SHOULD] - PENDIENTE
   - Categoría: Seguridad
   - Estado de Validación: PENDIENTE

5. **Perfil de usuario** [SHOULD] - EN DESARROLLO
   - Categoría: Gestión de Usuarios
   - Estado de Validación: EN REVISIÓN

### 📁 Gestión de Proyectos (5)

6. **Crear proyecto** [MUST] - APROBADO
   - Categoría: Gestión de Proyectos
   - Estado de Validación: VALIDADO

7. **Editar proyecto** [MUST] - APROBADO
   - Categoría: Gestión de Proyectos
   - Estado de Validación: VALIDADO

8. **Asignar participantes al proyecto** [MUST] - EN DESARROLLO
   - Categoría: Gestión de Proyectos
   - Estado de Validación: EN REVISIÓN

9. **Dashboard del proyecto** [SHOULD] - EN DESARROLLO
   - Categoría: Visualización
   - Estado de Validación: EN REVISIÓN

10. **Archivo de proyectos** [COULD] - PENDIENTE
    - Categoría: Gestión de Proyectos
    - Estado de Validación: PENDIENTE

### 📋 Gestión de Requerimientos (5)

11. **Crear requerimiento funcional** [MUST] - APROBADO
    - Categoría: Gestión de Requerimientos
    - Estado de Validación: VALIDADO

12. **Priorización MoSCoW** [MUST] - APROBADO
    - Categoría: Gestión de Requerimientos
    - Estado de Validación: VALIDADO

13. **Trazabilidad requerimiento-caso de uso** [MUST] - EN DESARROLLO
    - Categoría: Trazabilidad
    - Estado de Validación: EN REVISIÓN

14. **Historial de cambios de requerimientos** [SHOULD] - PENDIENTE
    - Categoría: Auditoría
    - Estado de Validación: PENDIENTE

15. **Exportar requerimientos a PDF** [COULD] - PENDIENTE
    - Categoría: Reportes
    - Estado de Validación: PENDIENTE

### ⚙️ Requerimientos No Funcionales (5)

16. **Tiempo de respuesta** [MUST] - APROBADO
    - Categoría: Performance
    - Descripción: El sistema debe responder en menos de 2 segundos

17. **Compatibilidad con navegadores** [MUST] - APROBADO
    - Categoría: Compatibilidad
    - Descripción: Chrome, Firefox, Safari, Edge (últimas 2 versiones)

18. **Diseño responsive** [SHOULD] - EN DESARROLLO
    - Categoría: Usabilidad
    - Descripción: Adaptación a móviles, tablets y escritorio

19. **Seguridad de datos** [MUST] - APROBADO
    - Categoría: Seguridad
    - Descripción: Encriptación en tránsito y en reposo

20. **Disponibilidad del sistema** [SHOULD] - PENDIENTE
    - Categoría: Disponibilidad
    - Descripción: 99.5% de disponibilidad mensual

---

## ✅ Validación de Integridad

- ✓ **20/20** requerimientos tienen detalles completos
- ✓ **Sin datos huérfanos**
- ✓ Todas las relaciones OneToOne son **consistentes**
- ✓ Fechas de compromiso asignadas para todos
- ✓ Fuentes y categorías definidas
- ✓ Estados de validación coherentes

---

## 🚀 Cómo Usar los Datos

### 1. Acceder al Sistema
```bash
python manage.py runserver
```

### 2. Login
- Usa las credenciales del superusuario
- El líder del proyecto está asignado automáticamente

### 3. Ver Requerimientos
- Ir al **Dashboard del Líder**
- Seleccionar el proyecto "GRCU Manager"
- Click en **"Ver Requerimientos"**

### 4. Funcionalidades Disponibles
- ✅ Listar todos los requerimientos
- ✅ Ver detalle de cada requerimiento
- ✅ Crear nuevos requerimientos
- ✅ Editar requerimientos existentes
- ✅ Priorizar usando MoSCoW
- ✅ Filtrar por tipo y estado

---

## 🔄 Recargar Datos

### Metodología Tradicional
```bash
.scripts/manage_seed.sh TRADICIONAL
```

o

```bash
python manage.py seed_requerimientos --metodologia TRADICIONAL
```

### Metodología Ágil
```bash
.scripts/manage_seed.sh AGIL
```

o

```bash
python manage.py seed_requerimientos --metodologia AGIL
```

### Con Proyecto Específico
```bash
python manage.py seed_requerimientos --proyecto-id 24 --metodologia TRADICIONAL
```

---

## 📌 Próximos Pasos

1. ✅ **Requerimientos cargados** - Completado
2. ⏳ **Crear casos de uso** - Por hacer
3. ⏳ **Vincular requerimientos con casos de uso** - Por hacer
4. ⏳ **Generar matriz de trazabilidad** - Por hacer
5. ⏳ **Exportar a PDF** - Por hacer

---

## 📚 Estructura de Datos

### Requerimiento
- nombre
- descripcion
- tipo (FUNCIONAL/NO_FUNCIONAL)
- estado (PENDIENTE/EN_DESARROLLO/APROBADO)
- proyecto (FK)
- creado_por (FK)

### DetalleRequerimientoTradicional
- requerimiento_padre (OneToOne)
- prioridad (MUST/SHOULD/COULD/WONT)
- fuente
- categoria
- fecha_compromiso
- estado_validacion
- observaciones

---

## 🎓 Método MoSCoW

- **MUST have**: Requisitos críticos, sin los cuales el sistema no funciona
- **SHOULD have**: Requisitos importantes pero no vitales
- **COULD have**: Requisitos deseables pero prescindibles
- **WON'T have**: Requisitos fuera del alcance actual

---

**Generado automáticamente por el sistema de seed**  
Fecha: 19 de octubre de 2025
