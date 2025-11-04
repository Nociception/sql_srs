import polars as pl
import streamlit as st



def main():
    BEVERAGES = pl.read_csv("beverages.csv")
    BEVERAGES_COPY = pl.read_csv("beverages_copy.csv")

    st.write(BEVERAGES.equals(BEVERAGES_COPY))


    result = result[solutions.columns]


if __name__ == "__main__":
    main()