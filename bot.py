import requests
import telebot
import secrets
import json 
from bs4 import BeautifulSoup as sp
import codecs 
import base64
import os



bot = telebot.TeleBot(secrets.TELEGRAM_TOKEN)

@bot.message_handler(commands=['patente','pat'])
def send_patente(message):
    patente_args = message.text
    patente_args = patente_args.split()
    patente_args = patente_args[1]
    send_patente.patente_arg = patente_args
    bot.send_message(message.chat.id, patente())

def patente():
    try:
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
        return 'RUT propietario: ' + rut_propietario + '\n' + 'Nombre del propietario: ' + nombre_propietario + '\n' + 'Numero Patente: ' + patente + '\n' + 'Tipo vehiculo '+ tipo_vehiculo + '\n' + 'Marca vehiculo: ' + marca_vehiculo + '\n'+ 'Modelo vehiculo: ' + modelo_vehiculo + '\n' + 'Color vehiculo' + color_vehiculo + '\n' + 'Año vehiculo: ' + ano_vehiculo + '\n' +'Numero de motor: '+ n_motor + '\n' +'Numero de chasis' + n_chasis + '\n' + 'Posee multas: ' + poseemultas + '\n' 
    except:
        return 'No se encontro ninguna patente con ese numero'

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
        nombre = soup.find_all('td')[1].text
        direccion = soup.find_all('td')[3].text
        comuna = soup.find_all('td')[4].text
        return "Nombre: " + nombre + "\n" + "Direccion: " + direccion + "\n" + "Comuna: " + comuna
    else: 
        return 'Error en request'




@bot.message_handler(commands=['sii'])
def send_sii(message):
    sii_args = message.text
    sii_args = sii_args.split()
    sii_args = sii_args[1]
    send_sii.sii_arg = sii_args
    bot.send_message(message.chat.id, findSii())



def findSii():

    #Datos de ejemplo
    rut = "{args}".format(args = send_sii.sii_arg)
    #split rut into rut and dv
    rut_split = rut.split('-')
    rut = rut_split[0]
    dv = rut_split[1]
    

    #Request al SII-captcha
    captcha_req = requests.post("https://zeus.sii.cl/cvc_cgi/stc/CViewCaptcha.cgi",data={'oper':'0'})
    respuesta = captcha_req.json()
    #Se obtiene el string que contiene la información del captcha
    txtCaptcha= respuesta['txtCaptcha']

    #Decodificación del texto anterior
    code = base64.b64decode(txtCaptcha)[36:40]

    #Petición al SII, con captcha resuelto
    consulta_sii = requests.post("https://zeus.sii.cl/cvc_cgi/stc/getstc",data={'RUT':rut,'DV':dv.upper(),'PRG':'STC','OPC':'NOR','txt_code':code,'txt_captcha':txtCaptcha}, verify=True)

    #Parseo de los datos
    datos = sp(consulta_sii.text,"html.parser")

    #Obtención de la razón social
    razon_social= consulta_sii.text.split("n Social&nbsp;:")
    razon_social = razon_social[1].split("</div>")
    razon_social = razon_social[1][74:].strip()

    #Inicio de actividades
    inicio_actividades = datos.find_all("span")
    inicio_actividades = consulta_sii.text.split("Fecha de Inicio de Actividades: ")
    if len(inicio_actividades)>1:    
        inicio_actividades = inicio_actividades[1][0:10]
    else:
        inicio_actividades = None

    return razon_social, inicio_actividades



def edad():
    rut = "{args}".format(args = send_rut.rut_arg)
    urlroted = 'uggcf://znfgrepuvyrncx.vasb/jf-oveguqnli3/ncv/?ehg='
    url = codecs.decode(urlroted, 'rot_13')  + rut
    response = requests.get(url)
    response = response .json()
    for item in response:
            return "Nombre                   : " + item['nombre'] + "\n" + "Edad                     : " + item['edad'] + "\n" + "Fecha de nacimiento      : " + item['fecha_nacimiento']

def multasDirTrabajo():
    #https://ventanilla.dirtrab.cl/RegistroEmpleador/consultamultas.aspx
    return


######################################### get all ###############################################

