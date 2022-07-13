import requests
import telebot
import secrets
import json 
from bs4 import BeautifulSoup as sp
import urllib
import codecs 
import base64
import pandas as pd

bot = telebot.TeleBot(secrets.TELEGRAM_TOKEN)



    



@bot.message_handler(commands=['patente','pat'])
def send_patente(message):
    patente_args = message.text
    patente_args = patente_args.split()
    patente_args = patente_args[1]
    send_patente.patente_arg = patente_args
    print(send_patente.patente_arg)
    bot.send_message(message.chat.id, patente())

def patente():
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




@bot.message_handler(commands=['sii'])
def send_sii(message):
    sii_args = message.text
    sii_args = sii_args.split()
    sii_args = sii_args[1]
    send_sii.sii_arg = sii_args
    bot.send_message(message.chat.id, findSii())



def findSii():
    import base64
    import requests
    from bs4 import BeautifulSoup

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
    datos = BeautifulSoup(consulta_sii.text,"html.parser")

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

def multasDirTrabajo():
    #https://ventanilla.dirtrab.cl/RegistroEmpleador/consultamultas.aspx
    return


def edad():
    rut = "{args}".format(args = send_rut.rut_arg)
    urlroted = 'uggcf://znfgrepuvyrncx.vasb/jf-oveguqnli3/ncv/?ehg='
    url = codecs.decode(urlroted, 'rot_13')  + rut
    print('')
    print('Datos de la persona')
    print('')

    response = requests.get(url)
    response = response .json()
    for item in response:
            return "Nombre                   : " + item['nombre'] + "\n" + "Edad                     : " + item['edad'] + "\n" + "Fecha de nacimiento      : " + item['fecha_nacimiento']








######################       trackers        ##############################

def getEnviame1():
    cookies = {
    'pll_language': 'es',
    '_ga': 'GA1.2.367181396.1656052990',
    '_gid': 'GA1.2.417214312.1656052990',
    '_gcl_au': '1.1.651115935.1656052991',
    '_hjFirstSeen': '1',
    '_hjIncludedInSessionSample': '0',
    '_hjSession_2905143': 'eyJpZCI6IjczY2ZhNzdjLWY2MzMtNGQ2Ni1iYmVlLWNlNjI1NTkyZTU2MyIsImNyZWF0ZWQiOjE2NTYwNTI5OTExMzksImluU2FtcGxlIjpmYWxzZX0=',
    '_hjIncludedInPageviewSample': '1',
    '_hjAbsoluteSessionInProgress': '0',
    '_fbp': 'fb.1.1656052991316.1924431910',
    '_hjSessionUser_2905143': 'eyJpZCI6IjJiMTEyOTk5LTFhNDUtNWU1MC1iYTVmLWIwOWE5ZDBlMmU1YiIsImNyZWF0ZWQiOjE2NTYwNTI5OTEwNzQsImV4aXN0aW5nIjp0cnVlfQ==',
    '__hstc': '52082678.57f0869aed01124378c6c48ffe4e7d6b.1656053012627.1656053012627.1656053012627.1',
    'hubspotutk': '57f0869aed01124378c6c48ffe4e7d6b',
    '__hssrc': '1',
    '__hssc': '52082678.1.1656053012627',
    }

    headers = {
        'Host': 'enviame.io',
        'Sec-Ch-Ua': '"Chromium";v="103", ".Not/A)Brand";v="99"',
        'Accept': '*/*',
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'Sec-Ch-Ua-Mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://enviame.io/tracking/',
        # 'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'es-ES,es;q=0.9',
        # Requests sorts cookies= alphabetically
        # 'Cookie': 'pll_language=es; _ga=GA1.2.367181396.1656052990; _gid=GA1.2.417214312.1656052990; _gcl_au=1.1.651115935.1656052991; _hjFirstSeen=1; _hjIncludedInSessionSample=0; _hjSession_2905143=eyJpZCI6IjczY2ZhNzdjLWY2MzMtNGQ2Ni1iYmVlLWNlNjI1NTkyZTU2MyIsImNyZWF0ZWQiOjE2NTYwNTI5OTExMzksImluU2FtcGxlIjpmYWxzZX0=; _hjIncludedInPageviewSample=1; _hjAbsoluteSessionInProgress=0; _fbp=fb.1.1656052991316.1924431910; _hjSessionUser_2905143=eyJpZCI6IjJiMTEyOTk5LTFhNDUtNWU1MC1iYTVmLWIwOWE5ZDBlMmU1YiIsImNyZWF0ZWQiOjE2NTYwNTI5OTEwNzQsImV4aXN0aW5nIjp0cnVlfQ==; __hstc=52082678.57f0869aed01124378c6c48ffe4e7d6b.1656053012627.1656053012627.1656053012627.1; hubspotutk=57f0869aed01124378c6c48ffe4e7d6b; __hssrc=1; __hssc=52082678.1.1656053012627',
    }

    params = {
        'tn': '2581',
    }

    response = requests.get('https://enviame.io/tracker-proxy.php', params=params, cookies=cookies, headers=headers, verify=True)
    return response


