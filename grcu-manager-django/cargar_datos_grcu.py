#!/usr/bin/env python3
"""
Script para cargar datos de prueba al proyecto GRCU:
- 17 requerimientos funcionales (RF-01 a RF-17)
- 8 requerimientos no funcionales (RNF-01 a RNF-08)
- 12 casos de uso (CU-01 a CU-12)
- Relaciones: 7 casos de uso relacionados, 5 huérfanos
"""

import os
import sys
import django
from datetime import date

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'grcu_manager.settings')
django.setup()

from proyectos.models import Proyecto
from accounts.models import Usuario
from requerimientos.models import Requerimiento, DetalleRequerimientoTradicional
from casos_de_uso.models import CasoDeUso, DetalleCasoDeUsoTradicional
from requerimientos.models import RequerimientoCaso


def cargar_datos():
    print("=" * 80)
    print("CARGANDO DATOS DE PRUEBA PARA PROYECTO GRCU")
    print("=" * 80)
    
    # 1. Obtener o crear el proyecto GRCU
    try:
        proyecto = Proyecto.objects.get(nombre__icontains="GRCU")
        print(f"✓ Proyecto encontrado: {proyecto.nombre} (ID: {proyecto.pk})")
    except Proyecto.DoesNotExist:
        print("✗ No se encontró el proyecto GRCU. Creando uno nuevo...")
        # Obtener primer usuario para asignar como líder
        usuario = Usuario.objects.first()
        if not usuario:
            print("ERROR: No hay usuarios en el sistema. Crea al menos un usuario primero.")
            return
        
        proyecto = Proyecto.objects.create(
            nombre="GRCU",
            descripcion="Gestión de Requerimientos y Casos de Uso",
            metodologia="TRADICIONAL",
            lider=usuario,
            creado_por=usuario
        )
        print(f"✓ Proyecto creado: {proyecto.nombre} (ID: {proyecto.pk})")
    
    # Obtener usuario para asignar como creador
    usuario = proyecto.lider or Usuario.objects.first()
    if not usuario:
        print("ERROR: No hay usuarios disponibles.")
        return
    
    print(f"✓ Usuario asignado: {usuario.email}")
    
    # 2. Crear 17 requerimientos funcionales
    print("\n" + "=" * 80)
    print("CREANDO 17 REQUERIMIENTOS FUNCIONALES (RF-01 a RF-17)")
    print("=" * 80)
    
    requerimientos_funcionales = []
    descripciones_rf = [
        "El sistema debe permitir el registro de nuevos usuarios con validación de correo electrónico",
        "El sistema debe autenticar usuarios mediante credenciales seguras",
        "El sistema debe permitir la gestión de proyectos (crear, editar, eliminar)",
        "El sistema debe permitir asignar roles a usuarios dentro de un proyecto",
        "El sistema debe permitir la creación de requerimientos funcionales y no funcionales",
        "El sistema debe permitir la validación de requerimientos por parte del líder",
        "El sistema debe permitir la priorización de requerimientos usando metodología MOSCOW",
        "El sistema debe permitir la creación de casos de uso",
        "El sistema debe permitir relacionar requerimientos con casos de uso",
        "El sistema debe generar una matriz de trazabilidad entre requerimientos y casos de uso",
        "El sistema debe mostrar un dashboard para el líder del proyecto",
        "El sistema debe identificar requerimientos y casos de uso huérfanos",
        "El sistema debe permitir adjuntar imágenes a requerimientos y casos de uso",
        "El sistema debe mantener un historial de cambios de requerimientos",
        "El sistema debe permitir comentarios y discusiones sobre requerimientos",
        "El sistema debe exportar la matriz de trazabilidad en formato PDF",
        "El sistema debe notificar cambios importantes en requerimientos a los interesados",
    ]
    
    for i in range(1, 18):
        nombre = f"RF-{i:02d}"
        descripcion = descripciones_rf[i-1]
        
        req, created = Requerimiento.objects.get_or_create(
            nombre=nombre,
            proyecto=proyecto,
            defaults={
                'descripcion': descripcion,
                'tipo': 'FUNCIONAL',
                'estado': 'BORRADOR',
                'creado_por': usuario,
            }
        )
        
        if created:
            # Crear detalle tradicional
            DetalleRequerimientoTradicional.objects.create(
                requerimiento_padre=req,
                prioridad='ALTA' if i <= 7 else 'MEDIA' if i <= 14 else 'BAJA',
                fuente='Cliente' if i % 2 == 0 else 'Líder de Proyecto',
                categoria='Funcionalidad Core' if i <= 10 else 'Funcionalidad Secundaria',
                fecha_compromiso=date(2025, 12, 31),
                estado_validacion='Pendiente',
                observaciones=f'Requerimiento funcional {i} del sistema GRCU'
            )
            print(f"  ✓ Creado: {nombre} - {descripcion[:60]}...")
        else:
            print(f"  → Ya existe: {nombre}")
        
        requerimientos_funcionales.append(req)
    
    # 3. Crear 8 requerimientos no funcionales
    print("\n" + "=" * 80)
    print("CREANDO 8 REQUERIMIENTOS NO FUNCIONALES (RNF-01 a RNF-08)")
    print("=" * 80)
    
    requerimientos_no_funcionales = []
    descripciones_rnf = [
        "El sistema debe responder a las solicitudes en menos de 2 segundos",
        "El sistema debe soportar al menos 100 usuarios concurrentes",
        "El sistema debe garantizar disponibilidad del 99.9% anual",
        "El sistema debe usar cifrado HTTPS para todas las comunicaciones",
        "El sistema debe realizar copias de seguridad diarias automáticas",
        "El sistema debe ser compatible con navegadores Chrome, Firefox y Edge",
        "El sistema debe cumplir con WCAG 2.1 nivel AA para accesibilidad",
        "El sistema debe mantener logs de auditoría de todas las operaciones críticas",
    ]
    
    for i in range(1, 9):
        nombre = f"RNF-{i:02d}"
        descripcion = descripciones_rnf[i-1]
        
        req, created = Requerimiento.objects.get_or_create(
            nombre=nombre,
            proyecto=proyecto,
            defaults={
                'descripcion': descripcion,
                'tipo': 'NO_FUNCIONAL',
                'estado': 'BORRADOR',
                'creado_por': usuario,
            }
        )
        
        if created:
            # Crear detalle tradicional
            DetalleRequerimientoTradicional.objects.create(
                requerimiento_padre=req,
                prioridad='ALTA' if i <= 4 else 'MEDIA',
                fuente='Requisitos Técnicos',
                categoria='Calidad' if i <= 4 else 'Restricción',
                fecha_compromiso=date(2025, 12, 31),
                estado_validacion='Pendiente',
                observaciones=f'Requerimiento no funcional {i} del sistema GRCU'
            )
            print(f"  ✓ Creado: {nombre} - {descripcion[:60]}...")
        else:
            print(f"  → Ya existe: {nombre}")
        
        requerimientos_no_funcionales.append(req)
    
    # 4. Crear 5 requerimientos de sistema
    print("\n" + "=" * 80)
    print("CREANDO 5 REQUERIMIENTOS DE SISTEMA (RS-01 a RS-05)")
    print("=" * 80)
    
    requerimientos_sistema = []
    descripciones_rs = [
        "El sistema debe estar implementado en Django 5.x con Python 3.11 o superior",
        "El sistema debe utilizar PostgreSQL como base de datos principal",
        "El sistema debe implementar autenticación mediante Django AllAuth",
        "El sistema debe ser desplegable en contenedores Docker",
        "El sistema debe utilizar Bootstrap 5 para la interfaz de usuario",
    ]
    
    for i in range(1, 6):
        nombre = f"RS-{i:02d}"
        descripcion = descripciones_rs[i-1]
        
        req, created = Requerimiento.objects.get_or_create(
            nombre=nombre,
            proyecto=proyecto,
            defaults={
                'descripcion': descripcion,
                'tipo': 'SISTEMA',
                'estado': 'BORRADOR',
                'creado_por': usuario,
            }
        )
        
        if created:
            # Crear detalle tradicional
            DetalleRequerimientoTradicional.objects.create(
                requerimiento_padre=req,
                prioridad='ALTA' if i <= 3 else 'MEDIA',
                fuente='Arquitectura Técnica',
                categoria='Infraestructura' if i <= 2 else 'Plataforma',
                fecha_compromiso=date(2025, 12, 31),
                estado_validacion='Pendiente',
                observaciones=f'Requerimiento de sistema {i} del sistema GRCU'
            )
            print(f"  ✓ Creado: {nombre} - {descripcion[:60]}...")
        else:
            print(f"  → Ya existe: {nombre}")
        
        requerimientos_sistema.append(req)
    
    # 5. Crear 12 casos de uso
    print("\n" + "=" * 80)
    print("CREANDO 12 CASOS DE USO (CU-01 a CU-12)")
    print("=" * 80)
    
    casos_de_uso = []
    descripciones_cu = [
        "Registrar nuevo usuario en el sistema",
        "Iniciar sesión en el sistema",
        "Crear proyecto de gestión de requerimientos",
        "Asignar roles a integrantes del proyecto",
        "Crear requerimiento funcional o no funcional",
        "Validar requerimiento como líder de proyecto",
        "Priorizar requerimientos usando MOSCOW",
        "Crear caso de uso para el proyecto",
        "Relacionar requerimiento con caso de uso",
        "Visualizar matriz de trazabilidad",
        "Exportar matriz de trazabilidad a PDF",
        "Consultar dashboard del líder de proyecto",
    ]
    
    for i in range(1, 13):
        nombre = f"CU-{i:02d}"
        descripcion = descripciones_cu[i-1]
        
        cu, created = CasoDeUso.objects.get_or_create(
            nombre=nombre,
            proyecto=proyecto,
            defaults={
                'descripcion': descripcion,
                'creado_por': usuario,
            }
        )
        
        if created:
            # Crear detalle tradicional
            DetalleCasoDeUsoTradicional.objects.create(
                caso_de_uso_padre=cu,
                actor_principal='Usuario' if i <= 2 else 'Líder de Proyecto' if i <= 7 else 'Miembro del Equipo',
                precondiciones=f'El usuario debe estar autenticado en el sistema' if i > 2 else 'Ninguna',
                flujo_principal=f'1. El actor accede a la funcionalidad\n2. El sistema muestra la interfaz\n3. El actor completa la acción\n4. El sistema confirma la operación',
                flujo_alternativo=f'1a. Si hay error, el sistema muestra mensaje\n2a. El actor corrige y reintenta',
                postcondiciones=f'La operación se registra en el sistema',
                observaciones=f'Caso de uso {i} del sistema GRCU'
            )
            print(f"  ✓ Creado: {nombre} - {descripcion[:60]}...")
        else:
            print(f"  → Ya existe: {nombre}")
        
        casos_de_uso.append(cu)
    
    # 5. Crear relaciones entre requerimientos y casos de uso
    # Dejar 5 CU huérfanos (CU-08 a CU-12 no tendrán relaciones)
    print("\n" + "=" * 80)
    print("CREANDO RELACIONES ENTRE REQUERIMIENTOS Y CASOS DE USO")
    print("=" * 80)
    print("→ Se relacionarán 7 casos de uso, dejando 5 huérfanos (CU-08 a CU-12)")
    
    # Mapeo de relaciones (requerimiento_index -> [lista de CU indices])
    relaciones = {
        0: [0],      # RF-01 -> CU-01 (Registro)
        1: [1],      # RF-02 -> CU-02 (Login)
        2: [2],      # RF-03 -> CU-03 (Crear proyecto)
        3: [3],      # RF-04 -> CU-04 (Asignar roles)
        4: [4],      # RF-05 -> CU-05 (Crear requerimiento)
        5: [5],      # RF-06 -> CU-06 (Validar requerimiento)
        6: [6],      # RF-07 -> CU-07 (Priorizar requerimientos)
        8: [4, 6],   # RF-09 -> CU-05, CU-07 (Relacionar requerimientos)
        9: [4, 6],   # RF-10 -> CU-05, CU-07 (Matriz de trazabilidad)
        10: [2, 4],  # RF-11 -> CU-03, CU-05 (Dashboard líder)
    }
    
    relaciones_creadas = 0
    for req_idx, cu_indices in relaciones.items():
        req = requerimientos_funcionales[req_idx]
        for cu_idx in cu_indices:
            cu = casos_de_uso[cu_idx]
            
            # Crear relación si no existe
            relacion, created = RequerimientoCaso.objects.get_or_create(
                requerimiento=req,
                caso_de_uso=cu,
                defaults={
                    'nota': f'Relación entre {req.nombre} y {cu.nombre}'
                }
            )
            
            if created:
                print(f"  ✓ {req.nombre} <-> {cu.nombre}")
                relaciones_creadas += 1
            else:
                print(f"  → Ya existe: {req.nombre} <-> {cu.nombre}")
    
    # 6. Resumen final
    print("\n" + "=" * 80)
    print("RESUMEN DE CARGA DE DATOS")
    print("=" * 80)
    print(f"✓ Proyecto: {proyecto.nombre}")
    print(f"✓ Requerimientos Funcionales: {len(requerimientos_funcionales)}")
    print(f"✓ Requerimientos No Funcionales: {len(requerimientos_no_funcionales)}")
    print(f"✓ Requerimientos de Sistema: {len(requerimientos_sistema)}")
    total_reqs = len(requerimientos_funcionales) + len(requerimientos_no_funcionales) + len(requerimientos_sistema)
    print(f"✓ Total Requerimientos: {total_reqs}")
    print(f"✓ Casos de Uso: {len(casos_de_uso)}")
    print(f"✓ Relaciones creadas: {relaciones_creadas}")
    print(f"✓ Casos de Uso huérfanos: 5 (CU-08 a CU-12)")
    print("\n" + "=" * 80)
    print("✓ CARGA COMPLETADA EXITOSAMENTE")
    print("=" * 80)
    
    # Verificar huérfanos
    print("\n📊 VERIFICACIÓN DE ELEMENTOS HUÉRFANOS:")
    for cu in casos_de_uso:
        relaciones_count = RequerimientoCaso.objects.filter(caso_de_uso=cu).count()
        if relaciones_count == 0:
            print(f"  ⚠ {cu.nombre} - HUÉRFANO (sin relaciones)")
        else:
            print(f"  ✓ {cu.nombre} - {relaciones_count} relación(es)")


if __name__ == "__main__":
    try:
        cargar_datos()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
