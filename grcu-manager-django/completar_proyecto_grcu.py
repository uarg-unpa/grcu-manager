"""
Script para completar el proyecto GRCU con:
- 3 integrantes adicionales
- 1 cliente/stakeholder
- Requerimientos funcionales y no funcionales
- Casos de uso
- Relaciones entre requerimientos y casos de uso
"""

import os
import django
from datetime import datetime, timedelta
from random import choice, sample, randint

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'grcu_manager.settings')
django.setup()

from django.contrib.auth import get_user_model
from proyectos.models import Proyecto, ParticipacionProyecto
from requerimientos.models import Requerimiento
from casos_de_uso.models import CasoDeUso
from roles.models import Rol

Usuario = get_user_model()

def agregar_participantes_grcu():
    """Agrega 3 desarrolladores y 1 cliente al proyecto GRCU"""
    print("\n" + "="*80)
    print("AGREGANDO PARTICIPANTES AL PROYECTO GRCU")
    print("="*80)
    
    try:
        proyecto = Proyecto.objects.get(nombre="GRCU")
    except Proyecto.DoesNotExist:
        print("❌ ERROR: No se encontró el proyecto GRCU")
        return None
    
    # Obtener roles
    rol_dev = Rol.objects.get(nombre="Desarrollador")
    rol_stakeholder = Rol.objects.get(nombre="Stakeholder")
    
    # Obtener usuarios que NO están en el proyecto
    usuarios_en_proyecto = proyecto.participantes.all()
    usuarios_disponibles = Usuario.objects.exclude(id__in=usuarios_en_proyecto.values_list('id', flat=True))
    
    if usuarios_disponibles.count() < 4:
        print("❌ ERROR: No hay suficientes usuarios disponibles")
        return None
    
    # Seleccionar 3 desarrolladores y 1 cliente
    nuevos_devs = sample(list(usuarios_disponibles), 3)
    usuarios_restantes = usuarios_disponibles.exclude(id__in=[u.id for u in nuevos_devs])
    nuevo_cliente = choice(list(usuarios_restantes))
    
    # Agregar desarrolladores
    print("\n📌 Agregando desarrolladores:")
    for dev in nuevos_devs:
        ParticipacionProyecto.objects.get_or_create(
            usuario=dev,
            proyecto=proyecto,
            defaults={'rol': rol_dev}
        )
        print(f"  ✓ {dev.nombre} ({dev.email})")
    
    # Agregar cliente
    print("\n📌 Agregando cliente/stakeholder:")
    ParticipacionProyecto.objects.get_or_create(
        usuario=nuevo_cliente,
        proyecto=proyecto,
        defaults={'rol': rol_stakeholder}
    )
    proyecto.clientes.add(nuevo_cliente)
    print(f"  ✓ {nuevo_cliente.nombre} ({nuevo_cliente.email})")
    
    print(f"\n✅ Total participantes en GRCU: {proyecto.participantes.count()}")
    
    return proyecto

