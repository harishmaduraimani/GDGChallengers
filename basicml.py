import time
import random
import pandas as pd
import folium
from pytrends.request import TrendReq
import googlemaps
import json
from model import fd


# 🔑 Google Maps API Key (Replace with your own API Key)
GOOGLE_MAPS_API_KEY = "AIzaSyDf6zbrfjDlkMAQ0BgCKJ2-vggSi0lXtgM"

# Initialize Google Maps client
gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)

# Initialize Pytrends
pytrends = TrendReq(hl='en-US', tz=360)

# 🔹 Fetch Trending Business Keywords
def fetch_trending_business_keywords():
    try:
        pytrends.build_payload(kw_list=['business', 'startup', 'small business'], timeframe='now 7-d')
        data = pytrends.related_queries()

        if data and 'business' in data and data['business']['top'] is not None:
            return data['business']['top']['query'].tolist()
        return ["small business", "startup ideas", "local shops"]  # Default fallback
    except Exception as e:
        print("❌ Error fetching Google Trends:", e)
        return []

# 🔹 Fetch Nearby Businesses from Google Maps API
def fetch_nearby_businesses(location, radius, business_types=None):
    if business_types is None:
        business_types = ["store", "supermarket", "electronics_store", "restaurant", "cafe", "shopping_mall"]

    businesses = []
    
    for b_type in business_types:
        try:
            places_result = gmaps.places_nearby(location=location, radius=radius, type=b_type)
        
            
            for place in places_result.get('results', []):
                businesses.append({
                    "name": place.get('name', 'Unknown'),
                    "rating": place.get('rating', 'N/A'),
                    "address": place.get('vicinity', 'No address available'),
                    "business_type": b_type,
                    "lat": place["geometry"]["location"]["lat"],
                    "lng": place["geometry"]["location"]["lng"]
                })
        except Exception as e:
            print(f"❌ Error fetching businesses ({b_type}):", e)

    return businesses

# 🔹 Create Business Map with Hotspots
def create_business_map(location, radius, businesses):
    business_map = folium.Map(location=location, zoom_start=13)

    # Add a shaded circular region to represent the search area
    folium.Circle(
        location=location,
        radius=radius,  
        color="blue",
        fill=True,
        fill_color="blue",
        fill_opacity=0.2
    ).add_to(business_map)

    # Add markers for each business
    for business in businesses:
        try:
            rating = float(business['rating']) if business['rating'] != 'N/A' else 0
        except ValueError:
            rating = 0

        # High-rated businesses (hot businesses)
        icon_color = "red" if rating >= 4.5 else "blue"

        folium.Marker(
            location=(business["lat"], business["lng"]),
            popup=f"{business['name']} ({business['business_type']})\nRating: {business['rating']}",
            icon=folium.Icon(color=icon_color)
        ).add_to(business_map)

    return business_map


# 🔹 Analyze Business Feasibility
import matplotlib.pyplot as plt

def analyze_business(location, business_category, radius=2000):
    competitors = fetch_nearby_businesses(location, radius, business_types=[business_category])
    comp_count = len(competitors)

    # Business category data
    business_data = {
        "electronics store": {
            "investment_range": (800000, 1200000),
            "profit_range": (250000, 450000),
            "peak_season": "Diwali"
        },
        "clothing store": {
            "investment_range": (500000, 900000),
            "profit_range": (150000, 300000),
            "peak_season": "Festival Season"
        },
        "Saloon": {
            "investment_range": (300000, 500000),
            "profit_range": (50000, 100000),
            "peak_season": "Weekends"
        },
        "Super Market": {
            "investment_range": (2500000, 7000000),
            "profit_range": (150000, 200000),
            "peak_season": "Festival Season"
        },
        "Resturant": {
            "investment_range": (1500000, 2000000),
            "profit_range": (50000, 100000),
            "peak_season": "Everyday"
        },
        "Clinic": {
            "investment_range": (300000, 500000),
            "profit_range": (50000, 100000),
            "peak_season": "Evening/Weekends"
        },
        "Food": {
            "investment_range": (100000, 500000),
            "profit_range": (50000, 100000),
            "peak_season": "Everyday"
        }
    }

    # Default values if business category not found
    default_investment = (100000, 500000)
    default_profit = (25000, 75000)
    default_season = "General Season"

    data = business_data.get(business_category, {})
    investment_needed = data.get("investment_range", default_investment)
    profit_estimate = data.get("profit_range", default_profit)
    peak_season = data.get("peak_season", default_season)

    risk_score = min((comp_count / 10) * 10, 10)  # Cap risk at 10
    risk_level = "High" if risk_score > 7 else "Moderate" if risk_score > 4 else "Low"

    # 📋 Business Report
    print(f"📍 Location: Chennai, India")
    print(f"🏢 Business Category: {business_category}")
    print("\n📈 Business Potential & Risk Analysis")
    print(f"💰 Estimated Monthly Profit: ₹{profit_estimate[0]:,} – ₹{profit_estimate[1]:,}")
    print(f"💵 Investment Needed: ₹{investment_needed[0]:,} – ₹{investment_needed[1]:,}")
    print(f"⚖ Competition Level: 🔥 {risk_level} ({comp_count} similar shops nearby)")
    print(f"⚠ Risk Score: {risk_score:.1f}/10 ({risk_level} risk)")
    print(f"⏳ Peak Profit Timeline: 8–12 months")
    print(f"📊 Seasonal Demand Trend: High sales during {peak_season}, moderate rest of the year")

    # 🥧 Pie Chart: Risk Score
    plt.figure(figsize=(4.5, 4.5))
    labels = ['Risk', 'Remaining']
    values = [risk_score, 10 - risk_score]
    colors = ['red', 'lightgreen']
    explode = (0.1, 0)  # Emphasize risk part

    plt.pie(values, labels=labels, colors=colors, autopct='%1.1f%%', explode=explode, startangle=90)
    plt.title("⚠ Risk Score Analysis (out of 10)")
    plt.tight_layout()
    plt.show()

    # 📊 Bar Chart: Investment vs Profit
    plt.figure(figsize=(6, 4))
    bars = ["Min Investment", "Max Investment", "Min Profit", "Max Profit"]
    values = [
        investment_needed[0], investment_needed[1],
        profit_estimate[0], profit_estimate[1]
    ]
    bar_colors = ['gray', 'gray', 'green', 'green']
    plt.bar(bars, values, color=bar_colors)
    plt.title("💵 Investment vs Monthly Profit Range")
    plt.ylabel("Amount (₹)")
    plt.xticks(rotation=15)
    plt.tight_layout()
    plt.show()

def main():
    location = (12.8942923,80.2024956)  # Chennai, India
    radius = 500  # 3km radius

    print("📌 Fetching trending business topics...")
    trending_keywords = fetch_trending_business_keywords()


    print("\n📌 Fetching all nearby businesses...")
    businesses = fetch_nearby_businesses(location, radius)
    
    if not businesses:
        print("❌ No businesses found! Try increasing the search radius or checking API key permissions.")
    else:
        # Save businesses to a JSON file
        fd(businesses)

    # 🔍 Analyze Business Feasibility
    #analyze_business(location, business_category="electronics_store", radius=2000)

    # 🌍 Create a business heatmap
    business_map = create_business_map(location, radius, businesses)
    business_map.save("business_map.html")
    print("\n📍 Business heatmap saved as 'business_map.html' (Open in browser)")
    cat_name=input("hey tell me ur bussiness category  \n")
    analyze_business(location,cat_name, radius)
# Run the program
if __name__ == "__main__":
    main()
