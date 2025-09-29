import tkinter as tk
from logica import Planificador, Proceso
from gui import InterfazGrafica

if __name__ == "__main__":
    root = tk.Tk()

    # la GUI recibe el callback de actualización
    def actualizar_gui(proceso):
        app.actualizar_proceso(proceso)

    mi_planificador = Planificador(actualizar_gui)

    # Crear procesos con referencia al callback
    proceso1 = Proceso(1, actualizar_gui)
    proceso2 = Proceso(2, actualizar_gui)
    proceso3 = Proceso(3, actualizar_gui)

    mi_planificador.agregar_proceso(proceso1)
    mi_planificador.agregar_proceso(proceso2)
    mi_planificador.agregar_proceso(proceso3)

    app = InterfazGrafica(root, mi_planificador)

    root.mainloop()
