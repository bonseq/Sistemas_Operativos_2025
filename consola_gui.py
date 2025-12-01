import os
import sys
import time 
from so_logica import Proceso, Particion, Simulador
from colorama import Fore, Style, init
from datetime import datetime
import getpass

GRUPO = "(que)S.O."
FACULTAD = "UTN - Universidad Tecnológica Nacional"
REGIONAL = "Facultad Regional Resistencia"
INTEGRANTES = [
     "Arriazu, Nerea Micaela",
      "Bonguan, Juliana Agostina",
     "Centurión, Constanza Abril",
     "Fernández Calvi, Gustavo Félix",
     "Valussi Melendes, Fabrizio Francisco",
 ]

def print_ascii_art():
    """Pingüino de queso + título del simulador"""
    print(Fore.YELLOW + Style.BRIGHT + r"""
          
        
          
                          ████████████████                      
                        ██                ████████              
                      ██                          ████████      
                    ██                                    ████  
                  ██░░██                                    ████
                ██░░░░██                              ██████  ██
              ██  ████                        ████████        ██
            ██        ██████            ██████                ██
          ██        ██░░░░░░██    ██████                  ██████
        ██        ██░░░░░░░░░░████                      ██░░██  
      ██          ██░░░░░░░░░░██                        ██░░██  
    ██      ████████░░░░░░░░░░██                          ██████
  ██  ██████      ██░░░░░░░░░░██                              ██
  ████              ██░░░░░░██          ████                  ██
██                    ██████          ██░░░░██          ████████
██                                    ██░░░░██        ██░░░░██  
██                                      ████        ██░░░░██    
████████        ██                                  ██░░░░██    
  ██░░██      ██░░██                                ██░░░░██    
  ██░░░░██      ██                                    ██░░░░██  
    ▓▓░░██                ▓▓████▓▓                    ░░▓▓████  
  ██░░░░██              ██░░░░░░░░██                        ██  
  ██░░██              ██░░░░░░░░░░░░██                ██████    
████████            ██░░░░░░██████░░░░██      ████████          
██                  ██░░░░██      ████████████                  
██                  ██░░██                                      
██                  ▒▒▒▒                                        
██                  ▓▓██                                        
  ██████████████████ 
  

   /$$$                               /$$$    /$$$$$$      /$$$$$$    
  /$$_/                              |_  $$  /$$__  $$    /$$__  $$   
 /$$/    /$$$$$$  /$$   /$$  /$$$$$$   \  $$| $$  \__/   | $$  \ $$   
| $$    /$$__  $$| $$  | $$ /$$__  $$   | $$|  $$$$$$    | $$  | $$   
| $$   | $$  \ $$| $$  | $$| $$$$$$$$   | $$ \____  $$   | $$  | $$   
|  $$  | $$  | $$| $$  | $$| $$_____/   /$$/ /$$  \ $$   | $$  | $$   
 \  $$$|  $$$$$$$|  $$$$$$/|  $$$$$$$ /$$$/ |  $$$$$$//$$|  $$$$$$//$$
  \___/ \____  $$ \______/  \_______/|___/   \______/|__/ \______/|__/
             | $$                                                     
             | $$                                                     
             |__/                  
          
""" + Style.RESET_ALL)

    print_hacker_status()

    ancho = 100
    print(Fore.CYAN + Style.BRIGHT)
    print("SISTEMAS OPERATIVOS".center(ancho))
    print("Gestión de Memoria con Particiones Fijas, Planificación SRTF y Algoritmo Best-Fit".center(ancho))
    print(("-" * 80).center(ancho))
    print(Style.RESET_ALL)

def print_hacker_status():
    """Línea tipo [ACCESS GRANTED] con fecha, hora y usuario"""
    usuario = getpass.getuser()
    hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ancho = 100
    mensaje = (
        Fore.GREEN + Style.BRIGHT + f"[ACCESS GRANTED] ({hora})  " +
        Fore.CYAN + f"[SIMULADOR LISTO] - Bienvenido, {usuario} | Grupo {GRUPO}" +
        Style.RESET_ALL
    )
    print(mensaje.center(ancho))

def print_banner():
    """Cuadro con nombre del grupo, facultad y lista de integrantes"""
    ancho = 60
    print()
    print(Fore.CYAN + "╔" + "═" * (ancho - 2) + "╗")
    print(Fore.CYAN + "║" + Style.BRIGHT + f"{'Simulador de S.O. - ' + GRUPO:^58}" + Style.RESET_ALL + Fore.CYAN + "║")
    print(Fore.CYAN + "║" + f"{FACULTAD:^58}" + "║")
    print(Fore.CYAN + "║" + f"{REGIONAL:^58}" + "║")
    print(Fore.CYAN + "╠" + "═" * (ancho - 2) + "╣")
    print(Fore.CYAN + "║" + Style.BRIGHT + "  Integrantes:".ljust(58) + Style.RESET_ALL + Fore.CYAN + "║")
    for nombre in INTEGRANTES:
        print(Fore.CYAN + "║" + f"    {nombre}".ljust(58) + "║")
    print(Fore.CYAN + "╚" + "═" * (ancho - 2) + "╝" + Style.RESET_ALL)
    print()

