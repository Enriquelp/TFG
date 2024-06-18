from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3 # Para la base de datos ligera
import json
from datetime import datetime # Para obtener la fecha en la que se realizo la busqueda
import scholar # Script que hace el scraping en Google Scholar

app = Flask(__name__)
CORS(app, supports_credentials=True)  

# Devuelve una lista de articulos encontrados en scholar
@app.route('/api/buscar-online', methods = ['GET']) 
def buscarEnScholar():
    # Recogemos los datos del Frontend
    idioma = request.args.get('idioma')
    busqueda = request.args.get('busqueda')
    paginas = int(request.args.get('paginas'))
    # invocamos al scraper para scholar, pasando los parametros de la busqueda
    return scholar.buscar(idioma, busqueda, paginas)


# Devuelve una lista de las busquedas almacenadas
@app.route('/api/busquedas-anteriores', methods = ['GET']) 
def buscarbd():
    # creamos la conexion con la base de datos (si no existe la db, la crea)
    conn = sqlite3.connect('databaseTFG.db') 
    c = conn.cursor()
    # ejecutamos la sentencia SQL
    c.execute('SELECT * FROM busquedas')
    # guardamos en una variable (una lista) los resultados de la consulta
    busquedas = c.fetchall()
    # cerramos la conexion con la bd
    conn.close()
    return busquedas

# Busca los articulos de una determinada busqueda
@app.route('/api/busqueda-bd', methods = ['GET']) 
def buscarPorId():
    # creamos la conexion con la base de datos (si no existe la db, la crea)
    conn = sqlite3.connect('databaseTFG.db') 
    c = conn.cursor()
    # recibimos el id de la busqueda que queremos encontrar en la bd
    id = request.args.get('idBusqueda') 
    # Ejecutamos la sentencia SQL
    c.execute("""
          SELECT a.titulo, a.citas, a.fecha_publicacion, a.enlace, a.aut_1, a.aut_2, a.aut_3 FROM articulos a
          INNER JOIN busquedas_articulos ba ON a.id = ba.articulo_id
          INNER JOIN busquedas b ON b.id = ba.busqueda_id
          WHERE b.id = ?; """, (id,))
    # guardamos en una variable (una lista) los resultados de la consulta
    filas = c.fetchall()
    # Iteramos sobre cada fila de la consulta SQL y la guardamos en una lista
    resultados = []
    for fila in filas:
        rdo = {
            'Titulo': fila[0],
            'Citas': fila[1],
            'Año': fila[2],
            'Enlace': fila[3],
            'Autor 1': fila[4],
            'Autor 2': fila[5],
            'Autor 3': fila[6],
        }
        resultados.append(rdo)
    # Creamos el json que devuelve la funcion
    resultados_json = json.dumps(resultados, indent=4)
    # cerramos la conexion con la bd
    conn.close()
    return resultados_json


