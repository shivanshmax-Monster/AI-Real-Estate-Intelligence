import numpy as np
import pandas as pd

def generate_housing_data(filename="housing_data.csv", n_samples=1200, seed=42):
    np.random.seed(seed)
    
    prop_ids = [f"PROP-{1000 + i}" for i in range(n_samples)]
    
    # Core numerical features
    sqft = np.random.normal(2100, 650, n_samples).astype(int)
    sqft = np.clip(sqft, 750, 4800)
    
    # Bedrooms correlated with sqft
    bedrooms = np.clip((sqft / 600 + np.random.normal(0, 0.6, n_samples)).astype(int), 1, 6)
    
    # Bathrooms correlated with bedrooms
    bathrooms = np.clip((bedrooms * 0.7 + np.random.normal(0.5, 0.4, n_samples)), 1.0, 5.0)
    bathrooms = np.round(bathrooms * 2) / 2 # quarter/half baths
    
    # Property age (0 to 60 years)
    age = np.random.randint(0, 55, n_samples)
    
    # Lot size
    lot_sqft = (sqft * np.random.uniform(1.8, 5.2, n_samples)).astype(int)
    
    # Garage capacity (0 to 3 cars)
    garage = np.clip((sqft / 1100 + np.random.normal(0, 0.7, n_samples)).astype(int), 0, 3)
    
    # Location tier
    location_tiers = np.random.choice(
        ["Urban Metro", "Suburban Prime", "Suburban Standard", "Emerging Tech Corridor", "Exurban"],
        size=n_samples,
        p=[0.25, 0.30, 0.20, 0.15, 0.10]
    )
    
    # Distance to city center (miles)
    distance_map = {
        "Urban Metro": (1, 6),
        "Emerging Tech Corridor": (5, 14),
        "Suburban Prime": (8, 22),
        "Suburban Standard": (12, 28),
        "Exurban": (25, 50)
    }
    distance = np.array([np.random.uniform(*distance_map[t]) for t in location_tiers]).round(1)
    
    # Renovation rating (1 to 10)
    renovation_score = np.random.choice(range(1, 11), size=n_samples, p=[0.05, 0.08, 0.12, 0.15, 0.20, 0.18, 0.10, 0.06, 0.04, 0.02])
    
    # Property condition
    condition = np.where(renovation_score >= 8, "Excellent",
                np.where(renovation_score >= 5, "Good",
                np.where(renovation_score >= 3, "Fair", "Needs Renovation")))
    
    # Price base calculation
    tier_multipliers = {
        "Urban Metro": 1.45,
        "Suburban Prime": 1.30,
        "Emerging Tech Corridor": 1.25,
        "Suburban Standard": 1.00,
        "Exurban": 0.82
    }
    
    tier_mult = np.array([tier_multipliers[t] for t in location_tiers])
    
    base_price = (
        sqft * 165 +
        bedrooms * 18000 +
        bathrooms * 22000 +
        garage * 14000 -
        age * 1200 +
        renovation_score * 7500 -
        distance * 2100 +
        lot_sqft * 6.5
    )
    
    price = (base_price * tier_mult + np.random.normal(0, 22000, n_samples)).astype(int)
    price = np.clip(price, 120000, 1450000)
    
    # Quarterly transaction tracking
    quarters = np.random.choice(["2023-Q1", "2023-Q2", "2023-Q3", "2023-Q4", "2024-Q1", "2024-Q2"], size=n_samples)
    
    # Annual property tax estimate (~1.1% of value)
    annual_tax = (price * 0.0112 + np.random.normal(0, 300, n_samples)).astype(int)
    
    df = pd.DataFrame({
        "Property_ID": prop_ids,
        "Square_Footage": sqft,
        "Bedrooms": bedrooms,
        "Bathrooms": bathrooms,
        "Property_Age_Years": age,
        "Lot_Size_SqFt": lot_sqft,
        "Garage_Cars": garage,
        "Location_Tier": location_tiers,
        "Distance_to_City_Miles": distance,
        "Renovation_Score": renovation_score,
        "Condition": condition,
        "Quarter_Sold": quarters,
        "Annual_Tax": annual_tax,
        "Price": price
    })
    
    df.to_csv(filename, index=False)
    print(f"Generated {n_samples} real estate records saved to {filename}")
    return df

if __name__ == "__main__":
    generate_housing_data()
