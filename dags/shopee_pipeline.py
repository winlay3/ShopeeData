import os
from datetime import datetime
from airflow.sdk import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.decorators import task
from elasticsearch import Elasticsearch, helpers

BASE_PATH = "/opt/airflow/dags/shopee_project"
DATA_PATH = os.path.join(BASE_PATH, "data")
SQL_PATH  = os.path.join(BASE_PATH, "sql", "schema.sql")
TRANSFORM_PATH = os.path.join(BASE_PATH, "sql", "transform.sql")

def load_csv_to_pg(table_name, csv_filename):
    hook = PostgresHook(postgres_conn_id="shopee_pg")
    conn = hook.get_conn()
    cursor = conn.cursor()
    cursor.execute(f"TRUNCATE TABLE {table_name} RESTART IDENTITY CASCADE;")
    filepath = os.path.join(DATA_PATH, csv_filename)
    with open(filepath, "r", encoding="utf-8") as f:
        next(f)
        cursor.copy_expert(
            f"COPY {table_name} FROM STDIN WITH CSV",
            f
        )
    conn.commit()
    cursor.close()
    conn.close()

with DAG(
    dag_id="shopee_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    tags=["shopee"],
) as dag:

    create_tables = SQLExecuteQueryOperator(
        task_id="create_tables",
        conn_id="shopee_pg",
        sql=open(SQL_PATH).read(),
    )

    @task
    def load_orders():
        load_csv_to_pg("raw_orders", "shopee_orders_thailand.csv")

    @task
    def load_order_items():
        load_csv_to_pg("raw_order_items", "shopee_order_items_thailand.csv")

    @task
    def load_products():
        load_csv_to_pg("raw_products", "shopee_products_thailand.csv")

    @task
    def transform_joined():
        hook = PostgresHook(postgres_conn_id="shopee_pg")
        conn = hook.get_conn()
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS mart_orders_enriched;")
        cursor.execute(open(TRANSFORM_PATH).read())
        conn.commit()
        cursor.close()
        conn.close()


    @task
    def load_to_elasticsearch():
        es = Elasticsearch(
            "http://host.docker.internal:9200",
            verify_certs=False,
            ssl_show_warn=False
        )
        # create index if it doesn't exist
        if not es.indices.exists(index="shopee_orders_enriched"):
            es.indices.create(index="shopee_orders_enriched")

        hook = PostgresHook(postgres_conn_id="shopee_pg")
        conn = hook.get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM mart_orders_enriched;")
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        cursor.close()
        conn.close()

        docs = []
        for row in rows:
            doc = dict(zip(columns, row))
            for key, val in doc.items():
                if hasattr(val, 'isoformat'):
                    doc[key] = val.isoformat()
            docs.append({
                "_index": "shopee_orders_enriched",
                "_id": f"{doc['order_id']}_{doc['order_item_id']}",
                "_source": doc
            })

        # print errors instead of raising exception
        success, failed = helpers.bulk(es, docs, raise_on_error=False)
        print(f"Success: {success}")
        print(f"Failed: {len(failed)}")
        for f in failed[:5]:  # print first 5 errors only
            print(f)

        

    # Dependencies
    create_tables >> [load_orders(), load_order_items(), load_products()] >> transform_joined() >> load_to_elasticsearch()