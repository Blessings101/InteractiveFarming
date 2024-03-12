import streamlit as st
import main
st.header("AgroScan")

if "page" not in st.session_state:
    st.session_state["page"] = "home"

with st.sidebar:
    if st.button("HOME"):
        st.session_state["page"] = "home"
    if st.button("ACCOUNT"):
        st.session_state["page"] = "account"
    if st.button("ABOUT US"):
        st.session_state["page"] = "about"
    if st.button("CONTACT US"):
        st.session_state["page"] = "contact"
    st.title('Common questions asked during pregnancy')

    # Path to your image file
    image_path = "images/farm.webp"

    # Display the image
    st.image(image_path, caption='Helping teen mothers figure out their way through pregnancy', use_column_width=True)
    st.markdown('''
    ## About
    EmpowerBot is an interactive chatbot application specifically designed to offer support and guidance to teen mothers throughout their pregnancy journey. This Streamlit-powered chatbot leverages cutting-edge technologies to provide comprehensive answers to a wide array of questions related to pregnancy.

    Built by ['Terah Jones Alukwe', 'Wawuda Natasha', 'Sila Silverster', 'Silas']
    ''')
if(st.session_state["page"] == "home"):
    main.main()
if(st.session_state["page"] == "account"):
    st.write("Welcome to the Account page")
if(st.session_state["page"] == "about"):
    st.write("Welcome to the about page")
if(st.session_state["page"] == "contact"):
    st.write("Welcome to the contact page")
    