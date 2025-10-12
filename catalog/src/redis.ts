import Redis from "ioredis"

export const redis = new Redis(process.env.REDIS_URL || "redis://localhost:6379",
    { lazyConnect: false });
    redis.on("connect", () => console.log("[redis] Connected to Redis"));
    redis.on("error", (err) => console.error("[redis] Redis error", err));