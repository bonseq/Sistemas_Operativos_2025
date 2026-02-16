# so_logic.py
class Proceso:  #clase proceso
    def __init__(self, pid, arribo, tam, irrupcion):
        self.pid =pid
        self.arribo =arribo
        self.tam =tam
        self.irrupcion =irrupcion
        self.t_restante =irrupcion
        self.irrupcion_original= irrupcion
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
        self.tam = tam
        self.proceso = None

    def libre(self):
        return self.proceso is None
    
    def frag_interna(self):
        return self.tam - self.proceso.tam if (self.proceso and self.proceso != "SO") else 0

    def __str__(self):  #define como se muestra la partición textual y retorna el valor de id, tamaño  y fragmentacion, mas que nada para el GUI
        proc_id = self.proceso.pid if hasattr(self.proceso, 'pid') else (self.proceso if self.proceso else "Libre") #detectar si hay un proceso esta en x particion y que no sea la del SO, porque ella no tiene PID(Auqnue no se si si deberia)
        return f"Part {self.idp} ({self.tam}K): Proc={proc_id}, Frag={self.frag_interna()}K"
    
class Simulador:
    def __init__(self, procesos_iniciales, particiones_iniciales, grado_multi):
        self.tiempo = 0
        self.cpu = None
        self.cola_listos = []
        self.cola_suspendidos = [] 
        self.nuevos = sorted(procesos_iniciales, key=lambda p: p.arribo)
        self.terminados = []
        self.particiones = particiones_iniciales
        self.particiones[0].proceso = "SO"
        self.particiones_usuario = [p for p in self.particiones if p.idp != "SO"]
        self.grado_multiprogramacion = grado_multi
        self.simulacion_activa = True
        self.log_eventos = ["Inicio de Simulación"]

    def _get_procesos_en_sistema(self):
        count = 0
        if self.cpu: count += 1  #preguntamos si hay un proceso cargado en cpu, si es asi sumamos uno, sino se saltea
        count += len(self.cola_listos) + len(self.cola_suspendidos) #sumamos la cola de listos mas la de suspendidos para sacar el gdm
        return count

    def tick(self):
        max_particion_sistema = max([p.tam for p in self.particiones_usuario]) if self.particiones_usuario else 0

        if not (self.nuevos or self.cola_listos or self.cola_suspendidos or self.cpu):
            self.simulacion_activa = False #desactivamos la simulacion cuando todas  las colas esten vacias
            return self.get_estado_actual() #devolvemos el ultimo reporte antes de cerrar

        self.log_eventos = []#borramos la lista que muestra os eventos
 
        #loop principal: entrada al so (controla multiprogramacion)
        while self.nuevos and self.nuevos[0].arribo <= self.tiempo: #revisamos si hay procesos en nuevo y si al primero le toca entrar segun el tiempo
            p = self.nuevos[0] #si es asi, miramos al que este
            if p.tam > max_particion_sistema: #en caso deque su tamaño supere una particion, 
                p=self.nuevos.pop(0) #lo sacamos
                p.t_fin= None #DIRECTAMNETE NO LE ASIGNAMOS TIEMPO
                self.log_eventos.append(f"t={self.tiempo}: ERROR - {p.pid} ({p.tam}K) excede RAM máxima") #infromamos error
                p.estado = "Rechazado"
                self.terminados.append(p) #terminados
                continue #saltamos al siguiente proceso
            if self._get_procesos_en_sistema() < self.grado_multiprogramacion: #preguntamos si el numero de procesos en sistema es menor a el GDM
                p = self.nuevos.pop(0) #si es asi, miramos al que este
                posibles = [part for part in self.particiones_usuario if part.libre() and part.tam >= p.tam] #creamos el listado de posibles particiones para nuestro p
                if posibles: #si esta lista existe :
                    mejor_p = min(posibles, key=lambda x: x.tam) #buscamos el minimo sgeun best-fit
                    mejor_p.proceso = p #asignamos el proceso
                    p.particion = mejor_p #luego le pasamosla informacion de la particion que pcupa
                    p.estado = "Listo" #pasa a listo eserando cpu
                    self.cola_listos.append(p) #lo ponemos en listo
                    self.log_eventos.append(f"t={self.tiempo}: {p.pid} cargado en Memoria") #informamos
                else:
                    p.estado = "Listo y Suspendido" #si vemos que no hay memoria lo mandamos a listo suspendido
                    self.cola_suspendidos.append(p) #lo colocamos en listo suspendido :V
                    self.log_eventos.append(f"t={self.tiempo}: {p.pid} a Listo y Suspendidos (Sin RAM)") #informamos
            else:
                break #si el gdm llego al maximo, cortamos

        # logica SRTF 
        if self.cola_listos: #si hay algo en listos
            mas_corto = min(self.cola_listos, key=lambda x: x.t_restante)  #le asignamos el que tenga menor t restante
            #dos caminos que quede un solo proceso o que haya un proceso con t_restante menor al que ya esta
            if self.cpu is None: #si la cpu esta vacia(A)
                self.cpu = mas_corto #agarramos el primero que quede en la cola de listos
                self.cola_listos.remove(mas_corto) #lo sacamos de la cola de listos
                self.cpu.estado = "Ejecución" #cambiamos su esatdo a ejecucion
            elif mas_corto.t_restante < self.cpu.t_restante: #se compara si es que hay un mejor candidato(B)
                self.log_eventos.append(f"t={self.tiempo}: {mas_corto.pid} apropia CPU") #informamos quien apropia
                self.cpu.estado = "Listo" #vulve a listo el proceso q se saco
                self.cola_listos.append(self.cpu)
                self.cpu = mas_corto #y ponemos al mas corto
                self.cola_listos.remove(mas_corto)
                self.cpu.estado = "Ejecución"

        #ejecución
        if self.cpu: #preguntamos si hay procesos en cpu
            self.cpu.t_restante -= 1 #si es asis restamos uno por cada tick
            if self.cpu.t_restante == 0: #si llega a cero-->
                self.cpu.t_fin = self.tiempo + 1 # marcamos que termino en el inicio del proximo segundo de la simulacion
                tr = self.cpu.t_fin - self.cpu.arribo #calculamos su tiempo de retorno
                self.cpu.t_espera = tr - self.cpu.irrupcion_original #y su tiempo de espera
                
                self.cpu.estado = "Terminado" 
                self.cpu.particion.proceso = None #sacamos al proceso una vez finalizado
                self.terminados.append(self.cpu)
                self.log_eventos.append(f"t={self.tiempo+1}: {self.cpu.pid} Finalizó") #informamos
                self.cpu = None #vaciamos cpu
                
                # al liberar RAM, chequear suspendidos
                for s in sorted(self.cola_suspendidos, key=lambda x: x.arribo): #miramos a suspendidos segun su arribo
                    libres = [part for part in self.particiones_usuario if part.libre() and part.tam >= s.tam] #buscamos la particion que le sirva a este proceso
                    if libres:
                        mejor = min(libres, key=lambda x: x.tam) #si hay alguna elegimos la de menor tamaño
                        mejor.proceso = s
                        s.particion = mejor
                        s.estado = "Listo" #pasa a listo
                        self.cola_listos.append(s) #lo ponemos en la cola de listos
                        self.cola_suspendidos.remove(s) #y la sacamos de suspendido
                        break 
        self.tiempo += 1 # aumentamos uno de tiempo al simulador total
        return self.get_estado_actual() #alfinal devolvemos todo al estado actual

    def get_estado_actual(self):
        # aseguramos todas las llaves que pide consola para mostrar por pantalla
        return {
            "tiempo": self.tiempo,
            "cpu": self.cpu.pid if self.cpu else "IDLE",
            "cpu_restante": self.cpu.t_restante if self.cpu else 0,
            "cola_listos": [p.pid for p in self.cola_listos],
            "cola_suspendidos": [p.pid for p in self.cola_suspendidos],
            "nuevos": [f"{p.pid}(t={p.arribo})" for p in self.nuevos],
            "terminados": [p.pid for p in self.terminados],
            "particiones": [str(p) for p in self.particiones],
            "log_eventos": self.log_eventos,
            "simulacion_activa": self.simulacion_activa
        }