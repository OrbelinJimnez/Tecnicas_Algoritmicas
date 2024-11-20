import random
import matplotlib.pyplot as plt
import numpy as np
import time

# Función para verificar si un número puede ser colocado en la celda
def es_valido(tablero, fila, col, num):
    # Verificar la fila y columna
    for i in range(9):
        if tablero[fila][i] == num or tablero[i][col] == num:
            return False

    # Verificar la subcuadrícula 3x3
    start_row, start_col = 3 * (fila // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if tablero[start_row + i][start_col + j] == num:
                return False
    return True

# Función para resolver el Sudoku usando programación dinámica con memoización
def resolver_sudoku_con_memoizacion(tablero, tablero_original, memo={}):
    key = tuple(tuple(row) for row in tablero)  # Representación única del tablero actual

    # Verificar si ya hemos resuelto este tablero
    if key in memo:
        return memo[key]

    for fila in range(9):
        for col in range(9):
            if tablero[fila][col] == 0:
                for num in range(1, 10):
                    if es_valido(tablero, fila, col, num):
                        tablero[fila][col] = num
                        if resolver_sudoku_con_memoizacion(tablero, tablero_original, memo):
                            memo[key] = True  # Guardar resultado exitoso en el memo
                            return True
                        tablero[fila][col] = 0  # Retroceso

                memo[key] = False  # Guardar resultado de fallo en el memo
                return False
    memo[key] = True
    return True

# Función para generar un tablero de Sudoku completo
def llenar_sudoku(tablero):
    for i in range(9):
        for j in range(9):
            if tablero[i][j] == 0:
                nums = list(range(1, 10))
                random.shuffle(nums)
                for num in nums:
                    if es_valido(tablero, i, j, num):
                        tablero[i][j] = num
                        if llenar_sudoku(tablero):
                            return True
                        tablero[i][j] = 0
                return False
    return True

# Función para quitar celdas y crear un Sudoku con espacios vacíos
def quitar_celdas(tablero, vacias):
    celdas_quitadas = 0
    while celdas_quitadas < vacias:
        fila, col = random.randint(0, 8), random.randint(0, 8)
        if tablero[fila][col] != 0:
            tablero[fila][col] = 0
            celdas_quitadas += 1
    return tablero

# Generar un Sudoku con celdas vacías
def generar_sudoku(vacias=40):
    tablero = [[0] * 9 for _ in range(9)]
    llenar_sudoku(tablero)
    tablero = quitar_celdas(tablero, vacias)
    return tablero

# Calcular el tiempo de resolución
def calcular_tiempo_resolucion(tablero):
    tablero_copia = [fila[:] for fila in tablero]
    inicio = time.time()
    resolver_sudoku_con_memoizacion(tablero_copia)
    fin = time.time()
    return fin - inicio

# Graficar el Sudoku
def graficar_sudoku(tablero, tablero_original, titulo="Sudoku"):
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.matshow(np.ones((9, 9)), cmap="gray_r")

    for i in range(10):
        lw = 2 if i % 3 == 0 else 0.5
        ax.plot([i, i], [0, 9], 'k', linewidth=lw)
        ax.plot([0, 9], [i, i], 'k', linewidth=lw)

    for i in range(9):
        for j in range(9):
            if tablero[i][j] != 0:
                color = "blue" if tablero_original[i][j] == 0 else "black"  # Azul para las celdas resueltas
                ax.text(j + 0.5, i + 0.5, str(tablero[i][j]),
                        va='center', ha='center', fontsize=14, color=color)

    ax.axis("off")
    ax.set_title(titulo)
    plt.show()

# Generar y graficar el Sudoku original
tablero_sudoku = generar_sudoku(vacias=40)
print("Tablero inicial:")
graficar_sudoku(tablero_sudoku, tablero_sudoku, titulo="Sudoku Original")

# Resolver el Sudoku y calcular el tiempo de resolución
tablero_resuelto = [fila[:] for fila in tablero_sudoku]
inicio = time.time()
resolver_sudoku_con_memoizacion(tablero_resuelto, tablero_sudoku)
fin = time.time()
tiempo_resolucion = fin - inicio
print(f"Tiempo de resolución: {tiempo_resolucion:.4f} segundos")

# Graficar el Sudoku resuelto
print("Tablero resuelto:")
graficar_sudoku(tablero_resuelto, tablero_sudoku, titulo="Sudoku Resuelto")
