import xarray as xr
import pandas as pd
import numpy as np

df = pd.read_csv("/Users/joaovyctor/Documents/GitHub/Temperature-Dashboards/dados/dados_Media-IC.csv")

# Converter a coluna 'time' para o formato de data
df['time'] = pd.to_datetime(df['time'])


# Extrair apenas a data (ignorando a informação de hora)
df['time'] = df['time'].dt.date

# Calcular a média da temperatura por dia
df = df.groupby('time')['t2m'].mean().reset_index()

df['t2m'] = df['t2m'].round()

df['state'] = 'São Paulo'

# Mostrar o resultado
print(df)

#print(df)
with open('dados_Media-IC.csv', 'a') as f:
    df.to_csv(f, header=f.tell()==0)

#df.to_csv('dados-IC.csv', index=False)  # index=False para evitar salvar o índice do DataFrame