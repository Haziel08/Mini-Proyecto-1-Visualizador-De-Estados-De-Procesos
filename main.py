import tkinter as tk
from logica import Planificador
from gui import InterfazGrafica

if __name__ == "__main__":
    root = tk.Tk()

    def actualizar_gui(proceso):
        root.after(0, lambda: app.actualizar_proceso(proceso))

    def finalizar_gui(proceso):
        root.after(0, lambda: app.finalizar_proceso(proceso))

    # Solo una instancia de Planificador
    mi_planificador = Planificador(actualizar_gui, finalizar_gui)
    app = InterfazGrafica(root, mi_planificador)

    root.mainloop()
