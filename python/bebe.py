import time
import math
from dataclasses import dataclass
from typing import List, Tuple
from concurrent.futures import ThreadPoolExecutor

@dataclass
class Bebe:
    nombre: str
    velocidad: float
    td: float

def simular_tiempo_bebe(bebe: Bebe, pista: List[int]) -> float:
    if bebe.velocidad <= 0.0:
        return math.inf
    t = 0.0
    for celda in pista:
        t += 1.0 / bebe.velocidad
        if celda == 1:
            t += bebe.td
    return t

def simular_bebe_individual(args: Tuple[Bebe, List[int]]) -> Tuple[str, float]:
    bebe, pista = args
    tiempo = simular_tiempo_bebe(bebe, pista)
    return bebe.nombre, tiempo

def simulacion_secuencial(REPETICIONES, bebes, pista):
    tiempos = []
    primer_resultado = None
    ultimo_resultado = None
    inicio_total = time.perf_counter()
    for rep in range(REPETICIONES):
        inicio = time.perf_counter()
        mejor_tiempo = math.inf
        idx_ganador = -1
        tiempos_bebes = []
        for i, bebe in enumerate(bebes):
            tiempo = simular_tiempo_bebe(bebe, pista)
            tiempos_bebes.append((bebe.nombre, bebe.velocidad, bebe.td, tiempo))
            if tiempo < mejor_tiempo:
                mejor_tiempo = tiempo
                idx_ganador = i
        if rep == 0:
            primer_resultado = (tiempos_bebes.copy(), bebes[idx_ganador].nombre if idx_ganador >= 0 else None, mejor_tiempo)
        if rep == REPETICIONES - 1:
            ultimo_resultado = (tiempos_bebes.copy(), bebes[idx_ganador].nombre if idx_ganador >= 0 else None, mejor_tiempo)
        fin = time.perf_counter()
        tiempos.append(fin - inicio)
    fin_total = time.perf_counter()
    tiempo_total = fin_total - inicio_total
    return tiempos, tiempo_total, primer_resultado, ultimo_resultado

def simulacion_paralela(REPETICIONES, bebes, pista, num_threads=4):
    tiempos = []
    primer_resultado = None
    ultimo_resultado = None
    inicio_total = time.perf_counter()
    for rep in range(REPETICIONES):
        inicio = time.perf_counter()
        mejor_tiempo = math.inf
        ganador = None
        tiempos_bebes = []
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            argumentos_bebes = [(bebe, pista) for bebe in bebes]
            resultados = list(executor.map(simular_bebe_individual, argumentos_bebes))
        for nombre, tiempo in resultados:
            bebe = next(b for b in bebes if b.nombre == nombre)
            tiempos_bebes.append((bebe.nombre, bebe.velocidad, bebe.td, tiempo))
            if tiempo < mejor_tiempo:
                mejor_tiempo = tiempo
                ganador = nombre
        if rep == 0:
            primer_resultado = (tiempos_bebes.copy(), ganador, mejor_tiempo)
        if rep == REPETICIONES - 1:
            ultimo_resultado = (tiempos_bebes.copy(), ganador, mejor_tiempo)
        fin = time.perf_counter()
        tiempos.append(fin - inicio)
    fin_total = time.perf_counter()
    tiempo_total = fin_total - inicio_total
    return tiempos, tiempo_total, primer_resultado, ultimo_resultado

def main():
    # Parámetros de entrada
    REPETICIONES = 10000  # Puedes ajustar este valor para pruebas grandes
    bebes = [
        Bebe("Ana", 0.5, 2.0),
        Bebe("Luis", 0.7, 1.0),
        Bebe("Mia", 0.6, 1.5)
    ]
    pista = [0, 0, 0, 1, 0, 0, 1]
    num_threads = 4  # Número de hilos para la versión paralela

    print("\n=== Simulación Secuencial ===")
    tiempos_seq, tiempo_total_seq, primer_seq, ultimo_seq = simulacion_secuencial(REPETICIONES, bebes, pista)
    print(f"Tiempo total secuencial: {tiempo_total_seq:.6f} segundos")

    print("\n=== Simulación Paralela (multithreading) ===")
    tiempos_par, tiempo_total_par, primer_par, ultimo_par = simulacion_paralela(REPETICIONES, bebes, pista, num_threads)
    print(f"Tiempo total paralelo (threads={num_threads}): {tiempo_total_par:.6f} segundos")

    # Speedup y eficiencia
    speedup = tiempo_total_seq / tiempo_total_par
    eficiencia = speedup / num_threads
    print(f"\nSpeedup: {speedup:.3f}")
    print(f"Eficiencia: {eficiencia:.3f}")

    # Mostrar parámetros usados
    print(f"\nParámetros usados:")
    print(f"Repeticiones: {REPETICIONES}")
    print(f"Bebés: {[b.nombre for b in bebes]}")
    print(f"Pista: {pista}")
    print(f"Hilos usados en paralelo: {num_threads}")

    # Mostrar resultados de la primera y última repetición de ambas versiones
    def mostrar_resultado(nombre, resultado):
        tiempos_bebes, ganador, mejor_tiempo = resultado
        print(f"Ganador: {ganador}")
        print(f"Tiempo del ganador: {mejor_tiempo:.3f} seg")
        print(f"{'Bebe':<10} {'Vel(c/s)':<12} {'TD(seg)':<12} {'Tiempo(seg)':<12}")
        for nombre, vel, td, tiempo in tiempos_bebes:
            print(f"{nombre:<10} {vel:<12.3f} {td:<12.3f} {tiempo:<12.3f}")

    print("\n--- Primera repetición secuencial ---")
    mostrar_resultado("Secuencial", primer_seq)
    print("\n--- Última repetición secuencial ---")
    mostrar_resultado("Secuencial", ultimo_seq)
    print("\n--- Primera repetición paralela ---")
    mostrar_resultado("Paralela", primer_par)
    print("\n--- Última repetición paralela ---")
    mostrar_resultado("Paralela", ultimo_par)
    
if __name__ == "__main__":
    main()
