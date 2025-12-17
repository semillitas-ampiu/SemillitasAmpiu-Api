"""
Configuración compartida para todos los tests de la API Semillitas Ampiu.
Fixtures y utilidades comunes.
"""
import pytest
import requests
import time

# URL base de la API
BASE_URL = "http://localhost:8000/api"

# Almacena IDs de recursos creados para cleanup
_created_resources = {
    "jugador": [],
    "administrador": [],
    "palabra": [],
    "evaluacion": [],
    "recoleccion": [],
    "resultado": [],
    "ejercicio": [],
    "evaluado": [],
}


def register_for_cleanup(endpoint: str, resource_id: int):
    """Registra un recurso para ser eliminado al final de los tests"""
    if endpoint in _created_resources:
        _created_resources[endpoint].append(resource_id)


def cleanup_resources():
    """Elimina todos los recursos registrados durante los tests"""
    # Orden de eliminación respetando FK
    cleanup_order = [
        "recoleccion",
        "resultado", 
        "evaluado",
        "ejercicio",
        "jugador",
        "administrador",
        "palabra",
        "evaluacion",
    ]
    
    total_deleted = 0
    for endpoint in cleanup_order:
        for resource_id in _created_resources[endpoint]:
            try:
                response = requests.delete(f"{BASE_URL}/{endpoint}/{resource_id}")
                if response.status_code == 204:
                    total_deleted += 1
            except:
                pass
        _created_resources[endpoint].clear()
    
    return total_deleted


# Generador de timestamps para nombres únicos
def get_timestamp():
    return str(int(time.time() * 1000))

@pytest.fixture(scope="session")
def base_url():
    """Retorna la URL base de la API"""
    return BASE_URL

@pytest.fixture(scope="session")
def nivel_id():
    """
    Obtiene o crea un nivel para usar en los tests.
    Retorna el ID del primer nivel disponible.
    """
    response = requests.get(f"{BASE_URL}/nivel/")
    if response.status_code == 200 and len(response.json()) > 0:
        return response.json()[0]["id"]
    # Si no hay niveles, se asume que existe el ID 1
    return 1

@pytest.fixture
def timestamp():
    """Genera un timestamp único para evitar conflictos de unicidad"""
    return get_timestamp()

@pytest.fixture
def jugador_data(timestamp):
    """Datos para crear un jugador de prueba"""
    return {
        "username": f"jugador_test_{timestamp}",
        "fecha_nacimiento": "2010-05-15"
    }

@pytest.fixture
def jugador_con_password_data(timestamp):
    """Datos para crear un jugador con password personalizado"""
    return {
        "username": f"jugador_pwd_{timestamp}",
        "password": "password123",
        "fecha_nacimiento": "2010-05-15"
    }

@pytest.fixture
def admin_data(timestamp):
    """Datos para crear un administrador de prueba"""
    return {
        "email": f"admin_{timestamp}@test.com",
        "first_name": "Admin",
        "last_name": "Test",
        "fecha_nacimiento": "1990-01-01"
    }

@pytest.fixture
def palabra_data(timestamp, nivel_id):
    """Datos para crear una palabra de prueba"""
    return {
        "pal_español": f"español_{timestamp}",
        "pal_ampiu": f"ampiu_{timestamp}",
        "nivel": nivel_id
    }

@pytest.fixture
def crear_jugador(jugador_data):
    """Crea un jugador y retorna sus datos incluyendo el ID"""
    response = requests.post(f"{BASE_URL}/jugador/", json=jugador_data)
    assert response.status_code == 201
    data = response.json()
    result = data.get("data", data)
    register_for_cleanup("jugador", result["id"])
    return result

@pytest.fixture
def crear_palabra(palabra_data):
    """Crea una palabra y retorna sus datos incluyendo el ID"""
    response = requests.post(f"{BASE_URL}/palabra/", json=palabra_data)
    assert response.status_code == 201
    data = response.json()
    result = data.get("data", data)
    register_for_cleanup("palabra", result["id"])
    return result

@pytest.fixture
def crear_evaluacion(nivel_id, timestamp):
    """Crea una evaluación y retorna sus datos"""
    evaluacion_data = {
        "nombre": f"Evaluacion Test {timestamp}",
        "descripcion": "Evaluacion para tests",
        "nivel": nivel_id
    }
    response = requests.post(f"{BASE_URL}/evaluacion/", json=evaluacion_data)
    assert response.status_code == 201
    data = response.json()
    result = data.get("data", data)
    register_for_cleanup("evaluacion", result["id"])
    return result


@pytest.fixture(scope="session", autouse=True)
def cleanup_after_tests(request):
    """Fixture que ejecuta limpieza automática al final de la sesión de tests"""
    yield  # Ejecutar todos los tests primero
    
    # Después de todos los tests, ejecutar limpieza
    print("\n\n🧹 Ejecutando limpieza automática de datos de prueba...")
    deleted = cleanup_resources()
    print(f"✅ Limpieza completada. {deleted} recursos eliminados de la sesión.")
    
    # También ejecutar limpieza profunda con el script
    try:
        from cleanup_test_data import main as deep_cleanup
        deep_cleanup()
    except ImportError:
        pass  # El script no está disponible como módulo
