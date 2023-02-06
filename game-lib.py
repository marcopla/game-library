from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'alura'

app.config['SQLALCHEMY_DATABASE_URI'] = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
    SGBD = 'mysql+mysqlconnector',
    usuario = 'root',
    senha = 'Mysql!',
    servidor = 'localhost',
    database = 'jogoteca'
    )

db = SQLAlchemy(app)

        
@app.route('/')
def index():
    lista_de_jogos = Jogos.query.order_by(Jogos.id)
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

    jogo = Jogos.query.filter_by(nome=nome).first()
    if jogo:
        flash('Jogo já existente!')
        return redirect(url_for('index'))
    
    novo_jogo = Jogos(nome=nome, categoria=categoria, console=console)
    db.session.add(novo_jogo)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/login')
def login():
    proxima = request.args.get('proxima')

    return render_template('login.html', proxima = proxima)


@app.route('/autenticar', methods = ['POST',])                                                                                   
def autenticar():
    usuario = Usuarios.query.filter_by(nickname=request.form['usuario']).first()
    if usuario:
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
