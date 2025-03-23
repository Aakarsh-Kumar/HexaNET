import pandas as pd
from sklearn.preprocessing import LabelEncoder

# Define column names
column_names = [
    "duration", "protocol_type", "service", "flag", "src_bytes", "dst_bytes", 
    "land", "wrong_fragment", "urgent", "hot", "num_failed_logins", 
    "logged_in", "num_compromised", "root_shell", "su_attempted", "num_root",
    "num_file_creations", "num_shells", "num_access_files", "num_outbound_cmds",
    "is_host_login", "is_guest_login", "count", "srv_count", "serror_rate",
    "srv_serror_rate", "rerror_rate", "srv_rerror_rate", "same_srv_rate",
    "diff_srv_rate", "srv_diff_host_rate", "dst_host_count", "dst_host_srv_count",
    "dst_host_same_srv_rate", "dst_host_diff_srv_rate", "dst_host_same_src_port_rate",
    "dst_host_srv_diff_host_rate", "dst_host_serror_rate", "dst_host_srv_serror_rate",
    "dst_host_rerror_rate", "dst_host_srv_rerror_rate", "label"
]

# Load datasets
train_df = pd.read_csv("KDDTrain+.txt", names=column_names, header=None)
test_df = pd.read_csv("KDDTest+.txt", names=column_names, header=None)

print("✅ Data Loaded Successfully")

# Encode categorical columns
categorical_columns = ["protocol_type", "service", "flag", "label"]
encoder = LabelEncoder()

for col in categorical_columns:
    train_df[col] = encoder.fit_transform(train_df[col])
    test_df[col] = encoder.transform(test_df[col])

# Drop irrelevant features
train_df.drop(columns=["is_host_login", "num_outbound_cmds"], inplace=True)
test_df.drop(columns=["is_host_login", "num_outbound_cmds"], inplace=True)

# Save processed data
train_df.to_pickle("train_df_processed.pkl")
test_df.to_pickle("test_df_processed.pkl")

print("✅ Data Preprocessing Completed and Saved")
