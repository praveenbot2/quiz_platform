from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Patient(db.Model):
    """Patient model for storing patient information"""
    __tablename__ = 'patients'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    blood_group = db.Column(db.String(5))
    phone = db.Column(db.String(15))
    email = db.Column(db.String(100), unique=True)
    address = db.Column(db.Text)
    medical_history = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with health data
    health_records = db.relationship('HealthData', backref='patient', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'blood_group': self.blood_group,
            'phone': self.phone,
            'email': self.email,
            'address': self.address,
            'medical_history': self.medical_history,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class HealthData(db.Model):
    """Health data model for storing patient vital signs and health metrics"""
    __tablename__ = 'health_data'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    
    # Vital signs
    heart_rate = db.Column(db.Float)  # bpm
    blood_pressure_systolic = db.Column(db.Float)  # mmHg
    blood_pressure_diastolic = db.Column(db.Float)  # mmHg
    temperature = db.Column(db.Float)  # Celsius
    oxygen_saturation = db.Column(db.Float)  # percentage
    respiratory_rate = db.Column(db.Float)  # breaths per minute
    
    # Additional health metrics
    blood_glucose = db.Column(db.Float)  # mg/dL
    weight = db.Column(db.Float)  # kg
    height = db.Column(db.Float)  # cm
    bmi = db.Column(db.Float)
    
    # Symptoms and notes
    symptoms = db.Column(db.Text)
    notes = db.Column(db.Text)
    
    # Timestamp
    recorded_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'heart_rate': self.heart_rate,
            'blood_pressure_systolic': self.blood_pressure_systolic,
            'blood_pressure_diastolic': self.blood_pressure_diastolic,
            'temperature': self.temperature,
            'oxygen_saturation': self.oxygen_saturation,
            'respiratory_rate': self.respiratory_rate,
            'blood_glucose': self.blood_glucose,
            'weight': self.weight,
            'height': self.height,
            'bmi': self.bmi,
            'symptoms': self.symptoms,
            'notes': self.notes,
            'recorded_at': self.recorded_at.isoformat() if self.recorded_at else None
        }


class Prediction(db.Model):
    """Prediction model for storing AI predictions and assessments"""
    __tablename__ = 'predictions'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    health_data_id = db.Column(db.Integer, db.ForeignKey('health_data.id'))
    
    prediction_type = db.Column(db.String(50), nullable=False)  # health_risk, disease, anomaly
    prediction_result = db.Column(db.Text, nullable=False)
    confidence_score = db.Column(db.Float)
    risk_level = db.Column(db.String(20))  # low, medium, high, critical
    recommendations = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'health_data_id': self.health_data_id,
            'prediction_type': self.prediction_type,
            'prediction_result': self.prediction_result,
            'confidence_score': self.confidence_score,
            'risk_level': self.risk_level,
            'recommendations': self.recommendations,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
