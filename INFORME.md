1. Metodologia

Use el promedio mensual del dolar observado del SII entre enero 2022 y diciembre 2025. Cargue el csv con np.genfromtxt y todo el redondeo/propagacion lo hice con las funciones de errores.py, siguiendo las reglas vistas en clases:

Redondeo por defecto a 2 cifras significativas.
Ea = |valor real - valor aproximado|.
Er (%) = (Ea / valor real) x 100.
Suma/resta: se suman los errores absolutos.
Multiplicacion/division: se suman los errores relativos.
M = 1.000.000 CLP para las simulaciones de compra/venta.

2. Preguntas del error

A1. Redondeando los 48 precios a 2 cifras significativas, los Er van entre 0.01% y 0.60%. El peor caso es Abril 2022 (815.12 -> 820, Ea = 4.88, Er = 0.60%), porque cae casi a mitad de camino entre dos valores representables.

A2. Compro Febrero 2023 (798.26 -> 800) y vendo Enero 2025 (1000.76 -> 1000), con M = 1.000.000: USD = 1.250, pesos finales = 1.250.000, ganancia = 250.000 +- 3.674 (Er aprox 1.47%). El error se acumula sumando el Er de la compra (0.22%) y el de la venta (0.08%).

A3. Diciembre 2022 (876) vs diciembre 2023 (875): ΔP = -1.00 +- 0.67 (Er aprox 67%). El error es casi del tamano del resultado, asi que no se puede afirmar con seguridad que el dolar bajo entre esos dos diciembres.

A4.

Año     Enero	Diciembre	Variacion   Error   Er%
2024	907.99	982.30	    +74.0	    +-0.31	0.4%
2022	822.05	875.66	    +54.0	    +-0.39	0.7%
2025	1000.76	916.16	    -84.0	    +-0.92	1.1%
2023	826.34	874.67	    +49.0	    +-0.67	1.4%

Orden de confiabilidad: 2024 > 2022 > 2025 > 2023. El error absoluto no cambia mucho entre años, pero la variacion real si, entonces cuando el dolar se mueve poco (2023) el mismo error pesa mas en porcentaje.

A5. Mes mas barato: Febrero 2023 (798.26). Mas caro: Enero 2025 (1000.76). Rentabilidad: 25.00% +- 0.37%. Como el error es mucho mas chico que la rentabilidad, la conclusion es confiable.

3. Preguntas del punto flotante

B1. Guardar pocas cifras significativas es como una mantisa corta en punto flotante. 1000.76 (mantisa 1.00076 x 10^3) con 3 cifras queda 1000, con Ea = 0.76 (Er aprox 0.08%): menos cifras, mas error.

B2. M = 1.000.000 pasado a USD y devuelta a pesos con cada uno de los 48 precios deberia dar el mismo monto, pero por redondeo de float64 queda una deriva de 1e-10 a 1e-9 pesos, del orden del epsilon de maquina y sin acumularse entre ciclos.

B4. 874.67 - 875.66: float64 da -0.9900000000000091, float32 da -0.98999023 (exacto: -0.99). Ambos muestran cancelacion catastrofica, mas marcada en float32 por tener menos bits de mantisa — el mismo fenomeno de A3.

4. Conclusion final
Mejor compra: Febrero 2023 (798.26), diferencia con meses vecinos muy superior al error de representacion — confiable.
Mejor venta: Enero 2025 (1000.76), misma logica, tambien confiable.
Comprar en Febrero 2023 y vender en Enero 2025 da 25.00% +- 0.37% de rentabilidad: recomendacion solida (error 60 veces menor que la ganancia).
No se puede afirmar con seguridad la baja entre diciembre 2022 y 2023 (-1.00 +- 0.67), ni la variacion 2023 en general (la menos confiable, Er aprox 1.4%).
Leccion: al restar numeros grandes y parecidos, el error absoluto no se achica aunque el resultado si, entonces el error relativo se dispara y una diferencia que parece clara puede estar escondida dentro del margen de error.