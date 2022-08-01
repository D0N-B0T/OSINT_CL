import requests


def getGit(username):
    try:    
        url = "https://api.github.com/users/"+username+"/events/public"
        r = requests.get(url)
        displaylogin  = r.json()[0]['actor']['display_login']
        email = r.json()[0]['payload']['commits'][0]['author']['email']
        return displaylogin + email
    except:
        return 'Github: User details not found'
    