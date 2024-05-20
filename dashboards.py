import pandas as pd
import plotly.express as px
import streamlit as st

# Usar a tela toda com o Streamlit
st.set_page_config(layout="wide")

st.title("Ondas de Calor")

# Carregar o CSV
df = pd.read_csv("dados/dados_Media-IC.csv")

# Converter coluna de time em datetime
df["time"] = pd.to_datetime(df["time"])

# Funcao para criar a coluna de ANO
df["year"] = df["time"].apply(lambda x: str(x.year))

# Botao lateral de selecao
estado = st.sidebar.selectbox("Estado", df["state"].unique())

# Botao lateral de selecao
anos = df["year"].unique()
anoInicial = st.sidebar.date_input("Data Inicial", min_value=df['time'].min(), max_value=df['time'].max(), value=df['time'].min())
anoFinal = st.sidebar.date_input("Data Final", min_value=df['time'].min(), max_value=df['time'].max(), value=df['time'].max())

# Converter objetos date para datetime
anoInicial = pd.to_datetime(anoInicial)
anoFinal = pd.to_datetime(anoFinal)

# DataFrame filtrado
df = df[(df['time'] >= anoInicial) & (df['time'] <= anoFinal)]

# Divide a tela em colunas para adicionar gráficos
coluna1, coluna2 = st.columns(2)
coluna3, coluna4 = st.columns(2)

# Criar plot da figura
fig_temp = px.line(df, x='time', y='t2m', title='Temperatura Média Diária')

# Adiciona o gráfico criado à coluna 1 do site
coluna1.plotly_chart(fig_temp)

# Exibir DataFrame filtrado
coluna2.write(df)
