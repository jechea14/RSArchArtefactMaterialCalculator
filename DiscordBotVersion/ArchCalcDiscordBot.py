import asyncio
import discord
import requests
from bs4 import BeautifulSoup
from secrets import code
from discord.ext import commands

client = commands.Bot(command_prefix = '!')

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.command()
async def ping(ctx):
  await ctx.send('Pong!')

def check(ctx):
    return lambda m: m.author == ctx.author and m.channel == ctx.channel

async def get_input_of_type(func, ctx):
    while True:
        try:
            msg = await client.wait_for('message', check=check(ctx))
            return func(msg.content)
        except ValueError:
            continue

@client.command()
async def calc(ctx):
    # Get inputs from user
    await ctx.send("Enter the Artifact")
    artifact = await get_input_of_type(str, ctx)
    await ctx.send("How many?")
    amt = await get_input_of_type(int, ctx)
    
    # Please provide a custom user agent to send information about yourself to be
    # considerate to the admins
    custom_agent = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
    'From': 'youremail@domain.com'
    }

    # Show the bot is typing
    async with ctx.typing():
        await asyncio.sleep(2)

        url_start = "https://runescape.wiki/w/"
        full_url = url_start + artifact
        status_check = requests.get(full_url, headers=custom_agent)

        # Check if artifact input is valid
        if status_check.status_code == 200:
            url = requests.get(full_url, headers=custom_agent).text
        else:
            await ctx.send('Invalid artifact. Please try again.')
            raise Exception('Invalid artifact. Please try again.')

        # Web scrape the RS Wiki to find the material data
        soup = BeautifulSoup(url, 'lxml')

        My_table = soup.find_all('table', class_='wikitable')[1]

        # Get artifact image
        img = My_table.find('a').find('img').get('src')

        t = []

        for item in My_table.find_all('tbody'):
            for a in item.find_all('tr')[9:]:
                for b in a.find_all('td'):
                    temp = b.get_text()
                    t.append(temp)

        experience = My_table.tbody.find_all('tr')[1]
        exp = experience.find('td').get_text()
        exp1 = exp.split()
        del(exp1[1])

        b = [x for x in t if x]

        # Split list into individual lists
        mat_name = b[:-1:4]
        mat_amount = b[1:-1:4]
        mat_price = b[2:-1:4]
        total_mat_price = b[3:-1:4]
        total_price = [b[-1]]

        # Remove commas in digit strings for future calculations
        index = 0
        while index < len(mat_price):
            mat_amount[index] = mat_amount[index].replace(',', '')
            mat_price[index] = mat_price[index].replace(',', '')
            total_mat_price[index] = total_mat_price[index].replace(',', '')
            index += 1

        index2 = 0
        while index2 < len(exp1):
            exp1[index2] = exp1[index2].replace(',', '')
            index2 += 1

        e = float(exp1[0])

        # Create class to store material data
        class Materials:
            def __init__(self, mat_name, mat_amount, mat_price, total_mat_price):
                self._mat_name = mat_name
                self._mat_amount = int(mat_amount)
                self._mat_price = int(mat_price)
                self._total_mat_price = int(total_mat_price)
                
            @property
            def MatName(self):
                return self._mat_name
            
            @property
            def MatAmount(self):
                return self._mat_amount
            
            @property
            def MatPrice(self):
                return self._mat_price

            @property
            def TotalMatPrice(self):
                return self._total_mat_price
            
            @MatAmount.setter
            def MatAmount(self, mat_amount):
                self._mat_amount = mat_amount

            @TotalMatPrice.setter
            def TotalMatPrice(self, total_mat_price):
                self._total_mat_price = total_mat_price

        class ArtifactExp:
            def __init__(self, experience):
                self._experience = experience

            @property
            def Experience(self):
                return self._experience

            @Experience.setter
            def Experience(self, experience):
                self._experience = experience

        # Store each Material class object into a list
        list2 = []

        for i in range(len(mat_name)):
            list2.append(Materials(mat_name[i], 
                                mat_amount[i], 
                                mat_price[i], 
                                total_mat_price[i]))

        # Calculate the total price of all materials
        def totalCost(amount):
            s = 0
            for item in list2:
                s += item.TotalMatPrice
            s *= amount
            return s    

        # Multiply the material amount and total material amount 
        # by the amount of artifacts
        def calcMats(amount):
            for i in range(len(mat_name)):
                list2[i].MatAmount *= amount
                list2[i].TotalMatPrice *= amount 

        art = ArtifactExp(e)

        # Total experience without full archaeology outfit
        def totalExperience(amount):
            exp = art.Experience * amount
            return exp

        # Total experience with full archaeology outfit
        def ExpWithOutfit(amount):
            # Full archaeology outfit gives +6% bonus experience
            outfit = 0.06
            exp = amount * (art.Experience + (art.Experience * outfit))
            return exp

        start = 'https://runescape.wiki'
        img_url = start + img
        sum = totalCost(amt)
        calcMats(amt)
        capitalize = artifact.title()
    
    # Embed message to make results look pretty
    embed = discord.Embed(title='{:,} {}(s)'.format(amt, capitalize),
                          color=discord.Color.blue()) 
    
    for item in list2:
        embed.add_field(name=item.MatName, 
                        value='''Amount: {:,}
                                Price: {:,} gp
                                Total Price: {:,} gp'''.format(item.MatAmount,
                                                            item.MatPrice, 
                                                            item.TotalMatPrice))
    
    embed.add_field(name="Total cost of materials:".format(amt, capitalize), 
                    value='{:,} gp'.format(sum), 
                    inline=False)
    
    embed.add_field(name="XP with outfit:", 
                value='{:,} xp'.format(ExpWithOutfit(amt)), 
                inline=True)
    
    embed.add_field(name="XP without outfit:", 
                value='{:,} xp'.format(totalExperience(amt)), 
                inline=True)
    
    embed.add_field(name="XP each:", 
                value='{:,} xp'.format(e), 
                inline=True)
    
    # User name
    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
    
    embed.set_thumbnail(url=img_url)
    await ctx.send(embed=embed)
          
client.run(code())