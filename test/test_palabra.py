"""
Tests para el endpoint de palabras (/api/palabra/)
Casos: P01-P10
"""
import requests
import pytest
import time

BASE_URL = "http://localhost:8000/api"


def get_timestamp():
    return str(int(time.time() * 1000))


class TestPalabraList:
    """Tests para GET y POST /api/palabra/"""
    
    def test_P01_listar_palabras(self):
        """P01: GET /palabra/ retorna lista de palabras"""
        response = requests.get(f"{BASE_URL}/palabra/")
        
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_P02_crear_palabra_completa(self, palabra_data):
        """P02: Crear palabra con pal_español, pal_ampiu y nivel retorna 201"""
        response = requests.post(f"{BASE_URL}/palabra/", json=palabra_data)
        
        assert response.status_code == 201
        data = response.json()
        assert "mensaje" in data
        assert data["mensaje"] == "Palabra creada correctamente."
        assert "data" in data
    
    def test_P03_crear_palabra_sin_nivel(self):
        """P03: Crear palabra sin nivel retorna 400"""
        ts = get_timestamp()
        palabra_sin_nivel = {
            "pal_español": f"español_{ts}",
            "pal_ampiu": f"ampiu_{ts}"
        }
        
        response = requests.post(f"{BASE_URL}/palabra/", json=palabra_sin_nivel)
        
        assert response.status_code == 400
    
    def test_P04_crear_palabra_nivel_inexistente(self):
        """P04: Crear palabra con nivel inexistente retorna 400"""
        ts = get_timestamp()
        palabra_nivel_invalido = {
            "pal_español": f"español_{ts}",
            "pal_ampiu": f"ampiu_{ts}",
            "nivel": 99999
        }
        
        response = requests.post(f"{BASE_URL}/palabra/", json=palabra_nivel_invalido)
        
        assert response.status_code == 400
    
    def test_P05_crear_palabra_español_duplicado(self, palabra_data, nivel_id):
        """P05: Crear palabra con pal_español duplicado retorna 400"""
        # Crear primera palabra
        response1 = requests.post(f"{BASE_URL}/palabra/", json=palabra_data)
        assert response1.status_code == 201
        
        # Intentar crear segunda con mismo pal_español
        ts = get_timestamp()
        palabra_duplicada = {
            "pal_español": palabra_data["pal_español"],  # Mismo español
            "pal_ampiu": f"ampiu_diferente_{ts}",
            "nivel": nivel_id
        }
        
        response2 = requests.post(f"{BASE_URL}/palabra/", json=palabra_duplicada)
        
        assert response2.status_code == 400
    
    def test_P06_crear_palabra_ampiu_duplicado(self, palabra_data, nivel_id):
        """P06: Crear palabra con pal_ampiu duplicado retorna 400"""
        # Crear primera palabra
        response1 = requests.post(f"{BASE_URL}/palabra/", json=palabra_data)
        assert response1.status_code == 201
        
        # Intentar crear segunda con mismo pal_ampiu
        ts = get_timestamp()
        palabra_duplicada = {
            "pal_español": f"español_diferente_{ts}",
            "pal_ampiu": palabra_data["pal_ampiu"],  # Mismo ampiu
            "nivel": nivel_id
        }
        
        response2 = requests.post(f"{BASE_URL}/palabra/", json=palabra_duplicada)
        
        assert response2.status_code == 400


class TestPalabraDetail:
    """Tests para GET, PUT, DELETE /api/palabra/<id>"""
    
    def test_P07_obtener_palabra_por_id_valido(self, crear_palabra):
        """P07: GET /palabra/<id> con ID válido retorna 200"""
        palabra_id = crear_palabra["id"]
        
        response = requests.get(f"{BASE_URL}/palabra/{palabra_id}")
        
        assert response.status_code == 200
        assert response.json()["id"] == palabra_id
    
    def test_P08_obtener_palabra_por_id_invalido(self):
        """P08: GET /palabra/<id> con ID inexistente retorna 404"""
        response = requests.get(f"{BASE_URL}/palabra/99999")
        
        assert response.status_code == 404
    
    def test_P09_actualizar_palabra(self, crear_palabra, nivel_id):
        """P09: PUT /palabra/<id> actualiza datos correctamente"""
        palabra_id = crear_palabra["id"]
        ts = get_timestamp()
        
        updated_data = {
            "pal_español": f"español_updated_{ts}",
            "pal_ampiu": f"ampiu_updated_{ts}",
            "nivel": nivel_id
        }
        
        response = requests.put(f"{BASE_URL}/palabra/{palabra_id}", json=updated_data)
        
        assert response.status_code == 200
        assert response.json()["pal_español"] == updated_data["pal_español"]
    
    def test_P10_eliminar_palabra(self, palabra_data):
        """P10: DELETE /palabra/<id> elimina correctamente"""
        # Crear palabra
        create_response = requests.post(f"{BASE_URL}/palabra/", json=palabra_data)
        assert create_response.status_code == 201
        palabra_id = create_response.json()["data"]["id"]
        
        # Eliminar
        response = requests.delete(f"{BASE_URL}/palabra/{palabra_id}")
        
        assert response.status_code == 204
        
        # Verificar que no existe
        get_response = requests.get(f"{BASE_URL}/palabra/{palabra_id}")
        assert get_response.status_code == 404
