import os
import logging
import requests
import pandas as pd
from sqlalchemy import create_engine

# Configuração de Logs
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def extract_currency_data():
    """Extrai cotações da API pública Open Exchange."""
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

def load_to_sql(df, table_name="cotacoes_moedas"):
    """
    Grava os dados no banco SQL.
    Prioriza a DATABASE_URL do PostgreSQL na nuvem; caso não exista, usa SQLite local.
    """
    db_url = os.getenv("DATABASE_URL")
    
    if db_url:
        logging.info("Conectando ao banco PostgreSQL na nuvem (Supabase)...")
        # Garante o uso explícito do driver psycopg2 instalado
        if db_url.startswith("postgres://"):
            db_url = db_url.replace("postgres://", "postgresql+psycopg2://", 1)
        elif db_url.startswith("postgresql://") and not db_url.startswith("postgresql+psycopg2://"):
            db_url = db_url.replace("postgresql://", "postgresql+psycopg2://", 1)
            
        engine = create_engine(db_url)
    else:
        logging.info("DATABASE_URL não configurada. Usando SQLite local...")
        engine = create_engine("sqlite:///warehouse.db")

    logging.info(f"Salvando dados na tabela SQL '{table_name}'...")
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