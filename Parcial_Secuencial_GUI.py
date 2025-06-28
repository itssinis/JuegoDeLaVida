"""
Juego de la Vida de Conway

1. Célula Viva:
    • Si tiene menos de dos vecinos vivos, muere por "soledad".
    • Si tiene dos o tres vecinos vivos, sobrevive a la siguiente generación.
    • Si tiene más de tres vecinos vivos, muere por "sobrepoblación".

2. Célula Muerta:
    • Si tiene exactamente tres vecinos vivos, nace y se convierte en una célula viva."""

import random
import time
import tkinter as tk


VIVA = 1
MUERTA = 0

def crear_matriz(filas, columnas):
    
    matriz= [[MUERTA for _ in range(columnas)] for _ in range(filas)] #se crea una matriz de 0 de tamaño filasxcolumnas
    fila_aleatoria = random.randint(0, filas - 1)
    fila_aleatoria = random.randint(0, filas - 1)
    columna_aleatoria = random.randint(0, columnas - 1)
    matriz[fila_aleatoria][columna_aleatoria] = VIVA #en una fila y columna aleatoria de la matriz creada se pondrá la primera celula viva

    return matriz

def imprimir_matriz(matriz):
    
    for fila in matriz:
        print(' '.join('O' if celula == VIVA else '.' for celula in fila)) #se imprime la matriz, "O" para las celulas vivas y "." para las muertas
    print()


def vecinos_validos(matriz, fila, columna, historial_vivas):
    
    vecinos = [(fila - 1, columna), (fila + 1, columna), (fila, columna - 1), (fila, columna + 1), (fila-1,columna-1), (fila-1, columna +1), (fila+1, columna-1), (fila+1, columna+1)] #posiciones de las celulas que pueden ser vecinas de la viva 
    
    return [(f,c) for f,c in vecinos
            if 0 <= f < len(matriz) and 0 <= c < len(matriz[0]) and matriz[f][c] == MUERTA and historial_vivas[f][c] == 0 ] #se retornan los vecinos en donde se pueden crear una nueva celula, teniendo en cuenta que no haya una viva y que tampoco haya estado viva anteriormente

def vecinos_vivos(matriz, fila, columna):
    
    vecinos = [(fila - 1, columna), (fila + 1, columna), (fila, columna - 1), (fila, columna + 1), (fila-1,columna-1), (fila-1, columna +1), (fila+1, columna-1), (fila+1, columna+1)] #vecinos de la celula
    
    return sum(1 for f,c in vecinos if 0 <= f < len(matriz) and 0 <= c < len(matriz[0]) and matriz[f][c] == VIVA) #cantidad de vecinos vivos que tiene una celula


def contar_vivas(matriz):
    return sum(celula == VIVA for fila in matriz for celula in fila) #cantidad de celulas vivas en toda la matriz

def agregar_celula_viva(matriz, historial_vivas):

    matriz_temporal = [fila.copy() for fila in matriz] 

    for i in range(len(matriz)): 
        for j in range(len(matriz[0])):
            if matriz[i][j] == VIVA:
                vecinos = vecinos_validos(matriz, i, j, historial_vivas)
                print(f"Celula viva en ({i}, {j}) tiene {len(vecinos)} vecinos validos")
                if vecinos:
                    nueva_fila, nueva_columna = random.choice(vecinos)
                    print(f"Agregando nueva célula viva en ({nueva_fila}, {nueva_columna})")
                    matriz_temporal[nueva_fila][nueva_columna] = VIVA #se hace el cambio en la matriz temporal para que guarde las nuevas celulas que se crearon
                    historial_vivas[nueva_fila][nueva_columna] = 1 #se marca en el historial como viva
    
    for i in range(len(matriz)):
        for j in range(len(matriz[0])):
            matriz[i][j] = matriz_temporal[i][j] #se actualiza la matriz original con los cambios hechos en la temporal


def crear_historial(matriz):
    return [fila.copy() for fila in matriz] 

def actualizar_historial(matriz, historial_vivas):

    for i in range(len(matriz)):
        for j in range(len(matriz[0])):
            if matriz[i][j] == VIVA:
                historial_vivas[i][j] = 1 #cambia el estado de la celula en el historial


