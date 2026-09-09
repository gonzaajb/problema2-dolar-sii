import numpy as np
from cargar_datos import cargar_precios, precios_como_lista_plana
from errores import redondear_cifras_significativas, error_absoluto


def analisis_B1():
    valor = 1000.76
    aprox_3 = redondear_cifras_significativas(valor, 3)
    ea = error_absoluto(valor, aprox_3)

    print("--- B1: mantisa corta ---")
    print("1000.76 = 1.00076 x 10^3 (esa es la mantisa completa)")
    print("con solo 3 cifras significativas queda:", aprox_3, " (mantisa corta 1.00 x 10^3)")
    print("error de representacion Ea =", round(ea, 2))
    return aprox_3, ea


def analisis_B2(monto_inicial=1_000_000):
    precios = cargar_precios()
    serie, etiquetas = precios_como_lista_plana(precios)

    # aca voy guardando el monto despues de cada ciclo ida y vuelta
    montos = np.zeros(len(serie) + 1)
    montos[0] = monto_inicial

    for i in range(len(serie)):
        precio = serie[i]
        usd = montos[i] / precio            # paso los pesos a dolares
        pesos_recuperados = usd * precio    # y los vuelvo a pasar a pesos, al mismo precio
        montos[i + 1] = pesos_recuperados

    deriva = montos[1:] - monto_inicial

    print("--- B2: ida y vuelta pesos -> dolares -> pesos ---")
    print("monto inicial:", monto_inicial)
    print("monto final despues de", len(serie), "ciclos:", montos[-1])
    print("deriva acumulada:", deriva[-1])
    print("esta deriva es casi cero, es solo el error de redondeo del float64 (epsilon de maquina),")
    print("no es un error que se vaya acumulando cada vez mas fuerte, se queda rondando el 0")

    return montos, deriva, etiquetas


def analisis_B4():
    a64 = np.float64(874.67)
    b64 = np.float64(875.66)
    resultado_64 = a64 - b64

    a32 = np.float32(874.67)
    b32 = np.float32(875.66)
    resultado_32 = a32 - b32

    print("--- B4: cancelacion en float32 vs float64 ---")
    print("float64: 874.67 - 875.66 =", resultado_64)
    print("float32: 874.67 - 875.66 =", resultado_32)

    # el valor "exacto" de esta resta es -1.0, lo uso para ver que tan lejos quedo cada float
    valor_exacto = -1.0
    ea_64 = abs(valor_exacto - float(resultado_64))
    ea_32 = abs(valor_exacto - float(resultado_32))

    print("error absoluto contra -1.0 -> float64:", ea_64, "  float32:", ea_32)
    print("en los dos casos se pierden cifras significativas por restar numeros grandes y parecidos")
    print("(esto se llama cancelacion catastrofica), pero float32 pierde mas precision porque")
    print("tiene menos bits en la mantisa. esto va en la misma linea de lo que vimos en A3.")

    return resultado_64, resultado_32, ea_64, ea_32


if __name__ == "__main__":
    analisis_B1()
    print("")
    analisis_B2()
    print("")
    analisis_B4()
