import logging
import requests
import pandas as pd
from sqlalchemy import create_engine

# Configuração de Logs
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def extract_currency_data():
    """Extrai cotações da API pública Open Exchange (compatível com servidores em nuvem)."""
    url = "https://open.er-api.com/v6/latest/USD"
    logging.info("Buscando dados da API...")
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()

def transform_data(raw_data):
    """Limpa e formata as taxas de conversão de USD para BRL e EUR."""
    logging.info("Tratando dados com Pandas...")
    rates = raw_data.get("rates", {})
    last_update = raw_data.get("time_last_update_utc")
    
    records = [
        {
            "moeda_base": "USD",
            "moeda_destino": "BRL",
            "taxa_conversao": float(rates.get("BRL", 0.0)),
            "data_atualizacao": last_update
        },
        {
            "moeda_base": "USD",
            "moeda_destino": "EUR",
            "taxa_conversao": float(rates.get("EUR", 0.0)),
            "data_atualizacao": last_update
        }
    ]
    df = pd.DataFrame(records)
    return df

def load_to_sql(df, db_name="warehouse.db", table_name="cotacoes_moedas"):
    """Grava os dados na tabela SQL."""
    logging.info(f"Salvando dados na tabela SQL '{table_name}'...")
    engine = create_engine(f"sqlite:///{db_name}")
    df.to_sql(table_name, con=engine, if_exists="append", index=False)
    logging.info("Carga concluída com sucesso!")

def run_pipeline():
    try:
        raw = extract_currency_data()
        df = transform_data(raw)
        load_to_sql(df)
        print("\n--- AMOSTRA DOS DADOS SALVOS NO SQL ---")
        print(df)
    except Exception as e:
        logging.error(f"Falha na execução do pipeline: {e}")
        raise

if __name__ == "__main__":
    run_pipeline()