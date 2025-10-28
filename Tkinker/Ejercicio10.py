import tkinter as tk
from tkinter import messagebox
import random
import time
import os
from PIL import Image, ImageTk

# --- CONFIGURACIÓN GLOBAL (RUTAS ABSOLUTAS DEL USUARIO) ---
FILAS, COLUMNAS = 4, 3  # Tablero de 4x3 con 10 cartas (2 espacios vacíos)
PARES_TOTALES = 5
# Directorio donde se encuentran img1.png, img2.png, etc.
RUTA_IMAGENES = r"C:\Users\Alumno\Documents\DAD\Tkinter\Memorizar" 
# Ruta completa para la imagen del reverso (Baraja.png). Usada directamente.
IMAGEN_REVERSO_PATH = r"C:\Users\Alumno\Documents\DAD\Tkinter\Memorizar\Baraja.png" 
TIEMPO_REVELADO = 1000  # 1000 ms (1 segundo) antes de voltear

# Definición de las dimensiones fijas del tablero para estabilidad
ANCHO_CARTA = 100
ALTO_CARTA = 100
PADDING = 10 # 5px en x y 5px en y = 10px total por celda

ANCHO_TABLERO = (ANCHO_CARTA + PADDING) * COLUMNAS
ALTO_TABLERO = (ALTO_CARTA + PADDING) * FILAS
ANCHO_VENTANA = ANCHO_TABLERO + 50 # Un poco más ancho
ALTO_VENTANA = ALTO_TABLERO + 200 # Espacio para encabezado y botones

