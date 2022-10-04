
from datetime import datetime
import re
from tkinter.messagebox import RETRY
from xml.dom.minidom import ReadOnlySequentialNamedNodeMap
from flask import Flask, jsonify, render_template, url_for, request, redirect, flash, session
import controlador
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)

app.secret_key = 'mi clave de secreta'+str(datetime.now)


#########Recuperar la informacion desde los formularios#####
###Recuperar y Almancenar los Registros de usuario######################

@app.route('/listamensindv', methods=['GET', 'POST'])
def listar_mens_ind():
    if request.method == 'POST':
        datos = request.get_json()
        username = datos['username']
        tipo = datos['tipo']
        if tipo == 1:
            resultado = controlador.listar_mensajes(1, '')
        else:
            resultado = controlador.listar_mensajes(2, username)
        return jsonify(resultado)
    else:
        resultado = controlador.listar_mensajes(1, '')
        return jsonify(resultado)


@app.route('/listarmensajes')
def listar_mensajes():
    resultado = controlador.listar_mensajes(1, '')
    return jsonify(resultado)


@app.route('/listarusuarios')
def lista_gral_usuarios():
    resultado = controlador.lista_gral_usuarios()
    return jsonify(resultado)


@app.route('/activar', methods=['POST'])
def activar_cuenta():
    datos = request.form
    username = datos['username']
    codver = datos['codverificacion']
    resultado = controlador.activar_usuario(username, codver)
    if resultado:
        flash('Cuenta activada satisfactoriamente')
    else:
        flash('Error en activación')

    return redirect(url_for('verificar'))


@app.route('/validarlogin', methods=['POST'])
def val_user():
    datos = request.form
    username = datos['username']
    passwd = datos['password']
<<<<<<< HEAD
    if username =='' or passwd =='':
        flash('datos incompletos')
        return redirect(url_for('login1'))
=======
    if username == '' or passwd == '':
        flash('Datos Incompletos')
>>>>>>> FranciscoOP
    else:
        resultado = controlador.validar_usuarios(username)
        if resultado == False:
            flash('error al ingresar')
            return redirect(url_for('login1'))
        else:
            print('Resultado: ' + str(resultado[0]['verificado']))
            if (resultado[0]['verificado'] == 1):

                if check_password_hash(resultado[0]['passwd'], passwd):
                    session['username'] = username
                    session['nombre'] = resultado[0]['nombre'] + \
                        " "+resultado[0]['apellido']
                    listadouser = controlador.listar_usuarios(username)
                    print(listadouser)
                    return render_template('mensajeria.html', datauser=listadouser)
                else:
                    flash('Contraseña Invalida')
                    return redirect(url_for('login1'))
            else:
                return redirect(url_for('verificar'))


@app.route('/enviarmensajes', methods=['POST'])
def enviar_mesanjes():
    datos = request.form
    remitente = session['username']
    asunto = datos['asunto']
    destinatario = datos['destinatario']
    cuerpo = datos['cuerpo']
    resultado = controlador.insertar_mensajes(
        remitente, destinatario, asunto, cuerpo)
    if resultado:
        flash('Mensaje Enviado Correctamente')

    else:
        flash('Error en el Envio')

    listadouser = controlador.listar_usuarios(remitente)
    return render_template('mensajeria.html', datauser=listadouser)


@app.route('/addregistro', methods=['POST'])
def add_registro():
    datos = request.form
    nom = datos['nombre']
    ape = datos['apellido']
    usu = datos['email']
    p1 = datos['pass1']
    p2 = datos['pass2']
    p1enc = generate_password_hash(p1)
    if nom == '' and ape == '' and usu == '' and p1 == '' and p2 == '':
        flash("Datos Imcompletos")
    elif p1 != p2:
        flash("Las Contraseñas no Coinciden")
    elif len(p1) < 8:
        flash('Contraseña no cumple tamaño minimo')
    else:
        resultado = controlador.insertar_usuarios(nom, ape, usu, p1enc)
        if resultado:
            flash('Informacion Almacenada')
        else:
            flash('Error en Almacenamiento')

    #flash(nom + ' ' + ape +' ' + usu +' ' + ' ' + foto + ' ' + passw)
    return redirect(url_for('registro'))
    # validacion de los registros
    # if nom !='':
    #    return '<h3>'+nom + ' ' + ape +' ' + usu +' ' + ' ' + foto + ' ' + passw + '</h3>'
    # else:
    #    return '<h1>No Ingreso el Nombre<h1>'


# Formularios de Usuarios


@app.route('/addusuario', methods=['POST'])
def add_usuario():
    datos = request.form
    nombre = datos['nombre']
    apellido = datos['apellido']
    usuario = datos['email']
    rol = datos['rol']
    foto = datos['foto']
    passw = datos['password']
    print(nombre)
    print(apellido)
    print(usuario)
    print(rol)
    print(foto)
    print(passw)

    return redirect(url_for('menu_user'))

# Recuperar desde el Formulario Materias


@app.route('/addmateria', methods=['POST'])
def add_materia():
    datos = request.form
    codigomat = datos['codigomat']
    nombremat = datos['nombremat']

    return redirect(url_for('menu_materias'))


#####################Rutas de Navegacion#######################################
@app.route('/')
def index():
    return render_template('login1.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/login1')
def login1():
    return render_template('login1.html')


@app.route('/registro')
def registro():
    return render_template('registro.html')


@app.route('/verificacion')
def verificar():
    return render_template('verificacion.html')


@app.route('/mensajeria')
def mensajeria():
    return render_template('mensajeria.html')


@app.route('/mensajes')
def mensajes():
    return render_template('mensajes.html')

@app.route('/clave')
def recordar_clave():
    return render_template('clave.html')

# @app.route('/menu')
# @app.route('/menu/<username>/')
# def menu(username):
#    return render_template('menu.html',usuvista=username)

# Detectar los metodos de envio desde el formulario de login

# @app.route('/menu', methods=['GET','POST'])
# def menu():
#    if request.method=='POST':
#        return render_template('menu.html')
#    else:
#       return '<h1>Metodo GET</h1>'


@app.route('/menu')
def menu():
    return render_template('menu.html')


@app.route('/usuarios')
def menu_user():
    return render_template('usuarios.html')


@app.route('/materias')
def menu_materias():
    return render_template('materias.html')


@app.route('/cursos')
def menu_cursos():
    return render_template('cursos.html')


@app.route('/matriculas')
def menu_matriculas():
    return render_template('matriculas.html')


@app.route('/actividades')
def menu_actividades():
    return render_template('actividades.html')


@app.route('/calificaciones')
def menu_calificaciones():
    return render_template('calificaciones.html')


if __name__ == '__main__':
    app.run(debug=True)
