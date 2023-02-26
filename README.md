# NeuralWorks-Challenge

El desafío consiste en un problema de clasificación binaria, el que busca predecir la probabilidad de atraso de los vuelos con origen en el aeropuerto de Santiago, Para esto se cuenta con el dataset “dataset_SCL.csv”, el que se puede descargar en el respositorio.

Para el desafio se resolvieron las siguientes preguntas:
-	Escoger el modelo que tenga una mejor performance.
-	Implementar mejoras sobre el modelo escogiendo la o las técnicas que prefieras.
-	Habilitar el modelo seleccionado como API REST para ser expuesto.
-	Hacer pruebas de estrés a la API con el modelo expuesto con al menos 50.000 requests durante 45 segundos. Para esto se utilizo la herramienta de testeto “wrk” que se encuentra en el siguiente link: https://github.com/wg/wrk
-	Finalmente ver como se podría mejorar la eficiencia de las pruebas anteriores.

## Modelacion

Originalmente se contaba con el archivo "to-expose-original.ipynb" que contenia en análisis y modelación preliminar del problema de machine learning. 
Se trabajo sobre este archivo base en "to-expose-modified.ipinb" donde se profundizo en el analisis y se agregaron nuevas variables y modelos para resolver las preguntas anteriores.

Se compararon 4 modelos: Regresion Logistica, XGBoost, KNeighborsClassifier y RandomForestClassifier. Se testearon estos modelos mediante diversas metricas de evaluacion, donde las metricas mas relevantes que se considerarn para la eleccion final fue f1_score y el Coeficiente de Correlacion de Matthews. Estas debido al inbalance de clases que se presenta en el target, donde solo el 18% de los datos que se usaron para la fase de testeo son atrasos (clase 1). En la siguiente figura se muestra la compraracon por metricas para los modelos.

![image](https://user-images.githubusercontent.com/120424248/221386201-251eb483-55b4-4f9f-860c-a47e1feb7600.png)

Del grafico y guiandonos por las metricas de f1-score y MCC al existir imbalance de clases, se observa que los modeos de KNeighbors y RandomForest se comportan bastante parecidos y suepran a los otros dos. Por simplicidad y dado que KNeighbors no tiene un metodo en particular para calcular feature importance, optamos por **RandomForestClassifier**.

Hay que señalar que todos los modelos fueron malos, debido a la gran cantidad de falsos negativos. Una de las posibles razones, la más clara, es el desbalanceo que existe en la clase 'atraso_15'.

Para poder mejorar la performance se realizo un Grid Search CV sobre RandomForest para tunear de mejor manera los hiperparámetros. Existen mas opciones que se podrian hacer en un futuro para seguir mejorando, como probar nuevos modelos o uno mas complejo. De la perspectiva de los datos, si se quiere seguir mejorando, una opcion tambien seria recolectar mas datos para poder entrenar mejor al modelo. Tambien se podria mejorar la estrategia de autorrelenado para los valores faltantes (para el caso de periododia) junto con la estrategia de encoding (cambiar los valores no numericos a numericos).

Se hizo una comparacion entre el modelo original de Random Forest, el modeo simplificao con las features mas importantes y el modelo tuneado con Grid Searcg CV. El grafico se muestra a continuacion:

![image](https://user-images.githubusercontent.com/120424248/221386510-8c5ea963-2672-4e20-a227-931d02852e31.png)

De la perpectiva del modelo, podemos seguir mejorando el modelo a traves de hyperparaeter tuning cambiando el rango de los parametros y volviendo a intentar con GridSearchCV, o simplemente buscar algun otro modelo que ajuste mejor. Pero nuevamente hay que que tener en consideracion el imbalance de clases que se presenta, lo que dificulta la evaluacion para el problema.

Para la realizacion del test de estres, se uso el modelo RandomForest Simplificado. Para esto se guardo el modelo en un archivo pkl.

Se creo un archivo con el resumen de la etapa de modelacion como "sumary_model.py". Para mas detalles revisar el archivo "to_expose-modified.ipynb"

## Habilitacion del modelo como API REST

Para la implementacion de la API REST se utilizo las herramientas entregadas por la flask. El codigo de la api se encuentra en el archivo "api.py" para ver mas detalles.

Construida la api, se hizo un primer testeo en Postman para verificar su funcionaminto, el cual fue un exito. 

## Test de estres con la herramienta de "wrk"

Terminada la primera fase de testeo, se procedió a realizar el test de stress con la herramienta “wrk”. Para esto se trabajo con el terminal de Ubuntu Bash dentro de Windows. Se hicieron 50.000 request durante 45 segundos utilizando el siguiente comando:

./wrk -t4 -c278 -d45s s post.lua http://localhost:5000/predict

El input que se usó para hacer el testeo se encuentra dentro de la carpeta wrk en un archivo llamado “post”.

Los resultados de las etricas se guardaron en un archico txt dentro de la carpeta "wrg", mediante el siguiente comando:

./wrk -t4 -c278 -d45s s post.lua http://localhost:5000/predict > wrk-results.txt

## Resultados y conclusiones

Los resultados de esta prueba se muestran a continuación y también se encuentran guardados en “wrk_results.txt”:

Running 45s test @ http://localhost:5000/predict
  4 threads and 228 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency     1.22s   450.16ms   1.97s    58.18%
    Req/Sec    12.97      9.75    60.00     75.30%
  1384 requests in 45.09s, 227.22KB read
  Socket errors: connect 0, read 0, write 0, timeout 1329
Requests/sec:     30.70
Transfer/sec:      5.04KB

Donde:
- Latency: El tiempo que tarda en completarse una sola petición, desde que se envía hasta que se recibe la respuesta.
- Req/seg: El número de solicitudes completadas por segundo, promediadas durante la duración de la prueba.
- Transfer/seg: La cantidad de datos transferidos por segundo, promediada durante la duración de la prueba.
- Socket errors: El número de errores de socket que se produjeron durante la prueba.

Basandonos en los resultados de la herramienta de testeo de "wrk", parece que el principal cuello de botella en la performance de la API es la latencia, la cual es bastante alta para un promedio de 1.22s y un maximo de 1.97s. Esto indica que pueden existir ciertas operaciones en el codifo de la API que estan causando que la latencia sea mas alta.

Para mejorar la performance, una manera seria optimizando el codigo de la API, especialmente el codigo que es ejcutado cuando una prediccion es solicitada. Un posible enfoque es utilizar caching para evitar realizar los mismos cálculos repetidamente para los mismos datos de entrada. Esto puede hacerse almacenando los datos de entrada y la predicción correspondiente en un cache, y comprobando el cache antes de realizar una nueva predicción.

Otro enfoque consiste en optimizar el propio modelo de machine learning. Por ejemplo, intentar reducir el número de características utilizadas en el modelo o probar diferentes algoritmos que puedan ser más eficientes para el problema. Además, se puede intentar optimizar los hiperparámetros del modelo Random para lograr un mejor rendimiento.

Por último, también se puede considerar la posibilidad de utilizar un servidor más potente o escalar horizontalmente añadiendo más servidores para gestionar los requests. Esto puede ayudar a distribuir la carga y reducir la latencia.

