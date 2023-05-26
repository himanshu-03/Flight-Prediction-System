import streamlit as st
import requests
from datetime import datetime
from streamlit.components.v1 import html

# Streamlit app code
def main():
    st.image("./static/img/background-2.jpg", use_column_width=True)
    st.title("Flight Price Prediction")

    # Input form
    with st.form("flight_form"):
        dep_date = st.date_input("Departure Date", value=datetime.now().date())
        dep_time = st.time_input("Departure Time", value=datetime.now().time())
        arrival_date = st.date_input("Arrival Date", value=datetime.now().date())
        arrival_time = st.time_input("Arrival Time", value=datetime.now().time())
        stops = st.number_input("Number of Stops", min_value=0, step=1)
        airline = st.selectbox("Airline", ["Select an Airline", "Jet Airways", "IndiGo", "Air India", "Multiple carriers", "SpiceJet", "Vistara", "GoAir", "Multiple carriers Premium economy", "Jet Airways Business", "Vistara Premium economy", "Trujet"], index = 0)
        source = st.selectbox("Source", ["Select Source City", "Delhi", "Kolkata", "Mumbai", "Chennai"], index = 0)
        destination = st.selectbox("Destination", ["Select Destination City", "Cochin", "Delhi", "Hyderabad", "Kolkata"], index = 0)

        submitted = st.form_submit_button("Predict")

    # Make API request to FastAPI
    if submitted:
        dep_datetime = datetime.combine(dep_date, dep_time).isoformat()
        arrival_datetime = datetime.combine(arrival_date, arrival_time).isoformat()

        payload = {
            "Dep_Time": dep_datetime,
            "Arrival_Time": arrival_datetime,
            "stops": stops,
            "airline": airline,
            "Source": source,
            "Destination": destination
        }

        response = requests.post("http://localhost:4000/predict", data=payload)
    
        if response.status_code == 200:
            prediction_rf = response.text
            st.markdown(prediction_rf.splitlines()[-20], unsafe_allow_html=True)
        else:
            st.error("Error occurred during prediction.")


if __name__ == "__main__":
    main()