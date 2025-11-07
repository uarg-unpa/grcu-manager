#!/usr/bin/env python3
"""
Script para cargar datos de demostración completos:
- 30 usuarios con diferentes roles
- 4 grupos con estudiantes
- 4 proyectos con temáticas diferentes
- Cada proyecto con cliente/stakeholder
- Requerimientos y casos de uso por proyecto
- 30% de requerimientos huérfanos
- Relaciones entre requerimientos y casos de uso
- Dependencias entre requerimientos
- Historial de versiones (ediciones múltiples)
"""

import os
import sys
import django
from datetime import date, datetime, timedelta
from random import choice, sample, randint

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'grcu_manager.settings')
django.setup()

from proyectos.models import Proyecto, Grupo, ParticipacionProyecto
from accounts.models import Usuario
from roles.models import Rol
from requerimientos.models import Requerimiento, DetalleRequerimientoTradicional, DetalleRequerimientoAgil, RequerimientoCaso
from casos_de_uso.models import CasoDeUso, DetalleCasoDeUsoTradicional


def crear_usuarios():
    """Crear 30 usuarios con diferentes roles"""
    print("\n" + "=" * 80)
    print("CREANDO 30 USUARIOS")
    print("=" * 80)
    
    nombres = [
        "Ana García", "Bruno Martínez", "Carla López", "Diego Fernández", "Elena Rodríguez",
        "Fernando Torres", "Gloria Santos", "Hugo Ramírez", "Isabel Flores", "Javier Morales",
        "Karla Díaz", "Luis Herrera", "María Castro", "Nicolás Ruiz", "Olivia Ortiz",
        "Pablo Vargas", "Quintín Jiménez", "Rosa Méndez", "Sergio Cruz", "Teresa Guzmán",
        "Ulises Romero", "Valeria Soto", "Walter Peña", "Ximena Vega", "Yago Reyes",
        "Zoe Navarro", "Andrés Silva", "Beatriz Campos", "Carlos Ramos", "Diana Núñez"
    ]
    
    usuarios_creados = []
    
    for i, nombre in enumerate(nombres, 1):
        email = f"{nombre.lower().replace(' ', '.')}.{i}@unpa.edu.ar"
        
        usuario, created = Usuario.objects.get_or_create(
            email=email,
            defaults={
                'nombre': nombre,
                'avatar': f'https://ui-avatars.com/api/?name={nombre.replace(" ", "+")}&background=random',
                'is_active': True,
            }
        )
        
        if created:
            usuario.set_password('demo123')  # Misma contraseña para todos en demo
            usuario.save()
            print(f"  ✓ {i:02d}. {nombre} ({email})")
        else:
            print(f"  → {i:02d}. {nombre} (ya existe)")
        
        usuarios_creados.append(usuario)
    
    return usuarios_creados


def crear_grupos(usuarios):
    """Crear 4 grupos de estudiantes"""
    print("\n" + "=" * 80)
    print("CREANDO 4 GRUPOS")
    print("=" * 80)
    
    nombres_grupos = [
        "Grupo Alpha - Ing. Sistemas",
        "Grupo Beta - Ing. Software",
        "Grupo Gamma - Lic. Informática",
        "Grupo Delta - Tec. Programación"
    ]
    
    grupos_creados = []
    
    for i, nombre in enumerate(nombres_grupos):
        # Asignar 6-8 miembros por grupo
        miembros = sample(usuarios, randint(6, 8))
        
        grupo, created = Grupo.objects.get_or_create(
            nombre=nombre,
            defaults={
                'creado_por': choice(usuarios),
            }
        )
        
        if created:
            grupo.integrantes.set(miembros)
            print(f"  ✓ {nombre} ({len(miembros)} miembros)")
        else:
            print(f"  → {nombre} (ya existe)")
        
        grupos_creados.append(grupo)
    
    return grupos_creados


