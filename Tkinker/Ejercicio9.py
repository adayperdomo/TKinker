import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os, random

# --- Diccionario de hiragana ---
hiragana_dict = {
    "a": "lluvia", "chi": "padre", "e": "estacion", "fu": "barco",
    "ha": "flor", "he": "habitacion", "hi": "fuego", "ho": "estrella",
    "i": "perro", "ma": "ventana", "me": "ojo", "mi": "agua",
    "mo": "bosque", "mu": "insecto", "n": "gato", "na": "verano",
    "ne": "gato", "ni": "japon", "no": "posesion", "nu": "tela",
    "o": "montaña", "ra": "radio", "re": "entrenar", "ri": "pez",
    "ro": "corredor", "ru": "pelo", "sa": "pequeño", "se": "mundo",
    "shi": "ciudad", "so": "cielo", "su": "nido", "ta": "arrozal",
    "te": "mano", "to": "puerta", "tsu": "puerto", "u": "conejo",
    "wa": "anillo", "wo": "objeto", "ya": "montaña", "yo": "noche",
    "yu": "nieve"
}

# --- Carpeta de imágenes ---
CARPETA_IMAGENES = r"C:\Users\Alumno.MEDUSAMAQ\Documents\DAD\hiragana"  # cambia esta ruta

# --- Cargar todas las imágenes del directorio ---
def cargar_imagenes():
    disponibles = []
    for archivo in os.listdir(CARPETA_IMAGENES):
        if archivo.lower().endswith((".jpg", ".png", ".jpeg", ".gif")):
            nombre = os.path.splitext(archivo)[0].lower()
            disponibles.append((archivo, nombre))
    return disponibles

# --- Elegir 10 imágenes aleatorias sin repetición ---
imagenes_disponibles = cargar_imagenes()
imagenes_juego = random.sample(imagenes_disponibles, 10)

# --- Variables de control ---
indice_actual = 0
aciertos = 0

# --- Ventana principal ---
root = tk.Tk()
root.title("Aprende Hiragana 🇯🇵")
root.geometry("600x500")
root.resizable(False, False)
root.configure(bg="#f0f0f5")

# --- Frames principales ---
frame_img = ttk.Frame(root, padding=10)
frame_img.pack(pady=20)

frame_input = ttk.Frame(root, padding=10)
frame_input.pack(pady=10)

frame_info = ttk.Frame(root, padding=10)
frame_info.pack(pady=10)

# --- Widgets globales ---
imagen_label = ttk.Label(frame_img)
imagen_label.pack()

respuesta_var = tk.StringVar()
entry_respuesta = ttk.Entry(frame_input, textvariable=respuesta_var, width=30)
entry_respuesta.pack(side="left", padx=5)

boton_comprobar = ttk.Button(frame_input, text="Comprobar", command=lambda: comprobar_respuesta())
boton_comprobar.pack(side="left", padx=5)

resultado_label = ttk.Label(frame_info, text="")
resultado_label.pack(pady=5)

progreso_label = ttk.Label(frame_info, text="")
progreso_label.pack()

# --- Función para mostrar imagen ---
def mostrar_imagen():
    global indice_actual
    archivo, nombre = imagenes_juego[indice_actual]
    ruta = os.path.join(CARPETA_IMAGENES, archivo)

    img = Image.open(ruta)
    img = img.resize((250, 250))
    foto = ImageTk.PhotoImage(img)

    imagen_label.config(image=foto)
    imagen_label.image = foto
    progreso_label.config(text=f"Imagen {indice_actual+1} de 10")
    resultado_label.config(text="")
    respuesta_var.set("")

# --- Función para comprobar respuesta ---
def comprobar_respuesta():
    global indice_actual, aciertos
    respuesta = respuesta_var.get().strip().lower()
    _, nombre = imagenes_juego[indice_actual]

    if respuesta == nombre:
        aciertos += 1
        resultado_label.config(text="Correcto")
    else:
        resultado_label.config(text=f"Incorrecto. Era: {nombre}")

    indice_actual += 1
    root.after(1000, siguiente_imagen)

# --- Siguiente imagen ---
def siguiente_imagen():
    if indice_actual < len(imagenes_juego):
        mostrar_imagen()
    else:
        mostrar_resultado_final()

# --- Mostrar resultado final ---
def mostrar_resultado_final():
    for widget in root.winfo_children():
        widget.destroy()

    nota = aciertos
    if nota < 5:
        calificacion = "Suspenso"
    elif nota == 5:
        calificacion = "Suficiente"
    elif nota == 6:
        calificacion = "Bien"
    elif nota == 7 or nota == 8:
        calificacion = "Notable"
    else:
        calificacion = "Sobresaliente"

    frame_final = ttk.Frame(root, padding=20)
    frame_final.pack(expand=True)

    ttk.Label(frame_final, text="RESULTADO FINAL").pack(pady=10)
    ttk.Label(frame_final, text=f"Aciertos: {aciertos}/10").pack(pady=10)
    ttk.Label(frame_final, text=f"Calificación: {calificacion}").pack(pady=10)

# --- Iniciar juego ---
mostrar_imagen()
root.mainloop()
