# so_logica.py
class Proceso:
    def __init__(self, pid, arribo, tam, irrupcion):
        self.pid = pid
        self.arribo = arribo
        self.tam = tam
        self.irrupcion = irrupcion
        self.t_restante = irrupcion
        self.estado = "Nuevo"
        self.particion = None
        self.t_inicio = None
        self.t_fin = None
        self.t_espera = 0  # Re-agregado para que el GUI no explote

    def __repr__(self):
        return f"{self.pid}({self.estado}, rest={self.t_restante})"

class Particion:
    def __init__(self, idp, inicio, tam):
        self.idp = idp
        self.tam = tam
        self.proceso = None

    def libre(self):
        return self.proceso is None
    
    def frag_interna(self):
        if self.proceso and self.proceso != "SO":
            return self.tam - self.proceso.tam
        return 0

    def __repr__(self):
        proc_id = self.proceso.pid if hasattr(self.proceso, 'pid') else (self.proceso if self.proceso else "Libre")
        return f"Part {self.idp} ({self.tam}K): Proc={proc_id}, Frag={self.frag_interna()}K"

def best_fit(proceso, particiones_usuario):
    posibles = [p for p in particiones_usuario if p.libre() and p.tam >= proceso.tam]
    if not posibles:
        return None
    return min(posibles, key=lambda x: x.tam)

class Simulador:
    def __init__(self, procesos_iniciales, particiones_iniciales, grado_multi):
        self.tiempo = 0
        self.cpu = None
        self.cola_listos = []
        self.cola_suspendidos = []
        self.terminados = []
        self.procesos_por_llegar = sorted(procesos_iniciales, key=lambda p: p.arribo)
        self.particiones = particiones_iniciales
        self.particiones[0].proceso = "SO" 
        self.particiones_usuario = [p for p in self.particiones if p.idp != "SO"]
        self.grado_multiprogramacion = grado_multi
        self.simulacion_activa = True
        self.log_eventos = ["Inicio de Simulación"]

    def get_procesos_en_sistema(self):
        count = 0
        if self.cpu: count += 1
        count += len(self.cola_listos)
        count += len(self.cola_suspendidos)
        return count
    
    def tick(self):
        if not (self.procesos_por_llegar or self.cola_listos or self.cola_suspendidos or self.cpu):
            self.simulacion_activa = False
            return self.get_estado_actual()

        self.log_eventos = []

        # 1. Admisión
        while self.procesos_por_llegar and self.procesos_por_llegar[0].arribo <= self.tiempo:
            if self.get_procesos_en_sistema() < self.grado_multiprogramacion:
                p = self.procesos_por_llegar.pop(0)
                particion_ok = best_fit(p, self.particiones_usuario)
                if particion_ok:
                    particion_ok.proceso = p
                    p.particion = particion_ok
                    p.estado = "Listo"
                    self.cola_listos.append(p)
                else:
                    p.estado = "Suspendido"
                    self.cola_suspendidos.append(p)
            else:
                break

        # 2. Planificación SRTF
        if self.cola_listos:
            mas_corto = min(self.cola_listos, key=lambda x: x.t_restante)
            if self.cpu is None:
                self.cpu = mas_corto
                self.cola_listos.remove(mas_corto)
                self.cpu.estado = "Ejecución"
                if self.cpu.t_inicio is None: self.cpu.t_inicio = self.tiempo
            elif mas_corto.t_restante < self.cpu.t_restante:
                self.cpu.estado = "Listo"
                self.cola_listos.append(self.cpu)
                self.cpu = mas_corto
                self.cola_listos.remove(mas_corto)
                self.cpu.estado = "Ejecución"

        # 3. Ejecución
        if self.cpu:
            self.cpu.t_restante -= 1
            if self.cpu.t_restante == 0:
                self.cpu.t_fin = self.tiempo + 1
                self.cpu.estado = "Terminado"
                # CÁLCULO DE MÉTRICAS AQUÍ PARA EL GUI
                retorno = self.cpu.t_fin - self.cpu.arribo
                self.cpu.t_espera = retorno - self.cpu.irrupcion 
                
                self.cpu.particion.proceso = None
                self.terminados.append(self.cpu)
                self.log_eventos.append(f"t={self.tiempo + 1}: {self.cpu.pid} Finalizó")
                
                # Intentar traer suspendidos
                for p_susp in sorted(self.cola_suspendidos, key=lambda x: x.arribo):
                    p_target = best_fit(p_susp, self.particiones_usuario)
                    if p_target:
                        p_target.proceso = p_susp
                        p_susp.particion = p_target
                        p_susp.estado = "Listo"
                        self.cola_listos.append(p_susp)
                        self.cola_suspendidos.remove(p_susp)
                        break
                self.cpu = None

        self.tiempo += 1
        return self.get_estado_actual()

    def get_estado_actual(self):
        # Mantenemos todas las llaves que pide consola_gui.py
        return {
            "tiempo": self.tiempo,
            "cpu": self.cpu.pid if self.cpu else "IDLE",
            "cpu_restante": self.cpu.t_restante if self.cpu else 0,
            "cola_listos": [p.pid for p in self.cola_listos],
            "cola_suspendidos": [p.pid for p in self.cola_suspendidos],
            "nuevos": [f"{p.pid}" for p in self.procesos_por_llegar],
            "terminados": [p.pid for p in self.terminados],
            "particiones": [str(part) for part in self.particiones],
            "log_eventos": self.log_eventos,
            "simulacion_activa": self.simulacion_activa,
            "metricas": [] # Se puede dejar vacío si el GUI usa los objetos directamente
        }
        