particiones_iniciales = [
    Particion("SO", 0, 100),
    Particion("G", 100, 250),
    Particion("M", 350, 150),
    Particion("P", 500, 50),
]
#documentacion : https://docs.google.com/document/d/1GoweT3P1DDfHdaz83uL-rqf13k6qRlM4cwD-WfkmuLo/edit?usp=sharing
# lista_procesos_inicial = [
#     Proceso("P1", 50, 0, 8),
#     Proceso("P2", 150, 1, 4),
#     Proceso("P3", 200, 2, 9),
#     Proceso("P4", 40, 3, 5),
# ]

GRADO_MULTIPROG = 5

def cargar_desde_archivo(nombre_archivo):
    procesos = []
    print(f"\n--- CARGANDO%: {nombre_archivo} ---")
    try:
        with open(nombre_archivo, 'r') as f:
            lineas = f.readlines() 
            print(f"El archivo tiene {len(lineas)} líneas de texto en total.")
            
            for i, linea in enumerate(lineas):
                linea_limpia = linea.strip()
                
                if not linea_limpia:
                    print(f"  [Línea {i+1}] Vacía -> Ignorada")
                    continue
                
                datos = linea_limpia.split(',')
                
                if len(datos) == 4:
                    try:
                        pid = datos[0].strip()
                        arribo = int(datos[1].strip())                        
                        tam = int(datos[2].strip())
                        irrupcion = int(datos[3].strip())
                        procesos.append(Proceso(pid, arribo, tam, irrupcion))
                        print(f"  [Línea {i+1}] OK: {pid}")
                    except ValueError:
                        print(f"  [Línea {i+1}] ERROR DE NUMEROS: '{linea_limpia}' (Revise que no haya letras donde van números)")
                else:
                    print(f"  [Línea {i+1}] ERROR DE FORMATO: '{linea_limpia}' (Tiene {len(datos)} datos, se esperan 4)")

        print(f"--- FIN DE CARGA: {len(procesos)} procesos válidos ---\n")
        return procesos

    except FileNotFoundError:
        print(f"ERROR archivo no encontrado '{nombre_archivo}'.")
        return []

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def imprimir_tabla_particiones(particiones_str):
    print("\n--- TABLA DE PARTICIONES ---")
    print(f"{'PARTICION':<10} | {'TAMAÑO':<8} | {'PROCESO':<10} | {'FRAG. INT.'}")
    print("-" * 50)
    for p_str in particiones_str:
        try:
            partes = p_str.replace("Part ", "").replace("K): Proc=", "|").replace(", Frag=", "|").replace("K", "").split("|")
            p_id_raw = partes[0].split(" (")
            print(f"{p_id_raw[0]:<10} | {p_id_raw[1]:<8} | {partes[1]:<10} | {partes[2]}")
        except:
            print(p_str) 

def mostrar_estadisticas_finales(terminados, tiempo_total):
    print("\n\n==========================================")
    print("          INFORME ESTADÍSTICO FINAL       ")
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
        print(f"{p.pid:<8} | {t_retorno:<10} | {p.t_espera:<10}")
        total_retorno += t_retorno
        total_espera += p.t_espera
    prom_retorno = total_retorno / len(terminados)
    prom_espera = total_espera / len(terminados)
    rendimiento = len(terminados) / tiempo_total if tiempo_total > 0 else 0
    print("-" * 34)
    print(f"Promedio T. Retorno : {prom_retorno:.2f}")
    print(f"Promedio T. Espera  : {prom_espera:.2f}")
    print(f"Rendimiento Sistema : {rendimiento:.4f} procesos/u.t.")
    print("==========================================")

# --- MAIN LOOP ---
def main():
    limpiar_pantalla()
    init(autoreset=True)
        
    print_ascii_art()
    print_banner()
    
    print("=========== SIMULADOR S.O. (Automático) ===========")
    
    nombre = input("Ingrese archivo de procesos(debe ser un .txt): ")
    #if not nombre: nombre = "procesos.txt"
    
    lista_procesos = cargar_desde_archivo(nombre)
    if not lista_procesos:
        input("Enter para salir...")
        return

    simulador = Simulador(lista_procesos, particiones_iniciales, GRADO_MULTIPROG)
    
    print("\nIniciando simulación automática en 2 segundos...")
    time.sleep(2)

    try:
        while simulador.simulacion_activa:
            # 1. Ejecutar lógica
            estado = simulador.tick()
            
            # 2. Limpiar y Mostrar
            limpiar_pantalla()
            print(f"⏱ TIEMPO: {estado['tiempo']}")
            print("-" * 30)
            print(f" CPU ACTUAL: {estado['cpu']} (Restante: {estado['cpu_restante']})")
            print(f" NUEVOS: {estado['nuevos']}")
            print(f"\n COLA DE LISTOS: {estado['cola_listos']}")
            print(f" COLA SUSPENDIDOS: {estado['cola_suspendidos']}")
            imprimir_tabla_particiones(estado['particiones'])
            print("\n EVENTOS:")
            for evento in estado['log_eventos']:
                print(f" > {evento}")
            
            if not estado['simulacion_activa']:
                print("\n SIMULACIÓN FINALIZADA")
                break
            
            input("\nenter para avanzar al siguiente instante...")

    except KeyboardInterrupt:
        print("\n\n Simulación interrumpida por el usuario.")

    mostrar_estadisticas_finales(simulador.terminados, simulador.tiempo)
    input("\nPresiona ENTER para cerrar.")

if __name__ == "__main__":
    main()
