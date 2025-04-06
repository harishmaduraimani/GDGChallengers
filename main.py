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
import plotly.express as px
import pandas as pd
import re

# LangChain imports
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

# Load environment variables
load_dotenv()

# API Keys
BUZZISSS_API_KEY = os.getenv("GENAI_API_KEY") or "your-gemini-api-key"
GOOGLE_MAPS_KEY = os.getenv("GOOGLE_MAPS_API_KEY") or "your-gmaps-api-key"

# Google Maps setup
gmaps = googlemaps.Client(key=GOOGLE_MAPS_KEY)
geolocator = Nominatim(user_agent="business_predictor")

# LangChain Buzzisss Model Setup
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=BUZZISSS_API_KEY)
memory = ConversationBufferMemory()
chat_chain = ConversationChain(llm=llm, memory=memory)

# --- Buzzisss REST API Call ---
def get_business_idea(location, budget, income, interest):
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-pro:generateContent?key={BUZZISSS_API_KEY}"
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
# --- Folium Heatmap with Rating-based Color Change ---
# --- Folium Heatmap with Rating-based Color Change and Popup Info ---
# --- Folium Heatmap with Circle of Radius and Rating-based Color Change ---
def plot_heatmap(businesses, lat, lng, radius=2000):
    m = folium.Map(location=[lat, lng], zoom_start=13, control_scale=True)

    # Add a circle with a specified radius around the central point
    folium.Circle(
        location=[lat, lng],  # Center of the circle (latitude and longitude)
        radius=radius,        # Radius in meters (default 2000 meters = 2 km)
        color='blue',         # Circle border color
        fill=True,            # Whether the circle should be filled
        fill_color='blue',    # Fill color for the circle
        fill_opacity=0.3      # Transparency of the fill
    ).add_to(m)

    # Define rating to color mapping
    def rating_to_color(rating):
        if rating >= 4.5:
            return 'green'  # High rating (green)
        elif rating >= 3.0:
            return 'yellow'  # Moderate rating (yellow)
        else:
            return 'red'  # Low rating (red)
    
    for biz in businesses:
        loc = biz['geometry']['location']
        name = biz.get('name', 'Unknown')
        rating = biz.get('rating', 'N/A')  # Default to 'N/A' if no rating is available
        
        # Create a marker with a popup that shows the name and rating
        folium.CircleMarker(
            location=[loc['lat'], loc['lng']],
            radius=5,
            color=rating_to_color(rating),
            fill=True,
            fill_color=rating_to_color(rating)
        ).add_to(m).add_child(
            folium.Popup(f"<b>{name}</b><br>Rating: {rating}", max_width=300)
        )
    
    return m


# --- Demand vs Risk Donut Chart ---
def plot_donut_chart():
    labels = ['High Demand, Low Risk', 'Moderate Demand, Moderate Risk', 'Low Demand, High Risk']
    values = [45, 35, 20]
    fig = px.pie(values=values, names=labels, hole=0.5, title="Demand vs Risk")
    return fig

# --- Category-wise Demand Line Chart ---
def plot_line_chart():
    df = pd.DataFrame({
        "Category": ["Food", "Clothing", "Tech", "Services"],
        "Demand": [70, 55, 80, 60]
    })
    fig = px.line(df, x="Category", y="Demand", markers=True, title="Category-wise Demand")
    return fig

# --- ROI Indicator ---
def plot_roi_indicator():
    fig = px.bar(x=["Investment", "Expected Profit"], y=[100000, 250000], text=["₹1L", "₹2.5L"], title="ROI Overview")
    return fig

# --- Streamlit UI Setup ---
st.set_page_config(page_title="Local Business Predictor", layout="wide")
from PIL import Image

# Load and display logo neatly at the top
logo_main = Image.open("jfv.png")
col1, col2 = st.columns([1, 5])
with col1:
    st.image(logo_main, width=300)
with col2:
    st.title("Local Business Prediction")


# Session State Initialization
if 'business_idea' not in st.session_state:
    st.session_state.business_idea = None
if 'business_map' not in st.session_state:
    st.session_state.business_map = None
if 'show_chat_button' not in st.session_state:
    st.session_state.show_chat_button = False