@bot.message_handler(commands=['starken'])
def send_starken(message):  
    starken_url = "https://gateway.starken.cl/tracking/orden-flete/of/{}".format(message.text[8:])
    starken_response = requests.get(starken_url)
    starken_json = json.loads(starken_response.text)

    receiver_name = starken_json['receiver_name']
    bot.send_message(message.chat.id, "Nombre: {}".format(receiver_name))
    
    receiver_phone = starken_json['receiver_phone']
    bot.send_message(message.chat.id, "Telefono: {}".format(receiver_phone))

    receiver_email = starken_json['receiver_email']
    bot.send_message(message.chat.id, "Email: {}".format(receiver_email))

    receiver_address = starken_json['receiver_address']
    bot.send_message(message.chat.id, "Direccion: {}".format(receiver_address))


@bot.message_handler(commands=['chilexpress'])
def send_chilexpress(message):
    headers = {
    'Host': 'services.wschilexpress.com',
    'Sec-Ch-Ua': '"-Not.A/Brand";v="8", "Chromium";v="102"',
    'Sec-Ch-Ua-Mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36',
    'Access-Control-Allow-Methods': 'GET',
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
    'Accept': 'application/json, text/plain, */*',
    'Ocp-Apim-Subscription-Key': '7b878d2423f349e3b8bbb9b3607d4215',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Origin': 'https://centrodeayuda.chilexpress.cl',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://centrodeayuda.chilexpress.cl/',
    'Accept-Language': 'es-ES,es;q=0.9',
    'Connection': 'close',
    }

    params = {'nroOt': '{}'.format(message.text[11:])}
    
    chilexpress_response = requests.get('https://services.wschilexpress.com/agendadigital/api/v2/Tracking/GetDatosOT', params=params, headers=headers, verify=True)
    chilexpress_json = json.loads(chilexpress_response.text)
    #print chilexpress_json as json

    
@bot.message_handler(commands=['bluexpress'])
def send_bluexpress(message):
    blue_data = 'action=getTrackingInfo&n_seguimiento=' + message.text[10:]
    cookies = {
        'pll_language': 'es',
        '_gcl_au': '1.1.1475810793.1654754442',
        '_ga_72TNF1225D': 'GS1.1.1654754442.1.0.1654754442.0',
        '_ga': 'GA1.2.943843959.1654754442',
        '_gid': 'GA1.2.545979431.1654754443',
        '_gat_UA-192954256-8': '1',
        'amp_c41cd2': 'eNkxWI8ZB0lYQbYuRjy2-5...1g53gq0g0.1g53gq0g0.0.0.0',
        '_fbp': 'fb.1.1654754443952.2096861925',
        '_clck': 'rz4769|1|f26|0',
        '_clsk': '8p8jha|1654754444979|1|1|www.clarity.ms/eus-f/collect',
    }
    headers = {
        'Host': 'www.blue.cl',
        'Sec-Ch-Ua': '"-Not.A/Brand";v="8", "Chromium";v="102"',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Sec-Ch-Ua-Mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Origin': 'https://www.blue.cl',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://www.blue.cl/seguimiento/',
        'Accept-Language': 'es-ES,es;q=0.9',
    }


    r = requests.post('https://www.blue.cl/wp-admin/admin-ajax.php', cookies=cookies, headers=headers, data=blue_data, verify=True)
    b_text = r.text

@bot.message_handler(commands=['pullmango'])
def send_pullmango(message):
    url = 'https://auto.segurosfalabella.com/api/people' + message.text[10:]
    respuesta = requests.get(url)
    data = respuesta.json()
    data_json = json.dumps(data)
    data_df = pd.read_json(data_json)
    bot.send_message(message.chat.id, data_df)

    destino = data_df.iloc[0]['destino']
    bot.send_message(message.chat.id, "Ciudad: {}".format(destino))

