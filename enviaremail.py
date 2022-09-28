from email.message import EmailMessage
import smtplib

def enviar_email(email_destino,codigo):
    remitente = "vaccar@uninorte.edu.co"
    destinatario = email_destino
    mensaje = "¡Hola, mundo!"
    email = EmailMessage()
    email["From"] = remitente
    email["To"] = destinatario
    email["Subject"] = "Correo de prueba"
    email.set_content(mensaje)
    smtp = smtplib.SMTP("smtp-mail.outlook.com", port=587)
    smtp.starttls()
    smtp.login(remitente, "")
    smtp.sendmail(remitente, destinatario, email.as_string())
    smtp.quit()