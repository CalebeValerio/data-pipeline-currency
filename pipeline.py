import logging
import requests
import pandas as pd
from sqlalchemy import create_engine

# Configuração de Logs
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def extract_currency_data():
    """Extrai cotacoes com cabecalho simulando navegador para evitar bloqueio 429."""
    url = "https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    logging.info("Buscando dados da API...")
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    return response.json()

def transform_data(raw_data):
    """Limpa e formata os dados com Pandas."""
    logging.info("Tratando dados com Pandas...")
    records = []
    for pair_key, values in raw_data.items():
        records.append({
            "par_moedas": values.get("name"),
            "codigo": values.get("code"),
            "cotacao_compra": float(values.get("bid", 0.0)),
            "cotacao_venda": float(values.get("ask", 0.0)),
            "data_hora_consulta": values.get("create_date")
        })
    df = pd.DataFrame(records)
    return df

def load_to_sql(df, db_name="warehouse.db", table_name="cotacoes_moedas"):
    """Grava os dados na tabela SQL local."""
    logging.info(f"Salvando dados na tabela SQL '{table_name}'...")
    engine = create_engine(f"sqlite:///{db_name}")
    df.to_sql(table_name, con=engine, if_exists="append", index=False)
    logging.info("Carga concluida com sucesso!")

def run_pipeline():
    try:
        raw = extract_currency_data()
        df = transform_data(raw)
        load_to_sql(df)
        print("\n--- AMOSTRA DOS DADOS SALVOS NO SQL ---")
        print(df)
    except Exception as e:
        logging.error(f"Falha na execucao do pipeline: {e}")
        # Lanca a excecao para gerar Exit Code 1 no terminal/orquestrador
        raise

if __name__ == "__main__":
    run_pipeline()