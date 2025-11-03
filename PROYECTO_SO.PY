# -----------------------------------------------
# Simulador de Planificación y Asignación de Memoria
# Algoritmo de planificación: SRTF
# Política de asignación de memoria: Best-Fit (particiones fijas)
# -----------------------------------------------

import heapq  # para la cola de prioridad del SRTF

# -----------------------------------------------
# CLASES PRINCIPALES
# -----------------------------------------------

class Proceso:
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


class Particion:
    def __init__(self, idp, inicio, tam):
        self.idp = idp
        self.inicio = inicio
        self.tam = tam
        self.proceso = None  # proceso asignado (None si está libre)

    def libre(self):
        return self.proceso is None

    def __repr__(self):
        return f"Particion {self.idp}: {self.tam}K -> {self.proceso}"


# -----------------------------------------------
# FUNCIONES DE ASIGNACIÓN DE MEMORIA (Best-Fit)
# -----------------------------------------------

def best_fit(proceso, particiones):
    """Devuelve la partición más pequeña donde el proceso puede entrar."""
    posibles = [p for p in particiones if p.libre() and p.tam >= proceso.tam]
    if not posibles:
        return None
    # se elige la de menor tamaño (best fit)
    return min(posibles, key=lambda x: x.tam)


# -----------------------------------------------
# FUNCIÓN DE PLANIFICACIÓN SRTF
# -----------------------------------------------

def seleccionar_srtf(cola_listos):
    """Selecciona el proceso con menor tiempo restante."""
    if not cola_listos:
        return None
    return min(cola_listos, key=lambda p: p.t_restante)


# -----------------------------------------------
# FUNCIÓN PRINCIPAL DE SIMULACIÓN
# -----------------------------------------------

def simulador(procesos, particiones, grado_multiprogramacion=5):
    tiempo = 0
    cpu = None
    cola_listos = []
    cola_suspendidos = []
    terminados = []

    print("\n--- INICIO DE SIMULACIÓN ---\n")

    while procesos or cola_listos or cpu:
        # 1️⃣ Llegada de nuevos procesos
        llegadas = [p for p in procesos if p.arribo == tiempo]
        for p in llegadas:
            print(f"t={tiempo}: Llega {p.pid}")
            p.estado = "Nuevo"

            # Intentar asignar memoria
            particion = best_fit(p, particiones)
            if particion and len([x for x in particiones if not x.libre()]) < grado_multiprogramacion:
                particion.proceso = p
                p.particion = particion
                p.estado = "Listo"
                cola_listos.append(p)
                print(f"  {p.pid} asignado a {particion.idp}")
            else:
                p.estado = "Suspendido"
                cola_suspendidos.append(p)
                print(f"  {p.pid} suspendido por falta de memoria")

            procesos.remove(p)

        # 2️⃣ Selección del proceso (SRTF)
        if cpu is None and cola_listos:
            cpu = seleccionar_srtf(cola_listos)
            cola_listos.remove(cpu)
            cpu.estado = "Ejecución"
            if cpu.t_inicio is None:
                cpu.t_inicio = tiempo
            print(f"t={tiempo}: CPU -> {cpu.pid}")

        # 3️⃣ Ejecución del proceso actual
        if cpu:
            cpu.t_restante -= 1
            if cpu.t_restante == 0:
                cpu.estado = "Terminado"
                cpu.t_fin = tiempo + 1
                terminados.append(cpu)
                print(f"t={tiempo+1}: {cpu.pid} finalizó")
                # liberar su partición
                if cpu.particion:
                    cpu.particion.proceso = None
                cpu = None

        # 4️⃣ Avanzar el tiempo
        tiempo += 1

    print("\n--- FIN DE SIMULACIÓN ---\n")
    for p in terminados:
        print(f"{p.pid}: inicio={p.t_inicio}, fin={p.t_fin}, retorno={p.t_fin - p.arribo}")

# -----------------------------------------------
# CARGA DE DATOS (puede ser desde archivo más adelante)
# -----------------------------------------------

if __name__ == "__main__":
    # Procesos de prueba (pid, tamaño, arribo, irrupción)
    lista_procesos = [
        Proceso("P1", 50, 0, 5),
        Proceso("P2", 150, 1, 3),
        Proceso("P3", 200, 2, 4),
    ]

    # Particiones fijas
    particiones = [
        Particion("SO", 0, 100),
        Particion("G", 100, 250),
        Particion("M", 350, 150),
        Particion("P", 500, 50),
    ]

    simulador(lista_procesos, particiones)
