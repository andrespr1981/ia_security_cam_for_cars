import os
import smtplib
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

def send_email(destinatario, motivo_alerta="Movimiento sospechoso"):
    remitente = os.getenv('EMAIL')
    password =  os.getenv('EMAIL_PASSWORD')
    
    msg = MIMEMultipart()
    msg['From'] = remitente
    msg['To'] = destinatario
    msg['Subject'] = f" ALERTA DE SEGURIDAD: {motivo_alerta}"

    cuerpo = f"""
    Hola,
    
    El sistema Driver Guard ha detectado una anomalía:
    - Evento: {motivo_alerta}
    - Estado: Revisión requerida de inmediato.
    
    Por favor, verifica la aplicación o los archivos guardados.
    
    Atentamente,
    Driver Guard AI.
    """
    
    msg.attach(MIMEText(cuerpo, 'plain'))
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        
        server.login(remitente, password)
        server.sendmail(remitente, destinatario, msg.as_string())
        server.quit()
        return
    except Exception as e:
        print(f"Error al enviar el correo: {e}")
        return False