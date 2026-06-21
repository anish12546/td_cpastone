from communication.mcp_server import mcp_client
import datetime


def log_compliance(decision):

    mcp_client.send("compliance_agent", decision)

    fair_lending_check = "Required" if decision["classification"] == "Rejected" else "Passed"
    fcra_notice_required = True if decision["classification"] == "Rejected" else False

    return {
        "action_taken": decision["classification"],
        "notification_sent": True,
        "case_id": f"CASE-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}",
        "timestamp": str(datetime.datetime.now()),
        "fair_lending_check": fair_lending_check,
        "fcra_notice_required": fcra_notice_required,
        "summary": decision["explanation"]
    }