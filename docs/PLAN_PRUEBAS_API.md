# DISEÑO DE LOS CASOS DE PRUEBA

| **Centro de Teleinformática y Producción Industrial** |                                                 |                                            |
| ----------------------------------------------------- | ----------------------------------------------- | ------------------------------------------ |
| **Número de Documento**                               | FS-DOC-DISEÑO CASOS DE PRUEBA                   | **Fecha de Creación:** Diciembre/15/2024   |
| **Nombre del Documento**                              | PLANTILLA PARA EL DISEÑO DE LOS CASOS DE PRUEBA | **Elaborado Por:** Equipo Semillitas Ampiu |

---

## Nombre del Proyecto: API REST Semillitas Ampiu

**Descripción:** API REST educativa para enseñar el idioma Ampiu. Backend Django con autenticación JWT, dos roles de usuario (Admin/Jugador) y sistema de vocabulario con palabras y seguimiento de progreso.

---

## Requerimientos de Ambiente de Pruebas (Globales)

| Requisito         | Detalle                                          |
| ----------------- | ------------------------------------------------ |
| Servidor          | Django corriendo en `http://localhost:8000`      |
| Base de Datos     | PostgreSQL con datos iniciales                   |
| Herramientas      | pytest, requests                                 |
| Navegador/Cliente | Cualquier cliente HTTP (Postman, curl, requests) |
| Conexión          | Red local o acceso al servidor de pruebas        |

---

## 1. MÓDULO: AUTENTICACIÓN JWT (Token)

### Historia de Usuario

> Como usuario registrado, quiero iniciar sesión en la aplicación utilizando mis credenciales para acceder a mis datos y funcionalidades personalizadas según mi rol (Admin o Jugador).

| Id  | Requerimiento/Historia           | Caso de Prueba                           | Descripción                                                       | Precondiciones                                      | Área Funcional | Pasos a Seguir                                                                                    | Datos/Acciones de Entrada                                                    | Resultado Esperado                                                          | Dependencias         | Responsable |
| --- | -------------------------------- | ---------------------------------------- | ----------------------------------------------------------------- | --------------------------------------------------- | -------------- | ------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- | --------------------------------------------------------------------------- | -------------------- | ----------- |
| T01 | Login con credenciales válidas   | test_T01_login_credenciales_validas      | Permite ingresar a la aplicación con usuario y contraseña válidos | _ Usuario registrado en el sistema _ Usuario activo | Autenticación  | 1. Enviar POST a `/api/token/` 2. Incluir username y password en body JSON 3. Verificar respuesta | `{"username": "jugador_test", "password": "jugador_test"}`                   | Status 200, respuesta contiene `access` y `refresh` tokens con longitud > 0 | Crear jugador previo | QA Team     |
| T02 | Login con credenciales inválidas | test_T02_login_credenciales_invalidas    | Rechaza acceso cuando las credenciales son incorrectas            | \* Ninguna                                          | Autenticación  | 1. Enviar POST a `/api/token/` 2. Usar credenciales inexistentes 3. Verificar error               | `{"username": "usuario_inexistente_xyz", "password": "password_incorrecto"}` | Status 401 Unauthorized                                                     | Ninguna              | QA Team     |
| T03 | Login sin password               | test_T03_login_sin_password              | Rechaza petición cuando falta el campo password                   | \* Ninguna                                          | Autenticación  | 1. Enviar POST a `/api/token/` 2. Enviar solo username sin password                               | `{"username": "cualquier_usuario"}`                                          | Status 400 Bad Request                                                      | Ninguna              | QA Team     |
| T04 | Refresh token válido             | test_T04_refresh_token_valido            | Permite renovar el access token usando un refresh token válido    | _ Login previo exitoso _ Refresh token activo       | Autenticación  | 1. Hacer login para obtener tokens 2. Enviar POST a `/api/token/refresh` con refresh token        | `{"refresh": "<refresh_token_obtenido>"}`                                    | Status 200, respuesta contiene nuevo `access` token                         | T01                  | QA Team     |
| T05 | Refresh token inválido           | test_T05_refresh_token_invalido          | Rechaza refresh tokens malformados o expirados                    | \* Ninguna                                          | Autenticación  | 1. Enviar POST a `/api/token/refresh` 2. Usar token inválido                                      | `{"refresh": "token_invalido_malformado"}`                                   | Status 401 Unauthorized                                                     | Ninguna              | QA Team     |
| T06 | Verificar claims personalizados  | test_T06_verificar_claims_personalizados | Verifica que el token JWT contenga información del usuario        | \* Usuario registrado                               | Autenticación  | 1. Hacer login 2. Verificar datos de usuario en respuesta                                         | Login válido con jugador existente                                           | Respuesta incluye `user` con: id, username, rol="Jugador"                   | T01                  | QA Team     |

