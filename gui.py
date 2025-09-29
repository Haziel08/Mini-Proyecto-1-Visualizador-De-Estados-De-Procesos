import tkinter as tk
from tkinter import ttk, font

# --- Paleta de Colores y Estilos Mejorada ---
COLOR_FONDO_INICIO = "#4A00E0"
COLOR_FONDO_FIN = "#8E2DE2"
COLOR_GLASS = "#FFFFFF" # Un blanco con transparencia alfa
COLOR_TEXTO_PRINCIPAL = "#FFFFFF"
COLOR_TEXTO_SECUNDARIO = "#E0E0E0"
COLOR_ACCENT = "#00F260"
COLOR_BLOQUEADO = "#FF512F"

class InterfazGrafica:
    def __init__(self, root, planificador):
        self.root = root
        self.planificador = planificador
        self.root.title("Quantum Process Visualizer")
        self.root.geometry("800x600")
        self.root.minsize(600, 400) # Tamaño mínimo para responsividad

        # --- Cargar tipografía moderna ---
        self.font_bold = font.Font(family="Roboto", size=12, weight="bold")
        self.font_normal = font.Font(family="Roboto", size=10)
        self.font_small = font.Font(family="Roboto", size=8)

        # --- Manejo del cierre y responsividad ---
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
        self.root.bind("<Configure>", self._on_resize) # Evento de cambio de tamaño

        self.widgets_proceso = {}
        self._crear_widgets_principales()
        self._configurar_estilos()

    def _crear_widgets_principales(self):
        # --- Canvas para el fondo degradado ---
        self.canvas_fondo = tk.Canvas(self.root, highlightthickness=0)
        self.canvas_fondo.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Frame superior para el título y el botón de agregar
        top_frame = tk.Frame(self.root, bg=COLOR_FONDO_INICIO)
        top_frame.pack(side="top", fill="x")
        top_frame.config(bg=top_frame.master.cget('bg')) # Hack para transparencia
        
        lbl_titulo = tk.Label(top_frame, text="Quantum Visualizer", font=font.Font(family="Roboto", size=16, weight="bold"), fg=COLOR_TEXTO_PRINCIPAL, bg=top_frame.cget('bg'))
        lbl_titulo.pack(pady=(10,0))
        
        btn_agregar = tk.Button(top_frame, text="+ Agregar Proceso", font=self.font_bold, bg=COLOR_ACCENT, fg="#000000", relief="flat", padx=15, pady=5, command=self._agregar_proceso)
        btn_agregar.pack(pady=10)
        self._animate_button(btn_agregar, COLOR_ACCENT, "#00C44E")

        # Frame contenedor con scroll para los procesos
        self.canvas_scroll = tk.Canvas(self.root, borderwidth=0, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas_scroll.yview)
        self.contenedor_procesos = tk.Frame(self.canvas_scroll)

        self.canvas_scroll.configure(yscrollcommand=scrollbar.set, bg=self.root.cget('bg'))
        self.canvas_scroll.pack(side="left", fill="both", expand=True, padx=20, pady=(0, 20))
        scrollbar.pack(side="right", fill="y")
        
        self.id_ventana_canvas = self.canvas_scroll.create_window((0, 0), window=self.contenedor_procesos, anchor="nw")
        self.contenedor_procesos.bind("<Configure>", lambda e: self.canvas_scroll.configure(scrollregion=self.canvas_scroll.bbox("all")))
        self.canvas_scroll.bind('<Configure>', self._on_canvas_resize)

    def _on_canvas_resize(self, event):
        """Ajusta el ancho del frame contenedor al del canvas."""
        self.canvas_scroll.itemconfig(self.id_ventana_canvas, width=event.width)

    def _on_resize(self, event=None):
        """Dibuja el degradado cuando la ventana cambia de tamaño."""
        self.canvas_fondo.delete("gradient")
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        (r1, g1, b1) = self.root.winfo_rgb(COLOR_FONDO_INICIO)
        (r2, g2, b2) = self.root.winfo_rgb(COLOR_FONDO_FIN)
        r_ratio = float(r2 - r1) / height
        g_ratio = float(g2 - g1) / height
        b_ratio = float(b2 - b1) / height

        for i in range(height):
            nr = int(r1 + (r_ratio * i))
            ng = int(g1 + (g_ratio * i))
            nb = int(b1 + (b_ratio * i))
            color = f"#{nr:04x}{ng:04x}{nb:04x}"
            self.canvas_fondo.create_line(0, i, width, i, tags=("gradient",), fill=color)

    def _configurar_estilos(self):
        style = ttk.Style(self.root)
        style.theme_use('clam')
        style.configure('TProgressbar', troughcolor='#1A1A1A', background=COLOR_ACCENT, thickness=12, borderwidth=0)
        style.configure('Bloqueado.TProgressbar', background=COLOR_BLOQUEADO)
        style.layout('Rounded.TProgressbar',
             [('Rounded.TProgressbar.trough',
               {'children': [('Rounded.TProgressbar.pbar',
                              {'side': 'left', 'sticky': 'ns'})],
                'sticky': 'nswe'})])
        
    def _agregar_proceso(self):
        proceso = self.planificador.crear_proceso()
        pid = proceso.id
        
        # Tarjeta de "Vidrio"
        card = tk.Frame(self.contenedor_procesos, bg=f'#{int(0.1*255):02x}{int(0.1*255):02x}{int(0.1*255):02x}', relief="flat", highlightthickness=1, highlightbackground=f"#{int(0.3*255):02x}{int(0.3*255):02x}{int(0.3*255):02x}")
        card.pack(fill="x", pady=8, padx=5)
        
        info_frame = tk.Frame(card, bg=card.cget('bg'))
        info_frame.pack(fill='x', padx=15, pady=10)
        
        lbl_id = tk.Label(info_frame, text=f"Proceso {pid}", font=self.font_bold, fg=COLOR_TEXTO_PRINCIPAL, bg=card.cget('bg'))
        lbl_id.pack(side='left')
        lbl_estado = tk.Label(info_frame, text=proceso.estado, font=self.font_normal, fg=COLOR_TEXTO_SECUNDARIO, bg=card.cget('bg'))
        lbl_estado.pack(side='right')

        progress_frame = tk.Frame(card, bg=card.cget('bg'))
        progress_frame.pack(fill='x', padx=15, pady=(0, 10))
        
        barra = ttk.Progressbar(progress_frame, maximum=proceso.tiempo_total, style='TProgressbar')
        barra.pack(fill='x', expand=True, side='left', ipady=2)
        
        lbl_porcentaje = tk.Label(progress_frame, text=" 0%", font=self.font_small, fg=COLOR_TEXTO_SECUNDARIO, bg=card.cget('bg'))
        lbl_porcentaje.pack(side='right', padx=(5,0))
        
        botones_frame = tk.Frame(card, bg=card.cget('bg'))
        botones_frame.pack(fill='x', padx=15, pady=(0,10))
        
        botones_proc = {}
        acciones = [("▶ Iniciar", lambda: self._iniciar_proceso(pid)),
                    ("⏸ Bloquear", lambda: self.planificador.bloquear_proceso_por_id(pid)),
                    ("▶ Desbloq.", lambda: self.planificador.desbloquear_proceso_por_id(pid)),
                    ("⏹ Detener", lambda: self._detener_proceso(pid))]
        
        for i, (texto, comando) in enumerate(acciones):
            btn = tk.Button(botones_frame, text=texto, font=self.font_normal, bg="#2E2E2E", fg=COLOR_TEXTO_SECUNDARIO, relief="flat", command=comando)
            btn.pack(side='left', expand=True, fill='x', padx=2)
            self._animate_button(btn, "#3A3A3A", "#2E2E2E")
            botones_proc[texto.split(" ")[1].lower()] = btn

        self.widgets_proceso[pid] = {"card": card, "estado": lbl_estado, "barra": barra, "porcentaje": lbl_porcentaje, "botones": botones_proc}

    def _animate_button(self, button, hover_color, leave_color):
        button.bind("<Enter>", func=lambda e: button.config(background=hover_color))
        button.bind("<Leave>", func=lambda e: button.config(background=leave_color))
        
    def _on_closing(self):
        for pid in list(self.planificador.procesos.keys()):
            self.planificador.detener_proceso_por_id(pid)
        self.root.destroy()
        
    def _iniciar_proceso(self, pid):
        self.planificador.iniciar_proceso(pid)
        self.widgets_proceso[pid]["botones"]["iniciar"].config(state="disabled")

    def _detener_proceso(self, pid):
        self.planificador.detener_proceso_por_id(pid)
        self.widgets_proceso[pid]["botones"]["detener"].config(state="disabled")

    def actualizar_proceso(self, proceso):
        pid = proceso.id
        if pid in self.widgets_proceso:
            widgets = self.widgets_proceso[pid]
            widgets["estado"].config(text=proceso.estado)

            if proceso.estado == "Bloqueado":
                widgets["barra"].config(style='Bloqueado.TProgressbar')
            else:
                widgets["barra"].config(style='TProgressbar')
            
            widgets["barra"]["value"] = proceso.tiempo_ejecutado
            porcentaje = (proceso.tiempo_ejecutado / proceso.tiempo_total) * 100 if proceso.tiempo_total > 0 else 0
            widgets["porcentaje"].config(text=f" {porcentaje:.0f}%")

            if proceso.estado == "Finalizado":
                self.finalizar_proceso(proceso)

    def finalizar_proceso(self, proceso):
        pid = proceso.id
        if pid in self.widgets_proceso:
            for boton in self.widgets_proceso[pid]["botones"].values():
                boton.config(state="disabled")
            # Efecto visual de finalización
            self.widgets_proceso[pid]['card'].config(bg="#004D25")