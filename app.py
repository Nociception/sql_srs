# pylint: disable=missing-module-docstring
import ast
import duckdb
import streamlit as st


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


# allowed_tables = con.execute("SHOW TABLES").df()["name"].to_list()
attempt_query = st.text_area(label="Type your query here")
if attempt_query:
    result = con.execute(attempt_query).df()
    st.dataframe(result)

#     try:
#         result = result.select(solution_df.columns)
#         assert result.equals(solution_df)

#     except pl.exceptions.ColumnNotFoundError:
#         st.write("Some columns are missing")
#     except AssertionError:
#         st.markdown(
#             "<span style='color:red; font-weight:bold'>"
#             "Error: some values are not the same!</span>",
#             unsafe_allow_html=True,
#         )
#         st.dataframe(result)
#         st.write("Expected")
#         st.dataframe(solution_df)

#     if delta := abs(result.shape[0] - solution_df.shape[0]) != 0:
#         st.write(f"{delta} lines are missing.")

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
        answer_filename = exercise.loc[0]["exercise_name"].strip()
        st.write(answer_filename)
        with open(f"/home/nociception/dus/sql_srs/answers/{answer_filename}.sql", "r") as f:
            answer_query = f.read()
        st.write(f"Solution Query: {answer_query}")

con.close()