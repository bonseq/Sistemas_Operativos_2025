import os
from so_logica_instancia2 import Proceso, Particion, Simulador

def limpiar_pantalla():
    """Limpia la terminal según el sistema operativo"""
    os.system('cls' if os.name == 'nt' else 'clear')

def cargar_datos(nombre_archivo):
    """Lee el archivo .txt y devuelve objetos Proceso"""
    procesos = []
    try:
        with open(nombre_archivo, 'r') as f:
            for linea in f:
                linea = linea.strip()
                if not linea or "[" in linea: continue
                datos = linea.split(',')
                if len(datos) == 4:
                    # Formato: ID, Arribo, Tam, Irrupción
                    pid, arribo, tam, irr = datos[0].strip(), int(datos[1]), int(datos[2]), int(datos[3])
                    procesos.append(Proceso(pid, arribo, tam, irr))
        return procesos
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{nombre_archivo}'")
        return None

def imprimir_dashboard(estado, sim):
    """Muestra el estado del sistema en el segundo actual"""
    print("\n" + "="*70)
    print(f"⏱  TIEMPO: {estado['tiempo']} | G.M.: {sim._get_procesos_en_sistema()}/5")
    print("="*70)
    
    # Panel de CPU y Colas
    print(f" [CPU] -> {estado['cpu']} (Restante: {estado['cpu_restante']} u.t.)")
    print(f" [NUEVOS]      : {estado['nuevos']}")
    print(f" [LISTOS]      : {estado['cola_listos']}")
    print(f" [SUSPENDIDOS] : {estado['cola_suspendidos']}")
    
    # Tabla de Memoria
    print("\n--- ESTADO DE MEMORIA PRINCIPAL ---")
    print(f"{'PART':<6} | {'CONTENIDO':<12} | {'TAM':<8} | {'FRAG. INT'}")
    print("-" * 50)
    for p_str in estado['particiones']:
        # Mostramos el string definido en la clase Particion
        print(p_str)

    # Registro de Eventos
    if estado['log_eventos']:
        print("\nREGISTRO DE EVENTOS:")
        for evento in estado['log_eventos']:
            print(f"  ➜ {evento}")

def mostrar_estadisticas(sim):
    """Muestra la tabla final de resultados"""
    print("\n\n" + "╔" + "═"*58 + "╗")
    print("║" + " RESULTADOS DE LA SIMULACIÓN ".center(58) + "║")
    print("╚" + "═"*58 + "╝")
    print(f"{'ID':<6} | {'ARR':<5} | {'IRR':<5} | {'FIN':<5} | {'RET (TR)':<8} | {'ESP (TE)':<8}")
    print("-" * 60)
    
    total_tr, total_te = 0, 0
    terminados = sorted(sim.terminados, key=lambda x: x.pid)
    
    for p in terminados:
        tr = p.t_fin - p.arribo  # Cálculo académico
        te = tr - p.irrupcion_original # Cálculo académico
        print(f"{p.pid:<6} | {p.arribo:<5} | {p.irrupcion_original:<5} | {p.t_fin:<5} | {tr:<8} | {te:<8}")
        total_tr += tr
        total_te += te
    
    cant = len(terminados)
    print("-" * 60)
    print(f" > Tiempo de retorno promedio (TR): {total_tr/cant:.2f}")
    print(f" > Tiempo de espera promedio (TE) : {total_te/cant:.2f}")
    print(f" > Rendimiento del Sistema        : {cant/sim.tiempo:.4f} proc/u.t.")
    print("="*60)

def main():
    limpiar_pantalla()
    print("=== SIMULADOR DE SISTEMAS OPERATIVOS (PASO A PASO) ===\n")
    
    # 1. Entrada de archivo
    archivo = input("Ingrese el nombre del archivo de procesos (ej: prueba2.txt): ")
    procesos = cargar_datos(archivo)
    
    if not procesos:
        return

    # 2. Configuración de Particiones (Best Fit)
    particiones = [
        Particion("SO", 0, 100), Particion("1", 100, 250),
        Particion("2", 350, 150), Particion("3", 500, 50)
    ]
    
    sim = Simulador(procesos, particiones, grado_multi=5)
    
    # 3. Loop Interactivo
    while sim.simulacion_activa:
        estado = sim.tick()
        limpiar_pantalla()
        imprimir_dashboard(estado, sim)
        
        if sim.simulacion_activa:
            input("\n[ Presioná ENTER para avanzar al siguiente tick ]")
    
    # 4. Finalización
    print("\n--- SIMULACIÓN FINALIZADA ---")
    mostrar_estadisticas(sim)
    input("\nPresioná ENTER para cerrar.")

if __name__ == "__main__":
    main()