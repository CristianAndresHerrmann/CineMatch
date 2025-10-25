from fastapi import FastAPI
from auth.routes import router as auth_router

app = FastAPI(title="CineMatch Usuarios", version="1.0.0")

# Rutas de autenticación
app.include_router(auth_router, prefix="/auth", tags=["auth"])

# Aquí se incluirán routers de usuarios, favoritos, vistos, preferencias
