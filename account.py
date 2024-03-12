import streamlit as st

def signup_form():
    st.title("Sign Up Form")
    username = st.text_input("User Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirmPassword = st.text_input("Confirm Password", type="password")

    if st.button("Sign Up"):
        if password == confirmPassword:
            st.success("You have successfully signed up")
        else:
            st.error("Passwords do not match")

    if st.checkbox("Already a member?"):
        if st.button("Login"):
            login_form()

def login_form():
    st.title("Login Form")
    username = st.text_input("User Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        st.success("You have successfully logged in")

    if not st.checkbox("Are you a member?"):
        if st.button("Sign Up"):
            signup_form()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    