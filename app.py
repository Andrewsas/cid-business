import os
import json
from utils.model_predict import ModelPredict
from flask import Flask, render_template, request, redirect, session, flash, url_for

app = Flask(__name__)
app.secret_key = os.environ['SECRET']

model = ModelPredict()

@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template('novo.html', titulo='Interesse de Aquisição')


@app.route('/criar', methods=['POST'])
def criar():
    data = model.predict(request.form)
    msg = "Alta probabilidade de Aquisição" if data > 0.7 else "Baixa probabilidade de Aquisição"
    flash(msg)
    return redirect(url_for('novo'))


@app.route('/')
def login():
    if 'usuario_logado' in session or session['usuario_logado'] != None:
        return redirect(url_for('novo'))
    proxima = (request.args.get('proxima') if request.args.get('proxima') != None else '/novo')
    return render_template('login.html', proxima=proxima)


@app.route('/autenticar', methods=['POST'])
def autenticar():
    
    if request.form['user'] == os.environ['USER'] and request.form['pass'] == os.environ['PASS']:
        session['usuario_logado'] = request.form['user']
        flash(request.form['user'] + ' logou com sucesso!')
        proxima_pagina = request.form['proxima']
        return redirect(proxima_pagina if request.form['proxima'] != None else url_for('novo'))
    else:
        flash('Não logado, tente denovo!')
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Nenhum usuário logado!')
    return redirect(url_for('login'))


if __name__ == '__main__': 
    print('start serve')

    from waitress import serve

    serve(app, port=8080)