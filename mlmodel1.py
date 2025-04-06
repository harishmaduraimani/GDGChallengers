import json
import pandas as pd
from test import ml  # Import your ML model function

# Load JSON data from file

# Business category mapping
def fd(data):
    business_counts = {}

    for business in data:
        business_name = business.get("name", "").strip()  # Extract and clean business name
        business_type = business.get("business_type", "Unknown").strip().lower()

        # Skip businesses with no name
        if not business_name:
            continue
        
        
        # If business type is vague, predict using ML model
        if business_type in ["shop", "store", "others", "unknown"]:
            predicted_category = ml([business_name])  # Pass as a single-element list
            business_type = predicted_category  # Replace vague type with predicted category
        print(business_name,business_type)
        # Count occurrences
        business_counts[business_type] = business_counts.get(business_type, 0) + 1

    # Convert to DataFrame for table representation
    df = pd.DataFrame(list(business_counts.items()), columns=["Business Type", "Count"])

    # Print the table
    print(df)
