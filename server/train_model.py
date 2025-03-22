import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler

# Load dataset
df = pd.read_csv("./server/raw_data.csv")

features = ['packet_size', 'protocol', 'source_port', 'destination_port']
X = df[features]
y = df['label']  

encoder = LabelEncoder()
y_encoded = encoder.fit_transform(y)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

pd.DataFrame(X_scaled, columns=features).to_csv("./server/raw_data.csv", index=False)
