# pylint: disable=missing-module-docstring
import os
import duckdb


def feed_db_from_data_files(con: duckdb.DuckDBPyConnection) -> None:
    """Create a table for each data file in `data` directory"""
    for filename in os.listdir("data"):
        if filename.endswith(".csv"):
            con.execute(
                f"""
                CREATE OR REPLACE TABLE
                    {filename[:-4]} AS SELECT *
                FROM
                    read_csv("data/{filename}")
            """
            )
        elif filename.endswith(".parquet"):
            con.execute(
                f"""
                CREATE OR REPLACE TABLE
                    {filename[:-8]} AS SELECT *
                FROM
                    read_parquet("data/{filename}")
            """
            )


def create_themes_table(con: duckdb.DuckDBPyConnection) -> None:
    """Create `themes` table from `exercises_list` table."""
    con.execute(
        """
        CREATE OR REPLACE TABLE
            themes AS SELECT DISTINCT theme
        FROM
            exercises_list
    """
    )


def init_db() -> None:
    """Initialize the db by creating all the tables the app needs."""
    with duckdb.connect(
        database="data/exercises_sql_tables.duckdb", read_only=False
    ) as con:
        feed_db_from_data_files(con)
        create_themes_table(con)


if __name__ == "__main__":
    init_db()
