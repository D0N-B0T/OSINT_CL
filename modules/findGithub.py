import requests


def getGit(username):
    try:    
        url = "https://api.github.com/users/"+username+"/events/public"
        r = requests.get(url)
        
        #if return code is {} then user does not exist
        displaylogin  = r.json()[0]['actor']['display_login']
        email = r.json()[0]['payload']['commits'][0]['author']['email']

        url2 = "https://api.github.com/users/"+username
        r2 = requests.get(url2)
        id = r2.json()['id']
        avatar = r2.json()['avatar_url']
        #save avatar
        with open('avatar.jpg', 'wb') as f:
            f.write(requests.get(avatar).content)

        return 'ID:'+'\n' + id +'Github nombre: '+ displaylogin +'\n'+ 'Github mail: '+ email
        

    except:
        return 'Github: error de conexion'
    