def juego(matriz, historial_vivas):

    nueva_matriz = crear_historial(matriz)
    
    if contar_vivas(matriz) > 3: #se aplican las reglas del juego únicamente si hay más de 3 células vivas
        for i in range(len(matriz)):
            for j in range(len(matriz[0])):
                vecinos = vecinos_vivos(matriz, i, j)
                if matriz[i][j] == VIVA:
                    if vecinos < 2 or vecinos > 3:
                        nueva_matriz[i][j] = MUERTA 
                    
                elif matriz[i][j] == MUERTA:
                    if vecinos == 3 and historial_vivas[i][j] == 1:
                        nueva_matriz[i][j] = VIVA  

    
    for i in range(len(matriz)):
        for j in range(len(matriz[0])):
            matriz[i][j] = nueva_matriz[i][j] #en caso de que hayan menos células, no se aplican las reglas y la matriz queda igual

    agregar_celula_viva(matriz, historial_vivas) #agrega las nuevas células

    actualizar_historial(matriz, historial_vivas)
    print("Celulas vivas:", contar_vivas(matriz)) #muestra cuantas células hay vivas

def main_secuencial():
    def ejecutar_juego():

        texto_salida.delete(1.0, tk.END) #se limpia el área de texto primero por si se ejecutó un juego anteriormente en la ventana
        
        try:
            num_matriz = int(entry_matriz.get())
            generacion = int(entry_generaciones.get())
        except ValueError:
            label_resultado.config(text="Introduzca los valores")
            return
        
        matriz = crear_matriz(num_matriz, num_matriz)
        historial_vivas = crear_historial(matriz)

        mostrar_matriz(matriz, "Matriz inicial:")

        actualizar_historial(matriz, historial_vivas)
        
        tiempo_inicio = time.time() #se empieza a contar el tiempo de ejecución 
        
        for gen in range(generacion):
            juego(matriz, historial_vivas)
            mostrar_matriz(matriz, f"Generación {gen + 1}:")
        
        tiempo_fin = time.time() #se termina de contar el tiempo de ejecución
        tiempo_ejecucion = tiempo_fin - tiempo_inicio
        
        texto_salida.insert(tk.END, f"Células vivas finales: {contar_vivas(matriz)}\n") #muestra cuantas células quedaron vivas al final
        
        label_resultado.config(text=f"Fin del juego. Tiempo: {tiempo_ejecucion:.4f} segundos") #muestra un mensaje final y el tiempo que demoró
        
        texto_salida.see(tk.END) #se desplaza automáticamente al final del texto

    def mostrar_matriz(matriz, titulo):

        texto_salida.insert(tk.END, f"{titulo}\n")
        for fila in matriz:
            texto_fila = ' '.join('O' if celula == VIVA else '.' for celula in fila)
            texto_salida.insert(tk.END, texto_fila + "\n")
        texto_salida.insert(tk.END, "\n")
        texto_salida.see(tk.END)  
    
    ventana = tk.Tk() #crea la ventana principal
    ventana.title("Juego de la Vida de Conway (Secuencial)")
    ventana.geometry("600x600") #tamaño inicial de la ventana 

    #dividimos la ventana en tres para separar la principal, la configuración y el resultado de cada generación del juego:
    frame_principal = tk.Frame(ventana, padx=10, pady=10)
    frame_principal.pack(fill=tk.BOTH, expand=True)

    frame_config = tk.LabelFrame(frame_principal, text="Configuración", padx=10, pady=10)
    frame_config.pack(fill=tk.X, padx=5, pady=5)

    frame_resultados = tk.LabelFrame(frame_principal, text="Resultados", padx=10, pady=10)
    frame_resultados.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    #etiquetas para los campos de entrada
    tk.Label(frame_config, text="Tamaño de la matriz (NxN):").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
    entry_matriz = tk.Entry(frame_config)
    entry_matriz.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(frame_config, text="Número de generaciones:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
    entry_generaciones = tk.Entry(frame_config)
    entry_generaciones.grid(row=1, column=1, padx=5, pady=5)

    #botón para ejecutar el juego
    tk.Button(frame_config, text="Ejecutar", command=ejecutar_juego).grid(row=2, column=1, columnspan=5, pady=10)

    #scrolls para tener una mejor vista de la matriz
    scrollbar_y = tk.Scrollbar(frame_resultados)
    scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
    
    scrollbar_x = tk.Scrollbar(frame_resultados, orient=tk.HORIZONTAL)
    scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
    
    texto_salida = tk.Text(frame_resultados, height=20, width=50, 
                          yscrollcommand=scrollbar_y.set,
                          xscrollcommand=scrollbar_x.set,
                          wrap=tk.NONE) 
    texto_salida.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    scrollbar_y.config(command=texto_salida.yview)
    scrollbar_x.config(command=texto_salida.xview)

    #etiqueta para saber el resultado
    label_resultado = tk.Label(frame_principal, text="", font=("Arial", 10, "bold"))
    label_resultado.pack(pady=5)

    ventana.mainloop()

if __name__ == "__main__":
    main_secuencial()
