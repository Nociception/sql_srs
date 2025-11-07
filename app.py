# pylint: disable=missing-module-docstring
import ast
import duckdb
import streamlit as st
import polars as pl


st.write("# SQL SRS")

st.write("Spaced Repetition System SQL Practice")

con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)


with st.sidebar:
    theme = st.selectbox(
        "What would you like to review?",
        ("cross_joins", "GroupBy", "Windows Functions"),
        index=None,
        placeholder="Select a theme",
    )

    exercise = None
    if theme:
        st.write("You selected:", theme)

        sidebar_query = """
            SELECT *
            FROM memory_state
            WHERE theme = ?
        """
        exercise = con.execute(sidebar_query, [theme]).df()
        st.write(exercise)

        answer_filename = exercise.loc[0]["exercise_name"].strip()
        st.write(answer_filename)
        with open(f"/home/nociception/dus/sql_srs/answers/{answer_filename}.sql", "r") as f:
            answer_query = f.read()
        answer_df = con.execute(answer_query).df()


# allowed_tables = con.execute("SHOW TABLES").df()["name"].to_list()
attempt_query = st.text_area(label="Type your query here")
attemp_df = None
if attempt_query:
    attemp_df = con.execute(attempt_query).df()
    st.dataframe(attemp_df)

if attemp_df is not None:
    try:
        assert attemp_df.equals(answer_df)
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
    if (delta := abs(attemp_df.shape[0] - answer_df.shape[0])) != 0:
        st.write(f"{delta} lines are missing.")
        # st.dataframe(attemp_df)
        # st.write("Expected")
        # st.dataframe(solution_df)


tab1, tab2 = st.tabs(
    [
        "Table",
        "Solution",
    ]
)

with tab1:
    if exercise is not None:
        st.write("Exercise Data:")
        st.dataframe(exercise)
        exercise_table = ast.literal_eval(exercise.loc[0]["tables"].strip())
        st.write(f"Exercise Table: {exercise_table}")
        for table in exercise_table:
            st.write(table)
            st.dataframe(con.execute(f"""
                SELECT *
                FROM {table}
            """).df())

        

with tab2:
    if exercise is not None:
        st.write("Solution Query:")
        st.code(answer_query)
        st.dataframe(con.execute(answer_query).df())

con.close()