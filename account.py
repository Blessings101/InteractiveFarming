import streamlit as st
import Main 
import db

def signup_form():
    with st.form(key='signup_form'):
        st.title("Sign Up Form")
        username = st.text_input("User Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirmPassword = st.text_input("Confirm Password", type="password")

        submit_button = st.form_submit_button(label='Sign Up')

        if submit_button:
            if password == confirmPassword:
                try:
                    db.new_user(username, email, password)
                    st.success("You have successfully created a valid account")
          
                    
                except:
                    st.error("An error occurred while creating your account. Please try again.")
            else:
                st.error("Passwords do not match")
            
def login_form():
    with st.form(key='login_form'):
        st.title("Login Form")
        username = st.text_input("User Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        submit_button = st.form_submit_button(label='Login')

        if submit_button:
            try:
                user = db.get_user(username, password)
                if user is not None:
                    st.success("You have successfully logged in")
                else:
                    st.error("Invalid username or password")
                     
            except:
                st.error("An error occurred while trying to log in. Please try again.")
                
                
    
    
def main():
    if ["account_page"] not in st.session_state:
        st.session_state["account_page"] = "login"
        
    st.title("Account Page")

    col1, col2 = st.columns(2)

    signup_button = col1.button('Signup', key="signup")
    login_button = col2.button('Login', key="login")

    if signup_button or st.session_state["account_page"] == "signup":
        st.write(signup_form())
    if login_button or st.session_state["account_page"] == "login":
        st.write(login_form())
    
    
if __name__ == "__main__":
    main()
    
    
    
    
    
    
    
    
    