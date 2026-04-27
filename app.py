import streamlit as st
import pandas as pd
import plotly.express as px
import joblib
import numpy as np
import os
import json
import time

# -------------------------
# CONFIG
# -------------------------
st.set_page_config(page_title="Healthcare Dashboard", layout="wide")

# ---------------------------
# DATABASE + AUTH SYSTEM
# ---------------------------

import sqlite3
import hashlib
import streamlit as st

# Connect DB
conn = sqlite3.connect("users.db", check_same_thread=False)
c = conn.cursor()

# Create table
c.execute('''
CREATE TABLE IF NOT EXISTS users (
    username TEXT UNIQUE,
    password TEXT
)
''')

# ---------------------------
# HASH FUNCTION
# ---------------------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ---------------------------
# ADD USER 
# ---------------------------
def add_user(username, password):
    try:
        c.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hash_password(password))
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False  # username already exists


# ---------------------------
# LOGIN USER
# ---------------------------
def login_user(username, password):
    c.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, hash_password(password))
    )
    return c.fetchone()


# ---------------------------
# SESSION STATE
# ---------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# ---------------------------
# LOGIN / SIGNUP UI
# ---------------------------
def login_signup():
    st.title("🔐 Login / Signup")

    choice = st.selectbox(
        "Select Option",
        ["Login", "Signup"],
        key="auth_choice"
    )

    username = st.text_input("Username", key="auth_user")
    password = st.text_input("Password", type="password", key="auth_pass")

    # -------- SIGNUP --------
    if choice == "Signup":
        if st.button("Create Account"):

            if username.strip() == "" or password.strip() == "":
                st.warning("Please enter username and password")

            else:
                if add_user(username, password):
                    st.success("✅ Account created! Now login.")
                else:
                    st.error("⚠️ Username already exists")

    # -------- LOGIN --------
    if choice == "Login":
        if st.button("Login"):

            if username.strip() == "" or password.strip() == "":
                st.warning("Please enter username and password")

            else:
                result = login_user(username, password)

                if result:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.success(f"Welcome {username} 👋")
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials")


# ---------------------------
# ACCESS CONTROL
# ---------------------------
if not st.session_state.logged_in:
    login_signup()
    st.stop()

# #region agent log
def _agent_log(hypothesisId, location, message, data=None, runId="pre-fix"):
    try:
        log_paths = []
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            log_paths.append(os.path.join(base_dir, "debug-971df6.log"))
        except Exception:
            base_dir = None
        log_paths.append("debug-971df6.log")

        payload = {
            "sessionId": "971df6",
            "runId": runId,
            "hypothesisId": hypothesisId,
            "location": location,
            "message": message,
            "data": data or {},
            "timestamp": int(time.time() * 1000),
        }
        line = json.dumps(payload, ensure_ascii=False) + "\n"
        for p in log_paths:
            try:
                with open(p, "a", encoding="utf-8") as f:
                    f.write(line)
            except Exception:
                pass
    except Exception:
        pass
# #endregion agent log

_agent_log(
    "A",
    "app.py:preload",
    "Entering post-login data/model load",
    {
        "cwd": os.getcwd(),
        "script_dir": os.path.dirname(os.path.abspath(__file__)),
        "files_exist": {
            "processed_data.csv": os.path.exists("processed_data.csv"),
            "model_results.csv": os.path.exists("model_results.csv"),
            "model.pkl": os.path.exists("model.pkl"),
            "users.db": os.path.exists("users.db"),
        },
    },
)

# -------------------------
# LOAD DATA
# -------------------------
data = pd.read_csv("processed_data.csv")
models = pd.read_csv("model_results.csv")
model = joblib.load("model.pkl")

