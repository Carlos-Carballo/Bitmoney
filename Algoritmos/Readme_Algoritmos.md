## Readme_Algoritmos
### Descripción algoritmos.

 - El archivo data_set.ipynb descarga de fuentes como Yahoo finance, KRAKEN y BITSTAMP datos financieros de las monedas en formato OHLC (open, high, low, close), donde se imputan los datos faltantes usando interpolación de orden 3. Estas se guardan en formato csv para su futura utilización.
 
 - En el archivo cluster.ipynb se leen los datos creados en data_set.ipynb, se convierten a datos diarios, semanales y mensuales, y a estos se les aplican las transformaciones matemáticas correspondientes, se agrupan en diez cluster usando k-means y se transforman en imágenes de 32x32 pixeles.
 
 - El archivo CNN.ipynb lee las imágenes generadas y crea un modelo usando una arquitectura propuesta.
 
 - Los archivos pred_moneda_-USD_x.py leen el modelo generado para cada moneda y periodicidad respectivamente para dar una predicción de compra, incertidumbre o venta.
 
 - Los archivos coin_metrics_moneda.ipynb descargan datos de la blockchain usando la api de coinmetrics para deducir cuales son las métricas más influyentes en el precio de la moneda correspondiente.    
 
### Description of algorithms.
The data_set.ipynb file downloads from sources such as Yahoo finance, KRAKEN and BITSTAMP financial data of the currencies in OHLC (open, high, low, close) format, where the missing data is imputed using order interpolation 3. These are saved in format csv for future use.

In the cluster.ipynb file, the data created in data_set.ipynb is read, converted to daily, weekly and monthly data, and the corresponding mathematical transformations are applied to them, they are grouped into ten clusters using k-means and transformed into images 32x32 pixels.

The CNN.ipynb file reads the generated images and creates a model using a proposed architecture.

The files pred_moneda_-USD_x.py read the generated model for each currency and periodicity respectively to give a prediction of buy, uncertainty or sale.

The coin_metrics_moneda.ipynb files download data from the blockchain using the coinmetrics api to deduce which are the most influential metrics on the price of the corresponding coin.
