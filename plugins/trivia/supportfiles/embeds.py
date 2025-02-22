from discord import Embed
import json

class triva_embeds():
    def __init__(self):
        pass

    with open('./plugins/trivia/embeds.json', 'r') as f:
        config_embed_settings = json.load(f)
    
    async def question(self, question:str):
        embed_settings = self.config_embed_settings['question']

        embed = Embed(title=question,
                      description="You get a bonus point if you don't view the options!",
                      color=int(embed_settings['color'], base=16))

        return embed