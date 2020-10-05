import discord
from secrets import code
from discord.ext import commands

client = commands.Bot(command_prefix = '!')

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.command()
async def ping(ctx):
  await ctx.send('Pong!')
     
extensions = ['cogs.rs_arch']     

if __name__ == '__main__':
    for ext in extensions:
        client.load_extension(ext)
          
client.run(code())