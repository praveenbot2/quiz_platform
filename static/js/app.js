// API Base URL
const API_BASE = window.location.origin + '/api';

// Tab Navigation
function showTab(tabName) {
    // Hide all tabs
    const tabs = document.querySelectorAll('.tab-content');
    tabs.forEach(tab => tab.classList.remove('active'));
    
    // Remove active class from all buttons
    const buttons = document.querySelectorAll('.tab-btn');
    buttons.forEach(btn => btn.classList.remove('active'));
    
    // Show selected tab
    document.getElementById(tabName).classList.add('active');
    event.target.classList.add('active');
    
    // Load data for specific tabs
    if (tabName === 'patients') {
        loadPatientsList();
    }
}

// Show message
function showMessage(elementId, message, type) {
    const messageEl = document.getElementById(elementId);
    messageEl.textContent = message;
    messageEl.className = `message ${type}`;
    messageEl.style.display = 'block';
    
    // Auto hide after 5 seconds
    setTimeout(() => {
        messageEl.style.display = 'none';
    }, 5000);
}

// Load patients into select dropdowns
async function loadPatients() {
    try {
        const response = await fetch(`${API_BASE}/patients`);
        const patients = await response.json();
        
        // Update all patient select elements
        const selectElements = [
            'vitals_patient_id',
            'symptoms_patient_id',
            'monitor_patient_id'
        ];
        
        selectElements.forEach(id => {
            const select = document.getElementById(id);
            if (select) {
                select.innerHTML = '<option value="">Select a patient</option>';
                patients.forEach(patient => {
                    const option = document.createElement('option');
                    option.value = patient.id;
                    option.textContent = `${patient.name} (Age: ${patient.age}, ID: ${patient.id})`;
                    select.appendChild(option);
                });
            }
        });
    } catch (error) {
        console.error('Error loading patients:', error);
    }
}

// Register Patient Form
document.getElementById('registerForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData.entries());
    
    try {
        const response = await fetch(`${API_BASE}/patients`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (response.ok) {
            showMessage('registerMessage', 'Patient registered successfully!', 'success');
            e.target.reset();
            loadPatients(); // Refresh patient lists
        } else {
            showMessage('registerMessage', result.error || 'Error registering patient', 'error');
        }
    } catch (error) {
        showMessage('registerMessage', 'Network error: ' + error.message, 'error');
    }
});

// Record Vitals Form
document.getElementById('vitalsForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const data = {};
    
    formData.forEach((value, key) => {
        if (value !== '') {
            data[key] = isNaN(value) ? value : parseFloat(value);
        }
    });
    
    try {
        const response = await fetch(`${API_BASE}/health-data`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (response.ok) {
            showMessage('vitalsMessage', 'Vitals recorded successfully!', 'success');
        } else {
            showMessage('vitalsMessage', result.error || 'Error recording vitals', 'error');
        }
    } catch (error) {
        showMessage('vitalsMessage', 'Network error: ' + error.message, 'error');
    }
});

