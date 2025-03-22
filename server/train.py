# import pandas as pd
# from sklearn.ensemble import IsolationForest
# from sklearn.preprocessing import MinMaxScaler, LabelEncoder
# import pickle
# columns = ["duration", "protocol_type", "service", "flag", "src_bytes", "dst_bytes", 
#            "land", "wrong_fragment", "urgent", "hot", "num_failed_logins", "logged_in",
#            "num_compromised", "root_shell", "su_attempted", "num_root", "num_file_creations", 
#            "num_shells", "num_access_files", "num_outbound_cmds", "is_host_login", 
#            "is_guest_login", "count", "srv_count", "serror_rate", "srv_serror_rate", 
#            "rerror_rate", "srv_rerror_rate", "same_srv_rate", "diff_srv_rate", 
#            "srv_diff_host_rate", "dst_host_count", "dst_host_srv_count", "dst_host_same_srv_rate",
#            "dst_host_diff_srv_rate", "dst_host_same_src_port_rate", "dst_host_srv_diff_host_rate",
#            "dst_host_serror_rate", "dst_host_srv_serror_rate", "dst_host_rerror_rate", 
#            "dst_host_srv_rerror_rate", "label", "difficulty"]

# df = pd.read_csv("raw_data.csv") 
# df.columns = columns

# df["src_bytes"] = pd.to_numeric(df["src_bytes"], errors="coerce")
# df["difficulty"] = pd.to_numeric(df["difficulty"], errors="coerce")

# # Then create your features dataframe
# label_col = "label"
# features = df.drop(columns=[label_col])
# labels = df[label_col]

# # Now check for categorical columns - they should exclude src_bytes and difficulty
# cat_cols = features.select_dtypes(include=['object']).columns.tolist()
# print(f"Categorical Columns Detected: {cat_cols}")
# print(f"Original Feature Shape: {features.shape}")

# # Apply one-hot encoding
# if cat_cols:
#     features = pd.get_dummies(features, columns=cat_cols)
#     print(f"After One-Hot Encoding: {features.shape}")
# scaler = MinMaxScaler()
# features_scaled = scaler.fit_transform(features)

# encoder = LabelEncoder()
# labels_encoded = encoder.fit_transform(labels)

# model = IsolationForest(n_estimators=100, contamination=0.1, random_state=42)
# model.fit(features_scaled)

# with open("isolation_forest_model.pkl", "wb") as model_file:
#     pickle.dump(model, model_file)
# with open("scaler.pkl", "wb") as scaler_file:
#     pickle.dump(scaler, scaler_file)

# with open("label_encoder.pkl", "wb") as encoder_file:
#     pickle.dump(encoder, encoder_file)

# print("trained")


###import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
import pickle
import numpy as np

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

# Load data
df = pd.read_csv("raw_data.csv")
df.columns = columns

# Preprocess categorical columns
categorical_cols = ["protocol_type", "service", "flag"]
for col in categorical_cols:
    df[col] = df[col].astype(str)

# Convert numeric columns
numeric_cols = [col for col in df.columns if col not in categorical_cols + ["label"]]
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Drop all-NA columns and fill remaining NAs
df = df.dropna(axis=1, how="all")
df = df.fillna(df.mean(numeric_only=True))

# Split features/labels
X = df.drop(columns=["label"])
y = df["label"]

# One-hot encode all categorical features
X_encoded = pd.get_dummies(X, columns=categorical_cols)

# Scale features
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X_encoded)

# Reduce to 6 features using PCA
pca = PCA(n_components=6)
X_reduced = pca.fit_transform(X_scaled)
print(f"Final feature shape: {X_reduced.shape}")

# Encode labels
encoder = LabelEncoder()
y_encoded = encoder.fit_transform(y)

# Train model
model = IsolationForest(n_estimators=100, contamination=0.1, random_state=42)
model.fit(X_reduced)

# Save artifacts
with open("isolation_forest_model.pkl", "wb") as f:
    pickle.dump(model, f)
with open("scaler.pkl", "wb") as f:
    pickle.dump(scaler, f)
with open("pca.pkl", "wb") as f:
    pickle.dump(pca, f)
with open("label_encoder.pkl", "wb") as f:
    pickle.dump(encoder, f)

print("Training completed with 6 features!")