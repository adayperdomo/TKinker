import tkinter as tk
from tkinter import ttk

# --- Funciones ---
def presionar(tecla):
    entrada_texto.set(entrada_texto.get() + str(tecla))

def sumar():
    global operando1
    operando1 = float(entrada_texto.get())
    entrada_texto.set("")  # Limpia la pantalla para el segundo número

def calcular():
    operando2 = float(entrada_texto.get())
    resultado = operando1 + operando2
    entrada_texto.set(str(resultado))

# --- Interfaz ---
root = tk.Tk()
root.title("Calculadora Simple")
root.geometry("313x350")      # Tamaño fijo
root.resizable(False, False)  # Desactiva el cambio de tamaño

frame = tk.Frame(root, bg="lightblue")
frame.pack(expand=True, fill="both")

entrada_texto = tk.StringVar()
pantalla = ttk.Entry(frame, textvariable=entrada_texto, justify="right", font=("Arial", 16))
pantalla.grid(row=0, column=0, columnspan=4, padx=10, pady=10, ipady=8, sticky="we")

# --- Botones numéricos ---
botones = [
    ('7', 1, 0), ('8', 1, 1), ('9', 1, 2),
    ('4', 2, 0), ('5', 2, 1), ('6', 2, 2),
    ('1', 3, 0), ('2', 3, 1), ('3', 3, 2),
    ('0', 4, 0)
]

for (texto, fila, columna) in botones:
    ttk.Button(frame, text=texto, padding=10, command=lambda t=texto: presionar(t)).grid(row=fila, column=columna, padx=5, pady=5)

# --- Botones de operaciones ---
ttk.Button(frame, text="+", padding=10, command=sumar).grid(row=4, column=1, padx=5, pady=5)
ttk.Button(frame, text="=", padding=10, command=calcular).grid(row=4, column=2, padx=5, pady=5)

root.mainloop()
