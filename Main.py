import folium
import streamlit as st
import account
from streamlit_extras.add_vertical_space import add_vertical_space

from helpers import display_crop_recommendation, fetch_disease_info, fetch_prevention_recommendations, get_coordinates, get_crop_recommendations, get_nearest_agrocrop, load_and_preprocess_image, predict_disease_or_pest_or_healthy, predict_plant_class

def main():
    if("username" not in st.session_state or "email" not in st.session_state ):
        account.main()
    else:
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
                  # prevention_recommendations = fetch_prevention_recommendations(disease_or_pest_or_healthy)
                  crop_recommendation = get_crop_recommendations(disease_or_pest_or_healthy)
                  st.write("Recommendations to prevent: ", disease_or_pest_or_healthy)
                  # for recommendation in prevention_recommendations:
                  #     st.write(recommendation)
                  display_crop_recommendation(disease_info=crop_recommendation)

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


if __name__ == "__main__":
    main()

