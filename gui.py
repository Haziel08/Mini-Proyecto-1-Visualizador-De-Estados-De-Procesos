import tkinter as tk
from tkinter import ttk, font

# --- Paleta de Colores y Estilos Mejorada ---
COLOR_FONDO_INICIO = "#4A00E0"
COLOR_FONDO_FIN = "#8E2DE2"
COLOR_CARD = "#2C2C4A" # Un morado oscuro sólido para contraste
COLOR_TEXTO_PRINCIPAL = "#FFFFFF"
COLOR_TEXTO_SECUNDARIO = "#D0D0FF"
COLOR_ACCENT_NORMAL = "#00F260"
COLOR_ACCENT_HOVER = "#00D455"
COLOR_BLOQUEADO = "#FF512F"
COLOR_FINALIZADO_CARD = "#004D25"
COLOR_FINALIZADO_BAR = "#4CAF50" # Verde para barra finalizada

class InterfazGrafica:
    def __init__(self, root, planificador):
        self.root = root
        self.planificador = planificador
        self.root.title("Mini Proyecto 1 - Visualizador de Procesos")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)

        self.font_bold = font.Font(family="Roboto", size=12, weight="bold")
        self.font_normal = font.Font(family="Roboto", size=10)
        self.font_small = font.Font(family="Roboto", size=9)
        
        self.style = ttk.Style(self.root)
        self.style.theme_use('clam')
        self._configurar_estilos()

        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
        self.root.bind("<Configure>", self._on_resize)

        self.widgets_proceso = {}
        self.top_frame = None
        self.lbl_titulo = None
        self.canvas_scroll = None
        self.contenedor_procesos = None

        self._crear_widgets_principales()
        self._on_resize()

    def _configurar_estilos(self):
        """Predefine todos los estilos de Ttk que se usarán, asegurando que tengan un layout válido."""
        # Copiamos el layout del progressbar horizontal por defecto a nuestros nuevos estilos.
        default_layout = self.style.layout('Horizontal.TProgressbar')
        
        self.style.layout('Normal.Horizontal.TProgressbar', default_layout)
        self.style.configure('Normal.Horizontal.TProgressbar', troughcolor='#1A1A1A', background=COLOR_ACCENT_NORMAL, thickness=12, borderwidth=0)
        
        self.style.layout('Bloqueado.Horizontal.TProgressbar', default_layout)
        self.style.configure('Bloqueado.Horizontal.TProgressbar', troughcolor='#1A1A1A', background=COLOR_BLOQUEADO, thickness=12, borderwidth=0)
        
        self.style.layout('Finalizado.Horizontal.TProgressbar', default_layout)
        self.style.configure('Finalizado.Horizontal.TProgressbar', troughcolor='#1A1A1A', background=COLOR_FINALIZADO_BAR, thickness=12, borderwidth=0)


    def _crear_widgets_principales(self):
        self.canvas_fondo = tk.Canvas(self.root, highlightthickness=0)
        self.canvas_fondo.place(x=0, y=0, relwidth=1, relheight=1)
        
        self.top_frame = tk.Frame(self.root)
        self.top_frame.pack(side="top", fill="x", pady=10)
        
        self.lbl_titulo = tk.Label(self.top_frame, text="Mini Proyecto 1 - Visualizador de Procesos", font=font.Font(family="Roboto", size=16, weight="bold"), fg=COLOR_TEXTO_PRINCIPAL)
        self.lbl_titulo.pack(pady=(5,0))
        
        btn_agregar = tk.Button(self.top_frame, text="+ Agregar Proceso", font=self.font_bold, bg=COLOR_ACCENT_NORMAL, fg="#000000", relief="flat", padx=15, pady=5, command=self._agregar_proceso, borderwidth=0, cursor="hand2")
        btn_agregar.pack(pady=15)
        self._animate_button(btn_agregar, COLOR_ACCENT_HOVER, COLOR_ACCENT_NORMAL)

        self.canvas_scroll = tk.Canvas(self.root, borderwidth=0, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas_scroll.yview)
        self.contenedor_procesos = tk.Frame(self.canvas_scroll)

        self.canvas_scroll.configure(yscrollcommand=scrollbar.set)
        self.canvas_scroll.pack(side="left", fill="both", expand=True, padx=20, pady=(0, 20))
        scrollbar.pack(side="right", fill="y", pady=(0, 20))
        
        self.id_ventana_canvas = self.canvas_scroll.create_window((0, 0), window=self.contenedor_procesos, anchor="nw")
        
        self.contenedor_procesos.bind("<Configure>", lambda e: self.canvas_scroll.configure(scrollregion=self.canvas_scroll.bbox("all")))
        self.canvas_scroll.bind('<Configure>', self._on_canvas_resize)

    def _on_canvas_resize(self, event):
        self.canvas_scroll.itemconfig(self.id_ventana_canvas, width=event.width)

    def _on_resize(self, event=None):
        self.canvas_fondo.delete("gradient")
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        if width <= 1 or height <= 1: return

        (r1, g1, b1) = self.root.winfo_rgb(COLOR_FONDO_INICIO)
        (r2, g2, b2) = self.root.winfo_rgb(COLOR_FONDO_FIN)
        r_ratio, g_ratio, b_ratio = float(r2 - r1) / height, float(g2 - g1) / height, float(b2 - b1) / height

        for i in range(height):
            nr, ng, nb = int(r1 + (r_ratio * i)), int(g1 + (g_ratio * i)), int(b1 + (b_ratio * i))
            color = f"#{nr:04x}{ng:04x}{nb:04x}"
            self.canvas_fondo.create_line(0, i, width, i, tags=("gradient",), fill=color)

        if self.canvas_fondo.find_all():
            top_color = self.canvas_fondo.itemcget(self.canvas_fondo.find_all()[0], "fill")
            for widget in [self.top_frame, self.lbl_titulo, self.canvas_scroll, self.contenedor_procesos]:
                if widget: widget.config(bg=top_color)

    def _agregar_proceso(self):
        proceso = self.planificador.crear_proceso()
        pid = proceso.id
        
        card = tk.Frame(self.contenedor_procesos, bg=COLOR_CARD, relief="flat", highlightthickness=1, highlightbackground="#4A4A7A")
        card.pack(fill="x", pady=8, padx=5)
        
        main_card_frame = tk.Frame(card, bg=card.cget('bg'))
        main_card_frame.pack(fill='x', expand=True, padx=15, pady=10)
        
        # --- CORRECCIÓN DE LAYOUT ---
        # 1. Colocar el menú a la derecha PRIMERO
        menu_button = tk.Menubutton(main_card_frame, text="•••", font=self.font_bold, bg="#3E3E5A", fg=COLOR_TEXTO_SECUNDARIO, 
                                    relief="flat", cursor="hand2", borderwidth=0, padx=10, activebackground="#4A4A7A", activeforeground=COLOR_TEXTO_PRINCIPAL)
        menu_button.pack(side='right', padx=(10, 0))

        # 2. Colocar el contenedor de información para que llene el espacio RESTANTE
        progress_info_container = tk.Frame(main_card_frame, bg=card.cget('bg'))
        progress_info_container.pack(side='left', fill='x', expand=True)

        info_frame = tk.Frame(progress_info_container, bg=card.cget('bg'))
        info_frame.pack(fill='x')
        
        lbl_id = tk.Label(info_frame, text=f"Proceso {pid}", font=self.font_bold, fg=COLOR_TEXTO_PRINCIPAL, bg=card.cget('bg'))
        lbl_id.pack(side='left')
        lbl_estado = tk.Label(info_frame, text=proceso.estado, font=self.font_normal, fg=COLOR_TEXTO_SECUNDARIO, bg=card.cget('bg'))
        lbl_estado.pack(side='right')

        progress_frame = tk.Frame(progress_info_container, bg=card.cget('bg'))
        progress_frame.pack(fill='x', pady=5)
        
        # Usar el estilo base correcto que ahora existe
        barra = ttk.Progressbar(progress_frame, maximum=proceso.tiempo_total, style='Normal.Horizontal.TProgressbar')
        barra.pack(fill='x', expand=True, side='left', ipady=2)
        
        lbl_porcentaje = tk.Label(progress_frame, text=" 0%", font=self.font_small, fg=COLOR_TEXTO_SECUNDARIO, bg=card.cget('bg'))
        lbl_porcentaje.pack(side='right', padx=(5,0))

        menu_acciones = tk.Menu(menu_button, tearoff=0, bg=COLOR_CARD, fg=COLOR_TEXTO_PRINCIPAL, 
                                activebackground=COLOR_FONDO_FIN, activeforeground=COLOR_TEXTO_PRINCIPAL)
        
        menu_acciones.add_command(label="▶ Iniciar", command=lambda: self._iniciar_proceso(pid))
        menu_acciones.add_command(label="⏸ Bloquear", command=lambda: self.planificador.bloquear_proceso_por_id(pid))
        menu_acciones.add_command(label="▶ Desbloquear", command=lambda: self.planificador.desbloquear_proceso_por_id(pid))
        menu_acciones.add_command(label="⏹ Detener", command=lambda: self._detener_proceso(pid))
        
        menu_button['menu'] = menu_acciones

        self.widgets_proceso[pid] = {"card": card, "estado": lbl_estado, "barra": barra, "porcentaje": lbl_porcentaje, 
                                     "menu_button": menu_button, "menu": menu_acciones}

    def _animate_button(self, button, hover_color, leave_color):
        button.bind("<Enter>", func=lambda e: button.config(background=hover_color))
        button.bind("<Leave>", func=lambda e: button.config(background=leave_color))
        
    def _on_closing(self):
        for pid in list(self.planificador.procesos.keys()):
            self.planificador.detener_proceso_por_id(pid)
        self.root.destroy()
        
    def _iniciar_proceso(self, pid):
        self.planificador.iniciar_proceso(pid)
        widgets = self.widgets_proceso[pid]
        widgets["menu"].entryconfig("▶ Iniciar", state="disabled")

    def _detener_proceso(self, pid):
        self.planificador.detener_proceso_por_id(pid)
    
    def actualizar_proceso(self, proceso):
        pid = proceso.id
        if pid in self.widgets_proceso:
            widgets = self.widgets_proceso[pid]
            widgets["estado"].config(text=proceso.estado)

            # Referenciar los estilos corregidos
            style_actual = 'Normal.Horizontal.TProgressbar'
            if proceso.estado == "Bloqueado":
                style_actual = 'Bloqueado.Horizontal.TProgressbar'
            elif proceso.estado == "Finalizado":
                style_actual = 'Finalizado.Horizontal.TProgressbar'

            widgets["barra"].config(style=style_actual)
            
            widgets["barra"]["value"] = proceso.tiempo_ejecutado
            porcentaje = (proceso.tiempo_ejecutado / proceso.tiempo_total) * 100 if proceso.tiempo_total > 0 else 0
            widgets["porcentaje"].config(text=f" {porcentaje:.0f}%")

            if proceso.estado == "Finalizado":
                self.finalizar_proceso(proceso)

    def finalizar_proceso(self, proceso):
        pid = proceso.id
        if pid in self.widgets_proceso:
            widgets = self.widgets_proceso[pid]
            widgets["menu_button"].config(state="disabled")
            
            widgets['card'].config(bg=COLOR_FINALIZADO_CARD, highlightbackground="#007A3D")
            # Simplificamos la lógica de cambio de color al finalizar
            for widget in widgets['card'].winfo_children():
                widget.config(bg=COLOR_FINALIZADO_CARD)
                for sub_widget in widget.winfo_children():
                    sub_widget.config(bg=COLOR_FINALIZADO_CARD)
                    for sub_sub_widget in sub_widget.winfo_children():
                        sub_sub_widget.config(bg=COLOR_FINALIZADO_CARD)

