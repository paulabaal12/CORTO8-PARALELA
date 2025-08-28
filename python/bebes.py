import time
import sys
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class Bebe:
    nombre: str
    velocidad: float
    td: float

def calcular_tiempo_celda_individual(args: Tuple[float, float, int]) -> float:
    velocidad, td, celda_valor = args
    t_celda = 1.0 / velocidad
    if celda_valor == 1:
        t_celda += td
    return t_celda

def simular_tiempo_bebe(bebe: Bebe, pista: List[int], n_celdas: int) -> float:
    if bebe.velocidad <= 0.0:
        return float('inf')
    t = 0.0
    for i in range(n_celdas):
        t_celda = 1.0 / bebe.velocidad
        if pista[i] == 1:
            t_celda += bebe.td
        t += t_celda
    return t

def simular_bebe_individual(args: Tuple[Bebe, List[int], int]) -> Tuple[str, float]:
    bebe, pista, n_celdas = args
    tiempo = simular_tiempo_bebe(bebe, pista, n_celdas)
    return bebe.nombre, tiempo

def ejecutar_repeticion(args: Tuple[List[Bebe], List[int], int, int]) -> Tuple[int, str, float, float]:
    bebes, pista, n_celdas, rep = args
    inicio = time.perf_counter()
    mejor_tiempo = float('inf')
    ganador = ""
    
    with ThreadPoolExecutor(max_workers=min(len(bebes), mp.cpu_count())) as executor:
        argumentos_bebes = [(bebe, pista, n_celdas) for bebe in bebes]
        resultados = list(executor.map(simular_bebe_individual, argumentos_bebes))
    
    for nombre, tiempo in resultados:
        if tiempo < mejor_tiempo:
            mejor_tiempo = tiempo
            ganador = nombre
    
    fin = time.perf_counter()
    tiempo_ejecucion = fin - inicio
    return rep, ganador, mejor_tiempo, tiempo_ejecucion

