# AI Health Monitoring System - Quick Start Guide

## Overview
This system provides real-time health monitoring and AI-powered predictions for patient care.

## Setup Instructions

### 1. Installation
```bash
# Clone the repository
git clone https://github.com/praveenbot2/quiz_platform.git
cd quiz_platform

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Initialize Database
```bash
python init_db.py
```

### 3. Train ML Models
```bash
python train_models.py
```

### 4. Start the Application
```bash
python app.py
```

The application will be available at: `http://localhost:5000`

## Features

### 1. Patient Registration
- Register new patients with demographic information
- Store medical history and contact details
- Blood group tracking

### 2. Vital Signs Monitoring
Record comprehensive health metrics:
- Heart Rate (bpm)
- Blood Pressure (systolic/diastolic)
- Body Temperature (°C)
- Oxygen Saturation (%)
- Respiratory Rate (breaths/min)
- Blood Glucose (mg/dL)
- Weight and Height (BMI calculated automatically)

### 3. AI Health Risk Prediction
The system analyzes patient data and predicts:
- Overall health risk level (Low, Medium, High, Critical)
- Risk score (0-100)
- Personalized health recommendations
- Early warning alerts

### 4. Disease Prediction
Based on symptoms, the AI predicts potential diseases:
- COVID-19
- Influenza
- Common Cold
- Pneumonia
- Gastroenteritis
- Migraine
- Bronchitis
- Allergic Reactions

### 5. Vital Signs Anomaly Detection
Real-time detection of abnormal vital signs:
- Tachycardia/Bradycardia
- Hypertension/Hypotension
- Fever/Hypothermia
- Hypoxemia
- Tachypnea/Bradypnea

### 6. Real-Time Monitoring Dashboard
- View latest vital signs
- Track prediction history
- Monitor patient health trends
- Access comprehensive health records

## API Endpoints

### Patient Management
```
POST   /api/patients              # Register new patient
GET    /api/patients              # List all patients
GET    /api/patients/<id>         # Get patient details
```

### Health Data
```
POST   /api/health-data           # Submit health data
GET    /api/health-data/<patient_id>  # Get health history
```

### AI Predictions
```
POST   /api/predict/health-risk   # Predict health risk
POST   /api/predict/disease       # Predict disease from symptoms
POST   /api/predict/vitals-anomaly # Detect vital sign anomalies
```

### Monitoring
```
GET    /api/monitor/<patient_id>  # Get monitoring data
GET    /api/health                # API health check
```

## Testing

### Test ML Models
```bash
python test_models.py
```

### Run Demo
```bash
# Start the server first
python app.py

# In another terminal
python demo.py
```

## Web Interface Usage

### Step 1: Register a Patient
1. Open http://localhost:5000
2. Fill in patient information
3. Click "Register Patient"

### Step 2: Record Vital Signs
1. Go to "Record Vitals" tab
2. Select the patient
3. Enter vital signs data
4. Click "Record Vitals" or "Analyze & Predict Risk"

### Step 3: Check Symptoms
1. Go to "Check Symptoms" tab
2. Select the patient
3. Check applicable symptoms
4. Click "Predict Disease"

### Step 4: Monitor Patient
1. Go to "Monitor Patient" tab
2. Select patient from dropdown
3. View real-time dashboard with latest vitals and predictions

## ML Models

### 1. Health Risk Model
- **Algorithm**: Random Forest Classifier
- **Features**: Age, heart rate, blood pressure, temperature, oxygen saturation
- **Output**: Risk level (0-3) and recommendations

### 2. Disease Prediction Model
- **Algorithm**: Decision Tree Classifier
- **Features**: 18 symptom categories
- **Output**: Disease name, confidence score, severity level

### 3. Vitals Anomaly Model
- **Algorithm**: Isolation Forest
- **Features**: 6 vital signs
- **Output**: Anomaly detection, specific issues, severity

## Example Use Cases

### Scenario 1: Routine Health Checkup
1. Register patient
2. Record normal vital signs
3. Get low-risk assessment
4. Receive preventive health tips

### Scenario 2: Emergency Assessment
1. Patient with abnormal vitals
2. System detects critical anomalies
3. Provides immediate recommendations
4. Alerts for medical attention

### Scenario 3: Disease Diagnosis
1. Patient reports symptoms
2. AI predicts possible disease
3. Provides severity assessment
4. Recommends treatment steps

## Troubleshooting

### Models not loading?
```bash
python train_models.py
```

### Database issues?
```bash
python init_db.py
```

### Port already in use?
Modify the port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

## Security Notes

- This is a demonstration system
- Do not use for actual medical diagnosis
- Consult healthcare professionals for real medical advice
- Protect patient data appropriately in production

## Support

For issues and questions:
- Open an issue on GitHub
- Check existing documentation
- Review API examples

## License

This project is open source under the MIT License.
