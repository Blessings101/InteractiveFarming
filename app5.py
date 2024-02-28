import streamlit as st
import tensorflow as tf
from PIL import Image
import requests
from bs4 import BeautifulSoup

# Load the trained model
model = tf.keras.models.load_model('keras_model1.h5')

# Function to preprocess uploaded image
def preprocess_image(image):
    img = Image.open(image)
    img = img.resize((224, 224))  # Resize image to match model input size
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)  # Add batch dimension
    return img_array

# Function to preprocess uploaded image
# def preprocess_image(image):
#     img = Image.open(image)
#     img = img.resize((128, 128))  # Resize image to match model input size
#     img_array = tf.keras.preprocessing.image.img_to_array(img)
#     img_array = tf.expand_dims(img_array, 0)  # Add batch dimension
#     return img_array

# Function to make predictions
def predict_disease(image):
    preprocessed_img = preprocess_image(image)
    predictions = model.predict(preprocessed_img)
    class_names = ['Cashew', 'Cassava', 'Maize', 'Tomato']
    plant_class = class_names[predictions.argmax()]
    disease_or_pest = None

    # Determine the disease or pest based on the plant class
    if plant_class == 'Cashew':
        disease_or_pest_classes = ['anthracnose', 'gumosis', 'leaf miner', 'red rust']
    elif plant_class == 'Cassava':
        disease_or_pest_classes = ['bacterial blight', 'brown spot', 'green mite', 'mosaic']
    elif plant_class == 'Maize':
        disease_or_pest_classes = ['fall armyworm', 'grasshopper', 'leaf beetle', 'leaf blight', 'leaf spot']
    elif plant_class == 'Tomato':
        disease_or_pest_classes = ['leaf blight', 'leaf curl', 'septoria leaf spot', 'verticulium wilt']

    disease_or_pest_probabilities = predictions[0, 1:]  # Exclude the plant class probability
    disease_or_pest_index = disease_or_pest_probabilities.argmax()
    disease_or_pest = disease_or_pest_classes[disease_or_pest_index]

    return plant_class, disease_or_pest

def google_search(query):
    url = f"https://www.google.com/search?q={query}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        return None

def extract_information(html_content):
    if html_content is not None:
        soup = BeautifulSoup(html_content, 'html.parser')

        # Initialize variables to store extracted information
        description = ""
        affected_crops = []
        prevention_methods = []
        treatment_options = []

        # Extract relevant information from the search results
        # You'll need to inspect the HTML structure of the search results
        # and identify the elements containing the desired information

        # Example: Extract description
        description_element = soup.find("div", class_="BNeawe s3v9rd AP7Wnd")
        if description_element:
            description = description_element.text.strip()

        # Example: Extract affected crops
        crops_elements = soup.find_all("div", class_="crops")
        for crops_element in crops_elements:
            affected_crops.append(crops_element.text.strip())

        # Example: Extract prevention methods
        prevention_elements = soup.find_all("div", class_="prevention")
        for prevention_element in prevention_elements:
            prevention_methods.append(prevention_element.text.strip())

        # Example: Extract treatment options
        treatment_elements = soup.find_all("div", class_="treatment")
        for treatment_element in treatment_elements:
            treatment_options.append(treatment_element.text.strip())

        # Return the extracted information
        return {
            "description": description,
            "affected_crops": affected_crops,
            "prevention_methods": prevention_methods,
            "treatment_options": treatment_options
        }
    else:
        return None

def generate_search_query(disease_or_pest):
    # Generate a search query based on the detected disease or pest
    return f"{disease_or_pest} description prevention methods treatment options"

def fetch_information(query):
    # Perform a Google search and retrieve search results
    search_results = google_search(query)
    # Extract relevant information from the search results
    information = extract_information(search_results)
    return information   

def fetch_recommendations(disease_or_pest):
    query = f"{disease_or_pest} disease or pest description, affected crops, prevention methods, treatment options"
    search_results = google_search(query)
    recommendations = extract_information(search_results)
    return recommendations


# Function to fetch recommendations from multiple websites
def fetch_recommendations(disease_or_pest):
    query = f"{disease_or_pest} disease or pest description, affected crops, prevention methods, treatment options"
    search_results = google_search(query)
    recommendations = extract_information(search_results)
    return recommendations

# Streamlit app
def main():
    st.title('Crop Disease and Pest Detection')
    st.write('Upload an image of a plant to classify the disease or pest.')

    uploaded_file = st.file_uploader("Choose an image...", type=['jpg', 'jpeg', 'png'])

    if uploaded_file is not None:
        st.image(uploaded_file, caption='Uploaded Image', use_column_width=True)
        st.write("")
        st.write("Classifying...")

        plant_class, disease_or_pest = predict_disease(uploaded_file)
        st.write(f"Predicted Plant Class: {plant_class}")
        st.write(f"Predicted Disease or Pest: {disease_or_pest}")

        # Fetch recommendations based on the detected disease
        if disease_or_pest is not None:
            st.write("Fetching recommendations...")

            recommendations = fetch_recommendations(disease_or_pest)
            if recommendations:
                st.write("Recommendations:")
                st.write(f"- Description: {recommendations.get('description', 'N/A')}")
                st.write(f"- Affected Crops: {', '.join(recommendations.get('affected_crops', ['N/A']))}")
                st.write(f"- Prevention Methods: {', '.join(recommendations.get('prevention_methods', ['N/A']))}")
                st.write(f"- Treatment Options: {', '.join(recommendations.get('treatment_options', ['N/A']))}")
                st.write(google_search(disease_or_pest))
            else:
                st.write("No recommendations found.")
        if disease_or_pest is not None:
            search_query = generate_search_query(disease_or_pest)
            information = fetch_information(search_query)
            if information:
                # Display the extracted information to the user
                st.write("Information about the detected disease or pest:")
                st.write("Description:", information.get("description"))
                st.write("Affected Crops:", information.get("affected_crops"))
                st.write("Prevention Methods:", information.get("prevention_methods"))
                st.write("Treatment Options:", information.get("treatment_options"))
            else:
                st.write("No information found for the detected disease or pest.")

if __name__ == '__main__':
    main()

