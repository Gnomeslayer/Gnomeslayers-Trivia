import json

from discord.ext.commands import Bot, Cog
from discord import app_commands
from discord.interactions import Interaction
from discord.app_commands import guild_only
import discord

from plugins.trivia.supportfiles.modals import answers
from plugins.trivia.supportfiles.buttons import trivia_options_buttons
from plugins.trivia.supportfiles.database import trivia_database
from plugins.trivia.supportfiles.embeds import triva_embeds

import uuid

class commands(Cog):
    def __init__(self, bot: Bot, tokens:dict):
        print("[Cog] Trivia Commands has been initiated")
        self.bot = bot
        self.tokens = tokens
        self.embed_factory = triva_embeds()
        self.functions = None
        self.database = trivia_database()
        
    with open('./plugins/trivia/settings.json', 'r') as f:
        config = json.load(f)

    async def cog_load(self):
        pass

    # Create a command group
    trivia_group = app_commands.Group(name="trivia", description="Test command group")


    @trivia_group.command()
    async def test_question(self, interaction:Interaction, question_number:str):
        question = await self.database.get_specific_question(question_number)
        if not question:
            await interaction.response.send_message("That question doesnt exist.", ephemeral=True)
            return
        button = trivia_options_buttons()
        button.question = question

        file = None

        trivia_embed = await self.embed_factory.question(question=question['question'])

        if question['file_url']:
            if question['question_type'] == "audio":
                file_name = question['file_url'].split('audiofiles/')[1]
            elif question['question_type'] == "image":
                file_name = question['file_url'].split('imagefiles/')[1]
            file = discord.File(question['file_url'], filename=f'{file_name}')

        if file:
            await interaction.response.send_message(embed=trivia_embed, view=button, file=file)
        else:
            await interaction.response.send_message(embed=trivia_embed, view=button)
        

    @trivia_group.command()
    async def add_audio_question(self, interaction:Interaction, question:str, audio_file:discord.Attachment):

        if audio_file.content_type and audio_file.content_type.startswith('audio/'):
            # You can download or process the file here if needed
            audio_data = await audio_file.read()
            file_name = audio_file.filename
            file_extension = file_name.split('.')[1]
            file_name = f"{uuid.uuid4()}.{file_extension}"

            location = f"./plugins/trivia/audiofiles/{file_name}"
            with open(location, 'wb') as f:
                f.write(audio_data)
            
            modal = answers()
            modal.question = question
            modal.location = location
            modal.question_type = "audio"
            await interaction.response.send_modal(modal)
        else:
            await interaction.response.send_message("Please upload a valid audio file.", ephemeral=True)

    @trivia_group.command()
    async def add_image_question(self, interaction:Interaction, question:str, image_file:discord.Attachment):
        if image_file.content_type and image_file.content_type.startswith('image/'):

            file_name = image_file.filename
            file_extension = file_name.split('.')[1]
            file_name = f"{uuid.uuid4()}.{file_extension}"

            location = f"./plugins/trivia/imagefiles/{file_name}"
            # You can download or process the image here if needed
            image_data = await image_file.read()
            # Save the image locally if needed
            with open(location, 'wb') as f:
                f.write(image_data)

            modal = answers()
            modal.question = question
            modal.location = location
            modal.question_type = "image"
            await interaction.response.send_modal(modal)

        else:
            await interaction.response.send_message("Please upload a valid image file.", ephemeral=True)

    @trivia_group.command()
    async def add_question(self, interaction:Interaction, question:str):
        modal = answers()
        modal.question = question
        modal.question_type = "general"
        await interaction.response.send_modal(modal)