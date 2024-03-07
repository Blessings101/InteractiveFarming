import streamlit as st
import tensorflow as tf
from PIL import Image
import requests
from bs4 import BeautifulSoup
import googlemaps
from geopy.geocoders import Nominatim
import folium
import pydeck as pdk
import os
import json
import io
from geopy.exc import GeocoderUnavailable
import numpy as np
from streamlit_modal import Modal

# Assuming dotenv is used for environment variable management
from dotenv import load_dotenv
from streamlit_extras.add_vertical_space import add_vertical_space

# Sidebar contents
with st.sidebar:
    st.title('Common questions asked during pregnancy')

    # Path to your image file
    image_path = "farm.webp"

    # Display the image
    st.image(image_path, caption='Helping teen mothers figure out their way through pregnancy', use_column_width=True)
    st.markdown('''
    ## About
    EmpowerBot is an interactive chatbot application specifically designed to offer support and guidance to teen mothers throughout their pregnancy journey. This Streamlit-powered chatbot leverages cutting-edge technologies to provide comprehensive answers to a wide array of questions related to pregnancy.

    Built by ['Terah Jones Alukwe', 'Wawuda Natasha', 'Sila Silverster', 'Silas']
    ''')

    add_vertical_space(3)

load_dotenv()

modal = Modal(key="Demo Key",title="Feedback")

# Load API keys from environment
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')

# Initialize API clients
gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY) if GOOGLE_MAPS_API_KEY else None

# Check for API key loading
if not GOOGLE_MAPS_API_KEY:
    st.error("Google Maps API key is missing. Please check your .env file.")
    st.stop()

# Placeholder for model prediction function for plant class
@st.cache(allow_output_mutation=True, suppress_st_warning=True)
def predict_plant_class(image_bytes):
    """Placeholder for model prediction function for plant class."""
    try:
        # Load the model for predicting plant class
        model_path = 'model.h5'
        if os.path.exists(model_path):
            model = tf.keras.models.load_model(model_path)
        else:
            st.error("Failed to load the plant class model. Please check the model path.")
            return None

        # Preprocess the image bytes for plant class prediction
        image = tf.image.decode_jpeg(image_bytes.getvalue(), channels=3)
        image = tf.image.resize(image, [128, 128])  # Resize the image to (128, 128)
        image = tf.expand_dims(image, axis=0)  # Add batch dimension
        image = tf.cast(image, tf.float32)  # Convert image to float32

        # Make predictions for plant class
        predictions = model.predict(image)

        # Placeholder logic to determine plant class
        class_names = ['Cashew', 'Cassava', 'Maize', 'Tomato']
        predicted_class = class_names[np.argmax(predictions)]

        return predicted_class

    except Exception as e:
        st.error(f"An error occurred during plant class prediction: {e}")
        return None


# Placeholder for model prediction function for disease, pest, or healthy status
@st.cache(allow_output_mutation=True, suppress_st_warning=True)
def predict_disease_or_pest_or_healthy(image_bytes, plant_class):
    """Placeholder for model prediction function for disease, pest, or healthy status."""
    try:
        # Load the model for predicting disease, pest, or healthy status
        model_path = 'model.h5'
        if os.path.exists(model_path):
            model = tf.keras.models.load_model(model_path)
        else:
            st.error("Failed to load the disease, pest, or healthy model. Please check the model path.")
            return None

        # Preprocess the image bytes for disease, pest, or healthy status prediction
        image = tf.image.decode_jpeg(image_bytes.getvalue(), channels=3)
        image = tf.image.resize(image, [128, 128])  # Resize the image
        image = tf.expand_dims(image, axis=0)  # Add batch dimension
        image = tf.cast(image, tf.float32)  # Convert image to float32

        # Placeholder logic to determine disease, pest, or healthy status
        predictions = model.predict(image)  # Make predictions based on the preprocessed input

        class_names = [
            'anthracnose_cashew', 'healthy_cashew', 'leaf_miner_cashew','gumosis_cashew', 'red_rust_cashew', # Cashew
            'bacterial_blight_cassava', 'brown_spot_cassava', 'green_mite_cassava', 'healthy_cassava', 'mosaic_cassava', # Cassava
            'fall_armyworm_maize', 'grasshopper_maize', 'healthy_maize', 'leaf_beetle_maize', 'leaf_blight_maize', 'leaf_spot_maize', 'streak_virus_maize',  # Maize
            'healthy_tomato', 'leaf_blight_tomato', 'leaf_curl_tomato', 'septoria_leaf_spot_tomato', 'verticulium_wilt_tomato'  # Tomato
        ]
        predicted_class = class_names[np.argmax(predictions)]  # Decode the predicted output

        return predicted_class

    except Exception as e:
        st.error(f"An error occurred during disease, pest, or healthy status prediction: {e}")
        return None

