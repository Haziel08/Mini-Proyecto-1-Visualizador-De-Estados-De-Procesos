import threading, time, random

# --- Definición de Estados ---
NUEVO = "Nuevo"
LISTO = "Listo"
EJECUCION = "En Ejecución"
BLOQUEADO = "Bloqueado"
FINALIZADO = "Finalizado"

class Proceso(threading.Thread):
    def __init__(self, id_proceso, callback_actualizacion, callback_finalizado):
        super().__init__()
        self.id = id_proceso
        self.estado = NUEVO
        self.tiempo_total = random.randint(5, 12)
        self.tiempo_ejecutado = 0
        self.callback = callback_actualizacion
        self.callback_finalizado = callback_finalizado
        self.bloqueado = False
        self.detener = False

        self.execution_start_time = None
        self.last_execution_time_ms = 0
        self.history = [(time.time(), self.estado)]

    def _set_estado(self, nuevo_estado):
        if self.estado == nuevo_estado and self.estado != EJECUCION:
            return

        timestamp = time.time()
        
        if self.estado == EJECUCION and self.execution_start_time:
            duration = timestamp - self.execution_start_time
            self.last_execution_time_ms = duration * 1000
        
        if nuevo_estado == EJECUCION:
            self.execution_start_time = timestamp
        
        self.estado = nuevo_estado
        self.history.append((timestamp, self.estado))
        self._notificar()

    def run(self):
        self._set_estado(LISTO)
        time.sleep(random.uniform(0.5, 1.5))

        while self.tiempo_ejecutado < self.tiempo_total and not self.detener:
            if self.bloqueado:
                self._set_estado(BLOQUEADO)
                time.sleep(random.uniform(1, 2))
                if not self.detener:
                    self._set_estado(LISTO)
                continue

            self._set_estado(EJECUCION)
            time.sleep(random.uniform(0.8, 1.2))
            self.tiempo_ejecutado += 1

            if self.tiempo_ejecutado < self.tiempo_total and not self.detener:
                self._set_estado(LISTO)
                time.sleep(random.uniform(0.2, 0.5))
        
        final_state = FINALIZADO if not self.detener else "Detenido"
        self._set_estado(final_state)
        
        if self.callback_finalizado:
            self.callback_finalizado(self)

    def _notificar(self):
        if self.callback:
            self.callback(self)

    def bloquear(self): self.bloqueado = True
    def desbloquear(self): self.bloqueado = False
    def terminar(self): self.detener = True

class Planificador:
    def __init__(self, callback_actualizacion, callback_finalizado):
        self.procesos = {}
        self.callback_actualizacion = callback_actualizacion
        self.callback_finalizado = callback_finalizado
        self.contador_id = 0

    def crear_proceso(self):
        self.contador_id += 1
        p = Proceso(self.contador_id, self.callback_actualizacion, self.callback_finalizado)
        self.procesos[self.contador_id] = p
        return p

    def iniciar_proceso(self, id_proceso):
        p = self.procesos.get(id_proceso)
        if p and not p.is_alive(): p.start()

    def bloquear_proceso_por_id(self, id_proceso):
        p = self.procesos.get(id_proceso)
        if p: p.bloquear()

    def desbloquear_proceso_por_id(self, id_proceso):
        p = self.procesos.get(id_proceso)
        if p: p.desbloquear()

    def detener_proceso_por_id(self, id_proceso):
        p = self.procesos.get(id_proceso)
        if p: p.terminar()