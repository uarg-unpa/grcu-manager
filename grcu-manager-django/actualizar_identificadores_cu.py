"""
Script para generar identificadores automáticos para casos de uso existentes
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'grcu_manager.settings')
django.setup()

from casos_de_uso.models import CasoDeUso

def generar_identificadores():
    """Genera identificadores para todos los casos de uso que no tienen uno"""
    casos_sin_id = CasoDeUso.objects.filter(identificador='')
    
    print(f"Encontrados {casos_sin_id.count()} casos de uso sin identificador")
    
    # Agrupar por proyecto
    proyectos = set(casos_sin_id.values_list('proyecto', flat=True))
    
    for proyecto_id in proyectos:
        casos_proyecto = casos_sin_id.filter(proyecto_id=proyecto_id).order_by('id')
        print(f"\nProcesando proyecto ID {proyecto_id}: {casos_proyecto.count()} casos de uso")
        
        for idx, caso in enumerate(casos_proyecto, start=1):
            caso.identificador = f"CU-{idx:03d}"
            caso.save(update_fields=['identificador'])
            print(f"  ✓ {caso.identificador} - {caso.nombre}")
    
    print(f"\n✅ Proceso completado")

if __name__ == '__main__':
    generar_identificadores()
