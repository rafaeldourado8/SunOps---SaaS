from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class BaseAgent(ABC):
    """Interface base para todos os agentes IA"""
    
    def __init__(self, agent_type: str):
        self.agent_type = agent_type
        self.context: Dict[str, Any] = {}
    
    @abstractmethod
    async def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Processa mensagem e retorna resposta"""
        pass
    
    @abstractmethod
    async def should_transfer_to_human(self, message: Dict[str, Any]) -> bool:
        """Verifica se deve transferir para humano"""
        pass
    
    def update_context(self, key: str, value: Any):
        """Atualiza contexto da conversa"""
        self.context[key] = value
    
    def get_context(self, key: str) -> Optional[Any]:
        """Recupera valor do contexto"""
        return self.context.get(key)
