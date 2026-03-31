import tkinter as tk
from tkinter import ttk
from datetime import datetime
import cv2
from PIL import Image, ImageTk  

cap = cv2.VideoCapture(0)

def agregar_notificacion(mensaje):
    fecha = datetime.now().strftime("%H:%M:%S")
    tabla.insert("", 0, values=(fecha, mensaje)) 

def simular_alerta():
    mensaje = "Persona sospechosa detectada"
    etiqueta_estado.config(text="⚠️ " + mensaje, fg="#ff5555")
    agregar_notificacion(mensaje)

def actualizar_video():
    """Función para capturar frames y mostrarlos en la interfaz"""
    ret, frame = cap.read()
    if ret:
        frame = cv2.resize(frame, (400, 250))
        
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        
        lbl_video.imgtk = imgtk
        lbl_video.configure(image=imgtk)
    
    lbl_video.after(10, actualizar_video)

ventana = tk.Tk()
ventana.title("Sistema de Alarma Inteligente")
ventana.geometry("1000x650")
ventana.configure(bg="#1e1e2f")

menu = tk.Frame(ventana, bg="#2c2c3e", width=200)
menu.pack(side="left", fill="y")

tk.Label(menu, text=" Alarma Inteligente", bg="#2c2c3e", fg="white", font=("Arial", 12, "bold")).pack(pady=20)

botones = ["Inicio", "Cámara", "Alertas", "Historial"]
for b in botones:
    tk.Button(menu, text=b, bg="#3a3a5a", fg="white", width=20, bd=0, pady=10).pack(pady=5)

principal = tk.Frame(ventana, bg="#1e1e2f")
principal.pack(side="right", expand=True, fill="both")

frame_camara = tk.LabelFrame(principal, text="Cámara en Vivo", bg="#1e1e2f", fg="white", font=("Arial", 10, "bold"))
frame_camara.pack(fill="x", padx=20, pady=10)

lbl_video = tk.Label(frame_camara, bg="black")
lbl_video.pack(pady=10)

etiqueta_estado = tk.Label(frame_camara, text="Estado: Sistema Vigilando", bg="#1e1e2f", fg="#55ff55", font=("Arial", 10))
etiqueta_estado.pack()

tk.Button(frame_camara, text="Simular detección", command=simular_alerta, bg="#44475a", fg="white").pack(pady=10)

frame_tabla = tk.LabelFrame(principal, text="Registro de Notificaciones", bg="#1e1e2f", fg="white", font=("Arial", 10, "bold"))
frame_tabla.pack(fill="both", expand=True, padx=20, pady=10)

columnas = ("Fecha y Hora", "Notificación")
tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings")

for col in columnas:
    tabla.heading(col, text=col)
    tabla.column(col, anchor="center")

style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview", background="#2c2c3e", foreground="white", fieldbackground="#2c2c3e", borderwidth=0)
style.map("Treeview", background=[('selected', '#44475a')])

tabla.pack(fill="both", expand=True)

actualizar_video() 

def al_cerrar():
    cap.release()
    ventana.destroy()

ventana.protocol("WM_DELETE_WINDOW", al_cerrar)
ventana.mainloop()