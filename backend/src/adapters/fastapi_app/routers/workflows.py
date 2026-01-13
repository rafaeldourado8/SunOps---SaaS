from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from uuid import UUID
from datetime import datetime

from ...infrastructure.database.config import AsyncSessionLocal
from ...infrastructure.database.models.workflow import Workflow, WorkflowExecution
from ..schemas.workflow import WorkflowCreate, WorkflowUpdate, WorkflowResponse, WorkflowExecutionResponse

router = APIRouter(prefix="/api/v1/workflows", tags=["workflows"])

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@router.get("/node-types")
async def get_node_types():
    from ..schemas.node_types import NodeType
    return [
        {
            "type": NodeType.AGENT_VENDAS,
            "name": NodeType.get_display_name(NodeType.AGENT_VENDAS),
            "icon": NodeType.get_icon(NodeType.AGENT_VENDAS),
            "category": "agents"
        },
        {
            "type": NodeType.AGENT_SUPORTE,
            "name": NodeType.get_display_name(NodeType.AGENT_SUPORTE),
            "icon": NodeType.get_icon(NodeType.AGENT_SUPORTE),
            "category": "agents"
        },
        {
            "type": NodeType.WHATSAPP,
            "name": NodeType.get_display_name(NodeType.WHATSAPP),
            "icon": NodeType.get_icon(NodeType.WHATSAPP),
            "category": "integrations"
        },
        {
            "type": NodeType.INVERSOR,
            "name": NodeType.get_display_name(NodeType.INVERSOR),
            "icon": NodeType.get_icon(NodeType.INVERSOR),
            "category": "integrations"
        },
        {
            "type": NodeType.PDF_GENERATOR,
            "name": NodeType.get_display_name(NodeType.PDF_GENERATOR),
            "icon": NodeType.get_icon(NodeType.PDF_GENERATOR),
            "category": "utilities"
        }
    ]

@router.post("", response_model=WorkflowResponse)
async def create_workflow(
    workflow: WorkflowCreate,
    db: AsyncSession = Depends(get_db)
):
    db_workflow = Workflow(
        name=workflow.name,
        user_id=1,  # TODO: Get from JWT token
        data_json=workflow.data_json
    )
    db.add(db_workflow)
    await db.commit()
    await db.refresh(db_workflow)
    return db_workflow

@router.get("", response_model=List[WorkflowResponse])
async def list_workflows(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Workflow))
    workflows = result.scalars().all()
    return workflows

@router.get("/{workflow_id}", response_model=WorkflowResponse)
async def get_workflow(workflow_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Workflow).where(Workflow.id == workflow_id))
    workflow = result.scalar_one_or_none()
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return workflow

@router.put("/{workflow_id}", response_model=WorkflowResponse)
async def update_workflow(
    workflow_id: UUID,
    workflow_update: WorkflowUpdate,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Workflow).where(Workflow.id == workflow_id))
    workflow = result.scalar_one_or_none()
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    if workflow_update.name:
        workflow.name = workflow_update.name
    if workflow_update.data_json is not None:
        workflow.data_json = workflow_update.data_json
    workflow.updated_at = datetime.utcnow()
    
    await db.commit()
    await db.refresh(workflow)
    return workflow

@router.delete("/{workflow_id}")
async def delete_workflow(workflow_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Workflow).where(Workflow.id == workflow_id))
    workflow = result.scalar_one_or_none()
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    await db.delete(workflow)
    await db.commit()
    return {"message": "Workflow deleted"}

@router.post("/{workflow_id}/execute", response_model=WorkflowExecutionResponse)
async def execute_workflow(workflow_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Workflow).where(Workflow.id == workflow_id))
    workflow = result.scalar_one_or_none()
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    execution = WorkflowExecution(
        workflow_id=workflow_id,
        status="running",
        logs="Workflow execution started"
    )
    db.add(execution)
    await db.commit()
    await db.refresh(execution)
    
    # TODO: Implement actual workflow execution logic
    execution.status = "completed"
    execution.finished_at = datetime.utcnow()
    execution.logs += "\nWorkflow execution completed"
    await db.commit()
    await db.refresh(execution)
    
    return execution

@router.get("/{workflow_id}/executions", response_model=List[WorkflowExecutionResponse])
async def list_executions(workflow_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(WorkflowExecution).where(WorkflowExecution.workflow_id == workflow_id)
    )
    executions = result.scalars().all()
    return executions
