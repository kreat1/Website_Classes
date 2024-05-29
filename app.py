import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Title of the web app
st.title("Dance Lessons Registration")

# Introduction text
st.write("Please fill out the form below to register for our dance lessons on either Tuesday or Thursday.")

# Load existing registrations
try:
    registrations_df = pd.read_csv('registrations.csv')
    # Ensure that the DataFrame has the correct columns, even if the CSV is empty
    if registrations_df.empty:
        registrations_df = pd.DataFrame(columns=["Name", "Email", "Day", "Date"])
except (FileNotFoundError, pd.errors.EmptyDataError):
    registrations_df = pd.DataFrame(columns=["Name", "Email", "Day", "Date"])

# Get today's date and the next Tuesday and Thursday
today = datetime.today()
next_tuesday = today + timedelta((1 - today.weekday() + 7) % 7)  # Next Tuesday
next_thursday = today + timedelta((3 - today.weekday() + 7) % 7)  # Next Thursday
following_tuesday = next_tuesday + timedelta(weeks=1)  # Following Tuesday
following_thursday = next_thursday + timedelta(weeks=1)  # Following Thursday

# Display the number of registrations for the next and following week
def get_count(day, date):
    return registrations_df[(registrations_df['Day'] == day) & (registrations_df['Date'] == date)].shape[0]

next_tuesday_count = get_count("Tuesday", next_tuesday.date())
next_thursday_count = get_count("Thursday", next_thursday.date())
following_tuesday_count = get_count("Tuesday", following_tuesday.date())
following_thursday_count = get_count("Thursday", following_thursday.date())

st.write(f"Registrations for next Tuesday ({next_tuesday.date()}): {next_tuesday_count}/15")
st.write(f"Registrations for next Thursday ({next_thursday.date()}): {next_thursday_count}/15")
st.write(f"Registrations for the following Tuesday ({following_tuesday.date()}): {following_tuesday_count}/15")
st.write(f"Registrations for the following Thursday ({following_thursday.date()}): {following_thursday_count}/15")

# Creating the form
with st.form(key='registration_form'):
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    day = st.selectbox("Preferred Day", ["Tuesday", "Thursday"])
    week = st.selectbox("Preferred Week", ["Next Week", "Following Week"])
    
    # Submit button
    submit_button = st.form_submit_button(label='Register')

# Handling form submission
if submit_button:
    # Determine the correct date based on user selection
    if day == "Tuesday":
        date = next_tuesday if week == "Next Week" else following_tuesday
    else:
        date = next_thursday if week == "Next Week" else following_thursday

    # Check for valid input
    if not name or not email:
        st.error("Please provide both your name and email.")
    else:
        # Count current registrations for the selected day and date
        day_count = get_count(day, date.date())
        
        if day_count >= 15:
            st.error(f"Sorry, the class for {day}, {date.date()} is full.")
        else:
            # Create a dictionary with the input data
            registration_data = {
                "Name": name,
                "Email": email,
                "Day": day,
                "Date": date.date()
            }
            
            # Append the new registration using pd.concat
            registrations_df = pd.concat([registrations_df, pd.DataFrame([registration_data])], ignore_index=True)
            
            # Save the updated registrations
            registrations_df.to_csv('registrations.csv', index=False)
            
            st.success(f"Thank you for registering for the {day} class on {date.date()}! We will contact you soon.")
            
            # Update the counts displayed
            next_tuesday_count = get_count("Tuesday", next_tuesday.date())
            next_thursday_count = get_count("Thursday", next_thursday.date())
            following_tuesday_count = get_count("Tuesday", following_tuesday.date())
            following_thursday_count = get_count("Thursday", following_thursday.date())
            st.write(f"Registrations for next Tuesday ({next_tuesday.date()}): {next_tuesday_count}/15")
            st.write(f"Registrations for next Thursday ({next_thursday.date()}): {next_thursday_count}/15")
            st.write(f"Registrations for the following Tuesday ({following_tuesday.date()}): {following_tuesday_count}/15")
            st.write(f"Registrations for the following Thursday ({following_thursday.date()}): {following_thursday_count}/15")

# Password protection for viewing registered participants
if st.checkbox("Show Registered Participants"):
    password = st.text_input("Enter Password", type="password")
    
    if password == "admin_password":  # Replace 'admin_password' with a secure password
        if not registrations_df.empty:
            for day, date in [("Tuesday", next_tuesday.date()), ("Thursday", next_thursday.date()), ("Tuesday", following_tuesday.date()), ("Thursday", following_thursday.date())]:
                registrations = registrations_df[(registrations_df['Day'] == day) & (registrations_df['Date'] == date)]
                
                st.write(f"### {day} Registrations for {date}")
                if not registrations.empty:
                    for index, row in registrations.iterrows():
                        st.write(f"{index+1}. {row['Name']}")
                else:
                    st.write(f"No registrations for {day} on {date} yet.")
        else:
            st.write("No registrations yet.")
    else:
        st.error("Incorrect password. Access denied.")
