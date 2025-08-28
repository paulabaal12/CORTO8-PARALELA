import time
import math

# Clase que representa a un bebé participante
class Bebe:
    def __init__(self, nombre, velocidad, td):
        self.nombre = nombre      # Nombre del bebé
        self.velocidad = velocidad  # Velocidad en celdas/segundo
        self.td = td              # Tiempo de distracción por juguete (segundos)

# Simula el tiempo que tarda un bebé en recorrer la pista
def simular_tiempo_bebe(bebe, pista):
    if bebe.velocidad <= 0.0:
        return math.inf  # Si la velocidad es inválida, retorna infinito
    t = 0.0
    for celda in pista:
        t += 1.0 / bebe.velocidad  # Tiempo en avanzar una celda
        if celda == 1:
            t += bebe.td           # Suma tiempo de distracción si hay juguete
    return t

# Función principal del programa
def main():
    REPETICIONES = 5  # Número de repeticiones de la simulación
    tiempos = []           # Lista para guardar los tiempos de cada repetición

    # Definición de los bebés participantes y pista
    bebes = [
        Bebe("Ana", 0.5, 2.0),
        Bebe("Luis", 0.7, 1.0),
        Bebe("Mia", 0.6, 1.5)
    ]
    pista = [0, 0, 0, 1, 0, 0, 1]  # Pista: 0=nada, 1=juguete
    n_celdas = len(pista)          # Número de celdas de la pista

    # Imprime los parámetros usados
    print("\n===== PARÁMETROS DE LA SIMULACIÓN SECUENCIAL =====")
    print(f"Cantidad de bebés: {len(bebes)}")
    print(f"Nombres de bebés: {[b.nombre for b in bebes]}")
    print(f"Pista: {pista}")
    print(f"Cantidad de celdas: {n_celdas}")
    print(f"Cantidad de iteraciones: {REPETICIONES}")

    inicio_total = time.time()  # Marca el inicio del tiempo total

    primer_resultado = {}  # Guardará los resultados de la primera repetición
    ultimo_resultado = {}  # Guardará los resultados de la última repetición
    for rep in range(REPETICIONES):
        inicio = time.time()  # Marca el inicio de la repetición

        mejor_tiempo = math.inf        # Mejor tiempo encontrado en la repetición
        idx_ganador = -1               # Índice del bebé ganador
        tiempos_bebes = []             # Lista de tiempos de cada bebé

        # Imprime resultados solo en la primera repetición
        if rep == 0:
            print(f"\n--- Repeticion {rep+1} ---")
            print(f"Pista de {n_celdas} celdas (0=nada, 1=juguete):", pista)
            print("\nResultados:")
            print(f"{'Bebe':<10} {'Vel(c/s)':<12} {'TD(seg)':<12} {'Tiempo(seg)':<12}")

        # Simula la carrera para cada bebé
        for i, bebe in enumerate(bebes):
            tiempo = simular_tiempo_bebe(bebe, pista)
            tiempos_bebes.append((bebe.nombre, bebe.velocidad, bebe.td, tiempo))
            if rep == 0:
                print(f"{bebe.nombre:<10} {bebe.velocidad:<12.3f} {bebe.td:<12.3f} {tiempo:<12.3f}")
            if tiempo < mejor_tiempo:
                mejor_tiempo = tiempo
                idx_ganador = i

        # Guarda e imprime el resultado de la primera repetición
        if rep == 0:
            if idx_ganador >= 0:
                print(f"\nGanador: {bebes[idx_ganador].nombre}\nTiempo del ganador: {mejor_tiempo:.3f} seg")
            else:
                print("\nNadie termino la carrera (verifica velocidades > 0).")
            primer_resultado = {
                'bebes': tiempos_bebes.copy(),
                'ganador': bebes[idx_ganador].nombre if idx_ganador >= 0 else None,
                'mejor_tiempo': mejor_tiempo
            }
        # Guarda el resultado de la última repetición
        if rep == REPETICIONES - 1:
            ultimo_resultado = {
                'bebes': tiempos_bebes.copy(),
                'ganador': bebes[idx_ganador].nombre if idx_ganador >= 0 else None,
                'mejor_tiempo': mejor_tiempo
            }

        fin = time.time()  # Marca el fin de la repetición
        tiempo_ejecucion = fin - inicio
        tiempos.append(tiempo_ejecucion)  # Guarda el tiempo de la repetición

    fin_total = time.time()  # Marca el fin del tiempo total
    tiempo_total = fin_total - inicio_total

    # Imprime el resumen de tiempos individuales
    print("\n===== RESUMEN DE TIEMPOS INDIVIDUALES =====")
    for i, t in enumerate(tiempos):
        print(f"Repeticion {i+1}: {t:.6f} segundos")

    # Imprime el tiempo total de todas las repeticiones
    print(f"\nTiempo total para completar las {REPETICIONES} repeticiones: {tiempo_total:.6f} segundos")

    # Comparación entre la primera y la última repetición
    print("\n===== COMPARACIÓN PRIMERA Y ÚLTIMA REPETICIÓN =====")
    print("\n--- Primera repetición ---")
    print(f"{'Bebe':<10} {'Vel(c/s)':<12} {'TD(seg)':<12} {'Tiempo(seg)':<12}")
    for nombre, vel, td, tiempo in primer_resultado['bebes']:
        print(f"{nombre:<10} {vel:<12.3f} {td:<12.3f} {tiempo:<12.3f}")
    if primer_resultado['ganador']:
        print(f"Ganador: {primer_resultado['ganador']}\nTiempo del ganador: {primer_resultado['mejor_tiempo']:.3f} seg")
    else:
        print("Nadie termino la carrera (verifica velocidades > 0).")

    print("\n--- Última repetición ---")
    print(f"{'Bebe':<10} {'Vel(c/s)':<12} {'TD(seg)':<12} {'Tiempo(seg)':<12}")
    for nombre, vel, td, tiempo in ultimo_resultado['bebes']:
        print(f"{nombre:<10} {vel:<12.3f} {td:<12.3f} {tiempo:<12.3f}")
    if ultimo_resultado['ganador']:
        print(f"Ganador: {ultimo_resultado['ganador']}\nTiempo del ganador: {ultimo_resultado['mejor_tiempo']:.3f} seg")
    else:
        print("Nadie termino la carrera (verifica velocidades > 0).")

if __name__ == "__main__":
    main()
