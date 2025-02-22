from discord import Interaction, TextStyle
from discord.ui import Modal, TextInput
import discord

from plugins.trivia.supportfiles.database import trivia_database
        

class answers(Modal, title='Answers'):
    def __init__(self):
        super().__init__()
        self.location = None
        self.question = None
        self.database = trivia_database()
        self.question_type = ""
        

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

    fake_four = TextInput(
        label='Fake answer 4 (optional)',
        placeholder="A fake answer goes here.",
        style=TextStyle.short,
        required=False,
        max_length=38
    )

    async def on_submit(self, interaction: Interaction):
        #self.config = dict(self.config[0])
        real_answer = self.real_answer.value
        fake_one = self.fake_one.value
        fake_two = self.fake_two.value
        fake_three = self.fake_three.value
        fake_four = self.fake_four.value

        await interaction.response.send_message("Question Submitted", ephemeral=True)

        await self.database.add_question(question=self.question, question_type=self.question_type,
                                         real_answer=real_answer,
                                         fake_answer_one=fake_one,
                                         fake_answer_two=fake_two,
                                         fake_answer_three=fake_three,
                                         fake_answer_four=fake_four,
                                         submitted_by=interaction.user.id,
                                         file_url=self.location)
