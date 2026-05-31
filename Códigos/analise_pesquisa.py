import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('./Dados/pesquisa_marketing.csv')

#print(df)
print(df["plataforma_favorita"].value_counts()).plot(kind="bar")





