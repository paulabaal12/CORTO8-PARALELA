#include <stdio.h>
#include <string.h>
#include <float.h>
#include <omp.h>

typedef struct {
    char nombre[64];
    double velocidad;
    double td;
} Bebe;

// Función para simular el tiempo que tarda un bebé
double simular_tiempo_bebe(const Bebe* b, const int* pista, int n_celdas) {
    if (b->velocidad <= 0.0) return DBL_MAX;

    double t = 0.0;

    // Paraleliza el recorrido de la pista por celdas
    #pragma omp parallel for reduction(+:t)
    for (int i = 0; i < n_celdas; ++i) {
        double t_celda = 1.0 / b->velocidad;
        if (pista[i] == 1) t_celda += b->td;
        t += t_celda;
    }
    return t;
}

int main(void) {
    const int REPETICIONES = 100000;
    double tiempos[REPETICIONES]; // Arreglo para guardar tiempos de ejecución

    // Datos de los bebés y la pista
    Bebe bebes[] = {
        {"Ana", 0.5, 2.0},
        {"Luis", 0.7, 1.0},
        {"Mia", 0.6, 1.5}
    };
    const int num_bebes = sizeof(bebes) / sizeof(bebes[0]);

    int pista[] = {0, 0, 0, 1, 0, 0, 1};
    const int n_celdas = sizeof(pista) / sizeof(pista[0]);

    printf("Inicio de la carrera de bebes con paralelismo anidado\n");


    //omp_set_nested(1);

    double tiempo_total_inicio = omp_get_wtime(); // Inicio del tiempo total

    // REPETICIONES
    #pragma omp parallel for
    for (int rep = 0; rep < REPETICIONES; rep++) {
        double inicio = omp_get_wtime();

        double mejor_tiempo = DBL_MAX;
        char ganador[64] = "";

        // Simula los bebés en paralelo usando sections (anidado)
        #pragma omp parallel sections
        {
            #pragma omp section
            {
                double tiempo = simular_tiempo_bebe(&bebes[0], pista, n_celdas);
                #pragma omp critical
                {
                    if (tiempo < mejor_tiempo) {
                        mejor_tiempo = tiempo;
                        snprintf(ganador, sizeof(ganador), "%s", bebes[0].nombre);
                    }
                }
            }
            #pragma omp section
            {
                double tiempo = simular_tiempo_bebe(&bebes[1], pista, n_celdas);
                #pragma omp critical
                {
                    if (tiempo < mejor_tiempo) {
                        mejor_tiempo = tiempo;
                        snprintf(ganador, sizeof(ganador), "%s", bebes[1].nombre);
                    }
                }
            }
            #pragma omp section
            {
                double tiempo = simular_tiempo_bebe(&bebes[2], pista, n_celdas);
                #pragma omp critical
                {
                    if (tiempo < mejor_tiempo) {
                        mejor_tiempo = tiempo;
                        snprintf(ganador, sizeof(ganador), "%s", bebes[2].nombre);
                    }
                }
            }
        } // fin parallel sections

        double fin = omp_get_wtime();
        double tiempo_ejecucion = fin - inicio;
        tiempos[rep] = tiempo_ejecucion;

        #pragma omp critical
        {
            printf("\n--- Repeticion %d ---\n", rep + 1);
            printf("Ganador: %s\nTiempo del ganador: %.3f seg\n", ganador, mejor_tiempo);
            printf("Tiempo de ejecucion de esta repeticion: %.6f segundos\n", tiempo_ejecucion);
        }
    }

    double tiempo_total_fin = omp_get_wtime();
    double tiempo_total = tiempo_total_fin - tiempo_total_inicio;

    // Mostrar resumen de tiempos individuales
    printf("\n===== RESUMEN DE TIEMPOS INDIVIDUALES =====\n");
    for (int i = 0; i < REPETICIONES; i++) {
        printf("Repeticion %d: %.6f segundos\n", i + 1, tiempos[i]);
    }

    printf("\nTiempo total para completar las %d repeticiones: %.6f segundos\n", REPETICIONES, tiempo_total);

    return 0;
}
