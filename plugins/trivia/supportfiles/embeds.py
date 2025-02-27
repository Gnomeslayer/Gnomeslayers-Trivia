from discord import Embed
import json
from discord.ext.commands import Bot

class trivia_embeds():
    def __init__(self, bot: Bot):
        self.bot:Bot = bot

    with open('./plugins/trivia/embeds.json', 'r') as f:
        config_embed_settings = json.load(f)
    
    async def question(self, question:str):
        embed_settings = self.config_embed_settings['question']

        embed = Embed(title=question['question'],
                      description="You get a bonus point if you don't view the options!",
                      color=int(embed_settings['color'], base=16))
        
        submitted_by = self.bot.get_user(int(question['submitted_by']))
        embed.add_field(name="Question info", value=f"Category: {question['category']}\nsubmitted by: {submitted_by.mention}")

        return embed
    
    async def report_embed(self, reporter, reason, question_number):
        embed_settings = self.config_embed_settings['report']

        embed = Embed(title="Question Reported",
                      color=int(embed_settings['color'], base=16))
        
        embed.add_field(name="Reporter", value=reporter, inline=False)
        embed.add_field(name="Reason", value=reason, inline=False)
        embed.add_field(name="Question Number", value=question_number, inline=False)

        return embed