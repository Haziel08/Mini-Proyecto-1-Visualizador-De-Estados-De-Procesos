import threading
import time
import random

# --- Definición de Estados ---
NUEVO = "Nuevo"
LISTO = "Listo"
EJECUCION = "En Ejecución"
BLOQUEADO = "Bloqueado"
FINALIZADO = "Finalizado"

class Proceso(threading.Thread):
    def __init__(self, id_proceso, callback_actualizacion):
        super().__init__()
        self.id = id_proceso
        self.estado = NUEVO
        self.tiempo_total = random.randint(5, 12)  # segundos de ejecución simulada
        self.tiempo_ejecutado = 0
        self.callback = callback_actualizacion
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

        if not self.detener:
            self.estado = FINALIZADO
            self._notificar()

    def _notificar(self):
        if self.callback:
            self.callback(self)

    def bloquear(self):
        self.bloqueado = True

    def desbloquear(self):
        self.bloqueado = False

    def terminar(self):
        self.detener = True
        self.estado = FINALIZADO
        self._notificar()


class Planificador:
    def __init__(self, callback_actualizacion):
        self.procesos = []
        self.callback = callback_actualizacion

    def agregar_proceso(self, proceso):
        self.procesos.append(proceso)

    def iniciar_procesos(self):
        for p in self.procesos:
            p.start()

    def bloquear_proceso_por_id(self, id_proceso):
        for p in self.procesos:
            if p.id == id_proceso:
                p.bloquear()
                break

    def desbloquear_proceso_por_id(self, id_proceso):
        for p in self.procesos:
            if p.id == id_proceso:
                p.desbloquear()
                break

    def detener_proceso_por_id(self, id_proceso):
        for p in self.procesos:
            if p.id == id_proceso:
                p.terminar()
                break
