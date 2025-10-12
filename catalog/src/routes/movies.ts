import { Router } from "express";
import Movie from "../models/Movie";
import { cacheByUrl } from "../cache";

const router = Router();

// GET /movies?genre=Action&page=1&size=20&year=2023&minRating=7
router.get("/", cacheByUrl, async (req, res, next) => {
    try {
        const page = Math.max(1, parseInt(req.query.page as string) || 1);
        const size = Math.min(100, Math.max(1, parseInt(req.query.size as string) || 20));
        const genre = req.query.genre as string | undefined;
        const year = req.query.year ? parseInt(req.query.year as string) : undefined;
        const minRating = req.query.minRating ? parseFloat(req.query.minRating as string) : undefined;
        const maxRating = req.query.maxRating ? parseFloat(req.query.maxRating as string) : undefined;

        // Construir filtros dinámicamente
        const filter: any = {};
        if (genre) filter.generos = genre;
        if (year) filter.anio = year;
        if (minRating || maxRating) {
            filter.calificacion_promedio = {};
            if (minRating) filter.calificacion_promedio.$gte = minRating;
            if (maxRating) filter.calificacion_promedio.$lte = maxRating;
        }

        const [docs, total] = await Promise.all([
            Movie.find(filter)
                .sort({ calificacion_promedio: -1, _id: 1 })
                .skip((page - 1) * size)
                .limit(size)
                .select("_id titulo url_portada calificacion_promedio generos anio director")
                .lean(),
            Movie.countDocuments(filter)
        ]);

        res.json({
            data: docs,
            pagination: {
                page,
                size,
                total,
                totalPages: Math.ceil(total / size),
                hasNext: page < Math.ceil(total / size),
                hasPrev: page > 1
            }
        });
    } catch (error) {
        next(error);
    }
});

// GET /movies/search?query=avengers&page=1&size=20
router.get("/search", cacheByUrl, async (req, res, next) => {
    try {
        const query = (req.query.query as string || "").trim();
        const page = Math.max(1, parseInt(req.query.page as string) || 1);
        const size = Math.min(100, Math.max(1, parseInt(req.query.size as string) || 20));
        
        if (!query) {
            return res.json({
                data: [],
                query,
                pagination: { page, size, total: 0, totalPages: 0, hasNext: false, hasPrev: false }
            });
        }

        const [docs, total] = await Promise.all([
            Movie.find({ $text: { $search: query } })
                .skip((page - 1) * size)
                .limit(size)
                .select("_id titulo url_portada calificacion_promedio generos anio director score")
                .sort({ score: { $meta: "textScore" } })
                .lean(),
            Movie.countDocuments({ $text: { $search: query } })
        ]);

        res.json({
            data: docs,
            query,
            pagination: {
                page,
                size,
                total,
                totalPages: Math.ceil(total / size),
                hasNext: page < Math.ceil(total / size),
                hasPrev: page > 1
            }
        });
    } catch (error) {
        next(error);
    }
});

// GET /movies/genres
router.get("/genres", cacheByUrl, async (_req, res, next) => {
    try {
        const genres = await Movie.distinct("generos");
        res.json({
            data: genres.sort(),
            total: genres.length
        });
    } catch (error) {
        next(error);
    }
});

// GET /movies/trending - Endpoint adicional para películas populares
router.get("/trending", cacheByUrl, async (_req, res, next) => {
    try {
        const docs = await Movie.find({})
            .sort({ calificacion_promedio: -1 })
            .limit(20)
            .select("_id titulo url_portada calificacion_promedio generos anio director")
            .lean();

        res.json({
            data: docs,
            total: docs.length
        });
    } catch (error) {
        next(error);
    }
});

// GET /movies/:id - Esta ruta debe ir AL FINAL para no interferir con las rutas específicas
router.get("/:id", cacheByUrl, async (req, res, next) => {
    try {
        const doc = await Movie.findById(req.params.id).lean();
        if (!doc) {
            return res.status(404).json({ 
                error: "Not Found",
                message: "Movie not found" 
            });
        }
        res.json(doc);
    } catch (error) {
        next(error);
    }
});

export default router;