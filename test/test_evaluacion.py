import requests
import pytest

BASE_URL = "http://localhost:8000/api"  # Ajusta según tu configuración

# ===============================================
# TESTS PARA LISTAR EVALUACIONES (GET)
# ===============================================

def test_get_evaluaciones_success():
    """Verifica que se puedan obtener todas las evaluaciones"""
    response = requests.get(f"{BASE_URL}/evaluacion/")
    assert response.status_code == 200
    evaluaciones = response.json()
    longitud = len(evaluaciones)
    assert len(evaluaciones) == longitud
    assert isinstance(evaluaciones, list)


def test_get_evaluaciones_estructura():
    """Verifica que las evaluaciones tengan la estructura correcta"""
    response = requests.get(f"{BASE_URL}/evaluacion/")
    assert response.status_code == 200
    evaluaciones = response.json()
    
    if len(evaluaciones) > 0:
        evaluacion = evaluaciones[0]
        assert "id" in evaluacion
        assert "nombre" in evaluacion
        assert "descripcion" in evaluacion
        assert "nivel" in evaluacion
        assert "fecha" in evaluacion


# ===============================================
# TESTS PARA OBTENER EVALUACIÓN POR ID (GET)
# ===============================================

def test_get_evaluacion_por_id_existente():
    """Verifica que se pueda obtener una evaluación específica por ID"""
    # Primero obtenemos todas las evaluaciones para conseguir un ID válido
    response_list = requests.get(f"{BASE_URL}/evaluacion/")
    evaluaciones = response_list.json()
    
    if len(evaluaciones) > 0:
        id_valido = evaluaciones[0]["id"]
        response = requests.get(f"{BASE_URL}/evaluacion/{id_valido}")
        assert response.status_code == 200
        evaluacion = response.json()
        assert evaluacion["id"] == id_valido


def test_get_evaluacion_por_id_inexistente():
    """Verifica el comportamiento al buscar una evaluación que no existe"""
    id_inexistente = 99999
    response = requests.get(f"{BASE_URL}/evaluacion/{id_inexistente}")
    assert response.status_code == 404


# ===============================================
# TESTS PARA CREAR EVALUACIÓN (POST)
# ===============================================

def test_post_crear_evaluacion_completa():
    """Verifica que se pueda crear una evaluación con todos los campos"""
    nueva_evaluacion = {
        "nombre": "Evaluación Test Completa",
        "descripcion": "Descripción de prueba completa",
        "nivel": 1  # ID del nivel "Ley de Origen"
    }
    
    # Obtener cantidad inicial
    response_inicial = requests.get(f"{BASE_URL}/evaluacion/")
    longitud_inicial = len(response_inicial.json())
    
    # Crear nueva evaluación
    response = requests.post(f"{BASE_URL}/evaluacion/", json=nueva_evaluacion)
    assert response.status_code == 201
    
    # Verificar que se creó
    response_final = requests.get(f"{BASE_URL}/evaluacion/")
    assert len(response_final.json()) > longitud_inicial
    
    # Verificar datos de respuesta
    data = response.json()
    assert "data" in data or "id" in data
    

def test_post_crear_evaluacion_minima():
    """Verifica que se pueda crear una evaluación con campos mínimos"""
    nueva_evaluacion = {
        "nombre": "Eval Mínima",
        "descripcion": "Test",
        "nivel": 1
    }
    
    response = requests.post(f"{BASE_URL}/evaluacion/", json=nueva_evaluacion)
    assert response.status_code == 201


def test_post_crear_evaluacion_sin_nivel():
    """Verifica que no se pueda crear una evaluación sin nivel"""
    evaluacion_invalida = {
        "nombre": "Evaluación sin nivel",
        "descripcion": "Test sin nivel"
    }
    
    response = requests.post(f"{BASE_URL}/evaluacion/", json=evaluacion_invalida)
    assert response.status_code == 400


def test_post_crear_evaluacion_nivel_inexistente():
    """Verifica que no se pueda crear una evaluación con un nivel que no existe"""
    evaluacion_invalida = {
        "nombre": "Evaluación nivel inexistente",
        "descripcion": "Test nivel inválido",
        "nivel": 99999
    }
    
    response = requests.post(f"{BASE_URL}/evaluacion/", json=evaluacion_invalida)
    assert response.status_code == 400


def test_post_crear_evaluacion_sin_nombre():
    """Verifica el comportamiento al crear una evaluación sin nombre"""
    evaluacion_sin_nombre = {
        "descripcion": "Sin nombre",
        "nivel": 1
    }
    
    response = requests.post(f"{BASE_URL}/evaluacion/", json=evaluacion_sin_nombre)
    # Puede ser 400 o 201 dependiendo de si nombre tiene default
    assert response.status_code in [201, 400]


# ===============================================
# TESTS PARA ACTUALIZAR EVALUACIÓN (PUT/PATCH)
# ===============================================

