"""
Simple test to verify ML models work correctly
"""
import sys
sys.path.append('.')

from models.health_risk_model import HealthRiskModel
from models.disease_prediction_model import DiseasePredictionModel
from models.vitals_anomaly_model import VitalsAnomalyModel

def test_health_risk_model():
    print("\n" + "="*60)
    print("Testing Health Risk Prediction Model")
    print("="*60)
    
    model = HealthRiskModel()
    model.load()
    
    # Test case 1: Normal vitals
    patient_data = {
        'age': 30,
        'heart_rate': 75,
        'blood_pressure_systolic': 120,
        'blood_pressure_diastolic': 80,
        'temperature': 37.0,
        'oxygen_saturation': 98
    }
    
    result = model.predict(patient_data)
    print(f"\nTest 1 - Normal vitals:")
    print(f"  Age: {patient_data['age']}")
    print(f"  Heart Rate: {patient_data['heart_rate']} bpm")
    print(f"  Blood Pressure: {patient_data['blood_pressure_systolic']}/{patient_data['blood_pressure_diastolic']} mmHg")
    print(f"  Temperature: {patient_data['temperature']}°C")
    print(f"  Oxygen Saturation: {patient_data['oxygen_saturation']}%")
    print(f"\nResult:")
    print(f"  Risk Level: {result['risk_level'].upper()}")
    print(f"  Risk Score: {result['risk_score']}")
    print(f"  Recommendations:")
    for rec in result['recommendations']:
        print(f"    - {rec}")
    
    # Test case 2: High risk vitals
    patient_data = {
        'age': 65,
        'heart_rate': 110,
        'blood_pressure_systolic': 160,
        'blood_pressure_diastolic': 100,
        'temperature': 38.5,
        'oxygen_saturation': 92
    }
    
    result = model.predict(patient_data)
    print(f"\nTest 2 - High risk vitals:")
    print(f"  Age: {patient_data['age']}")
    print(f"  Heart Rate: {patient_data['heart_rate']} bpm")
    print(f"  Blood Pressure: {patient_data['blood_pressure_systolic']}/{patient_data['blood_pressure_diastolic']} mmHg")
    print(f"  Temperature: {patient_data['temperature']}°C")
    print(f"  Oxygen Saturation: {patient_data['oxygen_saturation']}%")
    print(f"\nResult:")
    print(f"  Risk Level: {result['risk_level'].upper()}")
    print(f"  Risk Score: {result['risk_score']}")
    print(f"  Recommendations:")
    for rec in result['recommendations']:
        print(f"    - {rec}")

def test_disease_prediction_model():
    print("\n" + "="*60)
    print("Testing Disease Prediction Model")
    print("="*60)
    
    model = DiseasePredictionModel()
    model.load()
    
    # Test case 1: Common cold symptoms
    symptoms = ['fever', 'cough', 'sore_throat', 'runny_nose']
    result = model.predict(symptoms)
    print(f"\nTest 1 - Symptoms: {', '.join(symptoms)}")
    print(f"Result:")
    print(f"  Predicted Disease: {result['disease']}")
    print(f"  Confidence: {result['confidence']*100:.1f}%")
    print(f"  Severity: {result['severity']}")
    print(f"  Recommendations:")
    for rec in result['recommendations'][:3]:  # Show first 3 recommendations
        print(f"    - {rec}")
    
    # Test case 2: COVID-19 symptoms
    symptoms = ['fever', 'cough', 'fatigue', 'difficulty_breathing', 'loss_of_taste', 'loss_of_smell']
    result = model.predict(symptoms)
    print(f"\nTest 2 - Symptoms: {', '.join(symptoms)}")
    print(f"Result:")
    print(f"  Predicted Disease: {result['disease']}")
    print(f"  Confidence: {result['confidence']*100:.1f}%")
    print(f"  Severity: {result['severity']}")
    print(f"  Recommendations:")
    for rec in result['recommendations'][:3]:
        print(f"    - {rec}")

def test_vitals_anomaly_model():
    print("\n" + "="*60)
    print("Testing Vitals Anomaly Detection Model")
    print("="*60)
    
    model = VitalsAnomalyModel()
    model.load()
    
    # Test case 1: Normal vitals
    vitals = {
        'heart_rate': 75,
        'blood_pressure_systolic': 120,
        'blood_pressure_diastolic': 80,
        'temperature': 37.0,
        'oxygen_saturation': 98,
        'respiratory_rate': 16
    }
    
    result = model.predict(vitals)
    print(f"\nTest 1 - Normal vitals:")
    print(f"  Heart Rate: {vitals['heart_rate']} bpm")
    print(f"  Blood Pressure: {vitals['blood_pressure_systolic']}/{vitals['blood_pressure_diastolic']} mmHg")
    print(f"  Temperature: {vitals['temperature']}°C")
    print(f"  Oxygen Saturation: {vitals['oxygen_saturation']}%")
    print(f"  Respiratory Rate: {vitals['respiratory_rate']} breaths/min")
    print(f"\nResult:")
    print(f"  Anomaly Detected: {result['is_anomaly']}")
    print(f"  Severity: {result['severity']}")
    
    # Test case 2: Abnormal vitals
    vitals = {
        'heart_rate': 130,
        'blood_pressure_systolic': 180,
        'blood_pressure_diastolic': 110,
        'temperature': 39.5,
        'oxygen_saturation': 88,
        'respiratory_rate': 28
    }
    
    result = model.predict(vitals)
    print(f"\nTest 2 - Abnormal vitals:")
    print(f"  Heart Rate: {vitals['heart_rate']} bpm")
    print(f"  Blood Pressure: {vitals['blood_pressure_systolic']}/{vitals['blood_pressure_diastolic']} mmHg")
    print(f"  Temperature: {vitals['temperature']}°C")
    print(f"  Oxygen Saturation: {vitals['oxygen_saturation']}%")
    print(f"  Respiratory Rate: {vitals['respiratory_rate']} breaths/min")
    print(f"\nResult:")
    print(f"  Anomaly Detected: {result['is_anomaly']}")
    print(f"  Severity: {result['severity']}")
    print(f"  Detected Issues:")
    for issue in result['detected_issues']:
        print(f"    - {issue['vital']}: {issue['issue']} (Value: {issue['value']}, Normal: {issue['normal_range']})")

if __name__ == '__main__':
    print("\n" + "="*60)
    print("AI Health Monitoring System - ML Models Test")
    print("="*60)
    
    try:
        test_health_risk_model()
        test_disease_prediction_model()
        test_vitals_anomaly_model()
        
        print("\n" + "="*60)
        print("✓ All ML model tests completed successfully!")
        print("="*60)
        
    except Exception as e:
        print(f"\n✗ Error during testing: {e}")
        import traceback
        traceback.print_exc()
