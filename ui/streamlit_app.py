import streamlit as st
import requests

st.title("Agentic AI Loan Approval System")

applicant_id = st.text_input("Applicant ID")
age = st.number_input("Age", min_value=18, max_value=70)
income = st.number_input("Monthly Income")

employment = st.selectbox("Employment Type", ["Salaried", "Self-Employed"])

credit_score = st.number_input("Credit Score", min_value=300, max_value=850)
loan_amount = st.number_input("Loan Amount")
tenure = st.number_input("Tenure (months)")
liabilities = st.number_input("Existing Liabilities")

if st.button("Submit Application"):

    data = {
        "applicant_id": applicant_id,
        "age": age,
        "income": income,
        "employment": employment,
        "credit_score": credit_score,
        "loan_amount": loan_amount,
        "tenure": tenure,
        "liabilities": liabilities
    }

    response = requests.post(
        "http://127.0.0.1:8000/submit_application",
        json=data
    )

    if response.status_code == 200:
        result = response.json()

        st.success("Loan Decision")
        st.write(result)

    else:
        st.error("API Error")