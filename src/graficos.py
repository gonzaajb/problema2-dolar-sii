import numpy as np
import matplotlib.pyplot as plt
import os

#------------------------------------------------------------------------------------
from cargar_datos import cargar_precios, precios_como_lista_plana, MESES, ANIOS
from errores import (redondear_cifras_significativas, error_absoluto, error_relativo, propagar_suma_resta)
from anualidad import analisis_A4, analisis_A5
from punto_flotante import analisis_B2
from errores import analisis_A2, analisis_A3
#------------------------------------------------------------------------------------

CARPETA_GRAFICOS = os.path.join(os.path.dirname(__file__), "..", "graficos")
os.makedirs(CARPETA_GRAFICOS, exist_ok=True)


def guardar(nombre):
    # funcion chica solo para no repetir estas 3 lineas en cada grafico
    ruta = os.path.join(CARPETA_GRAFICOS, nombre)
    plt.savefig(ruta, dpi=150, bbox_inches="tight")
    plt.close()
    print("grafico guardado en:", ruta)


def grafico_1_serie_mensual():
    precios = cargar_precios()
    serie, etiquetas = precios_como_lista_plana(precios)
    x = np.arange(len(serie))

    plt.figure(figsize=(12, 5))
    plt.plot(x, serie, color="tab:blue", linewidth=1.5)
    plt.xticks(x[::3], etiquetas[::3], rotation=60, ha="right", fontsize=7)  # de 3 en 3 para que no se amontonen las etiquetas
    plt.ylabel("Dolar observado (CLP)")
    plt.title("Dolar observado SII - promedio mensual 2022-2025")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    guardar("1_serie_mensual.png")
#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
def grafico_2_variacion_mes_a_mes():
    precios = cargar_precios()
    serie, etiquetas = precios_como_lista_plana(precios)

    aproximados = redondear_cifras_significativas(serie, 2)
    ea = error_absoluto(serie, aproximados)

    delta_p = np.diff(aproximados)          # diferencia entre un mes y el siguiente

    # el error de una resta se suma (mismo criterio que en A3), lo hago mes a mes con un for
    ea_delta = []
    for i in range(len(delta_p)):
        ea_delta.append(ea[i] + ea[i + 1])
    ea_delta = np.array(ea_delta)

    x = np.arange(len(delta_p))

    # pinto de rojo los meses donde el error es mas grande (o igual) que la propia variacion
    colores = []
    for i in range(len(delta_p)):
        if abs(delta_p[i]) <= ea_delta[i]:
            colores.append("tab:red")
        else:
            colores.append("tab:green")

    plt.figure(figsize=(12, 5))
    plt.bar(x, delta_p, yerr=ea_delta, color=colores, alpha=0.8, capsize=2)
    plt.axhline(0, color="black", linewidth=0.8)
    plt.xticks(x[::3], etiquetas[1::3], rotation=60, ha="right", fontsize=7)
    plt.ylabel("Delta P (CLP)")
    plt.title("Variacion mes a mes (rojo = el error domina el resultado)")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    guardar("2_Variacion_MesAMes.png")
#----------------------------------------------------------------------------------


#-----------------------------------------------------------------------------------
def grafico_3_error_representacion():
    precios = cargar_precios()
    serie, etiquetas = precios_como_lista_plana(precios)

    aproximados = redondear_cifras_significativas(serie, 2)
    ea = error_absoluto(serie, aproximados)
    er = error_relativo(serie, ea)

    x = np.arange(len(serie))
    plt.figure(figsize=(12, 5))
    plt.bar(x, er, color="tab:orange")
    plt.xticks(x[::3], etiquetas[::3], rotation=60, ha="right", fontsize=7)
    plt.ylabel("Error relativo (%)")
    plt.title("Error de representacion por mes (2 cifras significativas)")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    guardar("3_error_representacion.png")
#-----------------------------------------------------------------------------