// Analyze Vitals
async function analyzeVitals() {
    const form = document.getElementById('vitalsForm');
    const formData = new FormData(form);
    const data = {};
    
    formData.forEach((value, key) => {
        if (value !== '') {
            data[key] = isNaN(value) ? value : parseFloat(value);
        }
    });
    
    if (!data.patient_id) {
        showMessage('vitalsMessage', 'Please select a patient first', 'error');
        return;
    }
    
    const analysisDiv = document.getElementById('vitalsAnalysis');
    analysisDiv.innerHTML = '<div class="loading"></div> Analyzing...';
    analysisDiv.classList.add('show');
    
    try {
        // Health Risk Prediction
        const riskResponse = await fetch(`${API_BASE}/predict/health-risk`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        const riskResult = await riskResponse.json();
        
        // Vitals Anomaly Detection
        const anomalyResponse = await fetch(`${API_BASE}/predict/vitals-anomaly`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        const anomalyResult = await anomalyResponse.json();
        
        // Display results
        displayAnalysisResults(riskResult.prediction, anomalyResult.prediction);
        
    } catch (error) {
        analysisDiv.innerHTML = `<div class="message error">Error during analysis: ${error.message}</div>`;
    }
}

function displayAnalysisResults(riskData, anomalyData) {
    const analysisDiv = document.getElementById('vitalsAnalysis');
    
    let html = '<h3>Analysis Results</h3>';
    
    // Health Risk
    html += `
        <div class="result-card">
            <h3>Health Risk Assessment</h3>
            <p>Risk Level: <span class="risk-badge risk-${riskData.risk_level}">${riskData.risk_level.toUpperCase()}</span></p>
            <p>Risk Score: ${riskData.risk_score}%</p>
            <p>Confidence: ${(riskData.confidence * 100).toFixed(1)}%</p>
            <div class="recommendations">
                <strong>Recommendations:</strong>
                <ul>
                    ${riskData.recommendations.map(rec => `<li>${rec}</li>`).join('')}
                </ul>
            </div>
        </div>
    `;
    
    // Vitals Anomaly
    html += `
        <div class="result-card">
            <h3>Vital Signs Analysis</h3>
            <p>Status: ${anomalyData.is_anomaly ? 
                '<span class="risk-badge risk-high">Anomaly Detected</span>' : 
                '<span class="risk-badge risk-low">Normal</span>'}</p>
            <p>Severity: <span class="risk-badge risk-${anomalyData.severity}">${anomalyData.severity.toUpperCase()}</span></p>
    `;
    
    if (anomalyData.detected_issues && anomalyData.detected_issues.length > 0) {
        html += '<div class="recommendations"><strong>Detected Issues:</strong>';
        anomalyData.detected_issues.forEach(issue => {
            const criticalClass = issue.severity === 'critical' ? 'issue-critical' : '';
            html += `
                <div class="issue-item ${criticalClass}">
                    <strong>${issue.vital}: ${issue.issue}</strong><br>
                    Value: ${issue.value} (Normal: ${issue.normal_range})<br>
                    Severity: ${issue.severity}
                </div>
            `;
        });
        html += '</div>';
    }
    
    html += '</div>';
    
    analysisDiv.innerHTML = html;
}

// Symptoms Form
document.getElementById('symptomsForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const patientId = document.getElementById('symptoms_patient_id').value;
    const checkboxes = document.querySelectorAll('input[name="symptom"]:checked');
    const symptoms = Array.from(checkboxes).map(cb => cb.value);
    
    if (!patientId) {
        showMessage('symptomsMessage', 'Please select a patient', 'error');
        return;
    }
    
    if (symptoms.length === 0) {
        showMessage('symptomsMessage', 'Please select at least one symptom', 'error');
        return;
    }
    
    const resultsDiv = document.getElementById('diseaseResults');
    resultsDiv.innerHTML = '<div class="loading"></div> Predicting...';
    resultsDiv.classList.add('show');
    
    try {
        const response = await fetch(`${API_BASE}/predict/disease`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ patient_id: patientId, symptoms: symptoms })
        });
        
        const result = await response.json();
        
        if (response.ok) {
            displayDiseaseResults(result.prediction);
            showMessage('symptomsMessage', 'Disease prediction completed!', 'success');
        } else {
            resultsDiv.innerHTML = '';
            resultsDiv.classList.remove('show');
            showMessage('symptomsMessage', result.error || 'Error predicting disease', 'error');
        }
    } catch (error) {
        resultsDiv.innerHTML = '';
        resultsDiv.classList.remove('show');
        showMessage('symptomsMessage', 'Network error: ' + error.message, 'error');
    }
});

function displayDiseaseResults(predictionData) {
    const resultsDiv = document.getElementById('diseaseResults');
    
    let html = `
        <div class="result-card">
            <h3>Disease Prediction Results</h3>
            <p>Predicted Disease: <strong style="color: #667eea; font-size: 1.2em;">${predictionData.disease}</strong></p>
            <p>Confidence: ${(predictionData.confidence * 100).toFixed(1)}%</p>
            <p>Severity: <span class="risk-badge risk-${predictionData.severity}">${predictionData.severity.toUpperCase()}</span></p>
            <div class="recommendations">
                <strong>Recommendations:</strong>
                <ul>
                    ${predictionData.recommendations.map(rec => `<li>${rec}</li>`).join('')}
                </ul>
            </div>
        </div>
    `;
    
    resultsDiv.innerHTML = html;
}

// Load Monitoring Data
async function loadMonitoringData() {
    const patientId = document.getElementById('monitor_patient_id').value;
    const dashboard = document.getElementById('monitoringDashboard');
    
    if (!patientId) {
        dashboard.innerHTML = '';
        return;
    }
    
    dashboard.innerHTML = '<div class="loading"></div> Loading...';
    
    try {
        const response = await fetch(`${API_BASE}/monitor/${patientId}`);
        const data = await response.json();
        
        if (response.ok) {
            displayMonitoringDashboard(data);
        } else {
            dashboard.innerHTML = `<div class="message error">${data.error}</div>`;
        }
    } catch (error) {
        dashboard.innerHTML = `<div class="message error">Error loading monitoring data: ${error.message}</div>`;
    }
}

