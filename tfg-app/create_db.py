import sqlite3 # Para la base de datos ligera


conn = sqlite3.connect('databaseTFG.db') # creamos la conexion con la base de datos (si no existe la db, la crea)
c = conn.cursor()
# tabla para almacenar los autores
c.execute(""" CREATE TABLE IF NOT EXISTS autores (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          nombre TEXT UNIQUE,
          firma TEXT)
          """)
# tabla para almacenar los articulos
c.execute(""" CREATE TABLE IF NOT EXISTS articulos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT UNIQUE,
        citas INTEGER DEFAULT 0,
        fecha_publicacion INTERGER,
        enlace TEXT,
        aut_1 TEXT,
        aut_2 TEXT,
        aut_3 TEXT)
          """)
# tabla para almacenar las busquedas
c.execute(""" CREATE TABLE IF NOT EXISTS busquedas (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          busqueda TEXT UNIQUE,
          fecha DATE)
          """)
# tabla que relaciona una busqueda con varios articulos
c.execute(""" CREATE TABLE IF NOT EXISTS busquedas_articulos (
        busqueda_id INTEGER,
        articulo_id INTEGER,
        FOREIGN KEY (busqueda_id) REFERENCES busquedas(id),
        FOREIGN KEY (articulo_id) REFERENCES articulos(id),
        PRIMARY KEY (busqueda_id, articulo_id))
          """)

#Creamos unos datos de prueba
c.execute("INSERT INTO articulos VALUES (1, 'La valoracion de la prueba', 490, 2018, 'http://www.derechopenalenlared.com/libros/la-valoracion-de-la-prueba-jordi-nieva.pdf', 'J Nieva Fenoll', '', '')")
c.execute("INSERT INTO articulos VALUES (2, 'Eportafolios en Procesos Blendedlearning Innovaciones de la Evaluacin en los Crditos Europeos', 56, 2009, 'https://revistas.um.es/redu/article/download/69941/67411', 'R Barragán', 'R García', 'O Buzón')")
c.execute("INSERT INTO busquedas VALUES (1, 'prueba', '25-03-2024')")
c.execute("INSERT INTO busquedas_articulos VALUES (1,1)")
c.execute("INSERT INTO busquedas_articulos VALUES (1,2)")

c.execute('SELECT * FROM articulos')
articulos = c.fetchall() #puede ser fetchone() o fetchmany(x)
#print(articulos)

c.execute('SELECT * FROM busquedas')
busquedas = c.fetchall() #puede ser fetchone() o fetchmany(x)
#print(busquedas)

c.execute('SELECT * FROM busquedas_articulos')
busquedasArticulos = c.fetchall()
#print(busquedasArticulos)

c.execute("""
          SELECT a.* FROM articulos a
          INNER JOIN busquedas_articulos ba ON a.id = ba.articulo_id
          INNER JOIN busquedas b ON b.id = ba.busqueda_id
          WHERE b.id = '1'; """)
rdo = c.fetchall()
#print(rdo)

conn.commit() # Para que se guarden los cambis
conn.close() # Cerramos la conexion (buena practica)