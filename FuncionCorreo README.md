# Se debe guardar en un archivo separado dentro de la carpeta utils o al principio del main.py.
# ¿Dónde mandar a llamar esta función?
Dentro del bucle principal del código (video_loop en el main.py), donde el modelo de Inteligencia 
Artificial cambia el estado o activa la alarma al reconocer un rostro desconocido o una distracción,
añadiendo  la línea:

# Ejemplo de uso cuando la IA detecta algo:
if alerta_detectada:
    enviar_alerta_correo("correo_del_usuario@gmail.com", "Se detectó un conductor no autorizado")
