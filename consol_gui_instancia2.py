import os
from so_logica_instancia2 import Proceso, Particion, Simulador
import sys 
import time
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
    """Muestra el estado del sistema manteniendo todo en verde y bien tabulado"""
    # Forzamos verde desde el inicio de la función
    print(Fore.GREEN + "\n" + "="*75)
    print(f"⏱  TIEMPO: {estado['tiempo']} | G.M.: {sim._get_procesos_en_sistema()}/5")
    print("="*75)
    
    # Panel de CPU y Colas
    cpu_info = f"{estado['cpu']} (Restante: {estado['cpu_restante']} u.t.)"
    print(f" [CPU]         -> {cpu_info}")
    print(f" [NUEVOS]      : {estado['nuevos']}")
    print(f" [LISTOS]      : {estado['cola_listos']}")
    print(f" [SUSPENDIDOS] : {estado['cola_suspendidos']}")
    
    # Tabla de Memoria TABULADA
    print("\n--- ESTADO DE MEMORIA PRINCIPAL ---")
    header = f"{'PART':<10} | {'CONTENIDO':<15} | {'TAM':<10} | {'FRAG. INT'}"
    print(header)
    print("-" * len(header))

    # Iteramos manteniendo el color verde en cada fila
    for p in sim.particiones:
        p_id = str(p.idp)
        
        if p.proceso == "SO":
            contenido = "Sistema Op."
        elif hasattr(p.proceso, 'pid'):
            contenido = str(p.proceso.pid)
        else:
            contenido = "Libre"
        
        tam_str = f"{p.tam}K"
        frag_str = f"{p.frag_interna()}K"
        
        # Todo se imprime con Fore.GREEN implícito por el inicio de la función
        print(f" {p_id:<9} | {contenido:<15} | {tam_str:<10} | {frag_str:<10}")

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
    print_ascii_art()
    print_banner()
    
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