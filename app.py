# pylint: disable=missing-module-docstring
# import polars as pl
import duckdb
import streamlit as st
import init_db

@st.cache_resource
def init_db_and_get_connection() -> duckdb.DuckDBPyConnection:
    """
    Initialize duckdb database.
    Return a DuckDB connection.
    (function `st.cache_resource` decorated: run only one time)
    """
    init_db.main()
    return duckdb.connect("data/exercises_sql_tables.duckdb", read_only=False)


class StreamlitApp:
    """
    Class to encapsulate the Streamlit app functionalities
    """
    def __init__(self, connection):
        """TODO initialize all these session_state variables with a dict, in specific commit"""
        self.con = connection
        st.session_state.setdefault("themes", self.get_themes())
        st.session_state.setdefault("selected_theme", None)
        st.session_state.setdefault("exercises", [])
        st.session_state.setdefault("selected_exercise", None)
        st.session_state.setdefault("solution_query", None)
        st.session_state.setdefault("solution_df", None)
        st.session_state.setdefault("attempt_query", None)
        # st.session_state.setdefault("attempt_df", None)
        
    def header(self) -> None:
        """Display the app header."""
        st.title("SQL Training App")
        st.write("(SQL Spaced Repetition System)")

    def get_themes(self) -> list[str]:
        """Gets all the existing themes in the exercises database"""
        return [
            elt[0]
            for elt in self.con
            .execute(
                """
                SELECT DISTINCT theme
                FROM exercises_list
            """
            )
            .fetchall()
        ]

    def theme_select_box(self) -> None:
        """
        Theme select box in the sidebar.
        `key` field stores `selected_theme` in the session_state.
        """
        st.selectbox(
            "Select a theme",
            options=st.session_state.themes,
            key="selected_theme",
            placeholder="No theme selected",
            index=None,
        )

    def get_exercises(self) -> list[str]:
        """Get the exercises list, theme (or not if none selected) related"""
        result: None | list = None
        sidebar_query: None | str = None
        if st.session_state.selected_theme:
            sidebar_query = """
                SELECT exercise_name
                FROM exercises_list
                WHERE theme = ?
                ORDER BY last_reviewed
            """
            result = (
                self.con
                .execute(sidebar_query, [st.session_state.selected_theme])
                .fetchall()
            )
        else:
            sidebar_query = """
                SELECT exercise_name
                FROM exercises_list
                ORDER BY last_reviewed
            """
            result = self.con.execute(sidebar_query).fetchall()

        return [elt[0] for elt in result]

    def exercise_select_box(self) -> None:
        """
        Exercise select box in the sidebar.
        `key` field stores `selected_exercise` in the session_state.
        """
        if st.session_state.selected_theme is not None:
            st.write(f'{st.session_state.selected_theme} related exercises:')
        else:
            st.write("No theme selected. Any exercise can be selected.")

        st.selectbox(
            "Select an exercise",
            options=st.session_state.exercises,
            key="selected_exercise",
            placeholder="No exercise selected",
            index=None,
        )

    def side_bar(self) -> None:
        """Display the sidebar, to choose the theme and exercise"""
        with st.sidebar:
            self.theme_select_box()
            st.session_state.exercises = self.get_exercises()
            self.exercise_select_box()

    def set_exercise_context(self) -> None:
        """
        Once an exercise is selected, store in `session_state`:
        - `solution_query`
        - `solution_df`
        - TODO: `subject` into the .sql file
        """
        if "selected_exercise" in st.session_state and st.session_state["selected_exercise"] is not None:
            with open(
                f'answers/{st.session_state["selected_exercise"]}.sql',
                "r",
                encoding="utf-8",
            ) as f:
                st.session_state["solution_query"] = f.read()
            st.session_state["solution_df"] = (
                self.con.execute(st.session_state["solution_query"]).df()
            )

    def attempt_query_area(self) -> None:
        """
        Provide a text area allowing user to type a query to answer the selected exercise.
        `key` field stores `attempt_query` in the session_state.
        """
        st.text_area(
            "Type your SQL query:",
            value=st.session_state.setdefault("attempt_query", ""),
            key="attempt_query",
        )

    def attempt_tab(self) -> None:
        """"""
        pass

    def solution_tab(self) -> None:
        """"""
        pass

    def tabs(self) -> None:
        """"""
        attempt_tab, solution_tab = st.tabs(
            [
                "Attempt",
                "Solution",
            ]
        )
        with attempt_tab:
            self.attempt_tab()
        with solution_tab:
            self.solution_tab()
#         self.display_result_tab()


#    def attempt_result_vs_expected_df_comparison(self) -> None:
#         """
#         Compare the attempt result df with the expected df
#         according to the selected exercise expected df
#         """
#         with self.attr["attempt_result_tab"]:
#             if (
#                 self.attr["attempt_df"] is not None
#                 and self.attr["solution_df"] is not None
#             ):
#                 try:
#                     assert self.attr["attempt_df"].equals(self.attr["solution_df"])
#                 except AttributeError:
#                     st.write("Please enter a valid query")
#                 except pl.exceptions.ColumnNotFoundError:
#                     st.write("Some columns are missing")
#                 except AssertionError:
#                     st.markdown(
#                         "<span style='color:red; font-weight:bold'>"
#                         "Error: some values are not the same!</span>",
#                         unsafe_allow_html=True,
#                     )
#                 if (
#                     delta := abs(
#                         self.attr["attempt_df"].shape[0]
#                         - self.attr["solution_df"].shape[0]
#                     )
#                 ) != 0:
#                     st.write(f"{delta} lines are missing.")


#     def display_solution(self) -> None:
#         """
#         Display solution query and solution df in the dedicated solution tab.
#         """
#         with self.attr["solution_tab"]:
#             if self.attr["solution_query"] is not None:

#                 st.write("Solution Query:")
#                 st.code(self.attr["solution_query"])
#                 st.dataframe(
#                     self.attr["connection"].execute(self.attr["solution_query"]).df()
#                 )


    def run(self) -> None:
        """Encapsulate the main flow of the Streamlit app"""
        self.header()
        self.side_bar()
        self.set_exercise_context()
        self.attempt_query_area()
        self.tabs()
#         remind to clean the current exercise variables after an exercise attempt session done (signaled from the user ?)



if "app" not in st.session_state:
    st.session_state.app = StreamlitApp(init_db_and_get_connection())

st.session_state.app.run()