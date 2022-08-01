import requests


def getGit(username):
    try:    
        url = "https://api.github.com/users/"+username+"/events/public"
        r = requests.get(url)
        displaylogin  = r.json()[0]['actor']['display_login']
        email = r.json()[0]['payload']['commits'][0]['author']['email']
        return displaylogin, email
        # url2 = "https://api.github.com/users/"
        # r2 = requests.get(url2+username)
        # id = r2.get('id')
        # avatar = r2.get('avatar_url')
        


        # return 'ID: '+'\n' + id +'Github nombre: '+ displaylogin +'\n'+ 'Github mail: '+ email  +'\n'+ 'Github avatar: '+ avatar
    except:
        return 'Github: error de conexion'
    