import { Request, Response, NextFunction } from 'express';

// Middleware para manejar errores globales
export function errorHandler(err: any, req: Request, res: Response, next: NextFunction) {
    console.error(`[Error] ${req.method} ${req.path}:`, err);

    // Error de MongoDB
    if (err.name === 'CastError') {
        return res.status(400).json({
            error: 'Invalid ID format'
        });
    }

    // Error de conexión a MongoDB
    if (err.name === 'MongooseError') {
        return res.status(503).json({
            error: 'Database connection error'
        });
    }

    // Error genérico del servidor
    res.status(500).json({
        error: 'Internal Server Error',
        message: process.env.NODE_ENV === 'development' ? err.message : 'Something went wrong'
    });
}

// Middleware para manejar rutas no encontradas
export function notFound(req: Request, res: Response) {
    res.status(404).json({
        error: 'Not Found',
        message: `Route ${req.method} ${req.path} not found`
    });
}