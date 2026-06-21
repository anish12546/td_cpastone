from communication.mcp_server import mcp_client

def analyze_profile(data):

    
    mcp_client.send("profile_agent", data)
    mcp_client.send("employment_verification_service", data)

   
    income_stability = "High" if data["income"] > 30000 else "Low"

    employment_risk = "Low" if data["employment"] == "Salaried" else "High"

    completeness = "Complete" if all(data.values()) else "Incomplete"

    return {
        "income_stability": income_stability,
        "employment_risk": employment_risk,
        "credit_history_summary": f"Credit Score : {data['credit_score']}",
        "application_flags": completeness
    }