---

## 2. MÓDULO: GESTIÓN DE ADMINISTRADORES

### Historia de Usuario

> Como sistema, necesito gestionar administradores que tengan email como identificador único y reciban sus credenciales automáticamente por correo electrónico.

| Id  | Requerimiento/Historia       | Caso de Prueba                         | Descripción                                                       | Precondiciones                     | Área Funcional | Pasos a Seguir                                                                                   | Datos/Acciones de Entrada                                                                                        | Resultado Esperado                                                                   | Dependencias | Responsable |
| --- | ---------------------------- | -------------------------------------- | ----------------------------------------------------------------- | ---------------------------------- | -------------- | ------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ | ------------ | ----------- |
| A01 | Listar administradores       | test_A01_listar_administradores        | Obtiene la lista completa de administradores                      | \* API disponible                  | CRUD Admin     | 1. Enviar GET a `/api/administrador/` 2. Verificar respuesta                                     | Ninguno (GET sin body)                                                                                           | Status 200, respuesta es un array (puede estar vacío)                                | Ninguna      | QA Team     |
| A02 | Crear admin datos completos  | test_A02_crear_admin_datos_completos   | Crea un administrador con todos los datos requeridos              | \* Email único no existente        | CRUD Admin     | 1. Enviar POST a `/api/administrador/` 2. Incluir email, first_name, last_name, fecha_nacimiento | `{"email": "admin_test@test.com", "first_name": "Admin", "last_name": "Test", "fecha_nacimiento": "1990-01-01"}` | Status 201, mensaje="Administrador creado correctamente", data contiene admin creado | Ninguna      | QA Team     |
| A03 | Crear admin sin email        | test_A03_crear_admin_sin_email         | Rechaza creación cuando falta el email (campo requerido)          | \* Ninguna                         | CRUD Admin     | 1. Enviar POST a `/api/administrador/` 2. Omitir campo email                                     | `{"first_name": "Admin", "last_name": "Test", "fecha_nacimiento": "1990-01-01"}`                                 | Status 400, errores incluyen validación de email                                     | Ninguna      | QA Team     |
| A04 | Crear admin email duplicado  | test_A04_crear_admin_email_duplicado   | Rechaza creación cuando el email ya existe                        | \* Admin con mismo email ya creado | CRUD Admin     | 1. Crear admin 2. Intentar crear otro con mismo email                                            | Mismo email que admin existente                                                                                  | Status 400 Bad Request                                                               | A02          | QA Team     |
| A05 | Obtener admin por ID válido  | test_A05_obtener_admin_por_id_valido   | Obtiene datos de un administrador específico                      | \* Admin existente con ID conocido | CRUD Admin     | 1. Crear admin 2. GET a `/api/administrador/{id}`                                                | ID del admin creado                                                                                              | Status 200, respuesta contiene datos del admin con id correcto                       | A02          | QA Team     |
| A06 | Obtener admin ID inválido    | test_A06_obtener_admin_por_id_invalido | Retorna error cuando el ID no existe                              | \* Ninguna                         | CRUD Admin     | 1. GET a `/api/administrador/99999`                                                              | ID inexistente: 99999                                                                                            | Status 404 Not Found                                                                 | Ninguna      | QA Team     |
| A07 | Actualizar admin             | test_A07_actualizar_admin              | Actualiza datos de un administrador existente                     | \* Admin existente                 | CRUD Admin     | 1. Crear admin 2. PUT a `/api/administrador/{id}` con nuevos datos                               | `{"first_name": "NombreActualizado", ...}`                                                                       | Status 200, first_name actualizado a "NombreActualizado"                             | A02          | QA Team     |
| A08 | Eliminar admin               | test_A08_eliminar_admin                | Elimina un administrador del sistema                              | \* Admin existente                 | CRUD Admin     | 1. Crear admin 2. DELETE a `/api/administrador/{id}` 3. Verificar que no existe                  | ID del admin a eliminar                                                                                          | Status 204 No Content, GET posterior retorna 404                                     | A02          | QA Team     |
| A09 | Username = Email automático  | test_A09_username_igual_a_email        | Verifica que el username se asigna automáticamente igual al email | \* Ninguna                         | Lógica Negocio | 1. Crear admin 2. Verificar campo username en respuesta                                          | Email de prueba                                                                                                  | username en respuesta igual al email enviado                                         | A02          | QA Team     |
| A10 | Rol asignado automáticamente | test_A10_rol_asignado_automaticamente  | Verifica que el rol 'Admin' se asigna automáticamente             | \* Ninguna                         | Lógica Negocio | 1. Crear admin 2. Verificar campo rol en respuesta                                               | Datos de admin válidos                                                                                           | rol="Admin" en respuesta                                                             | A02          | QA Team     |

