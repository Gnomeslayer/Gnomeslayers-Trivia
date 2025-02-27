from discord.ui import View,Button,button
from discord import ButtonStyle, Interaction
from plugins.trivia.supportfiles.database import trivia_database
from plugins.trivia.supportfiles.modals import report
import random


class trivia_options_buttons(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.question = None
        self.database = trivia_database()
        self.viewed_hints = []
        self.already_answered = []

    @button(label='view options', style=ButtonStyle.green)
    async def view_options(self, interaction: Interaction, button: Button):
        if interaction.user.id in self.viewed_hints:
            await interaction.response.send_message("You've already viewed the hints!", ephemeral=True)
            return
        
        if interaction.user.id in self.already_answered:
            await interaction.response.send_message("You've already answered the question!", ephemeral=True)
            return
        
        self.viewed_hints.append(interaction.user.id)
        question = self.question
        answer_buttons = trivia_answers_buttons()
        answer_buttons.question_number = question['id']
        answer_buttons.correct_answer = question['real_answer']
        answer_buttons.answers.append(question['real_answer'])
        answer_buttons.answers.append(question['fake_answer_one'])
        answer_buttons.answers.append(question['fake_answer_two'])
        answer_buttons.answers.append(question['fake_answer_three'])

        random.shuffle(answer_buttons.answers)
        
        answer_buttons.answer_one.label = answer_buttons.answers[0]
        answer_buttons.answer_two.label = answer_buttons.answers[1]
        answer_buttons.answer_three.label = answer_buttons.answers[2]
        answer_buttons.answer_four.label = answer_buttons.answers[3]

        #await interaction.message.edit(view=None)

        answer_buttons.hintbuttons = self
        await interaction.response.send_message(view=answer_buttons, ephemeral=True)



class trivia_answers_buttons(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.answers = []
        self.correct_answer = None
        self.answered = False
        self.question_number = 0
        self.hintbuttons:trivia_options_buttons = None
        self.database = trivia_database()

    #@button(label="Report this question", style=ButtonStyle.red, row=0)
    #async def report_question(self, interaction:Interaction, button:Button):
    #    report_modal = report()
    #    report_modal.question_number = self.question_number
#
    #    await interaction.response.send_modal(report_modal)

    @button(label='answer_one', style=ButtonStyle.green, row=1)
    async def answer_one(self, interaction: Interaction, button: Button):

        if interaction.user.id in self.hintbuttons.already_answered:
            await interaction.response.send_message("You've already answered this question.", ephemeral=True)
            return
        
        if self.answer_one.label == self.correct_answer:
            await interaction.response.send_message("That's correct!", ephemeral=True)
            await self.database.update_player(discord_id=interaction.user.id, add_point=True)
            self.hintbuttons.already_answered.append(interaction.user.id)
        else:
            await interaction.response.send_message("That's not correct", ephemeral=True)
            self.hintbuttons.already_answered.append(interaction.user.id)


    @button(label='answer_two', style=ButtonStyle.green, row=2)
    async def answer_two(self, interaction: Interaction, button: Button):
        if interaction.user.id in self.hintbuttons.already_answered:
            await interaction.response.send_message("You've already answered this question.", ephemeral=True)
            return
        
        if self.answer_two.label == self.correct_answer:
            await interaction.response.send_message("That's correct!", ephemeral=True)
            await self.database.update_player(discord_id=interaction.user.id, add_point=True)
            self.hintbuttons.already_answered.append(interaction.user.id)
        else:
            await interaction.response.send_message("That's not correct", ephemeral=True)
            self.hintbuttons.already_answered.append(interaction.user.id)

    @button(label='answer_three', style=ButtonStyle.green, row=3)
    async def answer_three(self, interaction: Interaction, button: Button):
        if interaction.user.id in self.hintbuttons.already_answered:
            await interaction.response.send_message("You've already answered this question.", ephemeral=True)
            return
        
        if self.answer_three.label == self.correct_answer:
            await interaction.response.send_message("That's correct!", ephemeral=True)
            await self.database.update_player(discord_id=interaction.user.id, add_point=True)
            self.hintbuttons.already_answered.append(interaction.user.id)
        else:
            await interaction.response.send_message("That's not correct", ephemeral=True)
            self.hintbuttons.already_answered.append(interaction.user.id)

    @button(label='answer_four', style=ButtonStyle.green, row=4)
    async def answer_four(self, interaction: Interaction, button: Button):
        if interaction.user.id in self.hintbuttons.already_answered:
            await interaction.response.send_message("You've already answered this question.", ephemeral=True)
            return
        
        if self.answer_four.label == self.correct_answer:
            await interaction.response.send_message("That's correct!", ephemeral=True)
            await self.database.update_player(discord_id=interaction.user.id, add_point=True)
            self.hintbuttons.already_answered.append(interaction.user.id)
        else:
            await interaction.response.send_message("That's not correct", ephemeral=True)
            self.hintbuttons.already_answered.append(interaction.user.id)