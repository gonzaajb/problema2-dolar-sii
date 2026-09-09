import numpy as np
import os

# esto es para que el csv se encuentre sin importar desde donde ejecute el script
RUTA_CSV = os.path.join(os.path.dirname(__file__), "..", "data", "dolar_observado_sii_2022_2025.csv")

MESES = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
ANIOS = [2022, 2023, 2024, 2025]


def cargar_precios(ruta=RUTA_CSV):
    # con genfromtxt cargamos directo las columnas del csv (columna 0 es el mes, por eso parto en la 1)
    datos = np.genfromtxt(ruta, delimiter=",", skip_header=1, usecols=(1, 2, 3, 4))
    return datos


def precios_como_lista_plana(matriz_precios):
    # la matriz viene como 12 filas (meses) y 4 columnas (Años)
    # aca la paso a una sola lista larga en orden cronologico, para poder graficarla como serie de tiempo
    n_meses, n_anios = matriz_precios.shape

    valores = np.zeros(n_meses * n_anios)
    etiquetas = []

    indice = 0
    for j in range(n_anios):
        for i in range(n_meses):
            valores[indice] = matriz_precios[i, j]
            etiquetas.append(MESES[i] + " " + str(ANIOS[j]))
            indice = indice + 1

    return valores, etiquetas


if __name__ == "__main__":
    precios = cargar_precios()
    print("matriz de precios (filas = meses, columnas = anios):")
    print(precios)

    serie, etiquetas = precios_como_lista_plana(precios)
    print("")
    print("serie completa ordenada por fecha:")
    for e, v in zip(etiquetas, serie):
        print(e, "->", v)
