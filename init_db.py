# pylint: disable=missing-module-docstring
import os
import duckdb


def main():
    """Initialize the db"""
    with duckdb.connect(
        database="data/exercises_sql_tables.duckdb", read_only=False
    ) as con:
        for csv in os.listdir("data"):
            if csv.endswith(".csv"):
                con.execute(
                    f"""
                    CREATE OR REPLACE TABLE {csv[:-4]} AS SELECT *
                    FROM read_csv("data/{csv}")
                """
                )


if __name__ == "__main__":
    main()
