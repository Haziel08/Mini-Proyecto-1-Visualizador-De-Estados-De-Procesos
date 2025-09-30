import tkinter as tk
from logica import Planificador
from gui import InterfazGrafica

if __name__ == "__main__":
    # Crea la ventana principal de la aplicación
    root = tk.Tk()

    # Funciones 'callback' para comunicar los hilos con la GUI de forma segura
    def actualizar_gui(proceso):
        # 'after' asegura que la actualización de la GUI se haga en el hilo principal
        root.after(0, lambda: app.actualizar_proceso(proceso))

    def finalizar_gui(proceso):
        root.after(0, lambda: app.finalizar_proceso(proceso))

    # Crea una única instancia del planificador y la interfaz
    mi_planificador = Planificador(actualizar_gui, finalizar_gui)
    app = InterfazGrafica(root, mi_planificador)

    # Inicia el bucle principal de Tkinter para mostrar la ventana
    root.mainloop()