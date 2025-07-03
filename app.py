from flask import Flask, render_template, request 
import pandas as pd 
import geopandas as gpd 
import matplotlib.pyplot as plt 
from sklearn.model_selection import train_test_split 
from sklearn.preprocessing import LabelEncoder 
from sklearn.ensemble import RandomForestClassifier 
app = Flask(__name__) 
# Load dataset 
data = pd.read_csv('sample.csv') 
data.dropna(inplace=True)  # Remove missing values 
# Convert Place to numerical encoding 
label_encoder = LabelEncoder() 
data['Place_Encoded'] = label_encoder.fit_transform(data['Place']) 
# Convert PestActivity to numerical values 
risk_mapping = {'Low': 0, 'Moderate': 1, 'High': 2} 
data['PestActivity'] = data['PestActivity'].map(risk_mapping) 
# Ensure numerical values in feature columns 
numeric_cols = ['WindFlow', 'Rainfall', 'Humidity', 'Temperature'] 
for col in numeric_cols: 
    data[col] = pd.to_numeric(data[col], errors='coerce')  # Convert, set errors to NaN 
data.dropna(subset=numeric_cols, inplace=True)  # Drop rows with NaN after conversion 
# Define features and target 
X = data[['WindFlow', 'Rainfall', 'Humidity', 'Temperature', 'Place_Encoded']] 
y = data['PestActivity'] 
# Train model 
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42) 
model = RandomForestClassifier(n_estimators=100, random_state=42) 
model.fit(X_train, y_train) 
# Function to map numerical prediction to risk level 
def map_risk(value): 
    risk_levels = {0: 'Low Risk', 1: 'Moderate Risk', 2: 'High Risk'} 
    return risk_levels.get(value, 'Unknown') 
@app.route('/') 
def home(): 
    return render_template('prediction.html') 
 
@app.route('/predict', methods=['POST']) 
def predict(): 
    try: 
        wind_flow = float(request.form['wind_flow']) 
        rainfall = float(request.form['rainfall']) 
        humidity = float(request.form['humidity']) 
        temperature = float(request.form['temperature']) 
        place = request.form['place'].strip() 
 
        # Validate place 
        place_data = data[data['Place'].str.lower() == place.lower()] 
        if place_data.empty: 
            return "Error: The entered place is not in the dataset. <a href='/'>Go Back</a>" 
 
        latitude = place_data['Latitude'].values[0] 
        longitude = place_data['Longitude'].values[0] 
        place_encoded = place_data['Place_Encoded'].values[0] 
 
        # Predict risk level 
        input_data = pd.DataFrame([[wind_flow, rainfall, humidity, temperature, place_encoded]], 
        columns=['WindFlow', 'Rainfall', 'Humidity', 'Temperature', 'Place_Encoded']) 
        prediction = model.predict(input_data)[0] 
        risk_level = map_risk(prediction) 
 
        # Generate risk map 
        india_map = gpd.read_file('shapefiles/ne_110m_admin_0_countries.shp')
        india_map = india_map[india_map['ADMIN'] == 'India'] 
 
        fig, ax = plt.subplots(figsize=(8, 8)) 
        india_map.plot(ax=ax, color='white', edgecolor='black') 
 
        colors = {'Low Risk': 'green', 'Moderate Risk': 'yellow', 'High Risk': 'red'} 
        ax.scatter(longitude, latitude, color=colors[risk_level], s=200, label=risk_level, edgecolors='black', linewidth=1.5) 
        ax.legend(title="Pest Risk Level", loc="upper right") 
 
        plt.title(f"Pest Risk Prediction for {place.title()}\nRisk Level: {risk_level}") 
        plt.savefig('static/map.png') 
        plt.close() 
 
        risk_class = risk_level.lower().replace(" ", "-")  # Format risk level for styling 
 
        return render_template('result.html', place=place, risk_level=risk_level, risk_class=risk_class) 
     
    except ValueError: 
        return "Invalid input. <a href='/'>Go Back</a>" 
if __name__ == '__main__': 
    app.run(debug=True)