def crear_proyectos(usuarios, grupos):
    """Crear 4 proyectos con diferentes temáticas"""
    print("\n" + "=" * 80)
    print("CREANDO 4 PROYECTOS CON TEMÁTICAS DIFERENTES")
    print("=" * 80)
    
    # Obtener roles
    rol_lider = Rol.objects.get(nombre='Líder')
    rol_stakeholder = Rol.objects.get(nombre='Stakeholder')
    rol_dev = Rol.objects.get(nombre='Desarrollador')
    
    proyectos_data = [
        {
            'nombre': 'Sistema de Gestión Hospitalaria',
            'descripcion': 'Sistema para gestionar pacientes, citas médicas, historias clínicas y farmacia en un hospital regional',
            'metodologia': 'TRADICIONAL',
            'tema': 'salud',
        },
        {
            'nombre': 'E-Commerce de Productos Artesanales',
            'descripcion': 'Plataforma de comercio electrónico para artesanos locales con sistema de pagos y envíos',
            'metodologia': 'AGIL',
            'tema': 'comercio',
        },
        {
            'nombre': 'App de Transporte Universitario',
            'descripcion': 'Aplicación móvil para coordinar transporte compartido entre estudiantes de la universidad',
            'metodologia': 'AGIL',
            'tema': 'transporte',
        },
        {
            'nombre': 'Sistema de Biblioteca Digital',
            'descripcion': 'Sistema para gestionar préstamos de libros, reservas, multas y catálogo digital de la biblioteca universitaria',
            'metodologia': 'TRADICIONAL',
            'tema': 'educacion',
        },
    ]
    
    proyectos_creados = []
    
    for i, data in enumerate(proyectos_data):
        # Asignar líder, cliente y grupo
        lider = usuarios[i * 7]  # Distribuir líderes
        cliente = usuarios[i * 7 + 1]  # Un stakeholder por proyecto
        grupo = grupos[i]
        participantes = list(grupo.integrantes.all())[:5]  # 5 desarrolladores
        
        proyecto, created = Proyecto.objects.get_or_create(
            nombre=data['nombre'],
            defaults={
                'descripcion': data['descripcion'],
                'metodologia': data['metodologia'],
                'lider': lider,
                'grupo': grupo,
                'creado_por': lider,
            }
        )
        
        if created:
            # Crear participación del stakeholder/cliente
            ParticipacionProyecto.objects.get_or_create(
                usuario=cliente,
                proyecto=proyecto,
                defaults={'rol': rol_stakeholder}
            )
            
            # Crear participación del líder
            ParticipacionProyecto.objects.get_or_create(
                usuario=lider,
                proyecto=proyecto,
                defaults={'rol': rol_lider}
            )
            
            # Crear participaciones de desarrolladores
            for dev in participantes:
                if dev != lider and dev != cliente:  # Evitar duplicados
                    ParticipacionProyecto.objects.get_or_create(
                        usuario=dev,
                        proyecto=proyecto,
                        defaults={'rol': rol_dev}
                    )
            
            print(f"  ✓ {data['nombre']}")
            print(f"    - Líder: {lider.nombre}")
            print(f"    - Cliente: {cliente.nombre}")
            print(f"    - Grupo: {grupo.nombre}")
            print(f"    - Metodología: {data['metodologia']}")
            print(f"    - Participantes: {len(participantes)}")
        else:
            print(f"  → {data['nombre']} (ya existe)")
        
        data['proyecto'] = proyecto
        data['lider'] = lider
        data['cliente'] = cliente
        proyectos_creados.append(data)
    
    return proyectos_creados


