import random
import time

import discord
from discord.ext import commands
from discord.ui import Button, View
import pymorphy2

FLAG = {'game': False, 'word': '', 'history': []}
words = [i.rstrip() for i in open('word.txt').readlines()]

bot = commands.Bot(command_prefix='!', intents=discord.Intents.default())


@bot.event
async def on_ready():
    print("Я запущен!")


@bot.command()
async def rand(ctx, *arg):
    await ctx.reply(random.randint(0, 100))


commands = ['привет, бот!', 'привет', 'hi', 'hello']


@bot.event
async def on_message(message):
    command = message.content.lower()
    if command in commands:
        if message.author != bot.user:
            await message.channel.send(f'Привет, {message.author.mention}!')
            await message.channel.send(f'Попробуй написать !find  и найди правильную кнопку для продолжения')
    if command == '!wordgame':
        view = Wordgame()
        await message.channel.send(view=view)

    if command == '!find':
        view = Menu()
        await message.channel.send(view=view)

    if FLAG['game'] and message.author != bot.user:
        print(FLAG['word'], command)
        if FLAG['word'][-1].lower() == command[0].lower():
            FLAG['history'].append(command.lower())
            await message.channel.send(view=Wordgame())


class Wordgame(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label='"слова"', style=discord.ButtonStyle.green)
    async def menu1(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Следущее слово:")
        FLAG['game'] = True
        FLAG['word'] = random.choice(words).lower()
        if not FLAG['history']:
            FLAG['history'].append(FLAG['word'].replace('ь', '').replace('ы', ''))
            await interaction.followup.send(FLAG['word'])

            return
        while FLAG['word'][0] != FLAG['history'][-1][-1]:
            FLAG['word'] = random.choice(words)

        else:
            await interaction.followup.send(FLAG['word'])
            FLAG['history'].append(FLAG['word'].replace('ь', '').replace('ы', ''))
            if len(FLAG['word']) > 1:
                await interaction.followup.send(random.choice(['Не надоело?', 'Я могу долго так играть', 'Может сдашься?']))

    @discord.ui.button(label='Сдаться', style=discord.ButtonStyle.red)
    async def button5(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Поздравляю! Вы проиграли бездушной машине")

class Menu(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label='Серая кнопка', style=discord.ButtonStyle.grey)
    async def button1(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Мимо!")

    @discord.ui.button(label='Зеленая кнопка', style=discord.ButtonStyle.green)
    async def button2(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Мимо!")

    @discord.ui.button(label='Красная кнопка', style=discord.ButtonStyle.red)
    async def button3(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Попал! Теперь пиши !wordgame")

    @discord.ui.button(label='Красная кнопка', style=discord.ButtonStyle.primary)
    async def button4(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Мимо!")


@bot.command()
async def wordgame(ctx):
    view = Wordgame()
    await ctx.reply(view=view)


@bot.command()
async def buttons(ctx):
    view = Menu()
    await ctx.reply(view=view)


TOKEN = 'MTEwMDgyNzQ2MjQ2NTc2MTM1Mg.Gamih-.W8B7CtBR3Jn2CvjcjaN0lHIyhuuuuN6RotKHuc'
bot.run(TOKEN)
