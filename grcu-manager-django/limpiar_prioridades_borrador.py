#!/usr/bin/env python
"""
Script para limpiar las prioridades de requerimientos en estado BORRADOR.
Los requerimientos sin validar no deberían tener prioridad asignada.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'grcu_manager.settings')
django.setup()

from requerimientos.models import Requerimiento, DetalleRequerimientoTradicional, DetalleRequerimientoAgil

def limpiar_prioridades_borrador():
    """Limpia las prioridades de requerimientos en estado BORRADOR"""
    
    print("=" * 80)
    print("LIMPIEZA DE PRIORIDADES EN REQUERIMIENTOS BORRADOR")
    print("=" * 80)
    
    # Obtener requerimientos en BORRADOR
    requerimientos_borrador = Requerimiento.objects.filter(estado='BORRADOR')
    total_borrador = requerimientos_borrador.count()
    
    print(f"\n📋 Total de requerimientos en BORRADOR: {total_borrador}")
    
    # Contar cuántos tienen prioridad en gestión tradicional
    count_tradicional = 0
    count_agil = 0
    
    for req in requerimientos_borrador:
        # Verificar gestión tradicional
        if hasattr(req, 'detalle_tradicional') and req.detalle_tradicional.prioridad:
            print(f"\n  🔹 {req.nombre} (ID: {req.id})")
            print(f"     Tipo: Tradicional")
            print(f"     Prioridad actual: {req.detalle_tradicional.prioridad}")
            req.detalle_tradicional.prioridad = ''
            req.detalle_tradicional.save()
            count_tradicional += 1
            print(f"     ✅ Prioridad eliminada")
        
        # Verificar gestión ágil
        if hasattr(req, 'detalle_agil') and req.detalle_agil.prioridad:
            print(f"\n  🔹 {req.nombre} (ID: {req.id})")
            print(f"     Tipo: Ágil")
            print(f"     Prioridad actual: {req.detalle_agil.prioridad}")
            req.detalle_agil.prioridad = ''
            req.detalle_agil.save()
            count_agil += 1
            print(f"     ✅ Prioridad eliminada")
    
    print("\n" + "=" * 80)
    print("RESUMEN")
    print("=" * 80)
    print(f"Requerimientos tradicionales actualizados: {count_tradicional}")
    print(f"Requerimientos ágiles actualizados: {count_agil}")
    print(f"Total de prioridades eliminadas: {count_tradicional + count_agil}")
    print("\n✅ Proceso completado")

if __name__ == '__main__':
    limpiar_prioridades_borrador()
