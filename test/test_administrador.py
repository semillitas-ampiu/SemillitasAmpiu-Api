"""
Tests para el endpoint de administradores (/api/administrador/)
Casos: A01-A10
"""
import requests
import pytest
import time

BASE_URL = "http://localhost:8000/api"


def get_timestamp():
    return str(int(time.time() * 1000))


class TestAdministradorList:
    """Tests para GET y POST /api/administrador/"""
    
    def test_A01_listar_administradores(self):
        """A01: GET /administrador/ retorna lista de administradores"""
        response = requests.get(f"{BASE_URL}/administrador/")
        
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_A02_crear_admin_datos_completos(self, admin_data):
        """A02: Crear admin con datos completos retorna 201"""
        response = requests.post(f"{BASE_URL}/administrador/", json=admin_data)
        
        assert response.status_code == 201
        data = response.json()
        assert "mensaje" in data
        assert "data" in data
        assert data["mensaje"] == "Administrador creado correctamente"
    
    def test_A03_crear_admin_sin_email(self):
        """A03: Crear admin sin email (requerido) retorna 400"""
        admin_sin_email = {
            "first_name": "Admin",
            "last_name": "Test",
            "fecha_nacimiento": "1990-01-01"
        }
        
        response = requests.post(f"{BASE_URL}/administrador/", json=admin_sin_email)
        
        assert response.status_code == 400
        data = response.json()
        assert "errores" in data or "email" in str(data)
    
    def test_A04_crear_admin_email_duplicado(self, admin_data):
        """A04: Crear admin con email duplicado retorna 400"""
        # Crear primer admin
        response1 = requests.post(f"{BASE_URL}/administrador/", json=admin_data)
        assert response1.status_code == 201
        
        # Intentar crear segundo admin con mismo email
        response2 = requests.post(f"{BASE_URL}/administrador/", json=admin_data)
        
        assert response2.status_code == 400


class TestAdministradorDetail:
    """Tests para GET, PUT, DELETE /api/administrador/<id>"""
    
    def test_A05_obtener_admin_por_id_valido(self, admin_data):
        """A05: GET /administrador/<id> con ID válido retorna 200"""
        # Crear admin
        create_response = requests.post(f"{BASE_URL}/administrador/", json=admin_data)
        assert create_response.status_code == 201
        admin_id = create_response.json()["data"]["id"]
        
        # Obtener por ID
        response = requests.get(f"{BASE_URL}/administrador/{admin_id}")
        
        assert response.status_code == 200
        assert response.json()["id"] == admin_id
    
    def test_A06_obtener_admin_por_id_invalido(self):
        """A06: GET /administrador/<id> con ID inexistente retorna 404"""
        response = requests.get(f"{BASE_URL}/administrador/99999")
        
        assert response.status_code == 404
    
    def test_A07_actualizar_admin(self, admin_data):
        """A07: PUT /administrador/<id> actualiza datos correctamente"""
        # Crear admin
        create_response = requests.post(f"{BASE_URL}/administrador/", json=admin_data)
        assert create_response.status_code == 201
        admin_id = create_response.json()["data"]["id"]
        
        # Actualizar
        updated_data = admin_data.copy()
        updated_data["first_name"] = "NombreActualizado"
        
        response = requests.put(f"{BASE_URL}/administrador/{admin_id}", json=updated_data)
        
        assert response.status_code == 200
        assert response.json()["first_name"] == "NombreActualizado"
    
    def test_A08_eliminar_admin(self):
        """A08: DELETE /administrador/<id> elimina correctamente"""
        # Crear admin
        ts = get_timestamp()
        admin_data = {
            "email": f"admin_delete_{ts}@test.com",
            "first_name": "Delete",
            "last_name": "Test",
            "fecha_nacimiento": "1990-01-01"
        }
        create_response = requests.post(f"{BASE_URL}/administrador/", json=admin_data)
        assert create_response.status_code == 201
        admin_id = create_response.json()["data"]["id"]
        
        # Eliminar
        response = requests.delete(f"{BASE_URL}/administrador/{admin_id}")
        
        assert response.status_code == 204
        
        # Verificar que no existe
        get_response = requests.get(f"{BASE_URL}/administrador/{admin_id}")
        assert get_response.status_code == 404


class TestAdministradorLogicaNegocio:
    """Tests para validar lógica de negocio específica de Admin"""
    
    def test_A09_username_igual_a_email(self, admin_data):
        """A09: Verificar que username se asigna automáticamente igual al email"""
        response = requests.post(f"{BASE_URL}/administrador/", json=admin_data)
        
        assert response.status_code == 201
        data = response.json()["data"]
        assert data["username"] == admin_data["email"]
    
    def test_A10_rol_asignado_automaticamente(self, admin_data):
        """A10: Verificar que rol se asigna automáticamente como 'Admin'"""
        response = requests.post(f"{BASE_URL}/administrador/", json=admin_data)
        
        assert response.status_code == 201
        data = response.json()["data"]
        assert data["rol"] == "Admin"
