# Application of Transformers in Time Series for Multivariate Forecasting

Este repositorio contiene el código, los datos y los notebooks de experimentación desarrollados para un Trabajo de Fin de Máster (TFM) centrado en la predicción multivariante en series temporales financieras.

El estudio se enfoca en la predicción sobre el mercado continuo español (incluyendo los componentes del IBEX 35), utilizando datos históricos acumulados durante un periodo de 20 años.

## Estructura del Proyecto

El repositorio está organizado en tres grandes bloques: la extracción y preparación del dataset, la búsqueda y ajuste de hiperparámetros para los distintos modelos, y la ejecución de los experimentos finales con su consecuente comparación.

### 1. Conjuntos de Datos y Scripts de Extracción

Los archivos `.py` fueron utilizados para construir y procesar los lotes de datos históricos desde cero:

- `dataset_1_get_dataset.py`: Script para la descarga de cotizaciones financieras (apertura, máximo, mínimo, volumen, cierre ajustado) del IBEX 35 y el Mercado Continuo a través de Yahoo Finance (`yfinance`).
- `dataset_2_filter.py`: Script que filtra el conjunto de datos para seleccionar únicamente las empresas "supervivientes", es decir, aquellas con un histórico ininterrumpido a lo largo de las últimas dos décadas.
- `dataset_3_script_final.py`: Script que aplica las últimas transformaciones y da formato final al dataset para alimentar los modelos predictivos.

Como resultado de este proceso, se generaron los siguientes datasets incluidos en el proyecto:
- `dataset_mercado_continuo_20y.csv`: Contiene la información de todas las acciones del universo inicial a lo largo de 20 años.
- `dataset_tfm_56_survivors.csv`: El dataset final filtrado (con 56 empresas) que sirve como base principal para los experimentos del TFM.

### 2. Notebooks de Búsqueda de Hiperparámetros

Para garantizar un rendimiento óptimo en la comparativa, se ha dedicado una serie de notebooks a la búsqueda iterativa de los mejores hiperparámetros (tuneo) de cada arquitectura de red evaluada:

- `main_prueba_hiperparametros.ipynb`: Notebook empleado para buscar los hiperparámetros óptimos del **modelo principal** en el que se basa el TFM.
- `main_modelo_LSTM.ipynb`: Búsqueda de hiperparámetros para el modelo recurrente LSTM (Long Short-Term Memory).
- `main_modelo_NHITS.ipynb`: Búsqueda de hiperparámetros para el modelo N-HiTS (Neural Hierarchical Interpolation for Time Series Forecasting).
- `main_modelo_PatchTST.ipynb`: Búsqueda de hiperparámetros para el modelo PatchTST (arquitectura basada en Transformers).
- `main_modelo_TCN.ipynb`: Búsqueda de hiperparámetros para el modelo de redes convolucionales TCN (Temporal Convolutional Network).

### 3. Experimentos y Comparación de Modelos

Una vez establecidos los mejores hiperparámetros, se procede a las pruebas definitivas:

- `main.ipynb`: Notebook central del proyecto ("main a secas"). Engloba la ejecución de los experimentos definitivos con el modelo principal, generando los resultados fundamentales del TFM.
- `main_modelos_comparacion.ipynb`: Un notebook conclusivo que consolida y compara los resultados, las métricas y el rendimiento de todos los modelos (el modelo principal frente al resto de arquitecturas ajustadas en los notebooks anteriores).

## Requisitos y Configuración

En el repositorio se incluye un entorno preconfigurado y las dependencias necesarias. Se pueden instalar los requerimientos utilizando el archivo proporcionado:

```bash
pip install -r requirements.txt
```

---