from discord import Interaction, TextStyle
from discord.ui import Modal, TextInput
import discord

from plugins.trivia.supportfiles.database import trivia_database
from plugins.trivia.supportfiles.embeds import trivia_embeds
import json

import uuid
        

class report(Modal, title="Report"):
    def __init__(self):
        super().__init__()
        self.question_number = 0
        self.embed_factory = trivia_embeds()
        
    
    reason = TextInput(
        label="Reason for reporting",
        placeholder="Put your reason here.",
        style=TextStyle.long,
        required=True
    )

    async def on_submit(self, interaction: Interaction):
        #self.config = dict(self.config[0])
        reason = self.reason.value
        with open('./plugins/trivia/settings.json', 'r') as f:
            config = json.load(f)
        
        report_channel = interaction.guild.get_channel(config['report_channel_id'])

        embed = await self.embed_factory.report_embed(reporter=interaction.user, reason=reason, question_number=self.question_number)

        await report_channel.send(embed=embed)
        await interaction.response.send_message("I've sent the report in!", ephemeral=True)


class answers(Modal, title='Answers'):
    def __init__(self):
        super().__init__()
        self.question = None
        self.database = trivia_database()
        self.question_type = ""
        self.category = "General"
        self.file:discord.Attachment = None
        

    real_answer = TextInput(
        label='Real answer here please',
        placeholder="The real answer goes here.",
        style=TextStyle.short,
        required=True,
        max_length=38
    )

    fake_one = TextInput(
        label='Fake answer 1',
        placeholder="A fake answer goes here.",
        style=TextStyle.short,
        required=True,
        max_length=38
    )
    
    fake_two = TextInput(
        label='Fake answer 2',
        placeholder="A fake answer goes here.",
        style=TextStyle.short,
        required=True,
        max_length=38
    )

    fake_three = TextInput(
        label='Fake answer 3',
        placeholder="A fake answer goes here.",
        style=TextStyle.short,
        required=True,
        max_length=38
    )

    async def on_submit(self, interaction: Interaction):
        #self.config = dict(self.config[0])
        real_answer = self.real_answer.value
        fake_one = self.fake_one.value
        fake_two = self.fake_two.value
        fake_three = self.fake_three.value

        await interaction.response.send_message("Question Submitted", ephemeral=True)

        if self.file:
            file_data = await self.file.read()
            file_name = self.file.filename
            file_extension = file_name.split('.')[1]
            file_name = f"{uuid.uuid4()}.{file_extension}"

            if self.question_type == "audio":
                location = f"./plugins/trivia/audiofiles/{file_name}"
            elif self.question_type == "image":
                location = f"./plugins/trivia/imagefiles/{file_name}"

            with open(location, 'wb') as f:
                f.write(file_data)

        await self.database.add_question(question=self.question, question_type=self.question_type,
                                         real_answer=real_answer,
                                         fake_answer_one=fake_one,
                                         fake_answer_two=fake_two,
                                         fake_answer_three=fake_three,
                                         submitted_by=interaction.user.id,
                                         file_url=location,
                                         category=self.category)
