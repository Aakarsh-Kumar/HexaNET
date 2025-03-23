import pandas as pd
import joblib

# Load test data
test_df = pd.read_pickle("test_df_processed.pkl")

# Load trained model
iso_forest = joblib.load("isolation_forest.pkl")

# Make predictions
X_test = test_df.drop(columns=["label"])
predictions = iso_forest.predict(X_test)

# Print predictions
print("✅ Predictions Completed")
print(predictions[:10])
