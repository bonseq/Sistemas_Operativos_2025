import os
import sys
from so_logica import Proceso, Particion, SimuladorManager

particiones_iniciales = [
    Particion("SO", 0, 100),
    Particion("G", 100, 250),
    Particion("M", 350, 150),
    Particion("P", 500, 50),
]
# lista_procesos_inicial = [
#     Proceso("P1", 50, 0, 8),
#     Proceso("P2", 150, 1, 4),
#     Proceso("P3", 200, 2, 9),
#     Proceso("P4", 40, 3, 5),
# ]
GRADO_MULTIPROG = 5

def cargar_desde_archivo(nombre_archivo):
    procesos = []
    try:
        with open(nombre_archivo, 'r') as f:
            for linea in f:
                # Limpiamos espacios y dividimos por coma
                datos = linea.strip().split(',')
                if len(datos) == 4:
                    pid = datos[0].strip()
                    tam = int(datos[1].strip())
                    arribo = int(datos[2].strip())
                    irrupcion = int(datos[3].strip())
                    procesos.append(Proceso(pid, tam, arribo, irrupcion))
        print(f"✅ Se cargaron {len(procesos)} procesos correctamente desde '{nombre_archivo}'.")
        return procesos
    except FileNotFoundError:
        print(f"❌ ERROR: No se encontró el archivo '{nombre_archivo}'.")
        return []
    except Exception as e:
        print(f"❌ ERROR al leer el archivo: {e}")
        return []

# --- FUNCIONES DE VISUALIZACIÓN ---
def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def imprimir_tabla_particiones(particiones_str):
    print("\n--- TABLA DE PARTICIONES ---")
    # Cabecera con formato fijo
    print(f"{'PARTICION':<10} | {'TAMAÑO':<8} | {'PROCESO':<10} | {'FRAG. INT.'}")
    print("-" * 50)
    
    for p_str in particiones_str:
        try:
            # Parseamos el string sucio que viene de la lógica
            # Formato esperado: "Part ID (SIZEK): Proc=X, Frag=YK"
            partes = p_str.replace("Part ", "").replace("K): Proc=", "|").replace(", Frag=", "|").replace("K", "").split("|")
            
            p_id_raw = partes[0].split(" (")
            pid_part = p_id_raw[0]
            tam_part = p_id_raw[1]
            proc_asig = partes[1]
            frag_int = partes[2]
            
            print(f"{pid_part:<10} | {tam_part:<8} | {proc_asig:<10} | {frag_int}")
        except:
            print(p_str) 

def mostrar_estadisticas_finales(terminados, tiempo_total):
    print("\n\n==========================================")
    print("       📊 INFORME ESTADÍSTICO FINAL       ")
    print("==========================================")
    
    if not terminados:
        print("No se completaron procesos.")
        return

    print(f"{'PROCESO':<8} | {'RETORNO':<10} | {'ESPERA':<10}")
    print("-" * 34)

    total_retorno = 0
    total_espera = 0

    for p in sorted(terminados, key=lambda x: x.pid):
        t_retorno = p.t_fin - p.arribo
        # El t_espera ya lo fuimos sumando en cada tick en la lógica
        print(f"{p.pid:<8} | {t_retorno:<10} | {p.t_espera:<10}")
        total_retorno += t_retorno
        total_espera += p.t_espera

    prom_retorno = total_retorno / len(terminados)
    prom_espera = total_espera / len(terminados)
    rendimiento = len(terminados) / tiempo_total if tiempo_total > 0 else 0

    print("-" * 34)
    print(f"Promedio T. Retorno : {prom_retorno:.2f}")
    print(f"Promedio T. Espera  : {prom_espera:.2f}")
    print(f"Rendimiento Sistema : {rendimiento:.4f} procesos/unidad tiempo")
    print("==========================================")


# --- MAIN LOOP ---
def main():
    limpiar_pantalla()
    print("=== SIMULADOR S.O. (Consola) ===")
    
    # 1. Cargar archivo
    nombre = input("Ingrese el nombre del archivo de procesos (ej: procesos.txt): ")
    if not nombre: nombre = "procesos.txt" # Default
    
    lista_procesos = cargar_desde_archivo(nombre)
    if not lista_procesos:
        input("Presione ENTER para salir...")
        return

    # 2. Iniciar Simulador
    simulador = SimuladorManager(lista_procesos, particiones_iniciales, GRADO_MULTIPROG)
    
    input("\nPresiona ENTER para iniciar la simulación paso a paso...")

    while simulador.simulacion_activa:
        # Tick de lógica
        estado = simulador.tick()
        limpiar_pantalla()

        print(f"⏱️  TIEMPO: {estado['tiempo']}")
        print("-" * 30)

        # CPU
        print(f"💻 CPU ACTUAL: {estado['cpu']} (Restante: {estado['cpu_restante']})")

        # Colas
        print(f"\n📥 COLA DE LISTOS: {estado['cola_listos']}")
        print(f"💤 COLA SUSPENDIDOS: {estado['cola_suspendidos']}")

        # Memoria
        imprimir_tabla_particiones(estado['particiones'])

        # Log
        print("\n📝 EVENTOS:")
        for evento in estado['log_eventos']:
            print(f" > {evento}")
        
        if not estado['simulacion_activa']:
            print("\n🛑 SIMULACIÓN FINALIZADA")
            break
        
        input("\n[ENTER] para siguiente tick...")

    # 3. Reporte Final
    # Accedemos a la lista de terminados dentro del manager
    mostrar_estadisticas_finales(simulador.terminados, simulador.tiempo)
    input("\nPresiona ENTER para cerrar.")

if __name__ == "__main__":
    main()