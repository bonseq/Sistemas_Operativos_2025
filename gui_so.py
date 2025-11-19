# # gui_app.py
# import tkinter as tk
# from tkinter import ttk, scrolledtext

# from so_logica import Proceso, Particion, SimuladorManager

# lista_procesos_inicial = [
#     Proceso("P1", 50, 0, 8),
#     Proceso("P2", 150, 1, 4),
#     Proceso("P3", 200, 2, 9),
#     Proceso("P4", 40, 3, 5),
# ]
# particiones_iniciales = [
#     Particion("SO", 0, 100),
#     Particion("G", 100, 250),
#     Particion("M", 350, 150),
#     Particion("P", 500, 50),
# ]
# GRADO_MULTIPROG = 5


# #(Una sola instancia de nuestro manager)
# simulador = SimuladorManager(lista_procesos_inicial, particiones_iniciales, GRADO_MULTIPROG)

# def avanzar_tick():
#     """Llama al simulador y actualiza las etiquetas."""
    
#     estado = simulador.tick()
    
#     var_tiempo.set(f"Tiempo: {estado['tiempo']}")
#     var_cpu.set(f"CPU: {estado['cpu']} (Restante: {estado['cpu_restante']})")
    
#     var_cola_listos.set("\n".join(estado['cola_listos']) or "Vacía")
#     var_cola_suspendidos.set("\n".join(estado['cola_suspendidos']) or "Vacía")
    
#     var_particiones.set("\n".join(estado['particiones']))

#     for log in estado['log_eventos']:
#         log_texto.insert(tk.END, log + "\n")
#     log_texto.see(tk.END) # uuto-scroll hacia abajo arreglar
    
#     if not estado['simulacion_activa']:
#         boton_tick.config(text="Simulación Finalizada", state="disabled")

# ventana = tk.Tk() #esto es la root
# ventana.title("Simulador S.O. (SRTF + Best-Fit)")
# ventana.geometry("1000x600")

# var_tiempo = tk.StringVar(value="Tiempo: 0")
# var_cpu = tk.StringVar(value="CPU: Ociosa")
# var_cola_listos = tk.StringVar(value="Vacía")
# var_cola_suspendidos = tk.StringVar(value="Vacía")
# var_particiones = tk.StringVar(value="\n".join([str(p) for p in particiones_iniciales]))

# ventana.columnconfigure(0, weight=1)
# ventana.columnconfigure(1, weight=1)
# ventana.rowconfigure(1, weight=1)

# frame_estado = ttk.Frame(ventana, padding=10)
# frame_estado.grid(row=0, column=0, columnspan=2, sticky="ew")
# ttk.Label(frame_estado, textvariable=var_tiempo, font=("Helvetica", 14, "bold")).pack(side="left")
# ttk.Label(frame_estado, textvariable=var_cpu, font=("Helvetica", 14)).pack(side="right", padx=20)

# frame_colas = ttk.LabelFrame(ventana, text="Colas", padding=10)
# frame_colas.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

# ttk.Label(frame_colas, text="Listos:", font=("Helvetica", 12, "bold")).pack()
# lbl_cola_listos = ttk.Label(frame_colas, textvariable=var_cola_listos, font=("Courier", 12))
# lbl_cola_listos.pack(pady=5, anchor="w")

# ttk.Label(frame_colas, text="Listos/Suspendidos:", font=("Helvetica", 12, "bold")).pack(pady=(20, 0))
# lbl_cola_suspendidos = ttk.Label(frame_colas, textvariable=var_cola_suspendidos, font=("Courier", 12))
# lbl_cola_suspendidos.pack(pady=5, anchor="w")

# frame_derecha = ttk.Frame(ventana)
# frame_derecha.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
# frame_derecha.rowconfigure(0, weight=1)
# frame_derecha.rowconfigure(1, weight=1)
# frame_derecha.columnconfigure(0, weight=1)

# frame_particiones = ttk.LabelFrame(frame_derecha, text="Memoria (Particiones Fijas)", padding=10)
# frame_particiones.grid(row=0, column=0, sticky="nsew", pady=(0, 5))
# lbl_particiones = ttk.Label(frame_particiones, textvariable=var_particiones, font=("Courier", 14), justify="left")
# lbl_particiones.pack()

# frame_log = ttk.LabelFrame(frame_derecha, text="Log de Eventos", padding=10)
# frame_log.grid(row=1, column=0, sticky="nsew", pady=(5, 0))
# log_texto = scrolledtext.ScrolledText(frame_log, wrap=tk.WORD, height=10, font=("Courier", 10))
# log_texto.pack(fill="both", expand=True)
# log_texto.insert(tk.END, "Presiona 'Avanzar Tick' para comenzar...\n")


# boton_tick = ttk.Button(ventana, text="Avanzar Tick", command=avanzar_tick)
# boton_tick.grid(row=2, column=0, columnspan=2, sticky="ew", padx=10, pady=10, ipady=10)

# ventana.mainloop()