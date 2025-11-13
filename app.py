# pylint: disable=missing-module-docstring
import duckdb
import streamlit as st
from init_db import init_db


@st.cache_resource
def init_db_and_get_connection() -> duckdb.DuckDBPyConnection:
    """
    Initialize duckdb database.
    Return a DuckDB connection.
    (function `st.cache_resource` decorated: run only one time per session)
    """
    init_db()
    return duckdb.connect("data/exercises_sql_tables.duckdb", read_only=False)


class StreamlitApp:
    """Class to encapsulate the Streamlit app functionalities."""

    def __init__(self, connection):
        self.con = connection

        defaults = {
            "themes": self.get_themes(),
            "selected_theme": None,
            "exercises": [],
            "selex": None,
            "selex_tables": [],
            "selex_subject": None,
            "selex_solution_query": None,
            "selex_solution_df": None,
            "attempt_query": None,
            "attempt_df": None,
        }
        for key, value in defaults.items():
            st.session_state.setdefault(key, value)

    def header(self) -> None:
        """Display the app header."""
        st.title("SQL SRS - Training App")
        st.write("(SQL Spaced Repetition System)")

    def get_themes(self) -> list[str]:
        """Gets all the existing themes in the exercises database."""
        return (
            self.con.execute(
                """
            SELECT
                *
            FROM
                themes
        """
            )
            .df()["theme_name"]
            .to_list()
        )

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
        """Return the list of exercise names, optionally filtered by selected theme."""

        if st.session_state.selected_theme:
            query = """
                SELECT
                    e.exercise_name
                FROM
                    exercises AS e
                JOIN
                    exercise_theme AS et ON e.id = et.exercise_id
                JOIN
                    themes AS t ON t.id = et.theme_id
                WHERE
                    t.theme_name = ?
                ORDER BY
                    e.exercise_name
            """
            rows = self.con.execute(query, [st.session_state.selected_theme]).fetchall()

        else:
            query = """
                SELECT
                    exercise_name
                FROM
                    exercises
                ORDER BY
                    exercise_name
            """
            rows = self.con.execute(query).fetchall()

        return [row[0] for row in rows]

    def exercise_select_box(self) -> None:
        """
        Exercise select box in the sidebar.
        `key` field stores `selex` in the session_state.
        """
        if st.session_state.selected_theme is not None:
            st.write(f"{st.session_state.selected_theme} related exercises:")
        else:
            st.write("No theme selected. Any exercise can be selected.")

        st.selectbox(
            "Select an exercise",
            options=st.session_state.exercises,
            key="selex",
            placeholder="No exercise selected",
            index=None,
        )

    def side_bar(self) -> None:
        """Display the sidebar, to choose the theme and exercise."""
        with st.sidebar:
            self.theme_select_box()
            st.session_state.exercises = self.get_exercises()
            self.exercise_select_box()

            st.write(f'Selected theme: {st.session_state["selected_theme"]}')
            st.write(f'Selected exercise: {st.session_state["selex"]}')

    def set_exercise_context(self) -> None:
        """
        Once an exercise is selected, store in `st.session_state`
        by parsing the metadata documented .sql file:
        - `subject`
        - `related table(s)`
        - `selex_solution_query`
        - `selex_solution_df`
        """
        if "selex" in st.session_state and st.session_state["selex"] is not None:
            metadata_pattern: str = "-- "
            sql_lines = []
            with open(
                f'exercises/{st.session_state["selex"]}.sql',
                "r",
                encoding="utf-8",
            ) as sql_file:
                for line in sql_file:
                    if line.startswith(metadata_pattern):
                        if metadata_pattern + "tables:" in line:
                            st.session_state["selex_tables"] = line[
                                line.index(":") + 1 :
                            ].split()
                        elif metadata_pattern + "subject:" in line:
                            st.session_state["selex_subject"] = line[
                                line.index(":") + 1 :
                            ]
                    else:
                        sql_lines.append(line)
            st.session_state["selex_solution_query"] = "".join(sql_lines)
            st.session_state["selex_solution_df"] = self.con.execute(
                st.session_state["selex_solution_query"]
            ).df()
        else:
            st.write("Selex exercise context not set.")

    def display_selex_context(self) -> None:
        """Display selected exercise subject just above the attempt query area."""
        st.write(f'Selected exercise subject:\n{st.session_state["selex_subject"]}')
        st.write(f"Relatad table(s): {', '.join(st.session_state['selex_tables'])}")
        st.write("Selected exercise related table(s):")
        for table in st.session_state["selex_tables"]:
            st.dataframe(
                self.con.execute(
                    f"""
                SELECT
                    *
                FROM
                    '{table}'
            """
                )
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

    def display_attempt_df(self) -> bool:
        """
        Display attempt_df if query is valid.
        TODO identify proper errors in case of invalid queries
        """
        try:
            st.session_state["attempt_df"] = self.con.execute(
                st.session_state["attempt_query"]
            ).df()
            st.write("Your query produces this dataframe:")
            st.dataframe(st.session_state["attempt_df"])
            st.markdown(
                "<span style='color:green'>Check: Query seems valid.</span>",
                unsafe_allow_html=True,
            )
            return True

        except duckdb.Error as e:
            st.error(f"DuckDB error: {e}")
        except (KeyError, TypeError, ValueError, RuntimeError) as e:
            st.error(f"Internal error: {type(e).__name__}: {e}")
        st.markdown(
            "<span style='color:red'>Your query does not seem valid.</span>",
            unsafe_allow_html=True,
        )
        return False

    def shape_checks(self) -> bool:
        """Check if `attempt_df` matches `selex_solution_df`'s shape."""
        if (
            "attempt_df" in st.session_state
            and st.session_state["attempt_df"] is not None
        ):
            attempt_df_shape: tuple[int] = st.session_state["attempt_df"].shape
            solution_df_shape: tuple[int] = st.session_state["selex_solution_df"].shape
            return_value = True

            if (lines_delta := attempt_df_shape[0] - solution_df_shape[0]) != 0:
                delta_message: str = "extra" if lines_delta > 0 else "missing"
                st.write(f"There are {abs(lines_delta)} {delta_message} line(s).")
                return_value = False

            if (columns_delta := attempt_df_shape[1] - solution_df_shape[1]) != 0:
                delta_message: str = "extra" if columns_delta > 0 else "missing"
                st.write(f"There are {abs(columns_delta)} {delta_message} columns(s).")
                return_value = False

            if return_value:
                st.markdown(
                    "<span style='color:green'>Check: Shapes match.</span>",
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    "<span style='color:red'>Shapes do not match.</span>",
                    unsafe_allow_html=True,
                )
            return return_value
        return True

    def values_checks(self) -> bool:
        """Check if `attempt_df`'s values match `solution_df` ones."""
        try:
            assert st.session_state["attempt_df"].equals(
                st.session_state["selex_solution_df"]
            )
            st.markdown(
                "<span style='color:green'>Check: Values match.</span>",
                unsafe_allow_html=True,
            )
            return True
        except AssertionError:
            st.markdown(
                "<span style='color:red'>"
                "Error: some values are not the same!</span>",
                unsafe_allow_html=True,
            )
            return False

    def attempt_tab(self) -> None:
        """
        Handle what is displayed in the attempt tab:
        - `attempt_df` according to user's `attempt_query`
        - comparison between `attempt_df` and `selex_solution_df`,
            without displaying it in this tab; just clues
        #TODO handle success scenario
        """
        if st.session_state["selex_solution_df"] is not None:
            if st.session_state["attempt_query"] is not None:
                if (
                    self.display_attempt_df()
                    and self.shape_checks()
                    and self.values_checks()
                ):
                    st.markdown(
                        "<span style='color:green; font-weight:bold'>"
                        "Success!</span>",
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        "<span style='color:red; font-weight:bold'>"
                        "Your query does not produce the expected dataframe. Try again :)</span>",
                        unsafe_allow_html=True,
                    )
        else:
            st.write(
                "You may select an exercise before trying anything in this query area."
            )

    def solution_tab(self) -> None:
        """
        Display in the solution tab:
        - `selex_solution_query`
        - `selex_solution_df`
        TODO: Add a button to reveal the solution_query
        """
        st.write("Solution query:")
        st.code(st.session_state["selex_solution_query"])
        st.dataframe(st.session_state["selex_solution_df"])

    def tabs(self) -> None:
        """
        TODO: clean the current exercise variables after
        an exercise attempt session done (signaled from the user ?)
        """
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

    def run(self) -> None:
        """Encapsulate the main flow of the Streamlit app"""
        self.header()
        self.side_bar()
        self.set_exercise_context()
        self.display_selex_context()
        self.attempt_query_area()
        self.tabs()


if "app" not in st.session_state:
    st.session_state.app = StreamlitApp(init_db_and_get_connection())

st.session_state.app.run()
