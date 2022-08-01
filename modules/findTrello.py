import requests
from bs4 import BeautifulSoup

def getTrello(username):
    try:
        url = "https://trello.com/members/"+username
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        print('Display Name: '+soup.find('h1', class_='full-name').text)
        print('Email: ' + soup.find('a', class_='email').text)
        email = soup.find('a', class_='email').text
        return email
    except:
        print('Trello: User details not found')
    
