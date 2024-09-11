import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import mplcyberpunk
import win32com.client as win32


tickers = ["^BVSP", "^GSPC", "BRL=X"]

dados_mercado = yf.download(tickers, period = "6mo")
dados_mercado = dados_mercado["Adj Close"]
dados_mercado

dados_mercado = dados_mercado.dropna()

dados_mercado

dados_mercado.columns = ["DOLAR", "IBOVESPA", "S&P500"]

dados_mercado

#gráfico
plt.style.use("cyberpunk")
plt.plot(dados_mercado["IBOVESPA"])
plt.title("IBOVESPA")
plt.savefig("ibovespa.png")

plt.plot(dados_mercado["DOLAR"])
plt.title("DOLAR")

plt.savefig("dolar.png")

plt.plot(dados_mercado["S&P500"])
plt.title("S&P500")

plt.savefig("sp500.png")

#retorno diário
retornos_diarios = dados_mercado.pct_change()

retornos_diarios

retornos_diarios["DOLAR"].iloc[-3]

retorno_dolar = retornos_diarios["DOLAR"].iloc[-1]
retorno_ibovespa = retornos_diarios["IBOVESPA"].iloc[-1]
retorno_sp = retornos_diarios["S&P500"].iloc[-1]

retorno_dolar = str(round(retorno_dolar * 100, 2)) + "%"

retorno_dolar

retorno_ibovespa = str(round(retorno_ibovespa * 100, 2)) + "%"
retorno_sp = str(round(retorno_sp * 100, 2)) + "%"

retorno_sp

retorno_ibovespa


#enviar por email

outlook = win32.Dispatch("outlook.application")

email = outlook.CreateItem(0)

email.To = "musica12hhh@gmail.com"
email.Subject = "Relatório de Mercado"
email.Body = f'''Segue o relatório de mercado:

* O Ibovespa teve o retorno de {retorno_ibovespa}.
* O Dólar teve o retorno de {retorno_dolar}.
* O S&P500 teve o retorno de {retorno_sp}.

Segue em anexo a peformance dos ativos nos últimos 6 meses.


'''

anexo_ibovespa = r"D:\www\Financias com python\ibovespa.png"
anexo_dolar = r"D:\www\Financias com python\dolar.png"
anexo_sp = r"D:\www\Financias com python\sp500.png"

email.Attachments.Add(anexo_ibovespa)
email.Attachments.Add(anexo_dolar)
email.Attachments.Add(anexo_sp)

email.Send()