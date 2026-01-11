import numpy as np
from sklearn.ensemble import IsolationForest
import joblib
import os

class VitalsAnomalyModel:
    """
    Vital Signs Anomaly Detection Model
    Detects abnormal patterns in patient vital signs using Isolation Forest
    """
    
    def __init__(self):
        self.model = None
        self.model_path = 'models/vitals_anomaly_model.joblib'
        
    def train(self, X_train=None):
        """Train the anomaly detection model"""
        if X_train is None:
            X_train = self._generate_synthetic_data()
        
        # Isolation Forest for anomaly detection
        self.model = IsolationForest(
            contamination=0.1,  # Assume 10% of data are anomalies
            random_state=42,
            n_estimators=100
        )
        
        self.model.fit(X_train)
        
        os.makedirs('models', exist_ok=True)
        joblib.dump(self.model, self.model_path)
        print(f"Vitals Anomaly Model trained and saved to {self.model_path}")
        
    def _generate_synthetic_data(self, n_samples=1000):
        """Generate synthetic normal vital signs data"""
        np.random.seed(42)
        
        X = []
        
        for _ in range(n_samples):
            # Generate normal vital signs with some variation
            heart_rate = np.random.normal(75, 10)  # Normal: 60-100 bpm
            bp_systolic = np.random.normal(120, 10)  # Normal: 90-140 mmHg
            bp_diastolic = np.random.normal(80, 8)  # Normal: 60-90 mmHg
            temperature = np.random.normal(37, 0.3)  # Normal: 36.5-37.5 C
            oxygen_saturation = np.random.normal(98, 1)  # Normal: 95-100%
            respiratory_rate = np.random.normal(16, 2)  # Normal: 12-20 breaths/min
            
            X.append([
                heart_rate, bp_systolic, bp_diastolic,
                temperature, oxygen_saturation, respiratory_rate
            ])
        
        return np.array(X)
    
    def load(self):
        """Load the trained model"""
        if os.path.exists(self.model_path):
            self.model = joblib.load(self.model_path)
            return True
        return False
    
    def predict(self, vital_signs):
        """
        Detect anomalies in vital signs
        
        Args:
            vital_signs: dict with keys: heart_rate, blood_pressure_systolic,
                        blood_pressure_diastolic, temperature, oxygen_saturation,
                        respiratory_rate
        
        Returns:
            dict with is_anomaly, anomaly_score, and detected_issues
        """
        if self.model is None:
            if not self.load():
                raise Exception("Model not trained or loaded")
        
        # Prepare features
        features = np.array([[
            vital_signs.get('heart_rate', 75),
            vital_signs.get('blood_pressure_systolic', 120),
            vital_signs.get('blood_pressure_diastolic', 80),
            vital_signs.get('temperature', 37),
            vital_signs.get('oxygen_saturation', 98),
            vital_signs.get('respiratory_rate', 16)
        ]])
        
        # Predict anomaly (-1 for anomaly, 1 for normal)
        prediction = self.model.predict(features)[0]
        
        # Get anomaly score (lower scores indicate anomalies)
        anomaly_score = self.model.score_samples(features)[0]
        
        is_anomaly = prediction == -1
        
        # Detect specific issues
        detected_issues = self._detect_specific_issues(vital_signs)
        
        return {
            'is_anomaly': bool(is_anomaly),
            'anomaly_score': float(anomaly_score),
            'detected_issues': detected_issues,
            'severity': self._assess_anomaly_severity(detected_issues)
        }
    
    def _detect_specific_issues(self, vital_signs):
        """Detect specific issues with individual vital signs"""
        issues = []
        
        # Heart rate
        hr = vital_signs.get('heart_rate', 75)
        if hr > 120:
            issues.append({
                'vital': 'heart_rate',
                'issue': 'Severe Tachycardia',
                'value': hr,
                'normal_range': '60-100 bpm',
                'severity': 'critical'
            })
        elif hr > 100:
            issues.append({
                'vital': 'heart_rate',
                'issue': 'Tachycardia',
                'value': hr,
                'normal_range': '60-100 bpm',
                'severity': 'high'
            })
        elif hr < 50:
            issues.append({
                'vital': 'heart_rate',
                'issue': 'Severe Bradycardia',
                'value': hr,
                'normal_range': '60-100 bpm',
                'severity': 'critical'
            })
        elif hr < 60:
            issues.append({
                'vital': 'heart_rate',
                'issue': 'Bradycardia',
                'value': hr,
                'normal_range': '60-100 bpm',
                'severity': 'medium'
            })
        
        # Blood pressure
        bp_sys = vital_signs.get('blood_pressure_systolic', 120)
        bp_dia = vital_signs.get('blood_pressure_diastolic', 80)
        
        if bp_sys >= 180 or bp_dia >= 120:
            issues.append({
                'vital': 'blood_pressure',
                'issue': 'Hypertensive Crisis',
                'value': f'{bp_sys}/{bp_dia}',
                'normal_range': '90-140/60-90 mmHg',
                'severity': 'critical'
            })
        elif bp_sys >= 140 or bp_dia >= 90:
            issues.append({
                'vital': 'blood_pressure',
                'issue': 'Hypertension',
                'value': f'{bp_sys}/{bp_dia}',
                'normal_range': '90-140/60-90 mmHg',
                'severity': 'high'
            })
        elif bp_sys < 90 or bp_dia < 60:
            issues.append({
                'vital': 'blood_pressure',
                'issue': 'Hypotension',
                'value': f'{bp_sys}/{bp_dia}',
                'normal_range': '90-140/60-90 mmHg',
                'severity': 'high'
            })
        
        # Temperature
        temp = vital_signs.get('temperature', 37)
        if temp >= 39.5:
            issues.append({
                'vital': 'temperature',
                'issue': 'High Fever',
                'value': temp,
                'normal_range': '36.5-37.5°C',
                'severity': 'critical'
            })
        elif temp >= 38:
            issues.append({
                'vital': 'temperature',
                'issue': 'Fever',
                'value': temp,
                'normal_range': '36.5-37.5°C',
                'severity': 'high'
            })
        elif temp < 35:
            issues.append({
                'vital': 'temperature',
                'issue': 'Hypothermia',
                'value': temp,
                'normal_range': '36.5-37.5°C',
                'severity': 'critical'
            })
        elif temp < 36:
            issues.append({
                'vital': 'temperature',
                'issue': 'Low Temperature',
                'value': temp,
                'normal_range': '36.5-37.5°C',
                'severity': 'medium'
            })
        
        # Oxygen saturation
        o2 = vital_signs.get('oxygen_saturation', 98)
        if o2 < 90:
            issues.append({
                'vital': 'oxygen_saturation',
                'issue': 'Critical Hypoxemia',
                'value': o2,
                'normal_range': '95-100%',
                'severity': 'critical'
            })
        elif o2 < 95:
            issues.append({
                'vital': 'oxygen_saturation',
                'issue': 'Hypoxemia',
                'value': o2,
                'normal_range': '95-100%',
                'severity': 'high'
            })
        
        # Respiratory rate
        rr = vital_signs.get('respiratory_rate', 16)
        if rr > 25:
            issues.append({
                'vital': 'respiratory_rate',
                'issue': 'Tachypnea',
                'value': rr,
                'normal_range': '12-20 breaths/min',
                'severity': 'high'
            })
        elif rr < 10:
            issues.append({
                'vital': 'respiratory_rate',
                'issue': 'Bradypnea',
                'value': rr,
                'normal_range': '12-20 breaths/min',
                'severity': 'high'
            })
        
        return issues
    
    def _assess_anomaly_severity(self, detected_issues):
        """Assess overall severity based on detected issues"""
        if not detected_issues:
            return 'normal'
        
        severities = [issue['severity'] for issue in detected_issues]
        
        if 'critical' in severities:
            return 'critical'
        elif 'high' in severities:
            return 'high'
        elif 'medium' in severities:
            return 'medium'
        else:
            return 'low'
