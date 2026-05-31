import pandas as pd
import numpy as np
from datetime import datetime, timedelta 

# Definir semente para resultados reproduzíveis 
np.random.seed(42)

# Gerar datas (últimos 30 dias)
datas = pd.date_range(start='2025-05-01', end='2025-05-30', freq='D')

# Cria dados 
dados = []

plataformas = ['Meta Ads', 'Google Ads', 'TikTok Ads']
campanhas = ['Black Friday', 'Cyber Monday', 'Ano Novo', 'Verão']
criativos = ['Video 15s', 'Carrossel', 'Imagem', 'Collection']
publicos = ['Frio', 'Quente', 'Lookalike']
dispositivos = ['Mobile', 'Desktop']
posicionamentos = ['Feed', 'Stories', 'Reels']


for data in datas: 
    for _ in range(np.random.randint(5, 15)): # 5-15 anúncios por dia 
        impressoes = np.random.randint(5000, 50000)
        ctr_gerado = np.random.uniform(1.0, 5.0)  # CTR entre 1% e 5%
        cliques = int(impressoes * ctr_gerado / 100)
        gasto = np.random.uniform(100, 500)
        conversoes = int(cliques * np.random.uniform(0.02, 0.15))  # 2-15% conv rate

        dados.append({
            'data': data,
            'plataforma': np.random.choice(plataformas),
            'campanha': np.random.choice(campanhas),
            'criativo': np.random.choice(criativos),
            'publico': np.random.choice(publicos),
            'dispositivos': np.random.choice(dispositivos),
            'posicionamento': np.random.choice(posicionamentos),
            'impressoes': impressoes,
            'cliques': cliques,
            'gasto': round(gasto, 2),
            'conversoes': conversoes,
            'receita': round(conversoes * np.random.uniform(50, 200), 2), 

        })

# CORREÇÃO AQUI: Criando o DataFrame do jeito certo, passando a lista 'dados'
df = pd.DataFrame(dados)

# Calcular métricas 
df['ctr'] = (df['cliques'] / df['impressoes'] * 100).round(2)
df['cpc'] = (df['gasto'] / df['cliques']).round(2)

# Evitar divisão por zero caso haja alguma conversão zerada
df['cpa'] = (df['gasto'] / df['conversoes']).replace([np.inf, -np.inf], 0).round(2)
df['roas'] = (df['receita'] / df['gasto']).round(2)
df['taxa_conversao'] = (df['conversoes'] / df['cliques'] * 100).round(2)

# Salvar como CSV 
df.to_csv('./campanhas_dado_fake.csv', index=False)

print("✅ Arquivo 'campanhas_dados_fake.csv' criado com sucesso!")
print(f"\nDados gerados: {len(df)} linhas")
print(f"\nPrimeiras linhas:")
print(df.head(10))

