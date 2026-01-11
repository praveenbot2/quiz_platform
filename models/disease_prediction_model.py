import numpy as np
from sklearn.tree import DecisionTreeClassifier
import joblib
import os

class DiseasePredictionModel:
    """
    Disease Prediction Model
    Predicts potential diseases based on symptoms
    """
    
    def __init__(self):
        self.model = None
        self.model_path = 'models/disease_prediction_model.joblib'
        self.symptom_map = {
            'fever': 0, 'cough': 1, 'fatigue': 2, 'difficulty_breathing': 3,
            'headache': 4, 'sore_throat': 5, 'body_ache': 6, 'nausea': 7,
            'vomiting': 8, 'diarrhea': 9, 'chest_pain': 10, 'dizziness': 11,
            'loss_of_taste': 12, 'loss_of_smell': 13, 'runny_nose': 14,
            'rash': 15, 'abdominal_pain': 16, 'chills': 17
        }
        self.disease_map = {
            0: 'Common Cold',
            1: 'Influenza (Flu)',
            2: 'COVID-19',
            3: 'Pneumonia',
            4: 'Gastroenteritis',
            5: 'Migraine',
            6: 'Allergic Reaction',
            7: 'Bronchitis',
            8: 'Healthy/Minor Ailment'
        }
        
    def train(self, X_train=None, y_train=None):
        """Train the disease prediction model"""
        if X_train is None or y_train is None:
            X_train, y_train = self._generate_synthetic_data()
        
        self.model = DecisionTreeClassifier(
            max_depth=15,
            min_samples_split=5,
            random_state=42
        )
        
        self.model.fit(X_train, y_train)
        
        os.makedirs('models', exist_ok=True)
        joblib.dump(self.model, self.model_path)
        print(f"Disease Prediction Model trained and saved to {self.model_path}")
        
    def _generate_synthetic_data(self, n_samples=2000):
        """Generate synthetic training data for disease prediction"""
        np.random.seed(42)
        
        X = []
        y = []
        
        # Number of symptoms
        n_symptoms = len(self.symptom_map)
        
        for _ in range(n_samples):
            symptoms = np.zeros(n_symptoms)
            
            # Generate random disease case
            disease = np.random.randint(0, len(self.disease_map))
            
            if disease == 0:  # Common Cold
                symptoms[[0, 1, 5, 14]] = 1  # fever, cough, sore_throat, runny_nose
                if np.random.random() > 0.5:
                    symptoms[4] = 1  # headache
            elif disease == 1:  # Influenza
                symptoms[[0, 1, 2, 6, 17]] = 1  # fever, cough, fatigue, body_ache, chills
                if np.random.random() > 0.5:
                    symptoms[4] = 1  # headache
            elif disease == 2:  # COVID-19
                symptoms[[0, 1, 2, 3]] = 1  # fever, cough, fatigue, difficulty_breathing
                if np.random.random() > 0.6:
                    symptoms[[12, 13]] = 1  # loss_of_taste, loss_of_smell
            elif disease == 3:  # Pneumonia
                symptoms[[0, 1, 3, 10]] = 1  # fever, cough, difficulty_breathing, chest_pain
                symptoms[17] = 1  # chills
            elif disease == 4:  # Gastroenteritis
                symptoms[[7, 8, 9, 16]] = 1  # nausea, vomiting, diarrhea, abdominal_pain
                if np.random.random() > 0.5:
                    symptoms[0] = 1  # fever
            elif disease == 5:  # Migraine
                symptoms[[4, 7, 11]] = 1  # headache, nausea, dizziness
            elif disease == 6:  # Allergic Reaction
                symptoms[[14, 15]] = 1  # runny_nose, rash
                if np.random.random() > 0.6:
                    symptoms[1] = 1  # cough
            elif disease == 7:  # Bronchitis
                symptoms[[1, 10]] = 1  # cough, chest_pain
                if np.random.random() > 0.5:
                    symptoms[[0, 2]] = 1  # fever, fatigue
            else:  # Healthy/Minor
                # Randomly add 0-2 mild symptoms
                n_mild = np.random.randint(0, 3)
                mild_symptoms = np.random.choice(n_symptoms, n_mild, replace=False)
                symptoms[mild_symptoms] = 1
            
            X.append(symptoms)
            y.append(disease)
        
        return np.array(X), np.array(y)
    
    def load(self):
        """Load the trained model"""
        if os.path.exists(self.model_path):
            self.model = joblib.load(self.model_path)
            return True
        return False
    
    def predict(self, symptoms_list):
        """
        Predict disease based on symptoms
        
        Args:
            symptoms_list: list of symptom names
        
        Returns:
            dict with disease name, confidence, and recommendations
        """
        if self.model is None:
            if not self.load():
                raise Exception("Model not trained or loaded")
        
        # Convert symptom list to feature vector
        features = np.zeros(len(self.symptom_map))
        for symptom in symptoms_list:
            symptom_lower = symptom.lower().replace(' ', '_')
            if symptom_lower in self.symptom_map:
                features[self.symptom_map[symptom_lower]] = 1
        
        # Make prediction
        disease_id = self.model.predict([features])[0]
        disease_proba = self.model.predict_proba([features])[0]
        
        disease_name = self.disease_map[disease_id]
        confidence = float(disease_proba[disease_id])
        
        # Generate recommendations
        recommendations = self._generate_disease_recommendations(disease_name, symptoms_list)
        
        return {
            'disease': disease_name,
            'confidence': confidence,
            'recommendations': recommendations,
            'severity': self._assess_severity(disease_name, confidence)
        }
    
    def _assess_severity(self, disease_name, confidence):
        """Assess severity of the predicted disease"""
        high_severity = ['Pneumonia', 'COVID-19']
        medium_severity = ['Influenza (Flu)', 'Bronchitis', 'Gastroenteritis']
        
        if disease_name in high_severity and confidence > 0.7:
            return 'high'
        elif disease_name in medium_severity and confidence > 0.6:
            return 'medium'
        else:
            return 'low'
    
    def _generate_disease_recommendations(self, disease_name, symptoms):
        """Generate recommendations based on predicted disease"""
        recommendations = []
        
        if disease_name == 'Common Cold':
            recommendations.extend([
                "Rest and get plenty of sleep",
                "Stay hydrated with water and warm fluids",
                "Use over-the-counter cold medications if needed",
                "Recovery typically takes 7-10 days"
            ])
        elif disease_name == 'Influenza (Flu)':
            recommendations.extend([
                "Rest and avoid physical exertion",
                "Stay hydrated",
                "Consider antiviral medications if within 48 hours of symptom onset",
                "Consult a doctor if symptoms worsen",
                "Isolate to prevent spreading"
            ])
        elif disease_name == 'COVID-19':
            recommendations.extend([
                "IMPORTANT: Get tested for COVID-19 immediately",
                "Isolate from others for at least 5 days",
                "Monitor oxygen levels if possible",
                "Seek medical attention if breathing difficulties worsen",
                "Stay hydrated and rest"
            ])
        elif disease_name == 'Pneumonia':
            recommendations.extend([
                "URGENT: Consult a doctor immediately",
                "May require antibiotics or hospitalization",
                "Monitor breathing and oxygen levels",
                "Rest and avoid strenuous activities",
                "Stay hydrated"
            ])
        elif disease_name == 'Gastroenteritis':
            recommendations.extend([
                "Stay well hydrated with clear fluids",
                "Follow BRAT diet (Bananas, Rice, Applesauce, Toast)",
                "Avoid dairy and fatty foods temporarily",
                "Rest and allow your body to recover",
                "Seek medical attention if severe dehydration occurs"
            ])
        elif disease_name == 'Migraine':
            recommendations.extend([
                "Rest in a quiet, dark room",
                "Apply cold compress to forehead",
                "Take prescribed migraine medication if available",
                "Avoid triggers like bright lights and loud sounds",
                "Consult a neurologist if migraines are frequent"
            ])
        elif disease_name == 'Allergic Reaction':
            recommendations.extend([
                "Identify and avoid the allergen",
                "Take antihistamines as needed",
                "If severe reaction, seek immediate medical attention",
                "Consider allergy testing",
                "Keep emergency medication if prescribed"
            ])
        elif disease_name == 'Bronchitis':
            recommendations.extend([
                "Rest and avoid irritants like smoke",
                "Stay hydrated with warm fluids",
                "Use a humidifier",
                "Consult a doctor if symptoms persist beyond 3 weeks",
                "Avoid strenuous activity"
            ])
        else:
            recommendations.extend([
                "Monitor symptoms",
                "Maintain healthy lifestyle habits",
                "Consult a doctor if symptoms worsen or persist"
            ])
        
        return recommendations
