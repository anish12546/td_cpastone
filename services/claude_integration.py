import os

def explain_decision(profile, risk, decision):
    """
    This function generates explanation using Claude API.
    If API is not available, fallback explanation is returned.
    """

    api_key = os.getenv("ANTHROPIC_API_KEY")

    
    if not api_key:
        return (
            f"Decision = {decision['classification']}. "
            f"Based on Income Stability = {profile['income_stability']}, "
            f"Credit Risk = {risk['credit_risk']}, "
            f"DTI Ratio = {risk['dti_ratio']}."
        )

    
    try:
        from anthropic import Anthropic

        client = Anthropic(api_key=api_key)

        prompt = f"""
        Explain loan decision:

        Profile:
        Income Stability: {profile['income_stability']}
        Employment Risk: {profile['employment_risk']}

        Risk:
        Credit Risk: {risk['credit_risk']}
        DTI Ratio: {risk['dti_ratio']}

        Decision:
        Classification: {decision['classification']}
        Confidence: {decision['confidence']}

        Give simple explanation.
        """

        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=200,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return response.content[0].text

    except Exception as e:
        return f"Claude error: {str(e)}"