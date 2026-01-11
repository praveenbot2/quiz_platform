from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from database.models import db, Patient, HealthData, Prediction
from models.health_risk_model import HealthRiskModel
from models.disease_prediction_model import DiseasePredictionModel
from models.vitals_anomaly_model import VitalsAnomalyModel
import json
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///health_monitoring.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)

# Initialize database
db.init_app(app)

# Initialize ML models
health_risk_model = HealthRiskModel()
disease_prediction_model = DiseasePredictionModel()
vitals_anomaly_model = VitalsAnomalyModel()

# Load models
try:
    health_risk_model.load()
    disease_prediction_model.load()
    vitals_anomaly_model.load()
    print("ML models loaded successfully")
except Exception as e:
    print(f"Warning: Could not load ML models: {e}")
    print("Please run train_models.py to train the models first")


@app.route('/')
def index():
    """Serve the main application page"""
    return render_template('index.html')


# Patient Management Endpoints
@app.route('/api/patients', methods=['POST'])
def create_patient():
    """Register a new patient"""
    try:
        data = request.json
        
        # Check if email already exists
        existing_patient = Patient.query.filter_by(email=data.get('email')).first()
        if existing_patient:
            return jsonify({'error': 'Patient with this email already exists'}), 400
        
        patient = Patient(
            name=data.get('name'),
            age=data.get('age'),
            gender=data.get('gender'),
            blood_group=data.get('blood_group'),
            phone=data.get('phone'),
            email=data.get('email'),
            address=data.get('address'),
            medical_history=data.get('medical_history')
        )
        
        db.session.add(patient)
        db.session.commit()
        
        return jsonify({
            'message': 'Patient registered successfully',
            'patient': patient.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/patients/<int:patient_id>', methods=['GET'])
def get_patient(patient_id):
    """Get patient details"""
    try:
        patient = Patient.query.get(patient_id)
        if not patient:
            return jsonify({'error': 'Patient not found'}), 404
        
        return jsonify(patient.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/patients', methods=['GET'])
def list_patients():
    """List all patients"""
    try:
        patients = Patient.query.all()
        return jsonify([patient.to_dict() for patient in patients]), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Health Data Endpoints
@app.route('/api/health-data', methods=['POST'])
def submit_health_data():
    """Submit health data for a patient"""
    try:
        data = request.json
        patient_id = data.get('patient_id')
        
        # Verify patient exists
        patient = Patient.query.get(patient_id)
        if not patient:
            return jsonify({'error': 'Patient not found'}), 404
        
        # Calculate BMI if height and weight provided
        bmi = None
        if data.get('height') and data.get('weight'):
            height_m = data.get('height') / 100  # Convert cm to meters
            bmi = data.get('weight') / (height_m ** 2)
        
        health_data = HealthData(
            patient_id=patient_id,
            heart_rate=data.get('heart_rate'),
            blood_pressure_systolic=data.get('blood_pressure_systolic'),
            blood_pressure_diastolic=data.get('blood_pressure_diastolic'),
            temperature=data.get('temperature'),
            oxygen_saturation=data.get('oxygen_saturation'),
            respiratory_rate=data.get('respiratory_rate'),
            blood_glucose=data.get('blood_glucose'),
            weight=data.get('weight'),
            height=data.get('height'),
            bmi=bmi,
            symptoms=data.get('symptoms'),
            notes=data.get('notes')
        )
        
        db.session.add(health_data)
        db.session.commit()
        
        return jsonify({
            'message': 'Health data submitted successfully',
            'health_data': health_data.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/health-data/<int:patient_id>', methods=['GET'])
def get_health_history(patient_id):
    """Get patient health data history"""
    try:
        patient = Patient.query.get(patient_id)
        if not patient:
            return jsonify({'error': 'Patient not found'}), 404
        
        health_records = HealthData.query.filter_by(patient_id=patient_id)\
            .order_by(HealthData.recorded_at.desc()).all()
        
        return jsonify([record.to_dict() for record in health_records]), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Prediction Endpoints
@app.route('/api/predict/health-risk', methods=['POST'])
def predict_health_risk():
    """Predict health risk based on patient data"""
    try:
        data = request.json
        patient_id = data.get('patient_id')
        
        # Verify patient exists
        patient = Patient.query.get(patient_id)
        if not patient:
            return jsonify({'error': 'Patient not found'}), 404
        
        # Prepare patient data for prediction
        patient_data = {
            'age': patient.age,
            'heart_rate': data.get('heart_rate'),
            'blood_pressure_systolic': data.get('blood_pressure_systolic'),
            'blood_pressure_diastolic': data.get('blood_pressure_diastolic'),
            'temperature': data.get('temperature'),
            'oxygen_saturation': data.get('oxygen_saturation')
        }
        
        # Make prediction
        prediction_result = health_risk_model.predict(patient_data)
        
        # Store prediction in database
        prediction = Prediction(
            patient_id=patient_id,
            prediction_type='health_risk',
            prediction_result=json.dumps({
                'risk_level': prediction_result['risk_level'],
                'risk_score': prediction_result['risk_score']
            }),
            confidence_score=prediction_result['confidence'],
            risk_level=prediction_result['risk_level'],
            recommendations='\n'.join(prediction_result['recommendations'])
        )
        
        db.session.add(prediction)
        db.session.commit()
        
        return jsonify({
            'message': 'Health risk prediction completed',
            'prediction': prediction_result
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/predict/disease', methods=['POST'])
def predict_disease():
    """Predict disease based on symptoms"""
    try:
        data = request.json
        patient_id = data.get('patient_id')
        symptoms = data.get('symptoms', [])
        
        # Verify patient exists
        patient = Patient.query.get(patient_id)
        if not patient:
            return jsonify({'error': 'Patient not found'}), 404
        
        if not symptoms:
            return jsonify({'error': 'No symptoms provided'}), 400
        
        # Make prediction
        prediction_result = disease_prediction_model.predict(symptoms)
        
        # Store prediction in database
        prediction = Prediction(
            patient_id=patient_id,
            prediction_type='disease',
            prediction_result=prediction_result['disease'],
            confidence_score=prediction_result['confidence'],
            risk_level=prediction_result['severity'],
            recommendations='\n'.join(prediction_result['recommendations'])
        )
        
        db.session.add(prediction)
        db.session.commit()
        
        return jsonify({
            'message': 'Disease prediction completed',
            'prediction': prediction_result
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/predict/vitals-anomaly', methods=['POST'])
def predict_vitals_anomaly():
    """Detect anomalies in vital signs"""
    try:
        data = request.json
        patient_id = data.get('patient_id')
        
        # Verify patient exists
        patient = Patient.query.get(patient_id)
        if not patient:
            return jsonify({'error': 'Patient not found'}), 404
        
        # Prepare vital signs data
        vital_signs = {
            'heart_rate': data.get('heart_rate'),
            'blood_pressure_systolic': data.get('blood_pressure_systolic'),
            'blood_pressure_diastolic': data.get('blood_pressure_diastolic'),
            'temperature': data.get('temperature'),
            'oxygen_saturation': data.get('oxygen_saturation'),
            'respiratory_rate': data.get('respiratory_rate')
        }
        
        # Make prediction
        prediction_result = vitals_anomaly_model.predict(vital_signs)
        
        # Store prediction if anomaly detected
        if prediction_result['is_anomaly']:
            prediction = Prediction(
                patient_id=patient_id,
                prediction_type='vitals_anomaly',
                prediction_result=json.dumps(prediction_result['detected_issues']),
                confidence_score=abs(prediction_result['anomaly_score']),
                risk_level=prediction_result['severity'],
                recommendations='Immediate medical attention recommended due to abnormal vital signs'
            )
            
            db.session.add(prediction)
            db.session.commit()
        
        return jsonify({
            'message': 'Vitals anomaly detection completed',
            'prediction': prediction_result
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# Monitoring Endpoint
@app.route('/api/monitor/<int:patient_id>', methods=['GET'])
def get_monitoring_data(patient_id):
    """Get real-time monitoring data for a patient"""
    try:
        patient = Patient.query.get(patient_id)
        if not patient:
            return jsonify({'error': 'Patient not found'}), 404
        
        # Get latest health data
        latest_health_data = HealthData.query.filter_by(patient_id=patient_id)\
            .order_by(HealthData.recorded_at.desc()).first()
        
        # Get recent predictions
        recent_predictions = Prediction.query.filter_by(patient_id=patient_id)\
            .order_by(Prediction.created_at.desc()).limit(5).all()
        
        return jsonify({
            'patient': patient.to_dict(),
            'latest_health_data': latest_health_data.to_dict() if latest_health_data else None,
            'recent_predictions': [pred.to_dict() for pred in recent_predictions]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    """API health check"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat()
    }), 200


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Database tables created successfully")
    
    print("Starting AI Health Monitoring System...")
    print("Server running at http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
