from scapy.all import sniff
import pandas as pd
import joblib
import os

# Load model
model, columns = joblib.load("model/model.pkl")

file_path = "live_data.csv"

# Create file if not exists
if not os.path.exists(file_path):
    pd.DataFrame(columns=["prediction"]).to_csv(file_path, index=False)

def process_packet(packet):
    try:
        # Simple features (approximation)
        data = {
            "duration": 0,
            "src_bytes": len(packet),
            "dst_bytes": len(packet),
            "count": 1,
            "srv_count": 1,
            "protocol_type": "tcp",
            "service": "http",
            "flag": "SF"
        }

        df = pd.DataFrame([data])
        df = pd.get_dummies(df)
        df = df.reindex(columns=columns, fill_value=0)

        pred = model.predict(df)[0]

        # Append to CSV
        df_out = pd.DataFrame({"prediction": [pred]})
        df_out.to_csv(file_path, mode='a', header=False, index=False)

        print("Packet:", pred)

    except:
        pass

# Start sniffing
sniff(prn=process_packet, store=False)