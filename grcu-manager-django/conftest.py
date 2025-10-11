import pytest

PROYECTO = "GRCU Manager"
GRUPO = "4Bytes"
UNIVERSIDAD = "Universidad Nacional de la Patagonia Austral"
MATERIA = "Laboratorio de Desarrollo de Software 2025"
DOCENTES = "Mg. Osiris Sofia - Lic. Karim Hallar - Lic. Esteban Gesto"
TESTER = "Martina Gagna"

def pytest_sessionstart(session):
    print("\n==============================")
    print(f"Proyecto: {PROYECTO}")
    print(f"Grupo: {GRUPO}")
    print(f"Universidad: {UNIVERSIDAD}")
    print(f"Materia: {MATERIA}")
    print(f"Docentes: {DOCENTES}")
    print(f"Tester: {TESTER}")
    print("==============================\n")
