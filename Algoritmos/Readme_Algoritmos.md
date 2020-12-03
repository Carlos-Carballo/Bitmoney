## Readme_Algoritmos
### Descripción algoritmos.

 - El archivo data_set.ipynb descarga de fuentes como Yahoo finance, KRAKEN y BITSTAMP datos financieros de las monedas en formato OHLC (open, high, low, close), donde se imputan los datos faltantes usando interpolación de orden 3. Estas se guardan en formato csv para su futura utilización.
 
 - En el archivo cluster.ipynb se leen los datos creados en data_set.ipynb, se convierten a datos diarios, semanales y mensuales, y a estos se les aplican las transformaciones matemáticas correspondientes, se agrupan en diez cluster usando k-means y se transforman en imágenes de 32x32 pixeles.
 
 - El archivo CNN.ipynb lee las imágenes generadas y crea un modelo usando una arquitectura propuesta.
 
 - Los archivos pred_moneda_-USD_x.py leen el modelo generado para cada moneda y periodicidad respectivamente para dar una predicción de compra, incertidumbre o venta.
 
 - Los archivos coin_metrics_moneda.ipynb descargan datos de la blockchain usando la api de coinmetrics para deducir cuales son las métricas más influyentes en el precio de la moneda correspondiente.    
 
