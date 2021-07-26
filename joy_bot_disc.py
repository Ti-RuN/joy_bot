import discord
from discord.ext import commands
from config import settings
from lexicon_bot import forbidden_words
from lexicon_bot import lex_bot
import random
from asyncio import sleep
from discord.utils import get


intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=settings["prefix"], intents=intents)
bot.remove_command("help")


@bot.event
async def on_ready():
    print("We have logged in as {0.user}".format(bot))
    while True:  # меняет свой статус
        await bot.change_presence(status=discord.Status.online,
                                  activity=discord.Activity(type=discord.ActivityType.listening, name="ветер"))
        await sleep(20)
        await bot.change_presence(status=discord.Status.online, activity=discord.Game("жизнь"))
        await sleep(20)


# присваивает роль зашедшему на сервер
@bot.event
async def on_member_join(member):
    channel = bot.get_channel(702835048227012612)  # id канала

    role = discord.utils.get(member.guild.roles, id=865237845315551255)  # id роли на сервере

    await member.add_roles(role)
    await channel.send(embed=discord.Embed(discription=f"Пользователь{member.name}, прис"))  # не работает, почему??? "Ignoring exception in on_member_join"


@bot.event
async def on_message(message):
    msg = message.content.lower()
    if msg in forbidden_words:  # не удаляет сообщение если в месте с кл.словом есть другой текст испр!!!
        await message.delete()
        await message.author.send(
            f"Вождь следит за тобой {message.author.name}, не используй в чате '{msg}', а то получишь по жопке!"
        )
    if msg in lex_bot["greeting"]:
        await message.channel.send("{} пидор".format(lex_bot["greeting"][random.randrange(0, 18)]))  # (если убрать текс зацикливается ответ)узнать как сделать рандомное значение из списка???

    await bot.process_commands(message)  # ????


@bot.command()  # тестовая команда
async def ping(ctx):
    author = ctx.message.author  # отправляет ответ
    await ctx.send(f"{author.mention}pong")  # с упоминанием отпрвавителя


@bot.command()
async def pin(ctx, arg, amount=1):
    await ctx.channel.purge(limit=amount)  # удаляет команду ($pin)
    author = ctx.message.author  # отправляет ответ
    await ctx.send(f"{author.mention}" + arg)  # с упоминанием отпрвавителя


# команды администратора
@bot.command()
@commands.has_permissions(administrator=True)
async def help_admin(ctx, amount=1):
    await ctx.channel.purge(limit=amount)
    emb = discord.Embed(title="Команды Joy бота", color=15105570)

    emb.add_field(name="{}help".format(settings["prefix"]), value="Команды бота для пользователей.")
    emb.add_field(name="{}leave_voice".format(settings["prefix"]), value="покинул")
    emb.add_field(name="{}clear".format(settings["prefix"]), value="Очистка чата от 1 до 100 сообщений.")
    emb.add_field(name="{}join_voice".format(settings["prefix"]),
                  value="Добавить бота к себе в голосовой канал.")
    emb.add_field(name="{}leave_voice".format(settings["prefix"]),
                  value="Удалить бота из голосового чата.")

    author = ctx.author
    await ctx.send(f"{author.mention}", embed=emb)


# удаляет сообщения
@bot.command()
@commands.has_permissions(administrator=True)
async def clear(ctx, amount=100):
    await ctx.channel.purge(limit=amount)


# команды пользователя
@bot.command()
async def help(ctx, amount=1):
    await ctx.channel.purge(limit=amount)
    emb = discord.Embed(title="Навигация", description="https://qna.habr.com/", url="https://qna.habr.com/", color=0x00ff00)

    emb.add_field(name="{}join_voice".format(settings["prefix"]),
                  value="Добавить бота к себе в голосовой канал.")
    emb.add_field(name="{}clear".format(settings["prefix"]), value="Очистка чата")
    emb.add_field(name="{}clear".format(settings["prefix"]), value="Очистка чата")
    emb.add_field(name="{}clear".format(settings["prefix"]), value="Очистка чата")

    emb.set_image(url="https://bit.ly/3elGRWo")
    emb.set_footer(text=",kf", icon_url=ctx.author.avatar_url)
    emb.set_image(url="http://joyreactor.cc/images/joyreactor_logo.png")
    emb.add_field(name="{}join_voice".format(settings["prefix"]),
                  value="Добавить бота к себе в голосовой канал.")
    emb.add_field(name="{}leave_voice".format(settings["prefix"]),
                  value="Удалить бота из голосового чата.")

    author = ctx.author
    await ctx.send(f"{author.mention}", embed=emb)


# добавить бота в голосовой канал
@bot.command()
async def join_voice(ctx, amount=1):
    await ctx.channel.purge(limit=amount)
    channel = ctx.message.author.voice.channel
    if not channel:  # не проверяет наличе наканале отправителя !
        await ctx.send("You are not connected to a voice channel")
        return
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        await channel.connect()
    await ctx.send(f"Вождь на канале '{channel}', ликуйте пидоры.")


# удаляет бота из голосового канала
@bot.command()
async def leave_voice(ctx, amount=1):  # есть баги
    await ctx.message.channel.purge(limit=amount)
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.disconnect()
        await ctx.send(f"Вождь покинул канал '{channel}'.")


bot.run(settings["token"])
