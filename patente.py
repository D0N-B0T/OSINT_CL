
import requests
from bs4 import BeautifulSoup as sp

url = "https://www.patentechile.com/resultados"
arg_patente = 'HKSX39'
data= ({'frmTerm':arg_patente,'frmOpcion':'vehiculo'})
r = requests.post(url, data=data)
soup = sp(r.text, 'html.parser')
if r.status_code == 200:
    rut_propietario = soup.find_all('td')[2].text
    nombre_propietario = soup.find_all('td')[4].text
    patente = soup.find_all('td')[8].text
    tipo_vehiculo = soup.find_all('td')[10].text
    marca_vehiculo = soup.find_all('td')[12].text
    modelo_vehiculo = soup.find_all('td')[14].text
    ano_vehiculo = soup.find_all('td')[16].text
    color_vehiculo = soup.find_all('td')[18].text
    n_motor = soup.find_all('td')[20].text
    n_chasis = soup.find_all('td')[22].text
    poseemultas = soup.find_all('td')[24].text
    print('RUT propietario: ' + rut_propietario + '\n' + 'Nombre del propietario: ' + nombre_propietario + '\n' + 'Numero Patente: ' + patente + '\n' + 'Tipo vehiculo '+ tipo_vehiculo + '\n' + 'Marca vehiculo: ' + marca_vehiculo + '\n'+ 'Modelo vehiculo: ' + modelo_vehiculo + '\n' + 'Color vehiculo' + color_vehiculo + '\n' + 'Año vehiculo: ' + ano_vehiculo + '\n' +'Numero de motor: '+ n_motor + '\n' +'Numero de chasis: '+  n_chasis + '\n' +'Multas: ' + poseemultas)
else:
    print('Error en request')
