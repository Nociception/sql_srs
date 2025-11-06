import duckdb


con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)

con.execute("""
    CREATE OR REPLACE TABLE memory_state AS SELECT *
    FROM read_json("exercises_list.json")
    """
)

con.execute("""
    CREATE OR REPLACE TABLE beverages AS SELECT *
    FROM read_csv("beverages.csv")
    """
)

con.execute("""
    CREATE OR REPLACE TABLE food_items AS SELECT *
    FROM read_csv("food_items.csv")
    """
)

con.close()