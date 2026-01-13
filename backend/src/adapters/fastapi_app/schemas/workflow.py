from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime
from uuid import UUID

class WorkflowCreate(BaseModel):
    name: str
    data_json: Dict[str, Any] = {}

class WorkflowUpdate(BaseModel):
    name: Optional[str] = None
    data_json: Optional[Dict[str, Any]] = None

class WorkflowResponse(BaseModel):
    id: UUID
    name: str
    user_id: int
    data_json: Dict[str, Any]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class WorkflowExecutionResponse(BaseModel):
    id: UUID
    workflow_id: UUID
    status: str
    started_at: datetime
    finished_at: Optional[datetime]
    logs: Optional[str]
    
    class Config:
        from_attributes = True
