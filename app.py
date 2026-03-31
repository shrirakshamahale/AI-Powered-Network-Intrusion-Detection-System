import streamlit as st
import joblib
import pandas as pd
import plotly.express as px
import time
import smtplib
from email.mime.text import MIMEText

# ---------------- LOAD MODEL ----------------
model, columns = joblib.load("model/model.pkl")

st.set_page_config(page_title="SentinelNet Pro", layout="wide")

# ---------------- CUSTOM UI ----------------
st.markdown("""
<style>
.main { background-color: #0f172a; }
.title { font-size: 48px; font-weight: 700; color: #38bdf8; }
.subtitle { font-size: 18px; color: #94a3b8; }
.section { font-size: 26px; font-weight: 600; color: #e2e8f0; }
.stButton>button { font-size: 18px; border-radius: 10px; padding: 10px; }
.metric { font-size: 22px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# ---------------- EMAIL ----------------
def send_email(pred):
    sender = "your_email@gmail.com"
    password = "your_app_password"
    receiver = "your_email@gmail.com"

    msg = MIMEText(f"⚠️ Alert: {pred} attack detected!")
    msg["Subject"] = "SentinelNet Alert"

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, receiver, msg.as_string())
        server.quit()
    except:
        pass

# ---------------- FILE READER ----------------
def load_file(file):
    name = file.name.lower()

    try:
        if name.endswith(".csv"):
            try:
                return pd.read_csv(file)
            except:
                return pd.read_csv(file, encoding='latin1')

        elif name.endswith(".txt"):
            try:
                return pd.read_csv(file, header=None)
            except:
                return pd.read_csv(file, header=None, encoding='latin1')

        elif name.endswith(".xlsx") or name.endswith(".xls"):
            return pd.read_excel(file)

        else:
            st.error("❌ Unsupported file format")
            return None

    except Exception as e:
        st.error(f"Error reading file: {e}")
        return None

# ---------------- HEADER ----------------
st.markdown('<p class="title">🔐 SentinelNet Pro</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">AI-Powered Intrusion Detection Dashboard</p>', unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
mode = st.sidebar.radio("Mode", [
    "Single Prediction",
    "Bulk Detection",
    "Real-Time Simulation"
])

# ---------------- PREPROCESS ----------------
def preprocess(data):
    df = pd.DataFrame([data])
    df = pd.get_dummies(df)
    df = df.reindex(columns=columns, fill_value=0)
    return df

# ---------------- SINGLE ----------------
if mode == "Single Prediction":

    st.markdown('<p class="section">🔍 Single Traffic Analysis</p>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        duration = st.number_input("Duration", 0.0)
        src_bytes = st.number_input("Source Bytes", 0.0)
        dst_bytes = st.number_input("Destination Bytes", 0.0)
        count = st.number_input("Count", 0.0)
        srv_count = st.number_input("Service Count", 0.0)

        protocol = st.selectbox("Protocol", ["tcp", "udp", "icmp"])
        service = st.selectbox("Service", ["http", "ftp", "smtp", "domain_u"])
        flag = st.selectbox("Flag", ["SF", "S0", "REJ"])

    with col2:
        if st.button("🚀 Detect Attack"):

            data = {
                "duration": duration,
                "src_bytes": src_bytes,
                "dst_bytes": dst_bytes,
                "count": count,
                "srv_count": srv_count,
                "protocol_type": protocol,
                "service": service,
                "flag": flag
            }

            df = preprocess(data)

            pred = model.predict(df)[0]
            probs = model.predict_proba(df)[0]

            if pred == "normal":
                st.success("✅ Normal Traffic")
            else:
                st.error(f"⚠️ {pred} Attack Detected")
                st.toast("🚨 Intrusion detected!")
                send_email(pred)

            st.markdown(f'<p class="metric">🧠 Confidence: {max(probs)*100:.2f}%</p>', unsafe_allow_html=True)

            fig = px.bar(
                x=model.classes_,
                y=probs,
                color=model.classes_,
                title="Prediction Confidence",
                text_auto=True
            )
            st.plotly_chart(fig, use_container_width=True)

# ---------------- BULK ----------------
elif mode == "Bulk Detection":

    st.markdown('<p class="section">📁 Bulk Traffic Analysis</p>', unsafe_allow_html=True)

    file = st.file_uploader("Upload File")

    if file:
        df = load_file(file)

        if df is not None:
            st.write("Preview:")
            st.dataframe(df.head())

            df_enc = pd.get_dummies(df)
            df_enc = df_enc.reindex(columns=columns, fill_value=0)

            preds = model.predict(df_enc)
            df["Prediction"] = preds

            st.dataframe(df.head())

            fig = px.histogram(df, x="Prediction", color="Prediction",
                               title="Attack Distribution")

            st.plotly_chart(fig, use_container_width=True)

# ---------------- REAL TIME ----------------
elif mode == "Real-Time Simulation":

    st.markdown('<p class="section">⚡ Live Simulation</p>', unsafe_allow_html=True)

    file = st.file_uploader("Upload File", key="rt")

    if file:
        df = load_file(file)

        if df is not None:
            df_enc = pd.get_dummies(df)
            df_enc = df_enc.reindex(columns=columns, fill_value=0)

            if st.button("▶️ Start Monitoring"):

                normal = 0
                attack = 0
                last_alert = None

                chart = st.empty()

                for i in range(len(df_enc)):
                    row = df_enc.iloc[i:i+1]
                    pred = model.predict(row)[0]

                    if pred == "normal":
                        normal += 1
                    else:
                        attack += 1

                        if pred != last_alert:
                            send_email(pred)
                            last_alert = pred

                    fig = px.bar(
                        x=["Normal", "Attack"],
                        y=[normal, attack],
                        color=["Normal", "Attack"],
                        title="Live Traffic Monitoring",
                        text_auto=True
                    )

                    chart.plotly_chart(fig, use_container_width=True)

                    time.sleep(0.4)