# pylint: disable=missing-module-docstring
import duckdb
import streamlit as st
import polars as pl
import init_db


class StreamlitApp:
    """Class to encapsulate the Streamlit app functionalities"""

    def __init__(self):
        self.attr = {
            "connexion": duckdb.connect(
                database="data/exercises_sql_tables.duckdb", read_only=False
            ),
            "selected_theme": None,
            "selected_exercise": None,
            "solution_query": None,
            "solution_df": None,
            "most_ancient_reviewed_exercise": None,
            "attempt_query": None,
            "attempt_df": None,
            "user_name": None,
            "exercises": None,
            "themes": self.get_themes(),
        }
        self.attr["attempt_result_tab"], self.attr["solution_tab"] = st.tabs(
            [
                "Attempt Result",
                "Solution",
            ]
        )

    def run(self) -> None:
        """Encapsulate the main flow of the Streamlit app"""
        init_db.main()
        self.header()
        self.side_bar()
        self.display_selected_exercise_context()
        self.attempt_query_field()
        self.attempt_result_vs_expected_df_comparison()
        self.display_solution()
        # self.con.close()

    def header(self) -> None:
        """Display the header of the Streamlit app"""
        st.write("# SQL SRS")
        st.write("(Spaced Repetition System SQL Practice)")
        st.write(f"\nHello {self.attr['user_name']}!")

    def get_themes(self) -> list[str]:
        """Gets all the existing themes in the exercises database"""
        return [
            elt[0]
            for elt in self.attr["connexion"]
            .execute(
                """
                SELECT DISTINCT theme
                FROM exercises_list
            """
            )
            .fetchall()
        ]

    def theme_select_box(self) -> None:
        """Display a select box for all existing themes,"""
        self.attr["selected_theme"] = st.selectbox(
            label="What would you like to review?",
            options=self.attr["themes"],
            index=None,
            placeholder="Select a theme",
        )
        if self.attr["selected_theme"]:
            st.write("You selected:", self.attr["selected_theme"])
        else:
            st.write("No theme selected.")

    def get_exercises(self) -> list[str]:
        """Get the exercises list, theme (or not if none selected) related"""
        if self.attr["selected_theme"]:
            sidebar_query = """
                SELECT exercise_name
                FROM exercises_list
                WHERE theme = ?
                ORDER BY last_reviewed
            """
            result = (
                self.attr["connexion"]
                .execute(sidebar_query, [self.attr["selected_theme"]])
                .fetchall()
            )
        else:
            sidebar_query = """
                SELECT exercise_name
                FROM exercises_list
                ORDER BY last_reviewed
            """
            result = self.attr["connexion"].execute(sidebar_query).fetchall()

        return [elt[0] for elt in result]

    def exercise_select_box(self) -> None:
        """
        Display a select box for all selected theme related exercise,
        and return the selected exercise name
        """
        self.attr["exercises"] = self.get_exercises()

        if self.attr["selected_theme"]:
            st.write(f'{self.attr["selected_theme"]} related exercises:')
        else:
            st.write("No theme selected. Any exercise can be selected.")
        self.attr["selected_exercise"] = st.selectbox(
            label="Which exercise would you like to do?",
            options=self.attr["exercises"],
            index=None,
            placeholder="Select an exercise",
        )

    def set_exercise_context(self) -> None:
        """Set the proper answer and the expected df"""
        # self.attr["selected_exercise_subject"] = ""
        # self.attr["selected_exercise_df"] = []
        if self.attr["selected_exercise"]:
            with open(
                f'answers/{self.attr["selected_exercise"]}.sql',
                "r",
                encoding="utf-8",
            ) as f:
                self.attr["solution_query"] = f.read()
            self.attr["solution_df"] = (
                self.attr["connexion"].execute(self.attr["solution_query"]).df()
            )

    def side_bar(self) -> None:
        """Display the sidebar, to choose the theme and exercise"""
        with st.sidebar:
            self.theme_select_box()
            self.exercise_select_box()
            self.set_exercise_context()

    def display_selected_exercise_context(self) -> None:
        """Display selected exercise context (except the proper query and the expected df)"""
        st.write(f'Selected theme: {self.attr["selected_theme"]}')
        st.write(f'Selected exercise: {self.attr["selected_exercise"]}')
        st.write('Selected exercise subject: self.attr["selected_exercise_subject"]')
        st.write('Selected exercise df(s): self.attr["selected_exercise_df"]')

    def attempt_query_field(self) -> None:
        """Section to attempt the exercise and compare with the expected answer"""
        self.attr["attempt_query"] = st.text_area(label="Type your query here:")
        if (
            self.attr["attempt_query"] is not None
            and self.attr["attempt_df"] is not None
        ):
            self.attr["attempt_df"] = (
                self.attr["connexion"].execute(self.attr["attempt_query"]).df()
            )
            st.dataframe(self.attr["attempt_df"])

    def attempt_result_vs_expected_df_comparison(self) -> None:
        """
        Compare the attempt result df with the expected df
        according to the selected exercise expected df
        """
        with self.attr["attempt_result_tab"]:
            if (
                self.attr["attempt_df"] is not None
                and self.attr["solution_df"] is not None
            ):
                try:
                    assert self.attr["attempt_df"].equals(self.attr["solution_df"])
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
                if (
                    delta := abs(
                        self.attr["attempt_df"].shape[0]
                        - self.attr["solution_df"].shape[0]
                    )
                ) != 0:
                    st.write(f"{delta} lines are missing.")

    def display_solution(self) -> None:
        """
        Display solution query and solution df in the dedicated solution tab.
        """
        with self.attr["solution_tab"]:
            if self.attr["solution_query"] is not None:

                st.write("Solution Query:")
                st.code(self.attr["solution_query"])
                st.dataframe(
                    self.attr["connexion"].execute(self.attr["solution_query"]).df()
                )


if __name__ == "__main__":
    streamlit_app = StreamlitApp()
    streamlit_app.run()
