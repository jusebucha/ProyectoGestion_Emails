from dataclasses import replace
from datetime import datetime
from re import M
import sqlite3

from flask import flash
import envioemail

DB_NAME = 'bdgestion.s3db'


def conectar_db():
    conn = sqlite3.connect(DB_NAME)
    return conn


def insertar_usuarios(nombre, apellido, usuario, passwd):
    cod_ver = str(datetime.now())
    cod_ver = cod_ver.replace("-", "")
    cod_ver = cod_ver.replace(" ", "")
    cod_ver = cod_ver.replace(":", "")
    cod_ver = cod_ver.replace(".", "")

    # flash(cod_ver)
    try:
        db = conectar_db()
        cursor = db.cursor()
        sql = "INSERT INTO usuarios(nombre,apellido,usuario,passw,cod_verificacion,verificado,id_rol) values(?,?,?,?,?,?,?)"
        cursor.execute(sql, [nombre, apellido, usuario,
                            passwd, cod_ver, 0, 1])
        db.commit()
        envioemail.enviar_email(usuario, cod_ver)
        return True
    except:
        return False


def validar_usuarios(username):

    try:
        db = conectar_db()
        cursor = db.cursor()
        sql = "SELECT * FROM usuarios WHERE usuario=?"
        cursor.execute(sql, [username])
        resultado = cursor.fetchone()
        usuario = [{
            'id': resultado[0],
            'nombre':resultado[1],
            'apellido':resultado[2],
            'usuario':resultado[3],
            'passwd':resultado[4],
            'codver':resultado[5],
            'verificado':resultado[6],
            'rol':resultado[7]
        }]
        return usuario
    except:
        return False


def activar_usuario(username, codver):
    try:
        db = conectar_db()
        cursor = db.cursor()
        sql = "update usuarios set verificado=1 where usuario=? and cod_verificacion =?"
        cursor.execute(sql, [username, codver])
        db.commit()
        return True
    except:
        return False


def listar_mensajes(tipo, username):
    listamensajeria = []

    try:
        db = conectar_db()
        cursor = db.cursor()
        sql = "SELECT * FROM mensajeria"
        if tipo == 1:
            cursor.execute(sql)
        else:
            sql = "SELECT * FROM mensajeria WHERE remitente=? or destinatario=?"
            cursor.execute(sql, [username, username])
        resultado = cursor.fetchall()

        for m in resultado:
            tipo = ''
            if m[1] == username:
                tipo = 'Mensaje Enviado'
            else:
                tipo = 'Mensaje Recibido'
            registro = {
                'id': m[0],
                'remitente': m[1],
                'destinatario': m[2],
                'asunto': m[3],
                'cuerpo': m[4],
                'fecha_consulta': datetime.now(),
                'Tipo': tipo
            }
            listamensajeria.append(registro)
    except:
        registro = {
            'resultado': 'No Existen Mensajes'}
        listamensajeria.append(registro)
    return listamensajeria


def lista_gral_usuarios():
    listagralusuarios = []
    try:
        db = conectar_db()
        cursor = db.cursor()
        sql = "SELECT * FROM usuarios"
        cursor.execute(sql)
        resultado = cursor.fetchall()
        i = 1
        for m in resultado:
            registro = {
                'id_reg': i,
                'id': m[0],
                'nombre': m[1],
                'apellido': m[2],
                'usuario': m[3],
                'id_rol': m[7],
                'fecha_consulta': datetime.now()
            }
            listagralusuarios.append(registro)
            i += 1
    except:
        registro = {
            'resultado': 'No Existen usuarios'}
        listagralusuarios.append(registro)
    return listagralusuarios


def listar_usuarios(username):
    try:
        db = conectar_db()
        cursor = db.cursor()
        sql = "SELECT * FROM usuarios WHERE usuario !=?"
        cursor.execute(sql, [username])
        resultado = cursor.fetchall()
        usuarios = []
        for u in resultado:
            registro = {
                'id': u[0],
                'nombre': u[1],
                'apellido': u[2],
                'usuario': u[3]
            }
            usuarios.append(registro)

        return usuarios
    except:
        return False


def insertar_mensajes(rem, dest, asunto, cuerpo):

    try:
        db = conectar_db()
        cursor = db.cursor()
        sql = "INSERT INTO mensajeria(remitente,destinatario,asunto,mensaje) VALUES(?,?,?,?)"
        cursor.execute(sql, [rem, dest, asunto, cuerpo])
        db.commit()

        return True
    except:
        return False
