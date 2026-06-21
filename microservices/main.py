

from fastapi import FastAPI
from orchestrator.langgraph_workflow import run_workflow as orchestrate
import logging

# logging setup
logging.basicConfig(level=logging.INFO)

app = FastAPI()

@app.post("/submit_application")
def submit_application(data: dict):
    try:
        logging.info(f"Received data: {data}")

        result = orchestrate(data)

        logging.info(f"Result generated: {result}")

        return result

    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")

        return {
            "status": "error",
            "message": str(e)
        }