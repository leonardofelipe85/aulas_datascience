import pandas as pd 
import matplotlib.pyplot as plt
import os 

#CARREGAMENTO DA BASE DE DADOS 
print("Carregando a base de dados 'SampleSuperstore.csv'...")
df = pd.read_csv("SampleSuperstore.csv", sep=";")

#CRIAÇÃO AUTOMÁTICA DA PASTA 
os.makedirs("graficos", exist_ok=True)

print("Pasta de gráficos verificada com sucesso!")

#REMOÇÃO DE COLUNAS VAZIAS 
print("Removendo colunas vazias geradas pelo Excel...")
df = df.loc[:, ~df.columns.str.contains('^Unnamed', na=False)]

#REMOVER DUPLICADOS 
print("\n🔍 Verificando registros duplicados...")

duplicados_antes = df.duplicated().sum()

print(f"Duplicados encontrados: {duplicados_antes}")

df = df.drop_duplicates()

duplicados_depois = df.duplicated().sum()

print(f"Duplicados restantes após limpeza: {duplicados_depois}")


#FUNÇÃO DE TRATAMENTO NUMÉRICO
print("Executando higinização dos dados numéricos...")
def blindar_numeros(valor):
    #Verifica se o valor é nulo 
    if pd.isna(valor): 
        return None
    #Converte para texto e remove espaços
    valor = str(valor).strip()
    #Troca vírgula por ponto
    valor = valor.replace(",", ".")
    try: 
        return float(valor)

    except: 
        return None 

#TRATAMENTO DAS COLUNAS NUMÉRICAS     
df["Sales"] = df["Sales"].apply(blindar_numeros)
df["Profit"] = df["Profit"].apply(blindar_numeros)
df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
df["Discount"] = pd.to_numeric(df["Discount"], errors="coerce")


#TRATAMENTO DE DATAS 
print("Convertendo datas para formato analítico...")

df["Ship Date"] = pd.to_datetime(
    df["Ship Date"], 
    format="%m/%d/%Y", 
    errors ="coerce"
)

df["Order Date"] = pd.to_datetime(
    df["Order Date"], 
    format="%m/%d/%Y", 
    errors="coerce"
)
print(f"Campos de data prontos: Ship Date ({df['Ship Date'].dtype}) | Order Date ({df['Order Date'].dtype})")

#TRATAMENTO DE VALORES NULOS 
print("Aplicando prrenchimento estatístico de segurança..")

"""
Utilizando a mediana para evitar distorções 
causados por valores extremos (outliers)
"""

df["Sales"] = df["Sales"].fillna(df["Sales"].median())
df["Profit"] = df["Profit"].fillna(df["Profit"].median())
df["Quantity"] = df["Quantity"].fillna(df["Quantity"].median())
df["Discount"] = df["Discount"].fillna(df["Discount"].median())

#DETECÇÃO DE OUTLIERS 
Q1 = df["Sales"].quantile(0.25)
Q3 = df["Sales"].quantile(0.75)

IQR = Q3 - Q1

limite_inferior = Q1 - 1.5 * IQR
limite_superior = Q3 + 1.5 * IQR

outliers = df[
    (df["Sales"] < limite_inferior) |
    (df["Sales"] > limite_superior)
]

print("\nOUTLIERS IDENTIFICADOS EM SALES:")
print(outliers.shape[0])

#QUALIDADE DOS DADOS 
print("\nRESUMO DA QUALIDADE DOS DADOS")
print(df.isnull().sum())

#RESUMO DO PROCESSAMENTO
print("\n PROCESSAMENTO CONCLUÍDO COM SUCESSO!")
print(f"Registros processados: {df.shape[0]}  Nulos em Sales: {df['Sales'].isnull().sum()} | Nulos no Profit: {df['Profit'].isnull().sum()}")

#VISÃO GERAL DOS DADOS 
print("\nPRIMEIRAS LINHAS:\n")

print(df.head())

print("\nINFORMAÇÕES DO DATASET:\n")

print(df.info())

print("\nESTATÍSTICA DESCRITIVA:\n")

print(df.describe())

# GRÁFICO 1: VENDAS POR CATEGORIA (BARRAS)
print("\n Gerando Gráfico 1: Vendas por Categoria...")
vendas_categoria = df.groupby("Category")["Sales"].sum()

plt.figure(figsize=(8, 5))
vendas_categoria.plot(kind="bar", color="royalblue", edgecolor="black") 
plt.title("Faturamento Bruto por Categoria de Produto", fontsize=12, fontweight='bold')
plt.xlabel("Categorias", fontsize=10)
plt.ylabel("Total de Vendas ($)", fontsize=10)
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("graficos/1_grafico_vendas_categoria.png")
plt.show()

