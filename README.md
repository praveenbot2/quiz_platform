# AI Based Health Monitoring and Prediction System

A real-time health monitoring and prediction system powered by artificial intelligence that helps track patient health metrics and predict potential health risks.

## Features

- **Patient Health Monitoring**: Track vital signs including heart rate, blood pressure, temperature, and oxygen levels
- **AI-Powered Predictions**: Machine learning models predict health risks and potential diseases
- **Real-Time Monitoring**: Live dashboard for monitoring patient vitals
- **Disease Prediction**: Symptom-based disease prediction using ML algorithms
- **Health Risk Assessment**: Comprehensive risk analysis based on patient data
- **Alert System**: Automatic alerts for critical health conditions

## Technology Stack

- **Backend**: Python Flask
- **Machine Learning**: scikit-learn, pandas, numpy
- **Database**: SQLite (SQLAlchemy ORM)
- **Frontend**: HTML, CSS, JavaScript
- **API**: RESTful API with CORS support

## Installation

1. Clone the repository:
```bash
git clone https://github.com/praveenbot2/quiz_platform.git
cd quiz_platform
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize the database:
```bash
python init_db.py
```

5. Train the ML models:
```bash
python train_models.py
```

## Usage

1. Start the Flask server:
```bash
python app.py
```

2. Open your browser and navigate to:
```
http://localhost:5000
```

3. Use the web interface to:
   - Register patients
   - Input health data
   - View predictions and risk assessments
   - Monitor real-time health metrics

## API Endpoints

### Patient Management
- `POST /api/patients` - Register a new patient
- `GET /api/patients/<id>` - Get patient details
- `GET /api/patients` - List all patients

### Health Data
- `POST /api/health-data` - Submit health data
- `GET /api/health-data/<patient_id>` - Get patient health history

### Predictions
- `POST /api/predict/health-risk` - Predict health risk score
- `POST /api/predict/disease` - Predict disease from symptoms
- `POST /api/predict/vitals-anomaly` - Detect anomalies in vital signs

### Monitoring
- `GET /api/monitor/<patient_id>` - Get real-time monitoring data

## Project Structure

```
quiz_platform/
├── app.py                 # Main Flask application
├── models/               # ML model files
│   ├── health_risk_model.py
│   ├── disease_prediction_model.py
│   └── vitals_anomaly_model.py
├── database/            # Database models
│   └── models.py
├── static/              # Frontend static files
│   ├── css/
│   ├── js/
│   └── index.html
├── utils/               # Utility functions
│   └── helpers.py
├── train_models.py      # Model training script
├── init_db.py          # Database initialization
├── requirements.txt     # Python dependencies
└── README.md           # Documentation
```

## ML Models

### 1. Health Risk Prediction Model
- Uses patient demographics and vital signs
- Predicts overall health risk score (0-100)
- Based on Random Forest classifier

### 2. Disease Prediction Model
- Takes symptoms as input
- Predicts potential diseases
- Uses Decision Tree classifier

### 3. Vital Signs Anomaly Detection
- Monitors real-time vital signs
- Detects abnormal patterns
- Uses Isolation Forest algorithm

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Author

Praveen Kumar

## Support

For issues and questions, please open an issue on GitHub.
