import requests
import telebot
import secrets
import json 
from bs4 import BeautifulSoup as sp

bot = telebot.TeleBot(secrets.TELEGRAM_TOKEN)




@bot.message_handler(commands=['salud'])
def send_salud(message):
    salud_args = message.text
    salud_args = salud_args.split()
    salud_args = salud_args[1]
    send_salud.salud_arg = salud_args
    bot.send_message(message.chat.id, findSalud())

    
def findSalud():
    url = "https://apigw.ucchristus.cl/agendaambulatoria-prod/Pacientes?tipoIdPaciente=RUN&paisIdentificador=CL&idPaciente={args}".format(args = send_salud.salud_arg)
    r = requests.get(url)
    if r.status_code == 200:
        datosJson = json.loads(r.text)
        data = json.loads(r.text)
        if data['statusCod'] == 'OK':
            return 'Nombre completo: ' + str(datosJson['listaPacientes'][0]['nombreCompleto']) + '\n' + 'Telefono: ' + str(datosJson['listaPacientes'][0]['numeroTelefonoPrincipal']) + '\n' + 'Direccion: ' + str(datosJson['listaPacientes'][0]['direccion']) + '\n' + 'Email: ' + str(datosJson['listaPacientes'][0]['email'])
        else:
            return 'No se encontro ningun paciente con ese rut'
    else:
        return 'Error en request'

@bot.message_handler(commands=['rut'])
def send_rut(message):
    rut_args = message.text
    rut_args = rut_args.split()
    rut_args = rut_args[1]
    send_rut.rut_arg = rut_args
    bot.send_message(message.chat.id, findRut())

def findRut():
    url = "https://rutificador.org/backend.php"
    rut = "{args}".format(args = send_rut.rut_arg)
    data= ({'action':'search_by_rut','rut':'{args}'.format(args = send_rut.rut_arg)})
    r = requests.post(url, data=data)
    soup = sp(r.text, 'html.parser')
    if r.status_code == 200:
        nombre_completo = soup.find_all('td')[1].text
        nombre_completo = nombre_completo.split()
        nombre1 = nombre_completo[2]
        nombre2 = nombre_completo[3]
        apellido1 = nombre_completo[0]
        apellido2 = nombre_completo[1]
        rut  = soup.find_all('td')[0].text
        sexo = soup.find_all('td')[2].text
        direccion = soup.find_all('td')[3].text
        comuna = soup.find_all('td')[4].text
        return 'Nombre completo: ' + nombre1 + ' ' + nombre2 + ' ' + apellido1 + ' ' + apellido2 + '\n' + 'Rut: ' + rut + '\n' + 'Sexo: ' + sexo + '\n' + 'Direccion: ' + direccion + '\n' + 'Comuna: ' + comuna
    else: 
        return 'Error en request'


@bot.message_handler(command=['patente','pat'])
def send_patente(message):
    patente_args = message.text
    print(patente_args)
    patente_args = patente_args.split()
    print(patente_args)
    patente_args = patente_args[1]
    print(patente_args)
    send_patente.patente_arg = patente_args
    print(send_patente.patente_arg)
    bot.send_message(message.chat.id, findPatente())

def findPatente():
    url = "https://www.patentechile.com/resultados"

    data= {'frmTerm':'{args}'.format(args = send_patente.patente_arg),'frmOpcion':'vehiculo'}
    r = requests.post(url, data=data)
    soup = sp(r.text, 'html.parser')
    
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
    return 'RUT propietario: ' + rut_propietario + '\n' + 'Nombre del propietario: ' + nombre_propietario + '\n' + 'Numero Patente: ' + patente + '\n' + 'Tipo vehiculo '+ tipo_vehiculo + '\n' + 'Marca vehiculo: ' + marca_vehiculo + '\n'+ 'Modelo vehiculo: ' + modelo_vehiculo + '\n' + 'Color vehiculo' + color_vehiculo + '\n' + 'Año vehiculo: ' + ano_vehiculo + '\n' +'Numero de motor: '+ n_motor + '\n' +'Numero de chasis: '+  n_chasis + '\n' +'Multas: ' + poseemultas
        



#add polling
bot.infinity_polling()
