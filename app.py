#!/usr/bin/env python
import csv
import os
import sys
import pandas as pd #Utilizamos la libreria pandas para realizar las consultas.
from flask import Flask, render_template, redirect, url_for, flash, session
from flask_bootstrap import Bootstrap
from flask_script import Manager
from forms import LoginForm, ConsultaForm, RegistrarForm
from IPython.display import HTML

app = Flask(__name__)
manager = Manager(app)
bootstrap = Bootstrap(app)

file_csv = 'lalala.csv' #En esta variable almacenamos el nombre del archivo csv, se puede modificar a gusto

app.config['SECRET_KEY'] = 'un string que funcione como llave'

#abre y guarda el archivo como una lista
with open(file_csv, 'r') as csv_file:
	csv_obj = csv.reader(csv_file)
	csv_list = list(csv_obj)
	
#abre y guarda el archivo como un diccionario
csv_obj_dict = csv.DictReader(open(file_csv, 'r'))
csv_dict = list(csv_obj_dict)

msg_err_cant = ''
cont_err_cant = 0
msg_err_blank = ''
msg_err_int =''
msg_err_precio =''
msg_err_code =''
variable=''

#Recorre la lista de diccionarios para realizar las consultas 
for obj in csv_dict:
	
	#Valida que CODIGO no se encuentre vacio
	if obj['CODIGO'] ==  '': 
		msg_err_blank = 'Hay registros de CÓDIGO que se encuentran vacios'
	#####
	
	#Valida que Cantidad sea un entero
	try:	
		entero = int(obj['CANTIDAD'])
	except:
		msg_err_int= 'La cantidad contiene uno o más numeros que no son enteros'
	#####
	
	#Valida que el precio sea un decimal
	if '.' not in obj['PRECIO']:
		msg_err_precio = 'El precio contiene uno o más números que no son decimales'			
	####
	
	#Valida que codigo este compuesto correctamente
	if obj['CODIGO'] != '':
		codigo = obj['CODIGO']
		letras = codigo[0:3]
		numeros = codigo[3:6]
		if numeros.isnumeric() and letras.isalpha():
			dummy = 'dummy'
		else:
			msg_err_code = 'El codigo no tiene un formato correcto'
	#######
	
	#Valida que no haya más de 5 campos
for line in csv_list:
	largo = len(line)
	if largo != 5:
		cont_err_cant = cont_err_cant + 1
if cont_err_cant > 0:
	msg_err_cant = 'El archivo contiene en sus registros más campos que los indicados.'
	########	
	
	#Valida que el archivo exista
if os.path.isfile(file_csv) == False:
	variable = 'El archivo no existe'
	######

#Chequea si hay alguna validacion que no pase y le agrega el numero correspondiente, esto será usado principalmente en los html para manejar que mostrará
if msg_err_cant != '' or cont_err_cant != 0 or msg_err_blank != '' or msg_err_int != '' or msg_err_precio != '' or variable != '' or msg_err_code != '':
	validacion = 0
else:
	validacion = 1
########

#Routeará a la pagina de validacion
@app.route('/validacion')
def validaciones():
	return render_template('prueba.html', archivo_exist=variable, largo=msg_err_cant, codigo_blank=msg_err_blank, codigo_int=msg_err_int, codigo_code=msg_err_code, codigo_precio=msg_err_precio, checkeo = validacion)

#Routeará a la pagina de Productos comprados por X cliente. Allí tomará la consulta desde el formulario, y buscará si existe un cliente con ese nombre. Si existe, poblará la tabla con los datos
@app.route('/prodcli',methods=['GET', 'POST'])
def prod_por_cliente():
	cons = ''
	ARCHIVO_1 = file_csv
	df = pd.read_csv(ARCHIVO_1) 
	formulario = ConsultaForm() 
	if formulario.validate_on_submit():
		cons = str(formulario.consulta.data) 
	respuesta = df[df.CLIENTE.str.upper() == cons.upper()] 
	respuesta = respuesta.groupby(by=['CODIGO','CLIENTE','PRODUCTO','CANTIDAD'], as_index=False).sum()
			
	return render_template('prodcli.html', prod_cli = respuesta, form=formulario)

