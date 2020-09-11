import requests
from bs4 import BeautifulSoup

#Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36
#Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36

# Please provide a custom user agent to send information about yourself to be
# considerate to the admins
custom_agent = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
    'From': 'youremail@domain.com'
}

artefact = input("Artefact: ")
amt = int(input("Amount: "))

# Web scrape the RS Wiki to find the material data
url_start = "https://runescape.wiki/w/"
full_url = url_start + artefact

url = requests.get(full_url, headers=custom_agent).text

soup = BeautifulSoup(url, 'lxml')

My_table = soup.find_all('table', class_='wikitable')[1]

t = []

for item in My_table.find_all('tbody'):
    for a in item.find_all('tr')[9:]:
        for b in a.find_all('td'):
            temp = b.get_text()
            t.append(temp)

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
while index2 < len(total_price):
    total_price[index2] = total_price[index2].replace(',', '')
    index2 += 1

# Create class to store material data
class Materials:
    def __init__(self, mat_name, mat_amount, mat_price, total_mat_price):
        self.mat_name = mat_name
        self.mat_amount = int(mat_amount)
        self.mat_price = int(mat_price)
        self.total_mat_price = int(total_mat_price)

# Store each Material class object into a list
list2 = []

for i in range(len(mat_name)):
    mat1 = list2.append(Materials(mat_name[i], mat_amount[i], mat_price[i], total_mat_price[i]))

# Calculate the total price of all materials
def mult(amount):
    s = 0
    for item in list2:
        s += item.total_mat_price
    s *= amount
    return s

sum = mult(amt)

# Print out summary
print(f"Total cost of {amt} {artefact}(s) is: {sum} gp")