import requests
from bs4 import BeautifulSoup

def getTrello(username):
    try:
        url = "https://trello.com/members/"+username
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        name = soup.find('h1', class_='full-name').text
        email = soup.find('a', class_='email').text
        return name + email
    except:
        return 'Trello: User details not found'
    
