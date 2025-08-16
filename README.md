 🐛 Fall Armyworm Pest Prediction

A machine learning project that predicts the risk zones of **Fall Armyworm infestations** using geospatial data. The system leverages ML models to analyze latitude/longitude-based datasets and generates **risk visualizations on maps**, helping farmers and policymakers in proactive pest management.

---

📖 Project Overview

This project uses:
- A trained ML model (`pest_risk_model.pkl`)
- A Flask web app (`app.py`)  
to process location-based input and provide **real-time pest risk predictions** with map visualizations.

Supporting files include:
- `model_train.py`: Train and update ML model  
- `sample.csv`: Example dataset for predictions  
- `templates/`, `static/`: Flask front-end assets  
- `shapefiles/`: Geospatial map data  

---

⚙️ Requirements


Flask
pandas
scikit-learn
numpy
matplotlib
geopandas

````

Install dependencies with:
```bash
pip install -r requirements.txt
````

---

🚀 How to Run

1. **Clone the repo**

   ```bash
   git clone https://github.com/adithya-bheema/FallArmy-Worm-Pest-Prediction.git
   cd FallArmy-Worm-Pest-Prediction
   ```

2. **Set up virtual environment (optional but recommended)**

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **(Optional) Train the model**

   ```bash
   python model_train.py
   ```

5. **Run the Flask application**

   ```bash
   python app.py
   ```

   Open your browser at 👉 [http://localhost:5000](http://localhost:5000)



🖼️ Screenshots

🔹 Home Page

![Home Page](screenshots/home.png)

🔹 Upload CSV & Prediction

![Prediction Page](screenshots/predict.png)

🔹 Risk Map Visualization

![Risk Map](screenshots/map.png)


---


🎯 Future Enhancements

* 🌍 Integrate real-time weather/satellite data
* 📡 Deploy REST API for automated queries
* 📱 Mobile-friendly dashboard
* 🗣️ Multi-language support

---

👨‍💻 Author

**Adithya Bheema**
AI/ML Enthusiast | Software Engineer
[LinkedIn](https://linkedin.com/in/your-profile) | [GitHub](https://github.com/adithya-bheema)
