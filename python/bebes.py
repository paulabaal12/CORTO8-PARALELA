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
    with ThreadPoolExecutor(max_workers=3) as executor:
        
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
        Bebe("Ana", 0.5, 2.0),
        Bebe("Luis", 0.7, 1.0),
        Bebe("Mia", 0.6, 1.5)
    ]
    num_bebes = len(bebes)  
    
    pista = [0, 0, 0, 1, 0, 0, 1]  
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