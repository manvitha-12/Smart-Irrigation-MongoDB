# Smart Irrigation & Water Usage Optimization System

A beginner-friendly MongoDB + Python + Streamlit portfolio project. It stores sample farm records in MongoDB, analyses soil moisture and water usage, and displays a dashboard with simple irrigation recommendations.

## Features
- MongoDB database: `SmartIrrigationDB`
- Collection: `FarmData`
- Load sample CSV records into MongoDB without duplicating farm IDs
- Analyse farm, crop, soil moisture, rainfall, temperature, humidity, and water usage
- Streamlit dashboard with interactive 3D Plotly charts, filters, and recommendations

## Requirements
- Windows, macOS, or Linux
- Python 3.10 or newer recommended
- MongoDB Community Server running locally at `mongodb://localhost:27017/`

MongoDB Compass is optional; it helps you view the database.

## Setup on Windows (VS Code)

1. Extract the ZIP file.
2. Open the extracted `Smart-Irrigation-MongoDB` folder in VS Code.
3. Open **Terminal → New Terminal**.
4. Create and activate a virtual environment (optional but recommended):

   ```powershell
   py -m venv .venv
   .venv\Scripts\activate
   ```

5. Install packages:

   ```powershell
   py -m pip install -r requirements.txt
   ```

6. Make sure the MongoDB Server service is running.
7. Load the sample CSV into MongoDB:

   ```powershell
   py database.py
   ```

   The script upserts records by `farm_id`, so rerunning it will update the same six records rather than creating duplicates.

8. Start the interactive 3D dashboard:

   ```powershell
   py -m streamlit run app.py
   ```

9. Streamlit will show a local address, usually `http://localhost:8501`. Open it in your browser.

## Optional: Run data analysis

```powershell
py data_analysis.py
```

This prints summary statistics and creates `soil_moisture.png` and `water_usage.png`.

## MongoDB Compass
Connect using:

```text
mongodb://localhost:27017/
```

Then open database `SmartIrrigationDB` and collection `FarmData`.

## Project structure

```text
Smart-Irrigation-MongoDB/
├── dataset/
│   └── irrigation_data.csv
├── app.py
├── database.py
├── data_analysis.py
├── irrigation_logic.py
├── requirements.txt
└── README.md
```

## Important note
The included six records are sample data. The irrigation thresholds are illustrative rules for a student project, not validated agricultural advice. A real system should calibrate recommendations using crop type, soil properties, crop growth stage, root depth, and local weather or sensor readings.