---

## 3. MÓDULO: GESTIÓN DE JUGADORES

### Historia de Usuario

> Como jugador, quiero registrarme en la aplicación con un username único para poder acceder al contenido educativo del idioma Ampiu.

| Id  | Requerimiento/Historia           | Caso de Prueba                                   | Descripción                                                       | Precondiciones                          | Área Funcional | Pasos a Seguir                                                    | Datos/Acciones de Entrada                                                                     | Resultado Esperado                                              | Dependencias | Responsable |
| --- | -------------------------------- | ------------------------------------------------ | ----------------------------------------------------------------- | --------------------------------------- | -------------- | ----------------------------------------------------------------- | --------------------------------------------------------------------------------------------- | --------------------------------------------------------------- | ------------ | ----------- |
| J01 | Listar jugadores                 | test_J01_listar_jugadores                        | Obtiene la lista completa de jugadores                            | \* API disponible                       | CRUD Jugador   | 1. Enviar GET a `/api/jugador/` 2. Verificar respuesta            | Ninguno (GET sin body)                                                                        | Status 200, respuesta es un array                               | Ninguna      | QA Team     |
| J02 | Crear jugador datos completos    | test_J02_crear_jugador_datos_completos           | Crea un jugador con username, fecha_nacimiento y password         | \* Username único                       | CRUD Jugador   | 1. POST a `/api/jugador/` con datos completos                     | `{"username": "jugador_test", "fecha_nacimiento": "2010-05-15", "password": "mipassword123"}` | Status 201, mensaje="Jugador creado correctamente"              | Ninguna      | QA Team     |
| J03 | Crear jugador sin password       | test_J03_crear_jugador_sin_password_usa_username | Crea jugador sin password, usa username como password por defecto | \* Username único                       | CRUD Jugador   | 1. POST sin password 2. Intentar login con username como password | `{"username": "jugador_test", "fecha_nacimiento": "2010-05-15"}`                              | Status 201, login posterior con username=password exitoso (200) | Ninguna      | QA Team     |
| J04 | Crear jugador sin username       | test_J04_crear_jugador_sin_username              | Rechaza creación cuando falta el username                         | \* Ninguna                              | CRUD Jugador   | 1. POST a `/api/jugador/` sin username                            | `{"fecha_nacimiento": "2010-05-15", "password": "test123"}`                                   | Status 400 Bad Request                                          | Ninguna      | QA Team     |
| J05 | Crear jugador username duplicado | test_J05_crear_jugador_username_duplicado        | Rechaza creación cuando el username ya existe                     | \* Jugador con mismo username existente | CRUD Jugador   | 1. Crear jugador 2. Intentar crear otro con mismo username        | Username duplicado                                                                            | Status 400 Bad Request                                          | J02          | QA Team     |
| J06 | Obtener jugador ID válido        | test_J06_obtener_jugador_por_id_valido           | Obtiene datos de un jugador específico                            | \* Jugador existente                    | CRUD Jugador   | 1. GET a `/api/jugador/{id}`                                      | ID del jugador                                                                                | Status 200, id en respuesta coincide                            | J02          | QA Team     |
| J07 | Obtener jugador ID inválido      | test_J07_obtener_jugador_por_id_invalido         | Retorna error cuando el ID no existe                              | \* Ninguna                              | CRUD Jugador   | 1. GET a `/api/jugador/99999`                                     | ID: 99999                                                                                     | Status 404 Not Found                                            | Ninguna      | QA Team     |
| J08 | Actualizar jugador               | test_J08_actualizar_jugador                      | Actualiza datos de un jugador existente                           | \* Jugador existente                    | CRUD Jugador   | 1. PUT a `/api/jugador/{id}` con nuevos datos                     | `{"first_name": "NombreActualizado", ...}`                                                    | Status 200, first_name actualizado                              | J02          | QA Team     |
| J09 | Eliminar jugador                 | test_J09_eliminar_jugador                        | Elimina un jugador del sistema                                    | \* Jugador existente                    | CRUD Jugador   | 1. DELETE a `/api/jugador/{id}` 2. Verificar eliminación          | ID del jugador                                                                                | Status 204, GET posterior retorna 404                           | J02          | QA Team     |
| J10 | Rol asignado automáticamente     | test_J10_rol_asignado_automaticamente            | Verifica que el rol 'Jugador' se asigna automáticamente           | \* Ninguna                              | Lógica Negocio | 1. Crear jugador 2. Verificar campo rol                           | Datos de jugador válidos                                                                      | rol="Jugador" en respuesta                                      | J02          | QA Team     |

