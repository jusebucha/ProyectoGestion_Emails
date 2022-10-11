from email.message import EmailMessage
import smtplib


def enviar_email(email_destino, codigo):
    remitente = "wreano@uninorte.edu.co"
    destinatario = email_destino
    mensaje = "Correo de activación"

    email = EmailMessage()
    email['From'] = remitente
    email['To'] = destinatario
    email['Subject'] = 'Confirmación de Correo'
    email.set_content("Bienvenido, para confirmar su cuenta ingrese el siguiente código. \n código de verificación: " +
                      codigo+" \n Recuerde ingresar este código para poder validar su cuenta")
    # email.set_content(mensaje)
    smtp = smtplib.SMTP("smtp-mail.outlook.com", port=587)
    smtp.starttls()
    smtp.login(remitente, "Wreano92_")
    smtp.sendmail(remitente, destinatario, email.as_string())
    smtp.quit()


def recuperar_email(email_destino):
    remitente = "wreano@uninorte.edu.co"
    destinatario = email_destino
    mensaje="<hr>"
    mensaje = "<h2>Recuperación de cuenta</h2>"
    mensaje = mensaje + "<a href='http://localhost:5000/restablecer/" + email_destino + \
        "'>Ingrese aquí para restablecer su contraseña</a>"
    mensaje=mensaje+ "<hr>"
    email = EmailMessage()
    email['From'] = remitente
    email['To'] = destinatario
    email['Subject'] = 'recuperar contraseña'
    email.set_content(mensaje, subtype="html")
    smtp = smtplib.SMTP("smtp-mail.outlook.com", port=587)
    smtp.starttls()
    smtp.login(remitente, "Wreano92_")
    smtp.sendmail(remitente, destinatario, email.as_string())
    smtp.quit()