def crear_requerimientos_grcu(proyecto):
    """Crea requerimientos funcionales y no funcionales para GRCU"""
    print("\n" + "="*80)
    print("CREANDO REQUERIMIENTOS PARA GRCU")
    print("="*80)
    
    lider = proyecto.lider
    
    # Requerimientos Funcionales
    reqs_funcionales = [
        {
            'nombre': 'RF-01: Gestión de usuarios y roles',
            'descripcion': 'El sistema debe permitir crear, modificar y eliminar usuarios asignándoles roles específicos (Líder, Desarrollador, Stakeholder).',
        },
        {
            'nombre': 'RF-02: Creación de proyectos',
            'descripcion': 'El sistema debe permitir a los usuarios crear nuevos proyectos especificando nombre, descripción y metodología (Tradicional o Ágil).',
        },
        {
            'nombre': 'RF-03: Asignación de participantes a proyectos',
            'descripcion': 'El sistema debe permitir asignar usuarios a proyectos con roles específicos dentro del mismo.',
        },
        {
            'nombre': 'RF-04: Registro de requerimientos',
            'descripcion': 'El sistema debe permitir registrar requerimientos funcionales y no funcionales con nombre, descripción y estado.',
        },
        {
            'nombre': 'RF-05: Gestión de casos de uso',
            'descripcion': 'El sistema debe permitir crear y gestionar casos de uso asociados a requerimientos funcionales.',
        },
        {
            'nombre': 'RF-06: Versionado de requerimientos',
            'descripcion': 'El sistema debe mantener un historial de versiones de cada requerimiento registrando quién y cuándo realizó cambios.',
        },
        {
            'nombre': 'RF-07: Versionado de casos de uso',
            'descripcion': 'El sistema debe mantener un historial de versiones de cada caso de uso con información de modificaciones.',
        },
        {
            'nombre': 'RF-08: Matriz de trazabilidad',
            'descripcion': 'El sistema debe generar una matriz de trazabilidad mostrando la relación entre requerimientos y casos de uso.',
        },
        {
            'nombre': 'RF-09: Exportación de documentación a PDF',
            'descripcion': 'El sistema debe permitir exportar la documentación del proyecto (requerimientos, casos de uso) en formato PDF.',
        },
        {
            'nombre': 'RF-10: Validación de requerimientos por stakeholder',
            'descripcion': 'El sistema debe permitir que los stakeholders validen o rechacen requerimientos con comentarios.',
        },
        {
            'nombre': 'RF-11: Validación de requerimientos por líder',
            'descripcion': 'El sistema debe permitir que el líder del proyecto valide o rechace requerimientos.',
        },
        {
            'nombre': 'RF-12: Dashboard de estadísticas',
            'descripcion': 'El sistema debe mostrar un dashboard con estadísticas del proyecto (cantidad de requerimientos por estado, etc.).',
        },
        {
            'nombre': 'RF-13: Gestión de dependencias entre requerimientos',
            'descripcion': 'El sistema debe permitir definir dependencias entre requerimientos indicando cuáles dependen de otros.',
        },
        {
            'nombre': 'RF-14: Búsqueda y filtrado de requerimientos',
            'descripcion': 'El sistema debe permitir buscar y filtrar requerimientos por nombre, estado y tipo.',
        },
        {
            'nombre': 'RF-15: Gestión de grupos de trabajo',
            'descripcion': 'El sistema debe permitir crear grupos de trabajo y asignarlos a proyectos específicos.',
        },
    ]
    
    # Requerimientos No Funcionales
    reqs_no_funcionales = [
        {
            'nombre': 'RNF-01: Usabilidad',
            'descripcion': 'La interfaz debe ser intuitiva y fácil de usar, siguiendo principios de diseño UX/UI modernos.',
        },
        {
            'nombre': 'RNF-02: Rendimiento',
            'descripcion': 'El sistema debe cargar las páginas principales en menos de 2 segundos con hasta 100 usuarios concurrentes.',
        },
        {
            'nombre': 'RNF-03: Seguridad',
            'descripcion': 'El sistema debe implementar autenticación segura y protección contra vulnerabilidades comunes (SQL injection, XSS, CSRF).',
        },
        {
            'nombre': 'RNF-04: Compatibilidad',
            'descripcion': 'El sistema debe ser compatible con los navegadores modernos (Chrome, Firefox, Safari, Edge).',
        },
        {
            'nombre': 'RNF-05: Mantenibilidad',
            'descripcion': 'El código debe seguir buenas prácticas de programación y estar documentado para facilitar el mantenimiento.',
        },
    ]
    
    print("\n📋 Creando Requerimientos Funcionales:")
    reqs_creados = []
    for data in reqs_funcionales:
        req, created = Requerimiento.objects.get_or_create(
            proyecto=proyecto,
            nombre=data['nombre'],
            defaults={
                'descripcion': data['descripcion'],
                'tipo': 'FUNCIONAL',
                'estado': 'BORRADOR',
                'creado_por': lider,
            }
        )
        if created:
            print(f"  ✓ {data['nombre']}")
            reqs_creados.append(req)
        else:
            print(f"  → {data['nombre']} (ya existe)")
    
    print("\n📋 Creando Requerimientos No Funcionales:")
    for data in reqs_no_funcionales:
        req, created = Requerimiento.objects.get_or_create(
            proyecto=proyecto,
            nombre=data['nombre'],
            defaults={
                'descripcion': data['descripcion'],
                'tipo': 'NO_FUNCIONAL',
                'estado': 'BORRADOR',
                'creado_por': lider,
            }
        )
        if created:
            print(f"  ✓ {data['nombre']}")
            reqs_creados.append(req)
        else:
            print(f"  → {data['nombre']} (ya existe)")
    
    return reqs_creados

