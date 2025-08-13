import asyncio
import discord
from typing import Dict

class BotInstance:
    def __init__(self, bot_id: str, token: str):
        self.bot_id = bot_id
        self.client = discord.Client(intents=discord.Intents.default())
        self.token = token
        
    async def start(self):
        await self.client.start(self.token)
        
    async def stop(self):
        await self.client.close()

class BotManager:
    def __init__(self):
        self.bots: Dict[str, BotInstance] = {}
        
    async def start_bot(self, bot_id: str, token: str):
        if bot_id not in self.bots:
            bot = BotInstance(bot_id, token)
            self.bots[bot_id] = bot
            asyncio.create_task(bot.start())
            return True
        return False
        
    async def stop_bot(self, bot_id: str):
        if bot_id in self.bots:
            await self.bots[bot_id].stop()
            del self.bots[bot_id]
            return True
        return False

# This will be integrated with your FastAPI backend later
bot_manager = BotManager()