from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
import os
from preprocess import load_data, encode_data

# Load
train_df, test_df = load_data("data/KDDTrain+.txt", "data/KDDTest+.txt")

X_train = train_df.drop("label", axis=1)
y_train = train_df["label"]

X_test = test_df.drop("label", axis=1)
y_test = test_df["label"]

# Encode
X_train, X_test = encode_data(X_train, X_test)

# Train
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))

# Save
os.makedirs("model", exist_ok=True)
joblib.dump(model, "model/model.pkl")