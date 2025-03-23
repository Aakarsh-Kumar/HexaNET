import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.model_selection import train_test_split

# Load preprocessed data
train_df = pd.read_pickle("train_df_processed.pkl")

# Define features (X) and target (y)
X = train_df.drop(columns=["label"])
y = train_df["label"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the Isolation Forest model
iso_forest = IsolationForest(n_estimators=100, contamination=0.1, random_state=42)
iso_forest.fit(X_train)

# Save trained model
import joblib
joblib.dump(iso_forest, "isolation_forest.pkl")

print("✅ Model Training Completed and Saved")
