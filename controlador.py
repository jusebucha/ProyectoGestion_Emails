from datetime import datetime
import sqlite3
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
