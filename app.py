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
        self.selected_theme = None
        self.selected_exercise = None
        self.answer_query = None
        self.answer_df = None
        self.most_ancient_reviewed_exercise = None
        self.attempt_query = None
        self.attempt_df = None
        self.user_name = "User"
        self.exercises = None
        self.attempt_result_tab, self.solution_tab = None, None
        self.themes = self.get_themes()
        self.run()

    def run(self) -> None:
        """Encapsulate the main flow of the Streamlit app"""
        init_db.main()
        self.header()
        self.side_bar()
        self.display_selected_exercise_context()
        self.attempt_query_field()
        self.set_tabs()
        self.attempt_result_vs_expected_df_comparison()
        self.con.close()

    def header(self) -> None:
        """Display the header of the Streamlit app"""
        st.write("# SQL SRS")
        st.write("(Spaced Repetition System SQL Practice)")
        st.write(f"\nHello {self.user_name}!")

    def get_themes(self) -> list[str]:
        """Gets all the existing themes in the exercises database"""
        return [
            elt[0]
            for elt in self.con.execute(
                """
                SELECT DISTINCT theme
                FROM exercises_list
            """
            ).fetchall()
        ]

    def theme_select_box(self) -> None:
        """Display a select box for all existing themes, """
        self.selected_theme = st.selectbox(
            label="What would you like to review?",
            options=self.themes,
            index=None,
            placeholder="Select a theme",
        )
        if self.selected_theme:
            st.write("You selected:", self.selected_theme)

    def get_exercises(self) -> list[str]:
        """Get the exercises list, theme (or not if none selected) related"""
        if self.selected_theme:
            sidebar_query = """
                SELECT exercise_name
                FROM exercises_list
                WHERE theme = ?
                ORDER BY last_reviewed
            """
            result = self.con.execute(sidebar_query, [self.selected_theme]).fetchall()
        else:
            sidebar_query = """
                SELECT exercise_name
                FROM exercises_list
                ORDER BY last_reviewed
            """
            result = self.con.execute(sidebar_query).fetchall()

        return [elt[0] for elt in result]

    def exercise_select_box(self) -> None:
        """Display a select box for all selected theme related exercise, and return the selected exercise name"""
        self.exercises = self.get_exercises()

        if self.selected_theme:
            st.write(f"{self.selected_theme} related exercises:")
        else:
            st.write("No theme selected. Any exercise can be selected.")
        self.selected_exercise = st.selectbox(
            label="Which exercise would like to do?",
            options=self.exercises,
            index=None,
            placeholder="Select an exercise"
        )

    def set_exercise_context(self) -> None:
        """Set the proper answer and the expected df"""
        # self.selected_exercise_subject = ""
        # self.selected_exercise_df = []
        if self.selected_exercise:
            with open(
                f"answers/{self.selected_exercise}.sql",
                "r",
                encoding="utf-8",
            ) as f:
                self.answer_query = f.read()
            self.answer_df = self.con.execute(self.answer_query).df()

    def side_bar(self) -> None:
        """Display the sidebar, to choose the theme and exercise"""
        with st.sidebar:
            self.theme_select_box()
            self.exercise_select_box()
            self.set_exercise_context()

    def display_selected_exercise_context(self) -> None:
        """Display selected exercise context (except the proper query and the expected df)"""
        st.write(f"Selected theme: {self.selected_theme}")
        st.write(f"Selected exercise: {self.selected_exercise}")
        st.write(f"Selected exercise subject: self.selected_exercise_subject")
        st.write(f"Selected exercise df(s): self.selected_exercise_df")

    def attempt_query_field(self) -> None:
        """Section to attempt the exercise and compare with the expected answer"""
        self.attempt_query = st.text_area(label="Type your query here")
        if self.attempt_query is not None and self.attempt_df is not None:
            self.attempt_df = self.con.execute(self.attempt_query).df()
            st.dataframe(self.attempt_df)

    def set_tabs(self) -> None:
        """Set attempt result and solution tabs"""
        self.attempt_result_tab, self.solution_tab = st.tabs(
            [
                "Attempt Result",
                "Solution",
            ]
        )

    def attempt_result_vs_expected_df_comparison(self) -> None:
        """Compare the attempt result df with the expected df according to the selected exercise expected df"""
        with self.attempt_result_tab:
            if self.attempt_df is not None and self.answer_df is not None:
                try:
                    assert self.attempt_df.equals(self.answer_df)
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
                if (delta := abs(self.attempt_df.shape[0] - self.answer_df.shape[0])) != 0:
                    st.write(f"{delta} lines are missing.")

    def display_solution(self) -> None:
        with self.solution_tab:
            if self.answer_query is not None:
                st.write("Solution Query:")
                st.code(self.answer_query)
                st.dataframe(self.con.execute(self.answer_query).df())


if __name__ == "__main__":
    StreamlitApp()