# --- Sidebar Toggle UI ---
with st.sidebar:
    st.image("jfv.png", width=200)
    st.title(" User Info / Chat")
    mode = st.radio("Choose mode:", ["📋 Input Form", "💬 Chat"])

    if mode == "📋 Input Form":
        with st.form("business_form"):
            location = st.text_input("📍 Location", "Coimbatore")
            budget = st.text_input("💸 Budget", "₹1.5 lakhs")
            income = st.text_input("💰 Monthly Income", "₹25,000")
            interest = st.text_input("💼 Business Interest", "food or clothing")
            submitted = st.form_submit_button("🚀 Generate")

    elif mode == "💬 Chat" and st.session_state.show_chat_button:
        user_query = st.text_input("Ask Buzzisss a question:")
        if st.button("Ask Buzzisss"):
            if user_query.strip():
                response = chat_chain.run(user_query)
                st.markdown(f"**Buzzisss:** {response}")
            else:
                st.warning("Please enter a question.")

# --- Main Area Output ---
if 'submitted' in locals() and submitted:
    with st.spinner("Analyzing and generating business ideas..."):
        idea = get_business_idea(location, budget, income, interest)
        st.session_state.business_idea = idea

        businesses, lat, lng = get_nearby_businesses(location, keyword=interest)
        if businesses:
            map_obj = plot_heatmap(businesses, lat, lng)
            st.session_state.business_map = map_obj

        st.session_state.show_chat_button = True

# --- Business Idea + Summary Cards ---
# --- Business Idea + Summary Cards ---
# --- Business Idea + Summary Cards ---
if st.session_state.business_idea:
    st.subheader("📌 Suggested Business Idea")

    # Extract metrics using regex
    idea_text = st.session_state.business_idea
    risk_match = re.search(r"(?i)risk(?: score)?:\s*(.*)", idea_text)
    investment_match = re.search(r"(?i)investment(?: required)?:\s*(.*)", idea_text)
    profit_match = re.search(r"(?i)(expected )?profit(?: margin|)?(?:\:|\s)?\s*(.*)", idea_text)

    risk = risk_match.group(1).strip() if risk_match else "N/A"
    investment = investment_match.group(1).strip() if investment_match else "N/A"
    profit = profit_match.group(2).strip() if profit_match else "N/A"

    # Card Styling
    st.markdown("""
        <style>
            .business-card {
                background-color: #f8f9fa;
                padding: 20px;
                border-radius: 15px;
                border-left: 6px solid #3b82f6;
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
                margin-bottom: 15px;
            }
            .summary-card {
                background-color: #ffffff;
                padding: 18px;
                border-radius: 15px;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
                font-size: 16px;
            }
            .summary-card ul {
                list-style-type: none;
                padding: 0;
            }
            .summary-card li {
                margin: 8px 0;
                font-weight: 500;
            }
            .considerations-card {
                background-color: #ffffff;
                padding: 18px;
                border-radius: 15px;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
                font-size: 16px;
                margin-top: 20px;
            }
        </style>
    """, unsafe_allow_html=True)

    # Use columns for side-by-side layout
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown(f"""
        <div class="business-card">
            <h5>💡 Buzzisss Suggestion</h5>
            <p style="font-size: 16px;">{idea_text}</p>
        </div>
        """ , unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="summary-card">
            <h6>📊 Key Metrics</h6>
            <ul>
                <li>🧮 <strong>Risk Score:</strong> {risk}</li>
                <li>💰 <strong>Investment:</strong> {investment}</li>
                <li>📈 <strong>Expected Profit:</strong> {profit}</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        # Important Considerations - Displayed beside key metrics
        st.markdown("""
        <div class="considerations-card">
            <h6>💡 Important Considerations</h6>
            <ul>
                <li>📊 <strong>Market Research:</strong> Conduct thorough market research in your local area.</li>
                <li>📋 <strong>Business Plan:</strong> Develop a detailed business plan outlining your target market, pricing strategy, marketing plan, and financial projections.</li>
                <li>⚖️ <strong>Legal and Regulatory Requirements:</strong> Obtain necessary licenses and permits to operate your business legally.</li>
                <li>📣 <strong>Marketing and Promotion:</strong> Invest in effective marketing strategies to reach your target customers.</li>
                <li>💵 <strong>Financial Management:</strong> Keep track of your income and expenses and manage your finances carefully.</li>
            </ul>
            <p style="font-size: 14px;">These considerations are essential for ensuring that your business is legally compliant and financially successful.</p>
        </div>
        """, unsafe_allow_html=True)

    # Charts Layout
    col1, col2, col3 = st.columns(3)
    with col1:
        st.plotly_chart(plot_donut_chart(), use_container_width=True)
    with col2:
        st.plotly_chart(plot_line_chart(), use_container_width=True)
    with col3:
        st.plotly_chart(plot_roi_indicator(), use_container_width=True)

# --- Business Map ---
if st.session_state.business_map:
    st.subheader("📍 Business Density Map (Nearby)")
    st_folium(st.session_state.business_map, width=1000, height=550)
