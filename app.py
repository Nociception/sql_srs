import duckdb
import streamlit as st
import polars as pl


def main():
    st.write("#SQL SRS")

    st.write("Spaced Repetition System SQL Practice")

    beverages = pl.read_csv("beverages.csv")
    food_items = pl.read_csv("food_items.csv")
    QUERY_ANSWER = """
    SELECT * FROM beverages
    CROSS JOIN food_items
    """
    solution_df = pl.DataFrame(duckdb.sql(QUERY_ANSWER))


    with st.sidebar:
        option = st.selectbox(
            "What would you like to review?",
            ("Joins", "Group by", "Windows functions"),
            index=None,
            placeholder="Select a theme",
        )

        st.write("You selected:", option)


    query = st.text_area(label="Type your query here")
    if query:
        result = pl.DataFrame(duckdb.query(query))
        st.dataframe(result)

        try :
            result = result.select(solution_df.columns)
            assert result.equals(solution_df)
            
        except pl.exceptions.ColumnNotFoundError:
            st.write("Some columns are missing")
        except AssertionError:
            st.markdown(
                "<span style='color:red; font-weight:bold'>Error: some values are not the same!</span>",
                unsafe_allow_html=True
            )
            st.dataframe(result)
            st.write("Expected")
            st.dataframe(solution_df)

        if delta := abs(result.shape[0] - solution_df.shape[0]) != 0:
            st.write(f"{delta} lines are missing.")


    tab1, tab2 = st.tabs(["Table", "Solution",])
    with tab1:
        st.write("beverages")
        st.dataframe(beverages)

        st.write("food_items")
        st.dataframe(food_items)

        st.write("Expected result:")
        st.dataframe(solution_df)
    with tab2:
        st.write(QUERY_ANSWER)



if __name__ == "__main__":
    main()
