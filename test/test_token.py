"""
Tests para el endpoint de autenticación JWT (/api/token/)
Casos: T01-T06
"""
import requests
import pytest
import base64
import json

BASE_URL = "http://localhost:8000/api"


class TestTokenLogin:
    """Tests de login con JWT"""
    
    def test_T01_login_credenciales_validas(self, crear_jugador):
        """T01: Login con credenciales válidas retorna tokens"""
        # El jugador creado sin password usa username como password
        jugador = crear_jugador
        username = jugador["username"]
        
        response = requests.post(f"{BASE_URL}/token/", json={
            "username": username,
            "password": username  # Password = username por defecto
        })
        
        assert response.status_code == 200
        data = response.json()
        assert "access" in data
        assert "refresh" in data
        assert len(data["access"]) > 0
        assert len(data["refresh"]) > 0
    
    def test_T02_login_credenciales_invalidas(self):
        """T02: Login con credenciales inválidas retorna 401"""
        response = requests.post(f"{BASE_URL}/token/", json={
            "username": "usuario_inexistente_xyz",
            "password": "password_incorrecto"
        })
        
        assert response.status_code == 401
    
    def test_T03_login_sin_password(self):
        """T03: Login sin password retorna 400"""
        response = requests.post(f"{BASE_URL}/token/", json={
            "username": "cualquier_usuario"
        })
        
        assert response.status_code == 400
    
    def test_T04_refresh_token_valido(self, crear_jugador):
        """T04: Refresh token válido retorna nuevo access token"""
        jugador = crear_jugador
        username = jugador["username"]
        
        # Primero hacemos login para obtener tokens
        login_response = requests.post(f"{BASE_URL}/token/", json={
            "username": username,
            "password": username
        })
        assert login_response.status_code == 200
        refresh_token = login_response.json()["refresh"]
        
        # Usamos el refresh token
        refresh_response = requests.post(f"{BASE_URL}/token/refresh", json={
            "refresh": refresh_token
        })
        
        assert refresh_response.status_code == 200
        assert "access" in refresh_response.json()
    
    def test_T05_refresh_token_invalido(self):
        """T05: Refresh token inválido retorna 401"""
        response = requests.post(f"{BASE_URL}/token/refresh", json={
            "refresh": "token_invalido_malformado"
        })
        
        assert response.status_code == 401
    
    def test_T06_verificar_claims_personalizados(self, crear_jugador):
        """T06: El token contiene claims personalizados (username, rol, id, nombre)"""
        jugador = crear_jugador
        username = jugador["username"]
        
        response = requests.post(f"{BASE_URL}/token/", json={
            "username": username,
            "password": username
        })
        
        assert response.status_code == 200
        data = response.json()
        
        # Verificar que la respuesta incluye datos del usuario
        assert "user" in data
        user_data = data["user"]
        assert "id" in user_data
        assert "username" in user_data
        assert "rol" in user_data
        assert user_data["username"] == username
        assert user_data["rol"] == "Jugador"
        
        # Decodificar el payload del JWT para verificar claims
        access_token = data["access"]
        # El token JWT tiene 3 partes separadas por punto
        payload_b64 = access_token.split(".")[1]
        # Agregar padding si es necesario
        payload_b64 += "=" * (4 - len(payload_b64) % 4)
        payload = json.loads(base64.urlsafe_b64decode(payload_b64))
        
        assert "username" in payload
        assert "rol" in payload
        assert "id" in payload
        assert payload["username"] == username
        assert payload["rol"] == "Jugador"
