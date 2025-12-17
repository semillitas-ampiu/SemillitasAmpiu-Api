"""
Tests para el endpoint de recolección (/api/recoleccion/)
Casos: R01-R10
"""
import requests
import pytest
import time

BASE_URL = "http://localhost:8000/api"


def get_timestamp():
    return str(int(time.time() * 1000))


class TestRecoleccionList:
    """Tests para GET y POST /api/recoleccion/"""
    
    def test_R01_listar_recolecciones(self):
        """R01: GET /recoleccion/ retorna lista de recolecciones"""
        response = requests.get(f"{BASE_URL}/recoleccion/")
        
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_R02_crear_recoleccion(self, crear_jugador, crear_palabra):
        """R02: Crear recolección con usuario y palabra retorna 201"""
        recoleccion_data = {
            "usuario": crear_jugador["id"],
            "palabra": crear_palabra["id"]
        }
        
        response = requests.post(f"{BASE_URL}/recoleccion/", json=recoleccion_data)
        
        assert response.status_code == 201
        data = response.json()
        assert "mensaje" in data
        assert data["mensaje"] == "Recoleccion creado correctamente."
    
    def test_R03_crear_recoleccion_duplicada(self, crear_jugador, crear_palabra):
        """R03: Crear recolección duplicada (mismo usuario+palabra) retorna 400"""
        recoleccion_data = {
            "usuario": crear_jugador["id"],
            "palabra": crear_palabra["id"]
        }
        
        # Crear primera recolección
        response1 = requests.post(f"{BASE_URL}/recoleccion/", json=recoleccion_data)
        assert response1.status_code == 201
        
        # Intentar crear duplicada
        response2 = requests.post(f"{BASE_URL}/recoleccion/", json=recoleccion_data)
        
        assert response2.status_code == 400
    
    def test_R04_crear_recoleccion_usuario_inexistente(self, crear_palabra):
        """R04: Crear recolección con usuario inexistente retorna 400"""
        recoleccion_data = {
            "usuario": 99999,
            "palabra": crear_palabra["id"]
        }
        
        response = requests.post(f"{BASE_URL}/recoleccion/", json=recoleccion_data)
        
        assert response.status_code == 400
    
    def test_R05_crear_recoleccion_palabra_inexistente(self, crear_jugador):
        """R05: Crear recolección con palabra inexistente retorna 400"""
        recoleccion_data = {
            "usuario": crear_jugador["id"],
            "palabra": 99999
        }
        
        response = requests.post(f"{BASE_URL}/recoleccion/", json=recoleccion_data)
        
        assert response.status_code == 400


class TestRecoleccionDetail:
    """Tests para GET y DELETE /api/recoleccion/<id>"""
    
    def test_R06_obtener_recoleccion_por_id(self, crear_jugador, crear_palabra):
        """R06: GET /recoleccion/<id> con ID válido retorna 200"""
        # Crear recolección
        recoleccion_data = {
            "usuario": crear_jugador["id"],
            "palabra": crear_palabra["id"]
        }
        create_response = requests.post(f"{BASE_URL}/recoleccion/", json=recoleccion_data)
        assert create_response.status_code == 201
        recoleccion_id = create_response.json()["data"]["id"]
        
        # Obtener por ID
        response = requests.get(f"{BASE_URL}/recoleccion/{recoleccion_id}")
        
        assert response.status_code == 200
        assert response.json()["id"] == recoleccion_id
    
    def test_R10_eliminar_recoleccion(self, crear_jugador, crear_palabra):
        """R10: DELETE /recoleccion/<id> elimina correctamente"""
        # Crear recolección
        recoleccion_data = {
            "usuario": crear_jugador["id"],
            "palabra": crear_palabra["id"]
        }
        create_response = requests.post(f"{BASE_URL}/recoleccion/", json=recoleccion_data)
        assert create_response.status_code == 201
        recoleccion_id = create_response.json()["data"]["id"]
        
        # Eliminar
        response = requests.delete(f"{BASE_URL}/recoleccion/{recoleccion_id}")
        
        assert response.status_code == 204
        
        # Verificar que no existe
        get_response = requests.get(f"{BASE_URL}/recoleccion/{recoleccion_id}")
        assert get_response.status_code == 404


class TestRecoleccionFiltros:
    """Tests para los filtros de django-filter en recolección"""
    
    def test_R07_filtrar_por_usuario(self, crear_jugador, crear_palabra):
        """R07: GET /recoleccion/?usuario=X filtra por usuario"""
        # Crear recolección
        recoleccion_data = {
            "usuario": crear_jugador["id"],
            "palabra": crear_palabra["id"]
        }
        requests.post(f"{BASE_URL}/recoleccion/", json=recoleccion_data)
        
        # Filtrar por usuario
        response = requests.get(f"{BASE_URL}/recoleccion/?usuario={crear_jugador['id']}")
        
        assert response.status_code == 200
        recolecciones = response.json()
        assert isinstance(recolecciones, list)
        # Todas las recolecciones retornadas deben ser del usuario
        for rec in recolecciones:
            assert rec["usuario"] == crear_jugador["id"]
    
    def test_R08_filtrar_por_palabra(self, crear_jugador, crear_palabra):
        """R08: GET /recoleccion/?palabra=X filtra por palabra"""
        # Crear recolección
        recoleccion_data = {
            "usuario": crear_jugador["id"],
            "palabra": crear_palabra["id"]
        }
        requests.post(f"{BASE_URL}/recoleccion/", json=recoleccion_data)
        
        # Filtrar por palabra
        response = requests.get(f"{BASE_URL}/recoleccion/?palabra={crear_palabra['id']}")
        
        assert response.status_code == 200
        recolecciones = response.json()
        assert isinstance(recolecciones, list)
        # Todas las recolecciones retornadas deben ser de la palabra
        for rec in recolecciones:
            assert rec["palabra"] == crear_palabra["id"]
    
    def test_R09_filtrar_por_usuario_y_palabra(self, crear_jugador, crear_palabra):
        """R09: GET /recoleccion/?usuario=X&palabra=Y filtra por ambos"""
        # Crear recolección
        recoleccion_data = {
            "usuario": crear_jugador["id"],
            "palabra": crear_palabra["id"]
        }
        create_response = requests.post(f"{BASE_URL}/recoleccion/", json=recoleccion_data)
        assert create_response.status_code == 201
        
        # Filtrar por ambos
        response = requests.get(
            f"{BASE_URL}/recoleccion/?usuario={crear_jugador['id']}&palabra={crear_palabra['id']}"
        )
        
        assert response.status_code == 200
        recolecciones = response.json()
        assert isinstance(recolecciones, list)
        assert len(recolecciones) >= 1
        # Verificar que la recolección específica está
        assert any(
            r["usuario"] == crear_jugador["id"] and r["palabra"] == crear_palabra["id"]
            for r in recolecciones
        )
