# pylint: disable=missing-module-docstring
import ast
import duckdb
import streamlit as st
import polars as pl
import init_db


class StreamlitApp:
    """Class to encapsulate the Streamlit app functionalities"""

    def __init__(self):
        self.con = duckdb.connect(
            database="data/exercises_sql_tables.duckdb", read_only=False
        )
        self.theme = None
        self.answer_query = None
        self.answer_df = None
        self.most_ancient_reviewed_exercise = None
        init_db.main()
        self.header()
        self.side_bar()
        self.attempt_section()
        self.con.close()

    def header(self):
        """Display the header of the Streamlit app"""
        st.write("# SQL SRS")
        st.write("Spaced Repetition System SQL Practice")

    def side_bar(self):
        """Display the sidebar, to choose the theme and exercise"""
        with st.sidebar:
            self.theme = st.selectbox(
                "What would you like to review?",
                ("cross_joins", "GroupBy", "Windows Functions"),
                index=None,
                placeholder="Select a theme",
            )

            exercise = None
            if self.theme:
                st.write("You selected:", self.theme)

                sidebar_query = """
                    SELECT *
                    FROM exercises_list
                    WHERE theme = ?
                    ORDER BY last_reviewed ASC
                """
                exercise = self.con.execute(sidebar_query, [self.theme]).df()

                st.write(f"{self.theme} related exercises:")
                st.dataframe(exercise)

                self.most_ancient_reviewed_exercise = exercise.loc[0][
                    "exercise_name"
                ].strip()

                answer_filename = exercise.loc[0]["exercise_name"].strip()
                with open(
                    f"answers/{answer_filename}.sql",
                    "r",
                    encoding="utf-8",
                ) as f:
                    self.answer_query = f.read()
                self.answer_df = self.con.execute(self.answer_query).df()

    def attempt_section(self):
        """Section to attempt the exercise and compare with the expected answer"""
        attempt_query = st.text_area(label="Type your query here")
        attempt_df = None
        if attempt_query:
            attempt_df = self.con.execute(attempt_query).df()
            st.dataframe(attempt_df)

        if attempt_df is not None and self.answer_df is not None:
            try:
                assert attempt_df.equals(self.answer_df)
            except AttributeError:
                st.write("Please enter a valid query")
            except pl.exceptions.ColumnNotFoundError:
                st.write("Some columns are missing")
            except AssertionError:
                st.markdown(
                    "<span style='color:red; font-weight:bold'>"
                    "Error: some values are not the same!</span>",
                    unsafe_allow_html=True,
                )
            if (delta := abs(attempt_df.shape[0] - self.answer_df.shape[0])) != 0:
                st.write(f"{delta} lines are missing.")

        tab1, tab2 = st.tabs(
            [
                "Table",
                "Solution",
            ]
        )

        with tab1:
            if self.most_ancient_reviewed_exercise is not None:
                st.write(
                    f"Most ancient reviewed exercise: {self.most_ancient_reviewed_exercise}"
                )

                exercise_table = ast.literal_eval(
                    self.con.execute(
                        f"""
                    SELECT tables
                    FROM exercises_list
                    WHERE exercise_name = '{self.most_ancient_reviewed_exercise}'
                """
                    )
                    .df()
                    .loc[0, "tables"]
                )
                st.write("Exercises tables:")
                for table in exercise_table:
                    st.write(table)
                    st.dataframe(
                        self.con.execute(
                            f"""
                            SELECT *
                            FROM {table}
                        """
                        ).df()
                    )

        with tab2:
            if self.most_ancient_reviewed_exercise is not None:
                st.write("Solution Query:")
                st.code(self.answer_query)
                st.dataframe(self.con.execute(self.answer_query).df())


if __name__ == "__main__":
    StreamlitApp()
