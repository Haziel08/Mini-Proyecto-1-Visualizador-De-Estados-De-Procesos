# 1. Importar la librería Tkinter
import tkinter as tk

# 2. Crear la ventana principal
# A esta ventana la llamamos 'root' por convención.
root = tk.Tk()

# 3. Personalizar la ventana
root.title("Mi Primera Ventana")  # Ponerle un título
root.geometry("400x300")          # Definir su tamaño en píxeles (ancho x alto)

# 4. Añadir un widget (un componente) para que no esté vacía
# En este caso, una etiqueta de texto simple.
etiqueta = tk.Label(root, text="¡Hola, Tkinter!", font=("Arial", 16))
etiqueta.pack(pady=20) # 'pack()' es la forma más simple de colocar algo en la ventana

# 5. Iniciar el bucle principal de la aplicación
# Esto mantiene la ventana abierta, esperando a que el usuario haga algo.
root.mainloop()