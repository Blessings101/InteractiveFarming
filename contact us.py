import streamlit as st

def create_contact_form():
    st.title("Contact Us")

    with st.form(key='contact_form'):
        st.markdown("<h2 style='text-align: center; color: blue;'>Contact Form</h2>", unsafe_allow_html=True)
        st.markdown("Please fill out the form below and we will get back to you as soon as possible.", unsafe_allow_html=True)

        name = st.text_input("Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone")
        address = st.text_input("Address")

        submit_button = st.form_submit_button(label='Submit')

        if submit_button:
            st.success("Thank you for your message. We will get back to you soon.")

create_contact_form()