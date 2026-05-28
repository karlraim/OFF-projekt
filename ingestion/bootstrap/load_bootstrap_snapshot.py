from pathlib import Path
import duckdb
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
import os

load_dotenv()


BOOTSTRAP_DATASET_PATH = Path("data/bootstrap/ee_products_bootstrap.parquet")


def get_postgres_connection():
    """
    PostgreSQL ühendus warehouse'i.
    """

    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
    )


def recreate_raw_table(cursor, columns):
    """
    Drop + recreate strategy.

    MVP/full refresh lähenemine.
    """

    create_columns_sql = ", ".join([f'"{column}" TEXT' for column in columns])

    cursor.execute(f"""
        DROP TABLE IF EXISTS raw.raw_products CASCADE;

        CREATE TABLE raw.raw_products (
            {create_columns_sql}
        );
    """)


def load_bootstrap_snapshot():
    """
    Laeb bootstrap parquet dataseti PostgreSQL raw layerisse.
    """

    if not BOOTSTRAP_DATASET_PATH.exists():

        raise FileNotFoundError(
            f"Bootstrap dataset puudub: " f"{BOOTSTRAP_DATASET_PATH}"
        )

    print(f"Laen bootstrap datasetti: " f"{BOOTSTRAP_DATASET_PATH}")

    # DuckDB kasutatakse parquet lugemiseks

    con = duckdb.connect()

    postgres_conn = get_postgres_connection()

    postgres_conn.autocommit = True

    cursor = postgres_conn.cursor()

    print("Loen parquet faili DuckDB kaudu...")

    duckdb_relation = con.execute(f"""
        SELECT *
        FROM read_parquet(
            '{BOOTSTRAP_DATASET_PATH}'
        )
    """)

    # Veerunimed DuckDB metadata põhjal

    columns = [description[0] for description in duckdb_relation.description]

    rows = duckdb_relation.fetchall()

    print(f"Laetud read parquet failist: {len(rows):,}")

    print("Loon raw.raw_products tabeli...")

    recreate_raw_table(cursor, columns)

    print("Kirjutan PostgreSQL raw layerisse...")

    insert_query = sql.SQL("""
        INSERT INTO raw.raw_products ({fields})
        VALUES ({values})
    """).format(
        fields=sql.SQL(", ").join(map(sql.Identifier, columns)),
        values=sql.SQL(", ").join(sql.Placeholder() * len(columns)),
    )

    cursor.executemany(
        insert_query,
        rows,
    )

    print(f"PostgreSQL kirjutatud read: {len(rows):,}")

    cursor.close()
    postgres_conn.close()
    con.close()

    print("Bootstrap ingest lõpetatud")


if __name__ == "__main__":
    load_bootstrap_snapshot()
