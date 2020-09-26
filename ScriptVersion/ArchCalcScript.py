import requests
from bs4 import BeautifulSoup
from tabulate import tabulate
from material import Materials
from experience import ArtifactExp

#Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36
#Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36

# Please provide a custom user agent to send information about yourself to be
# considerate to the RS Wiki admins
custom_agent = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
    'From': 'youremail@domain.com'
}

artifact = input("Artifact: ")

url_start = "https://runescape.wiki/w/"
full_url = url_start + artifact
status_check = requests.get(full_url, headers=custom_agent)

# Check if artifact input is valid
if status_check.status_code == 200:
    url = requests.get(full_url, headers=custom_agent).text
else:
    raise Exception('Invalid artifact. Please try again.')
    
# Check for invalid number
while True:
    try:
        amt = int(input("Amount: "))
        break
    except ValueError:
        print("Invalid number.  Please try again.")

# Web scrape the RS Wiki to find the material data
soup = BeautifulSoup(url, 'lxml')

My_table = soup.find_all('table', class_='wikitable')[1]

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
    
sum = totalCost(amt)
calcMats(amt)
capitalize = artifact.title()

# Formatting for summary. Too many lists and for loops
headers = ['Material', 'Amount', 'Price (gp)', 'Total Price (gp)']
name = []
amount = []
price = []
total_price = []

for item in list2:
    name.append(item.MatName)

for item in list2:
    amount.append("{:,}".format(item.MatAmount))

for item in list2:
    price.append("{:,}".format(item.MatPrice))

for item in list2:
    total_price.append("{:,}".format(item.TotalMatPrice))
    
table = zip(name, amount, price, total_price)
print(f'\n{tabulate(table, headers=headers)}')

xpheader = ['Total Cost (gp)', 'XP with outfit', 'XP without outfit', 'XP each']
table1 = zip(["{:,}".format(sum)], 
             ["{:,}".format(ExpWithOutfit(amt))], 
             ["{:,}".format(totalExperience(amt))])
print(f'\n{tabulate(table1, headers=xpheader)}')