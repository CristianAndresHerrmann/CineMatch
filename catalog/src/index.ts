// Entry point of the application
import { config } from "dotenv";
config();
import http from "http";
import app from "./app";
import { connectMongo } from "./db";
import { redis } from "./redis";

const PORT = process.env.PORT || 3001;

(async () => {
    try {
        await connectMongo();
        await redis.ping(); // verifica Redis
        const server = http.createServer(app);
        server.listen(PORT, () => console.log(`[catalog] listening on :${PORT}`));
    } catch (err) {
        console.error("Fatal init error:", err);
        process.exit(1);
    }
})();
