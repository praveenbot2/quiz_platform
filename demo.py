"""
Demo script showing the capabilities of the AI Health Monitoring System
Run this after starting the Flask server with: python app.py
"""
import requests
import json
import time

BASE_URL = 'http://localhost:5000/api'

def demo():
    print("\n" + "="*80)
    print(" AI HEALTH MONITORING & PREDICTION SYSTEM - LIVE DEMO")
    print("="*80)
    
    # Register a sample patient
    print("\n1️⃣  REGISTERING A NEW PATIENT")
    print("-" * 80)
    patient_data = {
        "name": "Sarah Johnson",
        "age": 52,
        "gender": "Female",
        "blood_group": "O+",
        "email": "sarah.johnson@example.com",
        "phone": "+1-555-0123",
        "address": "456 Oak Street, Springfield, IL 62701",
        "medical_history": "Type 2 Diabetes (controlled), Hypertension, Seasonal allergies"
    }
    
    response = requests.post(f'{BASE_URL}/patients', json=patient_data)
    patient = response.json()['patient']
    patient_id = patient['id']
    
    print(f"✓ Patient registered successfully!")
    print(f"  Name: {patient['name']}")
    print(f"  Age: {patient['age']} years")
    print(f"  Patient ID: {patient_id}")
    
    time.sleep(1)
    
    # Submit health vitals
    print("\n2️⃣  RECORDING PATIENT VITAL SIGNS")
    print("-" * 80)
    health_data = {
        "patient_id": patient_id,
        "heart_rate": 88,
        "blood_pressure_systolic": 145,
        "blood_pressure_diastolic": 92,
        "temperature": 37.2,
        "oxygen_saturation": 96,
        "respiratory_rate": 17,
        "blood_glucose": 142,
        "weight": 72.5,
        "height": 165,
        "symptoms": "Feeling slightly fatigued, mild headache"
    }
    
    response = requests.post(f'{BASE_URL}/health-data', json=health_data)
    print("✓ Vital signs recorded:")
    print(f"  Heart Rate: {health_data['heart_rate']} bpm")
    print(f"  Blood Pressure: {health_data['blood_pressure_systolic']}/{health_data['blood_pressure_diastolic']} mmHg")
    print(f"  Temperature: {health_data['temperature']}°C")
    print(f"  Oxygen Saturation: {health_data['oxygen_saturation']}%")
    print(f"  Blood Glucose: {health_data['blood_glucose']} mg/dL")
    
    time.sleep(1)
    
    # AI Health Risk Prediction
    print("\n3️⃣  AI HEALTH RISK PREDICTION")
    print("-" * 80)
    prediction_data = {
        "patient_id": patient_id,
        "heart_rate": health_data['heart_rate'],
        "blood_pressure_systolic": health_data['blood_pressure_systolic'],
        "blood_pressure_diastolic": health_data['blood_pressure_diastolic'],
        "temperature": health_data['temperature'],
        "oxygen_saturation": health_data['oxygen_saturation']
    }
    
    response = requests.post(f'{BASE_URL}/predict/health-risk', json=prediction_data)
    risk_prediction = response.json()['prediction']
    
    print(f"✓ Health Risk Analysis Complete:")
    print(f"  Risk Level: {risk_prediction['risk_level'].upper()}")
    print(f"  Risk Score: {risk_prediction['risk_score']}/100")
    print(f"  Confidence: {risk_prediction['confidence']*100:.1f}%")
    print(f"\n  AI Recommendations:")
    for i, rec in enumerate(risk_prediction['recommendations'], 1):
        print(f"    {i}. {rec}")
    
    time.sleep(1)
    
    # Vital Signs Anomaly Detection
    print("\n4️⃣  VITAL SIGNS ANOMALY DETECTION")
    print("-" * 80)
    vitals_data = {
        "patient_id": patient_id,
        "heart_rate": health_data['heart_rate'],
        "blood_pressure_systolic": health_data['blood_pressure_systolic'],
        "blood_pressure_diastolic": health_data['blood_pressure_diastolic'],
        "temperature": health_data['temperature'],
        "oxygen_saturation": health_data['oxygen_saturation'],
        "respiratory_rate": health_data['respiratory_rate']
    }
    
    response = requests.post(f'{BASE_URL}/predict/vitals-anomaly', json=vitals_data)
    anomaly_result = response.json()['prediction']
    
    print(f"✓ Anomaly Detection Results:")
    print(f"  Anomaly Detected: {'Yes ⚠️' if anomaly_result['is_anomaly'] else 'No ✓'}")
    print(f"  Severity: {anomaly_result['severity'].upper()}")
    
    if anomaly_result['detected_issues']:
        print(f"\n  Detected Issues:")
        for issue in anomaly_result['detected_issues']:
            print(f"    • {issue['vital'].replace('_', ' ').title()}: {issue['issue']}")
            print(f"      Value: {issue['value']} (Normal: {issue['normal_range']})")
            print(f"      Severity: {issue['severity']}")
    
    time.sleep(1)
    
    # Disease Prediction from Symptoms
    print("\n5️⃣  DISEASE PREDICTION FROM SYMPTOMS")
    print("-" * 80)
    # Simulate a different symptom pattern
    symptoms = ['fever', 'cough', 'fatigue', 'headache', 'body_ache']
    
    response = requests.post(f'{BASE_URL}/predict/disease', 
                            json={"patient_id": patient_id, "symptoms": symptoms})
    disease_prediction = response.json()['prediction']
    
    print(f"  Reported Symptoms: {', '.join([s.replace('_', ' ').title() for s in symptoms])}")
    print(f"\n✓ Disease Prediction Results:")
    print(f"  Predicted Disease: {disease_prediction['disease']}")
    print(f"  Confidence: {disease_prediction['confidence']*100:.1f}%")
    print(f"  Severity: {disease_prediction['severity'].upper()}")
    print(f"\n  Medical Recommendations:")
    for i, rec in enumerate(disease_prediction['recommendations'][:5], 1):
        print(f"    {i}. {rec}")
    
    time.sleep(1)
    
    # Real-time Monitoring Dashboard
    print("\n6️⃣  REAL-TIME PATIENT MONITORING")
    print("-" * 80)
    response = requests.get(f'{BASE_URL}/monitor/{patient_id}')
    monitor_data = response.json()
    
    print(f"✓ Monitoring Dashboard for {monitor_data['patient']['name']}")
    print(f"  Latest Reading: {monitor_data['latest_health_data']['recorded_at']}")
    print(f"  Recent Predictions: {len(monitor_data['recent_predictions'])} assessments")
    
    print("\n" + "="*80)
    print(" DEMO COMPLETED SUCCESSFULLY! 🎉")
    print("="*80)
    print("\nThe AI Health Monitoring System has demonstrated:")
    print("  ✓ Patient registration and management")
    print("  ✓ Vital signs recording and tracking")
    print("  ✓ AI-powered health risk assessment")
    print("  ✓ Real-time anomaly detection in vital signs")
    print("  ✓ Disease prediction from symptoms")
    print("  ✓ Real-time patient monitoring dashboard")
    print("\nAccess the web interface at: http://localhost:5000")
    print("="*80 + "\n")

if __name__ == '__main__':
    try:
        # Check if server is running
        response = requests.get(f'{BASE_URL}/health', timeout=2)
        if response.status_code == 200:
            demo()
        else:
            print("Server is not responding correctly. Please check the server.")
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to the Flask server")
        print("\nPlease start the server first by running:")
        print("  python app.py")
        print("\nThen run this demo script in a new terminal.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
