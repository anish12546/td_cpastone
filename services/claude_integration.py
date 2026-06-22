# import os

# def explain_decision(profile, risk, decision):
#     """
#     This function generates explanation using Claude API.
#     If API is not available, fallback explanation is returned.
#     """

#     api_key = os.getenv("ANTHROPIC_API_KEY")

    
#     if not api_key:
#         return (
#             f"Decision = {decision['classification']}. "
#             f"Based on Income Stability = {profile['income_stability']}, "
#             f"Credit Risk = {risk['credit_risk']}, "
#             f"DTI Ratio = {risk['dti_ratio']}."
#         )

    
#     try:
#         from anthropic import Anthropic

#         client = Anthropic(api_key=api_key)

#         prompt = f"""
#         Explain loan decision:

#         Profile:
#         Income Stability: {profile['income_stability']}
#         Employment Risk: {profile['employment_risk']}

#         Risk:
#         Credit Risk: {risk['credit_risk']}
#         DTI Ratio: {risk['dti_ratio']}

#         Decision:
#         Classification: {decision['classification']}
#         Confidence: {decision['confidence']}

#         Give simple explanation.
#         """

#         response = client.messages.create(
#             model="claude-3-haiku-20240307",
#             max_tokens=200,
#             messages=[
#                 {"role": "user", "content": prompt}
#             ]
#         )

#         return response.content[0].text

#     except Exception as e:
#         return f"Claude error: {str(e)}"

import os
from dotenv import load_dotenv


load_dotenv()


def explain_decision(profile, risk, decision):
    """
    Generates explanation using Claude API.
    Falls back if API is not available.
    """

    api_key = os.getenv("ANTHROPIC_API_KEY")
    model_id = os.getenv("MODEL_ID", "anthropic.claude-sonnet-4-6")
    print("API KEY:", os.getenv("ANTHROPIC_API_KEY"))

    if not api_key:
        return (
            f"Decision = {decision.get('classification')}. "
            f"Based on Income Stability = {profile.get('income_stability')}, "
            f"Credit Risk = {risk.get('credit_risk')}, "
            f"DTI Ratio = {risk.get('dti_ratio')}."
        )

    try:
        from anthropic import Anthropic

        client = Anthropic(api_key=api_key)

        prompt = f"""
Explain loan decision:

Profile:
Income Stability: {profile.get('income_stability')}
Employment Risk: {profile.get('employment_risk')}

Risk:
Credit Risk: {risk.get('credit_risk')}
DTI Ratio: {risk.get('dti_ratio')}

Decision:
Classification: {decision.get('classification')}
Confidence: {decision.get('confidence')}

Give simple explanation in 2-3 lines.
"""

        response = client.messages.create(
            model=model_id,  
            max_tokens=int(os.getenv("MAX_TOKENS", 200)),
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return response.content[0].text

    except Exception as e:
        return f"Claude error: {str(e)}"