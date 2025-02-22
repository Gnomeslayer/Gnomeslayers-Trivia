import json

from discord.ext.commands import Bot, Cog
from discord import app_commands
from discord.interactions import Interaction
from discord.app_commands import guild_only

class trivia(Cog):
    def __init__(self, bot: Bot, tokens:dict):
        print("[Cog] Trivia has been initiated")
        self.bot = bot
        self.tokens = tokens
        self.embed_factory = None
        self.functions = None
        
    with open('./plugins/trivia/settings.json', 'r') as f:
        config = json.load(f)

    async def cog_load(self):
        pass