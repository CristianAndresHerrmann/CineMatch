import { config } from "dotenv";
config();
import axios from "axios";
import pLimit from "p-limit";
import dayjs from "dayjs";
import mongoose from "mongoose";
import Movie from "../models/Movie";

// --- Config ---
const TMDB_API_KEY = process.env.TMDB_API_KEY!;
const TMDB_BASE_URL = process.env.TMDB_BASE_URL || "https://api.themoviedb.org/3";
const TMDB_LANG = process.env.TMDB_LANG || "es-ES";
const TMDB_PAGES = Number(process.env.TMDB_PAGES || 20); // Aumentamos a 20 páginas por categoría
const POSTER_SIZE = process.env.POSTER_SIZE || "w500";

// Categorías de películas para obtener más variedad
const MOVIE_CATEGORIES = [
    'popular',
    'top_rated',
    'now_playing',
    'upcoming'
];

const posterUrl = (path?: string | null) =>
    path ? `https://image.tmdb.org/t/p/${POSTER_SIZE}${path}` : undefined;

const limit = pLimit(6); // Reducimos ligeramente la concurrencia para mayor estabilidad con más datos
const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms));

type TmdbMovie = {
    id: number;
    title: string;
    original_title: string;
    overview: string;
    release_date?: string;
    genre_ids?: number[];
    vote_average?: number;
    poster_path?: string | null;
};

type TmdbGenre = { id: number; name: string; };
type TmdbCredits = {
    cast: Array<{ name: string; known_for_department?: string; order?: number }>;
    crew: Array<{ name: string; job?: string; department?: string }>;
};

async function tmdbGet<T>(path: string, params: Record<string, any> = {}): Promise<T> {
    const { data } = await axios.get<T>(`${TMDB_BASE_URL}${path}`, {
        params: { api_key: TMDB_API_KEY, language: TMDB_LANG, ...params },
        timeout: 15000,
    });
    return data;
}

async function fetchGenresMap(): Promise<Map<number, string>> {
    const data = await tmdbGet<{ genres: TmdbGenre[] }>("/genre/movie/list");
    const map = new Map<number, string>();
    data.genres.forEach(g => map.set(g.id, g.name));
    return map;
}

async function fetchMoviesByCategory(category: string, page: number): Promise<TmdbMovie[]> {
    const data = await tmdbGet<{ results: TmdbMovie[] }>(`/movie/${category}`, { page });
    return data.results || [];
}

async function fetchPopularPage(page: number): Promise<TmdbMovie[]> {
    return fetchMoviesByCategory('popular', page);
}

async function fetchCredits(movieId: number): Promise<TmdbCredits> {
    return await tmdbGet<TmdbCredits>(`/movie/${movieId}/credits`);
}

function mapMovie(doc: TmdbMovie, genresMap: Map<number, string>, credits?: TmdbCredits) {
    const anio = doc.release_date ? dayjs(doc.release_date).year() : undefined;
    const generos = (doc.genre_ids || []).map(id => genresMap.get(id)).filter(Boolean) as string[];

    const director = credits?.crew?.find(c => c.job === "Director")?.name;
    const actores = credits?.cast
        ?.sort((a, b) => (a.order ?? 999) - (b.order ?? 999))
        .slice(0, 5)
        .map(c => c.name) || [];

    return {
        _id: `tmdb:${doc.id}`,
        titulo: doc.title || doc.original_title,
        descripcion: doc.overview,
        anio,
        director,
        actores,
        generos,
        calificacion_promedio: typeof doc.vote_average === "number" ? Number(doc.vote_average.toFixed(1)) : undefined,
        url_portada: posterUrl(doc.poster_path),
        tmdb_id: doc.id,
        updated_at: new Date()
    };
}

async function upsertMovie(mapped: any) {
    await Movie.findOneAndUpdate(
        { _id: mapped._id },
        { $set: mapped },
        { upsert: true, new: true, setDefaultsOnInsert: true }
    );
}

export async function seedMovies() {
    const genresMap = await fetchGenresMap();
    console.log(`[seed] géneros cargados: ${genresMap.size}`);

    let totalMovies = 0;

    for (const category of MOVIE_CATEGORIES) {
        console.log(`\n[seed] === Categoría: ${category} ===`);
        
        for (let p = 1; p <= TMDB_PAGES; p++) {
            console.log(`[seed] página ${category} ${p}/${TMDB_PAGES}`);
            const results = await fetchMoviesByCategory(category, p);

            await Promise.all(results.map((m) => limit(async () => {
                try {
                    const credits = await fetchCredits(m.id);
                    const mapped = mapMovie(m, genresMap, credits);
                    await upsertMovie(mapped);
                    totalMovies++;
                    await sleep(50);
                } catch (e: any) {
                    console.warn(`[seed] error movie id=${m.id}:`, e?.response?.status || e.message);
                }
            })));

            await sleep(300);
        }
        
        console.log(`[seed] ${category} completada, esperando antes de la siguiente...`);
        await sleep(1000);
    }

    console.log(`\n[seed] 🎬 Seeding completado! Total de películas procesadas: ${totalMovies}`);
}

export async function seedPopular() {
    return seedMovies();
}