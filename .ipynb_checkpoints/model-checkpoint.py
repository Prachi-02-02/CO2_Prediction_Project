import pandas as pd
import joblib
from sklearn.linear_model import LinearRegression

# Load Dataset
df = pd.read_csv(r'C:\Users\ADMIN\Machine Learning\data.csv')

# Prepare data
X = df[['weight', 'volume']]
y = df['CO2']

# Train model
model = LinearRegression()
model.fit(X, y)

# Save the trained model
joblib.dump(model, "co2_model.pkl")
print("Model saved as co2_model.pkl")
