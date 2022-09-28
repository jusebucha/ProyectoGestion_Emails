from operator import truediv
from pickle import TRUE
from curses import flash
from datetime import datetime
import sqlite3
import envioemail

DB_NAME = 'bdgestion.s3db'


def conectar_db():
    conn = sqlite3.connect(DB_NAME)
    return conn


def insertar_usuarios(nombre, apellido, usuario, passwd):
    cod_ver =  datetime.now()
    cod_ver = cod_ver.replace ("-","")
    flash(str(cod_ver))
    try:
        db = conectar_db()
        cursor = db.cursor()
        sql = "INSERT INTO usuarios(nombre,apellido,usuario,passw,cod_verificacion,verificado,id_rol) VALUES(?,?,?,?,?,?,?)"
        cursor.execute(sql, [nombre, apellido, usuario,
                    passwd, 'MT-0001', False, 1])
        db.commit()
        envioemail.enviar_email(usuario, 'MT0001')
        return True
    except:
        return False
