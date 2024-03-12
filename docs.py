import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def create_docs():
    st.title("Crop Pest Detection System Documentation")

    st.markdown("<h2 style='text-align: center; color: green;'>System Description</h2>", unsafe_allow_html=True)
    st.image("https://plus.unsplash.com/premium_photo-1678344170545-c3edef92a16e?w=900&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8YWdyaWN1bHR1cmV8ZW58MHx8MHx8fDA%3D", use_column_width=True)
   
    st.markdown("""
    Our system is a **crop pest detection system** that uses advanced artificial intelligence (AI) algorithms to recognize pests infesting crops. 
    The AI model has been trained on thousands of images of crops, allowing it to accurately identify a wide range of pests.
    """, unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: purple;'>Prevention</h2>", unsafe_allow_html=True)
    st.image("https://images.unsplash.com/photo-1560493676-04071c5f467b?w=900&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8YWdyaWN1bHR1cmV8ZW58MHx8MHx8fDA%3D", use_column_width=True)

    st.markdown("""
    In addition to pest detection, the system provides comprehensive documentation on how to prevent and treat the diseases caused by these pests. 
    This information is based on extensive research and best practices in the field of agriculture.
    """, unsafe_allow_html=True)

    st.markdown("""
    If a crop is healthy, the system doesn't just stop there. It provides proactive recommendations on measures to take to prevent future pest infestations. 
    These recommendations are tailored to the specific type of crop and its associated pests.
    """, unsafe_allow_html=True)

    st.markdown("<h2 style='text-align: center; color: orange;'>Healthy Crops</h2>", unsafe_allow_html=True)
    st.image("https://images.unsplash.com/photo-1560493676-04071c5f467b?w=900&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8YWdyaWN1bHR1cmV8ZW58MHx8MHx8fDA%3D", use_column_width=True)

    st.markdown("<h2 style='text-align: center; color: blue;'>How to Use</h2>", unsafe_allow_html=True)
    st.markdown("""
    Using the system is straightforward:
    1. The user is prompted to upload an image of the crop. This can be done via a simple and intuitive interface.
    2. Once the image is uploaded, it is sent to our server. The server uses the AI model to classify the image and determine if there are any pests present.
    3. The output from the server is then returned and presented to the user. This includes the identification of any pests and relevant documentation on prevention and treatment.
    """, unsafe_allow_html=True)

    st.markdown("<h2 style='text-align: center; color: purple;'>Prevention</h2>", unsafe_allow_html=True)
    st.markdown("""
    Prevention is a key aspect of managing crop health. The system provides detailed recommendations on how to prevent pest infestations. 
    These recommendations are based on the type of crop, the current season, and the potential pests that could infest the crop.
    """, unsafe_allow_html=True)

    st.markdown("<h2 style='text-align: center; color: red;'>Treatment</h2>", unsafe_allow_html=True)
    st.markdown("""
    If a pest infestation is detected, the system doesn't leave you hanging. It provides a range of treatment options that you can use to address the problem. 
    These options are based on the type of pest, the severity of the infestation, and the specific type of crop. 
    The treatment options are designed to be effective while minimizing harm to the crop and the environment.
    """, unsafe_allow_html=True)

    st.markdown("<h2 style='text-align: center; color: orange;'>Healthy Crops</h2>", unsafe_allow_html=True)
    st.markdown("""
    For healthy crops, the system provides recommendations on how to keep them that way. 
    This includes tips on crop rotation, the use of natural predators, and other organic farming practices. 
    By following these recommendations, you can maintain the health of your crops and prevent future pest infestations.
    """, unsafe_allow_html=True)

    st.markdown("<h2 style='text-align: center; color: brown;'>Sample Chart</h2>", unsafe_allow_html=True)
    chart_data = pd.DataFrame(
        np.random.randn(20, 3),
        columns=['Healthy Crops', 'Pests Detected', 'Treated Crops'])
    st.line_chart(chart_data)

create_docs()