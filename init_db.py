# pylint: disable=missing-module-docstring
import os
from pathlib import Path
import re
import duckdb

DATA_PATH = Path("data/exercises_sql_tables.duckdb")
EXERCISES_DIR = Path("exercises")


def init_db() -> None:
    """
    Initialize DuckDB database with exercises, themes, and association tables.
    Parse .sql files once to populate everything.
    """

    with duckdb.connect(str(DATA_PATH), read_only=False) as con:

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

        con.execute("""
            CREATE SEQUENCE IF NOT EXISTS
                exercise_seq START 1;
        """)
        con.execute("""
            CREATE SEQUENCE IF NOT EXISTS
            theme_seq START 1
        """)

        con.execute("""
            CREATE TABLE IF NOT EXISTS
                exercises (
                    id INTEGER DEFAULT nextval('exercise_seq') PRIMARY KEY,
                    exercise_name TEXT UNIQUE NOT NULL
                )
        """)
        con.execute("""
            CREATE TABLE IF NOT EXISTS
                themes (
                    id INTEGER DEFAULT nextval('theme_seq') PRIMARY KEY,
                    theme_name TEXT UNIQUE NOT NULL
                )
        """)
        con.execute("""
            CREATE TABLE IF NOT EXISTS
                exercise_theme (
                    exercise_id INTEGER NOT NULL,
                    theme_id INTEGER NOT NULL,
                    UNIQUE(exercise_id, theme_id)
                )
        """)

        for sql_file in EXERCISES_DIR.glob("*.sql"):
            exercise_name = sql_file.stem

            con.execute(
                """
                    INSERT OR IGNORE INTO
                        exercises (exercise_name) VALUES (?)
                """,
                [exercise_name],
            )

            exercise_id = con.execute(
                """
                    SELECT
                        id
                    FROM
                        exercises
                    WHERE
                        exercise_name = ?
                """,
                [exercise_name],
            ).fetchone()[0]

            with open(sql_file, "r", encoding="utf-8") as f:
                content = f.read()

            match = re.search(r"--\s*themes:\s*(.+)", content)
            if not match:
                continue

            file_themes = match.group(1).strip().split()

            for theme in file_themes:
                con.execute(
                    """
                        INSERT OR IGNORE INTO
                            themes (theme_name) VALUES (?)
                    """,
                    [theme],
                )

                theme_id = con.execute(
                    """
                        SELECT
                            id
                        FROM
                            themes
                        WHERE
                            theme_name = ?
                    """,
                    [theme],
                ).fetchone()[0]

                con.execute(
                    """
                        INSERT OR IGNORE INTO
                            exercise_theme (exercise_id, theme_id) VALUES (?, ?)
                    """,
                    [exercise_id, theme_id],
                )


if __name__ == "__main__":
    init_db()




# # pylint: disable=missing-module-docstring
# import os
# import duckdb


# def feed_db_from_data_files(con: duckdb.DuckDBPyConnection) -> None:
#     """Create a table for each data file in `data` directory"""
#     for filename in os.listdir("data"):
#         if filename.endswith(".csv"):
#             con.execute(
#                 f"""
#                 CREATE OR REPLACE TABLE
#                     {filename[:-4]} AS SELECT *
#                 FROM
#                     read_csv("data/{filename}")
#             """
#             )
#         elif filename.endswith(".parquet"):
#             con.execute(
#                 f"""
#                 CREATE OR REPLACE TABLE
#                     {filename[:-8]} AS SELECT *
#                 FROM
#                     read_parquet("data/{filename}")
#             """
#             )


# def create_themes_table(con: duckdb.DuckDBPyConnection) -> None:
#     """Create `themes` table from `exercises_list` table."""
#     con.execute(
#         """
#         CREATE OR REPLACE TABLE
#             themes AS SELECT DISTINCT theme
#         FROM
#             exercises_list
#     """
#     )


# def init_db() -> None:
#     """Initialize the db by creating all the tables the app needs."""
#     with duckdb.connect(
#         database="data/exercises_sql_tables.duckdb", read_only=False
#     ) as con:
#         feed_db_from_data_files(con)
#         create_themes_table(con)


# if __name__ == "__main__":
#     init_db()
