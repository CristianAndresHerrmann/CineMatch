import { Request, Response, NextFunction } from "express";
import { redis } from "./redis";

const TTL = Number(process.env.CACHE_TTL_SECONDS || 600);

export async function cacheByUrl(req: Request, res: Response, next: NextFunction) {
    const key = `cache:${req.originalUrl}`;
    try {
        const hit = await redis.get(key);
        if (hit) return res.type("application/json").send(hit);

        const send = res.json.bind(res);
        res.json = (body: any) => {
            redis.set(key, JSON.stringify(body), "EX", TTL).catch(() => { });
            return send(body);
        };
        next();
    } catch {
        next();
    }
}
