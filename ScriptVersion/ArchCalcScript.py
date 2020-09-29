import requests
from bs4 import BeautifulSoup
from tabulate import tabulate
from material import Materials
from experience import ArtifactExp

def main():
    artifact = input("Artifact: ")

    url_start = "https://runescape.wiki/w/"
    full_url = url_start + artifact

    url = check_url(full_url)
    amt = check_amount()

    # Web scrape the RS Wiki
    soup = BeautifulSoup(url, 'lxml')
    wiki_mat_table = soup.find_all('table', class_='wikitable')[1]

    material_list = webscrape_materials(wiki_mat_table)
    experience_info = webscrape_experience(wiki_mat_table)
    
    remove_comma(material_list)
    temp_exp = remove_comma(experience_info)
    experience = float(temp_exp[0])
    
    mat_list = store(material_list)
    
    calc_mats(amt, mat_list)
    artifact_exp = ArtifactExp(experience)
    
    summary(mat_list, amt, artifact_exp)

# Check if artifact input is valid
def check_url(full_url):
    # Please provide a custom user agent to send information about yourself to
    # be considerate to the RS Wiki admins
    custom_agent = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
        'From': 'your_email@domain.com'
    }   
    
    status_check = requests.get(full_url, headers=custom_agent)

    if status_check.status_code == 200:
        url = requests.get(full_url, headers=custom_agent).text
        return url
    else:
        raise Exception('Invalid artifact. Please try again.')

# Check for invalid number    
def check_amount():
    while True:
        try:
            amt = int(input("Amount: "))
            return amt
            break
        except ValueError:
            print("Invalid number.  Please try again.")

# Webscrape the RS wiki for artifact materials
def webscrape_materials(table):
    temp_list = []

    for item in table.find_all('tbody'):
        for a in item.find_all('tr')[9:]:
            for b in a.find_all('td'):
                temp = b.get_text()
                temp_list.append(temp)
    
    return temp_list

# Webscrape the RS wiki for artifact experience
def webscrape_experience(table):
    experience_data = table.tbody.find_all('tr')[1]
    experience_text = experience_data.find('td').get_text()
    experience = experience_text.split()
    del(experience[1])
    return experience

# Remove commas for future calculations
def remove_comma(list):
    index = 0
    while index < len(list):
        list[index] = list[index].replace(',', '')
        index += 1
        
    return list

# Store each Material class object into a list
def store(list):
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
def total_cost(list):
    sum_price = 0
    for item in list:
        sum_price += item.total_mat_price
    return sum_price

# Multiply the material amount and total material amount 
# by the amount of artifacts
def calc_mats(amount, list):
    for i in range(len(list)):
        list[i].mat_amount *= amount
        list[i].total_mat_price *= amount 

# Total experience without full archaeology outfit
def exp_without_outfit(amount, experience):
    exp = experience.experience * amount
    return exp

# Total experience with full archaeology outfit
def exp_with_outfit(amount, experience):
    # Full archaeology outfit gives +6% bonus experience
    outfit = 0.06
    exp = amount * (experience.experience + (experience.experience * outfit))
    return exp

# Formatting for summary. Too many lists and for-loops
def summary(mat_list, amt, experience):
    headers = ['Material', 'Amount', 'Price', 'Total Price']
    name = []
    amount = []
    price = []
    total_price = []

    for item in mat_list:
        name.append(item.mat_name)

    for item in mat_list:
        amount.append("{:,}".format(item.mat_amount))

    for item in mat_list:
        price.append("{:,} gp".format(item.mat_price))

    for item in mat_list:
        total_price.append("{:,} gp".format(item.total_mat_price))
        
    table = zip(name, amount, price, total_price)
    print(f'\n{tabulate(table, headers=headers)}')

    xpheader = ['Total Cost', 
                'XP with outfit', 
                'XP without outfit',
                'XP each']
    table1 = zip(["{:,} gp".format(total_cost(mat_list))], 
                 ["{:,} xp".format(exp_with_outfit(amt, experience))], 
                 ["{:,} xp".format(exp_without_outfit(amt, experience))],
                 ["{:,} xp".format(experience.experience)])
    print(f'\n{tabulate(table1, headers=xpheader)}')  

if __name__ == "__main__":
    main()