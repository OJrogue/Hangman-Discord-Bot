from os import getenv
import random
from discord import Intents, Message
from discord.ext import commands
from discord.ext.commands import Context
from dotenv import load_dotenv


load_dotenv()
TOKEN = getenv("TOKEN")


intents = Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!", case_insensitive=True, intents=intents
)


@bot.event
async def on_ready() -> None:
    print(f'Signed in as {bot.user}')


class Hangman:
    def __init__(self, username) -> None:

        try:
            # Gets a random word from words.txt file for hangman game
            with open('words.txt', 'r') as content_file:
                self.word = random.choice(content_file.read().split('\n'))
        except FileNotFoundError:
            raise FileNotFoundError(
                "File words.txt not found, the game will not function")

        self.username = username
        self.letters = []
        self.lives = 7
        self.guessing_word = '-' * len(self.word)
        self.state = ''
        self.finished = False

    def play(self, letter):

        if len(letter) != 1:
            self.state = "Enter only 1 letter at a time."

        # alerady guessed letter
        elif letter in self.letters:
            self.state = "You already guessed that."

        # guessing new letter
        elif letter not in self.word:
            self.letters.append(letter)
            self.lives -= 1
            if self.lives == 0:
                self.finished = True
                self.state = f'You lost! The word was: {self.word}'
            else:
                self.state = "Wrong guess."

        else:
            self.letters.append(letter)

            indexes = []
            for i in range(len(self.word)):
                if self.word[i] == letter:
                    indexes.append(i)

            for i in indexes:
                gw = list(self.guessing_word)
                gw[i] = letter
                self.guessing_word = "".join(gw)

            if self.guessing_word == self.word:
                self.finished = True
                self.state = "You won!"
            else:
                self.state = "Correct guess."

        return self.return_message()

    def return_message(self):
        guessing_word = ''
        for letter in self.guessing_word:
            guessing_word += letter + " "
        message = f'**Hangman**\nPlayer: {self.username}\
            \nGuesses: {", ".join(self.letters).upper()}\
            \nLives: {self.lives}\nWord: {guessing_word.upper()}'
        if self.state:
            message += f'\n{self.state}'
        return message


instances = {}


@bot.command(name="play_hangman")
async def play_hangman(ctx: Context) -> None:
    instances[ctx.author.id] = Hangman(
        username=ctx.author.name)
    message = await ctx.channel.send(instances[ctx.author.id].return_message())
    instances[ctx.author.id].message = message


@bot.command(name="guess")
async def guess(ctx: Context, letter: str) -> None:
    hangman_instance = instances[ctx.author.id]
    if hangman_instance.finished:
        await ctx.channel.send("You have to start a new game first.")
        return
    await hangman_instance.message.edit(content=hangman_instance.play(letter.lower()))
    await ctx.message.delete()


bot.run(TOKEN)
