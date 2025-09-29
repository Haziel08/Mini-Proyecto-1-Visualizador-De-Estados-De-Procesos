import tkinter as tk
from tkinter import ttk

class InterfazGrafica:
    def __init__(self, root, planificador):
        self.root = root
        self.planificador = planificador
        self.root.title("Visualizador de Procesos")
        self.root.geometry("400x300")

        self.barras = {}
        self.etiquetas = {}

        self._crear_widgets()

    def _crear_widgets(self):
        for p in self.planificador.procesos:
            frame = ttk.Frame(self.root)
            frame.pack(fill="x", pady=5)

            label = ttk.Label(frame, text=f"Proceso {p.id}")
            label.pack(side="left", padx=5)
            self.etiquetas[p.id] = ttk.Label(frame, text=p.estado)
            self.etiquetas[p.id].pack(side="left", padx=5)

            barra = ttk.Progressbar(frame, maximum=p.tiempo_total, length=200)
            barra.pack(side="left", padx=5)
            self.barras[p.id] = barra

            ttk.Button(frame, text="Bloquear", command=lambda i=p.id: self.planificador.bloquear_proceso_por_id(i)).pack(side="left")
            ttk.Button(frame, text="Desbloquear", command=lambda i=p.id: self.planificador.desbloquear_proceso_por_id(i)).pack(side="left")
            ttk.Button(frame, text="Detener", command=lambda i=p.id: self.planificador.detener_proceso_por_id(i)).pack(side="left")

        # Botón global para iniciar
        ttk.Button(self.root, text="Iniciar", command=self.planificador.iniciar_procesos).pack(pady=10)

    def actualizar_proceso(self, proceso):
        self.etiquetas[proceso.id].config(text=proceso.estado)
        self.barras[proceso.id]["value"] = proceso.tiempo_ejecutado
