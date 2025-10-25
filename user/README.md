# CineMatch Users API

Microservicio de usuarios para CineMatch

## Descripción
Este microservicio gestiona el registro, autenticación y administración de usuarios para la plataforma CineMatch. Incluye endpoints para registro, login, y (a futuro) gestión de perfil, preferencias, favoritos y películas vistas.

## Tecnologías principales
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- JWT (python-jose)
- Bcrypt (passlib)
- Docker y Docker Compose

## Endpoints implementados

### Registro de usuario
- **POST /register**
  - Crea un nuevo usuario.
  - Body JSON: `{ "username": str, "email": str, "password": str (8-72 caracteres) }`
  - Respuestas:
    - 201: Usuario creado
    - 409: Usuario/email ya existe
    - 422: Datos inválidos

### Login de usuario
- **POST /login**
  - Autentica un usuario y devuelve un JWT.
  - Body JSON: `{ "username": str, "password": str }`
  - Respuestas:
    - 200: JWT y user_id
    - 401: Credenciales inválidas

## Seguridad
- Contraseñas hasheadas con bcrypt.
- JWT para autenticación.

## Base de datos
- Nombre: `cinematch_users`
- Usuario: `cinematch_user`
- Contraseña: `cinematch_password`
- Host: `db` (en Docker)

## Migraciones
- Alembic gestiona la creación y actualización de tablas.
- Comando para aplicar migraciones:
  ```sh
  docker compose exec users alembic upgrade head
  ```

## Cómo correr el microservicio
1. Clona el repositorio y entra a la carpeta `user`.
2. Ejecuta:
   ```sh
   docker compose up --build
   ```
3. Aplica migraciones si es necesario.
4. Usa Postman o similar para probar los endpoints.

---

## Historial de cambios

- v0.0.1: Estructura inicial, endpoints de registro y login funcionando, autenticación JWT, Docker y migraciones OK.

---

*Actualiza este archivo con cada cambio relevante en endpoints, lógica o configuración.*
