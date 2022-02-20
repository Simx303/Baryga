import discord
import typing
import json
import time
import bisect, random
from discord.ext import commands


class Doges(commands.Cog):
    def __init__(self,bot):
        self.doges = []
        self.bot = bot
        self.limiteddoges = 0
        self.gifs = []
        self.dogesMixed = []
        self.endStamp = 0
        self.limited = False

        with open(".//stats.json") as fie:
            self.stats = json.load(fie)
    def get_doges(self):
        return len(self.doges)+self.limiteddoges-1

    def get_ch(self, a):
        t = 0
        for i in self.doges:
            t+=i[1]
        return dict(self.doges)[a] / t * 100
    def redoge(self):
        self.doges = []
        for l in open('.//nums.txt'):
            if l.startswith('#') or l[0].strip() == '':
                continue
            elif l.startswith('$ldoges'):
                self.limiteddoges = int(l[8:].replace('\n',''))
                continue
            elif l.startswith('$gifs'):
                self.gifs = l[6:].replace('\n','').split(',')
                continue
            else:
                s = l.split(',')
                s[1]=int(s[1])
                self.doges.append(tuple(s))
        self.dogesMixed = WeightedChoice(self.doges)
        print(self.gifs)
    def rnd_doge(self):
        if self.limited and time.time() > self.endStamp:
            self.doges.pop()
            self.limiteddoges +=1
            self.limited = False
        return self.dogesMixed.next()

    def mod_ch(ctx):
        return ctx.channel.id == 816610119428734976
    def bot_ch(ctx):
        return ctx.author.bot == False
    @commands.command(hidden=True)
    @commands.check(mod_ch)
    async def rdoges(self, ctx):
        self.redoge()
    @commands.command(hidden=True)
    @commands.check(mod_ch)
    async def chancedoge(self, ctx, arg):
        await ctx.send("Šansų gauti {} yra {}%".format(arg.capitalize(),str(self.get_ch(arg))))
    @commands.command()
    async def doges(self, ctx, mem: typing.Optional[discord.Member] = 'NaN'):
        aid = 0
        if mem == 'NaN':
            aid = str(ctx.author.id)
        else:
            aid = str(mem.id)
        if aid in self.stats:
            if len(self.stats[aid]['doges']) > 10:
                await ctx.send("<@"+aid+"> doges **{}/{}**:\n\n".format(str(len(self.stats[aid]['doges'])),str(self.get_doges())) + ', '.join([x.capitalize() for x in self.stats[aid]['doges']]), allowed_mentions=discord.AllowedMentions.none())
            else:
                await ctx.send("<@"+aid+"> doges:\n\n~"+"\n~".join([x.capitalize() for x in self.stats[aid]['doges']]), allowed_mentions=discord.AllowedMentions.none())
        else:
            await ctx.send("Dar nesi rades neivieno rare doge.",delete_after=5)

    @commands.command(hidden=True)
    @commands.check(mod_ch)
    async def limitdoge(self,ctx):
        self.limited = True
        self.endStamp = round(time.time())+7200
        await ctx.guild.get_channel(816605947141160981).send("**RIBOTAS DOGE**\nPasibaigs {}".format(time.strftime("%X", time.localtime(self.endStamp))))
    @commands.command()
    @commands.check(bot_ch)
    async def doge(self, ctx, *, arg: str = None):
        auth = str(ctx.author.id)
        if arg:
            if arg in self.stats[auth]['doges']:
                if arg in self.gifs:
                    await ctx.send(file=discord.File(open(f"doges/doge-{arg}.gif",'rb')))
                else:
                    await ctx.send(file=discord.File(open(f"doges/doge-{arg}.png",'rb')))
            else:
                await ctx.send("Dar neatrakinai šito doge\nArba šito doge tiesiog nėra",delete_after=5)
        else:
            doge = self.rnd_doge()
            if doge != 'default':
                if auth not in self.stats:
                    self.stats[auth]= {'doges':[]}
                elif doge not in self.stats[auth]['doges']:
                    self.stats[auth]['doges'].append(doge)
                    await ctx.send(f"Naujas doge atrakintas **{doge.upper()} DOGE**\nGali jį bet kada pakviesti su `.doge {doge}`.\nSek savo doge kolekcija su `.doges`.")
                if doge in self.gifs:
                    await ctx.send(file=discord.File(open(f"doges/doge-{doge}.gif",'rb')))
                else:
                    await ctx.send(file=discord.File(open(f"doges/doge-{doge}.png",'rb')))
        with open('.//stats.json', 'w') as outfile:
            json.dump(self.stats, outfile)

class WeightedChoice(object):
    def __init__(self, weights):
        self.totals = []
        self.weights = weights
        running_total = 0

        for w in weights:
            running_total += w[1]
            self.totals.append(running_total)

    def next(self):
        rnd = random.random() * self.totals[-1]
        i = bisect.bisect_right(self.totals, rnd)
        return self.weights[i][0]
    def wigh(self, i):
        self.weights[i-1][1] += 1
    def tolist(self):
        return [x for x in self.weights]
def setup(bot):
    cog = Doges(bot)
    bot.add_cog(cog)
    cog.redoge()