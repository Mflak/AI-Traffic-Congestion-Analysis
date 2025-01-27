import pandas as pd
import numpy as np

# Function to generate random traffic data and save it to a CSV file
def generate_random_traffic_data(file_name="traffic_data_london.csv", num_rows=20000):
    # Random values for locations within London
    locations = ['Westminster', 'Camden', 'Islington', 'Kensington', 'Hackney', 
                 'Bromley', 'Greenwich', 'Croydon', 'Brent', 'Tower Hamlets']
    
    # Generate random data
    data = {
        "timestamp": pd.date_range(start="2024-08-01 00:00:00", periods=num_rows, freq="H").to_pydatetime(),
        "city": ["London"] * num_rows,  # Fixed city name as London
        "location": np.random.choice(locations, num_rows),  # Random locations in London
        "vehicle_count": np.random.randint(0, 200, size=num_rows)  # Random vehicle count
    }
    
    # Convert to DataFrame
    df = pd.DataFrame(data)
    
    # Save as CSV file
    df.to_csv(file_name, index=False)
    print(f"Random traffic data for London saved to {file_name}!")

# Generate the dataset
generate_random_traffic_data(file_name="traffic_data_london.csv", num_rows=20000)
