import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.decomposition import PCA
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
import pickle

columns = ["duration", "protocol_type", "service", "flag", "src_bytes", "dst_bytes", 
           "land", "wrong_fragment", "urgent", "hot", "num_failed_logins", "logged_in",
           "num_compromised", "root_shell", "su_attempted", "num_root", "num_file_creations", 
           "num_shells", "num_access_files", "num_outbound_cmds", "is_host_login", 
           "is_guest_login", "count", "srv_count", "serror_rate", "srv_serror_rate", 
           "rerror_rate", "srv_rerror_rate", "same_srv_rate", "diff_srv_rate", 
           "srv_diff_host_rate", "dst_host_count", "dst_host_srv_count", "dst_host_same_srv_rate",
           "dst_host_diff_srv_rate", "dst_host_same_src_port_rate", "dst_host_srv_diff_host_rate",
           "dst_host_serror_rate", "dst_host_srv_serror_rate", "dst_host_rerror_rate", 
           "dst_host_srv_rerror_rate", "label", "difficulty"]

df = pd.read_csv("raw_data.csv")
df.columns = columns

categorical_cols = ["protocol_type", "service", "flag"]
for col in categorical_cols:
    df[col] = df[col].astype(str)

numeric_cols = [col for col in df.columns if col not in categorical_cols + ["label"]]
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.dropna(axis=1, how="all")
df = df.fillna(df.mean(numeric_only=True))

X = df.drop(columns=["label"])
y = df["label"]

X_encoded = pd.get_dummies(X, columns=categorical_cols)

scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X_encoded)

pca = PCA(n_components=3)
X_reduced = pca.fit_transform(X_scaled)
print(f"Final feature shape: {X_reduced.shape}")

scaler_pca = MinMaxScaler()
X_reduced_scaled = scaler_pca.fit_transform(X_reduced)
print(f"Initial feature shape: {X_reduced_scaled.shape}")

encoder = LabelEncoder()
y_encoded = encoder.fit_transform(y)

model = IsolationForest(n_estimators=100, contamination=0.1, random_state=42)
model.fit(X_reduced_scaled)

with open("isolation_forest_model.pkl", "wb") as f:
    pickle.dump(model, f)
with open("scaler_pca.pkl", "wb") as f: 
    pickle.dump(scaler_pca, f)
with open("pca.pkl", "wb") as f:
    pickle.dump(pca, f)
with open("label_encoder.pkl", "wb") as f:
    pickle.dump(encoder, f)

print("Training completed with 3 features!")