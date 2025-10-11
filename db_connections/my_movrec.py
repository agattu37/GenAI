import streamlit as st
import pandas as pd
from my_movgroq_resp import get_movgroq_response

# A visual form to query details of movies from the database
def main():

    st.title("My Movie Recommendation Engine")
    st.subheader("Search for movies title")

    query = st.text_input("Enter your movie title")

    if query:
        filtered_products = get_movgroq_response(query)
        if filtered_products:
            df = pd.DataFrame(
                {
                    "Movie Id" : [movies["_id"] for movies in filtered_products],
                    "Title" : [movies["title"] for movies in filtered_products],
                    "Plot" : [movies["plot"] for movies in filtered_products],
                    "Year" : [movies["year"] for movies in filtered_products]
                }
            )
            st.table(df)
        else:
            st.write("No products found")


main()
