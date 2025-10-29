"""
Script de utilidad para sincronizar manualmente los participantes de proyectos con los integrantes de sus grupos.
Ejecutar con: python manage.py shell < sync_participants.py
"""

from grupos.models import Grupo
from proyectos.models import Proyecto, ParticipacionProyecto
from roles.models import Rol

def sincronizar_participantes_manuales():
    """
    Sincroniza manualmente todos los proyectos que tienen grupo asignado
    para asegurar que todos los integrantes del grupo sean participantes del proyecto.
    """
    
    # Obtener el rol Desarrollador
    try:
        rol_developer = Rol.objects.get(nombre__iexact='Desarrollador')
    except Rol.DoesNotExist:
        print("❌ ERROR: No se encontró el rol 'Desarrollador'")
        return
    
    # Obtener todos los proyectos activos que tienen un grupo asignado
    proyectos_con_grupo = Proyecto.objects.filter(grupo__isnull=False, activo=True)
    
    print(f"\n🔍 Encontrados {proyectos_con_grupo.count()} proyectos con grupo asignado\n")
    
    for proyecto in proyectos_con_grupo:
        grupo = proyecto.grupo
        print(f"📋 Procesando: Proyecto '{proyecto.nombre}' - Grupo '{grupo.nombre}'")
        
        # Obtener todos los integrantes del grupo
        integrantes = grupo.integrantes.all()
        print(f"   👥 Integrantes del grupo: {integrantes.count()}")
        
        # Obtener participantes actuales del proyecto
        participantes_actuales = proyecto.participantes.all()
        print(f"   ✅ Participantes actuales del proyecto: {participantes_actuales.count()}")
        
        # Agregar integrantes faltantes
        agregados = 0
        for integrante in integrantes:
            # Verificar si ya es participante
            if not participantes_actuales.filter(id=integrante.id).exists():
                # Agregar como Desarrollador (a menos que sea el líder)
                if proyecto.lider == integrante:
                    print(f"   ⚠️  {integrante.email} ya es líder del proyecto, saltando...")
                    continue
                
                ParticipacionProyecto.objects.create(
                    usuario=integrante,
                    proyecto=proyecto,
                    rol=rol_developer
                )
                print(f"   ➕ Agregado: {integrante.email}")
                agregados += 1
        
        if agregados == 0:
            print(f"   ✨ Proyecto ya está sincronizado correctamente")
        else:
            print(f"   ✅ Se agregaron {agregados} participantes")
        
        print()
    
    print("✅ Sincronización completada\n")


if __name__ == "__main__":
    sincronizar_participantes_manuales()
