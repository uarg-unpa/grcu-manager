from django.test import TestCase
from .models import Requerimiento

class RequerimientoModelTest(TestCase):
    def test_str(self):
        req = Requerimiento(nombre="Req test", tipo="FUNCIONAL", estado="PENDIENTE")
        self.assertEqual(str(req), "Req test")
