import requests
from bs4 import BeautifulSoup as sp



rut = "16163631-2"

url = "https://rutificador.org/backend.php"

data= ({'action':'search_by_rut','rut':rut})
r = requests.post(url, data=data)
soup = sp(r.text, 'html.parser')
if r.status_code == 200:
    rut = soup.find_all('td')[0].text
    nombre = soup.find_all('td')[1].text
    direccion = soup.find_all('td')[3].text
    comuna = soup.find_all('td')[4].text
    
    print("Rut: " + rut)
    print("Nombre: " + nombre)
    print("Direccion: " + direccion)
    print("Comuna: " + comuna)
else: 
    print ("Error")