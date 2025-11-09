# pylint: disable=missing-module-docstring
import os
import duckdb


def main():
    """Initialize the db"""
    with duckdb.connect(
        database="data/exercises_sql_tables.duckdb", read_only=False
    ) as con:
        for filename in os.listdir("data"):
            if filename.endswith(".csv"):
                con.execute(
                    f"""
                    CREATE OR REPLACE TABLE {filename[:-4]} AS SELECT *
                    FROM read_csv("data/{filename}")
                """
                )
            elif filename.endswith(".parquet"):
                con.execute(
                    f"""
                    CREATE OR REPLACE TABLE {filename[:-8]} AS SELECT *
                    FROM read_parquet("data/{filename}")
                """
                )


if __name__ == "__main__":
    main()