def crear_requerimientos_y_casos(proyectos_data):
    """Crear requerimientos y casos de uso para cada proyecto"""
    print("\n" + "=" * 80)
    print("CREANDO REQUERIMIENTOS Y CASOS DE USO POR PROYECTO")
    print("=" * 80)
    
    # Definir requerimientos por temática
    reqs_templates = {
        'salud': {
            'funcionales': [
                "Registrar paciente con datos personales y de contacto",
                "Agendar cita médica con especialista",
                "Consultar historia clínica del paciente",
                "Registrar diagnóstico y tratamiento médico",
                "Gestionar inventario de farmacia hospitalaria",
                "Emitir recetas médicas electrónicas",
                "Registrar signos vitales del paciente",
                "Gestionar turnos de médicos y enfermeras",
                "Generar reportes estadísticos de atenciones",
                "Controlar acceso por roles (médico, enfermera, admin)",
                "Registrar vacunas aplicadas",
                "Gestionar camas y habitaciones disponibles",
                "Enviar notificaciones de citas por email/SMS",
                "Registrar alergias y condiciones médicas",
                "Gestionar laboratorio y resultados de análisis",
            ],
            'no_funcionales': [
                "El sistema debe proteger datos sensibles con cifrado",
                "Cumplir con normativas HIPAA de privacidad médica",
                "Disponibilidad 24/7 con 99.9% uptime",
                "Respuesta en menos de 3 segundos",
                "Soportar 500 usuarios concurrentes",
            ],
            'casos_uso': [
                "Registrar nuevo paciente en el sistema",
                "Agendar cita con médico especialista",
                "Consultar historia clínica completa",
                "Registrar atención médica y diagnóstico",
                "Gestionar medicamentos en farmacia",
                "Emitir receta electrónica",
                "Registrar ingreso de paciente",
                "Generar reporte mensual de atenciones",
                "Gestionar turnos del personal médico",
                "Consultar disponibilidad de camas",
            ],
        },
        'comercio': {
            'funcionales': [
                "Registrar usuario comprador y vendedor",
                "Publicar producto artesanal con fotos",
                "Buscar productos por categoría y filtros",
                "Agregar productos al carrito de compras",
                "Realizar pago con tarjeta o transferencia",
                "Calificar vendedor y producto",
                "Gestionar envíos y seguimiento",
                "Chat entre comprador y vendedor",
                "Panel de administración de ventas",
                "Gestionar devoluciones y reembolsos",
                "Sistema de cupones y descuentos",
                "Notificaciones de ofertas y novedades",
                "Historial de compras y favoritos",
                "Verificación de vendedores artesanos",
                "Gestión de stock de productos",
            ],
            'no_funcionales': [
                "Integración segura con pasarelas de pago",
                "Protección de datos bancarios PCI-DSS",
                "Escalabilidad para 10,000 productos",
                "Optimización para dispositivos móviles",
                "Imágenes optimizadas para carga rápida",
            ],
            'casos_uso': [
                "Registrarse como vendedor artesano",
                "Publicar producto con fotos y descripción",
                "Buscar y filtrar productos",
                "Comprar producto artesanal",
                "Procesar pago seguro",
                "Calificar compra realizada",
                "Gestionar mis ventas",
                "Chatear con vendedor",
                "Rastrear pedido en envío",
                "Solicitar devolución de producto",
            ],
        },
        'transporte': {
            'funcionales': [
                "Registrar usuario estudiante con credenciales UNPA",
                "Publicar ruta de viaje disponible",
                "Buscar viajes por origen, destino y horario",
                "Solicitar asiento en viaje compartido",
                "Confirmar o rechazar solicitudes de pasajeros",
                "Calificar conductor y pasajero",
                "Dividir costos de combustible automáticamente",
                "Verificar identidad universitaria",
                "Chat entre conductor y pasajeros",
                "Historial de viajes realizados",
                "Notificaciones de viajes cercanos",
                "Reportar incidentes o problemas",
                "Gestionar vehículos registrados",
                "Sistema de puntos de encuentro predefinidos",
                "Modo de emergencia con contactos",
            ],
            'no_funcionales': [
                "Geolocalización en tiempo real GPS",
                "Notificaciones push instantáneas",
                "Disponibilidad en iOS y Android",
                "Verificación de estudiantes con base de datos UNPA",
                "Privacidad de datos de ubicación",
            ],
            'casos_uso': [
                "Registrarse como estudiante UNPA",
                "Publicar ruta de viaje compartido",
                "Buscar viajes disponibles",
                "Solicitar unirse a viaje",
                "Gestionar solicitudes de pasajeros",
                "Calificar experiencia de viaje",
                "Dividir gastos de combustible",
                "Chatear con conductor",
                "Reportar incidente en viaje",
                "Ver historial de viajes",
            ],
        },
        'educacion': {
            'funcionales': [
                "Registrar usuario (estudiante, docente, admin)",
                "Buscar libro en catálogo digital",
                "Solicitar préstamo de libro físico",
                "Reservar libro prestado",
                "Renovar préstamo activo",
                "Devolver libro prestado",
                "Calcular y registrar multas por retraso",
                "Gestionar catálogo de libros digitales",
                "Descargar libro digital en PDF",
                "Gestionar salas de estudio",
                "Reservar sala de estudio grupal",
                "Estadísticas de libros más prestados",
                "Sugerir libros según historial",
                "Notificar devoluciones próximas",
                "Gestionar proveedores de libros",
            ],
            'no_funcionales': [
                "Integración con sistema académico UNPA",
                "Búsqueda rápida en catálogo de 50,000 libros",
                "Backup diario de base de datos",
                "Acceso desde red interna y VPN",
                "Compatibilidad con lectores de PDF",
            ],
            'casos_uso': [
                "Buscar libro en catálogo",
                "Solicitar préstamo de libro",
                "Reservar libro no disponible",
                "Renovar préstamo de libro",
                "Devolver libro a biblioteca",
                "Consultar multas pendientes",
                "Descargar libro digital",
                "Reservar sala de estudio",
                "Gestionar catálogo de libros",
                "Ver estadísticas de préstamos",
            ],
        },
    }
    
    for proyecto_data in proyectos_data:
        proyecto = proyecto_data['proyecto']
        tema = proyecto_data['tema']
        metodologia = proyecto_data['metodologia']
        lider = proyecto_data['lider']
        
        print(f"\n📁 {proyecto.nombre}")
        print(f"   Temática: {tema.upper()} | Metodología: {metodologia}")
        
        templates = reqs_templates[tema]
        
        # Crear requerimientos funcionales
        reqs_funcionales = []
        for i, desc in enumerate(templates['funcionales'], 1):
            req = Requerimiento.objects.create(
                nombre=f"RF-{i:02d}",
                descripcion=desc,
                tipo='FUNCIONAL',
                estado=choice(['BORRADOR', 'VALIDADO', 'PRIORIZADO']),
                proyecto=proyecto,
                creado_por=lider,
            )
            
            if metodologia == 'TRADICIONAL':
                DetalleRequerimientoTradicional.objects.create(
                    requerimiento_padre=req,
                    prioridad=choice(['MUST', 'SHOULD', 'COULD', 'WONT']),
                    fuente=choice(['Cliente', 'Líder', 'Usuario Final']),
                    categoria='Funcionalidad Principal' if i <= 8 else 'Funcionalidad Secundaria',
                    fecha_compromiso=date.today() + timedelta(days=randint(30, 120)),
                )
            else:
                DetalleRequerimientoAgil.objects.create(
                    requerimiento_padre=req,
                    prioridad=choice(['MUST', 'SHOULD', 'COULD']),
                    historia_usuario=f"Como usuario, quiero {desc.lower()} para mejorar mi experiencia",
                    criterio_aceptacion=f"- El sistema debe {desc.lower()}\n- La operación debe confirmarse\n- Se debe mostrar mensaje de éxito",
                    puntos_estimados=randint(1, 8),
                )
            
            reqs_funcionales.append(req)
        
        # Crear requerimientos no funcionales
        reqs_no_funcionales = []
        for i, desc in enumerate(templates['no_funcionales'], 1):
            req = Requerimiento.objects.create(
                nombre=f"RNF-{i:02d}",
                descripcion=desc,
                tipo='NO_FUNCIONAL',
                estado=choice(['BORRADOR', 'VALIDADO']),
                proyecto=proyecto,
                creado_por=lider,
            )
            
            if metodologia == 'TRADICIONAL':
                DetalleRequerimientoTradicional.objects.create(
                    requerimiento_padre=req,
                    prioridad='MUST' if i <= 3 else 'SHOULD',
                    fuente='Requisitos Técnicos',
                    categoria='Calidad',
                )
            else:
                DetalleRequerimientoAgil.objects.create(
                    requerimiento_padre=req,
                    prioridad='MUST' if i <= 3 else 'SHOULD',
                    historia_usuario=f"Como sistema, debo {desc.lower()}",
                    criterio_aceptacion=f"- {desc}\n- Debe cumplir estándares de calidad",
                )
            
            reqs_no_funcionales.append(req)
        
        # Crear casos de uso
        casos_uso = []
        for i, desc in enumerate(templates['casos_uso'], 1):
            cu = CasoDeUso.objects.create(
                nombre=f"CU-{i:02d}",
                descripcion=desc,
                proyecto=proyecto,
                creado_por=lider,
            )
            
            DetalleCasoDeUsoTradicional.objects.create(
                caso_de_uso_padre=cu,
                actor_principal=choice(['Usuario', 'Administrador', 'Cliente', 'Estudiante', 'Médico']),
                precondiciones='Usuario autenticado en el sistema' if i > 1 else 'Ninguna',
                flujo_principal=f'1. El actor inicia la funcionalidad\n2. El sistema valida permisos\n3. El sistema muestra interfaz\n4. El actor completa acción\n5. El sistema confirma operación',
                flujo_alternativo='Si hay error, el sistema muestra mensaje y permite reintentar',
                postcondiciones='La operación queda registrada en el sistema',
            )
            
            casos_uso.append(cu)
        
        # Crear relaciones (70% de requerimientos tendrán casos de uso, 30% huérfanos)
        total_reqs = len(reqs_funcionales)
        reqs_a_relacionar = int(total_reqs * 0.7)  # 70% con relación
        
        reqs_seleccionados = sample(reqs_funcionales, reqs_a_relacionar)
        
        for req in reqs_seleccionados:
            # Cada req puede tener 1-2 casos de uso
            num_casos = randint(1, 2)
            casos_relacionados = sample(casos_uso, min(num_casos, len(casos_uso)))
            
            for cu in casos_relacionados:
                RequerimientoCaso.objects.create(
                    requerimiento=req,
                    caso_de_uso=cu,
                    nota=f'Relación {req.nombre} - {cu.nombre}'
                )
        
        # Crear dependencias entre requerimientos (algunos reqs dependen de otros)
        for i in range(3, min(10, len(reqs_funcionales))):
            # Los reqs posteriores pueden depender de los anteriores
            dependencias = sample(reqs_funcionales[:i], randint(1, 2))
            reqs_funcionales[i].dependencias.set(dependencias)
        
        # Simular ediciones para generar historial (editar algunos requerimientos)
        reqs_a_editar = sample(reqs_funcionales, min(5, len(reqs_funcionales)))
        for req in reqs_a_editar:
            req.descripcion += " [Actualizado con feedback del cliente]"
            req.save()
            # Segunda edición
            req.estado = 'VALIDADO' if req.estado == 'BORRADOR' else req.estado
            req.save()
        
        print(f"   ✓ Requerimientos Funcionales: {len(reqs_funcionales)}")
        print(f"   ✓ Requerimientos No Funcionales: {len(reqs_no_funcionales)}")
        print(f"   ✓ Casos de Uso: {len(casos_uso)}")
        print(f"   ✓ Requerimientos con relación: {reqs_a_relacionar} ({int(reqs_a_relacionar/total_reqs*100)}%)")
        print(f"   ✓ Requerimientos huérfanos: {total_reqs - reqs_a_relacionar} (~30%)")


