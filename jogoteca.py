from flask import Flask, render_template

app = Flask(__name__)

@app.route('/inicio')
def ola():
    lista_de_jogos = ['Tetris','Skyrim','Crash']
    return render_template('lista.html', titulo = 'Jogos', jogos = lista_de_jogos) 

app.run(host='0.0.0.0', port=8080)
