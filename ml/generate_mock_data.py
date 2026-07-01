import pandas as pd
import numpy as np
import random

# Set a random seed so the data is reproducible
np.random.seed(42)

# --- 1. Define Parameters & Constants ---
NUM_RECORDS = 500

# Tarkwa base coordinates (approximate)
BASE_LAT = 5.3018
BASE_LNG = -1.9930

# Hackathon target crops [cite: 10]
CROP_TYPES = ['Tomatoes', 'Peppers', 'Garden Eggs', 'Okra', 'Leafy Greens']
ROAD_CONDITIONS = ['Good', 'Fair', 'Poor']

# Pricing logic factors (in GHS)
BASE_FARE = 20.0
RATE_PER_KM = 3.5
RATE_PER_KG = 0.15

# --- 2. Generate Features ---
# Simulate distances between 2km (local) and 80km (Tarkwa to Takoradi outskirts)
distances_km = np.random.uniform(2.0, 80.0, NUM_RECORDS)

# Simulate payload weights from 50kg (small farm) to 1000kg (commercial load)
payloads_kg = np.random.uniform(50.0, 1000.0, NUM_RECORDS)

# Randomly assign crops and road conditions
crops = np.random.choice(CROP_TYPES, NUM_RECORDS)
roads = np.random.choice(ROAD_CONDITIONS, NUM_RECORDS, p=[0.4, 0.4, 0.2])

# Generate mock coordinates based on distance (simplified offset)
# 1 degree of latitude is roughly 111km
lat_offsets = (distances_km / 111.0) * np.random.choice([-1, 1], NUM_RECORDS) * np.random.rand(NUM_RECORDS)
lng_offsets = (distances_km / 111.0) * np.random.choice([-1, 1], NUM_RECORDS) * np.random.rand(NUM_RECORDS)

pickup_lats = BASE_LAT + lat_offsets
pickup_lngs = BASE_LNG + lng_offsets

# For simplicity in this mock, buyers are centrally located near the base
dropoff_lats = np.full(NUM_RECORDS, BASE_LAT) + (np.random.rand(NUM_RECORDS) * 0.05)
dropoff_lngs = np.full(NUM_RECORDS, BASE_LNG) + (np.random.rand(NUM_RECORDS) * 0.05)

# --- 3. Calculate the Target Variable (Estimated Cost in GHS) ---
costs_ghs = []
for i in range(NUM_RECORDS):
    # Base calculation
    cost = BASE_FARE + (distances_km[i] * RATE_PER_KM) + (payloads_kg[i] * RATE_PER_KG)
    
    # Apply road condition multipliers
    if roads[i] == 'Fair':
        cost *= 1.15 # 15% surcharge for fair roads
    elif roads[i] == 'Poor':
        cost *= 1.35 # 35% surcharge for poor roads
        
    # Add some random market noise (± 10%) to make the ML model actually have to learn
    noise = np.random.uniform(0.9, 1.1)
    final_cost = round(cost * noise, 2)
    costs_ghs.append(final_cost)

# --- 4. Assemble and Export ---
df = pd.DataFrame({
    'crop_type': crops,
    'payload_kg': np.round(payloads_kg, 1),
    'distance_km': np.round(distances_km, 1),
    'pickup_lat': np.round(pickup_lats, 6),
    'pickup_lng': np.round(pickup_lngs, 6),
    'dropoff_lat': np.round(dropoff_lats, 6),
    'dropoff_lng': np.round(dropoff_lngs, 6),
    'road_condition': roads,
    'actual_cost_ghs': costs_ghs
})

# Save to CSV
csv_filename = 'agritech_transport_data_mock.csv'
df.to_csv(csv_filename, index=False)

print(f"✅ Successfully generated {NUM_RECORDS} rows of mock data.")
print(f"📁 Saved to {csv_filename}")
print(df.head())