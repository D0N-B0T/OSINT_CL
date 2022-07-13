
from xml.dom import NO_MODIFICATION_ALLOWED_ERR
import requests
from bs4 import BeautifulSoup as sp

url = "https://www.patentechile.com/resultados"
#frmTerm=19266781-k&frmOpcion=rut
data= {'frmTerm': '8915821-4', 'frmOpcion': 'rut'}
r = requests.post(url, data=data)
soup = sp(r.text, 'html.parser')

patente_vehiculo = soup.find_all('td')[8].text
tipo_vehiculo = soup.find_all('td')[9].text
marca_vehiculo = soup.find_all('td')[10].text
modelo_vehiculo = soup.find_all('td')[11].text
n_motor = soup.find_all('td')[12].text
año_vehiculo = soup.find_all('td')[13].text

print('Patente: ' + patente_vehiculo+'\n'+ 'Tipo: ' + tipo_vehiculo+'\n'+ 'Marca: ' + marca_vehiculo+'\n'+ 'Modelo: ' + modelo_vehiculo+'\n'+ 'N° Motor: ' + n_motor+'\n'+ 'Año: ' + año_vehiculo)




