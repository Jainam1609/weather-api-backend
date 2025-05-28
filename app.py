from flask import Flask, request, jsonify
import requests
import json
import uuid
from datetime import datetime
from google.cloud import storage
from config import GCS_BUCKET_NAME
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
storage_client = storage.Client()

@app.route('/store-weather-data', methods=['POST'])
def store_weather_data():
    try:
        data = request.get_json()
        latitude = data.get("latitude")
        longitude = data.get("longitude")
        start_date = data.get("start_date")
        end_date = data.get("end_date")

        if not all([latitude, longitude, start_date, end_date]):
            return jsonify({"error": "Missing required fields"}), 400

        weather_api_url = (
            "https://archive-api.open-meteo.com/v1/archive?"
            f"latitude={latitude}&longitude={longitude}"
            f"&start_date={start_date}&end_date={end_date}"
            "&daily=temperature_2m_max,temperature_2m_min,temperature_2m_mean,"
            "apparent_temperature_max,apparent_temperature_min,apparent_temperature_mean"
            "&timezone=auto"
        )

        response = requests.get(weather_api_url)
        if response.status_code != 200:
            return jsonify({"error": "Failed to fetch data from Open-Meteo"}), 502

        file_name = f"weather_{latitude}_{longitude}_{start_date}_{end_date}_{uuid.uuid4().hex}.json"
        bucket = storage_client.bucket(GCS_BUCKET_NAME)
        blob = bucket.blob(file_name)
        blob.upload_from_string(json.dumps(response.json()), content_type='application/json')

        return jsonify({"message": "Weather data stored successfully", "file_name": file_name}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/list-weather-files', methods=['GET'])
def list_weather_files():
    try:
        bucket = storage_client.bucket(GCS_BUCKET_NAME)
        blobs = list(bucket.list_blobs())
        file_names = [blob.name for blob in blobs]
        return jsonify({"files": file_names}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/weather-file-content/<file_name>', methods=['GET'])
def get_weather_file(file_name):
    try:
        bucket = storage_client.bucket(GCS_BUCKET_NAME)
        blob = bucket.blob(file_name)
        if not blob.exists():
            return jsonify({"error": "File not found"}), 404
        content = json.loads(blob.download_as_text())
        return jsonify(content), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)