---

## 4. MÓDULO: GESTIÓN DE PALABRAS (Vocabulario)

### Historia de Usuario

> Como administrador, quiero gestionar el vocabulario del idioma Ampiu asociando palabras en español con su traducción en Ampiu.

| Id  | Requerimiento/Historia          | Caso de Prueba                           | Descripción                                   | Precondiciones                         | Área Funcional | Pasos a Seguir                                       | Datos/Acciones de Entrada                              | Resultado Esperado                                  | Dependencias | Responsable |
| --- | ------------------------------- | ---------------------------------------- | --------------------------------------------- | -------------------------------------- | -------------- | ---------------------------------------------------- | ------------------------------------------------------ | --------------------------------------------------- | ------------ | ----------- |
| P01 | Listar palabras                 | test_P01_listar_palabras                 | Obtiene la lista completa de palabras         | \* API disponible                      | CRUD Palabra   | 1. GET a `/api/palabra/`                             | Ninguno                                                | Status 200, array de palabras                       | Ninguna      | QA Team     |
| P02 | Crear palabra completa          | test_P02_crear_palabra_completa          | Crea una palabra con español y ampiu          | \* Ninguna                             | CRUD Palabra   | 1. POST a `/api/palabra/` con datos completos        | `{"pal_español": "hola", "pal_ampiu": "kua"}`          | Status 201, mensaje="Palabra creada correctamente." | Ninguna      | QA Team     |
| P03 | Crear palabra español duplicado | test_P03_crear_palabra_español_duplicado | Rechaza creación cuando pal_español ya existe | \* Palabra con mismo español existente | CRUD Palabra   | 1. Crear palabra 2. Crear otra con mismo pal_español | pal_español duplicado                                  | Status 400 Bad Request                              | P02          | QA Team     |
| P04 | Crear palabra ampiu duplicado   | test_P04_crear_palabra_ampiu_duplicado   | Rechaza creación cuando pal_ampiu ya existe   | \* Palabra con mismo ampiu existente   | CRUD Palabra   | 1. Crear palabra 2. Crear otra con mismo pal_ampiu   | pal_ampiu duplicado                                    | Status 400 Bad Request                              | P02          | QA Team     |
| P07 | Obtener palabra ID válido       | test_P07_obtener_palabra_por_id_valido   | Obtiene datos de una palabra específica       | \* Palabra existente                   | CRUD Palabra   | 1. GET a `/api/palabra/{id}`                         | ID de palabra                                          | Status 200, id coincide                             | P02          | QA Team     |
| P08 | Obtener palabra ID inválido     | test_P08_obtener_palabra_por_id_invalido | Retorna error cuando el ID no existe          | \* Ninguna                             | CRUD Palabra   | 1. GET a `/api/palabra/99999`                        | ID: 99999                                              | Status 404 Not Found                                | Ninguna      | QA Team     |
| P09 | Actualizar palabra              | test_P09_actualizar_palabra              | Actualiza datos de una palabra                | \* Palabra existente                   | CRUD Palabra   | 1. PUT a `/api/palabra/{id}`                         | Nuevos valores de pal_español, pal_ampiu               | Status 200, datos actualizados                      | P02          | QA Team     |
| P10 | Eliminar palabra                | test_P10_eliminar_palabra                | Elimina una palabra del sistema               | \* Palabra existente                   | CRUD Palabra   | 1. DELETE a `/api/palabra/{id}` 2. Verificar         | ID de palabra                                          | Status 204, GET posterior 404                       | P02          | QA Team     |