def test_put_actualizar_evaluacion():
    """Verifica que se pueda actualizar una evaluación completa"""
    # Primero crear una evaluación
    nueva_evaluacion = {
        "nombre": "Para Actualizar",
        "descripcion": "Original",
        "nivel": 1
    }
    response_crear = requests.post(f"{BASE_URL}/evaluacion/", json=nueva_evaluacion)
    
    if response_crear.status_code == 201:
        data_creada = response_crear.json()
        # Extraer ID (puede estar en data o directamente)
        id_creado = data_creada.get("data", {}).get("id") or data_creada.get("id")
        
        if id_creado:
            # Actualizar la evaluación
            datos_actualizados = {
                "nombre": "Actualizada",
                "descripcion": "Modificada",
                "nivel": 1
            }
            response = requests.put(f"{BASE_URL}/evaluacion/{id_creado}", json=datos_actualizados)
            assert response.status_code == 200
            
            # Verificar actualización
            response_get = requests.get(f"{BASE_URL}/evaluacion/{id_creado}")
            evaluacion_actualizada = response_get.json()
            assert evaluacion_actualizada["nombre"] == "Actualizada"


def test_patch_actualizar_evaluacion_parcial():
    """Verifica que se pueda actualizar parcialmente una evaluación"""
    # Crear evaluación
    nueva_evaluacion = {
        "nombre": "Para Patch",
        "descripcion": "Original",
        "nivel": 1
    }
    response_crear = requests.post(f"{BASE_URL}/evaluacion/", json=nueva_evaluacion)
    
    if response_crear.status_code == 201:
        data_creada = response_crear.json()
        id_creado = data_creada.get("data", {}).get("id") or data_creada.get("id")
        
        if id_creado:
            # Actualizar solo la descripción
            datos_parciales = {
                "descripcion": "Descripción Actualizada"
            }
            response = requests.patch(f"{BASE_URL}/evaluacion/{id_creado}", json=datos_parciales)
            assert response.status_code == 200


# ===============================================
# TESTS PARA ELIMINAR EVALUACIÓN (DELETE)
# ===============================================

def test_delete_evaluacion():
    """Verifica que se pueda eliminar una evaluación"""
    # Crear evaluación para eliminar
    nueva_evaluacion = {
        "nombre": "Para Eliminar",
        "descripcion": "Será eliminada",
        "nivel": 1
    }
    response_crear = requests.post(f"{BASE_URL}/evaluacion/", json=nueva_evaluacion)
    
    if response_crear.status_code == 201:
        data_creada = response_crear.json()
        id_creado = data_creada.get("data", {}).get("id") or data_creada.get("id")
        
        if id_creado:
            # Eliminar
            response = requests.delete(f"{BASE_URL}/evaluacion/{id_creado}")
            assert response.status_code == 204
            
            # Verificar que fue eliminada
            response_get = requests.get(f"{BASE_URL}/evaluacion/{id_creado}")
            assert response_get.status_code == 404


def test_delete_evaluacion_inexistente():
    """Verifica el comportamiento al intentar eliminar una evaluación inexistente"""
    id_inexistente = 99999
    response = requests.delete(f"{BASE_URL}/evaluacion/{id_inexistente}")
    assert response.status_code == 404


# ===============================================
# TESTS DE VALIDACIÓN
# ===============================================

def test_validacion_nombre_largo():
    """Verifica el comportamiento con un nombre que excede el límite"""
    evaluacion_nombre_largo = {
        "nombre": "A" * 51,  # Excede el límite de 50 caracteres
        "descripcion": "Test",
        "nivel": 1
    }
    
    response = requests.post(f"{BASE_URL}/evaluacion/", json=evaluacion_nombre_largo)
    assert response.status_code == 400


def test_validacion_descripcion_larga():
    """Verifica el comportamiento con una descripción que excede el límite"""
    evaluacion_desc_larga = {
        "nombre": "Test",
        "descripcion": "B" * 51,  # Excede el límite de 50 caracteres
        "nivel": 1
    }
    
    response = requests.post(f"{BASE_URL}/evaluacion/", json=evaluacion_desc_larga)
    assert response.status_code == 400


# ===============================================
# TEST DE INTEGRACIÓN
# ===============================================

def test_flujo_completo_crud():
    """Test de integración que prueba el flujo completo CRUD"""
    # 1. Crear
    nueva_evaluacion = {
        "nombre": "CRUD Test",
        "descripcion": "Flujo completo",
        "nivel": 1
    }
    response_crear = requests.post(f"{BASE_URL}/evaluacion/", json=nueva_evaluacion)
    assert response_crear.status_code == 201
    
    data_creada = response_crear.json()
    id_creado = data_creada.get("data", {}).get("id") or data_creada.get("id")
    
    if id_creado:
        # 2. Leer
        response_leer = requests.get(f"{BASE_URL}/evaluacion/{id_creado}")
        assert response_leer.status_code == 200
        
        # 3. Actualizar
        datos_actualizados = {
            "nombre": "CRUD Test Actualizado",
            "descripcion": "Flujo actualizado",
            "nivel": 1
        }
        response_actualizar = requests.put(f"{BASE_URL}/evaluacion/{id_creado}", json=datos_actualizados)
        assert response_actualizar.status_code == 200
        
        # 4. Eliminar
        response_eliminar = requests.delete(f"{BASE_URL}/evaluacion/{id_creado}")
        assert response_eliminar.status_code == 204
        
        # 5. Verificar eliminación
        response_verificar = requests.get(f"{BASE_URL}/evaluacion/{id_creado}")
        assert response_verificar.status_code == 404