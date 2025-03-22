import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
import joblib
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


label_col = "label" 

if label_col not in df.columns:
    raise KeyError(f"Column '{label_col}' not found in dataset. Available columns: {df.columns}")

features = df.drop(columns=[label_col])
labels = df[label_col]

cat_cols = features.select_dtypes(include=['object']).columns.tolist()
num_cols = features.select_dtypes(include=['int64', 'float64']).columns.tolist()

if cat_cols:
    print(f"Categorical Columns Detected: {cat_cols}")
    features = pd.get_dummies(features, columns=cat_cols, drop_first=True)


scaler = MinMaxScaler()
features_scaled = scaler.fit_transform(features)

encoder = LabelEncoder()
labels_encoded = encoder.fit_transform(labels)

model = IsolationForest(n_estimators=100, contamination=0.1, random_state=42)
model.fit(features_scaled)

joblib.dump(model, "isolation_forest_model.pkl")
joblib.dump(scaler, "scaler.pkl")
joblib.dump(encoder, "label_encoder.pkl")

print("trained")
