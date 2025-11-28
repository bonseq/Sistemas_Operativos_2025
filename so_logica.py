# so_logic.py

class Proceso:  #clase proceso
    def __init__(self, pid, tam, arribo, irrupcion):
        self.pid = pid
        self.tam = tam
        self.arribo = arribo
        self.irrupcion = irrupcion
        self.t_restante = irrupcion
        self.estado = "Nuevo"
        self.particion = None
        self.t_inicio = None
        self.t_fin = None
        self.t_espera = 0

    def __repr__(self):
        return f"P{self.pid}({self.estado}, t_rest={self.t_restante})"

class Particion:  #clase particion
    def __init__(self, idp, inicio, tam):
        self.idp = idp
        self.inicio = inicio
        self.tam = tam
        self.proceso = None

    def libre(self):
        return self.proceso is None
    
    def frag_interna(self):
        if self.proceso and self.proceso != "SO":
            return self.tam - self.proceso.tam
        return 0

    def __repr__(self):  #define como se muestra la partición textual y retorna el valor de id, tamaño  y fragmentacion, mas que nada para el GUI
        proc_id = self.proceso.pid if hasattr(self.proceso, 'pid') else (self.proceso if self.proceso else "Libre") #detectar si hay un proceso esta en x particion y que no sea la del SO, porque ella no tiene PID(Auqnue no se si si deberia)
        return f"Part {self.idp} ({self.tam}K): Proc={proc_id}, Frag={self.frag_interna()}K"


def best_fit(proceso, particiones_usuario):
    posibles = [p for p in particiones_usuario if p.libre() and p.tam >= proceso.tam]
    if not posibles:
        return None
    return min(posibles, key=lambda x: x.tam) #buscar elemento minimo de lo que retorne posibles

def revisar_suspendidos(cola_suspendidos, cola_listos, particiones_usuario, grado_multiprogramacion, tiempo):
    for p in sorted(cola_suspendidos, key=lambda x: x.arribo):
        procesos_en_memoria = len([x for x in particiones_usuario if not x.libre()])
        if procesos_en_memoria >= grado_multiprogramacion:
            break  #corta ya que hay 5 o mas procesos
        particion_asignada = best_fit(p, particiones_usuario) #se paso el break por encima asi que acomoda suspedido con besfir()
        if particion_asignada:
            particion_asignada.proceso = p
            p.particion = particion_asignada
            p.estado = "Listo"
            cola_listos.append(p)
            cola_suspendidos.remove(p)
            return True #(devulve al if haciendo que solo se cargue UN proceso y salga de aca)
    return False#en el caso de que no se pudiera traer a nadie() 

# eto e para el gui(so)
class SimuladorManager:
    
    def __init__(self, procesos_iniciales, particiones_iniciales, grado_multi):
        # guardar el estado de la simulacion 
        self.tiempo = 0
        self.cpu = None
        self.cola_listos = []
        self.cola_suspendidos = []
        self.terminados = []
        
        self.procesos_por_llegar = sorted(procesos_iniciales, key=lambda p: p.arribo)
        
        self.particiones = particiones_iniciales
        self.particion_so = self.particiones[0]
        self.particion_so.proceso = "SO"
        self.particiones_usuario = [p for p in self.particiones if p.idp != "SO"]
        
        self.grado_multiprogramacion = grado_multi
        
        self.simulacion_activa = True
        self.log_eventos = ["Inicio de Simulación"] # un log para el guiso

    def tick(self):
        """Avanza la simulación UN solo tick de tiempo."""

        #remirar esto
        if not (self.procesos_por_llegar or self.cola_listos or self.cola_suspendidos or self.cpu):
            self.simulacion_activa = False
            self.log_eventos.append(f"t={self.tiempo}: Fin de Simulación.")
            return self.get_estado_actual()

        self.log_eventos = [] # limpiar de eventos del tick anterior
        
        # llegaron procesos nuevos?
        while self.procesos_por_llegar and self.procesos_por_llegar[0].arribo == self.tiempo:
            p = self.procesos_por_llegar.pop(0)
            self.log_eventos.append(f"t={self.tiempo}: Llega {p.pid} (tam={p.tam}K, irrup={p.irrupcion}s)")
            p.estado = "Nuevo"
            
            procesos_en_memoria = len([x for x in self.particiones_usuario if not x.libre()])
            particion_asignada = best_fit(p, self.particiones_usuario)
            
            if particion_asignada and procesos_en_memoria < self.grado_multiprogramacion:
                particion_asignada.proceso = p
                p.particion = particion_asignada
                p.estado = "Listo"
                self.cola_listos.append(p)
                self.log_eventos.append(f"  {p.pid} asignado a {particion_asignada.idp} -> Listo")
            else:
                p.estado = "Listo y Suspendido"
                self.cola_suspendidos.append(p)
                self.log_eventos.append(f"  {p.pid} -> Suspendido (Sin memoria/Multiprogramación)")

        #termino el proceso en CPU?
        if self.cpu and self.cpu.t_restante == 0: 
            self.cpu.estado = "Terminado"
            self.cpu.t_fin = self.tiempo
            self.terminados.append(self.cpu)
            self.log_eventos.append(f"t={self.tiempo}: {self.cpu.pid} finalizó.")
            
            self.cpu.particion.proceso = None
            self.cpu.particion = None
            self.cpu = None
            
            if revisar_suspendidos(self.cola_suspendidos, self.cola_listos, self.particiones_usuario, self.grado_multiprogramacion, self.tiempo):
                self.log_eventos.append(f"  Proceso de suspendidos pasó a listos.")

        #logica SRTF
        proceso_mas_corto_listo = None
        if self.cola_listos:
            proceso_mas_corto_listo = min(self.cola_listos, key=lambda p: p.t_restante)

        if self.cpu is None:
            if proceso_mas_corto_listo:
                self.cpu = proceso_mas_corto_listo
                self.cola_listos.remove(self.cpu)
                self.cpu.estado = "Ejecución"
                if self.cpu.t_inicio is None:
                    self.cpu.t_inicio = self.tiempo
                self.log_eventos.append(f"t={self.tiempo}: CPU (Ociosa) -> {self.cpu.pid}")
        
        elif proceso_mas_corto_listo:
            if proceso_mas_corto_listo.t_restante < self.cpu.t_restante:
                self.log_eventos.append(f"t={self.tiempo}: {proceso_mas_corto_listo.pid} APROPIA a {self.cpu.pid}")
                self.cpu.estado = "Listo"
                self.cola_listos.append(self.cpu)
                self.cpu = proceso_mas_corto_listo
                self.cola_listos.remove(self.cpu)
                self.cpu.estado = "Ejecución"
                if self.cpu.t_inicio is None:
                    self.cpu.t_inicio = self.tiempo
        
      #anzar el tiempo
        for p in self.cola_listos:
            p.t_espera += 1
        if self.cpu:
            self.cpu.t_restante -= 1

        self.tiempo += 1
        
        return self.get_estado_actual()

    def get_estado_actual(self):  #resumen de que pasa en cada tick
        """devuelve un diccionario con el estado actual para la GUI."""
        return {
            "tiempo": self.tiempo, #-1 
            "cpu": self.cpu.pid if self.cpu else "no hay procesos",
            "cpu_restante": self.cpu.t_restante if self.cpu else 0,
            "cola_listos": [p.pid for p in self.cola_listos],
            "cola_suspendidos": [p.pid for p in self.cola_suspendidos],
            "particiones": [str(p) for p in self.particiones],  #srt se usa para mostras las particiones
            "log_eventos": self.log_eventos,
            "simulacion_activa": self.simulacion_activa
        }