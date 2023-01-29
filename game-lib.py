from flask import Flask, render_template, request, redirect, session, flash, url_for

app = Flask(__name__)
app.secret_key = 'alura'

class Jogo:
    def __init__(self, name, category, console):
        self.name = name
        self.category = category
        self.console = console

class Usuario:
    def __init__(self, nome, nickname, senha):
        self.nome = nome
        self.nickname = nickname
        self.senha = senha

usuario1 = Usuario('Guilherme Divino', 'BD', 'alohomora')
usuario2 = Usuario('Camila Ferreira', 'MIla', 'paozinho')
usuario3 = Usuario('Guilherme Louro', 'Cake', 'python_eh_vida')

usuarios = {usuario1.nickname : usuario1,
            usuario2.nickname : usuario2,
            usuario3.nickname : usuario3}

jogo1 = Jogo('Tetris', 'Puzzle', 'Atari')
jogo2 = Jogo('God of War', 'Rack and Slash', 'PS2')

lista_de_jogos = [jogo1, jogo2]

@app.route('/')
def index():
    return render_template('lista.html', title='Games', games = lista_de_jogos)


@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima = url_for('novo')))   
    return render_template('novo.html', title ='New Game' )

@app.route('/criar', methods = ['POST',])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console)
    lista_de_jogos.append(jogo)
    return redirect(url_for('index'))

@app.route('/login')
def login():
    proxima = request.args.get('proxima')

    return render_template('login.html', proxima = proxima)

@app.route('/autenticar', methods = ['POST',])                                                                                   
def autenticar():
    if request.form['usuario'] in usuarios:
        usuario = usuarios[request.form['usuario']]
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.nickname
            flash( usuario.nickname + ' ' + 'logado com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
        else: 
            flash('Usuário ou senha inválidos!')
            return redirect(url_for('login'))    
    else: 
        flash('Usuário ou senha inválidos!')
        return redirect(url_for('login'))            

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso')
    return redirect(url_for('login'))


app.run(host = '0.0.0.0', port = 8080, debug = True)
