# 🏥 Healthcare Analytics Dashboard

An end-to-end **data analytics and machine learning application** that enables hospitals to analyze operational data and predict patient cost categories for better decision-making.

---

## 🚀 Overview

Healthcare institutions generate massive amounts of data but often lack tools to derive actionable insights.
This project bridges that gap by combining **data analytics, visualization, and machine learning** into a single interactive dashboard.

---

## ✨ Key Features

### 📊 Interactive Dashboard

* Real-time KPIs: **Total Patients, Revenue, Average Age**
* Dynamic filtering by **Year and Month**
* Clean and responsive UI using Streamlit

### 📈 Advanced Visualizations

* Monthly patient trends using **Plotly**
* Model performance comparison
* Bed utilization insights

### 🤖 Machine Learning Integration

* Predicts **patient cost category**
* Model trained using **Random Forest**
* Compared with Logistic Regression, Decision Tree, ANN

### 🔐 Authentication System

* Login & Signup functionality using **SQLite**
* Session-based authentication handling

### 📥 Export & Reporting

* Download processed datasets
* Export model results for analysis

---

## 🧠 Tech Stack

| Category         | Tools Used    |
| ---------------- | ------------- |
| Programming      | Python        |
| Data Processing  | Pandas, NumPy |
| Visualization    | Plotly        |
| Machine Learning | Scikit-learn  |
| Backend/UI       | Streamlit     |
| Database         | SQLite        |
| Model Storage    | Joblib        |

---

## 📊 Machine Learning Workflow

* Data preprocessing and feature selection
* Model training and evaluation
* Accuracy comparison across models
* Deployment of best model (Random Forest)
* Integration into real-time prediction UI

---

## 📁 Project Structure

```
Healthcare_Project/
│
├── app.py                  # Main Streamlit application
├── model.pkl               # Trained ML model
├── processed_data.csv      # Cleaned dataset
├── model_results.csv       # Model evaluation results
├── requirements.txt        # Dependencies
├── users.db                # SQLite database (local auth)
└── README.md               # Project documentation
```

---

## ⚙️ Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## 🌐 Live Demo

👉 (https://healthcare-analytics-dashboard-yc9tki8dayfktjnua4bgrd.streamlit.app/)

---

## 🎯 Problem Statement

Hospitals often struggle to:

* Analyze patient flow efficiently
* Optimize resource utilization (beds, staff)
* Predict patient cost categories

This project solves these challenges using **data-driven insights and predictive modeling**.

---

## 💡 Key Highlights

* Built a **full-stack data application**
* Integrated **ML model into production UI**
* Designed **interactive analytics dashboard**
* Implemented **authentication system**
* Deployment-ready architecture

---

## 🚀 Future Improvements

* Cloud database integration (PostgreSQL / Firebase)
* Real-time data streaming
* Role-based authentication
* Advanced predictive models

---

## 👤 Author

**Lakshita Singh**
B.Tech CSE (Data Science)
