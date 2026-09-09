import numpy as np
from cargar_datos import cargar_precios, MESES, ANIOS
from errores import (redondear_cifras_significativas, error_absoluto, error_relativo, propagar_suma_resta, propagar_mult_div)


# ---------------------------------------------------------------------
# A4. cuanto vario el dolar entre enero y diciembre, para cada anio
# ---------------------------------------------------------------------
def analisis_A4(cifras=3):
    precios = cargar_precios()
    resultados = []

    for j, anio in enumerate(ANIOS):
        enero_real = precios[0, j]
        diciembre_real = precios[11, j]
        enero_aprox = redondear_cifras_significativas(enero_real, cifras)
        diciembre_aprox = redondear_cifras_significativas(diciembre_real, cifras)
        ea_enero = error_absoluto(enero_real, enero_aprox)
        ea_diciembre = error_absoluto(diciembre_real, diciembre_aprox)
        variacion = diciembre_aprox - enero_aprox


        # es una resta, entonces se suman los errores absolutos
        ea_variacion = propagar_suma_resta([ea_enero, ea_diciembre])

        if variacion != 0:
            er_variacion = error_relativo(np.abs(variacion), ea_variacion)
        else:
            er_variacion = np.inf

        resultados.append({
            "anio": anio,
            "enero": enero_real,
            "diciembre": diciembre_real,
            "variacion": variacion,
            "ea": ea_variacion,
            "er": er_variacion,
        })

    # ordeno de mas confiable (Er% mas chico) a menos confiable
    resultados_ordenados = sorted(resultados, key=lambda r: r["er"])

    print("--- A4: variacion enero -> diciembre por anio ---")
    for r in resultados_ordenados:
        print(r["anio"], ": enero=", round(r["enero"], 2), " diciembre=", round(r["diciembre"], 2),"  variacion=", round(r["variacion"], 1), " +/-", round(r["ea"], 2)," (Er=", round(r["er"], 1), "%)")

    print("")
    print("orden de mas confiable a menos confiable (segun Er%):", [r["anio"] for r in resultados_ordenados])

    return resultados_ordenados


def analisis_A5(monto=1_000_000, cifras=2):
    precios = cargar_precios()

    # arme las etiquetas y la serie a mano, en el mismo orden (mes por mes, anio por anio)
    etiquetas = []
    for j in range(len(ANIOS)):
        for i in range(len(MESES)):
            etiquetas.append(MESES[i] + " " + str(ANIOS[j]))

    serie = []
    for j in range(len(ANIOS)):
        for i in range(len(MESES)):
            serie.append(precios[i, j])
    serie = np.array(serie)

    # el mes mas barato es donde compro, el mas caro es donde vendo
    indice_min = np.argmin(serie)
    indice_max = np.argmax(serie)

    precio_compra_real = serie[indice_min]
    precio_venta_real = serie[indice_max]

    p_compra = redondear_cifras_significativas(precio_compra_real, cifras)
    p_venta = redondear_cifras_significativas(precio_venta_real, cifras)

    ea_compra = error_absoluto(precio_compra_real, p_compra)
    er_compra = error_relativo(precio_compra_real, ea_compra)
    ea_venta = error_absoluto(precio_venta_real, p_venta)
    er_venta = error_relativo(precio_venta_real, ea_venta)

    usd = monto / p_compra
    er_usd = propagar_mult_div([0, er_compra])

    pesos_final = usd * p_venta
    er_pesos_final = propagar_mult_div([er_usd, er_venta])
    ea_pesos_final = (er_pesos_final / 100) * pesos_final

    ganancia = pesos_final - monto
    ea_ganancia = propagar_suma_resta([ea_pesos_final, 0])

    rentabilidad = (ganancia / monto) * 100
    ea_rentabilidad = (ea_ganancia / monto) * 100

    print("--- A5: mejor compra y mejor venta del periodo completo ---")
    print("mes mas barato:", etiquetas[indice_min], "->", round(precio_compra_real, 2), "(aprox", round(p_compra, 1), ")")
    print("mes mas caro:  ", etiquetas[indice_max], "->", round(precio_venta_real, 2), "(aprox", round(p_venta, 1), ")")
    print("ganancia:", round(ganancia, 2), "+/-", round(ea_ganancia, 2))
    print("rentabilidad:", round(rentabilidad, 2), "% +/-", round(ea_rentabilidad, 2), "%")

    # si el error es mas chico que la rentabilidad, quiere decir que la ganancia es real y no puro ruido numerico
    if ea_rentabilidad < rentabilidad:
        print("la ganancia es bastante mas grande que el error, entonces la conclusion es solida")
    else:
        print("el error es del mismo orden que la rentabilidad, no se puede confiar del todo en el resultado")

    return etiquetas[indice_min], etiquetas[indice_max], ganancia, ea_ganancia, rentabilidad, ea_rentabilidad


if __name__ == "__main__":
    analisis_A4()
    print("")
    analisis_A5()
