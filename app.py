from flask import Flask, render_template, request, jsonify
import json

from gramatica import fighting
from sintactico import fighting2
from cst import NodoSimbolo, NodoError, Exporte #Falta el AST cuando entienda que pex xdxd

app = Flask(__name__, static_url_path='')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/reportes')
def reportes():
    return render_template('reportes.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        entrada = request.form['entrada']
        print('Este es ->' + entrada)
        fighting(entrada) #lexico

        #todo lo que viene del analizador
        importe =  fighting2(entrada) 

        # codigo interpretado
        mesg = importe.interpretacion

        #lista de errores
        listaErrores = importe.tabla_errores
        json_string2 = json.dumps([ob.__dict__ for ob in listaErrores])

        return render_template('index.html', mesg=mesg, entrada=entrada, listaErrores=listaErrores)

@app.route('/submit', methods=['GET'])
def submit2():
    if request.method == 'GET':
        return render_template('index.html')

if __name__ == '__main__':
    app.debug = True
    app.run()