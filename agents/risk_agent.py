
from communication.mcp_server import mcp_client

def analyze_risk(data):

    mcp_client.send("risk_agent", data)
    mcp_client.send("credit_score_service", data)

    dti_ratio = (data["liabilities"] + data["loan_amount"]) / max(data["income"], 1)

    if data["credit_score"] < 600:
        credit_risk = "High"
    elif data["credit_score"] < 700:
        credit_risk = "Medium"
    else:
        credit_risk = "Low"

    loan_risk = "High" if data["loan_amount"] > (data["income"] * 10) else "Low"

    anomaly = dti_ratio > 0.5 or loan_risk == "High"

    risk_score = (
        (0.4 * (1 if credit_risk == "High" else 0.5 if credit_risk == "Medium" else 0)) +
        (0.3 * dti_ratio) +
        (0.3 * (1 if loan_risk == "High" else 0))
    )

    risk_score = round(risk_score, 2)

    return {
        "dti_ratio": round(dti_ratio, 2),
        "credit_risk": credit_risk,
        "loan_risk": loan_risk,
        "anomaly": anomaly,
        "risk_score": risk_score
    }
