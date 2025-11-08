# pylint: disable=missing-module-docstring
import duckdb


def main():
    """Initialize the db"""
    with duckdb.connect(
        database="data/exercises_sql_tables.duckdb", read_only=False
    ) as con:
        con.execute(
            """
            CREATE OR REPLACE TABLE memory_state AS SELECT *
            FROM read_csv("exercises_list.csv")
            """
        )

        con.execute(
            """
            CREATE OR REPLACE TABLE beverages AS SELECT *
            FROM read_csv("beverages.csv")
            """
        )

        con.execute(
            """
            CREATE OR REPLACE TABLE food_items AS SELECT *
            FROM read_csv("food_items.csv")
            """
        )

        con.execute(
            """
            CREATE OR REPLACE TABLE sizes AS SELECT *
            FROM read_csv("sizes.csv")
            """
        )

        con.execute(
            """
            CREATE OR REPLACE TABLE trademarks AS SELECT *
            FROM read_csv("trademarks.csv")
            """
        )


if __name__ == "__main__":
    main()
