import tkinter as tk
from tkinter import ttk, messagebox

# -------------------------
# Función para abrir ventanas secundarias
# -------------------------
def abrir_ventana(tipo):
    ventana = tk.Toplevel(root)
    ventana.title(f"Conversor de {tipo}")
    ventana.geometry("400x300")
    ventana.resizable(False, False)

    ttk.Label(ventana, text=f"Conversor de {tipo}", font=("Arial", 14, "bold")).pack(pady=10)

    ttk.Label(ventana, text="Valor a convertir:").pack(pady=5)
    valor_var = tk.StringVar()
    ttk.Entry(ventana, textvariable=valor_var, width=20).pack()

    ttk.Label(ventana, text="De:").pack(pady=5)
    unidad_origen = ttk.Combobox(ventana, state="readonly")
    unidad_origen.pack()

    ttk.Label(ventana, text="A:").pack(pady=5)
    unidad_destino = ttk.Combobox(ventana, state="readonly")
    unidad_destino.pack()

    resultado_label = ttk.Label(ventana, text="", font=("Arial", 12))
    resultado_label.pack(pady=10)

    # --- Conversión según categoría ---
    if tipo == "Moneda":
        unidades = ["Euro", "Dólar", "Libra"]
        tasas = {"Euro": 1.0, "Dólar": 1.1, "Libra": 0.86}  # valores aproximados

        def convertir():
            try:
                valor = float(valor_var.get())
                de = unidad_origen.get()
                a = unidad_destino.get()
                if not de or not a:
                    messagebox.showwarning("Aviso", "Selecciona ambas unidades.")
                    return
                resultado = valor * (tasas[a] / tasas[de])
                resultado_label.config(text=f"{valor:.2f} {de} = {resultado:.2f} {a}")
            except ValueError:
                messagebox.showerror("Error", "Introduce un número válido.")

    elif tipo == "Longitud":
        unidades = ["Milímetro", "Centímetro", "Metro", "Kilómetro", "Pulgada", "Yarda", "Milla"]
        # todos en relación al metro
        factores = {
            "Milímetro": 0.001,
            "Centímetro": 0.01,
            "Metro": 1,
            "Kilómetro": 1000,
            "Pulgada": 0.0254,
            "Yarda": 0.9144,
            "Milla": 1609.34
        }

        def convertir():
            try:
                valor = float(valor_var.get())
                de = unidad_origen.get()
                a = unidad_destino.get()
                if not de or not a:
                    messagebox.showwarning("Aviso", "Selecciona ambas unidades.")
                    return
                metros = valor * factores[de]
                resultado = metros / factores[a]
                resultado_label.config(text=f"{valor:.2f} {de} = {resultado:.4f} {a}")
            except ValueError:
                messagebox.showerror("Error", "Introduce un número válido.")

    elif tipo == "Temperatura":
        unidades = ["Celsius", "Fahrenheit", "Kelvin"]

        def convertir():
            try:
                valor = float(valor_var.get())
                de = unidad_origen.get()
                a = unidad_destino.get()
                if not de or not a:
                    messagebox.showwarning("Aviso", "Selecciona ambas unidades.")
                    return

                # Convertimos a Celsius primero
                if de == "Celsius":
                    c = valor
                elif de == "Fahrenheit":
                    c = (valor - 32) * 5/9
                elif de == "Kelvin":
                    c = valor - 273.15

                # De Celsius a destino
                if a == "Celsius":
                    resultado = c
                elif a == "Fahrenheit":
                    resultado = c * 9/5 + 32
                elif a == "Kelvin":
                    resultado = c + 273.15

                resultado_label.config(text=f"{valor:.2f} {de} = {resultado:.2f} {a}")

            except ValueError:
                messagebox.showerror("Error", "Introduce un número válido.")

    # Cargar unidades
    unidad_origen["values"] = unidades
    unidad_destino["values"] = unidades

    ttk.Button(ventana, text="Convertir", command=convertir).pack(pady=10)

# -------------------------
# Ventana principal
# -------------------------
root = tk.Tk()
root.title("Conversor de Unidades")
root.geometry("400x300")
root.resizable(False, False)

ttk.Label(root, text="Conversor de Unidades", font=("Arial", 16, "bold")).pack(pady=20)
ttk.Label(root, text="Selecciona una categoría:", font=("Arial", 12)).pack(pady=10)

# Botones para abrir ventanas secundarias
ttk.Button(root, text="Unidades Monetarias", command=lambda: abrir_ventana("Moneda")).pack(pady=5)
ttk.Button(root, text="Unidades de Longitud", command=lambda: abrir_ventana("Longitud")).pack(pady=5)
ttk.Button(root, text="Unidades de Temperatura", command=lambda: abrir_ventana("Temperatura")).pack(pady=5)

root.mainloop()
