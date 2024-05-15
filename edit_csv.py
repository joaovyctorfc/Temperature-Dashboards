import pandas as pd

# Carregar o CSV
df = pd.read_csv("/Users/joaovyctor/Documents/GitHub/Temperature-Dashboards/dados/dados_Media-IC.csv")

# Remover a coluna desejada (substitua 'coluna_indesejada' pelo nome da coluna que deseja remover)
df = df.drop(columns=['year'])

# Salvar o DataFrame resultante de volta como um arquivo CSV
df.to_csv("/Users/joaovyctor/IC-INPE/dados/dados_Media-IC.csv", index=False)
print(df)