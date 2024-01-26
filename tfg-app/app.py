from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/buscar')
def hello_world():
    return 'Hola, mundo!'

if __name__ == '__main__':
    app.run(debug=True)