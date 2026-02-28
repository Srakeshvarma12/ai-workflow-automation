from prefect import flow, task
from app.services.gemini_service import classify_input
from app.services.rabbitmq_service import publish_task
import uuid

@task(retries=3, retry_delay_seconds=10, name="AI Processing")
async def ai_process_task(input_text: str) -> dict:
    """Process input with Gemini AI."""
    result = await classify_input(input_text)
    return result

@task(name="Queue Action")
async def queue_action_task(ai_result: dict, workflow_id: str):
    """Send result to RabbitMQ for further processing."""
    await publish_task("workflow_results", {
        "workflow_id": workflow_id,
        "result": ai_result,
    })

@task(name="Log Result")
async def log_result_task(workflow_id: str, result: dict):
    """Log the workflow result."""
    print(f"Workflow {workflow_id} completed: {result}")
    return True

from typing import Optional

@flow(name="main-ai-workflow", log_prints=True)
async def main_workflow(input_text: str, workflow_id: Optional[str] = None):
    """Main workflow: Input → AI → Queue → Log."""
    if not workflow_id:
        workflow_id = str(uuid.uuid4())

    # Step 1: Process with AI
    ai_result = await ai_process_task(input_text)

    # Step 2: Queue the result
    await queue_action_task(ai_result, workflow_id)

    # Step 3: Log
    await log_result_task(workflow_id, ai_result)

    return {"workflow_id": workflow_id, "result": ai_result}
