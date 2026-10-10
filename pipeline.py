import logging
import requests
import pandas as pd
from sqlalchemy import create_engine

# 1. Configuração de Logs (Padrão de produção para rastrear execuções)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def extract_currency_data():
    """Extrai cotações de moedas em tempo real via API pública."""
    url = "https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL"
    logging.info("Buscando dados da API...")
    response = requests.get(url, timeout=10)
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
    """Grava os dados tratados em uma tabela no banco SQL local."""
    logging.info(f"Salvando dados na tabela SQL '{table_name}'...")
    engine = create_engine(f"sqlite:///{db_name}")
    # O modo 'append' insere novos registros sem apagar o histórico
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

if __name__ == "__main__":
    run_pipeline()