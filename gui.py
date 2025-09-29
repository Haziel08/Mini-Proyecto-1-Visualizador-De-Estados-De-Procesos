import tkinter as tk
from tkinter import ttk

class InterfazGrafica:
    def __init__(self, root, planificador):
        self.root = root
        self.planificador = planificador
        self.root.title("Visualizador de Procesos")
        self.root.geometry("600x400")

        self.barras = {}
        self.etiquetas = {}
        self.frames = {}
        self.botones = {}

        ttk.Button(self.root, text="Agregar Proceso", command=self._agregar_proceso).pack(pady=10)

    def _agregar_proceso(self):
        # Crear proceso
        proceso = self.planificador.crear_proceso()

        # Frame
        frame = ttk.Frame(self.root, relief="ridge", padding=5)
        frame.pack(fill="x", pady=5)
        self.frames[proceso.id] = frame

        ttk.Label(frame, text=f"Proceso {proceso.id}").pack(side="left", padx=5)
        self.etiquetas[proceso.id] = ttk.Label(frame, text=proceso.estado)
        self.etiquetas[proceso.id].pack(side="left", padx=5)

        barra = ttk.Progressbar(frame, maximum=proceso.tiempo_total, length=150)
        barra.pack(side="left", padx=5)
        self.barras[proceso.id] = barra

        # Botones
        botones_proc = {}

        btn_iniciar = ttk.Button(frame, text="Iniciar",
                                 command=lambda i=proceso.id, b="iniciar": self._iniciar_proceso(i, b))
        btn_iniciar.pack(side="left", padx=2)
        botones_proc["iniciar"] = btn_iniciar

        btn_bloquear = ttk.Button(frame, text="Bloquear",
                                  command=lambda i=proceso.id: self.planificador.bloquear_proceso_por_id(i))
        btn_bloquear.pack(side="left", padx=2)
        botones_proc["bloquear"] = btn_bloquear

        btn_desbloquear = ttk.Button(frame, text="Desbloquear",
                                     command=lambda i=proceso.id: self.planificador.desbloquear_proceso_por_id(i))
        btn_desbloquear.pack(side="left", padx=2)
        botones_proc["desbloquear"] = btn_desbloquear

        btn_detener = ttk.Button(frame, text="Detener",
                                 command=lambda i=proceso.id, b="detener": self._detener_proceso(i, b))
        btn_detener.pack(side="left", padx=2)
        botones_proc["detener"] = btn_detener

        self.botones[proceso.id] = botones_proc

    def _iniciar_proceso(self, id_proceso, boton):
        self.planificador.iniciar_proceso(id_proceso)
        self.botones[id_proceso][boton].config(state="disabled")

    def _detener_proceso(self, id_proceso, boton):
        self.planificador.detener_proceso_por_id(id_proceso)
        self.botones[id_proceso][boton].config(state="disabled")

    def actualizar_proceso(self, proceso):
        if proceso.id in self.etiquetas:
            self.etiquetas[proceso.id].config(text=proceso.estado)
            self.barras[proceso.id]["value"] = proceso.tiempo_ejecutado

    def finalizar_proceso(self, proceso):
        # desactivar todos los botones cuando ya terminó
        for b in self.botones[proceso.id].values():
            b.config(state="disabled")
