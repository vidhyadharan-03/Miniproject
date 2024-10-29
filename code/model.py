# model.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
import joblib

# Load the dataset and select features and target
df = pd.read_csv('updated.csv')
X = df[['RBC', 'WBC', 'PLT']]
y = df['CML_Risk']

# Split the dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale the data
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Create and train the model
model = LogisticRegression()
model.fit(X_train, y_train)

# Save the model and scaler
joblib.dump(model, 'logistic_regression_model.pkl')
joblib.dump(scaler, 'scaler.pkl')

def predict_cml_risk(rbc, wbc, platelet):
    # Example logic for calculating risk score and probability
    probability = 0.0

    # Simple model to calculate probability based on thresholds
    if rbc < 4.5:  # Example RBC threshold
        probability += 0.3  # Increase probability for low RBC

    if wbc > 10.0:  # Example WBC threshold
        probability += 0.4  # Increase probability for high WBC

    if platelet < 150:  # Example Platelet threshold
        probability += 0.3  # Increase probability for low Platelet

    # Cap probability at 1.0
    probability = min(probability, 1.0)

    # Determine risk level based on probability
    if probability < 0.4:
        risk_level = "Low Risk"
    elif 0.4 <= probability < 0.7:
        risk_level = "Moderate Risk"
    else:
        risk_level = "High Risk"

    return risk_level, probability

