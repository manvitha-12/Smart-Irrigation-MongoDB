"""Load the sample CSV records into the local MongoDB database."""
from pathlib import Path
import pandas as pd
from pymongo import MongoClient, UpdateOne
from pymongo.errors import ServerSelectionTimeoutError

MONGO_URI = "mongodb://localhost:27017/"
DATABASE_NAME = "SmartIrrigationDB"
COLLECTION_NAME = "FarmData"

def main():
    csv_path = Path(__file__).parent / "dataset" / "irrigation_data.csv"
    df = pd.read_csv(csv_path)
    records = df.to_dict(orient="records")

    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        client.admin.command("ping")
        collection = client[DATABASE_NAME][COLLECTION_NAME]

        # Upsert by farm_id so running this script repeatedly won't create duplicates.
        operations = [
            UpdateOne({"farm_id": record["farm_id"]},
                      {"$set": record},
                      upsert=True)
            for record in records
        ]
        if operations:
            result = collection.bulk_write(operations)
        print(f"MongoDB connected: {DATABASE_NAME}.{COLLECTION_NAME}")
        print(f"CSV records processed: {len(records)}")
        print(f"Inserted: {result.upserted_count}; updated: {result.modified_count}")
        print(f"Total documents in collection: {collection.count_documents({})}")
        client.close()
    except ServerSelectionTimeoutError:
        print("Could not connect to MongoDB at mongodb://localhost:27017/")
        print("Start the MongoDB Server service, then run this script again.")

if __name__ == "__main__":
    main()
