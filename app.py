import streamlit as st
import pandas as pd

# Title of the web app
st.title("Dance Lessons Registration")

# Introduction text
st.write("Please fill out the form below to register for our dance lessons on either Tuesday or Thursday.")

# Load existing registrations
try:
    registrations_df = pd.read_csv('registrations.csv')
except FileNotFoundError:
    registrations_df = pd.DataFrame(columns=["Name", "Email", "Day"])

# Display the number of registrations
tuesday_count = registrations_df[registrations_df['Day'] == 'Tuesday'].shape[0]
thursday_count = registrations_df[registrations_df['Day'] == 'Thursday'].shape[0]

st.write(f"Registrations for Tuesday: {tuesday_count}/15")
st.write(f"Registrations for Thursday: {thursday_count}/15")

# Creating the form
with st.form(key='registration_form'):
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    day = st.selectbox("Preferred Day", ["Tuesday", "Thursday"])
    
    # Submit button
    submit_button = st.form_submit_button(label='Register')

# Handling form submission
if submit_button:
    # Check for valid input
    if not name or not email:
        st.error("Please provide both your name and email.")
    else:
        # Count current registrations for the selected day
        day_count = registrations_df[registrations_df['Day'] == day].shape[0]
        
        if day_count >= 15:
            st.error(f"Sorry, the class for {day} is full.")
        else:
            # Create a dictionary with the input data
            registration_data = {
                "Name": name,
                "Email": email,
                "Day": day
            }
            
            # Append the new registration
            registrations_df = registrations_df.append(registration_data, ignore_index=True)
            
            # Save the updated registrations
            registrations_df.to_csv('registrations.csv', index=False)
            
            st.success(f"Thank you for registering for the {day} class! We will contact you soon.")
            
            # Update the counts displayed
            tuesday_count = registrations_df[registrations_df['Day'] == 'Tuesday'].shape[0]
            thursday_count = registrations_df[registrations_df['Day'] == 'Thursday'].shape[0]
            st.write(f"Registrations for Tuesday: {tuesday_count}/15")
            st.write(f"Registrations for Thursday: {thursday_count}/15")

# Password protection for viewing registered participants
if st.checkbox("Show Registered Participants"):
    password = st.text_input("Enter Password", type="password")
    
    if password == "admin_password":  # Replace 'admin_password' with a secure password
        if not registrations_df.empty:
            tuesday_registrations = registrations_df[registrations_df['Day'] == 'Tuesday']
            thursday_registrations = registrations_df[registrations_df['Day'] == 'Thursday']
            
            st.write("### Tuesday Registrations")
            if not tuesday_registrations.empty:
                for index, row in tuesday_registrations.iterrows():
                    st.write(f"{index+1}. {row['Name']}")
            else:
                st.write("No registrations for Tuesday yet.")
            
            st.write("### Thursday Registrations")
            if not thursday_registrations.empty:
                for index, row in thursday_registrations.iterrows():
                    st.write(f"{index+1}. {row['Name']}")
            else:
                st.write("No registrations for Thursday yet.")
        else:
            st.write("No registrations yet.")
    else:
        st.error("Incorrect password. Access denied.")
