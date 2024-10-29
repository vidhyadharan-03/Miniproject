import streamlit as st
from pymongo import MongoClient
import bcrypt
from model import predict_cml_risk

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client['cml_risk_db']
users = db['users']

# Initialize session state variables
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user' not in st.session_state:
    st.session_state.user = None

# Sign-Up Function
def sign_up(username, password, name, age, gender):
    if users.find_one({"username": username}):
        st.error("Username already exists. Please choose another one.")
    else:
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        users.insert_one({
            "username": username,
            "password": hashed_password,
            "name": name,
            "age": age,
            "gender": gender
        })
        st.success("Account created successfully. You can now log in.")

# Login Function
def login(username, password):
    user = users.find_one({"username": username})
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
        st.session_state.logged_in = True
        st.session_state.user = user
        st.success("Logged in successfully!")
        blood_test_input_page()
    else:
        st.error("Incorrect username or password")

# Blood Test Input Page
def blood_test_input_page():
    st.title("CML Risk Prediction - Blood Test Input")

    # Blood test inputs
    rbc = st.number_input("Enter RBC count (millions/uL):", min_value=0.0, step=0.1)
    wbc = st.number_input("Enter WBC count (cells/uL):", min_value=0)
    platelet = st.number_input("Enter Platelet count (cells/uL):", min_value=0)

    # Prediction action
    if st.button("Predict CML Risk"):
        risk_level, probability = predict_cml_risk(rbc, wbc, platelet)
        st.write(f"Risk Level: {risk_level} (Probability Score: {probability:.2f})")

# Main App Logic
st.sidebar.title("Sign Up / Login")

# Check if user is logged in
if not st.session_state.logged_in:
    # Sidebar options for sign-up and login
    action = st.sidebar.radio("Choose Action", ["Login", "Sign Up"])

    if action == "Sign Up":
        st.sidebar.subheader("Create New Account")
        name = st.sidebar.text_input("Full Name")
        age = st.sidebar.number_input("Age", min_value=1, step=1)
        gender = st.sidebar.selectbox("Gender", ["Male", "Female", "Other"])
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type="password")
        if st.sidebar.button("Sign Up"):
            sign_up(username, password, name, age, gender)

    elif action == "Login":
        st.sidebar.subheader("Log In")
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type="password")
        if st.sidebar.button("Login"):
            login(username, password)

else:
    # Display welcome message and logout option in the sidebar
    st.sidebar.write(f"Welcome, {st.session_state.user['name']}!")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.experimental_rerun()  # Rerun to refresh the page after logout

    # Display the blood test input page for logged-in users
    blood_test_input_page()