class JuegoMemoria:
    def __init__(self, master):
        self.master = master
        master.title("Juego de Concentración (Memory)")
        
        # Bloquear y fijar el tamaño de la ventana ---
        # Usamos las dimensiones calculadas para mayor precisión
        master.geometry(f"{ANCHO_VENTANA}x{ALTO_VENTANA}") 
        master.resizable(False, False) # Evita que se cambie el tamaño de la ventana
        
        # Estilo para la aplicación
        master.configure(bg="#e0f7fa")

        # --- Variables de Estado del Juego ---
        self.cartas_visibles = []  # Almacena las 2 cartas volteadas en el turno (fila, columna)
        self.bloqueo_input = False  # Para evitar clics mientras se comprueba la pareja
        self.intentos = 0
        self.pares_encontrados = 0
        self.tiempo_inicio = 0
        self.temporizador_id = None
        self.imagenes_tk = {}  # Cache de imágenes reales de Tkinter
        self.tablero = []  # Matriz para almacenar los datos de las cartas (botones)

        # 1. Configuración del Juego: Cargar imágenes
        self.cargar_imagenes()

        # 3. Interfaz de Usuario: Widgets
        self.configurar_interfaz()
        self.iniciar_juego()


 # CONFIGURACIÓN DEL JUEGO

    def cargar_imagenes(self):
        # Carga 5 pares de imágenes desde RUTA_IMAGENES y la imagen de reverso.
        imagenes_parejas = []
        
        try:
            # 1. Cargar la imagen de reverso (ruta completa)
            # Usar dimensiones fijas
            self.imagen_reverso = ImageTk.PhotoImage(
                Image.open(IMAGEN_REVERSO_PATH).resize((ANCHO_CARTA, ALTO_CARTA))
            )

            # 2. Cargar 5 pares de imágenes diferentes (img1.png a img5.png)
            for i in range(1, PARES_TOTALES + 1):
                nombre_archivo = f"img{i}.png"
                # Usa os.path.join para unir la ruta del directorio y el nombre del archivo
                ruta_completa = os.path.join(RUTA_IMAGENES, nombre_archivo) 
                
                # Usar dimensiones fijas
                imagen_original = Image.open(ruta_completa).resize((ANCHO_CARTA, ALTO_CARTA))
                imagen_tk = ImageTk.PhotoImage(imagen_original)
                
                # Almacenar la imagen y su nombre para formar parejas
                self.imagenes_tk[nombre_archivo] = imagen_tk
                imagenes_parejas.extend([nombre_archivo, nombre_archivo])

        except FileNotFoundError as e:
            # Muestra un mensaje de error claro si falta alguna imagen
            messagebox.showerror("Error de Carga", 
                f"Error al cargar archivos. Asegúrese de que existe el directorio especificado y que contiene los archivos:\n- {IMAGEN_REVERSO_PATH}\n- img1.png a img5.png\nDetalle: {e}"
            )
            self.master.destroy()
            return

        # Distribución de las cartas aleatoriamente
        random.shuffle(imagenes_parejas)
        self.distribucion_cartas = imagenes_parejas

    def configurar_interfaz(self):
        # Diseña la interfaz de usuario (Contadores, Botones, Tablero).
        
        # Frame de Información (3. Mostrar información del juego)
        info_frame = tk.Frame(self.master, bg="#b2ebf2", padx=10, pady=10, relief=tk.RAISED, borderwidth=2)
        info_frame.pack(pady=10)

        # Labels con estilo
        font_style = ("Arial", 14, "bold")
        
        self.intentos_label = tk.Label(info_frame, text="Intentos: 0", font=font_style, bg="#b2ebf2", fg="#004d40")
        self.intentos_label.pack(side=tk.LEFT, padx=30)

        self.tiempo_label = tk.Label(info_frame, text="Tiempo: 0s", font=font_style, bg="#b2ebf2", fg="#004d40")
        self.tiempo_label.pack(side=tk.LEFT, padx=30)

        # Frame de Botones (3. Incluir botones)
        botones_frame = tk.Frame(self.master, bg="#e0f7fa")
        botones_frame.pack(pady=10)

        button_style = {"bg": "#00796b", "fg": "white", "font": ("Arial", 10, "bold"), "relief": tk.RAISED}
        
        tk.Button(botones_frame, text="Reiniciar Juego", command=self.iniciar_juego, **button_style).pack(side=tk.LEFT, padx=10)
        tk.Button(botones_frame, text="Salir", command=self.master.destroy, **button_style).pack(side=tk.LEFT, padx=10)

        # Frame para el Tablero
        self.tablero_frame = tk.Frame(self.master, padx=10, pady=10, bg="#4db6ac", relief=tk.GROOVE, 
                                      width=ANCHO_TABLERO, height=ALTO_TABLERO)
        self.tablero_frame.pack()
        
       # Asegurar que el frame no cambie su tamaño 
        self.tablero_frame.pack_propagate(False)
        
    def crear_tablero_interactivo(self):
        # Distribuye las cartas aleatoriamente y crea los botones/cartas.
        
        # Limpiar tablero anterior
        for widget in self.tablero_frame.winfo_children():
            widget.destroy()
        
        self.tablero = []
        k = 0 # Índice para la lista de distribución
        
        for i in range(FILAS):
            fila_cartas = []
            for j in range(COLUMNAS):
                
                # Para un tablero 4x3 con 10 cartas, 2 espacios deben quedar vacíos (índices 10 y 11)
                if k < len(self.distribucion_cartas): 
                    nombre_imagen = self.distribucion_cartas[k]
                    imagen_real_tk = self.imagenes_tk[nombre_imagen]
                    
                    # 4. Gestión de Estado: Crear un botón que representa la carta
                    carta_btn = tk.Button(
                        self.tablero_frame, 
                        image=self.imagen_reverso, 
                        command=lambda r=i, c=j: self.voltear_carta(r, c),
                        width=ANCHO_CARTA, height=ALTO_CARTA, # Usar dimensiones constantes
                        bg="#ffffff", # Color del borde/fondo de la carta boca abajo
                        activebackground="#26a69a", # Feedback visual al hacer clic
                        relief=tk.RAISED # Asegura que el botón tiene relieve al inicio
                    )
                    carta_btn.grid(row=i, column=j, padx=5, pady=5)
                    
                    # Almacenar el estado de la carta
                    estado_carta = {
                        'btn': carta_btn,
                        'nombre_img': nombre_imagen,
                        'img_tk': imagen_real_tk,
                        'estado': 'boca_abajo' # 'boca_abajo', 'volteada', 'emparejada'
                    }
                
                else: # Espacio vacío
                    # Usar un Label para ocupar el espacio sin funcionalidad, usando dimensiones fijas
                    estado_carta = {
                        'btn': tk.Label(self.tablero_frame, width=int(ANCHO_CARTA/8), height=int(ALTO_CARTA/13), bg="#4db6ac"), 
                        'nombre_img': None,
                        'img_tk': None,
                        'estado': 'vacio'
                    }
                    # Usar el label vacío para mantener la estructura y padding
                    estado_carta['btn'].grid(row=i, column=j, padx=5, pady=5)
                    
                fila_cartas.append(estado_carta)
                k += 1
            self.tablero.append(fila_cartas)
            
