from discord.ui import View,Button,button
from discord import ButtonStyle, Interaction
from plugins.trivia.supportfiles.database import trivia_database
import random


class trivia_options_buttons(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.question = None
        self.database = trivia_database()

    @button(label='view options', style=ButtonStyle.green)
    async def view_options(self, interaction: Interaction, button: Button):
        question = self.question
        answer_buttons = trivia_answers_buttons()
        answer_buttons.correct_answer = question['real_answer']
        answer_buttons.answers.append(question['real_answer'])
        answer_buttons.answers.append(question['fake_answer_one'])
        answer_buttons.answers.append(question['fake_answer_two'])
        answer_buttons.answers.append(question['fake_answer_three'])

        answer_buttons.clear_items()
        answer_buttons.add_item(answer_buttons.answer_one)
        answer_buttons.add_item(answer_buttons.answer_two)
        answer_buttons.add_item(answer_buttons.answer_three)
        answer_buttons.add_item(answer_buttons.answer_four)
        
        answer_buttons.answer_one.label = answer_buttons.answers[0]
        answer_buttons.answer_two.label = answer_buttons.answers[1]
        answer_buttons.answer_three.label = answer_buttons.answers[2]
        answer_buttons.answer_four.label = answer_buttons.answers[3]

        if question['fake_answer_four']:
            answer_buttons.answers.append(question['fake_answer_four'])
            answer_buttons.add_item(answer_buttons.answer_five)

        random.shuffle(answer_buttons.answers)



        await interaction.message.edit(view=None)
        await interaction.response.send_message(view=answer_buttons, ephemeral=True)



class trivia_answers_buttons(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.answers = []
        self.correct_answer = None
        self.answered = False

    @button(label='answer_one', style=ButtonStyle.green, row=0)
    async def answer_one(self, interaction: Interaction, button: Button):
        if self.answered:
            await interaction.response.send_message("You've already answered this question.", ephemeral=True)
            return
        
        if self.answer_one.label == self.correct_answer:
            await interaction.response.send_message("That's correct!", ephemeral=True)
            self.answered = True
        else:
            await interaction.response.send_message("That's not correct", ephemeral=True)


    @button(label='answer_two', style=ButtonStyle.green, row=0)
    async def answer_two(self, interaction: Interaction, button: Button):
        if self.answered:
            await interaction.response.send_message("You've already answered this question.", ephemeral=True)
            return
        
        if self.answer_two.label == self.correct_answer:
            await interaction.response.send_message("That's correct!", ephemeral=True)
            self.answered = True
        else:
            await interaction.response.send_message("That's not correct", ephemeral=True)

    @button(label='answer_three', style=ButtonStyle.green, row=1)
    async def answer_three(self, interaction: Interaction, button: Button):
        if self.answered:
            await interaction.response.send_message("You've already answered this question.", ephemeral=True)
            return
        
        if self.answer_three.label == self.correct_answer:
            await interaction.response.send_message("That's correct!", ephemeral=True)
            self.answered = True
        else:
            await interaction.response.send_message("That's not correct", ephemeral=True)

    @button(label='answer_four', style=ButtonStyle.green, row=1)
    async def answer_four(self, interaction: Interaction, button: Button):
        if self.answered:
            await interaction.response.send_message("You've already answered this question.", ephemeral=True)
            return
        
        if self.answer_four.label == self.correct_answer:
            await interaction.response.send_message("That's correct!", ephemeral=True)
            self.answered = True
        else:
            await interaction.response.send_message("That's not correct", ephemeral=True)

    @button(label='answer_five', style=ButtonStyle.green, row=1)
    async def answer_five(self, interaction: Interaction, button: Button):
        if self.answered:
            await interaction.response.send_message("You've already answered this question.", ephemeral=True)
            return
        
        if self.answer_five.label == self.correct_answer:
            await interaction.response.send_message("That's correct!", ephemeral=True)
            self.answered = True
        else:
            await interaction.response.send_message("That's not correct", ephemeral=True)