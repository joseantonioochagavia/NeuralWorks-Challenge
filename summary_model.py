import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from joblib import dump, load

# Data Processing
df = pd.read_csv('data_procesado.csv', index_col=0)
features_importantes = df[['MES', 'temporada_alta', 'DIA_Jueves', 'DIA_Domingo', 'DIA_Lunes', 'DIA_Miercoles',
                                'OPERA_Grupo LATAM', 'periodo_dia_tarde', 'DIA_Martes', 'DIA_Viernes', 'periodo_dia_mañana',
                                'DIA_Sabado', 'periodo_dia_noche', 'OPERA_Sky Airline', 'OPERA_Latin American Wings',
                                'DES_Buenos Aires', 'DES_Puerto Montt', 'DES_Lima', 'DES_Iquique', 'OPERA_Air Canada']]
label = df['atraso_15']

# Split data
x_train2, x_test2, y_train2, y_test2 = train_test_split(features_importantes, label, test_size = 0.33, random_state = 42)

# Train the model
model_RFC_2 = RandomForestClassifier(random_state=42)
model_RFC_2 = model_RFC_2.fit(x_train2, y_train2)

# Save the model
dump(model_RFC_2, 'random_forest_simplificado.pkl')
print("Random Forest Model Saved")

# Load the model
model_RFC_2 = load('random_forest_simplificado.pkl')

columns = {
    "MES": 4,
    "temporada_alta": 0,
    "DIA_Jueves": 0,
    "DIA_Domingo": 1,
    "DIA_Lunes": 0,
    "DIA_Miercoles": 0,
    "OPERA_Grupo LATAM": 1,
    "periodo_dia_tarde": 0,
    "DIA_Martes": 0,
    "DIA_Viernes": 0,
    "periodo_dia_mañana": 0,
    "DIA_Sabado": 0,
    "periodo_dia_noche": 1,
    "OPERA_Sky Airline": 0,
    "OPERA_Latin American Wings": 0,
    "DES_Buenos Aires": 0,
    "DES_Puerto Montt": 0,
    "DES_Lima": 0,
    "DES_Iquique": 0,
    "OPERA_Air Canada": 0
}
input_df = pd.DataFrame([columns])

prediction = model_RFC_2.predict(input_df)
print(prediction)

# Save features from training
rf_columns_simplificado= list(x_train2.columns)
dump(rf_columns_simplificado, 'rf_columns_simplificado.pkl')
print("Random Forest Model Colums Saved")


