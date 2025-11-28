import requests
import pandas as pd

def collect_renta_per_capita():
    # 1. OBTENER RNB PER CÁPITA EN DÓLARES (US$) DESDE 2015
    url_gni_usd = "http://api.worldbank.org/v2/country/es/indicator/NY.GNP.PCAP.CD?format=json&date=2015:2025"
    response_gni = requests.get(url_gni_usd)
    data_gni = response_gni.json()

    df_gni = pd.DataFrame()
    if len(data_gni) > 1 and data_gni[1]:
        df_gni = pd.DataFrame(data_gni[1])[['date', 'value']].rename(columns={'date': 'Año', 'value': 'RNB per Cápita (US$)'})
        df_gni['Año'] = pd.to_numeric(df_gni['Año'])

    # 2. OBTENER TIPO DE CAMBIO ANUAL (EUR por US$) DESDE 2015
    url_exchange = "http://api.worldbank.org/v2/country/XC/indicator/PA.NUS.FCRF?format=json&date=2015:2025"
    response_exchange = requests.get(url_exchange)
    data_exchange = response_exchange.json()

    df_exchange = pd.DataFrame()
    if len(data_exchange) > 1 and data_exchange[1]:
        df_exchange = pd.DataFrame(data_exchange[1])[['date', 'value']].rename(columns={'date': 'Año', 'value': 'Tipo de Cambio (€ por US$)'})
        df_exchange['Año'] = pd.to_numeric(df_exchange['Año'])

    # 3. UNIR, CONVERTIR Y MOSTRAR RESULTADO
    if not df_gni.empty and not df_exchange.empty:
        df_final = pd.merge(df_gni, df_exchange, on='Año')
        df_final['RNB per Cápita (€)'] = df_final['RNB per Cápita (US$)'] * df_final['Tipo de Cambio (€ por US$)']
        df_resultado = df_final[['Año', 'RNB per Cápita (€)']].sort_values('Año', ascending=False).reset_index(drop=True)
        df_resultado['RNB per Cápita (€)'] = df_resultado['RNB per Cápita (€)'].round(2)
        
        print("RNB per Cápita de España en Euros (desde 2015) guardada")
        df_resultado['pais'] = 'España'
        df_resultado.to_csv('data/raw/WorldBank/rnbpc.csv')
    else:
        print("No se pudieron obtener todos los datos para realizar el cálculo.")