def crear_casos_uso_grcu(proyecto, requerimientos):
    """Crea casos de uso para GRCU"""
    print("\n" + "="*80)
    print("CREANDO CASOS DE USO PARA GRCU")
    print("="*80)
    
    lider = proyecto.lider
    
    casos_uso = [
        {
            'nombre': 'CU-01: Iniciar sesión',
            'descripcion': 'El usuario ingresa sus credenciales para acceder al sistema.',
            'actores': 'Usuario',
            'precondiciones': 'El usuario debe estar registrado en el sistema.',
            'flujo_principal': '1. El usuario ingresa email y contraseña\n2. El sistema valida las credenciales\n3. El sistema muestra el dashboard principal',
            'postcondiciones': 'El usuario accede al sistema autenticado.',
        },
        {
            'nombre': 'CU-02: Crear proyecto',
            'descripcion': 'El usuario crea un nuevo proyecto en el sistema.',
            'actores': 'Líder',
            'precondiciones': 'El usuario debe tener rol de Líder.',
            'flujo_principal': '1. El líder accede a la sección de proyectos\n2. Selecciona "Crear proyecto"\n3. Ingresa nombre, descripción y metodología\n4. El sistema crea el proyecto',
            'postcondiciones': 'El proyecto queda registrado en el sistema.',
        },
        {
            'nombre': 'CU-03: Registrar requerimiento',
            'descripcion': 'El desarrollador registra un nuevo requerimiento.',
            'actores': 'Desarrollador, Líder',
            'precondiciones': 'Debe existir un proyecto activo.',
            'flujo_principal': '1. El usuario accede a la lista de requerimientos\n2. Selecciona "Nuevo requerimiento"\n3. Ingresa nombre, descripción y tipo\n4. El sistema guarda el requerimiento en estado BORRADOR',
            'postcondiciones': 'El requerimiento queda registrado.',
        },
        {
            'nombre': 'CU-04: Validar requerimiento (Stakeholder)',
            'descripcion': 'El stakeholder valida o rechaza un requerimiento.',
            'actores': 'Stakeholder',
            'precondiciones': 'El requerimiento debe estar en estado BORRADOR.',
            'flujo_principal': '1. El stakeholder accede a requerimientos pendientes\n2. Revisa el requerimiento\n3. Valida o rechaza con comentarios\n4. El sistema actualiza el estado',
            'postcondiciones': 'El requerimiento cambia a VALIDADO o permanece en BORRADOR.',
        },
        {
            'nombre': 'CU-05: Validar requerimiento (Líder)',
            'descripcion': 'El líder del proyecto valida requerimientos ya aprobados por stakeholder.',
            'actores': 'Líder',
            'precondiciones': 'El requerimiento debe estar VALIDADO por stakeholder.',
            'flujo_principal': '1. El líder accede a requerimientos validados\n2. Revisa el requerimiento\n3. Aprueba o rechaza\n4. El sistema actualiza el estado a PRIORIZADO',
            'postcondiciones': 'El requerimiento pasa a PRIORIZADO o vuelve a BORRADOR.',
        },
        {
            'nombre': 'CU-06: Crear caso de uso',
            'descripcion': 'El usuario crea un caso de uso asociado a un requerimiento funcional.',
            'actores': 'Desarrollador, Líder',
            'precondiciones': 'Debe existir al menos un requerimiento funcional.',
            'flujo_principal': '1. El usuario accede a casos de uso\n2. Selecciona "Nuevo caso de uso"\n3. Ingresa nombre, actores, flujos\n4. Asocia requerimiento\n5. El sistema guarda el caso de uso',
            'postcondiciones': 'El caso de uso queda registrado y asociado.',
        },
        {
            'nombre': 'CU-07: Ver historial de versiones',
            'descripcion': 'El usuario consulta el historial de cambios de un requerimiento o caso de uso.',
            'actores': 'Todos los roles',
            'precondiciones': 'El elemento debe haber sido modificado al menos una vez.',
            'flujo_principal': '1. El usuario accede al detalle del elemento\n2. Selecciona "Ver historial"\n3. El sistema muestra todas las versiones con cambios\n4. El usuario puede comparar versiones',
            'postcondiciones': 'Se visualiza el historial completo.',
        },
        {
            'nombre': 'CU-08: Generar matriz de trazabilidad',
            'descripcion': 'El usuario genera la matriz de trazabilidad del proyecto.',
            'actores': 'Líder, Desarrollador',
            'precondiciones': 'Deben existir requerimientos y casos de uso.',
            'flujo_principal': '1. El usuario accede a reportes\n2. Selecciona "Matriz de trazabilidad"\n3. El sistema genera la matriz mostrando relaciones\n4. El usuario puede exportar a PDF',
            'postcondiciones': 'Se visualiza/exporta la matriz de trazabilidad.',
        },
        {
            'nombre': 'CU-09: Exportar documentación a PDF',
            'descripcion': 'El usuario exporta la documentación del proyecto en PDF.',
            'actores': 'Líder',
            'precondiciones': 'El proyecto debe tener datos cargados.',
            'flujo_principal': '1. El líder accede al detalle del proyecto\n2. Selecciona "Exportar a PDF"\n3. El sistema genera el documento con toda la información\n4. El usuario descarga el PDF',
            'postcondiciones': 'Se genera y descarga el archivo PDF.',
        },
        {
            'nombre': 'CU-10: Gestionar dependencias de requerimientos',
            'descripcion': 'El usuario define dependencias entre requerimientos.',
            'actores': 'Líder, Desarrollador',
            'precondiciones': 'Deben existir múltiples requerimientos.',
            'flujo_principal': '1. El usuario edita un requerimiento\n2. Selecciona otros requerimientos como dependencias\n3. El sistema guarda las relaciones\n4. Las dependencias se visualizan en la lista',
            'postcondiciones': 'Las dependencias quedan registradas.',
        },
    ]
    
    # Obtener solo requerimientos funcionales para asociar
    reqs_funcionales = [r for r in requerimientos if r.tipo == 'FUNCIONAL']
    
    # Import necesario para DetalleCasoDeUsoTradicional
    from casos_de_uso.models import DetalleCasoDeUsoTradicional
    
    casos_creados = []
    for i, data in enumerate(casos_uso):
        cu, created = CasoDeUso.objects.get_or_create(
            proyecto=proyecto,
            nombre=data['nombre'],
            defaults={
                'descripcion': data['descripcion'],
                'creado_por': lider,
            }
        )
        
        if created:
            # Asociar 1 requerimiento funcional si hay disponibles
            if reqs_funcionales:
                req_asociado = reqs_funcionales[i % len(reqs_funcionales)]
                cu.requerimiento = req_asociado
                cu.save()
            
            # Crear detalle tradicional
            DetalleCasoDeUsoTradicional.objects.get_or_create(
                caso_de_uso_padre=cu,
                defaults={
                    'actor_principal': data['actores'],
                    'precondiciones': data['precondiciones'],
                    'flujo_principal': data['flujo_principal'],
                    'postcondiciones': data['postcondiciones'],
                }
            )
            
            print(f"  ✓ {data['nombre']}")
            casos_creados.append(cu)
        else:
            print(f"  → {data['nombre']} (ya existe)")
    
    return casos_creados

