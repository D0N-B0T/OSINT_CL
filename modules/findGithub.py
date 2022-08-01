import requests


def getGit(username):
    try:    
        url = "https://api.github.com/users/"+username+"/events/public"
        r = requests.get(url)
        print('Display Login: '+r.json()[0]['actor']['display_login'])
        print('Email: ' + r.json()[0]['payload']['commits'][0]['author']['email'])
        email = r.json()[0]['payload']['commits'][0]['author']['email']
        return email
    except:
        print('Github: User details not found')
    