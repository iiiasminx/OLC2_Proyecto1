from flask import Flask, render_template, request, jsonify

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
        #entrada = request.form['entrada']
        #print(entrada)
        return jsonify('algo pasa acá')


if __name__ == '__main__':
    app.debug = True
    app.run()