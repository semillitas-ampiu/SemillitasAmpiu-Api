import requests

BASE_URL = "http://localhost:8000/api"

def test_agregar_ejecicio():
    nuevo_ejercicio = {
        "ejercicio":1,
        "palabra":2,
    }
    response2 = requests.get(f"{BASE_URL}/ejercicio/")
    longitud_inicial = len(response2.json())
    response = requests.post(f"{BASE_URL}/ejercicio/", json=nuevo_ejercicio)
    response3 = requests.get(f"{BASE_URL}/ejercicio/")
    assert response.status_code == 201
    assert response2.status_code == 200
    assert len(response3.json()) > longitud_inicial
    