def main():
    REPETICIONES = 100000
    tiempos = [0.0] * REPETICIONES
    
    
    bebes = [
        Bebe("Ana1", 0.5, 2.0), Bebe("Luis1", 0.7, 1.0), Bebe("Mia1", 0.6, 1.5), Bebe("Sofia1", 0.8, 1.2), Bebe("Carlos1", 0.4, 2.5),
        Bebe("Elena1", 0.9, 0.8), Bebe("Diego1", 0.55, 1.8), Bebe("Lucia1", 0.65, 1.3), Bebe("Pablo1", 0.75, 1.1), Bebe("Carmen1", 0.45, 2.2),
        Bebe("Alex1", 0.85, 0.9), Bebe("Maria1", 0.6, 1.6), Bebe("Jose1", 0.7, 1.4), Bebe("Laura1", 0.5, 2.0), Bebe("Pedro1", 0.8, 1.0),
        Bebe("Isabel1", 0.55, 1.9), Bebe("Manuel1", 0.65, 1.7), Bebe("Rosa1", 0.75, 1.2), Bebe("Antonio1", 0.9, 0.7), Bebe("Clara1", 0.4, 2.3),
        Bebe("Ana2", 0.52, 2.1), Bebe("Luis2", 0.72, 1.1), Bebe("Mia2", 0.62, 1.6), Bebe("Sofia2", 0.82, 1.3), Bebe("Carlos2", 0.42, 2.6),
        Bebe("Elena2", 0.92, 0.9), Bebe("Diego2", 0.57, 1.9), Bebe("Lucia2", 0.67, 1.4), Bebe("Pablo2", 0.77, 1.2), Bebe("Carmen2", 0.47, 2.3),
        Bebe("Alex2", 0.87, 1.0), Bebe("Maria2", 0.62, 1.7), Bebe("Jose2", 0.72, 1.5), Bebe("Laura2", 0.52, 2.1), Bebe("Pedro2", 0.82, 1.1),
        Bebe("Isabel2", 0.57, 2.0), Bebe("Manuel2", 0.67, 1.8), Bebe("Rosa2", 0.77, 1.3), Bebe("Antonio2", 0.92, 0.8), Bebe("Clara2", 0.42, 2.4),
        Bebe("Ana3", 0.54, 2.2), Bebe("Luis3", 0.74, 1.2), Bebe("Mia3", 0.64, 1.7), Bebe("Sofia3", 0.84, 1.4), Bebe("Carlos3", 0.44, 2.7),
        Bebe("Elena3", 0.94, 1.0), Bebe("Diego3", 0.59, 2.0), Bebe("Lucia3", 0.69, 1.5), Bebe("Pablo3", 0.79, 1.3), Bebe("Carmen3", 0.49, 2.4),
        Bebe("Alex3", 0.89, 1.1), Bebe("Maria3", 0.64, 1.8), Bebe("Jose3", 0.74, 1.6), Bebe("Laura3", 0.54, 2.2), Bebe("Pedro3", 0.84, 1.2),
        Bebe("Isabel3", 0.59, 2.1), Bebe("Manuel3", 0.69, 1.9), Bebe("Rosa3", 0.79, 1.4), Bebe("Antonio3", 0.94, 0.9), Bebe("Clara3", 0.44, 2.5),
        Bebe("Ana4", 0.56, 2.3), Bebe("Luis4", 0.76, 1.3), Bebe("Mia4", 0.66, 1.8), Bebe("Sofia4", 0.86, 1.5), Bebe("Carlos4", 0.46, 2.8),
        Bebe("Elena4", 0.96, 1.1), Bebe("Diego4", 0.61, 2.1), Bebe("Lucia4", 0.71, 1.6), Bebe("Pablo4", 0.81, 1.4), Bebe("Carmen4", 0.51, 2.5),
        Bebe("Alex4", 0.91, 1.2), Bebe("Maria4", 0.66, 1.9), Bebe("Jose4", 0.76, 1.7), Bebe("Laura4", 0.56, 2.3), Bebe("Pedro4", 0.86, 1.3),
        Bebe("Isabel4", 0.61, 2.2), Bebe("Manuel4", 0.71, 2.0), Bebe("Rosa4", 0.81, 1.5), Bebe("Antonio4", 0.96, 1.0), Bebe("Clara4", 0.46, 2.6),
        Bebe("Ana5", 0.58, 2.4), Bebe("Luis5", 0.78, 1.4), Bebe("Mia5", 0.68, 1.9), Bebe("Sofia5", 0.88, 1.6), Bebe("Carlos5", 0.48, 2.9),
        Bebe("Elena5", 0.98, 1.2), Bebe("Diego5", 0.63, 2.2), Bebe("Lucia5", 0.73, 1.7), Bebe("Pablo5", 0.83, 1.5), Bebe("Carmen5", 0.53, 2.6),
        Bebe("Alex5", 0.93, 1.3), Bebe("Maria5", 0.68, 2.0), Bebe("Jose5", 0.78, 1.8), Bebe("Laura5", 0.58, 2.4), Bebe("Pedro5", 0.88, 1.4),
        Bebe("Isabel5", 0.63, 2.3), Bebe("Manuel5", 0.73, 2.1), Bebe("Rosa5", 0.83, 1.6), Bebe("Antonio5", 0.98, 1.1), Bebe("Clara5", 0.48, 2.7)
    ]
    
    num_bebes = len(bebes)
    
    
    pista = [0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0,
             1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0,
             0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1,
             0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0,
             0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1,
             0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0,
             1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0,
             0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1,
             0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0,
             0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1,
             0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0,
             1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0,
             0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1]  
    
    n_celdas = len(pista)
    
    print("Inicio de la carrera de bebes con paralelismo anidado")
    
    tiempo_total_inicio = time.perf_counter()
    
    with ProcessPoolExecutor() as executor:
        argumentos_repeticiones = [(bebes, pista, n_celdas, rep) for rep in range(REPETICIONES)]
        resultados_repeticiones = list(executor.map(ejecutar_repeticion, argumentos_repeticiones))
    
    for rep, ganador, mejor_tiempo, tiempo_ejecucion in resultados_repeticiones:
        tiempos[rep] = tiempo_ejecucion
        print(f"\n--- Repeticion {rep + 1} ---")
        print(f"Ganador: {ganador}")
        print(f"Tiempo del ganador: {mejor_tiempo:.3f} seg")
        print(f"Tiempo de ejecucion de esta repeticion: {tiempo_ejecucion:.6f} segundos")
    
    tiempo_total_fin = time.perf_counter()
    tiempo_total = tiempo_total_fin - tiempo_total_inicio
    
    print("\n===== RESUMEN DE TIEMPOS INDIVIDUALES =====")
    for i in range(REPETICIONES):
        print(f"Repeticion {i + 1}: {tiempos[i]:.6f} segundos")
    
    print(f"\nTiempo total para completar las {REPETICIONES} repeticiones: {tiempo_total:.6f} segundos")

if __name__ == "__main__":
    mp.set_start_method('spawn', force=True)
    main()
