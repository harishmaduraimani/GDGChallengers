import os
import requests
import json
from pytrends.request import TrendReq
import googlemaps
from geopy.geocoders import Nominatim
import folium
from streamlit_folium import st_folium
from dotenv import load_dotenv
import streamlit as st

# LangChain imports
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

# Load environment variables
load_dotenv()

# API Keys
GEMINI_API_KEY = os.getenv("GENAI_API_KEY") or "your-gemini-api-key"
GOOGLE_MAPS_KEY = os.getenv("GOOGLE_MAPS_API_KEY") or "your-gmaps-api-key"

# Google Maps setup
gmaps = googlemaps.Client(key=GOOGLE_MAPS_KEY)
geolocator = Nominatim(user_agent="business_predictor")

# LangChain Gemini Model Setup
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=GEMINI_API_KEY)
memory = ConversationBufferMemory()
chat_chain = ConversationChain(llm=llm, memory=memory)

# --- Gemini REST API Call ---
def get_business_idea(location, budget, income, interest):
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-pro:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [{
            "parts": [{
                "text": f"I'm from {location}. I have a budget of {budget}, monthly income of {income}, "
                        f"and I'm interested in {interest}. Suggest a profitable business idea with risk score, investment, and expected profit."
            }]
        }]
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    try:
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    except:
        return "❌ Error generating business idea. Check your API key or input."

# --- Google Maps Nearby Search ---
def get_nearby_businesses(location_name, keyword="shop", radius=2000):
    location = geolocator.geocode(location_name)
    lat, lng = location.latitude, location.longitude
    results = gmaps.places_nearby(location=(lat, lng), radius=radius, keyword=keyword)
    return results['results'], lat, lng

# --- Folium Heatmap ---
def plot_heatmap(businesses, lat, lng):
    m = folium.Map(location=[lat, lng], zoom_start=13, control_scale=True)
    for biz in businesses:
        loc = biz['geometry']['location']
        folium.CircleMarker(
            location=[loc['lat'], loc['lng']],
            radius=5,
            color='blue',
            fill=True,
            fill_color='blue'
        ).add_to(m)
    return m

# --- Streamlit UI ---
st.set_page_config(page_title="Local Business Predictor", layout="wide")
st.title("🧠 Gemini-Powered Local Business Predictor")

# Initialize session state variables for persistent data
if 'business_idea' not in st.session_state:
    st.session_state.business_idea = None
if 'business_map' not in st.session_state:
    st.session_state.business_map = None
if 'show_chat_button' not in st.session_state:
    st.session_state.show_chat_button = False

# Form submission
with st.form("business_form"):
    location = st.text_input("📍 Your Location", "Coimbatore")
    budget = st.text_input("💸 Your Budget", "₹1.5 lakhs")
    income = st.text_input("💰 Monthly Income", "₹25,000")
    interest = st.text_input("💼 Your Business Interest", "food or clothing")

    submitted = st.form_submit_button("🚀 Generate Business Insights")

if submitted:
    with st.spinner("Analyzing and generating business ideas..."):
        # Generate business idea
        idea = get_business_idea(location, budget, income, interest)
        st.session_state.business_idea = idea  # Store the business idea in session state

        # Display business density map
        businesses, lat, lng = get_nearby_businesses(location, keyword=interest)
        if businesses:
            map_obj = plot_heatmap(businesses, lat, lng)
            st.session_state.business_map = map_obj  # Store the map in session state

        # Set the flag to True to show the 'Ask Gemini' button after generating insights
        st.session_state.show_chat_button = True

# --- Displaying Persistent Data ---
if st.session_state.business_idea:
    st.subheader("📌 Suggested Business Idea")
    st.markdown(st.session_state.business_idea)

if st.session_state.business_map:
    st.subheader("📍 Business Density Map (Nearby)")
    st_folium(st.session_state.business_map, width=900, height=600)

# --- Chatbot Interface (Appears after generating business insights) ---
if st.session_state.show_chat_button:
    st.markdown("---")
    st.subheader("💬 Ask Anything About Business")
    
    user_query = st.text_input("Type your question below:")

    if st.button("Ask Gemini"):
        if user_query.strip():
            response = chat_chain.run(user_query)
            st.markdown(f"**Gemini:** {response}")
        else:
            st.warning("Please enter a question to ask Gemini.")
