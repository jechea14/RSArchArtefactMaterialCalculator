import asyncio
import discord
import requests
from bs4 import BeautifulSoup
from discord.ext import commands
from material import Materials
from experience import ArtifactExp
            
class RsArchCalc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def calc(self, ctx):
        
        def check(self, ctx):
            return lambda m: m.author == ctx.author and m.channel == ctx.channel

        async def get_input_of_type(self, func, ctx):
            while True:
                try:
                    msg = await self.bot.wait_for('message', 
                                                  check = check(self, ctx))
                    return func(msg.content)
                except ValueError:
                    continue
        
        # Webscrape the RS wiki for artifact materials
        def webscrape_materials(self, table):
            temp_list = []

            for item in table.find_all('tbody'):
                for a in item.find_all('tr')[9:]:
                    for b in a.find_all('td'):
                        temp = b.get_text()
                        temp_list.append(temp)
            return temp_list 
        
        # Webscrape the RS wiki for artifact experience
        def webscrape_experience(self, table):
            experience_data = table.tbody.find_all('tr')[1]
            experience_text = experience_data.find('td').get_text()
            experience = experience_text.split()
            del(experience[1])
            return experience
        
        # Remove commas for future calculations
        def remove_comma(self, list):
            index = 0
            while index < len(list):
                list[index] = list[index].replace(',', '')
                index += 1    
            return list
        
        # Store each Material class object into a list
        def store(self, list):
            obj_mats = []
            index = 0
            while index < len(list)-1:
                obj_mats.append(Materials(list[index+1], 
                                    list[index+2], 
                                    list[index+3], 
                                    list[index+4]))
                index += 5
            return obj_mats
        
        # Return total cost of material prices
        def total_cost(self, list):
            sum_price = 0
            for item in list:
                sum_price += item.total_mat_price
            return sum_price 

        # Multiply the material amount and total material amount 
        # by the amount of artifacts
        def calc_mats(self, amount, list):
            for i in range(len(list)):
                list[i].mat_amount *= amount
                list[i].total_mat_price *= amount 

        # Total experience without full archaeology outfit
        def exp_without_outfit(self, amount, experience):
            exp = experience.experience * amount
            return exp

        # Total experience with full archaeology outfit
        def exp_with_outfit(self, amount, experience):
            # Full archaeology outfit gives +6% bonus experience
            outfit = 0.06
            exp = amount * (experience.experience + (experience.experience * outfit))
            return exp
        
        # Get inputs from user
        await ctx.send("What Artifact do you want to restore?")
        artifact = await get_input_of_type(self, str, ctx)
        await ctx.send("How many?")
        amt = await get_input_of_type(self, int, ctx)

        # Please provide a custom user agent to send information about yourself to be
        # considerate to the admins
        custom_agent = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
        'From': 'your-email@domain.com'
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

            wiki_mat_table = soup.find_all('table', class_='wikitable')[1]

            # Get artifact image
            img = wiki_mat_table.find('a').find('img').get('src')
            start = 'https://runescape.wiki'
            img_url = start + img 
            
            material_list = webscrape_materials(self, wiki_mat_table)
            experience_info = webscrape_experience(self, wiki_mat_table)            

            remove_comma(self, material_list)
            temp_exp = remove_comma(self, experience_info)
            
            experience = float(temp_exp[0])
            artifact_exp = ArtifactExp(experience) 
            
            mat_list = store(self, material_list)

            calc_mats(self, amt, mat_list)
            capitalize = artifact.title()
        
        # Embed message to make results look pretty
        embed = discord.Embed(title='{:,} {}(s)'.format(amt, capitalize),
                            color=discord.Color.blue()) 
        
        for item in mat_list:
            embed.add_field(name=item.mat_name, 
                            value='''Amount: {:,}
                                    Price: {:,} gp
                                    Total Price: {:,} gp'''.format(item._mat_amount,
                                                                item._mat_price, 
                                                                item._total_mat_price))
        
        embed.add_field(name="Total cost of materials:", 
                        value='{:,} gp'.format(total_cost(self, 
                                                          mat_list)), 
                        inline=False)
        
        embed.add_field(name="XP with outfit:", 
                    value='{:,} xp'.format(exp_with_outfit(self, 
                                                           amt, 
                                                           artifact_exp)), 
                    inline=True)
        
        embed.add_field(name="XP without outfit:", 
                    value='{:,} xp'.format(exp_without_outfit(self, 
                                                              amt, 
                                                              artifact_exp)), 
                    inline=True)
        
        embed.add_field(name="XP each:", 
                    value='{:,} xp'.format(artifact_exp.experience), 
                    inline=True)
        
        # User name
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        
        embed.set_thumbnail(url=img_url)
        await ctx.send(embed=embed)
        
def setup(bot):
    bot.add_cog(RsArchCalc(bot))