def main():
    """Función principal"""
    print("=" * 80)
    print("SCRIPT DE CARGA DE DATOS COMPLETOS PARA DEMOSTRACIÓN")
    print("=" * 80)
    print("Este script creará:")
    print("  • 30 usuarios con avatares")
    print("  • 4 grupos de estudiantes")
    print("  • 4 proyectos con diferentes temáticas")
    print("  • Requerimientos y casos de uso por proyecto")
    print("  • 30% de requerimientos huérfanos")
    print("  • Relaciones y dependencias")
    print("  • Historial de versiones")
    print("=" * 80)
    
    # Ejecutar carga automáticamente
    usuarios = crear_usuarios()
    grupos = crear_grupos(usuarios)
    proyectos = crear_proyectos(usuarios, grupos)
    crear_requerimientos_y_casos(proyectos)
    
    print("\n" + "=" * 80)
    print("✅ CARGA COMPLETADA EXITOSAMENTE")
    print("=" * 80)
    print("\n📊 RESUMEN:")
    print(f"  • Usuarios: {len(usuarios)}")
    print(f"  • Grupos: {len(grupos)}")
    print(f"  • Proyectos: {len(proyectos)}")
    print("\n💡 CREDENCIALES DE ACCESO:")
    print("  • Email: cualquier usuario creado (ej: ana.garcía.1@unpa.edu.ar)")
    print("  • Password: demo123")
    print("\n" + "=" * 80)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Cancelado por el usuario")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