@bot.message_handler(commands=['falabella'])
def send_rut(message):
    cookies = {
    '__cf_bm': 'c66l26oJbGA4rtlrtCxbOaD4EUSI6W0VGvrnDzmFL5I-1655022023-0-ATkXSjk+kZHIA6JUSW9/fCZ+eWZYCrv4gXeBNTe1c6XvB4lFtNG4nJmvHWuRA5mrogvvQ/P9M8a2FUQybDXfu67kWBYzsuLrC/zx2kwwlE4E',
    '_gcl_au': '1.1.690789503.1655022027',
    '_ga': 'GA1.2.1032358755.1655022029',
    '_gid': 'GA1.2.696688995.1655022029',
    '_hjFirstSeen': '1',
    '_hjSession_2564504': 'eyJpZCI6IjQ0YjRjMGMyLWJiNTgtNGIxNi1iNzNiLTRmYzY5NTNlNTVlMCIsImNyZWF0ZWQiOjE2NTUwMjIwMjkyOTMsImluU2FtcGxlIjpmYWxzZX0=',
    '_hjIncludedInSessionSample': '0',
    '_hjIncludedInPageviewSample': '1',
    '_hjAbsoluteSessionInProgress': '0',
    '_fbp': 'fb.1.1655022031404.197221308',
    '_hjSessionUser_2564504': 'eyJpZCI6IjJlM2RlOWFhLWRhMjgtNWVmYi05NDVjLThjZDM5NTg5ZjY2MiIsImNyZWF0ZWQiOjE2NTUwMjIwMjkxOTQsImV4aXN0aW5nIjp0cnVlfQ==',
    }

    headers = {
    'Host': 'auto.segurosfalabella.com',
    # 'Content-Length': '515',
    'X-Instana-T': '1989913f8a68aa8',
    'Sec-Ch-Ua-Mobile': '?0',
    'X-Instana-L': '1,correlationType=web;correlationId=1989913f8a68aa8',
    'Content-Type': 'application/json;charset=UTF-8',
    'Accept': 'application/json, text/plain, */*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36',
    'X-Instana-S': '1989913f8a68aa8',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Sec-Ch-Ua': '"-Not.A/Brand";v="8", "Chromium";v="102"',
    'Origin': 'https://auto.segurosfalabella.com',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    # 'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'es-ES,es;q=0.9',
    # Requests sorts cookies= alphabetically
    # 'Cookie': '__cf_bm=c66l26oJbGA4rtlrtCxbOaD4EUSI6W0VGvrnDzmFL5I-1655022023-0-ATkXSjk+kZHIA6JUSW9/fCZ+eWZYCrv4gXeBNTe1c6XvB4lFtNG4nJmvHWuRA5mrogvvQ/P9M8a2FUQybDXfu67kWBYzsuLrC/zx2kwwlE4E; _gcl_au=1.1.690789503.1655022027; _ga=GA1.2.1032358755.1655022029; _gid=GA1.2.696688995.1655022029; _hjFirstSeen=1; _hjSession_2564504=eyJpZCI6IjQ0YjRjMGMyLWJiNTgtNGIxNi1iNzNiLTRmYzY5NTNlNTVlMCIsImNyZWF0ZWQiOjE2NTUwMjIwMjkyOTMsImluU2FtcGxlIjpmYWxzZX0=; _hjIncludedInSessionSample=0; _hjIncludedInPageviewSample=1; _hjAbsoluteSessionInProgress=0; _fbp=fb.1.1655022031404.197221308; _hjSessionUser_2564504=eyJpZCI6IjJlM2RlOWFhLWRhMjgtNWVmYi05NDVjLThjZDM5NTg5ZjY2MiIsImNyZWF0ZWQiOjE2NTUwMjIwMjkxOTQsImV4aXN0aW5nIjp0cnVlfQ==',
    }

    json_data = {
    'captcha': '03AGdBq25HqBATgXUyFSBMk_u4hwBUkhCT_2G9YylXmSFktE9boMC7GyyOKNNS044nOkIcvJLCK_iGTbzGsVev0hA4EdANnQx3xKF6vs9Ijrb12b7nRYiJpdvPmKl7hd1vxG3ufkx9i0UPAJXL3-G0gV5jh4V-PLwAzayhzrHDWo9f0OcGuk3b1ORxiAp4956SaXIMWaLOrBrYI3Jc3MwxFam9gHlPxIZ143TIonCjSa1LfYY93kcEXCCtCYqNt8W2Sr6jt0CtkEGg5ZVMi_9UJHP1mEkmk_MYFj8syaeznMovFAVGGFJE-TA0gN0aTXzOv8amcxpORXw5uTwqVGywjGWPZSsIumIRPw1qmA0-9-QqnZintcnLdhC2Fw6pcOzgP_0mOwI6G8Z65GJTZbvT-Y0d7bjEA8XDm1Ion8sMZYOZ-tUUOcnXyLNBzEx-mfjGLLK0ox9U2aOMI2mNbpvvLBeU1PNXEEbe9g',
    'rut': '{}'.format(message.text[8:]) 
    }

    response = requests.post('https://auto.segurosfalabella.com/api/people', cookies=cookies, headers=headers, json=json_data, verify=True)
    #print as json
    bot.send_message(message.chat.id, "Buscando...")
    b_text = response.text
    bot.send_message(message.chat.id, "Mira lo que encontre:")
    bot.send_message(message.chat.id, json_data)
    bot.send_message(message.chat.id, b_text)


    rutinput = message.text[8:]
    #recibir rut y colocar puntos y guion 
    rut = rutinput.replace(".", "")
    rut = rut.replace("-", "")
    rut = rut.replace(" ", "")
    rut = rut.upper()
    rut = rut[:-1] + "-" + rut[-1]
    rutfinal = rut 
    #buscar solo nombre
    
    
    nryf = "https://nombrerutyfirma.com/rut?term={}".format(rutfinal)

    response = requests.get(nryf)
    bot.send_message(message.chat.id, "Encontré mas info:")
    bot.send_message(message.chat.id, nryf)
    bot.send_message(message.chat.id, response.text)

