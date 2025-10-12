import mongoose from "mongoose";

export async function connectMongo() {
    const mongoUri = process.env.MONGODB_URI!;
    await mongoose.connect(mongoUri, {autoIndex: true});
    console.log("[mongo] Connected to MongoDB");
}