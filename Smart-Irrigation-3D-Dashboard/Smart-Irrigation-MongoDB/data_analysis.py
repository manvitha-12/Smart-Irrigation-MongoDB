"""Run basic analysis and save charts from the MongoDB collection."""
import pandas as pd
import matplotlib.pyplot as plt
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
client.admin.command("ping")
collection = client["SmartIrrigationDB"]["FarmData"]
df = pd.DataFrame(list(collection.find({}, {"_id": 0})))

if df.empty:
    raise SystemExit("No farm records found. Run: python database.py")

print("Total farms:", len(df))
print("Average soil moisture:", round(df["soil_moisture"].mean(), 2))
print("Average temperature:", round(df["temperature"].mean(), 2))
print("Average humidity:", round(df["humidity"].mean(), 2))
print("Average rainfall:", round(df["rainfall"].mean(), 2))
print("Total water usage:", df["water_usage"].sum(), "litres")
print("\\nIrrigation status counts:\\n", df["irrigation_status"].value_counts())

plt.figure(figsize=(9, 5))
plt.bar(df["farm_name"], df["soil_moisture"])
plt.xlabel("Farm")
plt.ylabel("Soil moisture (%)")
plt.title("Soil Moisture by Farm")
plt.xticks(rotation=30, ha="right")
plt.tight_layout()
plt.savefig("soil_moisture.png", dpi=150)
plt.show()

plt.figure(figsize=(9, 5))
plt.bar(df["farm_name"], df["water_usage"])
plt.xlabel("Farm")
plt.ylabel("Water usage (litres)")
plt.title("Water Usage by Farm")
plt.xticks(rotation=30, ha="right")
plt.tight_layout()
plt.savefig("water_usage.png", dpi=150)
plt.show()

client.close()
