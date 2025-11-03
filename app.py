import duckdb
import streamlit as st
import polars as pl


def main():
    st.write("#SQL SRS")

    st.write("Spaced Repetition System SQL Practice")


    option = st.selectbox(
        "What would you like to review?",
        ("Joins", "Group by", "Windows functions"),
        index=None,
        placeholder="Select a theme",
    )

    st.write("You selected:", option)



    tab1, tab2, tab3 = st.tabs(["Cat", "Dog", "Owl"])

    data = {
        "a": [1, 2, 3],
        "b": [4, 5, 6],
    }
    df = pl.DataFrame(data)

    with tab1:
        pass
        query = st.text_area(label="type your query here")
        st.write(f"You typed: {query}")
        result = duckdb.query(query).df()
        st.dataframe(result)

    with tab2:
        st.header("Dog")
        st.image(
            "https://static.streamlit.io/examples/dog.jpg",
            caption="A friendly dog",
            width=300
        )
        
    with tab3:
        st.header("Owl")
        st.image(
            "https://static.streamlit.io/examples/owl.jpg",
            caption="A wise owl",
            width=300
        )

if __name__ == "__main__":
    main()
