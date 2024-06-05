import pandas as pd
import plotly.express as px
import streamlit as st
import numpy as np

st.set_page_config(layout="wide")
st.title("TMAX")

df = pd.read_csv("dados/dados_TMAX-IC.csv")
df["time"] = pd.to_datetime(df["time"])
df["year"] = df["time"].apply(lambda x: str(x.year))

estado = st.sidebar.selectbox("Estado", df["state"].unique())
anos = df["year"].unique()
anoInicial = st.sidebar.date_input("Data Inicial", min_value=df['time'].min(), max_value=df['time'].max(), value=df['time'].min())
anoFinal = st.sidebar.date_input("Data Final", min_value=df['time'].min(), max_value=df['time'].max(), value=df['time'].max())
label_trimestre = ["JFM", "AMJ", "JAS", "OND"]
trimestre = st.sidebar.selectbox("Trimestre", label_trimestre)
anoInicial = pd.to_datetime(anoInicial)
anoFinal = pd.to_datetime(anoFinal)

df = df[(df['time'] >= anoInicial) & (df['time'] <= anoFinal)]
df = df[df['state'] == estado]  # Filtra os dados pelo estado selecionado
df = df.drop(columns=['Unnamed: 0'])

coluna1, coluna2 = st.columns(2)
coluna3, coluna4 = st.columns(2)

df_JFM = df[df['time'].dt.month.isin([1, 2, 3])]
df_AMJ = df[df['time'].dt.month.isin([4, 5, 6])]
df_JAS = df[df['time'].dt.month.isin([7, 8, 9])]
df_OND = df[df['time'].dt.month.isin([10, 11, 12])]

percentil_JFM = np.percentile(df_JFM['t2m'], 90)
percentil_AMJ = np.percentile(df_AMJ['t2m'], 90)
percentil_JAS = np.percentile(df_JAS['t2m'], 90)
percentil_OND = np.percentile(df_OND['t2m'], 90)

def plot_percentil(trimestre):
    if trimestre == "JFM":
        df_trimestre = df_JFM
        percentil = percentil_JFM
    elif trimestre == "AMJ":
        df_trimestre = df_AMJ
        percentil = percentil_AMJ
    elif trimestre == "JAS":
        df_trimestre = df_JAS
        percentil = percentil_JAS
    elif trimestre == "OND":
        df_trimestre = df_OND
        percentil = percentil_OND
    
    fig = px.scatter(df_trimestre, x='time', y='t2m', labels={'time': 'Data', 't2m': 'Valor'}, title=f'Dados do trimestre {trimestre} e P90')
    fig.add_hline(y=percentil, line_dash="dot", line_color="red", annotation_text=f'P90 {trimestre}', annotation_position="top right")
    return fig

fig_percentil = plot_percentil(trimestre)
coluna1.plotly_chart(fig_percentil)

def filtrar_df(trimestre):
    if trimestre == "JFM":
        df_trimestre = df_JFM
    elif trimestre == "AMJ":
        df_trimestre = df_AMJ
    elif trimestre == "JAS":
        df_trimestre = df_JAS
    elif trimestre == "OND":
        df_trimestre = df_OND
    return df_trimestre

coluna3.write(filtrar_df(trimestre))
