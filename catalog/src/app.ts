import express from "express";
import cors from "cors";
import morgan from "morgan";
import moviesRouter from "./routes/movies";
import { errorHandler, notFound } from "./middleware/errorHandler";

const app = express();

// Middlewares básicos
app.use(cors());
app.use(express.json({ limit: '10mb' }));
app.use(morgan("combined"));

// Health check endpoint
app.get("/health", (_req, res) => {
    res.json({ 
        ok: true, 
        service: "catalog",
        timestamp: new Date().toISOString(),
        uptime: process.uptime()
    });
});

// Rutas principales
app.use("/movies", moviesRouter);

// Middleware para rutas no encontradas
app.use(notFound);

// Middleware global de manejo de errores (debe ir al final)
app.use(errorHandler);

export default app;
