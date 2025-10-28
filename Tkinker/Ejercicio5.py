# Importamos tkinter para Python 3
import tkinter as tk
# Importamos ttk para utilizar los widgets personalizables y de aspecto nativo
from tkinter import ttk

root = tk.Tk()
root.title("Sistema CRUD")
root.geometry("500x400")
root.resizable(False, False)

def crear():
    tarea = escribir.get().strip()
    if tarea:
        lista_tareas.insert(tk.END, tarea)
        escribir.delete(0, tk.END)

def leer():
    seleccion = lista_tareas.curselection()
    if seleccion:
        tarea = lista_tareas.get(seleccion)
        escribir.delete(0, tk.END)
        escribir.insert(0, tarea)
        
def actualizar():
    seleccion = lista_tareas.curselection()
    if seleccion:
        tarea = escribir.get().strip()
        if tarea:
            lista_tareas.delete(seleccion)
            lista_tareas.insert(seleccion, tarea)
            escribir.delete(0, tk.END)

def eliminar():
    seleccion = lista_tareas.curselection()
    for i in seleccion[::-1]:  # Eliminamos en orden inverso para no alterar índices
        lista_tareas.delete(i)

frame = ttk.Frame(root, padding=1)
frame.pack(fill="both", expand=True)

escribir = ttk.Entry(frame, width=50)
escribir.pack(pady=10, padx=10)

boton_crear = ttk.Button(root, text="Crear", command=crear)
boton_crear.pack(padx=1, expand=True)

boton_leer = ttk.Button(root, text="Leer", command=leer)
boton_leer.pack(padx=1, expand=True)

boton_actualizar = ttk.Button(root, text="Actualizar", command=actualizar)
boton_actualizar.pack(padx=1, expand=True)

boton_eliminar = ttk.Button(root, text="Eliminar", command=eliminar)
boton_eliminar.pack(padx=1, expand=True)

frame = ttk.Frame(padding=1)
frame.pack(fill="both", expand=True)

lista_tareas = tk.Listbox(frame, height=15, width=50)
lista_tareas.pack(pady=10)

# La ventana, widgets y eventos no empiezan a ejecutarse hasta que ejecutamos el mainloop() de la ventana principal
root.mainloop()