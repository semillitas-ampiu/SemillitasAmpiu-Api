"""
Tests para el endpoint de resultados (/api/resultado/)
Casos: RE01-RE10
"""

import requests
import pytest
import time

BASE_URL = "http://localhost:8000/api"


def get_timestamp():
    return str(int(time.time() * 1000))


class TestResultadoList:
    """Tests para GET y POST /api/resultado/"""

    def test_RE01_listar_resultados(self):
        """RE01: GET /resultado/ retorna lista de resultados"""
        response = requests.get(f"{BASE_URL}/resultado/")

        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_RE02_crear_resultado_completo(self, crear_jugador):
        """RE02: Crear resultado con todos los campos retorna 201"""
        resultado_data = {
            "usuario": crear_jugador["id"],
            "puntaje": 85,
            "completado": True,
        }

        response = requests.post(f"{BASE_URL}/resultado/", json=resultado_data)

        assert response.status_code == 201
        data = response.json()
        assert "mensaje" in data
        assert data["mensaje"] == "Resultado creado correctamente."
        assert data["data"]["puntaje"] == 85
        assert data["data"]["completado"] == True

    def test_RE03_crear_resultado_valores_por_defecto(self, crear_jugador):
        """RE03: Crear resultado sin puntaje ni completado usa valores por defecto"""
        resultado_data = {"usuario": crear_jugador["id"]}

        response = requests.post(f"{BASE_URL}/resultado/", json=resultado_data)

        assert response.status_code == 201
        data = response.json()["data"]
        # Valores por defecto del modelo: puntaje=20, completado=False
        assert data["puntaje"] == 20
        assert data["completado"] == False

    def test_RE04_crear_resultado_usuario_inexistente(self):
        """RE04: Crear resultado con usuario inexistente retorna 400"""
        resultado_data = {"usuario": 99999, "puntaje": 50}

        response = requests.post(f"{BASE_URL}/resultado/", json=resultado_data)

        assert response.status_code == 400


class TestResultadoDetail:
    """Tests para GET, PUT, DELETE /api/resultado/<id>"""

    def test_RE06_obtener_resultado_por_id_valido(self, crear_jugador):
        """RE06: GET /resultado/<id> con ID válido retorna 200"""
        # Crear resultado
        resultado_data = {"usuario": crear_jugador["id"], "puntaje": 75}
        create_response = requests.post(f"{BASE_URL}/resultado/", json=resultado_data)
        assert create_response.status_code == 201
        resultado_id = create_response.json()["data"]["id"]

        # Obtener por ID
        response = requests.get(f"{BASE_URL}/resultado/{resultado_id}")

        assert response.status_code == 200
        assert response.json()["id"] == resultado_id

    def test_RE07_obtener_resultado_por_id_invalido(self):
        """RE07: GET /resultado/<id> con ID inexistente retorna 404"""
        response = requests.get(f"{BASE_URL}/resultado/99999")

        assert response.status_code == 404

    def test_RE09_actualizar_resultado(self, crear_jugador):
        """RE09: PUT /resultado/<id> actualiza correctamente"""
        # Crear resultado
        resultado_data = {
            "usuario": crear_jugador["id"],
            "puntaje": 50,
            "completado": False,
        }
        create_response = requests.post(f"{BASE_URL}/resultado/", json=resultado_data)
        assert create_response.status_code == 201
        resultado_id = create_response.json()["data"]["id"]

        # Actualizar
        updated_data = {
            "usuario": crear_jugador["id"],
            "puntaje": 100,
            "completado": True,
        }

        response = requests.put(
            f"{BASE_URL}/resultado/{resultado_id}", json=updated_data
        )

        assert response.status_code == 200
        assert response.json()["puntaje"] == 100
        assert response.json()["completado"] == True

    def test_RE10_eliminar_resultado(self, crear_jugador):
        """RE10: DELETE /resultado/<id> elimina correctamente"""
        # Crear resultado
        resultado_data = {"usuario": crear_jugador["id"], "puntaje": 60}
        create_response = requests.post(f"{BASE_URL}/resultado/", json=resultado_data)
        assert create_response.status_code == 201
        resultado_id = create_response.json()["data"]["id"]

        # Eliminar
        response = requests.delete(f"{BASE_URL}/resultado/{resultado_id}")

        assert response.status_code == 204

        # Verificar que no existe
        get_response = requests.get(f"{BASE_URL}/resultado/{resultado_id}")
        assert get_response.status_code == 404


class TestResultadoFiltros:
    """Tests para los filtros de django-filter en resultado"""

    def test_RE08_filtrar_por_usuario(self, crear_jugador):
        """RE08: GET /resultado/?usuario=X filtra por usuario"""
        # Crear resultado
        resultado_data = {"usuario": crear_jugador["id"], "puntaje": 70}
        requests.post(f"{BASE_URL}/resultado/", json=resultado_data)

        # Filtrar por usuario
        response = requests.get(f"{BASE_URL}/resultado/?usuario={crear_jugador['id']}")

        assert response.status_code == 200
        resultados = response.json()
        assert isinstance(resultados, list)
        # Todos los resultados retornados deben ser del usuario
        for res in resultados:
            assert res["usuario"] == crear_jugador["id"]
