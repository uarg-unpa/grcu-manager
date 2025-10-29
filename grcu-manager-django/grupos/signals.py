from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Grupo
from proyectos.models import Proyecto, ParticipacionProyecto
from roles.models import Rol


@receiver(m2m_changed, sender=Grupo.integrantes.through)
def sincronizar_participantes_proyecto(sender, instance, action, pk_set, **kwargs):
    """
    Cuando se agregan o eliminan integrantes de un grupo, 
    sincroniza automáticamente los participantes de los proyectos asignados a ese grupo.
    """
    # Solo actuar cuando se agregan integrantes (post_add) o se eliminan (post_remove)
    if action not in ['post_add', 'post_remove']:
        return
    
    # Obtener el grupo
    grupo = instance
    
    # Obtener todos los proyectos asignados a este grupo
    proyectos = Proyecto.objects.filter(grupo=grupo, activo=True)
    
    if not proyectos.exists():
        return  # Si el grupo no tiene proyectos, no hacer nada
    
    # Obtener el rol por defecto (Desarrollador)
    try:
        rol_developer = Rol.objects.get(nombre__iexact='Desarrollador')
    except Rol.DoesNotExist:
        print("⚠️ Advertencia: No se encontró el rol 'Desarrollador'. No se pueden sincronizar participantes.")
        return
    
    if action == 'post_add':
        # Se agregaron nuevos integrantes al grupo
        # pk_set contiene los IDs de los usuarios agregados
        from accounts.models import Usuario
        nuevos_usuarios = Usuario.objects.filter(id__in=pk_set)
        
        for proyecto in proyectos:
            for usuario in nuevos_usuarios:
                # Verificar si el usuario ya es participante del proyecto
                participacion_existente = ParticipacionProyecto.objects.filter(
                    usuario=usuario,
                    proyecto=proyecto
                ).exists()
                
                if not participacion_existente:
                    # Agregar el usuario al proyecto con rol Desarrollador
                    ParticipacionProyecto.objects.create(
                        usuario=usuario,
                        proyecto=proyecto,
                        rol=rol_developer
                    )
                    print(f"✅ Usuario {usuario.email} agregado al proyecto {proyecto.nombre}")
    
    elif action == 'post_remove':
        # Se eliminaron integrantes del grupo
        # pk_set contiene los IDs de los usuarios eliminados
        from accounts.models import Usuario
        usuarios_eliminados = Usuario.objects.filter(id__in=pk_set)
        
        for proyecto in proyectos:
            for usuario in usuarios_eliminados:
                # Eliminar al usuario del proyecto (a menos que sea el líder)
                if proyecto.lider != usuario:
                    ParticipacionProyecto.objects.filter(
                        usuario=usuario,
                        proyecto=proyecto
                    ).delete()
                    print(f"❌ Usuario {usuario.email} eliminado del proyecto {proyecto.nombre}")
                else:
                    print(f"⚠️ No se puede eliminar al líder {usuario.email} del proyecto {proyecto.nombre}")
