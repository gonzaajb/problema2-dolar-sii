problema2-dolar-sii

Laboratorio evaluado 1 de Analisis Numerico

La idea del trabajo es analizar el error y como se propaga, usando como dato el dolar observado del SII (promedio mensual, desde enero 2022 hasta diciembre 2025).

Estructura de las carpetas solicitado por el profesor

```
problema2-dolar-sii/
├── README.md
├── INFORME.md
├── requirements.txt
├── data/
│   └── dolar_observado_sii_2022_2025.csv
├── src/
│   ├── cargar_datos.py
│   ├── errores.py
│   ├── anualidad.py
│   ├── punto_flotante.py
│   └── graficos.py
└── graficos/
```

Como se ejecuta

Primero instalar lo que pide `requirements.txt`, y despues correr los scripts desde la carpeta `src`:


pip install -r requirements.txt
cd src
python3 errores.py          # esto corre A1, A2 y A3
python3 anualidad.py        # esto corre A4 y A5
python3 punto_flotante.py   # esto corre B1, B2 y B4
python3 graficos.py         # genera las 5 graficas y el csv de evaluacion_error

Resultados

- A1: redondeando cada precio a 2 cifras significativas, el mes que salio con peor error relativo fue Abril 2022, con un Er de mas o menos 0.60%.


- A2: si compro en Febrero 2023 (798.26) y vendo en Enero 2025 (1000.76), con un millon de pesos, la ganancia queda en 250.000 +- 3.674 (Er ≈ 1.47%).


- A3: entre diciembre 2022 y diciembre 2023 el dolar vario -1.00 +- 0.67 (usando 3 cifras significativas). Aca el error es casi del mismo tamaño que el resultado, entonces la caida del dolar se puede afirmar pero raspando.


- A4: si ordeno los anios de mas confiable a menos confiable segun el Er%, queda: 2024 > 2022 > 2025 > 2023. Basicamente los anios con menos error son los que tuvieron una variacion anual mas chica.


- A5: el mes mas barato de todo el periodo fue Febrero 2023 (798.26) y el mas caro Enero 2025 (1000.76). La rentabilidad da 25.00% +- 0.37%, o sea el error es bastante mas chico que la ganancia, asi que esta conclusion si es confiable.


- B4: al restar 874.67 - 875.66, en float64 da -0.9900000000000091 y en float32 da -0.98999023. En los dos casos se ve la cancelacion catastrofica (se pierden cifras significativas comparado con el -1.00 esperado), pero en float32 se nota mas.


