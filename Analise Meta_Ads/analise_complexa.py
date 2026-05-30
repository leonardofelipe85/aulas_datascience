import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

print("📊 --- INICIANDO ANÁLISE EXPLORATÓRIA DE PERFORMANCE --- 📊\n")

# 1. Carregar o arquivo CSV que você gerou (Usando o caminho relativo correto)
df = pd.read_csv('./campanhas_dado_fake.csv')

# Exibir o tamanho do relatório capturado
print(f"Dimensões do relatório: {df.shape[0]} linhas carregadas com sucesso.\n")

print("--- 1. METRICAS GERAIS POR PLATAFORMA ---")
print("-" * 60)
# Agrupando os dados por plataforma para ver Investimento e Receita Total
analise_plataforma = df.groupby('plataforma')[['gasto', 'receita']].sum()
# Calculando o ROAS Real Total de cada mídia (Receita / Gasto)
analise_plataforma['roas_total'] = (analise_plataforma['receita'] / analise_plataforma['gasto']).round(2)
print(analise_plataforma)
print("-" * 60)

print("\n--- 2. CUSTO POR AQUISIÇÃO (CPA) MÉDIO POR PÚBLICO ---")
print("-" * 60)
# Descobrindo qual público entrega o lead ou venda mais barata
analise_publico = df.groupby('publico')['cpa'].mean().round(2).sort_values()
print(analise_publico)
print("-" * 60)

print("\n--- 3. PERFORMANCE POR DISPOSITIVO (TAXA DE CONVERSÃO) ---")
print("-" * 60)
# Analisando se o cliente compra mais pelo celular ou pelo computador
analise_dispositivo = df.groupby('dispositivos')['taxa_conversao'].mean().round(2)
print(analise_dispositivo)
print("-" * 60)


# --- CONFIGURAÇÃO VISUAL DO GRÁFICO COM SEABORN ---
print("\n🎨 Gerando gráfico executivo de barras. Aguarde a janela abrir...")

# Define um estilo de fundo limpo com linhas de grade
sns.set_theme(style="whitegrid")

# Define o tamanho da janela do gráfico
plt.figure(figsize=(11, 6))

# Cria o gráfico cruzando Público (X), ROAS Médio (Y) e separando por Plataforma (Cores)
grafico = sns.barplot(
    data=df, 
    x='publico', 
    y='roas', 
    hue='plataforma', 
    palette='muted',
    errorbar=None  # Limpa as linhas pretas de erro para o gráfico ficar mais executivo
)

# Títulos e legendas do relatório visual
plt.title('Performance de ROAS: Cruzamento de Públicos por Canal de Mídia', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Segmentação de Público', fontsize=12, fontweight='bold')
plt.ylabel('Retorno Sobre o Gasto (ROAS Médio)', fontsize=12, fontweight='bold')
plt.legend(title='Plataformas', title_fontsize='11', loc='upper right')

# Comando automático para colocar os valores das médias no topo de cada barra do gráfico
for container in grafico.containers:
    grafico.bar_label(container, fmt='%.2f', padding=3, fontsize=9)

# Ajusta o espaçamento para o gráfico não cortar as bordas
plt.tight_layout()

# Força o Windows a abrir a tela com o gráfico interativo
plt.show()


