# Importamos tkinter para Python 3
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# Ventana principal
root = tk.Tk()
root.title("Visor de imágenes")
root.geometry("500x400")
root.resizable(False, False)

# Lista de rutas de imágenes (ajusta las rutas según tus archivos locales)
imagenes = [
    r"C:\Users\Alumno.MEDUSAMAQ\Documents\DAD\imagen\dios.jpg",
    r"C:\Users\Alumno.MEDUSAMAQ\Documents\DAD\imagen\Horario.png",
    r"C:\Users\Alumno.MEDUSAMAQ\Documents\DAD\imagen\si.png"
]


# Índice actual
indice = 0

# Cargar imagen inicial
def mostrar_imagen():
    global img_label, img
    imagen = Image.open(imagenes[indice])
    imagen = imagen.resize((400, 300))  # Redimensionar para ajustar al visor
    img = ImageTk.PhotoImage(imagen)
    img_label.config(image=img)

# Función para ir a la siguiente imagen
def siguiente():
    global indice
    if indice < len(imagenes) - 1:
        indice += 1
    else:
        indice = 0  # vuelve al inicio
    mostrar_imagen()

# Función para ir a la imagen anterior
def anterior():
    global indice
    if indice > 0:
        indice -= 1
    else:
        indice = len(imagenes) - 1  # va al final
    mostrar_imagen()

# Etiqueta para mostrar la imagen
img_label = ttk.Label(root)
img_label.pack(pady=10)

# Botones
frame_botones = ttk.Frame(root)
frame_botones.pack()

boton_anterior = ttk.Button(frame_botones, text="<", command=anterior)
boton_anterior.grid(row=0, column=0, padx=10)

boton_siguiente = ttk.Button(frame_botones, text=">", command=siguiente)
boton_siguiente.grid(row=0, column=1, padx=10)

# Mostrar primera imagen
mostrar_imagen()

# Iniciar aplicación
root.mainloop()
