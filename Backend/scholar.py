import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from bs4 import BeautifulSoup
import re # Para expresiones regulares
import pandas as pd
import time # Para poder parar la ejecucion del codigo durante x segundos

app = Flask(__name__)
CORS(app, supports_credentials=True)  

def buscar(idioma, busqueda, paginas):
    
    # listas donde se guardaran los datos
    titulos = list()
    citas = list()
    autores1 = list()
    autores2 = list()
    autores3 = list()
    listaAutores = list()
    anoPublicacion = list()
    link = list()
    
    # direccion base en la que buscar (por ahora google scholar)
    raiz ='https://scholar.google.es/'
    
    # Cambiamos el string a buscar para poder meterlo en la url
    busqueda = busqueda.replace(' ', '+')
    
    # iteramos por las diferentes paginas hasta procesar numero de paginas especificado
    cont=0
    while(cont <= paginas):
        # modifica la url para añadir los parametros de bsuqueda
        url = raiz+f'scholar?hl={idioma}&as_sdt=0%2C5&q={busqueda}&start={str(cont)}0'
        # obtenemos el contenido de lapagina y lo preprocesamos con bs4
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        # nos quedamos con todos los div (en una lista) que tengan como nombre de clase los especificados en la funcion
        resultados = soup.findAll('div', class_='gs_r gs_or gs_scl')
        
        # Iteramos por cada resultado guardando los datos que nos interesan
        for i in resultados:
            
            #separamos la pagina en 2 variables, la que contiene el enlace al documento y el resto
            cuerpo = i.find('div', class_='gs_ri')
            enlace = i.find('div', class_='gs_or_ggsm')
            if cuerpo is not None:
            
                # buscamos el titulo
                if cuerpo.find('h3', class_='gs_rt').find('a'):
                    tit = cuerpo.find('h3', class_='gs_rt').find('a')
                    #eliminamos los caracteres no alfanumericos del titulo
                    titulos.append(re.sub(r'[^a-zA-Z0-9\s]', '', tit.text)) 
                else: titulos.append("No encontrado")
                
                # buscamos las citas
                if cuerpo.find('div', class_='gs_fl').find_all('a')[2]:
                    num_citas = cuerpo.find('div', class_='gs_fl').find_all('a')[2]
                    num_citas = re.findall('[1234567890]+', num_citas.text)
                    if num_citas:
                        citas.append(num_citas[0])
                    else:
                        citas.append('0')
                else: titulos.append("No encontrado")

                # buscamos el autor y la fecha fecha
                if cuerpo.find('div', class_='gs_a'):
                    # aut es un string que contiene los autores del articulo, ademas de la fecha
                    aut = cuerpo.find('div', class_='gs_a')
                    # Con ayuda de la funcion tratar_autores, rescatamos toda la informacion que necesitamos
                    autores1, autores2, autores3, anoPublicacion, listaAutores = tratar_autores(aut, autores1, autores2, autores3, anoPublicacion, listaAutores)
                else: titulos.append("No encontrado")
                
                # enlace del documento (Puede tener o no)
                if enlace != None:
                    link.append(enlace.find('a', href=True)['href'])
                else: 
                    link.append('')
                
        cont +=1
        time.sleep(2) # Paramos la ejecucion 2 segudno para evitar bloqueos de scrapping
            
    # creamos los dataframes y guardamos los datos en csv (se han comentado las lineas que guardan en un archivo estas busquedas)
    df_autores = pd.DataFrame({"Nombre": listaAutores, "firma": ""}) # no se usa actualmente
    #df_autores.to_csv("Lista de autores", index=False)
    df_articulos = pd.DataFrame({'Titulo': titulos, 'Citas': citas, 'Año': anoPublicacion, 'Enlace': link,'Autor 1': autores1, 'Autor 2': autores2, 'Autor 3': autores3, })
    #df_articulos.to_csv("Lista de articulos", index=False)

    #devolvemos un json con los datos procesados
    return jsonify(df_articulos.to_dict(orient='records'))

# Tratamos el string para eliminar todo lo que no sea el nombre del autor o autores, y tambien guardamos la fecha
def tratar_autores(aut, autores1, autores2, autores3, anoPublicacion, listaAutores):
    # variables donde guardaremos los autores y la fecha
    aut1 = ''
    aut2 = ''
    aut3 = ''
    str=''
    fecha = ''
    # variables auxiliares
    seguir = True
    i = 0
    numeros = ['1','2','3','4','5','6','7','8','9','0']

    # iteramos por cada caracter de la lista de autores + fecha.
    for j in aut:
        str = str + j.text
    while(seguir):
        # si no sencontramos un numero, ya no hay mas autores, y lo que sigue es la fecha
        if any(x in numeros for x in list(str.partition('-')[0])):
            seguir = False
            fecha = str.partition('-')[0]
        else:
            aut1 += str.partition('-')[0]
            if str.partition('-')[2] != '' and not re.match('.', str.partition('-')[2]):
                str = str.partition('-')[2]
            else: seguir = False
        
    # algunos nombres de autor vienen separados por un guion, debemos quitarlo
    aut1 = aut1.replace('-', '')
    
    # miramos si hay mas de un autor en la publicacion y los separamos
    if aut1.partition(',')[2] != '':
        aut2 = aut1.partition(',')[2]
        aut1 = aut1.partition(',')[0]
        if aut2.partition(',')[2] != '':
            aut3 = aut2.partition(',')[2]
            aut2 = aut2.partition(',')[0]  
    
    try:
        fecha = re.findall('[1234567890]+', str)[0]
    except:
        fecha = ''
    
    # eliminamos espacis en blanco que puedan haber al principio y al final de los autores
    aut1 = aut1.strip()
    aut2 = aut2.strip()
    aut3 = aut3.strip()
    # Guardamos los tres primeros autores y la fecha
    autores1.append(aut1)
    autores2.append(aut2)
    autores3.append(aut3)
    anoPublicacion = fecha
    # si los autores no son cadenas vacias, los guardo en la listaAutores (una lista para poder guardarlos en un dataframe)
    if aut1 != '' : listaAutores.append(aut1)
    if aut2 != '' : listaAutores.append(aut2)          
    if aut3 != '' : listaAutores.append(aut3)
    listaAutores = list(set(listaAutores)) #elimino autores repetidos
    
    return autores1, autores2, autores3, anoPublicacion, listaAutores 