# Define or import the google_search function
def google_search(query):
    try:
        url = f"https://www.google.com/search?q={query}"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.text
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to perform Google search: {e}")
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return None

# Define or import the extract_information function
def extract_information(html_content):
    if html_content is not None:
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            # Initialize variables to store extracted information
            description = ""
            affected_crops = []
            prevention_methods = []
            treatment_options = []

            # Example: Extract description
            description_element = soup.find("div", class_="s3v9rd")
            if description_element:
                description = description_element.text.strip()

            # Example: Extract affected crops
            crops_elements = soup.find_all("div", class_="s3v9rd")
            for crops_element in crops_elements:
                affected_crops.append(crops_element.text.strip())

            # Example: Extract prevention methods
            prevention_elements = soup.find_all("div", class_="s3v9rd")
            for prevention_element in prevention_elements:
                prevention_methods.append(prevention_element.text.strip())

            # Example: Extract treatment options
            treatment_elements = soup.find_all("div", class_="s3v9rd")
            for treatment_element in treatment_elements:
                treatment_options.append(treatment_element.text.strip())

            # Return the extracted information
            return {
                "description": description,
                "affected_crops": affected_crops,
                "prevention_methods": prevention_methods,
                "treatment_options": treatment_options
            }
        except Exception as e:
            st.error(f"An error occurred while extracting information: {e}")
            return None
    else:
        return None


# Define the function to generate a search query based on the detected disease or pest
def generate_search_query(disease_or_pest):
    return f"{disease_or_pest} description prevention methods treatment options"

# Define the function to perform a Google search and extract relevant information
def fetch_information(query):
    try:
        # Perform a Google search and retrieve search results
        search_results = google_search(query)
        if search_results:
            # Extract relevant information from the search results
            information = extract_information(search_results)
            return information
        else:
            return None
    except Exception as e:
        st.error(f"An error occurred while fetching information: {e}")
        return None

def fetch_disease_info(disease_or_pest):
    query = generate_search_query(disease_or_pest)
    information = fetch_information(query)
    return information

def fetch_prevention_recommendations(disease_or_pest):
    # This function could fetch recommendations for preventing a specific disease or pest
    # You can customize it based on your requirements, such as querying a database or API
    # For demonstration purposes, let's return some sample recommendations
    return [
        "Keep the planting area clean and free from debris.",
        "Practice crop rotation to reduce pest populations.",
        "Apply appropriate pesticides or fungicides as preventive measures."
    ]

def fetch_maintenance_recommendations(plant_class):
    # This function could fetch recommendations for maintaining the health of a plant
    # You can customize it based on your requirements, such as querying a database or API
    # For demonstration purposes, let's return some sample recommendations
    return [
        f"Regularly water the {plant_class} plants to keep the soil moist.",
        f"Fertilize the {plant_class} plants with appropriate nutrients as needed.",
        f"Inspect the {plant_class} plants regularly for signs of pests or diseases."
    ]

# Assuming a function to load and preprocess image
def load_and_preprocess_image(image_path):
    """Load and preprocess the image for prediction."""
    image = Image.open(image_path)
    # Convert the image to bytes
    image_bytes = io.BytesIO()
    image.save(image_bytes, format='JPEG')  # Convert to JPEG format
    return image_bytes

# Assuming a function to fetch recommendations (simplified for demonstration)
def fetch_information(query):
    try:
        # Perform a Google search and retrieve search results
        search_results = google_search(query)
        if search_results:
            # Extract relevant information from the search results
            information = extract_information(search_results)
            return information
        else:
            return None
    except Exception as e:
        st.error(f"An error occurred while fetching information: {e}")
        return None

