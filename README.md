# 🧠 Simulador de Asignación de Memoria y Planificación de Procesos

## 📘 Descripción del proyecto
Este proyecto consiste en la implementación de un **simulador educativo** que permite observar los aspectos fundamentales de la **Planificación a Corto Plazo** y la **Gestión de Memoria con Particiones Fijas**, dentro de un sistema con un solo procesador.

El simulador reproduce el **ciclo de vida de un proceso** desde su ingreso al sistema hasta su finalización, aplicando los algoritmos **Best-Fit** (para la asignación de memoria) y **SRTF – Shortest Remaining Time First** (para la planificación del CPU).

---

## 🧩 Características principales

- 🧱 **Memoria con particiones fijas:**
  - 100K reservados al Sistema Operativo.
  - 250K para trabajos grandes.
  - 150K para trabajos medianos.
  - 50K para trabajos pequeños.
- 🧮 **Asignación de memoria:** Best-Fit.
- ⚙️ **Planificación del CPU:** SRTF (Shortest Remaining Time First).
- 💾 **Máximo de procesos:** 10.
- 🧍 **Grado de multiprogramación:** 5 procesos simultáneos en memoria.
- 🧠 **Estados de los procesos:** Nuevo, Listo, Listo/Suspendido, Ejecución y Terminado.
- 📊 **Salida del simulador:**
  - Estado del procesador.
  - Tabla de particiones (id, tamaño, proceso, fragmentación).
  - Colas de listos y suspendidos.
  - Estadísticas finales (tiempos de espera, retorno y rendimiento del sistema).

---

## 📁 Estructura del proyecto
📂 Simulador-Memoria-Procesos/
├── main.py # Programa principal del simulador
├── proceso.py # Clase que define un proceso
├── particion.py # Clase que define una partición de memoria
├── planificador.py # Lógica del algoritmo SRTF
├── memoria.py # Gestión de particiones y asignación Best-Fit
├── procesos.txt # Archivo de entrada con procesos de prueba
├── README.md # Este archivo :)
└── docs/
├── howto.pdf # Guía de uso para ejecutar el simulador
└── informe_final.pdf # Informe con resultados y conclusiones

El simulador leerá automáticamente el archivo procesos.txt y mostrará los eventos de la simulación paso a paso:

Llegada de nuevos procesos.

Asignación o liberación de memoria.

Cambio de proceso en ejecución.

Finalización de la simulación con informe estadístico.

🧰 Herramientas utilizadas

🐍 Python 3.10

📋 Trello (para seguimiento del proyecto)

🧮 Google Sheets (para pruebas y cálculos de tiempos)

🧑‍💻 VSCode(entorno de desarrollo)

🧑‍🎓 Autores

Equipo: [que(SO) / integrantes]
📚 Facultad Regional Resistencia – UTN
📆 Año: 2025
📘 Materia: Sistemas Operativos
👩‍🏫 Docentes: [pupi]

🏁 Estado del proyecto

✅ En desarrollo
📅 Avance 1: Base del simulador + lectura de procesos
📅 Avance 2: Integración Best-Fit y SRTF
📅 Entrega final: 02/12/2025