# MECÁNICA DE JUEGO Y GESTIÓN DE ESTADO

    def voltear_carta(self, fila, columna):
        # Maneja el evento de clic en una carta.
        
        carta = self.tablero[fila][columna]
        
        # 4. Gestión de Estado: Validaciones
        if carta['estado'] == 'vacio' or self.bloqueo_input:
            return # Bloqueo temporal o espacio vacío
        
        if carta['estado'] in ('volteada', 'emparejada'): 
            return # Prevenir doble clic o selección de carta emparejada

        # 4. Controlar el estado: Marcar como volteada y mostrar imagen real
        carta['estado'] = 'volteada'
        carta['btn'].config(image=carta['img_tk'])
        self.cartas_visibles.append((fila, columna))

        # 4. Validar: No seleccionar más de dos cartas
        if len(self.cartas_visibles) == 2:
            self.bloqueo_input = True # Bloquear clics adicionales
            self.master.update()      # Asegurar que las 2 imágenes se muestren

            # 2. Implementar contador de intentos
            self.intentos += 1
            self.intentos_label.config(text=f"Intentos: {self.intentos}")

            # Comprobar la pareja después de un breve período
            self.master.after(TIEMPO_REVELADO, self.comprobar_pareja)


    def comprobar_pareja(self):
        # Compara las dos cartas volteadas.
        
        (r1, c1), (r2, c2) = self.cartas_visibles
        carta1 = self.tablero[r1][c1]
        carta2 = self.tablero[r2][c2]

        # 2. Si las dos cartas forman una pareja
        if carta1['nombre_img'] == carta2['nombre_img']:
            # 4. Gestión de Estado: Marcar como emparejadas
            carta1['estado'] = 'emparejada'
            carta2['estado'] = 'emparejada'
            
            # --- CAMBIO CLAVE: Mantener la carta visible, solo deshabilitar ---
            # Se queda la imagen de la carta, pero no se puede volver a hacer clic.
            carta1['btn'].config(state=tk.DISABLED, relief=tk.SUNKEN) # Leve hundimiento para indicar estado
            carta2['btn'].config(state=tk.DISABLED, relief=tk.SUNKEN) 
            
            self.pares_encontrados += 1
            if self.pares_encontrados == PARES_TOTALES:
                self.juego_terminado()
        
        # 2. Si no forman pareja, volver a voltearlas
        else:
            carta1['estado'] = 'boca_abajo'
            carta2['estado'] = 'boca_abajo'
            carta1['btn'].config(image=self.imagen_reverso)
            carta2['btn'].config(image=self.imagen_reverso)
            
        # Reiniciar variables de turno
        self.cartas_visibles = []
        self.bloqueo_input = False


    def actualizar_temporizador(self):
        # Actualiza el tiempo transcurrido.
        if self.pares_encontrados < PARES_TOTALES:
            tiempo_actual = int(time.time() - self.tiempo_inicio)
            self.tiempo_label.config(text=f"Tiempo: {tiempo_actual}s")
            # Llamada recursiva para actualizar cada segundo
            self.temporizador_id = self.master.after(1000, self.actualizar_temporizador)
    
# INTERFAZ DE USUARIO Y CONTROL DE JUEGO

    def iniciar_juego(self):
        # Inicializa o reinicia el juego.
        
        # Resetear contadores y estados
        self.intentos = 0
        self.pares_encontrados = 0
        self.intentos_label.config(text="Intentos: 0")
        self.bloqueo_input = False
        self.cartas_visibles = []
        
        # Cancelar temporizador anterior si existe
        if self.temporizador_id:
            self.master.after_cancel(self.temporizador_id)
        
        self.tiempo_inicio = time.time()
        self.tiempo_label.config(text="Tiempo: 0s")

        # Recargar, distribuir cartas y crear tablero
        self.cargar_imagenes()
        self.crear_tablero_interactivo()

        # Iniciar temporizador
        self.actualizar_temporizador()


    def juego_terminado(self):
        # Muestra el mensaje de felicitación y detiene el tiempo.
        
        # Detener temporizador
        if self.temporizador_id:
            self.master.after_cancel(self.temporizador_id)
            
        tiempo_final = int(time.time() - self.tiempo_inicio)
        
        # 3. Mostrar mensajes de felicitación
        mensaje = (
            f"🎉 ¡Felicidades! ¡Juego Completado! 🎉\n\n"
            f"Tiempo total: {tiempo_final} segundos\n"
            f"Intentos: {self.intentos}"
        )
        messagebox.showinfo("¡VICTORIA!", mensaje)


# --- INICIO DE LA APLICACIÓN ---
if __name__ == "__main__":
    try:
        from PIL import Image, ImageTk
    except ImportError:
        print("La librería 'Pillow' (PIL) no está instalada. Ejecute: pip install Pillow")
        exit()

    root = tk.Tk()
    app = JuegoMemoria(root)
    root.mainloop()