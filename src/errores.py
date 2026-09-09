import numpy as np
from cargar_datos import cargar_precios, precios_como_lista_plana, MESES, ANIOS


def redondear_cifras_significativas(valor, cifras):
    # esta funcion redondea a "cifras" cifras significativas, no es lo mismo que redondear decimales
    # por ejemplo con 2 cifras: 874.67 -> 870.0

    # caso en que me pasan un arreglo completo de numpy (para no tener que llamar la funcion uno por uno)
    if isinstance(valor, np.ndarray):
        resultados = []
        for numero in valor:
            if numero == 0:
                resultados.append(0)
            else:
                orden = np.floor(np.log10(abs(numero)))
                factor = 10 ** (orden - cifras + 1)
                resultado = np.round(numero / factor) * factor
                resultados.append(resultado)
        return np.array(resultados)

    # caso normal, un solo numero
    if valor == 0:
        return 0

    orden = np.floor(np.log10(abs(valor)))
    factor = 10 ** (orden - cifras + 1)
    resultado = np.round(valor / factor) * factor

    return resultado


def error_absoluto(valor_real, valor_aprox):
    # Ea = |valor real - valor aproximado|
    resultado = abs(valor_real - valor_aprox)
    return resultado


def error_relativo(valor_real, ea):
    # Er en porcentaje, por eso el *100
    resultado = (ea / abs(valor_real)) * 100
    return resultado


def propagar_suma_resta(errores_absolutos):
    # regla vista en clases: al sumar o restar numeros, los errores absolutos se suman
    resultado = 0
    for error in errores_absolutos:
        resultado = resultado + abs(error)
    return resultado


def propagar_mult_div(errores_relativos):
    # regla vista en clases: al multiplicar o dividir, los errores relativos se suman
    resultado = 0
    for error in errores_relativos:
        resultado = resultado + abs(error)
    return resultado


def analisis_A1(cifras=2):
    precios = cargar_precios()
    serie, etiquetas = precios_como_lista_plana(precios)

    aproximados = []
    for precio in serie:
        aprox = redondear_cifras_significativas(precio, cifras)
        aproximados.append(aprox)

    ea = []
    er = []
    for i in range(len(serie)):
        ea_i = error_absoluto(serie[i], aproximados[i])
        er_i = error_relativo(serie[i], ea_i)
        ea.append(ea_i)
        er.append(er_i)

    # con argmax busco en que mes el error relativo fue el peor de todos
    indice_peor = np.argmax(er)

    print("--- A1: error de representacion ---")
    for i in range(len(etiquetas)):
        print(etiquetas[i], "  real=", round(serie[i], 2), "  aprox=", round(aproximados[i], 1),"  Ea=", round(ea[i], 2), "  Er=", round(er[i], 2), "%")

    print("")
    print("el mes con mayor error relativo fue:", etiquetas[indice_peor],"(real=", serie[indice_peor], ", aprox=", aproximados[indice_peor],", Er=", round(er[indice_peor], 2), "%)")

    return serie, np.array(aproximados), np.array(ea), np.array(er), etiquetas


# ---------------------------------------------------------------------
# A2. si compro dolares en un mes y vendo en otro, cuanto error arrastro
# ---------------------------------------------------------------------
def analisis_A2(precio_compra_real, precio_venta_real, monto=1_000_000, cifras=2):

    # primero redondeo los dos precios, como si solo tuviera esa info aproximada
    p_compra = redondear_cifras_significativas(precio_compra_real, cifras)
    p_venta = redondear_cifras_significativas(precio_venta_real, cifras)

    # error de cada precio por separado
    ea_compra = error_absoluto(precio_compra_real, p_compra)
    er_compra = error_relativo(precio_compra_real, ea_compra)

    ea_venta = error_absoluto(precio_venta_real, p_venta)
    er_venta = error_relativo(precio_venta_real, ea_venta)

    # cuantos dolares me alcanzan para comprar con el monto
    usd = monto / p_compra

    # es una division, entonces el error relativo se propaga sumando (el 0 es porque el monto en pesos no tiene error)
    er_usd = propagar_mult_div([0, er_compra])

    # ahora vendo esos dolares al precio de venta
    pesos_final = usd * p_venta

    # otra multiplicacion/division, se vuelve a sumar el error relativo
    er_pesos_final = propagar_mult_div([er_usd, er_venta])
    ea_pesos_final = (er_pesos_final / 100) * pesos_final

    ganancia = pesos_final - monto

    # esto es una resta, entonces toca sumar los errores absolutos (el monto inicial no tiene error, por eso el 0)
    ea_ganancia = propagar_suma_resta([ea_pesos_final, 0])

    if ganancia != 0:
        er_ganancia = error_relativo(abs(ganancia), ea_ganancia)
    else:
        er_ganancia = np.inf

    print("--- A2: compra y venta ---")
    print("compra a", round(p_compra, 1), "(real", precio_compra_real, ") Er=", round(er_compra, 2), "%")
    print("venta a", round(p_venta, 1), "(real", precio_venta_real, ") Er=", round(er_venta, 2), "%")
    print("dolares comprados:", round(usd, 2))
    print("pesos finales:", round(pesos_final, 2), "+/-", round(ea_pesos_final, 2))
    print("ganancia:", round(ganancia, 2), "+/-", round(ea_ganancia, 2), " (Er=", round(er_ganancia, 2), "%)")

    return ganancia, ea_ganancia, er_ganancia


def analisis_A3(precio_inicial_real=875.66, precio_final_real=874.67, cifras=3):

    p_inicial = redondear_cifras_significativas(precio_inicial_real, cifras)
    p_final = redondear_cifras_significativas(precio_final_real, cifras)

    ea_inicial = error_absoluto(precio_inicial_real, p_inicial)
    ea_final = error_absoluto(precio_final_real, p_final)

    delta_p = p_final - p_inicial

    ea_delta = propagar_suma_resta([ea_inicial, ea_final])

    if delta_p != 0:
        er_delta = error_relativo(abs(delta_p), ea_delta)
    else:
        er_delta = np.inf

    print("--- A3: cancelacion ---")
    print("P_inicial (dic 2022): real=", precio_inicial_real, " aprox=", round(p_inicial, 1), " Ea=", round(ea_inicial, 3))
    print("P_final (dic 2023): real=", precio_final_real, " aprox=", round(p_final, 1), " Ea=", round(ea_final, 3))
    print("Delta P =", round(delta_p, 2), "+/-", round(ea_delta, 3), " (Er=", round(er_delta, 1), "%)")

    # aca esta la idea central de la cancelacion catastrofica: si el error es mas grande que el propio resultado
    # entonces en realidad no se puede confiar en el signo ni en el valor de la diferencia
    if abs(delta_p) <= ea_delta:
        print("el error es igual o mayor que Delta P, no se puede asegurar si el dolar subio o bajo")
    else:
        print("Delta P es mas grande que el error, entonces el resultado si es confiable")

    return delta_p, ea_delta, er_delta


if __name__ == "__main__":
    analisis_A1()
    print("")
    analisis_A2(precio_compra_real=798.26, precio_venta_real=1000.76)
    print("")
    analisis_A3()
