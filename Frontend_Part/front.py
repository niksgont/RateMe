import streamlit as st
from pathlib import Path
from streamlit_option_menu import option_menu
from src.styles.menu_styles import FOOTER_STYLES, HEADER_STYLES

# Set page config
st.set_page_config(page_title="Review Platform", page_icon=":handshake:", layout='wide')

current_dir: Path = Path(__file__).parent if "__file__" in locals() else Path.cwd()
css_file: Path = current_dir / "src/styles/.css"


with open(css_file) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def main():

    selected_footer = option_menu(
        menu_title=None,
        options=[
            "Home",
            "Reviews",
            "Help",
            "Authors"
        ],
        icons=["", "chat-square-text", "info-circle", ""],  # https://icons.getbootstrap.com/
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
        styles=HEADER_STYLES
    )





    # st.title("Review Platform")

    # # Create a header for the page with pages
    # st.header("Navigation")

    # menu = ["Home", "Search", "Write a review", "User Profile"]
    # choice = st.sidebar.selectbox("Menu", menu)

    # if choice == "Home":
    #     st.subheader("Home")
    #     # Here you can show the trending items, the best rated items etc.

    # elif choice == "Search":
    #     st.subheader("Search for Reviews")
    #     search_term = st.text_input("Enter your search term")
    #     # Here you should implement the logic for searching for reviews in your database based on the search_term
    #     # The result should be displayed in a user-friendly format, probably in a table or a list.

    # elif choice == "Write a review":
    #     st.subheader("Write a review")
    #     item_name = st.text_input("Item Name")
    #     review_text = st.text_area("Your review")
    #     rating = st.slider("Rate the item", 0.0, 5.0)
    #     if st.button("Submit"):
    #         # Here you should implement the logic for adding a review to your database
    #         st.success("Your review has been submitted!")

    # elif choice == "User Profile":
    #     st.subheader("User Profile")
    #     # Here you should implement the logic for displaying and editing user profile.
    #     # User should be able to see his/her past reviews, edit them, delete them etc.

if __name__ == "__main__":
    main()