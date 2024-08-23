import streamlit as st
from datetime import datetime
import requests
import folium
from streamlit_folium import st_folium

# Add custom CSS to set the background color
st.markdown("""
    <style>
    .stApp {
        background-color: #ADD8E6; /* Light Blue Background */
    }
    </style>
""", unsafe_allow_html=True)

'''
# TaxiFareModel Prediction
'''

st.markdown('''
Welcome to the Taxi Fare Predictor! Estimate the fare of your ride based on various parameters.
''')

'''
## Please provide the details of your ride:

1. Date and Time
2. Pickup Longitude
3. Pickup Latitude
4. Dropoff Longitude
5. Dropoff Latitude
6. Passenger Count
'''

# User inputs for the ride parameters
pickup_datetime = st.text_input("Pickup Date and Time", value=str(datetime.now()))
pickup_longitude = st.number_input("Pickup Longitude", value=-73.985428)
pickup_latitude = st.number_input("Pickup Latitude", value=40.748817)
dropoff_longitude = st.number_input("Dropoff Longitude", value=-73.985428)
dropoff_latitude = st.number_input("Dropoff Latitude", value=40.748817)
passenger_count = st.number_input("Passenger Count", min_value=1, max_value=10, value=1)

url = 'https://taxifare.lewagon.ai/predict'

# Initialize session state for prediction
if 'prediction_value' not in st.session_state:
    st.session_state.prediction_value = None

# Button to trigger the prediction
if st.button('Predict Fare'):
    params = {
        'pickup_datetime': pickup_datetime,
        'pickup_longitude': pickup_longitude,
        'pickup_latitude': pickup_latitude,
        'dropoff_longitude': dropoff_longitude,
        'dropoff_latitude': dropoff_latitude,
        'passenger_count': passenger_count
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Check for HTTP errors

        # Get the JSON response and debug output
        json_response = response.json()
        st.write("Full API Response:", json_response)  # Debug output

        # Extract and debug the prediction
        if 'fare' in json_response:
            prediction = json_response['fare']
            st.write(f"Raw prediction value: {prediction}")  # Debug output

            # Attempt to convert to float and store in session state
            try:
                st.session_state.prediction_value = float(prediction)
            except ValueError:
                st.session_state.prediction_value = None
                st.error("Prediction value is not a valid number")
        else:
            st.error("Prediction key 'fare' not found in the response")

    except requests.RequestException as e:
        st.error(f"An error occurred: {e}")

# Display the stored prediction value if available
if st.session_state.prediction_value is not None:
    st.success(f"Predicted Fare: ${st.session_state.prediction_value:.2f}")

# Adding a map to display pickup and dropoff locations
st.markdown("### Map of Pickup and Dropoff Locations")
map_center = [(pickup_latitude + dropoff_latitude) / 2, (pickup_longitude + dropoff_longitude) / 2]
m = folium.Map(location=map_center, zoom_start=12)

# Add markers for pickup and dropoff
folium.Marker([pickup_latitude, pickup_longitude], tooltip="Pickup Location", icon=folium.Icon(color='blue')).add_to(m)
folium.Marker([dropoff_latitude, dropoff_longitude], tooltip="Dropoff Location", icon=folium.Icon(color='red')).add_to(m)

# Display the map in Streamlit
st_folium(m, width=700)
