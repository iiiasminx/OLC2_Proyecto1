from flask import Flask, render_template, request, jsonify
from gramatica import fighting
from sintactico import fighting2

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
        mesg =  fighting2(entrada)
        #mesg = 'este es mi codigo traducido y toda la onda' + entrada
        return render_template('index.html', mesg=mesg, entrada=entrada)

@app.route('/submit', methods=['GET'])
def submit2():
    if request.method == 'GET':
        return render_template('index.html')

if __name__ == '__main__':
    app.debug = True
    app.run()