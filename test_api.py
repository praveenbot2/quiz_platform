"""
Test script to verify the health monitoring system API
"""
import requests
import json
import time

BASE_URL = 'http://localhost:5000/api'

def print_response(title, response):
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_api():
    print("Testing AI Health Monitoring System API")
    print("="*60)
    
    # Test 1: Health Check
    print("\n1. Testing health check endpoint...")
    response = requests.get(f'{BASE_URL}/health')
    print_response("Health Check", response)
    
    # Test 2: Register a patient
    print("\n2. Testing patient registration...")
    patient_data = {
        "name": "John Doe",
        "age": 45,
        "gender": "Male",
        "blood_group": "A+",
        "email": "john.doe@example.com",
        "phone": "1234567890",
        "address": "123 Main St, City",
        "medical_history": "Diabetes, Hypertension"
    }
    response = requests.post(f'{BASE_URL}/patients', json=patient_data)
    print_response("Patient Registration", response)
    
    if response.status_code == 201:
        patient_id = response.json()['patient']['id']
        print(f"\n✓ Patient registered with ID: {patient_id}")
        
        # Test 3: Submit health data
        print("\n3. Testing health data submission...")
        health_data = {
            "patient_id": patient_id,
            "heart_rate": 85,
            "blood_pressure_systolic": 140,
            "blood_pressure_diastolic": 90,
            "temperature": 37.5,
            "oxygen_saturation": 96,
            "respiratory_rate": 18,
            "weight": 80,
            "height": 175,
            "symptoms": "Feeling tired, slight headache"
        }
        response = requests.post(f'{BASE_URL}/health-data', json=health_data)
        print_response("Health Data Submission", response)
        
        # Test 4: Health Risk Prediction
        print("\n4. Testing health risk prediction...")
        prediction_data = {
            "patient_id": patient_id,
            "heart_rate": 85,
            "blood_pressure_systolic": 140,
            "blood_pressure_diastolic": 90,
            "temperature": 37.5,
            "oxygen_saturation": 96
        }
        response = requests.post(f'{BASE_URL}/predict/health-risk', json=prediction_data)
        print_response("Health Risk Prediction", response)
        
        # Test 5: Disease Prediction
        print("\n5. Testing disease prediction...")
        symptoms_data = {
            "patient_id": patient_id,
            "symptoms": ["fever", "cough", "fatigue", "difficulty_breathing"]
        }
        response = requests.post(f'{BASE_URL}/predict/disease', json=symptoms_data)
        print_response("Disease Prediction", response)
        
        # Test 6: Vitals Anomaly Detection
        print("\n6. Testing vitals anomaly detection...")
        vitals_data = {
            "patient_id": patient_id,
            "heart_rate": 120,
            "blood_pressure_systolic": 160,
            "blood_pressure_diastolic": 100,
            "temperature": 38.5,
            "oxygen_saturation": 93,
            "respiratory_rate": 24
        }
        response = requests.post(f'{BASE_URL}/predict/vitals-anomaly', json=vitals_data)
        print_response("Vitals Anomaly Detection", response)
        
        # Test 7: Get Patient Info
        print("\n7. Testing get patient info...")
        response = requests.get(f'{BASE_URL}/patients/{patient_id}')
        print_response("Get Patient Info", response)
        
        # Test 8: Get Health History
        print("\n8. Testing get health history...")
        response = requests.get(f'{BASE_URL}/health-data/{patient_id}')
        print_response("Get Health History", response)
        
        # Test 9: Monitoring Data
        print("\n9. Testing monitoring data...")
        response = requests.get(f'{BASE_URL}/monitor/{patient_id}')
        print_response("Monitoring Data", response)
        
        # Test 10: List All Patients
        print("\n10. Testing list all patients...")
        response = requests.get(f'{BASE_URL}/patients')
        print_response("List All Patients", response)
        
    print("\n" + "="*60)
    print("API Testing Complete!")
    print("="*60)

if __name__ == '__main__':
    # Wait for server to start
    time.sleep(2)
    
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server.")
        print("Please make sure the Flask server is running on http://localhost:5000")
    except Exception as e:
        print(f"Error during testing: {e}")
