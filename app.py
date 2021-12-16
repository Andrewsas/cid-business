import os
import pickle
import numpy as np
import xgboost as xgb
import utils.constants as Constants
from flask import Flask, render_template, request, redirect, session, flash, url_for

def load_model(file_name):
    return pickle.load(open(file_name, "rb"))

modelo = load_model(file_name = os.environ['PATH_MODEL'])

app = Flask(__name__)
app.secret_key = os.environ['SECRET']


@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template('novo.html', titulo='Nova predição')


@app.route('/criar', methods=['POST'])
def criar():
    dados = request.get_json()
    payload = np.array([dados[col] for col in Constants.cols])
    payload = xgb.DMatrix([payload], feature_names=Constants.cols)
    _score = np.float64(modelo.predict(payload)[0])
    return redirect()


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