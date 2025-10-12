import { config } from "dotenv";
config();
import mongoose from "mongoose";
import { seedPopular } from "./tmdbSeeder";

async function main() {
    const uri = process.env.MONGODB_URI || "mongodb://localhost:27017/cinematch";
    await mongoose.connect(uri, { autoIndex: true });
    console.log("[mongo] Connected to MongoDB for seeding");

    try {
        await seedPopular(); // cantidad de películas a seedear
    } catch (error) {
        console.error("[mongo] Error seeding database:", error);
    } finally {
        await mongoose.disconnect();
        console.log("[mongo] Disconnected from MongoDB");
    }
}

main().catch(err => {
    console.error("[seed] Fatal error during seeding:", err);
    process.exit(1);
});