def agregar_dependencias_grcu(requerimientos):
    """Agrega algunas dependencias entre requerimientos de GRCU"""
    print("\n" + "="*80)
    print("AGREGANDO DEPENDENCIAS ENTRE REQUERIMIENTOS")
    print("="*80)
    
    # Definir dependencias lógicas (nombre completo del requerimiento)
    dependencias = [
        ('RF-03: Asignación de participantes a proyectos', ['RF-01: Gestión de usuarios y roles', 'RF-02: Creación de proyectos']),
        ('RF-04: Registro de requerimientos', ['RF-02: Creación de proyectos']),
        ('RF-05: Gestión de casos de uso', ['RF-04: Registro de requerimientos']),
        ('RF-06: Versionado de requerimientos', ['RF-04: Registro de requerimientos']),
        ('RF-07: Versionado de casos de uso', ['RF-05: Gestión de casos de uso']),
        ('RF-08: Matriz de trazabilidad', ['RF-04: Registro de requerimientos', 'RF-05: Gestión de casos de uso']),
        ('RF-10: Validación de requerimientos por stakeholder', ['RF-04: Registro de requerimientos']),
        ('RF-11: Validación de requerimientos por líder', ['RF-10: Validación de requerimientos por stakeholder']),
        ('RF-13: Gestión de dependencias entre requerimientos', ['RF-04: Registro de requerimientos']),
    ]
    
    count = 0
    for req_nombre, deps_nombres in dependencias:
        try:
            req = Requerimiento.objects.get(nombre=req_nombre, proyecto__nombre="GRCU")
            deps = Requerimiento.objects.filter(
                nombre__in=deps_nombres,
                proyecto__nombre="GRCU"
            )
            
            if deps.exists():
                req.dependencias.set(deps)
                print(f"  ✓ {req_nombre} depende de {deps.count()} requerimientos")
                count += 1
        except Requerimiento.DoesNotExist:
            pass
    
    print(f"\n✅ Total dependencias agregadas: {count}")


