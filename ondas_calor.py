import xarray as xr
import pandas as pd
from datetime import datetime
import numpy as np
#import matplotlib.pyplot as plt
import plotly.express as px

df = pd.read_csv("dados/dados_TMAX-IC.csv")

df = df.drop('Unnamed: 0', axis = 1)

# Definir o intervalo de datas desejado
data_inicio = '1981-01-01'
data_fim = '2023-12-31'

df_filtrado = df.loc[(df['time'] >= data_inicio) & (df['time'] <= data_fim)]

df_filtrado = df_filtrado.loc[df['state'] == "São Paulo"]

#frequência de cada temperatura
contagem = df_filtrado['temperature'].value_counts()

# Ordenar os dados em ordem crescente de temperatura
contagem = contagem.sort_index()

del df
df = df_filtrado

#Calcular o Percentil 90
percentil = np.percentile(df['temperature'], 90)

# IDENTIFICAR ONDAS DE CALOR

def identificar_ondas(df):
    contador_ondas_de_calor = 0 # Contador para contabilizar o numero de dias acima do p90
    datas_ondas_de_calor = [] #Array para armazenar a data dos dias durante a onda de calor
    numero_ondas = 0 # Contador do numero total de ondas de calor
    for indice, linha in df.iterrows():
        if linha['temperature'] > percentil:  # Verificar se a temperatura é maior que o percentil
            contador_ondas_de_calor += 1
            datas_ondas_de_calor.append(linha['time'])
        else:
            if contador_ondas_de_calor >= 6:
                print(f'Onda de calor registrada: {datas_ondas_de_calor[0]} até {datas_ondas_de_calor[-1]}')
                # Plotar o gráfico da onda de calor
                fig = px.line(df.loc[df['time'].isin(datas_ondas_de_calor)], x='time', y='temperature', labels={'temperature': 'Temperatura (°C)'}, title='Onda de Calor')
                fig.add_hline(y=percentil, line_dash="dash", line_color="blue", name="Percentil 90")
                fig.update_layout(xaxis_title='Data', yaxis_title='Temperatura (°C)', xaxis_tickangle=-45)
                fig.show()
                datas_ondas_de_calor = []
                numero_ondas = numero_ondas + 1
            contador_ondas_de_calor = 0
    print("Número total de Ondas de Calor Registradas: ", numero_ondas)


identificar_ondas(df)
