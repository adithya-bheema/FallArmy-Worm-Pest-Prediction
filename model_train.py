import numpy as np 
import pandas as pd 
import pickle 
from sklearn.model_selection import train_test_split 
from sklearn.ensemble import RandomForestRegressor 
from sklearn.preprocessing import StandardScaler 
from sklearn.metrics import mean_squared_error 
# Load dataset 
data = pd.read_csv('sample.csv') 
data.dropna(inplace=True)  # Remove missing values 
# Encode categorical variables (Convert 'Place' to numbers) 
data['Place_Encoded'] = data['Place'].astype('category').cat.codes 
# Define features and target 
features = ['WindFlow', 'Rainfall', 'Humidity', 'Temperature', 'Place_Encoded'] 
scaler = StandardScaler() 
# Convert feature columns to numeric, coerce errors to NaN
for col in features:
    data[col] = pd.to_numeric(data[col], errors='coerce')

# Drop rows with any NaN after conversion
data.dropna(subset=features, inplace=True)

# Now scale
data[features] = scaler.fit_transform(data[features])
 # Standardize features 
# Encode target variable numerically (Low = 1, Moderate = 2, High = 3) 
risk_mapping = {'Low': 1, 'Moderate': 2, 'High': 3} 
data['PestActivity_Encoded'] = data['PestActivity'].map(risk_mapping) 
# Split data into training (80%) and testing (20%) 
X = data[features] 
y = data['PestActivity_Encoded'] 
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42) 
# Train the RandomForestRegressor Model 
model = RandomForestRegressor(n_estimators=300, random_state=42) 
model.fit(X_train, y_train) 
# Model evaluation 
predictions = model.predict(X_test) 
mse = mean_squared_error(y_test, predictions) 
print("Mean Squared Error:", mse) 
# Save the trained model 
with open('pest_risk_model.pkl', 'wb') as file: 
    pickle.dump({'model': model, 'scaler': scaler}, file) 
print("Model saved as 'pest_risk_model.pkl'") 
# Function to map predicted values to risk levels 
def map_risk(value): 
    if value < 1.5: 
        return 'Low Risk' 
    elif value < 2.5: 
        return 'Moderate Risk' 
    else: 
        return 'High Risk' 
# Test the model with sample input 
def predict_risk(wind_flow, rainfall, humidity, temperature, place): 
    if place.lower() not in data['Place'].str.lower().values: 
        return "Error: Place not found in dataset. Please enter a valid place." 
    # Get place encoding 
    place_encoded = data[data['Place'].str.lower() == 
    place.lower()]['Place_Encoded'].values[0] 
    # Prepare input data 
    input_data = pd.DataFrame([[wind_flow, rainfall, humidity, temperature, 
    place_encoded]],  
    columns=features) 
    input_data_scaled = pd.DataFrame(scaler.transform(input_data), columns=features) 
    # Make prediction 
    predicted_value = model.predict(input_data_scaled)[0] 
    risk_level = map_risk(predicted_value) 
    return f"Predicted Pest Risk Level: {risk_level}"