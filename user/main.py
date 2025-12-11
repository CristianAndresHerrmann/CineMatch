
from fastapi import FastAPI
from auth.routes import router as auth_router
from user.routes import router as user_router
from favorites.routes import router as favorites_router


app = FastAPI(title="CineMatch Usuarios", version="1.0.0")


# Rutas de autenticación
app.include_router(auth_router, prefix="/auth", tags=["auth"])

# Rutas de usuarios
app.include_router(user_router, prefix="/users", tags=["users"])

# Rutas de favoritos
app.include_router(favorites_router, prefix="/users", tags=["favorites"])
