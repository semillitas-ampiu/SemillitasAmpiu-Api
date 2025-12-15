"""
Tests para el endpoint de jugadores (/api/jugador/)
Casos: J01-J10
"""
import requests
import pytest
import time

BASE_URL = "http://localhost:8000/api"


def get_timestamp():
    return str(int(time.time() * 1000))


class TestJugadorList:
    """Tests para GET y POST /api/jugador/"""
    
    def test_J01_listar_jugadores(self):
        """J01: GET /jugador/ retorna lista de jugadores"""
        response = requests.get(f"{BASE_URL}/jugador/")
        
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_J02_crear_jugador_datos_completos(self, jugador_con_password_data):
        """J02: Crear jugador con username, fecha_nacimiento y password retorna 201"""
        response = requests.post(f"{BASE_URL}/jugador/", json=jugador_con_password_data)
        
        assert response.status_code == 201
        data = response.json()
        assert "mensaje" in data
        assert data["mensaje"] == "Jugador creado correctamente"
        assert "data" in data
    
    def test_J03_crear_jugador_sin_password_usa_username(self, jugador_data):
        """J03: Crear jugador sin password permite login con username como password"""
        # Crear jugador sin password
        response = requests.post(f"{BASE_URL}/jugador/", json=jugador_data)
        assert response.status_code == 201
        
        username = jugador_data["username"]
        
        # Intentar login con username como password
        login_response = requests.post(f"{BASE_URL}/token/", json={
            "username": username,
            "password": username  # Password = username por defecto
        })
        
        assert login_response.status_code == 200
        assert "access" in login_response.json()
    
    def test_J04_crear_jugador_sin_username(self):
        """J04: Crear jugador sin username (requerido) retorna 400"""
        jugador_sin_username = {
            "fecha_nacimiento": "2010-05-15",
            "password": "test123"
        }
        
        response = requests.post(f"{BASE_URL}/jugador/", json=jugador_sin_username)
        
        assert response.status_code == 400
    
    def test_J05_crear_jugador_username_duplicado(self, jugador_data):
        """J05: Crear jugador con username duplicado retorna 400"""
        # Crear primer jugador
        response1 = requests.post(f"{BASE_URL}/jugador/", json=jugador_data)
        assert response1.status_code == 201
        
        # Intentar crear segundo jugador con mismo username
        response2 = requests.post(f"{BASE_URL}/jugador/", json=jugador_data)
        
        assert response2.status_code == 400


class TestJugadorDetail:
    """Tests para GET, PUT, DELETE /api/jugador/<id>"""
    
    def test_J06_obtener_jugador_por_id_valido(self, crear_jugador):
        """J06: GET /jugador/<id> con ID válido retorna 200"""
        jugador_id = crear_jugador["id"]
        
        response = requests.get(f"{BASE_URL}/jugador/{jugador_id}")
        
        assert response.status_code == 200
        assert response.json()["id"] == jugador_id
    
    def test_J07_obtener_jugador_por_id_invalido(self):
        """J07: GET /jugador/<id> con ID inexistente retorna 404"""
        response = requests.get(f"{BASE_URL}/jugador/99999")
        
        assert response.status_code == 404
    
    def test_J08_actualizar_jugador(self, crear_jugador):
        """J08: PUT /jugador/<id> actualiza datos correctamente"""
        jugador_id = crear_jugador["id"]
        
        updated_data = {
            "username": crear_jugador["username"],
            "first_name": "NombreActualizado",
            "fecha_nacimiento": "2010-05-15"
        }
        
        response = requests.put(f"{BASE_URL}/jugador/{jugador_id}", json=updated_data)
        
        assert response.status_code == 200
        assert response.json()["first_name"] == "NombreActualizado"
    
    def test_J09_eliminar_jugador(self, jugador_data):
        """J09: DELETE /jugador/<id> elimina correctamente"""
        # Crear jugador
        create_response = requests.post(f"{BASE_URL}/jugador/", json=jugador_data)
        assert create_response.status_code == 201
        jugador_id = create_response.json()["data"]["id"]
        
        # Eliminar
        response = requests.delete(f"{BASE_URL}/jugador/{jugador_id}")
        
        assert response.status_code == 204
        
        # Verificar que no existe
        get_response = requests.get(f"{BASE_URL}/jugador/{jugador_id}")
        assert get_response.status_code == 404


class TestJugadorLogicaNegocio:
    """Tests para validar lógica de negocio específica de Jugador"""
    
    def test_J10_rol_asignado_automaticamente(self, jugador_data):
        """J10: Verificar que rol se asigna automáticamente como 'Jugador'"""
        response = requests.post(f"{BASE_URL}/jugador/", json=jugador_data)
        
        assert response.status_code == 201
        data = response.json()["data"]
        assert data["rol"] == "Jugador"