@bot.message_handler(commands=['r'])
def start(message):
    bot.send_message(message.chat.id, 'Obteniendo datos de la persona...')
    rut_args = message.text
    rut_args = rut_args.split()
    rut_args = rut_args[1]

    #rutificador
    bot.send_message(message.chat.id, '====================================')
    try:   
        url = "https://rutificador.org/backend.php"
        rut = "{args}".format(args = rut_args)
        data= ({'action':'search_by_rut','rut':'{args}'.format(args = rut_args)})
        r = requests.post(url, data=data)
        soup = sp(r.text, 'html.parser')
          
        if r.status_code == 200:
            nombre = soup.find_all('td')[1].text
            direccion = soup.find_all('td')[3].text
            comuna = soup.find_all('td')[4].text
            return "Nombre: " + str(nombre) + "\n" + "Direccion: " + str(direccion) + "\n" + "Comuna: " + str(comuna)
        else: 
            bot.send_message(message.chat.id, 'No se encontro ese rut')
    except:
        bot.send_message(message.chat.id, 'No se encontro ese rut')

    #edad
    bot.send_message(message.chat.id, '====================================')
    try: 
        rut = "{args}".format(args = rut_args)
        urlroted = 'uggcf://znfgrepuvyrncx.vasb/jf-oveguqnli3/ncv/?ehg='
        url = codecs.decode(urlroted, 'rot_13')  + rut
        response = requests.get(url)
        response = response .json()
        for item in response:
                bot.send_message(message.chat.id, "Edad: " + str(item['edad']) + "\n" + "Fecha de nacimiento: " + str(item['fecha_nacimiento']))
    except:
        bot.send_message(message.chat.id, 'Error en request')


    # SALUD    
    try:
        bot.send_message(message.chat.id, '====================================')
        url = "https://apigw.ucchristus.cl/agendaambulatoria-prod/Pacientes?tipoIdPaciente=RUN&paisIdentificador=CL&idPaciente={args}".format(args = rut_args)
        r = requests.get(url)  
        if r.status_code == 200:
            datosJson = json.loads(r.text)
            data = json.loads(r.text)
            if data['statusCod'] == 'OK':
                bot.send_message(message.chat.id, 'Nombre completo: ' + str(datosJson['listaPacientes'][0]['nombreCompleto']) + '\n' + 'Telefono: ' + str(datosJson['listaPacientes'][0]['numeroTelefonoPrincipal']) + '\n' + 'Direccion: ' + str(datosJson['listaPacientes'][0]['direccion']) + '\n' + 'Email: ' + str(datosJson['listaPacientes'][0]['email']))
            else:
                bot.send_message(message.chat.id, 'No se encontro ningun paciente con ese rut')
        else:
            bot.send_message(message.chat.id, 'Error en request')
    except:
        bot.send_message(message.chat.id, 'Error en request')
    
    # PATENTE
    bot.send_message(message.chat.id, '====================================')
    try: 
        url = "https://www.patentechile.com/resultados"
        data= {'frmTerm': '{args}'.format(args = rut_args), 'frmOpcion': 'rut'}
        r = requests.post(url, data=data)
        soup = sp(r.text, 'html.parser')
        if r.status_code == 200:
            tipo_vehiculo = soup.find_all('td')[9].text
            marca_vehiculo = soup.find_all('td')[10].text
            modelo_vehiculo = soup.find_all('td')[11].text
            n_motor = soup.find_all('td')[12].text
            año_vehiculo = soup.find_all('td')[13].text
            bot.send_message(message.chat.id, 'Patente: ' + str(tipo_vehiculo) + ' ' + str(marca_vehiculo) + ' ' + str(modelo_vehiculo) + ' ' + str(n_motor) + ' ' + str(año_vehiculo))
        else:
            bot.send_message(message.chat.id, 'La persona no tiene vehiculo.')
    except:
        bot.send_message(message.chat.id, 'Error em requests.')



@bot.message_handler(commands=['usr'])
def getUser(message):
    import modules.findGithub as fg
    import modules.findTrello as ft
    bot.send_message(message.chat.id, 'Obteniendo datos...')
    username = message.text
    username = username.split()
    username = username[1]    
    b1 = fg.getGit(username)
    b2 = ft.getTrello(username)
    bot.send_message(message.chat.id, b1)
    bot.send_message(message.chat.id, b2)

#add polling


@bot.message_handler(commands=['email'])
def getEmail(message):
    email = message.text
    email = email.split()
    email = email[1]

    mail = os.system('holehe {email} --only-used > text.txt'.format(email = email))

    import re
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    with open('text.txt', 'r') as f:
        text = f.read()
        text = ansi_escape.sub('', text)
        for line in f:
            if line.startswith('[32m[+]'):
                    bot.send_message(message.chat.id, line)

    
        
            
   



bot.infinity_polling()
