# Importamos tkinter para Python 3
import tkinter as tk

# Importamos ttk para utilizar los widgets personalizables y de aspecto nativo
from tkinter import ttk

conversor = 1.609

def kilometroAmilla():
    km = float(kilometro.get())
    millas = km / conversor
    milla.delete(0, tk.END)
    milla.insert(0, f"{millas:.2f}")

def millaAkilometro():
    m = float(milla.get())
    kilometros = m * conversor
    kilometro.delete(0, tk.END)
    kilometro.insert(0, f"{kilometros:.2f}")

# Ventana principal
root = tk.Tk()
root.title("Conversor entre kilómetros y millas con actualización en tiempo real")
root.geometry("400x200")
root.resizable(False, False)

kil = tk.Label(root, text=str("Kilómetros:"))
kil.pack()

frame = ttk.Frame(root, padding=1)
frame.pack(fill="both", expand=True)

kilometro = ttk.Entry(frame, width=10)
kilometro.pack(pady=10)

mil = tk.Label(root, text=str("Millas:"))
mil.pack()

frame = ttk.Frame(root, padding=1)
frame.pack(fill="both", expand=True)


milla = ttk.Entry(frame, width=10)
milla.pack(pady=10)

frame = ttk.Frame(padding=1)
frame.pack(fill="both", expand=True)

# Botones
root = ttk.Frame(frame)
root.pack(pady=5)

boton_conversor = ttk.Button(root, text="Conversor km --> millas", command=kilometroAmilla)
boton_conversor.pack(side="left", padx=5)

boton_conversor = ttk.Button(root, text="Conversor millas --> km", command=millaAkilometro)
boton_conversor.pack(side="left", padx=5)

# La ventana, widgets y eventos no empiezan a ejecutarse hasta que ejecutamos el mainloop() de la ventana principal
root.mainloop() 