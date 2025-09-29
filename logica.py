import threading, time, random

# --- Estados ---
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

    def run(self):
        self.estado = LISTO
        self._notificar()
        time.sleep(1)

        while self.tiempo_ejecutado < self.tiempo_total and not self.detener:
            if self.bloqueado:
                self.estado = BLOQUEADO
                self._notificar()
                time.sleep(1)
                continue

            self.estado = EJECUCION
            self._notificar()
            time.sleep(1)
            self.tiempo_ejecutado += 1

            self.estado = LISTO
            self._notificar()
            time.sleep(0.5)

        self.estado = FINALIZADO
        self._notificar()
        if self.callback_finalizado:
            self.callback_finalizado(self)

    def _notificar(self):
        if self.callback:
            self.callback(self)

    def bloquear(self):
        self.bloqueado = True

    def desbloquear(self):
        self.bloqueado = False

    def terminar(self):
        self.detener = True

# --- Planificador ---
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
        if p and not p.is_alive():
            p.start()

    def bloquear_proceso_por_id(self, id_proceso):
        p = self.procesos.get(id_proceso)
        if p:
            p.bloquear()

    def desbloquear_proceso_por_id(self, id_proceso):
        p = self.procesos.get(id_proceso)
        if p:
            p.desbloquear()

    def detener_proceso_por_id(self, id_proceso):
        p = self.procesos.get(id_proceso)
        if p:
            p.terminar()
