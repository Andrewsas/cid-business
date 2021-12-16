from flask import Flask, render_template, request, redirect, session, flash, url_for, send_from_directory
import os, time

app = Flask(__name__)
app.secret_key = 'akçsmdakdlçamsd'


@app.route('/novo')
def novo():
    return render_template('novo.html', titulo='Nova predição')


@app.route('/criar', methods=['POST'])
def criar():
    return redirect(url_for('novo'))


@app.route('/')
def login():
    proxima = (request.args.get('proxima') if request.args.get('proxima') != None else '/novo')
    return render_template('login.html', proxima=proxima)


@app.route('/autenticar', methods=['POST'])
def autenticar():
    
    if request.form['user'] == os.environ['USER'] and request.form['pass'] == os.environ['PASS']:
        return redirect(url_for('novo'))
    else:
        flash('Não logado, tente denovo!')
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Nenhum usuário logado!')
    return redirect(url_for('/'))


if __name__ == '__main__': 
    print('start serve')

    from waitress import serve

    serve(app, port=8080)