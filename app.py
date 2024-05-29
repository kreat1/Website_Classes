import streamlit as st
import pandas as pd

# Title of the web app
st.title("Dance Lessons Registration")

# Introduction text
st.write("Please fill out the form below to register for our dance lessons.")

# Creating the form
with st.form(key='registration_form'):
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    dance_style = st.selectbox("Preferred Dance Style", ["Ballet", "Hip-Hop", "Salsa", "Jazz", "Contemporary"])
    skill_level = st.selectbox("Skill Level", ["Beginner", "Intermediate", "Advanced"])
    
    # Submit button
    submit_button = st.form_submit_button(label='Register')

# Handling form submission
if submit_button:
    # Check for valid input
    if not name or not email:
        st.error("Please provide both your name and email.")
    else:
        # Create a dictionary with the input data
        registration_data = {
            "Name": name,
            "Email": email,
            "Dance Style": dance_style,
            "Skill Level": skill_level
        }
        
        # Load existing registrations
        try:
            registrations_df = pd.read_csv('registrations.csv')
        except FileNotFoundError:
            registrations_df = pd.DataFrame(columns=["Name", "Email", "Dance Style", "Skill Level"])
        
        # Append the new registration
        registrations_df = registrations_df.append(registration_data, ignore_index=True)
        
        # Save the updated registrations
        registrations_df.to_csv('registrations.csv', index=False)
        
        st.success("Thank you for registering! We will contact you soon.")

# Displaying registered participants
if st.checkbox("Show Registered Participants"):
    try:
        registrations_df = pd.read_csv('registrations.csv')
        st.write(registrations_df)
    except FileNotFoundError:
        st.write("No registrations yet.")
