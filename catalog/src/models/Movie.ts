// Modelo + indices
import { Schema, model } from "mongoose";

const MovieSchema = new Schema({
    _id: { type: String },                 // usaremos "tmdb:<id>" como clave
    titulo: { type: String, required: true, index: true },
    descripcion: String,
    anio: Number,
    director: String,
    actores: [String],
    generos: { type: [String], index: true },
    calificacion_promedio: { type: Number, index: true },
    url_portada: String,
    tmdb_id: { type: Number, index: true, unique: true },
    updated_at: { type: Date, default: () => new Date(), index: true }
}, { versionKey: false });

MovieSchema.index({ titulo: "text", director: "text", actores: "text" });

export default model("Movie", MovieSchema);

