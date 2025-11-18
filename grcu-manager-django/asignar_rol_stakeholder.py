#!/usr/bin/env python3
"""
Script para asignar el rol Stakeholder a usuarios específicos o a todos los clientes existentes en proyectos.
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'grcu_manager.settings')
django.setup()

from accounts.models import Usuario
from roles.models import Rol
from proyectos.models import Proyecto

def asignar_stakeholder_a_clientes_actuales():
    """Asigna rol Stakeholder a todos los usuarios que ya son clientes en algún proyecto"""
    print("=" * 80)
    print("ASIGNANDO ROL STAKEHOLDER A CLIENTES EXISTENTES EN PROYECTOS")
    print("=" * 80)
    
    # Obtener o crear el rol Stakeholder
    rol_stakeholder, created = Rol.objects.get_or_create(
        nombre='Stakeholder',
        defaults={'color': '#17a2b8'}
    )
    
    if created:
        print(f"✓ Rol 'Stakeholder' creado")
    else:
        print(f"→ Rol 'Stakeholder' ya existe")
    
    # Obtener todos los clientes de todos los proyectos
    clientes_ids = set()
    for proyecto in Proyecto.objects.all():
        for cliente in proyecto.clientes.all():
            clientes_ids.add(cliente.id)
    
    if not clientes_ids:
        print("\n⚠️  No se encontraron clientes asignados a proyectos")
        return
    
    print(f"\n📊 Se encontraron {len(clientes_ids)} usuarios únicos como clientes en proyectos")
    print("\nAsignando rol Stakeholder...")
    
    count = 0
    for usuario_id in clientes_ids:
        usuario = Usuario.objects.get(id=usuario_id)
        if not usuario.roles.filter(nombre='Stakeholder').exists():
            usuario.roles.add(rol_stakeholder)
            print(f"  ✓ {usuario.nombre} ({usuario.email})")
            count += 1
        else:
            print(f"  → {usuario.nombre} ya tiene el rol")
    
    print(f"\n✅ Se asignó el rol Stakeholder a {count} usuarios")


def asignar_stakeholder_a_usuarios_especificos():
    """Permite asignar rol Stakeholder a usuarios específicos por email"""
    print("=" * 80)
    print("ASIGNAR ROL STAKEHOLDER A USUARIOS ESPECÍFICOS")
    print("=" * 80)
    
    # Obtener o crear el rol Stakeholder
    rol_stakeholder, created = Rol.objects.get_or_create(
        nombre='Stakeholder',
        defaults={'color': '#17a2b8'}
    )
    
    print("\nIngresa los emails de los usuarios (uno por línea).")
    print("Presiona Enter dos veces cuando termines:")
    print()
    
    emails = []
    while True:
        email = input("Email: ").strip()
        if not email:
            break
        emails.append(email)
    
    if not emails:
        print("\n⚠️  No se ingresaron emails")
        return
    
    print(f"\n📊 Procesando {len(emails)} emails...")
    
    count = 0
    for email in emails:
        try:
            usuario = Usuario.objects.get(email=email)
            if not usuario.roles.filter(nombre='Stakeholder').exists():
                usuario.roles.add(rol_stakeholder)
                print(f"  ✓ {usuario.nombre} ({usuario.email})")
                count += 1
            else:
                print(f"  → {usuario.nombre} ya tiene el rol")
        except Usuario.DoesNotExist:
            print(f"  ✗ No existe usuario con email: {email}")
    
    print(f"\n✅ Se asignó el rol Stakeholder a {count} usuarios")


def mostrar_stakeholders_actuales():
    """Muestra todos los usuarios que tienen el rol Stakeholder"""
    print("=" * 80)
    print("USUARIOS CON ROL STAKEHOLDER")
    print("=" * 80)
    
    stakeholders = Usuario.objects.filter(roles__nombre='Stakeholder').distinct().order_by('nombre')
    
    if not stakeholders.exists():
        print("\n⚠️  No hay usuarios con rol Stakeholder")
        return
    
    print(f"\nTotal: {stakeholders.count()} usuarios\n")
    for s in stakeholders:
        print(f"  • {s.nombre} ({s.email})")


def main():
    """Menú principal"""
    while True:
        print("\n" + "=" * 80)
        print("GESTIÓN DE ROL STAKEHOLDER")
        print("=" * 80)
        print("\n1. Asignar rol Stakeholder a CLIENTES ACTUALES de proyectos (automático)")
        print("2. Asignar rol Stakeholder a usuarios ESPECÍFICOS (manual)")
        print("3. Mostrar usuarios que YA TIENEN el rol Stakeholder")
        print("4. Salir")
        print()
        
        opcion = input("Selecciona una opción (1-4): ").strip()
        
        if opcion == '1':
            asignar_stakeholder_a_clientes_actuales()
        elif opcion == '2':
            asignar_stakeholder_a_usuarios_especificos()
        elif opcion == '3':
            mostrar_stakeholders_actuales()
        elif opcion == '4':
            print("\n👋 ¡Hasta luego!")
            break
        else:
            print("\n⚠️  Opción inválida")


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