# Almacena la busqueda realizada relacionandola con los articulos encontrados en dicha busqueda
@app.route('/api/almacenarBusqueda', methods=['POST'])
def almacenarBusqueda():
    # recibimos los datos del frontend
    data = request.json
    busqueda = data['busqueda']
    articulos = data['articulos']
    # creamos la conexion con la base de datos (si no existe la db, la crea)
    conn = sqlite3.connect('databaseTFG.db') 
    c = conn.cursor()
    # añadimos la busqueda y guardamos los cambios, quedandonos con el id de la busqueda añadida
    try: 
        c.execute(""" INSERT INTO busquedas (busqueda, fecha) values (?,?)""", (busqueda, datetime.now().strftime("%d-%m-%Y")))
        conn.commit()
        idBusqueda = c.lastrowid
    # si ya estuviera almacenada, buscamos el id y actualizamos la fecha de busqueda
    except sqlite3.IntegrityError: 
        print("Esta busqueda ya se ha realizado antes")
        c.execute(""" SELECT id from busquedas WHERE busqueda = ? """, (busqueda,))
        idBusqueda = c.fetchone()[0]
        c.execute(""" UPDATE busquedas SET fecha = ? WHERE id = ? """, (datetime.now().strftime("%d-%m-%Y"), idBusqueda)) # Actualizamos la fecha de busqueda
        conn.commit()
    # añadimos cada articulo que se haya encontrado   
    for articulo in articulos: 
        try:
            c.execute("""INSERT INTO articulos (titulo, citas, fecha_publicacion, enlace, aut_1, aut_2, aut_3) values (?,?,?,?,?,?,?)""" , (articulo['Titulo'], articulo['Citas'], articulo['Año'], articulo['Enlace'], articulo['Autor 1'], articulo['Autor 2'], articulo['Autor 3']))
            conn.commit()        
            idArticulo = c.lastrowid
        except sqlite3.IntegrityError:
            print("El articulo ya existe en la base de datos")
            c.execute(""" SELECT id from articulos WHERE titulo = ? """, (articulo['Titulo'],))
            idArticulo = c.fetchone()[0]
        # añadimos la relacion entre la busqueda y el articulo 
        try: 
            c.execute(""" INSERT INTO busquedas_articulos values (?,?)""", (idBusqueda, idArticulo))
            conn.commit()
        except sqlite3.IntegrityError:
            print("Relacion entre busqueda y articulo ya existente")
        # añadimos al primer autor si existe
        if articulo['Autor 1'] != '': 
            try: 
                c.execute(""" INSERT INTO autores (nombre) VALUES (?) """, (articulo['Autor 1'],))
                idAutor1 = c.lastrowid
                conn.commit()
            except sqlite3.IntegrityError:
                c.execute(""" SELECT id from autores WHERE nombre = ? """, (articulo['Autor 1'],))
                idAutor1 = c.fetchone()[0]
                print ("El autor ya existe")
            # añadimos la relacion entre el articulo y el primer autor
            try: 
                c.execute(""" INSERT INTO autores_articulos values (?,?) """, (idAutor1, idArticulo))
                conn.commit()
            except sqlite3.IntegrityError:
                print ("Relacion entre articulo y autor 1 ya existente")
        # añadimos al segundo autor si existe
        if articulo['Autor 2'] != '':
            try: 
                c.execute(""" INSERT INTO autores (nombre) VALUES (?) """, (articulo['Autor 2'],))
                idAutor2 = c.lastrowid
                conn.commit()
            except sqlite3.IntegrityError:
                c.execute(""" SELECT id from autores WHERE nombre = ? """, (articulo['Autor 2'],))
                idAutor2 = c.fetchone()[0]
                print ("El autor ya existe")
            # añadimos la relacion entre el articulo y el segundo autor
            try: 
                c.execute(""" INSERT INTO autores_articulos values (?,?) """, (idAutor2, idArticulo))
                conn.commit()
            except sqlite3.IntegrityError:
                print ("Relacion entre articulo y autor 1 ya existente")  
    # cerramos la conexion con la bd y devolvemos un mensaje de que no ha habido errores. 
    conn.close
    return jsonify({'message': 'Datos almacenados correctamente'}), 200

# Borra la busqueda de la base de datos
@app.route('/api/borrarBusqueda', methods=['POST'])
def borrarBusqueda():
    # recibimos los datos del Frontend
    data = request.json
    id = data['id']
    # creamos la conexion con la base de datos (si no existe la db, la crea)
    conn = sqlite3.connect('databaseTFG.db') 
    c = conn.cursor()
    # Borra la relacion entre la busqueda y el articulo 
    c.execute("""DELETE FROM busquedas_articulos
        WHERE busqueda_id = ?; """, (id,))
    # borra la busqueda
    c.execute("""DELETE FROM busquedas
        WHERE id = ?; """, (id,))
    # guardamos los cambios, cerramos la conexion y devolvemos mensaje de que se ha borrado correctamente
    conn.commit()
    conn.close()
    return jsonify({'message': 'Busqueda borrada correctamente'}), 200

# EndPoint de prueba para comprobar que el Backend y el Fronend se pueden comunicar.
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