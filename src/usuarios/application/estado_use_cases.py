from typing import Optional, Dict, Any
from usuarios.infrastructure.estado_repository import UsuarioEstadoRepository


class GerenciarEstadoUsuario:
    def __init__(self, repository: UsuarioEstadoRepository):
        self.repository = repository
    
    def salvar_preferencia(self, usuario_id: str, chave: str, valor: Any):
        """Salva preferência do usuário (tema, idioma, etc)"""
        return self.repository.salvar(usuario_id, f"pref:{chave}", valor)
    
    def obter_preferencia(self, usuario_id: str, chave: str, default: Any = None) -> Any:
        """Obtém preferência do usuário"""
        valor = self.repository.obter(usuario_id, f"pref:{chave}")
        return valor if valor is not None else default
    
    def salvar_filtro(self, usuario_id: str, tela: str, filtros: Dict):
        """Salva filtros aplicados em uma tela"""
        return self.repository.salvar(usuario_id, f"filtro:{tela}", filtros)
    
    def obter_filtro(self, usuario_id: str, tela: str) -> Optional[Dict]:
        """Obtém filtros salvos de uma tela"""
        return self.repository.obter(usuario_id, f"filtro:{tela}")
    
    def salvar_dashboard(self, usuario_id: str, config: Dict):
        """Salva configuração do dashboard"""
        return self.repository.salvar(usuario_id, "dashboard:config", config)
    
    def obter_dashboard(self, usuario_id: str) -> Optional[Dict]:
        """Obtém configuração do dashboard"""
        return self.repository.obter(usuario_id, "dashboard:config")
    
    def salvar_estado_tela(self, usuario_id: str, tela: str, estado: Dict):
        """Salva estado geral de uma tela (scroll, abas, etc)"""
        return self.repository.salvar(usuario_id, f"tela:{tela}", estado)
    
    def obter_estado_tela(self, usuario_id: str, tela: str) -> Optional[Dict]:
        """Obtém estado de uma tela"""
        return self.repository.obter(usuario_id, f"tela:{tela}")
    
    def obter_todos_estados(self, usuario_id: str) -> Dict[str, Any]:
        """Obtém todos os estados do usuário"""
        return self.repository.obter_todos(usuario_id)
    
    def limpar_estados(self, usuario_id: str) -> int:
        """Limpa todos os estados do usuário"""
        return self.repository.deletar_todos(usuario_id)