_agent_log(
    "A",
    "app.py:postload",
    "Loaded CSVs and model",
    {
        "data_shape": list(getattr(data, "shape", (None, None))),
        "models_shape": list(getattr(models, "shape", (None, None))),
        "data_cols": list(getattr(data, "columns", []))[:80],
        "models_cols": list(getattr(models, "columns", []))[:80],
        "data_dtypes": {k: str(v) for k, v in getattr(data, "dtypes", {}).items()},
        "models_dtypes": {k: str(v) for k, v in getattr(models, "dtypes", {}).items()},
        "model_type": str(type(model)),
        "has_feature_importances": bool(hasattr(model, "feature_importances_")),
        "feature_importances_len": int(len(getattr(model, "feature_importances_", [])))
        if hasattr(model, "feature_importances_")
        else None,
    },
)

# -------------------------
# FIX DATA FOR INTERACTIVITY
# -------------------------

# Ensure `year` exists
if "year" not in data.columns:
    data["year"] = 2021 + (data.index % 4)
else:
    # If only one year → create structured multi-year data
    if data["year"].nunique() == 1:
        data["year"] = 2021 + (data.index % 4)

# Ensure month exists and is meaningful
if "month" not in data.columns:
    data["month"] = (data.index % 12) + 1

# Create month names (for better charts)
data["month_name"] = data["month"].map({
    1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr",
    5: "May", 6: "Jun", 7: "Jul", 8: "Aug",
    9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"
})

_agent_log(
    "B",
    "app.py:postfixup",
    "After year/month/month_name fixups",
    {
        "year_in_cols": bool("year" in data.columns),
        "month_in_cols": bool("month" in data.columns),
        "year_nunique": int(data["year"].nunique()) if "year" in data.columns else None,
        "month_nunique": int(data["month"].nunique()) if "month" in data.columns else None,
        "year_sample": data["year"].head(5).tolist() if "year" in data.columns else None,
        "month_sample": data["month"].head(5).tolist() if "month" in data.columns else None,
        "month_name_sample": data["month_name"].head(5).tolist()
        if "month_name" in data.columns
        else None,
        "year_nulls": int(data["year"].isna().sum()) if "year" in data.columns else None,
        "month_nulls": int(data["month"].isna().sum()) if "month" in data.columns else None,
        "month_name_nulls": int(data["month_name"].isna().sum())
        if "month_name" in data.columns
        else None,
    },
)

# -------------------------
# DEBUG (optional)
# -------------------------
with st.sidebar.expander("Debug", expanded=False):
    show_debug = st.checkbox("Show data diagnostics", value=False)
if show_debug:
    st.write("Year Distribution:", data["year"].value_counts())

# -------------------------
# SIDEBAR FILTERS
# -------------------------
st.sidebar.header("🔍 Filters")

selected_month = st.sidebar.selectbox(
    "Select Month",
    sorted(data["month"].unique()),
    key="month_filter"
)

selected_year = st.sidebar.selectbox(
    "Select Year",
    sorted(data["year"].unique()),
    key="year_filter"
)

# Year filter (for charts)
filtered_data = data[data["year"] == selected_year]

# Month filter (for KPIs only)
month_filtered = filtered_data[filtered_data["month"] == selected_month]

# -------------------------
# TITLE
# -------------------------
st.title("🏥 Healthcare Analytics Dashboard")

st.markdown("""
### 📌 Project Overview
This dashboard analyzes hospital operations and predicts patient cost categories using machine learning.
""")

# -------------------------
# TABS
# -------------------------
tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "🤖 Prediction", "📥 Reports"])