@bot.message_handler(commands=['enviame'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Encontré mas info:")
    bot.send_message(message.chat.id, getEnviame1())





######################################### RUT ###############################################

@bot.message_handler(commands=['rut'])
def start(message):
    rut_args = message.text
    rut_args = rut_args.split()
    rut_args = rut_args[1]

    # SALUD
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
    
    # PATENTE
    url = "https://www.patentechile.com/resultados"
    data= {'frmTerm':rut_args,'frmOpcion':'vehiculo'}
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
    bot.send_message(message.chat.id, 'RUT propietario: ' + rut_propietario + '\n' + 'Nombre del propietario: ' + nombre_propietario + '\n' + 'Numero Patente: ' + patente + '\n' + 'Tipo vehiculo '+ tipo_vehiculo + '\n' + 'Marca vehiculo: ' + marca_vehiculo + '\n'+ 'Modelo vehiculo: ' + modelo_vehiculo + '\n' + 'Color vehiculo' + color_vehiculo + '\n' + 'Año vehiculo: ' + ano_vehiculo + '\n' +'Numero de motor: '+ n_motor + '\n' +'Numero de chasis' + n_chasis + '\n' + 'Posee multas: ' + poseemultas + '\n' + 'Link: ' + url) 
    
    #edad
    rut = "{args}".format(args = send_rut.rut_arg)
    urlroted = 'uggcf://znfgrepuvyrncx.vasb/jf-oveguqnli3/ncv/?ehg='
    url = codecs.decode(urlroted, 'rot_13')  + rut_args
    print('')
    print('Datos de la persona')
    print('')

    response = requests.get(url)
    response = response .json()
    for item in response:
            bot.send_message(message.chat.id, "Nombre                   : " + item['nombre'] + "\n" + "Edad                     : " + item['edad'] + "\n" + "Fecha de nacimiento      : " + item['fecha_nacimiento'])

    #rutificador
    url = "https://rutificador.org/backend.php"
    rut = "{args}".format(args = send_rut.rut_arg)
    data= ({'action':'search_by_rut','rut':'{args}'.format(args = rut.args)})
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
        bot.send_message(message.chat.id, 'Nombre completo: ' + nombre1 + ' ' + nombre2 + ' ' + apellido1 + ' ' + apellido2 + '\n' + 'Rut: ' + rut + '\n' + 'Sexo: ' + sexo + '\n' + 'Direccion: ' + direccion + '\n' + 'Comuna: ' + comuna)
    else: 
        bot.send_message(message.chat.id, 'No se encontro ese rut')






#add polling
bot.infinity_polling()
