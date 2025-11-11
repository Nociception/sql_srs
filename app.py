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
    """Class to encapsulate the Streamlit app functionalities"""

    def __init__(self, connection):
        self.con = connection

    def header(self) -> None:
        """
        Display the app header.
        (function `st.cache_resource` decorated: run only one time)
        """
        st.title("# SQL Training App")

    def attempt_query_area(self) -> None:
        """
        Provide a text area allowing user to type a query to answer the selected exercise.
        `key` field stores the `attempt_query` in the session_state.
        """
        st.text_area(
            "Type your SQL query:",
            value=st.session_state.setdefault("attempt_query", ""),
            key="attempt_query",
        )

    def run(self):
        self.header()
        self.attempt_query_area()


if "app" not in st.session_state:
    st.session_state.app = StreamlitApp(init_db_and_get_connection())

st.session_state.app.run()



#         self.attr = {
#             "connection": init_db_and_get_connection(),
#             "selected_theme": None,
#             "selected_exercise": None,
#             "solution_query": None,
#             "solution_df": None,
#             "attempt_query": None,
#             "attempt_df": None,
#             "user_name": None,
#             "exercises": None,
#             "themes": None,
#         }
#         self.attr["themes"] = self.get_themes()

#         for key, value in {
#             "selected_theme": None,
#             "selected_exercise": None,
#             "solution_query": None,
#             "solution_df": None,
#             "attempt_query": "",
#             "attempt_df": None,
#         }.items():
#             st.session_state.setdefault(key, value)

#     def run(self) -> None:
#         """Encapsulate the main flow of the Streamlit app"""
#         
#         self.header()
#         self.side_bar()
#         self.display_selected_exercise_context()
#         self.attempt_query_field()
#         self.display_result_tab()

#     def header(self) -> None:
#         """Display the header of the Streamlit app"""
#         st.write("# SQL SRS")
#         st.write("(SQL Spaced Repetition System)")
#         # st.write(f"\nHello {self.attr['user_name']}!")

#     def side_bar(self) -> None:
#         """Display the sidebar, to choose the theme and exercise"""
#         with st.sidebar:
#             themes = self.get_themes()
#             st.session_state.selected_theme = st.selectbox(
#                 "Theme", options=themes, index=None, placeholder="Select a theme",
#                 key="theme_select"
#             )


#             self.theme_select_box()
#             self.exercise_select_box()
#             self.set_exercise_context()
    
#     def get_themes(self) -> list[str]:
#         """Gets all the existing themes in the exercises database"""
#         return [
#             elt[0]
#             for elt in self.attr["connection"]
#             .execute(
#                 """
#                 SELECT DISTINCT theme
#                 FROM exercises_list
#             """
#             )
#             .fetchall()
#         ]

#     def theme_select_box(self) -> None:
#         """Display a select box for all existing themes,"""
#         self.attr["selected_theme"] = st.selectbox(
#             label="What would you like to review?",
#             options=self.attr["themes"],
#             index=None,
#             placeholder="Select a theme",
#         )
#         if self.attr["selected_theme"]:
#             st.write("You selected:", self.attr["selected_theme"])
#         else:
#             st.write("No theme selected.")

#     def get_exercises(self) -> list[str]:
#         """Get the exercises list, theme (or not if none selected) related"""
#         if self.attr["selected_theme"]:
#             sidebar_query = """
#                 SELECT exercise_name
#                 FROM exercises_list
#                 WHERE theme = ?
#                 ORDER BY last_reviewed
#             """
#             result = (
#                 self.attr["connection"]
#                 .execute(sidebar_query, [self.attr["selected_theme"]])
#                 .fetchall()
#             )
#         else:
#             sidebar_query = """
#                 SELECT exercise_name
#                 FROM exercises_list
#                 ORDER BY last_reviewed
#             """
#             result = self.attr["connection"].execute(sidebar_query).fetchall()

#         return [elt[0] for elt in result]

#     def exercise_select_box(self) -> None:
#         """
#         Display a select box for all selected theme related exercise,
#         and return the selected exercise name
#         """
#         self.attr["exercises"] = self.get_exercises()

#         if self.attr["selected_theme"]:
#             st.write(f'{self.attr["selected_theme"]} related exercises:')
#         else:
#             st.write("No theme selected. Any exercise can be selected.")
#         self.attr["selected_exercise"] = st.selectbox(
#             label="Which exercise would you like to do?",
#             options=self.attr["exercises"],
#             index=None,
#             placeholder="Select an exercise",
#         )

#     def set_exercise_context(self) -> None:
#         """
#         Set the proper answer and the expected df
#         # self.attr["selected_exercise_subject"] = ""
#         # self.attr["selected_exercise_df"] = []
#         """
#         if self.attr["selected_exercise"]:

#             with open(
#                 f'answers/{self.attr["selected_exercise"]}.sql',
#                 "r",
#                 encoding="utf-8",
#             ) as f:
#                 self.attr["solution_query"] = f.read()
#             self.attr["solution_df"] = (
#                 self.attr["connection"].execute(self.attr["solution_query"]).df()
#             )


#     def display_selected_exercise_context(self) -> None:
#         """Display selected exercise context (except the proper query and the expected df)"""
#         st.write(f'Selected theme: {self.attr["selected_theme"]}')
#         st.write(f'Selected exercise: {self.attr["selected_exercise"]}')
#         st.write('Selected exercise subject: self.attr["selected_exercise_subject"]')
#         st.write('Selected exercise df(s): self.attr["selected_exercise_df"]')

#     def attempt_query_field(self) -> None:
#         """Section to attempt the exercise and compare with the expected answer"""
#         self.attr["attempt_query"] = st.text_area(label="Type your query here:")
#         if (
#             self.attr["attempt_query"] is not None
#             and self.attr["attempt_df"] is not None
#         ):
#             self.attr["attempt_df"] = (
#                 self.attr["connection"].execute(self.attr["attempt_query"]).df()
#             )
#             st.dataframe(self.attr["attempt_df"])

#     def attempt_result_vs_expected_df_comparison(self) -> None:
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


