# Importamos tkinter para Python 3
import tkinter as tk
# Importamos ttk para utilizar los widgets personalizables y de aspecto nativo
from tkinter import ttk

contador = 0

def incrementar():
    global contador
    contador += 1
    numero.config(text=str(contador))

def decrementar():
    global contador
    contador -= 1 
    numero.config(text=str(contador))

root = tk.Tk()
root.geometry('200x200')

numero = tk.Label(root, text=str(contador))
numero.pack()

boton_incrementar = ttk.Button(root, text="INCREMENTAR", command = incrementar)
boton_incrementar.pack(side="left", expand=True)

boton_decrementar = ttk.Button(root, text="DECREMENTAR", command = decrementar)
boton_decrementar.pack(side="left", expand=True) 


# La ventana, widgets y eventos no empiezan a ejecutarse hasta que ejecutamos el mainloop() de la ventana principal
root.mainloop()