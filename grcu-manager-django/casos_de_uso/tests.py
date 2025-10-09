from django.test import TestCase
from .models import CasoDeUso

class CasoDeUsoModelTest(TestCase):
    def test_str(self):
        caso = CasoDeUso(nombre="Caso test")
        self.assertEqual(str(caso), "Caso test")
