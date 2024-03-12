import streamlit as st

# Define the URL you want to redirect to (in this case, Google)
redirect_url = "https://www.google.com"

# Create a button that triggers the redirection
if st.button("Go to Google"):
    st.markdown(f'<meta http-equiv="refresh" content="0;url={redirect_url}" target="_blank">', unsafe_allow_html=True)
