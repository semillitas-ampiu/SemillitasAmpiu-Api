"""
Script de limpieza de datos de prueba.
Elimina todos los datos creados durante la ejecución de tests.

Uso:
    python test/cleanup_test_data.py

O ejecutar después de pytest:
    pytest test/ -v && python test/cleanup_test_data.py
"""

import requests
import sys

BASE_URL = "http://localhost:8000/api"

# Patrones que identifican datos de prueba
TEST_PATTERNS = {
    "jugador": ["jugador_test_", "jugador_pwd_", "TESTUSER"],
    "administrador": ["admin_", "@test.com"],
    "palabra": ["español_", "ampiu_", "palabra_test_"],
}


def delete_resource(endpoint: str, resource_id: int, name: str = "") -> bool:
    """Elimina un recurso por ID"""
    try:
        response = requests.delete(f"{BASE_URL}/{endpoint}/{resource_id}")
        if response.status_code == 204:
            print(f"  ✓ Eliminado {endpoint}/{resource_id} {name}")
            return True
        elif response.status_code == 404:
            print(f"  - No existe {endpoint}/{resource_id}")
            return False
        else:
            print(
                f"  ✗ Error eliminando {endpoint}/{resource_id}: {response.status_code}"
            )
            return False
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def is_test_data(item: dict, patterns: list, field: str) -> bool:
    """Verifica si un item es dato de prueba basándose en patrones"""
    value = str(item.get(field, ""))
    return any(pattern.lower() in value.lower() for pattern in patterns)


def cleanup_recolecciones():
    """Elimina recolecciones de usuarios de prueba"""
    print("\n🧹 Limpiando recolecciones...")
    deleted = 0

    try:
        # Obtener todos los jugadores de prueba primero
        response = requests.get(f"{BASE_URL}/jugador/")
        if response.status_code != 200:
            print("  No se pudo obtener lista de jugadores")
            return deleted

        test_user_ids = []
        for jugador in response.json():
            if is_test_data(jugador, TEST_PATTERNS["jugador"], "username"):
                test_user_ids.append(jugador["id"])

        # Eliminar recolecciones de usuarios de prueba
        response = requests.get(f"{BASE_URL}/recoleccion/")
        if response.status_code == 200:
            for rec in response.json():
                if rec.get("usuario") in test_user_ids:
                    if delete_resource("recoleccion", rec["id"]):
                        deleted += 1

    except Exception as e:
        print(f"  Error: {e}")

    return deleted


def cleanup_resultados():
    """Elimina resultados de usuarios de prueba"""
    print("\n🧹 Limpiando resultados...")
    deleted = 0

    try:
        # Obtener IDs de usuarios de prueba
        response = requests.get(f"{BASE_URL}/jugador/")
        if response.status_code != 200:
            return deleted

        test_user_ids = []
        for jugador in response.json():
            if is_test_data(jugador, TEST_PATTERNS["jugador"], "username"):
                test_user_ids.append(jugador["id"])

        # También incluir admins de prueba
        response = requests.get(f"{BASE_URL}/administrador/")
        if response.status_code == 200:
            for admin in response.json():
                if is_test_data(admin, TEST_PATTERNS["administrador"], "email"):
                    test_user_ids.append(admin["id"])

        # Eliminar resultados
        response = requests.get(f"{BASE_URL}/resultado/")
        if response.status_code == 200:
            for resultado in response.json():
                if resultado.get("usuario") in test_user_ids:
                    if delete_resource("resultado", resultado["id"]):
                        deleted += 1

    except Exception as e:
        print(f"  Error: {e}")

    return deleted


def cleanup_jugadores():
    """Elimina jugadores de prueba"""
    print("\n🧹 Limpiando jugadores...")
    deleted = 0

    try:
        response = requests.get(f"{BASE_URL}/jugador/")
        if response.status_code == 200:
            for jugador in response.json():
                if is_test_data(jugador, TEST_PATTERNS["jugador"], "username"):
                    if delete_resource(
                        "jugador", jugador["id"], jugador.get("username", "")
                    ):
                        deleted += 1
    except Exception as e:
        print(f"  Error: {e}")

    return deleted


def cleanup_administradores():
    """Elimina administradores de prueba"""
    print("\n🧹 Limpiando administradores...")
    deleted = 0

    try:
        response = requests.get(f"{BASE_URL}/administrador/")
        if response.status_code == 200:
            for admin in response.json():
                if is_test_data(admin, TEST_PATTERNS["administrador"], "email"):
                    if delete_resource(
                        "administrador", admin["id"], admin.get("email", "")
                    ):
                        deleted += 1
    except Exception as e:
        print(f"  Error: {e}")

    return deleted


def cleanup_palabras():
    """Elimina palabras de prueba"""
    print("\n🧹 Limpiando palabras...")
    deleted = 0

    try:
        response = requests.get(f"{BASE_URL}/palabra/")
        if response.status_code == 200:
            for palabra in response.json():
                pal_esp = palabra.get("pal_español", "")
                pal_amp = palabra.get("pal_ampiu", "")

                is_test = any(
                    pattern.lower() in pal_esp.lower()
                    or pattern.lower() in pal_amp.lower()
                    for pattern in TEST_PATTERNS["palabra"]
                )

                if is_test:
                    if delete_resource("palabra", palabra["id"], pal_esp):
                        deleted += 1
    except Exception as e:
        print(f"  Error: {e}")

    return deleted


def main():
    """Ejecuta la limpieza completa en orden correcto (respetando FK)"""
    print("=" * 60)
    print("🗑️  LIMPIEZA DE DATOS DE PRUEBA - Semillitas Ampiu API")
    print("=" * 60)

    # Verificar conexión
    try:
        response = requests.get(f"{BASE_URL}/jugador/", timeout=5)
        if response.status_code != 200:
            print(f"\n❌ Error: No se puede conectar a la API en {BASE_URL}")
            print("   Asegúrate de que el servidor Django esté corriendo.")
            sys.exit(1)
    except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
        print(f"\n❌ Error: No se puede conectar a la API en {BASE_URL}")
        print("   Asegúrate de que el servidor Django esté corriendo:")
        print("   cd project_semillitas && python manage.py runserver")
        sys.exit(1)

    total_deleted = 0

    # Orden de limpieza: primero tablas dependientes, luego principales
    # Esto respeta las Foreign Keys

    # 1. Tablas con FK a Usuario y otras
    total_deleted += cleanup_recolecciones()
    total_deleted += cleanup_resultados()

    # 2. Tablas principales
    total_deleted += cleanup_jugadores()
    total_deleted += cleanup_administradores()
    total_deleted += cleanup_palabras()

    print("\n" + "=" * 60)
    print(f"✅ Limpieza completada. Total eliminados: {total_deleted}")
    print("=" * 60)

    return total_deleted


if __name__ == "__main__":
    main()