# GRÁFICO 2: LUCRO POR CATEGORIA (BARRAS)
print("\n Gerando Gráfico 2: Lucro por Categoria...")
lucro_categoria = df.groupby("Category")["Profit"].sum()

plt.figure(figsize=(8, 5))
lucro_categoria.plot(kind="bar", color="mediumseagreen", edgecolor="black") 
plt.title("Lucro Líquido Real por Categoria de Produto", fontsize=12, fontweight='bold')
plt.xlabel("Categorias", fontsize=10)
plt.ylabel("Lucro Total ($)", fontsize=10)
plt.xticks(rotation=0)
plt.savefig("graficos/2_grafico_lucro_categoria.png")
plt.tight_layout()
plt.show()

# GRÁFICO 3: VENDAS POR REGIÃO (BARRAS HORIZONTAIS)
print("\n Gerando Gráfico 3: Vendas por Região Comercial...")
vendas_regiao = df.groupby("Region")["Sales"].sum().sort_values(ascending=True)

plt.figure(figsize=(8, 5))
vendas_regiao.plot(kind="barh", color="darkorange", edgecolor="black") 
plt.title("Distribuição do Faturamento por Região Geográfica", fontsize=12, fontweight='bold')
plt.xlabel("Total de Vendas ($)", fontsize=10)
plt.ylabel("Regiões", fontsize=10)
plt.tight_layout()
plt.savefig("graficos/3_grafico_vendas_regiao.png")
plt.show()

# GRÁFICO 4: IMPACTO DO DESCONTO NO LUCRO (DISPERSÃO)
print("\n Gerando Gráfico 4: Impacto do Desconto no Lucro...")
plt.figure(figsize=(8, 5))

# Criando o gráfico de dispersão (Scatter Plot)
plt.scatter(df["Discount"], df["Profit"], alpha=0.5, color="crimson", edgecolor="white")

# Linha de referência no Lucro Zero (tudo abaixo dela é prejuízo)
plt.axhline(y=0, color="black", linestyle="--", linewidth=1.2)

plt.title("Análise de Causa e Efeito: Margem de Desconto vs Lucro Líquido", fontsize=12, fontweight='bold')
plt.xlabel("Taxa de Desconto (0.0 a 0.8)", fontsize=10)
plt.ylabel("Lucro / Prejuízo Real ($)", fontsize=10)
plt.grid(True, linestyle=":", alpha=0.6)
plt.tight_layout()
plt.savefig("graficos/4_grafico_desconto_lucro.png")
plt.show()

df["Profit"] = df["Profit"].fillna(df["Profit"].median())

# EXTRA 1 — TOP 10 PRODUTOS MAIS LUCRATIVOS
print("\nTOP 10 PRODUTOS MAIS LUCRATIVOS:\n")

top_produtos = (
    df
    .groupby("Product Name")["Profit"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print(top_produtos)

# EXTRA 2 — LUCRO TOTAL POR REGIÃO
print("\nLUCRO TOTAL POR REGIÃO:\n")

lucro_regiao = (
    df
    .groupby("Region")["Profit"]
    .sum()
)

print(lucro_regiao)

# EXTRA 3 — LUCRO TOTAL POR SEGMENTO
print("\nLUCRO TOTAL POR SEGMENTO:\n")

lucro_segmento = (
    df
    .groupby("Segment")["Profit"]
    .sum()
)

print(lucro_segmento)

# EXTRA 4 — VENDAS POR ANO
print("\nVENDAS POR ANO:\n")

df["Ano"] = df["Order Date"].dt.year

vendas_ano = (
    df
    .groupby("Ano")["Sales"]
    .sum()
)

print(vendas_ano)

#EXPORTAÇÃO DE DATASET TRATADO 
df.to_excel(
    "dataset_tratado.xlsx", 
    index=False 
    )
os.makedirs("graficos", exist_ok=True)

print("Pasta de gráficos verificada com sucesso!")

#EXPORTAÇÃO DO RESUMO GERENCIAL 
resumo = {
    "Total Vendas": [df["Sales"].sum()],
    "Total Lucro": [df["Profit"].sum()],
    "Quantidade Registros": [df.shape[0]],
    "Outliers Sales": [outliers.shape[0]]
}

df_resumo = pd.DataFrame(resumo)

df_resumo.to_excel(
    "resumo_gerencial.xlsx",
    index=False
)

print("Resumo gerencial exportado com sucesso!")

#FINALIZAÇÃO 
print("\n [FIM] Todas as análises foram executadas com sucesso!")