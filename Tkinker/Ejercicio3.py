# Importamos tkinter para Python 3
import tkinter as tk
from tkinter import ttk

def añadir():
    tarea = entrada_tarea.get().strip()
    if tarea:
        lista_tareas.insert(tk.END, tarea)
        entrada_tarea.delete(0, tk.END)

def eliminar():
    seleccion = lista_tareas.curselection()
    for i in seleccion[::-1]:  # Eliminamos en orden inverso para no alterar índices
        lista_tareas.delete(i)

# Ventana principal
root = tk.Tk()
root.title("Lista de Tareas")
root.geometry("400x400")
root.resizable(False, False)

# Frame principal
frame = ttk.Frame(root, padding=10)
frame.pack(fill="both", expand=True)

# Entrada de texto
entrada_tarea = ttk.Entry(frame, width=40)
entrada_tarea.pack(pady=10)

# Botones
botones_frame = ttk.Frame(frame)
botones_frame.pack(pady=5)

boton_añadir = ttk.Button(botones_frame, text="Añadir", command=añadir)
boton_añadir.pack(side="left", padx=5)

boton_eliminar = ttk.Button(botones_frame, text="Eliminar", command=eliminar)
boton_eliminar.pack(side="left", padx=5)

# Lista de tareas
lista_tareas = tk.Listbox(frame, height=15, width=50)
lista_tareas.pack(pady=10)

# Iniciar la interfaz
root.mainloop()
