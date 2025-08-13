from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from supabase import create_client, Client
import os
from dotenv import load_dotenv
import sys
import asyncio

# Add bot folder to path
sys.path.append('../bot')
from bot_manager import bot_manager

load_dotenv()

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Supabase setup
supabase: Client = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

class BotCreate(BaseModel):
    bot_token: str
    bot_name: str

@app.get("/")
def read_root():
    return {"message": "API is running"}

@app.post("/api/bots")
async def create_bot(bot: BotCreate):
    # Get current user from Supabase auth
    # For now, using hardcoded creator_id
    creator_id = "test-creator-id"
    
    result = supabase.table("discord_bots").insert({
        "creator_id": creator_id,
        "bot_token": bot.bot_token,
        "bot_name": bot.bot_name
    }).execute()
    
    return result.data

@app.get("/api/bots")
async def list_bots():
    creator_id = "test-creator-id"
    
    result = supabase.table("discord_bots").select("*").eq(
        "creator_id", creator_id
    ).execute()
    
    return result.data

@app.post("/api/bots/{bot_id}/start")
async def start_bot(bot_id: str):
    # Fetch bot from database
    result = supabase.table("discord_bots").select("*").eq("id", bot_id).execute()
    
    if result.data:
        bot = result.data[0]
        success = await bot_manager.start_bot(bot_id, bot['bot_token'])
        
        if success:
            # Update status in database
            supabase.table("discord_bots").update(
                {"status": "active"}
            ).eq("id", bot_id).execute()
            
            return {"status": "started", "bot_id": bot_id}
    
    raise HTTPException(status_code=404, detail="Bot not found")

@app.post("/api/bots/{bot_id}/stop")
async def stop_bot(bot_id: str):
    # Stop the bot
    success = await bot_manager.stop_bot(bot_id)
    
    if success:
        # Update status in database
        supabase.table("discord_bots").update(
            {"status": "inactive"}
        ).eq("id", bot_id).execute()
        
        return {"status": "stopped", "bot_id": bot_id}
    
    raise HTTPException(status_code=404, detail="Bot not found or not running")