import requests

BASE_URL = "http://localhost:8000/api"

def test_get_jugadores_success():
    response = requests.get(f"{BASE_URL}/jugador/")
    assert response.status_code == 200
    jugadores = response.json()
    longitud=len(jugadores)
    assert len(jugadores)==longitud


def test_get_jugadores_por_id():
    id=3
    response = requests.get(f"{BASE_URL}/jugador/{id}")
    assert response.status_code == 200
    jugador=response.json()
    assert jugador['username']=="MAUBRY"

def test_post_agregar_jugador():
    nuevo_jugador = {
        "username": "TESTUSER2",
        "fecha_nacimiento": "2010-01-01",
    }
    response2=requests.get(f"{BASE_URL}/jugador/")
    longitud_inicial=len(response2.json())
    response = requests.post(f"{BASE_URL}/jugador/", json=nuevo_jugador)
    response3=requests.get(f"{BASE_URL}/jugador/")
    assert response.status_code == 201
    assert response2.status_code==200
    assert len(response3.json())>longitud_inicial
    
