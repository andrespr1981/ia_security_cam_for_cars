import os
import smtplib
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()
from email.mime.image import MIMEImage
import cv2

def send_email(
    destinatario,
    motivo_alerta="Movimiento sospechoso",
    frame=None
):

    remitente = os.getenv('EMAIL')
    password = os.getenv('EMAIL_PASSWORD')

    msg = MIMEMultipart()

    msg['From'] = remitente
    msg['To'] = destinatario
    msg['Subject'] = f"ALERTA DE SEGURIDAD: {motivo_alerta}"

    cuerpo = f"""
    Hola,

    El sistema Driver Guard ha detectado una anomalía:

    Evento: {motivo_alerta}

    Se adjunta una captura del momento detectado.

    Atentamente,
    Driver Guard AI
    """

    msg.attach(MIMEText(cuerpo, 'plain'))

    try:

        if frame is not None:

            image_path = "alert.jpg"

            cv2.imwrite(image_path, frame)

            with open(image_path, 'rb') as img:

                image = MIMEImage(img.read())

                image.add_header(
                    'Content-Disposition',
                    'attachment',
                    filename='alert.jpg'
                )

                msg.attach(image)

        server = smtplib.SMTP('smtp.gmail.com', 587)

        server.starttls()

        server.login(remitente, password)

        server.sendmail(
            remitente,
            destinatario,
            msg.as_string()
        )

        server.quit()

        print("Correo enviado")

        return True

    except Exception as e:

        print(f"Error al enviar el correo: {e}")

        return False