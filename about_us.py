import streamlit as st

def create_about_us_page():
    st.title("About Us")

    st.markdown("<h2 style='text-align: center; color: blue;'>Our System</h2>", unsafe_allow_html=True)
    st.markdown("""
    Our system is a **crop pest detection system** that uses advanced artificial intelligence (AI) algorithms to recognize pests infesting crops. 
    The AI model has been trained on thousands of images of crops, allowing it to accurately identify a wide range of pests.
    """, unsafe_allow_html=True)

    st.markdown("<h2 style='text-align: center; color: green;'>Our Website</h2>", unsafe_allow_html=True)
    st.markdown("""
    Our website is designed to be user-friendly and intuitive. It provides comprehensive information about our system, 
    including detailed documentation and a contact form for any inquiries. We are committed to providing excellent service 
    and support to our users.
    """, unsafe_allow_html=True)

    st.markdown("<h2 style='text-align: center; color: purple;'>Our Team</h2>", unsafe_allow_html=True)
    st.markdown("""
    Our team is composed of dedicated professionals with expertise in artificial intelligence, agriculture, and web development. 
    We are passionate about using technology to solve real-world problems and are constantly working to improve our system.
    """, unsafe_allow_html=True)

create_about_us_page()