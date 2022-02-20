import discord, API
import pafy, urllib
import re, time
import random
from discord.voice_client import VoiceClient
from discord.ext import commands
import os
from io import BytesIO
from io import BufferedIOBase
bot = commands.Bot(command_prefix='.',help_command=None)
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn'}
@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))
@bot.event
async def on_message(msg):
    if msg.author.bot or msg.content == "" or (msg.author.id == 477480560651141131 and msg.content.startswith(".settimer")):
        await bot.process_commands(msg)
        return
    else:
        res = [ele.lower() if not idx % 2 else ele.upper() for idx, ele in enumerate(msg.content)]
        res = "".join(res)
        await msg.channel.send(res)
        newd = msg.channel.slowmode_delay * 2
        if newd > 21600:
            newd = 21600
        await msg.channel.edit(slowmode_delay=newd)
        print(msg.channel.slowmode_delay)
        await bot.process_commands(msg)
def mod_ch():
    def predicate(ctx):
        return ctx.author.id == 477480560651141131
    return commands.check(predicate)
def bot_ch(ctx):
    def predicate(ctx):
        return ctx.author.bot == False
    return commands.check(predicate)
@bot.command(hidden=True)
@mod_ch()
async def settimer(ctx, ch: discord.TextChannel, arg: int):
    await ch.edit(slowmode_delay=arg)
@bot.command()
async def clean(ctx, arg):
    await ctx.channel.purge(limit=int(arg))
    await ctx.send("**{0}** žinučiu ištrinta :white_check_mark:".format(str(arg)),delete_after=5)
@bot.command()
async def recomend(ctx):
    await ctx.send(API.get_video())
@bot.command()
async def bars(ctx):
    await ctx.send(API.get_lyrics(),tts=True)
@bot.command()
async def join(ctx):
    await ctx.author.voice.channel.connect()
@bot.command()
async def play(ctx, *sh: str):
    vc = ctx.voice_client
    if vc == None:
        time.sleep(2)
        await ctx.send(API.response("prijunk"))
        return
    vc.stop()
    if not re.search(r'^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$', sh[0]):
        search = ' '.join(sh)
        search = search.replace(" ", "+")
        html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search)
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        sh = ["https://www.youtube.com/watch?v="+video_ids[0]]
    song = pafy.new(sh[0])
    await ctx.send(sh[0], delete_after=song.length+1)
    audio = song.getbestaudio()

    src = discord.FFmpegPCMAudio(audio.url, **FFMPEG_OPTIONS)

    vc.play(source=src, after=None)
@bot.command()
async def stop(ctx):
    ctx.voice_client.stop()
@bot.command()
async def isjunk(ctx):
    time.sleep(1)
    await ctx.send(API.response("isjunk"))
    await ctx.voice_client.disconnect()
    await bot.close()
@bot.command()
async def disc(ctx):
    await ctx.voice_client.disconnect()
@bot.command(hidden=True)
@mod_ch()
async def say(ctx, ch: discord.TextChannel, arg):
    if ctx.message.attachments != []:
        obj = ctx.message.attachments[0].filename
        await ctx.message.attachments[0].save(obj)
        await ch.send(file=discord.File(obj))
    else:
        await ch.send(arg)

@bot.command(hidden=True)
@mod_ch()
async def load(ctx, ext):
    bot.load_extension(f'cogs.{ext}')

@bot.command(hidden=True)
@mod_ch()
async def unload(ctx, ext):
    bot.unload_extension(f'cogs.{ext}')

@bot.command(hidden=True)
@mod_ch()
async def reload(ctx, ext):
    bot.unload_extension(f'cogs.{ext}')
    bot.load_extension(f'cogs.{ext}')

for filename in os.listdir('cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(open('token').readline())
# permision id: 2080898167
# bot invite link: https://discord.com/oauth2/authorize?client_id=764198572975194134&permissions=2080898167&scope=bot