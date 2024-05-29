from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3 # Para la base de datos ligera
import json
from datetime import datetime # Para obtener la fecha en la que se realizo la busqueda
import scholar

app = Flask(__name__)
CORS(app, supports_credentials=True)  

# Devuelve una lista de articulos encontrados en scholar
@app.route('/api/buscar-online', methods = ['GET']) 

def buscarEnScholar():
    idioma = request.args.get('idioma')
    busqueda = request.args.get('busqueda')
    paginas = int(request.args.get('paginas'))

    return scholar.buscar(idioma, busqueda, paginas)


# devuelve una lista de las busquedas almacenadas
@app.route('/api/busquedas-anteriores', methods = ['GET']) 
def buscarbd():
    conn = sqlite3.connect('databaseTFG.db') # creamos la conexion con la base de datos (si no existe la db, la crea)
    c = conn.cursor()
    c.execute('SELECT * FROM busquedas')
    busquedas = c.fetchall()
    conn.close()
    return busquedas

# Busca los articulos de una determinada busqueda
@app.route('/api/busqueda-bd', methods = ['GET']) 
def buscarPorId():
    conn = sqlite3.connect('databaseTFG.db') # creamos la conexion con la base de datos (si no existe la db, la crea)
    c = conn.cursor()
    id = request.args.get('idBusqueda')
    c.execute("""
          SELECT a.titulo, a.citas, a.fecha_publicacion, a.enlace, a.aut_1, a.aut_2, a.aut_3 FROM articulos a
          INNER JOIN busquedas_articulos ba ON a.id = ba.articulo_id
          INNER JOIN busquedas b ON b.id = ba.busqueda_id
          WHERE b.id = ?; """, (id,))
    filas = c.fetchall()
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
    resultados_json = json.dumps(resultados, indent=4)
    conn.close()
    return resultados_json

@app.route('/api/test', methods=['GET'])
def saludar():
    idioma = request.args.get('idioma')
    busqueda = request.args.get('busqueda')
    paginas = request.args.get('paginas')
    print(busqueda, idioma, paginas)
    data = {"mensaje": "Hola desde Flask!", "busqueda": busqueda}
    return jsonify(data)

# Almacena la busqueda realizada relacionandola con los articulos encontrados en dicha busqueda
@app.route('/api/almacenarBusqueda', methods=['POST'])
def almacenarBusqueda():
    data = request.json
    busqueda = data['busqueda']
    articulos = data['articulos']
    
    print("Búsqueda:", busqueda)
    print("Artículos:", articulos)

    
    
    conn = sqlite3.connect('databaseTFG.db') # creamos la conexion con la base de datos (si no existe la db, la crea)
    c = conn.cursor()
    
    
    try: # añadimos la busqueda
        c.execute(""" INSERT INTO busquedas (busqueda, fecha) values (?,?)""", (busqueda, datetime.now().strftime("%d-%m-%Y")))
        conn.commit()
        idBusqueda = c.lastrowid
    except sqlite3.IntegrityError: # si ya estuviera, buscamos el id
        print("Esta busqueda ya se ha realizado antes")
        c.execute(""" SELECT id from busquedas WHERE busqueda = ? """, (busqueda,))
        idBusqueda = c.fetchone()[0]
        c.execute(""" UPDATE busquedas SET fecha = ? WHERE id = ? """, (datetime.now().strftime("%d-%m-%Y"), idBusqueda)) # Actualizamos la fecha de busqueda
        conn.commit()
        
    for articulo in articulos: # añadimos cada articulo que se haya encontrado
        try:
            c.execute("""INSERT INTO articulos (titulo, citas, fecha_publicacion, enlace, aut_1, aut_2, aut_3) values (?,?,?,?,?,?,?)""" , (articulo['Titulo'], articulo['Citas'], articulo['Año'], articulo['Enlace'], articulo['Autor 1'], articulo['Autor 2'], articulo['Autor 3']))
            conn.commit()        
            idArticulo = c.lastrowid
        except sqlite3.IntegrityError:
            print("El articulo ya existe en la base de datos")
            c.execute(""" SELECT id from articulos WHERE titulo = ? """, (articulo['Titulo'],))
            idArticulo = c.fetchone()[0]
        
        try: # añadimos la relacion entre la busqueda y el articulo 
            c.execute(""" INSERT INTO busquedas_articulos values (?,?)""", (idBusqueda, idArticulo))
            conn.commit()
        except sqlite3.IntegrityError:
            print("Relacion entre busqueda y articulo ya existente")
        
        if articulo['Autor 1'] != '': 
            try: # añadimos al primer autor
                c.execute(""" INSERT INTO autores (nombre) VALUES (?) """, (articulo['Autor 1'],))
                idAutor1 = c.lastrowid
                conn.commit()
            except sqlite3.IntegrityError:
                c.execute(""" SELECT id from autores WHERE nombre = ? """, (articulo['Autor 1'],))
                idAutor1 = c.fetchone()[0]
                print ("El autor ya existe")
                
            try: # añadimos la relacion entre el articulo y el primer autor
                c.execute(""" INSERT INTO autores_articulos values (?,?) """, (idAutor1, idArticulo))
                conn.commit()
            except sqlite3.IntegrityError:
                print ("Relacion entre articulo y autor 1 ya existente")
        
        if articulo['Autor 2'] != '':
            try: # añadimos al segundo autor
                c.execute(""" INSERT INTO autores (nombre) VALUES (?) """, (articulo['Autor 2'],))
                idAutor2 = c.lastrowid
                conn.commit()
            except sqlite3.IntegrityError:
                c.execute(""" SELECT id from autores WHERE nombre = ? """, (articulo['Autor 2'],))
                idAutor2 = c.fetchone()[0]
                print ("El autor ya existe")

            try: # añadimos la relacion entre el articulo y el segundo autor
                c.execute(""" INSERT INTO autores_articulos values (?,?) """, (idAutor2, idArticulo))
                conn.commit()
            except sqlite3.IntegrityError:
                print ("Relacion entre articulo y autor 1 ya existente")  
        
    conn.close
    return jsonify({'message': 'Datos almacenados correctamente'}), 200

@app.route('/api/borrarBusqueda', methods=['POST'])
def borrarBusqueda():
    data = request.json
    id = data['id']
    
    conn = sqlite3.connect('databaseTFG.db') # creamos la conexion con la base de datos (si no existe la db, la crea)
    c = conn.cursor()
    
    c.execute("""DELETE FROM busquedas_articulos
        WHERE busqueda_id = ?; """, (id,))
    
    c.execute("""DELETE FROM busquedas
        WHERE id = ?; """, (id,))
 
    conn.commit()
    conn.close()
    return jsonify({'message': 'Busqueda borrada correctamente'}), 200

if __name__ == '__main__':
    app.run(debug=True) 