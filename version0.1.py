#!/usr/bin/env python
import csv
import os
import sys
from datetime import datetime
from flask import Flask, render_template, redirect, url_for, flash, session
from flask_bootstrap import Bootstrap
# from flask_moment import Moment
from flask_script import Manager
from forms import LoginForm, SaludarForm, RegistrarForm

app = Flask(__name__)
manager = Manager(app)
bootstrap = Bootstrap(app)
# moment = Moment(app)

app.config['SECRET_KEY'] = 'un string que funcione como llave'

"""def lista_directorio ():
	lista_archivos = []
	for file in os.listdir('.'):
		lista_archivos = lista_archivos.append(file)
	return lista_archivos"""

"""def leer_archivo():
	with open('lalala.csv', 'r') as csv_file:
		csv = csv.reader(csv_file)"""

#def existe_archivo():
	#if leer_archivo
	
	#csv_path = './static/incendios.csv'
csv_obj = csv.DictReader(open('lalala.csv', 'r'))
csv_list = list(csv_obj)

	
"""@app.route('/prueba')
def ver_datos():
	return render_template('prueba.html',
     lista=csv_list)"""

@app.route('/prueba')
def verif_archivo():
	msg_err_cant = ''
	cont_err_cant = 0
	msg_err_blank = ''
	for 'CODIGO' in csv_obj:
		print (CODIGO)
		#if row == '':
		#	print('LCDTM')
		#	msg_err_blank = 'CODIGO se encuentra vacio'
		
	for line in csv_list:		
		largo = len(line)
		if largo != 5:
			cont_err_cant = cont_err_cant + 1
	
	if cont_err_cant > 0:
		msg_err_cant = 'El archivo contiene en sus registros más campos que los indicados.'
	variable = os.path.isfile('lalala.csv')
	return render_template('prueba.html',lista=variable, largo=msg_err_cant, codigo_blank=msg_err_blank)
	
@app.route('/prodcompradosxcli')
def prod_por_cliente():
	return render_template('prod_x_cli.html')
 
@app.route('/clicompraronxprod')
def cli_por_prod():
	return render_template('cli_x_prod.html')
	
@app.route('/prodmasvend')
def prod_mas_vendido():
	return render_template('prod_mas_vendido.html')

@app.route('/climayorgasto')
def cli_mas_gasto():
	return render_template('cli_mayor_gasto.html')
	
@app.route('/')
def index():
    return render_template('index.html', fecha_actual=datetime.utcnow())


@app.route('/saludar', methods=['GET', 'POST'])
def saludar():
    formulario = SaludarForm()
    if formulario.validate_on_submit():
        print(formulario.usuario.name)
        return redirect(url_for('saludar_persona', usuario=formulario.usuario.data))
    return render_template('saludar.html', form=formulario)


@app.route('/saludar/<usuario>')
def saludar_persona(usuario):
    return render_template('usuarios.html', nombre=usuario)


@app.errorhandler(404)
def no_encontrado(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def error_interno(e):
    return render_template('500.html'), 500


@app.route('/ingresar', methods=['GET', 'POST'])
def ingresar():
    formulario = LoginForm()
    if formulario.validate_on_submit():
        with open('usuarios') as archivo:
            archivo_csv = csv.reader(archivo)
            registro = next(archivo_csv)
            while registro:
                if formulario.usuario.data == registro[0] and formulario.password.data == registro[1]:
                    flash('Bienvenido')
                    session['username'] = formulario.usuario.data
                    return render_template('ingresado.html')
                registro = next(archivo_csv, None)
            else:
                flash('Revisa nombre de usuario y contrasena')
                return redirect(url_for('ingresar'))
    return render_template('login.html', formulario=formulario)


@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    formulario = RegistrarForm()
    if formulario.validate_on_submit():
        if formulario.password.data == formulario.password_check.data:
            with open('usuarios', 'a+') as archivo:
                archivo_csv = csv.writer(archivo)
                registro = [formulario.usuario.data, formulario.password.data]
                archivo_csv.writerow(registro)
            flash('Usuario creado correctamente')
            return redirect(url_for('ingresar'))
        else:
            flash('Las passwords no matchean')
    return render_template('registrar.html', form=formulario)


@app.route('/secret', methods=['GET'])
def secreto():
    if 'username' in session:
        return render_template('private.html', username=session['username'])
    else:
        return render_template('sin_permiso.html')


@app.route('/logout', methods=['GET'])
def logout():
    if 'username' in session:
        session.pop('username')
        return render_template('logged_out.html')
    else:
        return redirect(url_for('index'))


if __name__ == "__main__":
    # app.run(host='0.0.0.0', debug=True)
    manager.run()