function displayMonitoringDashboard(data) {
    const dashboard = document.getElementById('monitoringDashboard');
    
    let html = `
        <div class="monitoring-card">
            <h3>Patient Information</h3>
            <div class="patient-info">
                <p><strong>Name:</strong> ${data.patient.name}</p>
                <p><strong>Age:</strong> ${data.patient.age}</p>
                <p><strong>Gender:</strong> ${data.patient.gender}</p>
                <p><strong>Blood Group:</strong> ${data.patient.blood_group || 'N/A'}</p>
            </div>
        </div>
    `;
    
    if (data.latest_health_data) {
        const hd = data.latest_health_data;
        html += `
            <div class="monitoring-card">
                <h3>Latest Vital Signs</h3>
                <p style="color: #6c757d; font-size: 0.9em;">Recorded: ${new Date(hd.recorded_at).toLocaleString()}</p>
                <div class="vital-grid">
                    ${hd.heart_rate ? `<div class="vital-item">
                        <div class="vital-label">Heart Rate</div>
                        <div class="vital-value">${hd.heart_rate} <span class="vital-unit">bpm</span></div>
                    </div>` : ''}
                    ${hd.temperature ? `<div class="vital-item">
                        <div class="vital-label">Temperature</div>
                        <div class="vital-value">${hd.temperature} <span class="vital-unit">°C</span></div>
                    </div>` : ''}
                    ${hd.blood_pressure_systolic && hd.blood_pressure_diastolic ? `<div class="vital-item">
                        <div class="vital-label">Blood Pressure</div>
                        <div class="vital-value">${hd.blood_pressure_systolic}/${hd.blood_pressure_diastolic} <span class="vital-unit">mmHg</span></div>
                    </div>` : ''}
                    ${hd.oxygen_saturation ? `<div class="vital-item">
                        <div class="vital-label">Oxygen Saturation</div>
                        <div class="vital-value">${hd.oxygen_saturation} <span class="vital-unit">%</span></div>
                    </div>` : ''}
                    ${hd.respiratory_rate ? `<div class="vital-item">
                        <div class="vital-label">Respiratory Rate</div>
                        <div class="vital-value">${hd.respiratory_rate} <span class="vital-unit">breaths/min</span></div>
                    </div>` : ''}
                    ${hd.bmi ? `<div class="vital-item">
                        <div class="vital-label">BMI</div>
                        <div class="vital-value">${hd.bmi.toFixed(1)}</div>
                    </div>` : ''}
                </div>
            </div>
        `;
    }
    
    if (data.recent_predictions && data.recent_predictions.length > 0) {
        html += `
            <div class="monitoring-card">
                <h3>Recent Predictions</h3>
        `;
        
        data.recent_predictions.forEach(pred => {
            html += `
                <div class="result-card">
                    <p><strong>Type:</strong> ${pred.prediction_type.replace('_', ' ').toUpperCase()}</p>
                    <p><strong>Result:</strong> ${pred.prediction_result}</p>
                    <p><strong>Risk Level:</strong> <span class="risk-badge risk-${pred.risk_level}">${pred.risk_level ? pred.risk_level.toUpperCase() : 'N/A'}</span></p>
                    <p><strong>Time:</strong> ${new Date(pred.created_at).toLocaleString()}</p>
                    ${pred.recommendations ? `<p><strong>Recommendations:</strong> ${pred.recommendations}</p>` : ''}
                </div>
            `;
        });
        
        html += '</div>';
    }
    
    dashboard.innerHTML = html;
}

// Load Patients List
async function loadPatientsList() {
    const listDiv = document.getElementById('patientsList');
    listDiv.innerHTML = '<div class="loading"></div> Loading...';
    
    try {
        const response = await fetch(`${API_BASE}/patients`);
        const patients = await response.json();
        
        if (patients.length === 0) {
            listDiv.innerHTML = '<p>No patients registered yet.</p>';
            return;
        }
        
        let html = '';
        patients.forEach(patient => {
            html += `
                <div class="patient-card">
                    <div class="patient-info">
                        <p><strong>ID:</strong> ${patient.id}</p>
                        <p><strong>Name:</strong> ${patient.name}</p>
                        <p><strong>Age:</strong> ${patient.age}</p>
                        <p><strong>Gender:</strong> ${patient.gender}</p>
                        <p><strong>Blood Group:</strong> ${patient.blood_group || 'N/A'}</p>
                        <p><strong>Email:</strong> ${patient.email}</p>
                        <p><strong>Phone:</strong> ${patient.phone || 'N/A'}</p>
                        <p><strong>Registered:</strong> ${new Date(patient.created_at).toLocaleDateString()}</p>
                    </div>
                </div>
            `;
        });
        
        listDiv.innerHTML = html;
    } catch (error) {
        listDiv.innerHTML = `<div class="message error">Error loading patients: ${error.message}</div>`;
    }
}

// Initialize - Load patients when page loads
document.addEventListener('DOMContentLoaded', () => {
    loadPatients();
});
