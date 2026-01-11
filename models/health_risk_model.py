import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

class HealthRiskModel:
    """
    Health Risk Prediction Model
    Predicts overall health risk score based on patient data and vital signs
    """
    
    def __init__(self):
        self.model = None
        self.model_path = 'models/health_risk_model.joblib'
        
    def train(self, X_train=None, y_train=None):
        """Train the health risk prediction model"""
        # If no training data provided, use synthetic data for initialization
        if X_train is None or y_train is None:
            X_train, y_train = self._generate_synthetic_data()
        
        # Create Random Forest classifier
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        
        # Train the model
        self.model.fit(X_train, y_train)
        
        # Save the model
        os.makedirs('models', exist_ok=True)
        joblib.dump(self.model, self.model_path)
        print(f"Health Risk Model trained and saved to {self.model_path}")
        
    def _generate_synthetic_data(self, n_samples=1000):
        """Generate synthetic training data for the model"""
        np.random.seed(42)
        
        # Features: age, heart_rate, bp_systolic, bp_diastolic, temperature, oxygen_saturation
        X = []
        y = []
        
        for _ in range(n_samples):
            age = np.random.randint(18, 90)
            heart_rate = np.random.normal(75, 15)
            bp_systolic = np.random.normal(120, 20)
            bp_diastolic = np.random.normal(80, 10)
            temperature = np.random.normal(37, 0.5)
            oxygen_saturation = np.random.normal(97, 2)
            
            # Calculate risk level based on thresholds
            risk_score = 0
            
            # Age factor
            if age > 60:
                risk_score += 2
            elif age > 45:
                risk_score += 1
                
            # Heart rate factor
            if heart_rate > 100 or heart_rate < 60:
                risk_score += 2
            elif heart_rate > 90 or heart_rate < 70:
                risk_score += 1
                
            # Blood pressure factor
            if bp_systolic > 140 or bp_diastolic > 90:
                risk_score += 2
            elif bp_systolic > 130 or bp_diastolic > 85:
                risk_score += 1
                
            # Temperature factor
            if temperature > 38 or temperature < 36:
                risk_score += 2
            elif temperature > 37.5 or temperature < 36.5:
                risk_score += 1
                
            # Oxygen saturation factor
            if oxygen_saturation < 92:
                risk_score += 2
            elif oxygen_saturation < 95:
                risk_score += 1
            
            # Determine risk level (0=low, 1=medium, 2=high, 3=critical)
            if risk_score >= 6:
                risk_level = 3  # critical
            elif risk_score >= 4:
                risk_level = 2  # high
            elif risk_score >= 2:
                risk_level = 1  # medium
            else:
                risk_level = 0  # low
            
            X.append([age, heart_rate, bp_systolic, bp_diastolic, temperature, oxygen_saturation])
            y.append(risk_level)
        
        return np.array(X), np.array(y)
    
    def load(self):
        """Load the trained model"""
        if os.path.exists(self.model_path):
            self.model = joblib.load(self.model_path)
            return True
        return False
    
    def predict(self, patient_data):
        """
        Predict health risk for a patient
        
        Args:
            patient_data: dict with keys: age, heart_rate, blood_pressure_systolic, 
                         blood_pressure_diastolic, temperature, oxygen_saturation
        
        Returns:
            dict with risk_level, risk_score, and recommendations
        """
        if self.model is None:
            if not self.load():
                raise Exception("Model not trained or loaded")
        
        # Prepare features
        features = np.array([[
            patient_data.get('age', 30),
            patient_data.get('heart_rate', 75),
            patient_data.get('blood_pressure_systolic', 120),
            patient_data.get('blood_pressure_diastolic', 80),
            patient_data.get('temperature', 37),
            patient_data.get('oxygen_saturation', 98)
        ]])
        
        # Make prediction
        risk_level = self.model.predict(features)[0]
        risk_proba = self.model.predict_proba(features)[0]
        
        # Map risk level to text
        risk_levels = ['low', 'medium', 'high', 'critical']
        risk_text = risk_levels[risk_level]
        
        # Calculate risk score (0-100)
        risk_score = int(risk_proba[risk_level] * 100)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(patient_data, risk_text)
        
        return {
            'risk_level': risk_text,
            'risk_score': risk_score,
            'confidence': float(risk_proba[risk_level]),
            'recommendations': recommendations
        }
    
    def _generate_recommendations(self, patient_data, risk_level):
        """Generate health recommendations based on patient data and risk level"""
        recommendations = []
        
        # Heart rate recommendations
        hr = patient_data.get('heart_rate', 75)
        if hr > 100:
            recommendations.append("High heart rate detected. Consider consulting a cardiologist.")
        elif hr < 60:
            recommendations.append("Low heart rate detected. Monitor for symptoms of bradycardia.")
        
        # Blood pressure recommendations
        bp_sys = patient_data.get('blood_pressure_systolic', 120)
        bp_dia = patient_data.get('blood_pressure_diastolic', 80)
        if bp_sys > 140 or bp_dia > 90:
            recommendations.append("High blood pressure detected. Reduce salt intake and consult a doctor.")
        elif bp_sys < 90 or bp_dia < 60:
            recommendations.append("Low blood pressure detected. Stay hydrated and monitor symptoms.")
        
        # Temperature recommendations
        temp = patient_data.get('temperature', 37)
        if temp > 38:
            recommendations.append("Fever detected. Rest, stay hydrated, and monitor temperature.")
        elif temp < 36:
            recommendations.append("Low body temperature detected. Keep warm and seek medical attention if persistent.")
        
        # Oxygen saturation recommendations
        o2 = patient_data.get('oxygen_saturation', 98)
        if o2 < 92:
            recommendations.append("Low oxygen saturation. Seek immediate medical attention.")
        elif o2 < 95:
            recommendations.append("Slightly low oxygen levels. Monitor breathing and consider seeing a doctor.")
        
        # General recommendations based on risk level
        if risk_level == 'critical':
            recommendations.append("CRITICAL: Seek immediate medical attention.")
        elif risk_level == 'high':
            recommendations.append("Schedule a doctor's appointment soon.")
        elif risk_level == 'medium':
            recommendations.append("Monitor your health closely and maintain healthy lifestyle habits.")
        else:
            recommendations.append("Continue maintaining healthy lifestyle habits.")
        
        return recommendations
