"""
Comando para cargar 20 requerimientos de ejemplo sobre un proyecto de gestión de requerimientos y casos de uso.
Uso: python manage.py seed_requerimientos
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from accounts.models import Usuario
from proyectos.models import Proyecto
from requerimientos.models import Requerimiento, DetalleRequerimientoTradicional, DetalleRequerimientoAgil
from casos_de_uso.models import CasoDeUso
from datetime import datetime, timedelta
from django.utils import timezone


class Command(BaseCommand):
    help = 'Carga 20 requerimientos de ejemplo para un proyecto de gestión de requerimientos'

    def add_arguments(self, parser):
        parser.add_argument(
            '--proyecto-id',
            type=int,
            help='ID del proyecto donde cargar los requerimientos (opcional)',
        )
        parser.add_argument(
            '--metodologia',
            type=str,
            choices=['TRADICIONAL', 'AGIL'],
            default='TRADICIONAL',
            help='Metodología del proyecto (TRADICIONAL o AGIL)',
        )

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('=' * 70))
        self.stdout.write(self.style.SUCCESS('INICIANDO CARGA DE REQUERIMIENTOS'))
        self.stdout.write(self.style.SUCCESS('=' * 70))
        
        # Obtener o crear el proyecto
        proyecto_id = options.get('proyecto_id')
        metodologia = options.get('metodologia')
        
        if proyecto_id:
            try:
                proyecto = Proyecto.objects.get(id=proyecto_id)
                self.stdout.write(self.style.WARNING(f'Usando proyecto existente: {proyecto.nombre}'))
            except Proyecto.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Proyecto con ID {proyecto_id} no existe'))
                return
        else:
            # Buscar líder con proyectos o crear uno nuevo
            lider = Usuario.objects.filter(is_staff=True).first()
            if not lider:
                self.stdout.write(self.style.ERROR('No hay usuarios staff. Crea un superusuario primero.'))
                return
            
            # Intentar usar un proyecto existente del líder
            proyecto_existente = lider.lidera_proyectos.first()
            
            if proyecto_existente:
                self.stdout.write(self.style.WARNING(f'Usando proyecto existente del líder: {proyecto_existente.nombre}'))
                proyecto = proyecto_existente
                # Actualizar metodología si es diferente
                if proyecto.metodologia != metodologia:
                    proyecto.metodologia = metodologia
                    proyecto.save()
                    self.stdout.write(self.style.SUCCESS(f'✅ Metodología actualizada a: {metodologia}'))
            else:
                # Crear nuevo proyecto
                proyecto = Proyecto.objects.create(
                    nombre='GRCU Manager - Sistema de Gestión de Requerimientos',
                    descripcion='Sistema web para gestionar requerimientos y casos de uso de proyectos de software',
                    lider=lider,
                    metodologia=metodologia,
                    activo=True
                )
                self.stdout.write(self.style.SUCCESS(f'✅ Proyecto creado: {proyecto.nombre}'))
        
        # Obtener usuario creador
        creador = proyecto.lider
        
        # Limpiar requerimientos anteriores del proyecto (opcional)
        reqs_existentes = Requerimiento.objects.filter(proyecto=proyecto).count()
        if reqs_existentes > 0:
            self.stdout.write(self.style.WARNING(f'⚠️  El proyecto ya tiene {reqs_existentes} requerimientos'))
            # No eliminamos, solo agregamos
        
        self.stdout.write(self.style.SUCCESS(f'\n📋 Creando 20 requerimientos con metodología {metodologia}...\n'))
        
        if metodologia == 'TRADICIONAL':
            requerimientos_creados = self._crear_requerimientos_tradicionales(proyecto, creador)
        else:
            requerimientos_creados = self._crear_requerimientos_agiles(proyecto, creador)
        
        self.stdout.write(self.style.SUCCESS(f'\n✅ Se crearon {len(requerimientos_creados)} requerimientos exitosamente'))
        self.stdout.write(self.style.SUCCESS('=' * 70))
        self.stdout.write(self.style.SUCCESS(f'Proyecto: {proyecto.nombre}'))
        self.stdout.write(self.style.SUCCESS(f'Metodología: {proyecto.get_metodologia_display()}'))
        self.stdout.write(self.style.SUCCESS(f'Total requerimientos: {Requerimiento.objects.filter(proyecto=proyecto).count()}'))
        self.stdout.write(self.style.SUCCESS('=' * 70))

    def _crear_requerimientos_tradicionales(self, proyecto, creador):
        """Crea 20 requerimientos con metodología tradicional"""
        
        requerimientos_data = [
            # Funcionales - Gestión de Usuarios (5)
            {
                'nombre': 'Autenticación de usuarios',
                'descripcion': 'El sistema debe permitir a los usuarios autenticarse mediante usuario y contraseña',
                'tipo': 'FUNCIONAL',
                'estado': 'APROBADO',
                'prioridad': 'MUST',
                'fuente': 'Gerente de Proyecto',
                'categoria': 'Seguridad',
                'fecha_compromiso': timezone.now().date() + timedelta(days=30),
                'estado_validacion': 'VALIDADO'
            },
            {
                'nombre': 'Registro de nuevos usuarios',
                'descripcion': 'El sistema debe permitir el registro de nuevos usuarios con validación de email',
                'tipo': 'FUNCIONAL',
                'estado': 'EN_DESARROLLO',
                'prioridad': 'MUST',
                'fuente': 'Product Owner',
                'categoria': 'Gestión de Usuarios',
                'fecha_compromiso': timezone.now().date() + timedelta(days=25),
                'estado_validacion': 'EN_REVISION'
            },
            {
                'nombre': 'Gestión de roles y permisos',
                'descripcion': 'El sistema debe permitir asignar roles (Líder, Developer, Tester) y gestionar permisos',
                'tipo': 'FUNCIONAL',
                'estado': 'APROBADO',
                'prioridad': 'MUST',
                'fuente': 'Equipo de Seguridad',
                'categoria': 'Seguridad',
                'fecha_compromiso': timezone.now().date() + timedelta(days=35),
                'estado_validacion': 'VALIDADO'
            },
            {
                'nombre': 'Recuperación de contraseña',
                'descripcion': 'El sistema debe permitir a los usuarios recuperar su contraseña vía email',
                'tipo': 'FUNCIONAL',
                'estado': 'PENDIENTE',
                'prioridad': 'SHOULD',
                'fuente': 'Soporte Técnico',
                'categoria': 'Seguridad',
                'fecha_compromiso': timezone.now().date() + timedelta(days=45),
                'estado_validacion': 'PENDIENTE'
            },
            {
                'nombre': 'Perfil de usuario',
                'descripcion': 'Los usuarios deben poder ver y editar su información de perfil',
                'tipo': 'FUNCIONAL',
                'estado': 'EN_DESARROLLO',
                'prioridad': 'SHOULD',
                'fuente': 'Usuarios Finales',
                'categoria': 'Gestión de Usuarios',
                'fecha_compromiso': timezone.now().date() + timedelta(days=40),
                'estado_validacion': 'EN_REVISION'
            },
            
            # Funcionales - Gestión de Proyectos (5)
            {
                'nombre': 'Crear proyecto',
                'descripcion': 'El líder debe poder crear nuevos proyectos con nombre, descripción y metodología',
                'tipo': 'FUNCIONAL',
                'estado': 'APROBADO',
                'prioridad': 'MUST',
                'fuente': 'Gerente de Proyecto',
                'categoria': 'Gestión de Proyectos',
                'fecha_compromiso': timezone.now().date() + timedelta(days=20),
                'estado_validacion': 'VALIDADO'
            },
            {
                'nombre': 'Editar proyecto',
                'descripcion': 'El líder debe poder modificar la información de los proyectos existentes',
                'tipo': 'FUNCIONAL',
                'estado': 'APROBADO',
                'prioridad': 'MUST',
                'fuente': 'Gerente de Proyecto',
                'categoria': 'Gestión de Proyectos',
                'fecha_compromiso': timezone.now().date() + timedelta(days=22),
                'estado_validacion': 'VALIDADO'
            },
            {
                'nombre': 'Asignar participantes al proyecto',
                'descripcion': 'El líder debe poder agregar y remover participantes de un proyecto',
                'tipo': 'FUNCIONAL',
                'estado': 'EN_DESARROLLO',
                'prioridad': 'MUST',
                'fuente': 'Gerente de Proyecto',
                'categoria': 'Gestión de Proyectos',
                'fecha_compromiso': timezone.now().date() + timedelta(days=28),
                'estado_validacion': 'EN_REVISION'
            },
            {
                'nombre': 'Dashboard del proyecto',
                'descripcion': 'El sistema debe mostrar un dashboard con métricas y estado del proyecto',
                'tipo': 'FUNCIONAL',
                'estado': 'EN_DESARROLLO',
                'prioridad': 'SHOULD',
                'fuente': 'Product Owner',
                'categoria': 'Visualización',
                'fecha_compromiso': timezone.now().date() + timedelta(days=50),
                'estado_validacion': 'EN_REVISION'
            },
            {
                'nombre': 'Archivo de proyectos',
                'descripcion': 'El sistema debe permitir archivar proyectos completados',
                'tipo': 'FUNCIONAL',
                'estado': 'PENDIENTE',
                'prioridad': 'COULD',
                'fuente': 'Gerente de Proyecto',
                'categoria': 'Gestión de Proyectos',
                'fecha_compromiso': timezone.now().date() + timedelta(days=60),
                'estado_validacion': 'PENDIENTE'
            },
            
            # Funcionales - Gestión de Requerimientos (5)
            {
                'nombre': 'Crear requerimiento funcional',
                'descripcion': 'El sistema debe permitir crear requerimientos funcionales con todos sus atributos',
                'tipo': 'FUNCIONAL',
                'estado': 'APROBADO',
                'prioridad': 'MUST',
                'fuente': 'Analista de Requerimientos',
                'categoria': 'Gestión de Requerimientos',
                'fecha_compromiso': timezone.now().date() + timedelta(days=15),
                'estado_validacion': 'VALIDADO'
            },
            {
                'nombre': 'Priorización MoSCoW',
                'descripcion': 'El líder debe poder priorizar requerimientos usando el método MoSCoW',
                'tipo': 'FUNCIONAL',
                'estado': 'APROBADO',
                'prioridad': 'MUST',
                'fuente': 'Product Owner',
                'categoria': 'Gestión de Requerimientos',
                'fecha_compromiso': timezone.now().date() + timedelta(days=18),
                'estado_validacion': 'VALIDADO'
            },
            {
                'nombre': 'Trazabilidad requerimiento-caso de uso',
                'descripcion': 'El sistema debe permitir vincular requerimientos con casos de uso',
                'tipo': 'FUNCIONAL',
                'estado': 'EN_DESARROLLO',
                'prioridad': 'MUST',
                'fuente': 'Analista de Requerimientos',
                'categoria': 'Trazabilidad',
                'fecha_compromiso': timezone.now().date() + timedelta(days=35),
                'estado_validacion': 'EN_REVISION'
            },
            {
                'nombre': 'Historial de cambios de requerimientos',
                'descripcion': 'El sistema debe registrar todos los cambios realizados a los requerimientos',
                'tipo': 'FUNCIONAL',
                'estado': 'PENDIENTE',
                'prioridad': 'SHOULD',
                'fuente': 'Auditoría',
                'categoria': 'Auditoría',
                'fecha_compromiso': timezone.now().date() + timedelta(days=55),
                'estado_validacion': 'PENDIENTE'
            },
            {
                'nombre': 'Exportar requerimientos a PDF',
                'descripcion': 'El sistema debe permitir exportar la lista de requerimientos a formato PDF',
                'tipo': 'FUNCIONAL',
                'estado': 'PENDIENTE',
                'prioridad': 'COULD',
                'fuente': 'Usuarios Finales',
                'categoria': 'Reportes',
                'fecha_compromiso': timezone.now().date() + timedelta(days=70),
                'estado_validacion': 'PENDIENTE'
            },
            
            # No Funcionales (5)
            {
                'nombre': 'Tiempo de respuesta',
                'descripcion': 'El sistema debe responder a las peticiones del usuario en menos de 2 segundos',
                'tipo': 'NO_FUNCIONAL',
                'estado': 'APROBADO',
                'prioridad': 'MUST',
                'fuente': 'Arquitecto de Software',
                'categoria': 'Performance',
                'fecha_compromiso': timezone.now().date() + timedelta(days=40),
                'estado_validacion': 'VALIDADO'
            },
            {
                'nombre': 'Compatibilidad con navegadores',
                'descripcion': 'El sistema debe ser compatible con Chrome, Firefox, Safari y Edge (últimas 2 versiones)',
                'tipo': 'NO_FUNCIONAL',
                'estado': 'APROBADO',
                'prioridad': 'MUST',
                'fuente': 'Arquitecto de Software',
                'categoria': 'Compatibilidad',
                'fecha_compromiso': timezone.now().date() + timedelta(days=30),
                'estado_validacion': 'VALIDADO'
            },
            {
                'nombre': 'Diseño responsive',
                'descripcion': 'La interfaz debe adaptarse a dispositivos móviles, tablets y escritorio',
                'tipo': 'NO_FUNCIONAL',
                'estado': 'EN_DESARROLLO',
                'prioridad': 'SHOULD',
                'fuente': 'UX Designer',
                'categoria': 'Usabilidad',
                'fecha_compromiso': timezone.now().date() + timedelta(days=45),
                'estado_validacion': 'EN_REVISION'
            },
            {
                'nombre': 'Seguridad de datos',
                'descripcion': 'Todos los datos sensibles deben ser encriptados en tránsito y en reposo',
                'tipo': 'NO_FUNCIONAL',
                'estado': 'APROBADO',
                'prioridad': 'MUST',
                'fuente': 'Oficial de Seguridad',
                'categoria': 'Seguridad',
                'fecha_compromiso': timezone.now().date() + timedelta(days=25),
                'estado_validacion': 'VALIDADO'
            },
            {
                'nombre': 'Disponibilidad del sistema',
                'descripcion': 'El sistema debe tener una disponibilidad mínima del 99.5% mensual',
                'tipo': 'NO_FUNCIONAL',
                'estado': 'PENDIENTE',
                'prioridad': 'SHOULD',
                'fuente': 'Operations',
                'categoria': 'Disponibilidad',
                'fecha_compromiso': timezone.now().date() + timedelta(days=60),
                'estado_validacion': 'PENDIENTE'
            },
        ]
        
        requerimientos_creados = []
        
        for idx, data in enumerate(requerimientos_data, 1):
            # Crear requerimiento base
            req = Requerimiento.objects.create(
                nombre=data['nombre'],
                descripcion=data['descripcion'],
                tipo=data['tipo'],
                estado=data['estado'],
                proyecto=proyecto,
                creado_por=creador
            )
            
            # Crear detalle tradicional
            DetalleRequerimientoTradicional.objects.create(
                requerimiento_padre=req,
                prioridad=data['prioridad'],
                fuente=data['fuente'],
                categoria=data['categoria'],
                fecha_compromiso=data['fecha_compromiso'],
                estado_validacion=data['estado_validacion'],
                observaciones=f'Requerimiento cargado automáticamente por el sistema de seed'
            )
            
            requerimientos_creados.append(req)
            self.stdout.write(f'  {idx}. ✅ {req.nombre} [{data["prioridad"]}]')
        
        return requerimientos_creados

    def _crear_requerimientos_agiles(self, proyecto, creador):
        """Crea 20 requerimientos con metodología ágil (User Stories)"""
        
        user_stories_data = [
            # Epic: Gestión de Usuarios
            {
                'nombre': 'Login de usuario',
                'descripcion': 'Funcionalidad de autenticación en el sistema',
                'tipo': 'FUNCIONAL',
                'estado': 'COMPLETADO',
                'historia': 'Como usuario registrado, quiero poder iniciar sesión con mi email y contraseña para acceder al sistema',
                'criterios': '- El usuario ingresa email y contraseña\n- El sistema valida las credenciales\n- Si son correctas, el usuario accede al dashboard\n- Si son incorrectas, se muestra un mensaje de error',
                'puntos': 5,
                'sprint': 'Sprint 1',
                'responsable': 'Backend Team',
                'estado_scrum': 'DONE'
            },
            {
                'nombre': 'Registro de usuario',
                'descripcion': 'Crear cuenta nueva en el sistema',
                'tipo': 'FUNCIONAL',
                'estado': 'COMPLETADO',
                'historia': 'Como nuevo usuario, quiero registrarme con mi email para poder usar el sistema',
                'criterios': '- Formulario con nombre, email, contraseña\n- Validación de email único\n- Confirmación por email\n- Creación de cuenta exitosa',
                'puntos': 8,
                'sprint': 'Sprint 1',
                'responsable': 'Backend Team',
                'estado_scrum': 'DONE'
            },
            {
                'nombre': 'Recuperar contraseña',
                'descripcion': 'Recuperación de acceso cuando olvida la contraseña',
                'tipo': 'FUNCIONAL',
                'estado': 'EN_DESARROLLO',
                'historia': 'Como usuario, quiero recuperar mi contraseña mediante mi email para poder acceder nuevamente',
                'criterios': '- Botón "Olvidé mi contraseña"\n- Envío de email con token\n- Formulario para nueva contraseña\n- Actualización exitosa',
                'puntos': 5,
                'sprint': 'Sprint 2',
                'responsable': 'Backend Team',
                'estado_scrum': 'IN_PROGRESS'
            },
            {
                'nombre': 'Editar perfil',
                'descripcion': 'Actualizar información personal del usuario',
                'tipo': 'FUNCIONAL',
                'estado': 'PENDIENTE',
                'historia': 'Como usuario, quiero editar mi información de perfil para mantener mis datos actualizados',
                'criterios': '- Formulario con datos actuales\n- Validación de campos\n- Actualización en base de datos\n- Mensaje de confirmación',
                'puntos': 3,
                'sprint': 'Sprint 2',
                'responsable': 'Frontend Team',
                'estado_scrum': 'TODO'
            },
            
            # Epic: Gestión de Proyectos
            {
                'nombre': 'Crear proyecto',
                'descripcion': 'Iniciar un nuevo proyecto en el sistema',
                'tipo': 'FUNCIONAL',
                'estado': 'COMPLETADO',
                'historia': 'Como líder, quiero crear un nuevo proyecto con nombre y descripción para comenzar a gestionarlo',
                'criterios': '- Formulario de creación\n- Campos: nombre, descripción, metodología, fecha inicio\n- Asignación automática como líder\n- Redirección al dashboard del proyecto',
                'puntos': 8,
                'sprint': 'Sprint 1',
                'responsable': 'Full Stack Team',
                'estado_scrum': 'DONE'
            },
            {
                'nombre': 'Editar proyecto',
                'descripcion': 'Modificar información de proyecto existente',
                'tipo': 'FUNCIONAL',
                'estado': 'COMPLETADO',
                'historia': 'Como líder, quiero editar la información de mi proyecto para mantenerla actualizada',
                'criterios': '- Acceso solo para líder\n- Formulario pre-llenado\n- Validación de cambios\n- Actualización exitosa',
                'puntos': 5,
                'sprint': 'Sprint 1',
                'responsable': 'Full Stack Team',
                'estado_scrum': 'DONE'
            },
            {
                'nombre': 'Agregar participantes',
                'descripcion': 'Invitar miembros del equipo al proyecto',
                'tipo': 'FUNCIONAL',
                'estado': 'EN_DESARROLLO',
                'historia': 'Como líder, quiero agregar participantes a mi proyecto para que puedan colaborar',
                'criterios': '- Lista de usuarios disponibles\n- Asignación de rol (Developer/Tester)\n- Notificación al usuario agregado\n- Actualización de lista de participantes',
                'puntos': 8,
                'sprint': 'Sprint 2',
                'responsable': 'Backend Team',
                'estado_scrum': 'IN_PROGRESS'
            },
            {
                'nombre': 'Dashboard de proyecto',
                'descripcion': 'Vista general del estado del proyecto',
                'tipo': 'FUNCIONAL',
                'estado': 'EN_DESARROLLO',
                'historia': 'Como líder, quiero ver un dashboard con métricas de mi proyecto para monitorear su progreso',
                'criterios': '- Gráficos de estado de requerimientos\n- Lista de casos de uso\n- Métricas de avance\n- Acciones rápidas',
                'puntos': 13,
                'sprint': 'Sprint 2',
                'responsable': 'Frontend Team',
                'estado_scrum': 'IN_PROGRESS'
            },
            {
                'nombre': 'Archivar proyecto',
                'descripcion': 'Marcar proyecto como finalizado',
                'tipo': 'FUNCIONAL',
                'estado': 'PENDIENTE',
                'historia': 'Como líder, quiero archivar proyectos completados para mantener organizada mi lista',
                'criterios': '- Botón de archivar\n- Confirmación de acción\n- Proyecto no aparece en lista activa\n- Posibilidad de desarchivar',
                'puntos': 3,
                'sprint': 'Sprint 3',
                'responsable': 'Backend Team',
                'estado_scrum': 'TODO'
            },
            
            # Epic: Gestión de Requerimientos
            {
                'nombre': 'Crear requerimiento',
                'descripcion': 'Agregar nuevo requerimiento al proyecto',
                'tipo': 'FUNCIONAL',
                'estado': 'COMPLETADO',
                'historia': 'Como miembro del proyecto, quiero crear requerimientos para documentar las necesidades del sistema',
                'criterios': '- Formulario adaptado a metodología\n- Campos específicos según tipo\n- Validación de datos\n- Creación exitosa',
                'puntos': 8,
                'sprint': 'Sprint 2',
                'responsable': 'Full Stack Team',
                'estado_scrum': 'DONE'
            },
            {
                'nombre': 'Editar requerimiento',
                'descripcion': 'Modificar requerimiento existente',
                'tipo': 'FUNCIONAL',
                'estado': 'EN_DESARROLLO',
                'historia': 'Como miembro del proyecto, quiero editar requerimientos para corregir o actualizar información',
                'criterios': '- Acceso para líder y participantes\n- Formulario pre-llenado\n- Validación de cambios\n- Registro de cambios',
                'puntos': 5,
                'sprint': 'Sprint 3',
                'responsable': 'Full Stack Team',
                'estado_scrum': 'IN_PROGRESS'
            },
            {
                'nombre': 'Listar requerimientos',
                'descripcion': 'Ver todos los requerimientos del proyecto',
                'tipo': 'FUNCIONAL',
                'estado': 'COMPLETADO',
                'historia': 'Como miembro del proyecto, quiero ver la lista de requerimientos para conocer el alcance del sistema',
                'criterios': '- Tabla con todos los requerimientos\n- Filtros por tipo y estado\n- Paginación\n- Enlaces a detalle',
                'puntos': 5,
                'sprint': 'Sprint 2',
                'responsable': 'Frontend Team',
                'estado_scrum': 'DONE'
            },
            {
                'nombre': 'Priorizar requerimientos',
                'descripcion': 'Asignar prioridades a los requerimientos',
                'tipo': 'FUNCIONAL',
                'estado': 'COMPLETADO',
                'historia': 'Como líder, quiero priorizar requerimientos usando MoSCoW para planificar el desarrollo',
                'criterios': '- Solo acceso para líder\n- Drag and drop o select\n- Guardado automático\n- Indicadores visuales',
                'puntos': 8,
                'sprint': 'Sprint 2',
                'responsable': 'Frontend Team',
                'estado_scrum': 'DONE'
            },
            {
                'nombre': 'Vincular con caso de uso',
                'descripcion': 'Establecer trazabilidad entre requerimientos y casos de uso',
                'tipo': 'FUNCIONAL',
                'estado': 'EN_DESARROLLO',
                'historia': 'Como analista, quiero vincular requerimientos con casos de uso para mantener trazabilidad',
                'criterios': '- Selector de casos de uso\n- Relación muchos a muchos\n- Visualización de vínculos\n- Detección de huérfanos',
                'puntos': 13,
                'sprint': 'Sprint 3',
                'responsable': 'Full Stack Team',
                'estado_scrum': 'IN_PROGRESS'
            },
            
            # Epic: Gestión de Casos de Uso
            {
                'nombre': 'Crear caso de uso',
                'descripcion': 'Documentar nuevo caso de uso',
                'tipo': 'FUNCIONAL',
                'estado': 'COMPLETADO',
                'historia': 'Como analista, quiero crear casos de uso para documentar las interacciones del sistema',
                'criterios': '- Formulario con nombre, actores, precondiciones\n- Flujo normal y alternativo\n- Guardado en base de datos\n- Confirmación de creación',
                'puntos': 8,
                'sprint': 'Sprint 2',
                'responsable': 'Full Stack Team',
                'estado_scrum': 'DONE'
            },
            {
                'nombre': 'Matriz de trazabilidad',
                'descripcion': 'Visualizar relaciones entre requerimientos y casos de uso',
                'tipo': 'FUNCIONAL',
                'estado': 'PENDIENTE',
                'historia': 'Como líder, quiero ver una matriz de trazabilidad para validar la cobertura de requerimientos',
                'criterios': '- Matriz visual\n- Filtros por categoría\n- Exportación a Excel\n- Identificación de gaps',
                'puntos': 13,
                'sprint': 'Sprint 4',
                'responsable': 'Full Stack Team',
                'estado_scrum': 'TODO'
            },
            
            # Epic: Reportes y Exportación
            {
                'nombre': 'Exportar a PDF',
                'descripcion': 'Generar documento PDF con requerimientos',
                'tipo': 'FUNCIONAL',
                'estado': 'PENDIENTE',
                'historia': 'Como líder, quiero exportar requerimientos a PDF para compartir con stakeholders',
                'criterios': '- Botón de exportación\n- Generación de PDF\n- Formato profesional\n- Descarga automática',
                'puntos': 8,
                'sprint': 'Sprint 4',
                'responsable': 'Backend Team',
                'estado_scrum': 'TODO'
            },
            {
                'nombre': 'Historial de cambios',
                'descripcion': 'Registro de auditoría de modificaciones',
                'tipo': 'FUNCIONAL',
                'estado': 'PENDIENTE',
                'historia': 'Como líder, quiero ver el historial de cambios de requerimientos para auditoría',
                'criterios': '- Log de todas las modificaciones\n- Usuario y fecha de cambio\n- Valores anteriores y nuevos\n- Filtros por fecha',
                'puntos': 13,
                'sprint': 'Sprint 4',
                'responsable': 'Backend Team',
                'estado_scrum': 'TODO'
            },
            
            # Técnicas
            {
                'nombre': 'Performance del sistema',
                'descripcion': 'Optimización de tiempos de respuesta',
                'tipo': 'NO_FUNCIONAL',
                'estado': 'EN_DESARROLLO',
                'historia': 'Como usuario, quiero que el sistema responda rápido para tener una buena experiencia',
                'criterios': '- Tiempo de carga < 2 segundos\n- Queries optimizadas\n- Caché implementado\n- Medición de performance',
                'puntos': 13,
                'sprint': 'Sprint 3',
                'responsable': 'Backend Team',
                'estado_scrum': 'IN_PROGRESS'
            },
            {
                'nombre': 'Diseño responsive',
                'descripcion': 'Adaptación a todos los dispositivos',
                'tipo': 'NO_FUNCIONAL',
                'estado': 'EN_DESARROLLO',
                'historia': 'Como usuario móvil, quiero que el sistema se adapte a mi pantalla para usarlo cómodamente',
                'criterios': '- Breakpoints definidos\n- Pruebas en móvil/tablet/desktop\n- Bootstrap responsive\n- Navegación táctil',
                'puntos': 8,
                'sprint': 'Sprint 3',
                'responsable': 'Frontend Team',
                'estado_scrum': 'IN_PROGRESS'
            },
        ]
        
        requerimientos_creados = []
        
        for idx, data in enumerate(user_stories_data, 1):
            # Crear requerimiento base
            req = Requerimiento.objects.create(
                nombre=data['nombre'],
                descripcion=data['descripcion'],
                tipo=data['tipo'],
                estado=data['estado'],
                proyecto=proyecto,
                creado_por=creador
            )
            
            # Crear detalle ágil
            DetalleRequerimientoAgil.objects.create(
                requerimiento_padre=req,
                historia_usuario=data['historia'],
                criterio_aceptacion=data['criterios'],
                puntos_estimados=data['puntos'],
                sprint_asignado=data['sprint'],
                responsable=data['responsable'],
                estado_scrum=data['estado_scrum'],
                observaciones=f'User Story cargada automáticamente por el sistema de seed'
            )
            
            requerimientos_creados.append(req)
            self.stdout.write(f'  {idx}. ✅ {req.nombre} [{data["puntos"]} pts - {data["sprint"]}]')
        
        return requerimientos_creados