# Main app interface
def main():
    st.title('Welcome to the Recommendation App')

    uploaded_file = st.file_uploader("Choose an image...", type="jpg")
    if uploaded_file is not None:
        # Load and preprocess the image
        image_bytes = load_and_preprocess_image(uploaded_file)

        # Display the uploaded image
        st.image(image_bytes, caption='Uploaded Image.', use_column_width=True)

        # Predict the plant class
        plant_class = predict_plant_class(image_bytes)

        if plant_class:
            # Predict the disease, pest, or healthy status based on the predicted plant class
            disease_or_pest_or_healthy = predict_disease_or_pest_or_healthy(image_bytes, plant_class)

            # Display predicted plant class and disease, pest, or healthy status
            st.write("Predicted Plant Class:", plant_class)
            if disease_or_pest_or_healthy:
                st.write("Disease or Pest or healthy:", disease_or_pest_or_healthy)
            else:
                st.error("Failed to predict the disease, pest or healthy class.")
        else:
            st.error("Failed to predict the plant class.")

        # Assuming fetching recommendations based on predictions
        if disease_or_pest_or_healthy:
            # Fetch information about the disease or pest
            disease_info = fetch_disease_info(disease_or_pest_or_healthy)
            st.write("Information about: ", disease_or_pest_or_healthy)
            st.write(disease_info)

            # Recommendations on how to prevent the disease
            prevention_recommendations = fetch_prevention_recommendations(disease_or_pest_or_healthy)
            st.write("Recommendations to prevent: ", disease_or_pest_or_healthy)
            for recommendation in prevention_recommendations:
                st.write(recommendation)

        # Get user input for their location only once
        location_name = st.text_input("Enter your location name (e.g., Nakuru):", key="location_input")
        if location_name:
            # Get the coordinates for the specified location
            user_coordinates = get_coordinates(location_name)

            if user_coordinates:
                st.write(f"Coordinates for {location_name}:", user_coordinates)

                # Get the nearest agrocrop center
                nearest_agrocrop = get_nearest_agrocrop(user_coordinates)

                if nearest_agrocrop:
                    st.write("Nearest Agrocrop Center:", nearest_agrocrop)

                    # Create a Folium map
                    agrocrop_map = folium.Map(location=[user_coordinates[0], user_coordinates[1]], zoom_start=15)

                    # Add a marker for the user's location
                    folium.Marker(location=[user_coordinates[0], user_coordinates[1]],
                                  popup="Your Location").add_to(agrocrop_map)

                    # Add a marker for the nearest agrocrop center
                    folium.Marker(location=[nearest_agrocrop['lat'], nearest_agrocrop['lng']],
                                  popup="Nearest Agrocrop Center").add_to(agrocrop_map)

                    # Add tile layer for better visualization
                    folium.TileLayer('openstreetmap').add_to(agrocrop_map)

                    # Draw a line between user's location and nearest agrocrop center
                    folium.PolyLine(
                        locations=[[user_coordinates[0], user_coordinates[1]], [nearest_agrocrop['lat'], nearest_agrocrop['lng']]],
                                    color='red').add_to(agrocrop_map)
                    # Display the map
                    st.write(agrocrop_map)

                else:
                    st.warning(f"No nearby agrocrop centers found for {location_name}")
                    # Display a map centered around the specified location
                    st.map({'lat': [user_coordinates[0]], 'lon': [user_coordinates[1]]}, zoom=15)

            else:
                st.error("Error getting coordinates. Please check the location name.")
        else:
            st.info("Please enter a location name to find the nearest agrocrop center.")
            # Placeholder for user feedback loop
            feedback = st.text_area("Feedback on recommendations:")
            if st.button("Submit Feedback"):
                st.write("Thank you for your feedback!")


# Function to get coordinates from location name
@st.cache_data
def get_coordinates(location_name):
    geolocator = Nominatim(user_agent="agrocrop_locator")
    try:
        location = geolocator.geocode(location_name)
        if location:
            return location.latitude, location.longitude
        else:
            return None
    except GeocoderUnavailable:
        st.error("Geocoding service is currently unavailable. Please try again later.")
        return None
    except Exception as e:
        st.error(f"Error occurred while fetching coordinates: {str(e)}")
        return None


# Function to get the nearest agrocrop center
def get_nearest_agrocrop(user_coordinates):
    try:
        if not gmaps:
            st.error("Google Maps client is not initialized.")
            return None

        # Search for agrocrop centers near the user's location
        places = gmaps.places_nearby(location=user_coordinates, radius=20000, type='agrocrop')
        if 'results' in places and places['results']:
            nearest_agrocrop = places['results'][0]['geometry']['location']
            return nearest_agrocrop
        else:
            return None
    except googlemaps.exceptions.ApiError as e:
        st.error("Google Maps API error: REQUEST_DENIED. You must enable Billing on the Google Cloud Project to use the Google Maps Places API. Learn more at https://developers.google.com/maps/gmp-get-started")
        return None

if __name__ == "__main__":
    main()

