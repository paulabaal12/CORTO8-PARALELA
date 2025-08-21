#include <stdio.h>
#include <string.h>
#include <float.h>
#include <time.h> // Para medir tiempo

typedef struct {
    char   nombre[64];  
    double velocidad;   
    double td;          
} Bebe;

double simular_tiempo_bebe(const Bebe* b, const int* pista, int n_celdas) {
    if (b->velocidad <= 0.0) return DBL_MAX;
    double t = 0.0;
    for (int i = 0; i < n_celdas; ++i) {
        t += 1.0 / b->velocidad;   
        if (pista[i] == 1) {      
            t += b->td;
        }
    }
    return t;
}

int main(void) {
    const int REPETICIONES = 100000;
    double tiempos[REPETICIONES]; // Arreglo para guardar tiempos

    // Inicio del tiempo total de todas las repeticiones
    clock_t inicio_total = clock();

    for (int rep = 0; rep < REPETICIONES; rep++) {
        clock_t inicio = clock();

        Bebe bebes[] = {
            {"Ana",  0.5, 2.0},
            {"Luis", 0.7, 1.0},
            {"Mia",  0.6, 1.5}
        };
        const int num_bebes = (int)(sizeof(bebes) / sizeof(bebes[0]));

        int pista[] = {0, 0, 0, 1, 0, 0, 1};
        const int n_celdas = (int)(sizeof(pista) / sizeof(pista[0]));

        double mejor_tiempo = DBL_MAX;
        int idx_ganador = -1;

        printf("\n--- Repeticion %d ---\n", rep + 1);
        printf("Pista de %d celdas (0=nada, 1=juguete): ", n_celdas);
        for (int i = 0; i < n_celdas; ++i) printf("%d ", pista[i]);
        printf("\n\nResultados:\n");
        printf("%-10s %-12s %-12s %-12s\n", "Bebe", "Vel(c/s)", "TD(seg)", "Tiempo(seg)");

        for (int i = 0; i < num_bebes; ++i) {
            double tiempo = simular_tiempo_bebe(&bebes[i], pista, n_celdas);
            printf("%-10s %-12.3f %-12.3f %-12.3f\n",
                   bebes[i].nombre, bebes[i].velocidad, bebes[i].td, tiempo);

            if (tiempo < mejor_tiempo) {
                mejor_tiempo = tiempo;
                idx_ganador = i;
            }
        }

        if (idx_ganador >= 0) {
            printf("\nGanador: %s\nTiempo del ganador: %.3f seg\n",
                   bebes[idx_ganador].nombre, mejor_tiempo);
        } else {
            printf("\nNadie termino la carrera (verifica velocidades > 0).\n");
        }

        clock_t fin = clock();
        double tiempo_ejecucion = (double)(fin - inicio) / CLOCKS_PER_SEC;
        tiempos[rep] = tiempo_ejecucion; // Guardar tiempo de esta repetición
        printf("Tiempo de ejecucion de esta repeticion: %.6f segundos\n", tiempo_ejecucion);
    }

    // Fin del tiempo total de todas las repeticiones
    clock_t fin_total = clock();
    double tiempo_total = (double)(fin_total - inicio_total) / CLOCKS_PER_SEC;

    // Mostrar resumen de tiempos individuales
    printf("\n===== RESUMEN DE TIEMPOS INDIVIDUALES =====\n");
    for (int i = 0; i < REPETICIONES; i++) {
        printf("Repeticion %d: %.6f segundos\n", i + 1, tiempos[i]);
    }

    // Mostrar tiempo total de todas las repeticiones
    printf("\nTiempo total para completar las %d repeticiones: %.6f segundos\n", REPETICIONES, tiempo_total);

    return 0;
}