---

## 5. MÓDULO: RECOLECCIÓN DE PALABRAS (UsuarioPalabras)

### Historia de Usuario

> Como jugador, quiero que se registren las palabras que voy aprendiendo para poder ver mi progreso en el vocabulario Ampiu.

| Id  | Requerimiento/Historia                | Caso de Prueba                                 | Descripción                                      | Precondiciones                                     | Área Funcional   | Pasos a Seguir                                   | Datos/Acciones de Entrada          | Resultado Esperado                                      | Dependencias | Responsable |
| --- | ------------------------------------- | ---------------------------------------------- | ------------------------------------------------ | -------------------------------------------------- | ---------------- | ------------------------------------------------ | ---------------------------------- | ------------------------------------------------------- | ------------ | ----------- |
| R01 | Listar recolecciones                  | test_R01_listar_recolecciones                  | Obtiene todas las recolecciones de palabras      | \* API disponible                                  | CRUD Recolección | 1. GET a `/api/recoleccion/`                     | Ninguno                            | Status 200, array de recolecciones                      | Ninguna      | QA Team     |
| R02 | Crear recolección                     | test_R02_crear_recoleccion                     | Registra que un usuario aprendió una palabra     | \* Usuario y palabra existentes                    | CRUD Recolección | 1. POST a `/api/recoleccion/`                    | `{"usuario": 1, "palabra": 1}`     | Status 201, mensaje="Recoleccion creado correctamente." | J02, P02     | QA Team     |
| R03 | Crear recolección duplicada           | test_R03_crear_recoleccion_duplicada           | Rechaza duplicados (unique_together)             | \* Recolección existente con mismo usuario+palabra | CRUD Recolección | 1. Crear recolección 2. Intentar crear la misma  | Misma combinación usuario+palabra  | Status 400 Bad Request                                  | R02          | QA Team     |
| R04 | Crear recolección usuario inexistente | test_R04_crear_recoleccion_usuario_inexistente | Rechaza cuando el usuario no existe              | \* Palabra existente                               | CRUD Recolección | 1. POST con usuario=99999                        | `{"usuario": 99999, "palabra": 1}` | Status 400 Bad Request                                  | P02          | QA Team     |
| R05 | Crear recolección palabra inexistente | test_R05_crear_recoleccion_palabra_inexistente | Rechaza cuando la palabra no existe              | \* Usuario existente                               | CRUD Recolección | 1. POST con palabra=99999                        | `{"usuario": 1, "palabra": 99999}` | Status 400 Bad Request                                  | J02          | QA Team     |
| R06 | Obtener recolección por ID            | test_R06_obtener_recoleccion_por_id            | Obtiene una recolección específica               | \* Recolección existente                           | CRUD Recolección | 1. GET a `/api/recoleccion/{id}`                 | ID de recolección                  | Status 200, id coincide                                 | R02          | QA Team     |
| R07 | Filtrar por usuario                   | test_R07_filtrar_por_usuario                   | Filtra recolecciones por usuario (django-filter) | \* Recolecciones existentes                        | Filtros          | 1. GET a `/api/recoleccion/?usuario=X`           | usuario=ID del jugador             | Status 200, todas las recolecciones tienen usuario=X    | R02          | QA Team     |
| R08 | Filtrar por palabra                   | test_R08_filtrar_por_palabra                   | Filtra recolecciones por palabra                 | \* Recolecciones existentes                        | Filtros          | 1. GET a `/api/recoleccion/?palabra=X`           | palabra=ID de palabra              | Status 200, todas tienen palabra=X                      | R02          | QA Team     |
| R09 | Filtrar por ambos                     | test_R09_filtrar_por_ambos                     | Filtra por usuario Y palabra                     | \* Recolección específica existente                | Filtros          | 1. GET con `?usuario=X&palabra=Y`                | usuario=X, palabra=Y               | Status 200, recolección específica                      | R02          | QA Team     |
| R10 | Eliminar recolección                  | test_R10_eliminar_recoleccion                  | Elimina una recolección                          | \* Recolección existente                           | CRUD Recolección | 1. DELETE a `/api/recoleccion/{id}` 2. Verificar | ID de recolección                  | Status 204, GET posterior 404                           | R02          | QA Team     |

