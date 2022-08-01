import requests


def getGit(username):
    try:    
        url = "https://api.github.com/users/"
        r = requests.get(url+username+"/events/public")
        displaylogin  = r.json()[0]['actor']['display_login']
        email = r.json()[0]['payload']['commits'][0]['author']['email']
        return displaylogin, email
    except:
        return 'Github: error de conexion'

        
def getGit2(username):
    try:
        url = "https://api.github.com/users/"
        r2 = requests.get(url + username)
        id = r2.get('id')
        avatar = r2.get('avatar_url')
        return 'ID: '+'\n' + id +'Github nombre: '+ displaylogin +'\n'+ 'Github mail: '+ email  +'\n'+ 'Github avatar: '+ avatar
    except:
        return 'Github: error de conexion'
    