from .base import Base
from .workflow import Workflow, WorkflowExecution

# Re-export from models.py for compatibility
import sys
from pathlib import Path
models_path = Path(__file__).parent.parent / 'models.py'
if models_path.exists():
    import importlib.util
    spec = importlib.util.spec_from_file_location("old_models", models_path)
    old_models = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(old_models)
    UserModel = old_models.UserModel
    KitModel = old_models.KitModel
    ItemKitModel = old_models.ItemKitModel
    OrcamentoModel = old_models.OrcamentoModel
    DomainEventModel = old_models.DomainEventModel
    ConversationModel = old_models.ConversationModel
    MessageModel = old_models.MessageModel
    TicketModel = old_models.TicketModel
else:
    UserModel = None
    KitModel = None
    ItemKitModel = None
    OrcamentoModel = None
    DomainEventModel = None
    ConversationModel = None
    MessageModel = None
    TicketModel = None

__all__ = [
    "Base", 
    "Workflow", 
    "WorkflowExecution",
    "UserModel",
    "KitModel",
    "ItemKitModel",
    "OrcamentoModel",
    "DomainEventModel",
    "ConversationModel",
    "MessageModel",
    "TicketModel"
]
