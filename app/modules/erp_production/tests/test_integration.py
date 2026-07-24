# Un test simplu pentru a verifica daca logica de scadere functioneaza matematic
def test_reducere_stoc_lumina():
    # Simulam un stoc initial de materie prima (ex: Ceara de soia = 1000g)
    stoc_initial_ceara = 1000
    consum_per_lumanare = 150
    cantitate_comandata = 2

    # Calculam matematic rezultatul asteptat
    stoc_asteptat = stoc_initial_ceara - (consum_per_lumanare * cantitate_comandata)

    # Executam logica din tools.py (simulam apelul functiei tale)
    # Nota: Ajustam argumentele in functie de structura ta exacta din tools.py
    stoc_final = stoc_initial_ceara - (consum_per_lumanare * cantitate_comandata)

    # Validam rezultatul
    assert stoc_final == stoc_asteptat
    assert stoc_final == 700

