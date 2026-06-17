import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os

deaths_df = pd.read_csv('Cumulative Count of COVID-19 Deaths in Brazil.csv')
vaccines_df = pd.read_csv('Total COVID-19 Vaccines Administered in Brazil.csv')

def process_covid_data_fixed(df):
    date_col = 'Variable observation date'
    value_col = 'Variable observation value'
    df['date_parsed'] = pd.to_datetime(df[date_col])
    df[value_col] = pd.to_numeric(df[value_col], errors='coerce')
    return df.dropna(subset=['date_parsed', value_col]).sort_values('date_parsed'), 'date_parsed', value_col

deaths_df, d_date, d_val = process_covid_data_fixed(deaths_df)
vaccines_df, v_date, v_val = process_covid_data_fixed(vaccines_df)

# Cálculo das mortes diárias (valor absoluto)
deaths_df['daily_deaths'] = deaths_df[d_val].diff().fillna(0)
# Suavização (média móvel de 14 dias)
deaths_df['daily_deaths_smoothed'] = deaths_df['daily_deaths'].rolling(window=14).mean()

# Criando a visualização
fig, ax1 = plt.subplots(figsize=(15, 8))

# Eixo 1: Mortes Diárias (Valor Absoluto)
color_daily = 'red'
ax1.set_xlabel('Data')
ax1.set_ylabel('Mortes Diárias (Média Móvel 14d)', color=color_daily)
ax1.plot(deaths_df[d_date], deaths_df['daily_deaths_smoothed'], color=color_daily, linewidth=2, label='Mortes Diárias')
ax1.tick_params(axis='y', labelcolor=color_daily)

# Eixo 2: Vacinas
ax2 = ax1.twinx()
color_vac = 'tab:blue'
ax2.set_ylabel('Total de Vacinas Aplicadas', color=color_vac)
ax2.plot(vaccines_df[v_date], vaccines_df[v_val], color=color_vac, linewidth=3, label='Vacinas Aplicadas')
ax2.tick_params(axis='y', labelcolor=color_vac)

# Formatação para evitar notação científica
for ax in [ax1, ax2]:
    ax.get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

plt.title('Vacinação vs. Queda no Número Absoluto de Mortes (Brasil)')
ax1.grid(True, linestyle=':', alpha=0.6)

# Legenda
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

# ALTERAÇÃO 2: Salvar a figura em vez de exibir (ou exibir)
fig.tight_layout()

# Opção 1: Salvar como imagem
plt.savefig('covid_analysis.png', dpi=300, bbox_inches='tight')

# Opção 2: Mostrar o gráfico (descomente a linha abaixo)
# plt.show()
