# 🌤️ Weather Data API (Open-Meteo + GCS)

This Flask-based backend service uses the Open-Meteo Historical Weather API to fetch weather data and store it in Google Cloud Storage (GCS). It's deployed using Docker on Google Cloud Run.

## 🚀 Live URL

> [https://weather-api-881059367176.us-central1.run.app/](https://weather-api-881059367176.us-central1.run.app/)

---

## 📦 API Endpoints

---

### 1. `POST /store-weather-data`

**Purpose**: Fetch historical weather data from Open-Meteo API and store the response in GCS.

**Endpoint**:

```
POST /store-weather-data
```

**Request Body** (JSON):

```json
{
  "latitude": 35.6895,
  "longitude": 139.6917,
  "start_date": "2023-01-01",
  "end_date": "2023-01-05"
}
```

**Example `curl` Command**:

```bash
curl -X POST https://weather-api-881059367176.us-central1.run.app/store-weather-data \
  -H "Content-Type: application/json" \
  -d '{"latitude":35.6895,"longitude":139.6917,"start_date":"2023-01-01","end_date":"2023-01-05"}'
```

**Success Response** (HTTP 200):

```json
{
  "message": "Weather data stored successfully.",
  "file_name": "weather_35.6895_139.6917_2023-01-01_2023-01-05_aa13c51b239d411aa322011d4fd16b44.json"
}
```

---

### 2. `GET /list-weather-files`

**Purpose**: List all stored weather data files in GCS.

**Endpoint**:

```
GET /list-weather-files
```

**Example `curl` Command**:

```bash
curl https://weather-api-881059367176.us-central1.run.app/list-weather-files
```

**Success Response**:

```json
{
    "files": [
        "weather_35.6895_139.6917_2023-01-01_2023-01-05_6c8b6b5e127e460a8a38f42a8fd8728e.json",
        "weather_35.6895_139.6917_2023-01-01_2023-01-05_aa13c51b239d411aa322011d4fd16b44.json"
    ]
}
```

---

### 3. `GET /weather-file-content/<file_name>`

**Purpose**: Fetch the contents of a specific weather data JSON file.

**Endpoint**:

```
GET /weather-file-content/weather_35.6895_139.6917_2023-01-01_to_2023-01-05.json
```

**Example `curl` Command**:

```bash
curl https://weather-api-881059367176.us-central1.run.app/weather-file-content/weather_35.6895_139.6917_2023-01-01_2023-01-05_aa13c51b239d411aa322011d4fd16b44.json
```

**Success Response**:

```json
{
    "daily": {
        "apparent_temperature_max": [
            7.6,
            4.9,
            5.1,
            4.7,
            3.1
        ],
        "apparent_temperature_mean": [
            0.8,
            -0.7,
            -1.1,
            -1.1,
            -2.1
        ],
        "apparent_temperature_min": [
            -6.0,
            -4.1,
            -5.8,
            -4.8,
            -5.7
        ],
        "temperature_2m_max": [
            10.7,
            8.7,
            8.8,
            8.4,
            9.2
        ],
        "temperature_2m_mean": [
            4.2,
            4.1,
            3.4,
            3.4,
            3.3
        ],
        "temperature_2m_min": [
            -2.3,
            1.0,
            -1.3,
            0.2,
            0.0
        ],
        "time": [
            "2023-01-01",
            "2023-01-02",
            "2023-01-03",
            "2023-01-04",
            "2023-01-05"
        ]
    },
    "daily_units": {
        "apparent_temperature_max": "°C",
        "apparent_temperature_mean": "°C",
        "apparent_temperature_min": "°C",
        "temperature_2m_max": "°C",
        "temperature_2m_mean": "°C",
        "temperature_2m_min": "°C",
        "time": "iso8601"
    },
    "elevation": 40.0,
    "generationtime_ms": 8.362531661987305,
    "latitude": 35.676624,
    "longitude": 139.69112,
    "timezone": "Asia/Tokyo",
    "timezone_abbreviation": "GMT+9",
    "utc_offset_seconds": 32400
}
```
---

## 🛠 Setup Instructions

### 1. **Clone the repository**

```bash
git clone https://github.com/your-username/weather-api.git
cd weather-api
```

---

### 2. **Set up a virtual environment**

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

---

### 3. **Install dependencies**

```bash
pip install -r requirements.txt
```

---

### 4. **Add your Google Cloud credentials**

Download your service account key from GCP and set the environment variable:

```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/weather-api-xxxx.json"
```

For example:

```bash
export GOOGLE_APPLICATION_CREDENTIALS="/Users/jainam/Downloads/weather-api-460609-52a4f16e5d7d.json"
```

---

### 5. **Set environment variables**

Create a `.env` file or export these manually:

```bash
export GCS_BUCKET_NAME=your-gcs-bucket-name
```

---

### 6. **Run locally**

```bash
python app.py
```

Then visit: [http://localhost:5000](http://localhost:5000)