---

## 6. MÓDULO: RESULTADOS DE EVALUACIONES

### Historia de Usuario

> Como sistema, necesito registrar los resultados que completan los jugadores, incluyendo puntaje y estado de completitud.

| Id   | Requerimiento/Historia              | Caso de Prueba                                | Descripción                                             | Precondiciones        | Área Funcional | Pasos a Seguir                              | Datos/Acciones de Entrada                              | Resultado Esperado                                                       | Dependencias | Responsable |
| ---- | ----------------------------------- | --------------------------------------------- | ------------------------------------------------------- | --------------------- | -------------- | ------------------------------------------- | ------------------------------------------------------ | ------------------------------------------------------------------------ | ------------ | ----------- |
| RE01 | Listar resultados                   | test_RE01_listar_resultados                   | Obtiene todos los resultados                            | \* API disponible     | CRUD Resultado | 1. GET a `/api/resultado/`                  | Ninguno                                                | Status 200, array de resultados                                          | Ninguna      | QA Team     |
| RE02 | Crear resultado completo            | test_RE02_crear_resultado_completo            | Crea resultado con todos los campos                     | \* Usuario existente  | CRUD Resultado | 1. POST a `/api/resultado/`                 | `{"usuario": 1, "puntaje": 85, "completado": true}`    | Status 201, mensaje="Resultado creado correctamente.", puntaje=85, completado=true | J02          | QA Team     |
| RE03 | Crear resultado valores por defecto | test_RE03_crear_resultado_valores_por_defecto | Crea resultado sin puntaje ni completado (usa defaults) | \* Usuario existente  | CRUD Resultado | 1. POST sin puntaje ni completado           | `{"usuario": 1}`                                       | Status 201, puntaje=20 (default), completado=false (default)             | J02          | QA Team     |
| RE04 | Crear resultado usuario inexistente | test_RE04_crear_resultado_usuario_inexistente | Rechaza cuando el usuario no existe                     | \* Ninguna            | CRUD Resultado | 1. POST con usuario=99999                   | `{"usuario": 99999, "puntaje": 50}`                    | Status 400 Bad Request                                                   | Ninguna      | QA Team     |
| RE06 | Obtener resultado por ID válido     | test_RE06_obtener_resultado_por_id_valido     | Obtiene un resultado específico                         | \* Resultado existente| CRUD Resultado | 1. GET a `/api/resultado/{id}`              | ID de resultado                                        | Status 200, id coincide                                                  | RE02         | QA Team     |
| RE07 | Obtener resultado ID inválido       | test_RE07_obtener_resultado_por_id_invalido   | Retorna error cuando el ID no existe                    | \* Ninguna            | CRUD Resultado | 1. GET a `/api/resultado/99999`             | ID: 99999                                              | Status 404 Not Found                                                     | Ninguna      | QA Team     |
| RE08 | Filtrar por usuario                 | test_RE08_filtrar_por_usuario                 | Filtra resultados por usuario (django-filter)           | \* Resultados existentes | Filtros     | 1. GET a `/api/resultado/?usuario=X`        | usuario=ID del jugador                                 | Status 200, todos los resultados tienen usuario=X                        | RE02         | QA Team     |
| RE09 | Actualizar resultado                | test_RE09_actualizar_resultado                | Actualiza datos de un resultado existente               | \* Resultado existente| CRUD Resultado | 1. PUT a `/api/resultado/{id}` con nuevos datos | `{"usuario": 1, "puntaje": 100, "completado": true}`   | Status 200, puntaje=100, completado=true                                  | RE02         | QA Team     |
| RE10 | Eliminar resultado                  | test_RE10_eliminar_resultado                  | Elimina un resultado del sistema                        | \* Resultado existente| CRUD Resultado | 1. DELETE a `/api/resultado/{id}` 2. Verificar | ID del resultado                                       | Status 204, GET posterior retorna 404                                    | RE02         | QA Team     |

