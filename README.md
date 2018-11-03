Documentacion del SISTEMA honeyBees s.a.

Para poder ejecutar el programa por favor ingesar el siguiente comando "pipenv intall" dentro de cmd y posicionado dentro de la carpeta donde se encuentra el codigo.

Flujo de ejecucion.
El sistema cuanta con un flujo sencillo, cuenta con funciones, las cuales se encargan de hacer las consultas y manejo de todo el archivo .csv. Por medio de jinja/html se hace todo lo que se muestra por el buscador web.

Como utilizar el sistema:
Primero el sistema pedirá un ingreso o logueo de un usuario, para que este pueda generar consultas sobre la venta de productos de la compañia. Si el usuario no se loguea, no podrá consultar los datos.
Una vez logueado se mostrara la tabla general de ventas si es que el archivo es correcto y pasa las validaciones, a su vez, podrá utilizar las ventanas de consultas. Si el archivo no es correcto y/o no pasa las validaciones, estás se indicarán en la pestaña de 'Validaciones' y no tendrá acceso a las consultas.
Las consultas serán las siguientes:
 - Que se ingrese el nombre del cliente a averiguar, y mostrará todos los productos que compró.
 - Que se ingrese el nombre del producto a averiguar, y mostrará todos los clientes que lo compraron.
 - Una lista de los productos más vendidos
 - Una lista de los clientes que mayor dinero gastaron

Librerias:

	csv: para poder manejar todo lo referido a los archivos .csv, tanto su apertura como recorrido para las validaciones.
	pandas: Para poder manejar el .csv de una manera sencilla de una forma similar a generar consultas sql.
	forms: para poder utilizar los formularios, que se encuentran creados en forms.py.
	OS: Para poder ver el path del archivo.

Funciones utilizadas:

	Validaciones: Renderiza el HTML mostrando los errores del archivo
	
	Prod_por_cliente: Se ingresa el nombre de el cliente y esto lista los productos que compró.
	
	cli_por_prod: En esta funcion se puede ingresar un producto y mostrará los clientes que lo compraron.
	
	prod_mas_vendido: Lista ascendentemente de los productos más vendidos.
	
	cli_mas_gasto: Lista ascendentemente de los clientes que más gastaron.
	
	index: Index te lleva al inicio.
	
	no_encontrado: Mensaje de error por 404 o 500.
	
	ingresar: Permite loguear un usuario en base a todos los que esten en el archivo de usuario.csv	