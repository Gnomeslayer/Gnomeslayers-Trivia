import json

from discord.ext.commands import Bot, Cog
from discord.ext import tasks
from discord import app_commands
from discord.interactions import Interaction
from discord.app_commands import guild_only, Choice
from typing import List


from plugins.trivia.supportfiles.modals import answers
from plugins.trivia.supportfiles.buttons import trivia_options_buttons
from plugins.trivia.supportfiles.database import trivia_database
from plugins.trivia.supportfiles.embeds import trivia_embeds

import uuid
import random
import discord


class commands(Cog):
    def __init__(self, bot: Bot, tokens:dict):
        print("[Cog] Trivia Commands has been initiated")
        self.bot = bot
        self.tokens = tokens
        self.embed_factory = trivia_embeds(bot)
        self.functions = None
        self.database = trivia_database()
        self.trivia_running = False
        self.correct_answer = ""
        self.hints_buttons = None
        self.trivia_questions = []
        self.trivia_channel = None
        self.categories = []
        
    with open('./plugins/trivia/settings.json', 'r') as f:
        config = json.load(f)

    async def cog_load(self):
        pass

    # Create a command group
    trivia_group = app_commands.Group(name="trivia", description="Test command group")

    async def autocomplete(self, interaction: discord.Interaction, current: str) -> List[Choice[str]]:
        """Provide autocomplete suggestions for player names."""

        if current:
            choicelist = [category for category in self.categories if current.lower() in category.lower()][:20]
            return [Choice(name=c, value=c) for c in choicelist]
        else:
            default = ["Start typing a category"]
            return [Choice(name=d, value=d) for d in default]

    async def cog_load(self):
        try:
            self.categories = await self.database.get_all_categories()
        except Exception as e:
            pass

    @Cog.listener()
    async def on_message(self, message:discord.Message):
        if message.author.bot:
            return
        
        if not self.trivia_running:
            return
        
        if message.content.lower() == self.correct_answer.lower():
            if not message.author.id in self.hints_buttons.already_answered:
                if not message.author.id in self.hints_buttons.viewed_hints:
                    await message.channel.send("Correct! Double points for you!")
                    self.hints_buttons.already_answered.append(message.author.id)
                    await self.database.update_player(discord_id=message.author.id, add_point=True, add_double=True)
                else:
                    await message.channel.send("Correct! However you viewed the hints, single point!")
                    await self.database.update_player(discord_id=message.author.id, add_point=True)
                    self.hints_buttons.already_answered.append(message.author.id)
            else:
                await message.channel.send("You've already answered!")

    @trivia_group.command()
    async def add_category(self, interaction:Interaction, category:str):
        roles = interaction.user.roles
        proceed = False
        for role in roles:
            if role.id in self.config['roles_that_can_add_questions']:
                proceed = True
                break
        
        if not proceed:
            await interaction.response.send_message("You do not have permission to run this command!", ephemeral=True)
            return
        
        if category in self.categories:
            await interaction.response.send_message("That category is already there.")
        else:
            await interaction.response.send_message("Added category!")
            self.categories.append(category)
        

    @trivia_group.command()
    @app_commands.autocomplete(category=autocomplete)
    async def add_audio_question(self, interaction:Interaction, question:str, audio_file:discord.Attachment, category:str=None):
        roles = interaction.user.roles
        proceed = False
        for role in roles:
            if role.id in self.config['roles_that_can_add_questions']:
                proceed = True
                break
        
        if not proceed:
            await interaction.response.send_message("You do not have permission to run this command!", ephemeral=True)
            return
    
        if not category:
            category = "General"

        if audio_file.content_type and audio_file.content_type.startswith('audio/'):
            # You can download or process the file here if needed

            
            modal = answers()
            modal.question = question
            modal.question_type = "audio"
            modal.category = category
            modal.file = audio_file
            await interaction.response.send_modal(modal)
        else:
            await interaction.response.send_message("Please upload a valid audio file.", ephemeral=True)

    @trivia_group.command()
    @app_commands.autocomplete(category=autocomplete)
    async def add_image_question(self, interaction:Interaction, question:str, image_file:discord.Attachment, category:str = None):
        roles = interaction.user.roles
        proceed = False
        for role in roles:
            if role.id in self.config['roles_that_can_add_questions']:
                proceed = True
                break
        
        if not proceed:
            await interaction.response.send_message("You do not have permission to run this command!", ephemeral=True)
            return
    
        if not category:
            category = "General"
        if image_file.content_type and image_file.content_type.startswith('image/'):
            modal = answers()
            modal.question = question
            modal.question_type = "image"
            modal.category = "General"
            modal.file = image_file
            await interaction.response.send_modal(modal)

        else:
            await interaction.response.send_message("Please upload a valid image file.", ephemeral=True)

    @trivia_group.command()
    @app_commands.autocomplete(category=autocomplete)
    async def add_question(self, interaction:Interaction, question:str, category:str = None):
        roles = interaction.user.roles
        proceed = False
        for role in roles:
            if role.id in self.config['roles_that_can_add_questions']:
                proceed = True
                break
        
        if not proceed:
            await interaction.response.send_message("You do not have permission to run this command!", ephemeral=True)
            return
    
        if not category:
            category = "General"
        modal = answers()
        modal.question = question
        modal.question_type = "general"
        modal.category = category
        await interaction.response.send_modal(modal)

    
    @trivia_group.command()
    @app_commands.autocomplete(category=autocomplete)
    async def start(self, interaction:Interaction, interval_seconds:int = None, channel:discord.TextChannel = None, category:str=None):
        roles = interaction.user.roles
        proceed = False
        for role in roles:
            if role.id in self.config['roles_that_can_start_stop_trivia']:
                proceed = True
                break
        
        if not proceed:
            await interaction.response.send_message("You do not have permission to run this command!", ephemeral=True)
            return
    
        await interaction.response.defer(ephemeral=True)
        if not channel:
            try:
                channel = self.bot.get_channel(self.config['trivia_channel_id'])
            except Exception as e:
                await interaction.response.send_message("No trivia channel set, trivia will not commence!", ephemeral=True)
        
        self.trivia_channel = channel

        if not self.trivia_running:
            if not interval_seconds:
                
                await interaction.followup.send(f"Starting trivia! A new question will appear every 30 seconds in the channel {channel.mention}!", ephemeral=True)
            else:
                await interaction.followup.send(f"Starting trivia! A new question will appear every {interval_seconds} seconds in the channel {channel.mention}!", ephemeral=True)
                self.trivia.change_interval(seconds=interval_seconds)

            self.trivia_running = True
            if category:
                questions = await self.database.get_all_questions(category=category)
            else:
                questions = await self.database.get_all_questions()

            if not questions:
                await interaction.followup.send("There are no questions to show. Trivia will not commence.", ephemeral=True)
                return
            
            for question in questions:
                self.trivia_questions.append(question)
                random.shuffle(self.trivia_questions)

            self.trivia.start()
        else:
            await interaction.followup.send("Trivia is already running..", ephemeral=True)
            return

    @trivia_group.command()
    async def stop(self, interaction:Interaction):
        roles = interaction.user.roles
        proceed = False
        for role in roles:
            if role.id in self.config['roles_that_can_start_stop_trivia']:
                proceed = True
                break
        
        if not proceed:
            await interaction.response.send_message("You do not have permission to run this command!", ephemeral=True)
            return
    
        if not self.trivia_running:
            await interaction.response.send_message("Trivia is not running!", ephemeral=True)
            return
        
        await interaction.response.send_message("Stopping trivia!", ephemeral=True)
        self.trivia.stop()
        self.trivia_running = False
        self.trivia_questions = None

    @trivia_group.command()
    async def update(self, interaction:Interaction):
        if not self.trivia_running:
            await interaction.response.send_message("The trivia questions will update when it is started.", ephemeral=True)
            return
        
        questions = await self.database.get_all_questions()

        for question in questions:
            if not question in self.trivia_questions:
                self.trivia_questions.append(question)
                random.shuffle(self.trivia_questions)

    @tasks.loop(seconds=30)
    async def trivia(self):
        question = None

        if self.correct_answer:
            await self.trivia_channel.send(f"The correct answer was: `{self.correct_answer}`, did you guess it right?")

        for q in self.trivia_questions:
            if not q['shown']:
                q['shown'] = True
                question = q
                break

        random.shuffle(self.trivia_questions)

        if not question:
            await self.trivia_channel.send("There are no more questions to show. You've seen them all! Trivia will now end!")
            self.trivia_running = False
            self.trivia.stop()
            return
        
        button = trivia_options_buttons()
        button.question = question

        file = None

        trivia_embed = await self.embed_factory.question(question=question)
        self.correct_answer = question['real_answer']

        if question['file_url']:
            if question['question_type'] == "audio":
                file_name = question['file_url'].split('audiofiles/')[1]
            elif question['question_type'] == "image":
                file_name = question['file_url'].split('imagefiles/')[1]
            file = discord.File(question['file_url'], filename=f'{file_name}')

        self.hints_buttons = button
        if file:
            await self.trivia_channel.send(embed=trivia_embed, view=button, file=file)
        else:
            await self.trivia_channel.send(embed=trivia_embed, view=button)