---

## Matriz de Prioridades

| Prioridad | Casos                                                                          | Justificación                  |
| --------- | ------------------------------------------------------------------------------ | ------------------------------ |
| **ALTA**  | T01, T02, J02, J03, A02, P02, R02, RE02                                        | Funcionalidad core del sistema |
| **MEDIA** | T06, A09, A10, J10, R07, R08, RE03, RE08                                       | Lógica de negocio específica   |
| **BAJA**  | Casos de eliminación y actualización (A07-A08, J08-J09, P09-P10, R10, RE09-RE10) | Operaciones secundarias        |

---

## Datos de Prueba

### Jugador de Prueba

```json
{
  "username": "jugador_test_TIMESTAMP",
  "fecha_nacimiento": "2010-05-15"
}
```

### Administrador de Prueba

```json
{
  "email": "admin_TIMESTAMP@test.com",
  "first_name": "Admin",
  "last_name": "Test",
  "fecha_nacimiento": "1990-01-01"
}
```

### Palabra de Prueba

```json
{
  "pal_español": "palabra_test_TIMESTAMP",
  "pal_ampiu": "ampiu_test_TIMESTAMP"
}
```

---

## Estructura de Archivos de Test

```
test/
├── conftest.py              # Fixtures compartidos (BASE_URL, datos de prueba)
├── test_token.py            # Tests de autenticación JWT (T01-T06)
├── test_administrador.py    # Tests CRUD de administradores (A01-A10)
├── test_jugador.py          # Tests CRUD de jugadores (J01-J10)
├── test_palabra.py          # Tests CRUD de palabras (P01-P04, P07-P10)
├── test_recoleccion.py      # Tests CRUD de recolecciones (R01-R10)
├── test_resultado.py        # Tests CRUD de resultados (RE01-RE04, RE06-RE10)
```

---

## Ejecución de Pruebas

```bash
# Pre-requisito: Servidor Django corriendo
cd project_semillitas
python manage.py runserver

# En otra terminal, ejecutar tests
cd ..
pytest test/ -v

# Ejecutar módulo específico
pytest test/test_token.py -v
pytest test/test_jugador.py -v

# Ejecutar caso específico
pytest test/test_token.py::TestTokenLogin::test_T01_login_credenciales_validas -v
```

---

## Comandos de Ejecución

```bash
# Ejecutar todos los tests
pytest test/ -v

# Ejecutar tests específicos
pytest test/test_token.py -v
pytest test/test_jugador.py -v

# Ejecutar con reporte de cobertura
pytest test/ -v --tb=short

# Ejecutar solo tests de alta prioridad (por marca)
pytest test/ -v -m "alta_prioridad"
```

---

## Criterios de Aceptación

1. **Todos los tests de prioridad ALTA deben pasar**
2. **Cobertura de casos positivos y negativos para cada endpoint**
3. **Verificación de estructura de respuesta (mensajes en español)**
4. **Validación de códigos HTTP correctos**

---

## Notas Importantes

1. **Servidor requerido**: Los tests usan `requests` contra un servidor corriendo, no Django TestCase
2. **Limpieza de datos**: Algunos tests crean datos que pueden requerir limpieza manual
3. **Timestamps**: Se usan timestamps en nombres para evitar conflictos de unicidad
4. **Email en Admin**: El endpoint de admin envía correos reales, considerar mock en producción
