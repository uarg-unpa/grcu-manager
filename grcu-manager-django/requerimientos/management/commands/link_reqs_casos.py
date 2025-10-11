from django.core.management.base import BaseCommand
from requerimientos.models import Requerimiento, RequerimientoCaso
from casos_de_uso.models import CasoDeUso
from django.db import transaction

class Command(BaseCommand):
    help = 'Relaciona requerimientos y casos de uso: crea 6 relaciones y deja 3 requerimientos y 1 caso huérfanos (ajusta si no hay suficientes registros).'

    def handle(self, *args, **options):
        reqs = list(Requerimiento.objects.all())
        casos = list(CasoDeUso.objects.all())

        total_reqs = len(reqs)
        total_casos = len(casos)

        if total_reqs == 0 or total_casos == 0:
            self.stdout.write(self.style.ERROR('No hay requerimientos o casos de uso en la base de datos.'))
            return

        # Deseamos exactamente 6 relaciones (pares req<->caso) en total.
        # También queremos dejar 3 requerimientos sin relacionar y 1 caso sin relacionar.
        # Si no hay suficientes objetos ajustamos en función de lo disponible.

        desired_relations = 6
        desired_orphan_reqs = 3
        desired_orphan_casos = 1

        # Limpiar relaciones previas en la tabla intermedia
        RequerimientoCaso.objects.all().delete()

        # Strategy: emparejar en round-robin hasta desired_relations
        relations_created = 0
        ri = 0
        ci = 0

        # Pre-calc maximum possible relations without making all linked
        max_possible = min(total_reqs * total_casos, desired_relations)

        with transaction.atomic():
            while relations_created < max_possible:
                req = reqs[ri % total_reqs]
                caso = casos[ci % total_casos]
                # Evitar duplicados (consultar la tabla intermedia directamente)
                if not RequerimientoCaso.objects.filter(requerimiento=req, caso_de_uso=caso).exists():
                    RequerimientoCaso.objects.create(requerimiento=req, caso_de_uso=caso)
                    relations_created += 1
                ri += 1
                ci += 1

        # Ahora forzamos huérfanos si hay suficientes
        # Aseguramos que al menos desired_orphan_reqs reqs tengan 0 relaciones
        # Requerimientos huérfanos: aquellos sin filas en la tabla intermedia
        orphan_reqs = [r for r in Requerimiento.objects.all() if RequerimientoCaso.objects.filter(requerimiento=r).count() == 0]
        if len(orphan_reqs) < desired_orphan_reqs:
            # quitamos relaciones de algunos requerimientos con más de 1 relación
            candidates = [r for r in Requerimiento.objects.all() if RequerimientoCaso.objects.filter(requerimiento=r).count() > 0]
            idx = 0
            while len(orphan_reqs) < desired_orphan_reqs and idx < len(candidates):
                r = candidates[idx]
                # eliminar relaciones de este requerimiento en la tabla intermedia
                RequerimientoCaso.objects.filter(requerimiento=r).delete()
                orphan_reqs.append(r)
                idx += 1

        # Asegurar al menos desired_orphan_casos casos sin relaciones
        # Casos huérfanos: aquellos sin filas en la tabla intermedia
        orphan_casos = [c for c in CasoDeUso.objects.all() if RequerimientoCaso.objects.filter(caso_de_uso=c).count() == 0]
        if len(orphan_casos) < desired_orphan_casos:
            candidates = [c for c in CasoDeUso.objects.all() if RequerimientoCaso.objects.filter(caso_de_uso=c).count() > 0]
            idx = 0
            while len(orphan_casos) < desired_orphan_casos and idx < len(candidates):
                c = candidates[idx]
                # quitar todas las relaciones de este caso (tabla intermedia)
                RequerimientoCaso.objects.filter(caso_de_uso=c).delete()
                orphan_casos.append(c)
                idx += 1

        # Informar del resultado
        # contar filas en la tabla intermedia
        total_links = RequerimientoCaso.objects.count()
        self.stdout.write(self.style.SUCCESS(f'Relations created (total links): {total_links}'))
        self.stdout.write(self.style.SUCCESS(f'Total requerimientos: {Requerimiento.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Total casos de uso: {CasoDeUso.objects.count()}'))
        orphan_reqs_count = Requerimiento.objects.filter(relaciones_casos__isnull=True).count()
        orphan_casos_count = CasoDeUso.objects.filter(relaciones_requerimientos__isnull=True).count()
        self.stdout.write(self.style.SUCCESS(f'Requerimientos huérfanos: {orphan_reqs_count}'))
        self.stdout.write(self.style.SUCCESS(f'Casos huérfanos: {orphan_casos_count}'))

