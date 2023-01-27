from flask import Flask, render_template

app = Flask(__name__)


class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console


@app.route('/inicio')
def ola():
    jogo1 = Jogo('Tetris', 'Puzzle', 'Atari')
    jogo2 = Jogo('God of War', 'Rack and Slash', 'PS2')

    lista_de_jogos = [jogo1, jogo2]

    return render_template('lista.html', titulo='Jogos', jogos=lista_de_jogos)


@app.route('/novo')
def novo():
    return render_template('novo.html', titulo='Novo Jogo', )


app.run(host='0.0.0.0', port=8080)
