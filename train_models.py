"""
Train and save all ML models for the health monitoring system
"""
from models.health_risk_model import HealthRiskModel
from models.disease_prediction_model import DiseasePredictionModel
from models.vitals_anomaly_model import VitalsAnomalyModel

def main():
    """
    Main function to train all machine learning models for the health monitoring system.
    
    This function trains three models:
    1. Health Risk Prediction Model - Predicts patient health risk levels
    2. Disease Prediction Model - Predicts diseases based on symptoms
    3. Vitals Anomaly Detection Model - Detects abnormal vital signs
    
    All models are saved to the 'models/' directory for later use by the application.
    """
    print("=" * 60)
    print("AI Health Monitoring System - Model Training")
    print("=" * 60)
    print()
    
    # Train Health Risk Model
    print("Training Health Risk Prediction Model...")
    health_risk_model = HealthRiskModel()
    health_risk_model.train()
    print("✓ Health Risk Model trained successfully\n")
    
    # Train Disease Prediction Model
    print("Training Disease Prediction Model...")
    disease_prediction_model = DiseasePredictionModel()
    disease_prediction_model.train()
    print("✓ Disease Prediction Model trained successfully\n")
    
    # Train Vitals Anomaly Model
    print("Training Vitals Anomaly Detection Model...")
    vitals_anomaly_model = VitalsAnomalyModel()
    vitals_anomaly_model.train()
    print("✓ Vitals Anomaly Model trained successfully\n")
    
    print("=" * 60)
    print("All models trained and saved successfully!")
    print("=" * 60)
    print("\nYou can now start the application with: python app.py")

if __name__ == '__main__':
    main()
