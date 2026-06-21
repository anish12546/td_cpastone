from orchestrator.orchestrator import orchestrate


def test_workflow():
    data={"income":40000,"employment":"salaried","credit_score":700,"loan_amount":100000, "liabilities":20000}
    result=orchestrate(data)
    assert result["classification"] in ["Approved","Rejected","Review"]