def main():
    print("\n" + "="*80)
    print("COMPLETANDO PROYECTO GRCU")
    print("="*80)
    print("Este script agregará:")
    print("  • 3 desarrolladores adicionales")
    print("  • 1 cliente/stakeholder")
    print("  • 15 requerimientos funcionales")
    print("  • 5 requerimientos no funcionales")
    print("  • 10 casos de uso")
    print("  • Dependencias entre requerimientos")
    print("="*80)
    
    # Paso 1: Agregar participantes
    proyecto = agregar_participantes_grcu()
    if not proyecto:
        return
    
    # Paso 2: Crear requerimientos
    requerimientos = crear_requerimientos_grcu(proyecto)
    
    # Paso 3: Crear casos de uso
    casos_uso = crear_casos_uso_grcu(proyecto, requerimientos)
    
    # Paso 4: Agregar dependencias
    agregar_dependencias_grcu(requerimientos)
    
    # Resumen final
    print("\n" + "="*80)
    print("✅ PROYECTO GRCU COMPLETADO EXITOSAMENTE")
    print("="*80)
    print(f"\n📊 RESUMEN:")
    print(f"  • Participantes: {proyecto.participantes.count()}")
    print(f"  • Requerimientos: {proyecto.requerimientos.count()}")
    print(f"  • Casos de Uso: {CasoDeUso.objects.filter(proyecto=proyecto).count()}")
    
    # Calcular huérfanos
    total_reqs = proyecto.requerimientos.filter(tipo='FUNCIONAL').count()
    reqs_con_cu = proyecto.requerimientos.filter(tipo='FUNCIONAL', casos_de_uso__isnull=False).distinct().count()
    huerfanos = total_reqs - reqs_con_cu
    porcentaje = (huerfanos / total_reqs * 100) if total_reqs > 0 else 0
    
    print(f"  • Requerimientos con casos de uso: {reqs_con_cu}")
    print(f"  • Requerimientos huérfanos: {huerfanos} ({porcentaje:.0f}%)")
    print("="*80 + "\n")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
