import discord
import random
from discord.ext import commands
import logging
import requests
import re
import os

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='a+')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

#client = discord.Client()
bot = commands.Bot(command_prefix='.')
link_blacklist = ["https://e621.net"]

def get_ur_mom_line():
    s = open('ur_mom_jokes.txt', 'r')
    m = s.readlines()
    l = []
    for i in range(0, len(m) - 1):
        x = m[i]
        z = len(x)
        a = x[:z - 1]
        l.append(a)
    l.append(m[i + 1])
    o = random.choice(l)
    s.close()
    return o

async def find_links(message):
    regex = r"https?:\/\/(.+?\.)?e621\.net(\/[A-Za-z0-9\-\._~:\/\?#\[\]@!$&'\(\)\*\+,;\=]*)?"
    url = re.findall(regex, message.content)
    #print(x[0] for x in url)
    for i in range(len(url)):
        logger.info("message by {} in channel {} found to have a restricted domain {}".format(message.author, message.channel, url[i]))
        await message.delete()
        await message.channel.send("Hey, that site is not gamer approved, use e926 instead!")


def get_inspirational_quote():
    r = requests.get('https://inspirobot.me/api?generate=true')
    response = r.text
    return response

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.event
async def on_message(message):
    try:
        roles = message.author.roles
        for i in range(len(roles)):
            if str.lower(str((roles[i]))) == str.lower('Final Warning'):
                if not message.attachments:
                    pass
                else:
                    await message.delete()
                    logger.info("Message by {} in channel {} deleted due to final warning role".format(message.author, message.channel))
    except AttributeError:
        pass

    await find_links(message)

    await bot.process_commands(message)


#Hug and Headpat from Kazyu

#@bot.command(pass_context=True)
#async def test(ctx, arg):
    #print(arg)
#    await ctx.send(arg)

@bot.command(pass_context = True, name='mom')
@commands.cooldown(1,15)
async def mom(ctx):
    line = get_ur_mom_line()
    await ctx.send(line)
    pass

@bot.command(pass_context=True)
@commands.cooldown(1, 10)
async def okay(ctx):
    await ctx.send("<:okay:728254351365374072>")

@bot.command(pass_context=True, name='inspire')
@commands.cooldown(1,60)
async def inspire(ctx):
    inspiration = get_inspirational_quote()
    await ctx.send(inspiration)

bot.run(os.environ['BOTKEY'])

