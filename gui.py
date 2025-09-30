import tkinter as tk
from tkinter import ttk, font
import time

# --- Constantes y Paleta de Colores (LÍMITE CAMBIADO) ---
MAX_PROCESOS = 10
COLOR_FONDO_INICIO = "#4A00E0"
COLOR_FONDO_FIN = "#8E2DE2"
COLOR_CARD = "#2C2C4A"
COLOR_TEXTO_PRINCIPAL = "#FFFFFF"
COLOR_TEXTO_SECUNDARIO = "#D0D0FF"
COLOR_ACCENT_NORMAL = "#00F260"
COLOR_ACCENT_HOVER = "#00D455"
COLOR_BLOQUEADO = "#FF512F"
COLOR_FINALIZADO_CARD = "#004D25"
COLOR_FINALIZADO_BAR = "#4CAF50"

class VentanaGrafica:
    def __init__(self, master, procesos_dict):
        self.top = tk.Toplevel(master)
        self.top.title("Gráfica de Comportamiento de Procesos (Actualización en vivo)")
        self.top.geometry("1000x600")
        self.top.configure(bg="#F0F0F0")

        self.procesos_dict = procesos_dict
        self.is_running = True
        self.top.protocol("WM_DELETE_WINDOW", self._on_close)
        
        self.canvas = tk.Canvas(self.top, bg="white")
        
        hbar = ttk.Scrollbar(self.top, orient="horizontal", command=self.canvas.xview)
        hbar.pack(side="bottom", fill="x")
        self.canvas.pack(side="top", fill="both", expand=True, padx=10, pady=10)
        self.canvas.configure(xscrollcommand=hbar.set)
        
        self._dibujar_leyenda()
        self.actualizar_grafica()

    def _on_close(self):
        self.is_running = False
        self.top.destroy()

    def actualizar_grafica(self):
        if not self.is_running:
            return
        self.dibujar_grafica()
        self.top.after(1000, self.actualizar_grafica)

    def dibujar_grafica(self):
        self.canvas.delete("grafica")
        
        procesos = list(self.procesos_dict.values())
        if not procesos or not any(p.history for p in procesos):
            self.canvas.create_text(500, 300, text="Inicie al menos un proceso para ver la gráfica.", font=("Roboto", 16), tags="grafica")
            return

        PADDING_Y = 50
        ROW_HEIGHT = 60
        PADDING_X = 110

        start_time = min(p.history[0][0] for p in procesos if p.history)
        
        all_finished = all(p.estado in ("Finalizado", "Detenido") for p in procesos)
        if all_finished:
            end_time = max(p.history[-1][0] for p in procesos if p.history)
        else:
            end_time = time.time()

        total_duration = end_time - start_time
        if total_duration < 1: total_duration = 1

        if total_duration <= 30: tick_interval = 2
        elif total_duration <= 120: tick_interval = 10
        elif total_duration <= 300: tick_interval = 30
        else: tick_interval = 60

        canvas_width = 2000
        self.canvas.config(scrollregion=(0, 0, canvas_width, len(procesos) * ROW_HEIGHT + PADDING_Y))
        pixels_per_second = (canvas_width - PADDING_X) / total_duration

        self.canvas.create_line(PADDING_X, PADDING_Y - 20, PADDING_X, PADDING_Y + len(procesos) * ROW_HEIGHT, fill="gray", tags="grafica")
        for t in range(0, int(total_duration) + tick_interval, tick_interval):
            x = PADDING_X + t * pixels_per_second
            self.canvas.create_line(x, PADDING_Y - 10, x, PADDING_Y - 20, fill="gray", tags="grafica")
            self.canvas.create_text(x, PADDING_Y - 25, text=f"{t}s", anchor="n", font=("Roboto", 8), tags="grafica")

        for i, proceso in enumerate(procesos):
            y_base = PADDING_Y + i * ROW_HEIGHT
            self.canvas.create_text(PADDING_X - 10, y_base + ROW_HEIGHT/2, text=f"Proceso {proceso.id}", anchor="e", font=("Roboto", 10, "bold"), tags="grafica")

            process_creation_time = proceso.history[0][0]
            if process_creation_time > start_time:
                inactive_start_x = PADDING_X
                inactive_end_x = PADDING_X + (process_creation_time - start_time) * pixels_per_second
                self.canvas.create_line(inactive_start_x, y_base + ROW_HEIGHT/2, inactive_end_x, y_base + ROW_HEIGHT/2, fill="#E0E0E0", width=5, tags="grafica")

            for j in range(len(proceso.history)):
                ts, estado = proceso.history[j]
                start_x = PADDING_X + (ts - start_time) * pixels_per_second
                current_end_time = time.time() if not all_finished else end_time
                end_ts = proceso.history[j+1][0] if j + 1 < len(proceso.history) else current_end_time
                end_x = PADDING_X + (end_ts - start_time) * pixels_per_second

                if estado == "En Ejecución":
                    self.canvas.create_rectangle(start_x, y_base + 10, end_x, y_base + ROW_HEIGHT - 10, fill=COLOR_ACCENT_NORMAL, outline="", tags="grafica")
                elif estado == "Bloqueado":
                    self.canvas.create_rectangle(start_x, y_base + 20, end_x, y_base + ROW_HEIGHT - 20, fill=COLOR_BLOQUEADO, outline="", tags="grafica")
                elif estado == "Listo":
                    self.canvas.create_line(start_x, y_base + ROW_HEIGHT/2, end_x, y_base + ROW_HEIGHT/2, fill="#777777", width=3, dash=(2, 4), tags="grafica")
            
            if proceso.estado in ("Finalizado", "Detenido"):
                lifetime = proceso.history[-1][0] - proceso.history[0][0]
                final_x = PADDING_X + (proceso.history[-1][0] - start_time) * pixels_per_second
                self.canvas.create_text(final_x + 8, y_base + ROW_HEIGHT/2, text=f"({lifetime:.1f}s)", anchor="w", font=("Roboto", 8, "italic"), fill="#555", tags="grafica")

    def _dibujar_leyenda(self):
        y_pos, x_pos, font_leyenda = 20, 110, ("Roboto", 9)
        
        self.canvas.create_rectangle(x_pos, y_pos-5, x_pos+20, y_pos+5, fill=COLOR_ACCENT_NORMAL, outline="")
        self.canvas.create_text(x_pos + 25, y_pos, text="En Ejecución", anchor="w", font=font_leyenda)
        x_pos += 120
        self.canvas.create_rectangle(x_pos, y_pos-3, x_pos+20, y_pos+3, fill=COLOR_BLOQUEADO, outline="")
        self.canvas.create_text(x_pos + 25, y_pos, text="Bloqueado", anchor="w", font=font_leyenda)
        x_pos += 120
        self.canvas.create_line(x_pos, y_pos, x_pos+20, y_pos, fill="#777777", width=3, dash=(2, 4))
        self.canvas.create_text(x_pos + 25, y_pos, text="Listo", anchor="w", font=font_leyenda)
        x_pos += 100
        self.canvas.create_line(x_pos, y_pos, x_pos+20, y_pos, fill="#E0E0E0", width=5)
        self.canvas.create_text(x_pos + 25, y_pos, text="Inactivo", anchor="w", font=font_leyenda)


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
        self._crear_widgets_principales()
        self._on_resize()

    def _configurar_estilos(self):
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
        self.top_frame.pack(side="top", fill="x", pady=5)
        
        self.lbl_titulo = tk.Label(self.top_frame, text="Mini Proyecto 1 - Visualizador de Procesos", font=font.Font(family="Roboto", size=16, weight="bold"), fg=COLOR_TEXTO_PRINCIPAL)
        self.lbl_titulo.pack(pady=(5,0))

        main_controls_container = tk.Frame(self.top_frame)
        main_controls_container.pack(pady=10)

        self.btn_agregar = tk.Button(main_controls_container, text="+ Agregar Proceso", font=self.font_bold, bg=COLOR_ACCENT_NORMAL, fg="#000000", relief="flat", padx=15, pady=5, command=self._agregar_proceso, borderwidth=0, cursor="hand2")
        self.btn_agregar.pack(side="left", padx=10)
        self._animate_button(self.btn_agregar, COLOR_ACCENT_HOVER, COLOR_ACCENT_NORMAL)

        btn_grafica = tk.Button(main_controls_container, text="📊 Ver Gráfica", font=self.font_bold, bg="#7F00FF", fg="white", relief="flat", padx=15, pady=5, command=self._abrir_ventana_grafica, borderwidth=0, cursor="hand2")
        btn_grafica.pack(side="left", padx=10)
        self._animate_button(btn_grafica, "#9933FF", "#7F00FF")

        global_controls_frame = tk.Frame(self.top_frame)
        global_controls_frame.pack(pady=(0, 5))
        
        font_global_btn = font.Font(family="Roboto", size=9)
        
        btn_iniciar_todos = tk.Button(global_controls_frame, text="▶ Iniciar Todos", font=font_global_btn, bg="#2E7D32", fg="white", relief="flat", command=self.planificador.iniciar_todos, borderwidth=0, cursor="hand2")
        btn_iniciar_todos.pack(side="left", padx=5, pady=5)
        self._animate_button(btn_iniciar_todos, "#388E3C", "#2E7D32")

        btn_bloquear_todos = tk.Button(global_controls_frame, text="⏸ Bloquear Activos", font=font_global_btn, bg="#F57C00", fg="white", relief="flat", command=self.planificador.bloquear_todos_activos, borderwidth=0, cursor="hand2")
        btn_bloquear_todos.pack(side="left", padx=5, pady=5)
        self._animate_button(btn_bloquear_todos, "#FF9800", "#F57C00")

        btn_desbloquear_todos = tk.Button(global_controls_frame, text="▶ Desbloquear Todos", font=font_global_btn, bg="#0288D1", fg="white", relief="flat", command=self.planificador.desbloquear_todos_bloqueados, borderwidth=0, cursor="hand2")
        btn_desbloquear_todos.pack(side="left", padx=5, pady=5)
        self._animate_button(btn_desbloquear_todos, "#03A9F4", "#0288D1")

        btn_detener_todos = tk.Button(global_controls_frame, text="⏹ Detener Todos", font=font_global_btn, bg="#D32F2F", fg="white", relief="flat", command=self.planificador.detener_todos_activos, borderwidth=0, cursor="hand2")
        btn_detener_todos.pack(side="left", padx=5, pady=5)
        self._animate_button(btn_detener_todos, "#F44336", "#D32F2F")
        
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
            for widget in self.top_frame.winfo_children():
                widget.config(bg=top_color)
            for widget in [self.top_frame, self.lbl_titulo, self.canvas_scroll, self.contenedor_procesos]:
                if widget and widget.winfo_exists(): widget.config(bg=top_color)
    
    def _abrir_ventana_grafica(self):
        VentanaGrafica(self.root, self.planificador.procesos)

    def _agregar_proceso(self):
        if len(self.planificador.procesos) >= MAX_PROCESOS:
            return

        proceso = self.planificador.crear_proceso()
        pid = proceso.id

        if len(self.planificador.procesos) >= MAX_PROCESOS:
            self.btn_agregar.config(state="disabled", text="Límite alcanzado")
        
        card = tk.Frame(self.contenedor_procesos, bg=COLOR_CARD, relief="flat", highlightthickness=1, highlightbackground="#4A4A7A")
        card.pack(fill="x", pady=8, padx=5)
        
        main_card_frame = tk.Frame(card, bg=card.cget('bg'))
        main_card_frame.pack(fill='x', expand=True, padx=15, pady=10)
        
        menu_button = tk.Menubutton(main_card_frame, text="•••", font=self.font_bold, bg="#3E3E5A", fg=COLOR_TEXTO_SECUNDARIO, relief="flat", cursor="hand2", borderwidth=0, padx=10, activebackground="#4A4A7A", activeforeground=COLOR_TEXTO_PRINCIPAL)
        menu_button.pack(side='right', padx=(10, 0))

        progress_info_container = tk.Frame(main_card_frame, bg=card.cget('bg'))
        progress_info_container.pack(side='left', fill='x', expand=True)

        info_frame = tk.Frame(progress_info_container, bg=card.cget('bg'))
        info_frame.pack(fill='x')
        
        lbl_id = tk.Label(info_frame, text=f"Proceso {pid}", font=self.font_bold, fg=COLOR_TEXTO_PRINCIPAL, bg=card.cget('bg'))
        lbl_id.pack(side='left')
        
        status_frame = tk.Frame(info_frame, bg=card.cget('bg'))
        status_frame.pack(side='right')

        lbl_tcpu = tk.Label(status_frame, text="0 ms", font=self.font_normal, fg=COLOR_TEXTO_SECUNDARIO, bg=card.cget('bg'))
        lbl_tcpu.pack(side='right', padx=(5,0))
        tk.Label(status_frame, text="T. CPU (ms):", font=self.font_normal, fg=COLOR_TEXTO_SECUNDARIO, bg=card.cget('bg')).pack(side='right')

        lbl_estado = tk.Label(status_frame, text=proceso.estado, font=self.font_normal, fg=COLOR_TEXTO_SECUNDARIO, bg=card.cget('bg'))
        lbl_estado.pack(side='right', padx=(10,0))
        
        progress_frame = tk.Frame(progress_info_container, bg=card.cget('bg'))
        progress_frame.pack(fill='x', pady=5)
        
        barra = ttk.Progressbar(progress_frame, maximum=proceso.tiempo_total, style='Normal.Horizontal.TProgressbar')
        barra.pack(fill='x', expand=True, side='left', ipady=2)
        
        lbl_porcentaje = tk.Label(progress_frame, text=" 0%", font=self.font_small, fg=COLOR_TEXTO_SECUNDARIO, bg=card.cget('bg'))
        lbl_porcentaje.pack(side='right', padx=(5,0))

        menu_acciones = tk.Menu(menu_button, tearoff=0, bg=COLOR_CARD, fg=COLOR_TEXTO_PRINCIPAL, activebackground=COLOR_FONDO_FIN, activeforeground=COLOR_TEXTO_PRINCIPAL)
        menu_acciones.add_command(label="▶ Iniciar", command=lambda: self._iniciar_proceso(pid))
        menu_acciones.add_command(label="⏸ Bloquear", command=lambda: self.planificador.bloquear_proceso_por_id(pid))
        menu_acciones.add_command(label="▶ Desbloquear", command=lambda: self.planificador.desbloquear_proceso_por_id(pid))
        menu_acciones.add_command(label="⏹ Detener", command=lambda: self._detener_proceso(pid))
        menu_button['menu'] = menu_acciones

        self.widgets_proceso[pid] = {"card": card, "estado": lbl_estado, "barra": barra, "porcentaje": lbl_porcentaje, "tcpu": lbl_tcpu, "menu_button": menu_button, "menu": menu_acciones}

    def _animate_button(self, button, hover_color, leave_color):
        button.bind("<Enter>", func=lambda e: button.config(background=hover_color))
        button.bind("<Leave>", func=lambda e: button.config(background=leave_color))
        
    def _on_closing(self):
        self.root.destroy()
        
    def _iniciar_proceso(self, pid):
        self.planificador.iniciar_proceso(pid)
        widgets = self.widgets_proceso[pid]
        widgets["menu"].entryconfig("▶ Iniciar", state="disabled")

    def _detener_proceso(self, pid):
        self.planificador.detener_proceso_por_id(pid)
    
    def actualizar_proceso(self, proceso):
        pid = proceso.id
        if pid in self.widgets_proceso and self.widgets_proceso[pid]["card"].winfo_exists():
            widgets = self.widgets_proceso[pid]
            widgets["estado"].config(text=proceso.estado)
            widgets["tcpu"].config(text=f"{proceso.last_execution_time_ms:.0f} ms")

            style_actual = 'Normal.Horizontal.TProgressbar'
            if proceso.estado == "Bloqueado": style_actual = 'Bloqueado.Horizontal.TProgressbar'
            elif proceso.estado in ("Finalizado", "Detenido"): style_actual = 'Finalizado.Horizontal.TProgressbar'
            widgets["barra"].config(style=style_actual)
            
            widgets["barra"]["value"] = proceso.tiempo_ejecutado
            porcentaje = (proceso.tiempo_ejecutado / proceso.tiempo_total) * 100 if proceso.tiempo_total > 0 else 0
            widgets["porcentaje"].config(text=f" {porcentaje:.0f}%")

            if proceso.estado in ("Finalizado", "Detenido"):
                self.finalizar_proceso(proceso)

    def finalizar_proceso(self, proceso):
        pid = proceso.id
        if pid in self.widgets_proceso and self.widgets_proceso[pid]["card"].winfo_exists():
            widgets = self.widgets_proceso[pid]
            widgets["menu_button"].config(state="disabled")
            
            widgets['card'].config(bg=COLOR_FINALIZADO_CARD, highlightbackground="#007A3D")
            for widget in widgets['card'].winfo_children():
                widget.config(bg=COLOR_FINALIZADO_CARD)
                for sub_widget in widget.winfo_children():
                    sub_widget.config(bg=COLOR_FINALIZADO_CARD)
                    for sub_sub_widget in sub_widget.winfo_children():
                        sub_sub_widget.config(bg=COLOR_FINALIZADO_CARD)