#Routeará a la pagina de quienes compraron X producto. Allí tomará la consulta desde el formulario, y buscará si existe un producto con ese nombre. Si existe, poblará la tabla con los datos
@app.route('/clicompraronxprod',methods=['GET', 'POST'])
def cli_por_prod():
	cons = ''
	ARCHIVO_1 = file_csv
	df = pd.read_csv(ARCHIVO_1)
	formulario = ConsultaForm()
	if formulario.validate_on_submit():
		cons = str(formulario.consulta.data)
	respuesta = df[df.PRODUCTO.str.upper() == cons.upper()]
	respuesta = respuesta.groupby(by=['CODIGO','PRODUCTO','CLIENTE','CANTIDAD'], as_index=False).sum()
    #respuesta = respuesta.sort_values(by=['TOTAL'])
	return render_template('cli_x_prod.html', cli_prod=respuesta, form=formulario)

	
#Routeará a la pagina de productos mas vendidos. Se le realiza un group by para agruparlos en caso de que se repitan, y luego se ordenará el resultado segun cantidad
@app.route('/prodmasvend')
def prod_mas_vendido():
	ARCHIVO_1 = file_csv 
	df = pd.read_csv(ARCHIVO_1) #traigo el archivo csv, que lo convertirá en un dataframe
	respuesta = df.groupby(by=['PRODUCTO'], as_index=False).sum()
	respuesta = respuesta.sort_values(by=['CANTIDAD'], ascending = False) #Ordena por los valores a cantidad.
	return render_template('prod_mas_vendido.html', prod_vend=respuesta)
	
#Routeará a la pagina de que clientes gastaron más. Se creará la columna total producto de la multiplicacion de cantidad por precio, agrupará por cliente y luego ordenará por total.
@app.route('/climayorgasto')
def cli_mas_gasto():
	ARCHIVO_1 = file_csv 
	df = pd.read_csv(ARCHIVO_1)
	df['TOTAL'] = df['CANTIDAD']*df['PRECIO']# creamos una columna total el cual va indicar el multiplo de cantidad y precio
	respuesta = df.groupby(by=['CLIENTE'], as_index=False).sum() # se va agrupar por cliente
	respuesta = respuesta.sort_values(by=['TOTAL'], ascending = False)
	return render_template('cli_mayor_gasto.html', cli_gasto = respuesta )
	
#Routea al inicio	
@app.route('/')
def index():
    return render_template('index.html')

#Maneja el error 404
@app.errorhandler(404)
def no_encontrado(e):
    return render_template('404.html'), 404

#Maneja el error 500
@app.errorhandler(500)
def error_interno(e):
    return render_template('500.html'), 500

#Routea a la página de ingreso al sistema. Allí el usuario ingresa sus credenciales, si son correctas, ingresará al sistema y sino se le pedirá que vuelva a ingresar sus credenciales. Estos datos para el ingreso son obtenidos desde usuarios.csv.
@app.route('/ingresar', methods=['GET', 'POST'])
def ingresar():
    formulario = LoginForm()
    if formulario.validate_on_submit():
        with open('usuarios.csv', 'r') as archivo:
            archivo_csv = csv.reader(archivo)
            registro = next(archivo_csv)
            while registro:
                if formulario.usuario.data == registro[0] and formulario.password.data == registro[1]:
                    session['username'] = formulario.usuario.data
                    return render_template('ingresado.html', checkeo = validacion, lista = csv_dict)
                registro = next(archivo_csv, None)
            else:
                flash('Revisa nombre de usuario y contraseña')
                return redirect(url_for('ingresar'))
    return render_template('login.html', formulario=formulario)


if __name__ == "__main__":
    # app.run(host='0.0.0.0', debug=True)
    manager.run()
