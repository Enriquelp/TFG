from flask import Flask, jsonify, request
from flask_cors import CORS
from bs4 import BeautifulSoup
import requests
import pandas as pd
import re # Para expresiones regulares

app = Flask(__name__)
CORS(app, supports_credentials=True)  

@app.route('/api/buscaronline', methods = ['GET'])
def buscar():

    idioma = request.args.get('idioma')
    busqueda = request.args.get('busqueda')
    paginas = int(request.args.get('paginas'))
    
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
    
    # iteramos por lass diferentes paginas hasta llegar al numero de paginas especificado
    cont=0
    while(cont <= paginas):
        url = raiz+f'scholar?hl={idioma}&as_sdt=0%2C5&q={busqueda}&start={str(cont)}0'
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        resultados = soup.findAll('div', class_='gs_r gs_or gs_scl')
        
        
        # Iteramos por cada resultado guardando los datos que nos interesan
        for i in resultados:
            
            #separamos la pagina en 2 variables, la que contiene el enlace al documento y el resto
            cuerpo = i.find('div', class_='gs_ri')
            enlace = i.find('div', class_='gs_or_ggsm')
            if cuerpo is not None:
            
                # titulo
                if cuerpo.find('h3', class_='gs_rt').find('a'):
                    tit = cuerpo.find('h3', class_='gs_rt').find('a')
                    titulos.append(re.sub(r'[^a-zA-Z0-9\s]', '', tit.text)) #eliminamos los caracteres no alfanumericos del titulo
                else: titulos.append("No encontrado")
                
                # citas
                if cuerpo.find('div', class_='gs_fl').find_all('a')[2]:
                    num_citas = cuerpo.find('div', class_='gs_fl').find_all('a')[2]
                    num_citas = re.findall('[1234567890]+', num_citas.text)
                    if num_citas:
                        citas.append(num_citas[0])
                    else:
                        citas.append('0')
                else: titulos.append("No encontrado")

                # autor y fecha
                if cuerpo.find('div', class_='gs_a'):
                    aut = cuerpo.find('div', class_='gs_a')
                    autores1, autores2, autores3, anoPublicacion, listaAutores = tratar_autores(aut, autores1, autores2, autores3, anoPublicacion, listaAutores)
                else: titulos.append("No encontrado")
                
                # enlace del documento (Puede tener o no)
                if enlace != None:
                    link.append(enlace.find('a', href=True)['href'])
                else: 
                    link.append('')
                
        cont +=1
            
    # creamos los dataframe y guardamos los datos en csv
    df_autores = pd.DataFrame({"Nombre": listaAutores, "firma": ""})
    df_autores.to_csv("/src/app/assets/Lista_de_autores.csv", index=False)
    #print(df_autores)
    df_articulos = pd.DataFrame({'Titulo': titulos, 'Citas': citas, 'Autor 1': autores1, 'Autor 2': autores2, 'Autor 3': autores3, 'Año': anoPublicacion, 'Enlace': link})
    df_articulos.to_csv("/src/app/assets/Lista_de_articulos.csv", index=False)
    print(df_articulos) 
    return jsonify(df_articulos.to_dict(orient='records'))

# Tratamos el string para eliminar todo lo que no sea el nombre del autor o autores, y de paso guardamos la fecha
def tratar_autores(aut, autores1, autores2, autores3, anoPublicacion, listaAutores):
    aut1 = ''
    aut2 = ''
    aut3 = ''
    str=''
    fecha = ''
    seguir = True
    i = 0
    numeros = ['1','2','3','4','5','6','7','8','9','0']
    for j in aut:
        str = str + j.text
    while(seguir):
        if any(x in numeros for x in list(str.partition('-')[0])):
            seguir = False
            fecha = str.partition('-')[0]
        else:
            aut1 += str.partition('-')[0]
            if str.partition('-')[2] != '' and not re.match('.', str.partition('-')[2]):
                str = str.partition('-')[2]
            else: seguir = False
        
    
    aut1 = aut1.replace('-', '')
    
    # miramos si hay mas de un autor en la publicacion y los separamos
    if aut1.partition(',')[2] != '':
        aut2 = aut1.partition(',')[2]
        aut1 = aut1.partition(',')[0]
        if aut2.partition(',')[2] != '':
            aut3 = aut2.partition(',')[2]
            aut2 = aut2.partition(',')[0]
    
    fecha = re.findall('[1234567890]+', str)[0]
    
    aut1 = aut1.strip()
    aut2 = aut2.strip()
    aut3 = aut3.strip()
    
    autores1.append(aut1)
    autores2.append(aut2)
    autores3.append(aut3)
    anoPublicacion = fecha
    if aut1 != '' : listaAutores.append(aut1)
    if aut2 != '' : listaAutores.append(aut2)          
    if aut3 != '' : listaAutores.append(aut3)
    listaAutores = list(set(listaAutores)) #elimino autores repetidos
    
    return autores1, autores2, autores3, anoPublicacion, listaAutores 

@app.route('/api/buscarbd')
def buscarbd():
    return 'Buscar en base de datos'


@app.route('/api/test', methods=['GET'])
def saludar():
    idioma = request.args.get('idioma')
    busqueda = request.args.get('busqueda')
    paginas = request.args.get('paginas')
    print(busqueda, idioma, paginas)
    data = {"mensaje": "Hola desde Flask!", "busqueda": busqueda}
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)