#----------------------------------------------------------------------------------
def grafico_4_rentabilidad():
    precios = cargar_precios()
    serie, etiquetas = precios_como_lista_plana(precios)
    monto = 1_000_000

    # busco el mes mas barato de todo el periodo, para simular que compro justo ahi
    indice_min = np.argmin(serie)
    p_compra_real = serie[indice_min]
    p_compra = redondear_cifras_significativas(p_compra_real, 2)
    ea_compra = error_absoluto(p_compra_real, p_compra)
    er_compra = error_relativo(p_compra_real, ea_compra)
    usd = monto / p_compra

    aproximados = redondear_cifras_significativas(serie, 2)
    ea_serie = error_absoluto(serie, aproximados)
    er_serie = error_relativo(serie, ea_serie)

    # con esos dolares, voy calculando cuanto tendria si vendiera en cada mes posterior
    pesos_final = usd * aproximados
    er_pesos_final = er_compra + er_serie
    ea_pesos_final = (er_pesos_final / 100) * pesos_final

    rentabilidad = (pesos_final - monto) / monto * 100
    ea_rentabilidad = (ea_pesos_final / monto) * 100

    # esto solo tiene sentido para los meses despues de haber comprado
    x = np.arange(len(serie))
    mascara = x > indice_min

    plt.figure(figsize=(12, 5))
    plt.errorbar(x[mascara], rentabilidad[mascara], yerr=ea_rentabilidad[mascara],fmt="o-", color="tab:green", ecolor="tab:gray", elinewidth=1, capsize=2, markersize=3)
    plt.axhline(0, color="black", linewidth=0.8)
    plt.xticks(x[mascara][::3], [etiquetas[i] for i in x[mascara][::3]], rotation=60, ha="right", fontsize=7)
    plt.ylabel("Rentabilidad (%)")
    plt.title("Rentabilidad de comprar en " + etiquetas[indice_min] + " y vender despues")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    guardar("4_rentabilidad.png")
#------------------------------------------------------------------------

def grafico_5_deriva_flotante():
    montos, deriva, etiquetas = analisis_B2()
    x = np.arange(len(deriva))

    plt.figure(figsize=(12, 5))
    plt.plot(x, deriva, marker="o", markersize=3, color="tab:purple")
    plt.axhline(0, color="black", linewidth=0.8)
    plt.xticks(x[::3], etiquetas[::3], rotation=60, ha="right", fontsize=7)
    plt.ylabel("Deriva respecto al monto inicial (CLP)")
    plt.title("Deriva acumulada: ida y vuelta pesos -> dolares -> pesos")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    guardar("5_deriva_flotante.png")


def generar_tabla_evaluacion_error():
    precios = cargar_precios()
    serie, etiquetas = precios_como_lista_plana(precios)
    aproximados = redondear_cifras_significativas(serie, 2)
    ea = error_absoluto(serie, aproximados)
    er = error_relativo(serie, ea)

    resultados_a4 = analisis_A4()
    ruta = os.path.join(os.path.dirname(__file__), "..", "graficos", "evaluacion_error.csv")
    # armo un csv chico con todos los errores calculados, mensuales y anuales juntos
    f = open(ruta, "w", encoding="utf-8")
    f.write("tipo,etiqueta,valor_real,valor_aprox,error_absoluto,error_relativo_pct\n")
    for i in range(len(etiquetas)):
        etq = etiquetas[i]
        real = serie[i]
        aprox = aproximados[i]
        e_a = ea[i]
        e_r = er[i]
        f.write("mensual," + etq + "," + str(round(real, 2)) + "," + str(round(aprox, 1)) + "," +
                str(round(e_a, 3)) + "," + str(round(e_r, 3)) + "\n")

    for r in resultados_a4:
        f.write("anual," + str(r["anio"]) + ",,," + str(round(r["ea"], 3)) + "," + str(round(r["er"], 3)) + "\n")

    # agrego los pares de puntos evaluados en A2 (compra-venta) y A3 (cancelacion),
    # que el enunciado pide explicitamente en la tabla de evaluacion de error
    ganancia, ea_ganancia, er_ganancia = analisis_A2(precio_compra_real=798.26, precio_venta_real=1000.76)
    f.write("par,A2_compra-venta," + str(round(ganancia, 2)) + ",," +
            str(round(ea_ganancia, 3)) + "," + str(round(er_ganancia, 3)) + "\n")

    delta_p, ea_delta, er_delta = analisis_A3()
    f.write("par,A3_cancelacion_dic22-dic23," + str(round(delta_p, 2)) + ",," +
            str(round(ea_delta, 3)) + "," + str(round(er_delta, 3)) + "\n")

    f.close()

    print("tabla de evaluacion de error guardada en:", ruta)


if __name__ == "__main__":
    grafico_1_serie_mensual()
    grafico_2_variacion_mes_a_mes()
    grafico_3_error_representacion()
    grafico_4_rentabilidad()
    grafico_5_deriva_flotante()
    generar_tabla_evaluacion_error()