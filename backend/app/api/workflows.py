from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.workflow import Workflow, WorkflowStatus
from app.flows.main_workflow import main_workflow
from pydantic import BaseModel
import uuid

router = APIRouter()

class WorkflowCreate(BaseModel):
    name: str
    input_data: str

@router.post("/")
async def create_workflow(data: WorkflowCreate, db: AsyncSession = Depends(get_db)):
    """Create and trigger a new workflow."""
    workflow = Workflow(
        id=uuid.uuid4(),
        name=data.name,
        input_data=data.input_data,
        status=WorkflowStatus.running,
    )
    db.add(workflow)
    await db.commit()
    await db.refresh(workflow)

    # Run the Prefect flow
    result = await main_workflow(
        input_text=data.input_data,
        workflow_id=str(workflow.id)
    )

    # Update status
    workflow.status = WorkflowStatus.completed
    workflow.ai_result = str(result)
    await db.commit()

    return {"id": str(workflow.id), "status": "completed", "result": result}

@router.get("/")
async def list_workflows(db: AsyncSession = Depends(get_db)):
    """Get all workflows."""
    result = await db.execute(select(Workflow).order_by(Workflow.created_at.desc()))
    workflows = result.scalars().all()
    return [
        {
            "id": str(w.id),
            "name": w.name,
            "status": w.status,
            "created_at": str(w.created_at),
        }
        for w in workflows
    ]

@router.get("/{workflow_id}")
async def get_workflow(workflow_id: str, db: AsyncSession = Depends(get_db)):
    """Get a single workflow by ID."""
    result = await db.execute(select(Workflow).where(Workflow.id == workflow_id))
    workflow = result.scalar_one_or_none()
    if not workflow:
        return {"error": "Workflow not found"}
    return {
        "id": str(workflow.id),
        "name": workflow.name,
        "input_data": workflow.input_data,
        "ai_result": workflow.ai_result,
        "status": workflow.status,
        "created_at": str(workflow.created_at),
    }
