import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

columns = [
    "duration","protocol_type","service","flag","src_bytes","dst_bytes","land",
    "wrong_fragment","urgent","hot","num_failed_logins","logged_in","num_compromised",
    "root_shell","su_attempted","num_root","num_file_creations","num_shells",
    "num_access_files","num_outbound_cmds","is_host_login","is_guest_login",
    "count","srv_count","serror_rate","srv_serror_rate","rerror_rate",
    "srv_rerror_rate","same_srv_rate","diff_srv_rate","srv_diff_host_rate",
    "dst_host_count","dst_host_srv_count","dst_host_same_srv_rate",
    "dst_host_diff_srv_rate","dst_host_same_src_port_rate",
    "dst_host_srv_diff_host_rate","dst_host_serror_rate",
    "dst_host_srv_serror_rate","dst_host_rerror_rate",
    "dst_host_srv_rerror_rate","label","difficulty"
]

train_df = pd.read_csv("data/KDDTrain+.txt", names=columns)
test_df = pd.read_csv("data/KDDTest+.txt", names=columns)

train_df.drop("difficulty", axis=1, inplace=True)
test_df.drop("difficulty", axis=1, inplace=True)

def map_attack(label):
    if label == "normal":
        return "normal"
    elif label in ["neptune","smurf","back","teardrop","pod"]:
        return "DoS"
    elif label in ["ipsweep","nmap","portsweep","satan"]:
        return "Probe"
    elif label in ["guess_passwd","ftp_write","imap","phf"]:
        return "R2L"
    else:
        return "U2R"

train_df["label"] = train_df["label"].apply(map_attack)
test_df["label"] = test_df["label"].apply(map_attack)

features = [
    "duration","protocol_type","service","flag",
    "src_bytes","dst_bytes","count","srv_count"
]

X_train = train_df[features]
y_train = train_df["label"]

X_test = test_df[features]
y_test = test_df["label"]

X_train = pd.get_dummies(X_train)
X_test = pd.get_dummies(X_test)
X_test = X_test.reindex(columns=X_train.columns, fill_value=0)

model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

os.makedirs("model", exist_ok=True)
joblib.dump((model, X_train.columns), "model/model.pkl")

print("✅ Model trained successfully!")