# =========================
# TAB 1: DASHBOARD
# =========================
with tab1:

    st.subheader("📊 Key Metrics")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Patients", len(month_filtered))
    col2.metric("Total Revenue", f"{int(month_filtered['amount'].sum())}")
    col3.metric("Avg Age", int(month_filtered["age"].mean()))

    # MODEL COMPARISON
    st.subheader("🤖 Model Comparison")
    fig = px.bar(models, x="Model", y="Accuracy", color="Model")
    st.plotly_chart(fig, use_container_width=True)

    # PATIENT FLOW
    st.subheader("📈 Monthly Patient Trends")

    # Group properly
    monthly = data.groupby("month").size().reset_index(name="count")

    # Sort months
    monthly = monthly.sort_values("month")

    # Make month names (instead of numbers)
    month_map = {
        1:"Jan",2:"Feb",3:"Mar",4:"Apr",5:"May",6:"Jun",
        7:"Jul",8:"Aug",9:"Sep",10:"Oct",11:"Nov",12:"Dec"
    }
    monthly["month_name"] = monthly["month"].map(month_map)

    # Plot better chart
    fig = px.line(
        monthly,
        x="month_name",
        y="count",
        markers=True,
        title="Patient Visits Over Months",
    )

    # Style improvements
    fig.update_traces(line=dict(width=4))
    fig.update_layout(
        title_x=0.3,
        plot_bgcolor="#0E1117",
        paper_bgcolor="#0E1117",
        font=dict(color="white")
    )

    st.plotly_chart(fig, use_container_width=True, key="monthly_chart")

# BED UTILIZATION
if "bed_type" in filtered_data.columns:

    st.subheader("🛏️ Bed Utilization")

    if filtered_data.empty:
        st.warning("No data available for selected filters")

    else:
        bed = filtered_data["bed_type"].value_counts().reset_index()
        bed.columns = ["bed_type", "count"]

        fig = px.pie(
            bed,
            names="bed_type",
            values="count",
            title="Bed Distribution"
        )

        st.plotly_chart(fig, use_container_width=True, key="bed_chart")

# -------------------------
# FEATURE IMPORTANCE
# -------------------------
st.subheader("📊 Feature Importance")

# Extract importance from model
importance = model.feature_importances_

features = ["age", "treatment_duration", "month", "year"]

imp_df = pd.DataFrame({
    "Feature": features,
    "Importance": importance
})

fig = px.bar(
    imp_df,
    x="Feature",
    y="Importance",
    color="Feature",
    title="Feature Contribution to Prediction"
)

st.plotly_chart(fig, use_container_width=True)

# =========================
# TAB 2: PREDICTION (REAL ML)
# =========================
with tab2:

    st.subheader("🤖 Predict Patient Cost Category")

    col1, col2 = st.columns(2)

    with col1:
        age = st.slider("Age", 0, 100, 30)
        treatment_duration = st.slider("Treatment Duration", 1, 30, 5)

    with col2:
        month = st.slider("Month", 1, 12, 6)
        year = st.slider("Year", 2020, 2026, 2023)

    if st.button("Predict"):

        # Create input array (VERY IMPORTANT)
        input_data = np.array([[age, treatment_duration, month, year]])

        # Prediction
        prediction = model.predict(input_data)[0]

        # Probability (only if supported)
        prob = None
        if hasattr(model, "predict_proba"):
            prob = model.predict_proba(input_data)[0][1]

        # Output
        if prediction == 1:
            st.error("⚠️ High Cost Patient — Requires Attention")
        else:
            st.success("✅ Low Cost Patient — Stable")

        # Confidence
        if prob is not None:
            st.progress(int(prob * 100))
            st.caption(f"Confidence: {prob:.2%}")

        # Input summary
        st.info(f"""
    📊 Input Summary:
    - Age: {age}
    - Treatment Duration: {treatment_duration}
    - Month: {month}
    - Year: {year}
    """)
        
# =========================
# TAB 3: DOWNLOAD REPORT
# =========================
with tab3:

    st.subheader("📥 Download Reports")

    st.download_button(
        label="Download Processed Data",
        data=data.to_csv(index=False),
        file_name="processed_data.csv"
    )

    st.download_button(
        label="Download Model Results",
        data=models.to_csv(index=False),
        file_name="model_results.csv"
    )

# -------------------------
# FOOTER
# -------------------------
st.markdown("---")
st.markdown("🚀 Built using Spark + ML + Streamlit")