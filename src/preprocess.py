import pandas as pd
from sklearn.preprocessing import LabelEncoder

def load_data(train_path, test_path):
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

    train_df = pd.read_csv(train_path, names=columns)
    test_df = pd.read_csv(test_path, names=columns)

    train_df.drop("difficulty", axis=1, inplace=True)
    test_df.drop("difficulty", axis=1, inplace=True)

    # Binary classification
    train_df["label"] = train_df["label"].apply(lambda x: 0 if x=="normal" else 1)
    test_df["label"] = test_df["label"].apply(lambda x: 0 if x=="normal" else 1)

    return train_df, test_df


def encode_data(X_train, X_test):
    le = LabelEncoder()

    for col in X_train.select_dtypes(include=['object']).columns:
        X_train[col] = le.fit_transform(X_train[col])
        X_test[col] = le.transform(X_test[col])

    return X_train, X_test