import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk

# Ventana principal
root = tk.Tk()
root.title("Gestión de Productos")
root.geometry("600x500")
root.resizable(False, False)

# Lista de productos (cada uno será un diccionario)
productos = []

# Variables
nombre_var = tk.StringVar()
precio_var = tk.StringVar()
imagen_path = None

# Función para seleccionar imagen
def seleccionar_imagen():
    global imagen_path
    ruta = filedialog.askopenfilename(
        title="Seleccionar imagen",
        filetypes=[("Archivos de imagen", "*.jpg *.jpeg *.png *.gif")]
    )
    if ruta:
        imagen_path = ruta
        img = Image.open(ruta)
        img = img.resize((100, 100))
        foto = ImageTk.PhotoImage(img)
        imagen_label.config(image=foto)
        imagen_label.image = foto

# Función para crear producto
def crear_producto():
    global imagen_path
    nombre = nombre_var.get().strip()
    precio = precio_var.get().strip()

    if not nombre or not precio or not imagen_path:
        messagebox.showwarning("Campos vacíos", "Debes completar todos los campos y seleccionar una imagen.")
        return

    try:
        precio_float = float(precio)
    except ValueError:
        messagebox.showerror("Error", "El precio debe ser un número.")
        return

    producto = {"nombre": nombre, "precio": precio_float, "imagen": imagen_path}
    productos.append(producto)

    actualizar_lista()
    limpiar_campos()

# Función para actualizar lista visual
def actualizar_lista():
    lista_productos.delete(0, tk.END)
    for p in productos:
        lista_productos.insert(tk.END, f"{p['nombre']} - ${p['precio']:.2f}")

# Función para mostrar producto seleccionado
def leer_producto():
    seleccion = lista_productos.curselection()
    if not seleccion:
        return

    indice = seleccion[0]
    producto = productos[indice]
    nombre_var.set(producto["nombre"])
    precio_var.set(str(producto["precio"]))

    img = Image.open(producto["imagen"])
    img = img.resize((100, 100))
    foto = ImageTk.PhotoImage(img)
    imagen_label.config(image=foto)
    imagen_label.image = foto

# Función para actualizar producto
def actualizar_producto():
    seleccion = lista_productos.curselection()
    if not seleccion:
        return

    indice = seleccion[0]
    nombre = nombre_var.get().strip()
    precio = precio_var.get().strip()

    if not nombre or not precio:
        messagebox.showwarning("Campos vacíos", "Completa todos los campos.")
        return

    try:
        precio_float = float(precio)
    except ValueError:
        messagebox.showerror("Error", "El precio debe ser un número.")
        return

    productos[indice]["nombre"] = nombre
    productos[indice]["precio"] = precio_float
    if imagen_path:
        productos[indice]["imagen"] = imagen_path

    actualizar_lista()
    limpiar_campos()

# Función para eliminar producto
def eliminar_producto():
    seleccion = lista_productos.curselection()
    if not seleccion:
        return
    indice = seleccion[0]
    del productos[indice]
    actualizar_lista()
    limpiar_campos()

# Función para limpiar campos
def limpiar_campos():
    global imagen_path
    nombre_var.set("")
    precio_var.set("")
    imagen_label.config(image="")
    imagen_label.image = None
    imagen_path = None

frame_inputs = ttk.Frame(root, padding=10)
frame_inputs.pack()

ttk.Label(frame_inputs, text="Nombre:").grid(row=0, column=0, sticky="w")
entry_nombre = ttk.Entry(frame_inputs, textvariable=nombre_var, width=40)
entry_nombre.grid(row=0, column=1, padx=5)

ttk.Label(frame_inputs, text="Precio:").grid(row=1, column=0, sticky="w")
entry_precio = ttk.Entry(frame_inputs, textvariable=precio_var, width=40)
entry_precio.grid(row=1, column=1, padx=5)

boton_imagen = ttk.Button(frame_inputs, text="Seleccionar imagen", command=seleccionar_imagen)
boton_imagen.grid(row=2, column=0, columnspan=2, pady=5)

imagen_label = ttk.Label(frame_inputs)
imagen_label.grid(row=3, column=0, columnspan=2, pady=5)

frame_botones = ttk.Frame(root, padding=5)
frame_botones.pack()

ttk.Button(frame_botones, text="Crear", command=crear_producto).grid(row=0, column=0, padx=5)
ttk.Button(frame_botones, text="Leer", command=leer_producto).grid(row=0, column=1, padx=5)
ttk.Button(frame_botones, text="Actualizar", command=actualizar_producto).grid(row=0, column=2, padx=5)
ttk.Button(frame_botones, text="Eliminar", command=eliminar_producto).grid(row=0, column=3, padx=5)

frame_lista = ttk.Frame(root, padding=10)
frame_lista.pack(fill="both", expand=True)

lista_productos = tk.Listbox(frame_lista, height=10, width=60)
lista_productos.pack(pady=10)

root.mainloop()
