from datetime import date, datetime
from matplotlib import pyplot as plt
import numpy as np
from bcb import sgs

# Entrada de dados
capital = float(input("Digite o capital investido: "))
frequencia = input("Digite a frequência do período ('Y' para Anual, 'M' para Mensal, 'D' para Diário): ").upper()
inicio = input("Digite a data inicial maior do que 1995/01/01 no formato YYYY/MM/DD: ")
final = input("Digite a data final no seguinte formato YYYY/MM/DD: ")

data_inicial = datetime.strptime(inicio, "%Y/%m/%d").date()
data_final = datetime.strptime(final, "%Y/%m/%d").date()

if frequencia == 'Y':
    frequencia = 'YE'  
elif frequencia == 'M':
    frequencia = 'ME'  
elif frequencia != 'D': 
    raise ValueError("Frequência inválida. Utilize 'Y', 'M' ou 'D'.")

# Pegar dados da SELIC do Banco Central
taxas_selic = sgs.get({"selic": 11}, start=data_inicial, end=data_final)

# Converter taxa de SELIC para percentual (dividindo por 100)
taxas_selic = taxas_selic / 100

# Calcular o retorno acumulado no período
capital_acumulado = capital * (1 + taxas_selic["selic"]).cumprod()

# Resampling conforme a frequência
capital_com_frequencia = capital_acumulado.resample(frequencia).last()

# Filtrando os dados para janela de 500 dias (2000/01/01 a 2022/03/31)
data_inicial_2 = date(2000, 1, 1)
data_final_2 = date(2022, 3, 31)

selic_questao_2 = sgs.get({"selic": 11}, start=data_inicial_2, end=data_final_2) / 100


janelas_500_dias = ((1 + selic_questao_2["selic"]).rolling(window=500).apply(np.prod, raw=True) - 1)


janelas_500_dias = janelas_500_dias.reset_index()


janelas_500_dias["data_inicial"] = janelas_500_dias["Date"].shift(500)

# Remover valores nulos
janelas_500_dias = janelas_500_dias.dropna()

# Renomear as colunas para melhor legibilidade
janelas_500_dias.columns = ["data_final", "retorno_selic_500d", "data_inicial"]

# Pegar o maior retorno da tabela
maior_retorno = janelas_500_dias["retorno_selic_500d"].max()
gabarito = janelas_500_dias[janelas_500_dias["retorno_selic_500d"] == maior_retorno]

# Dashboard
fig, axs = plt.subplots(3, 1, figsize=(10, 15))


axs[0].plot(taxas_selic.index, capital_acumulado, label="Capital Acumulado", color="blue")
axs[0].set_title('Evolução do Capital Investido com SELIC')
axs[0].set_xlabel('Data')
axs[0].set_ylabel('Capital Acumulado (R$)')
axs[0].legend()
axs[0].grid(True)

capital_com_frequencia_diff = capital_com_frequencia.diff().dropna()
axs[1].bar(capital_com_frequencia_diff.index, capital_com_frequencia_diff, color='green')
axs[1].set_title('Lucro Acumulado por Frequência')
axs[1].set_xlabel('Data')
axs[1].set_ylabel('Lucro (R$)')
axs[1].grid(True)


axs[2].plot(janelas_500_dias['data_final'], janelas_500_dias['retorno_selic_500d'], label="Retorno SELIC em 500 Dias", color="red")
axs[2].set_title('Rentabilidade das Janelas de 500 Dias')
axs[2].set_xlabel('Data Final')
axs[2].set_ylabel('Rentabilidade (%)')
axs[2].legend()
axs[2].grid(True)


print(f'Maior Retorno em Janela de 500 Dias: {maior_retorno:.2%}')
print(gabarito)

plt.tight_layout()
plt.show()
