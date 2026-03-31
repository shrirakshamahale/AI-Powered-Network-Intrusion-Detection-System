import joblib
import numpy as np

model = joblib.load("model/model.pkl")

def predict(data):
    data = np.array(data).reshape(1, -1)
    return model.predict(data)[0]