from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session
from sqlalchemy import select
from usuarios.infrastructure.models import UsuarioEstadoModel
import uuid


class UsuarioEstadoRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def salvar(self, usuario_id: str, chave: str, valor: Any) -> UsuarioEstadoModel:
        """Salva ou atualiza estado do usuário"""
        estado = self.db.query(UsuarioEstadoModel).filter(
            UsuarioEstadoModel.usuario_id == usuario_id,
            UsuarioEstadoModel.chave == chave
        ).first()
        
        if estado:
            estado.valor = valor
        else:
            estado = UsuarioEstadoModel(
                id=uuid.uuid4(),
                usuario_id=usuario_id,
                chave=chave,
                valor=valor
            )
            self.db.add(estado)
        
        self.db.commit()
        self.db.refresh(estado)
        return estado
    
    def obter(self, usuario_id: str, chave: str) -> Optional[Any]:
        """Obtém valor do estado"""
        estado = self.db.query(UsuarioEstadoModel).filter(
            UsuarioEstadoModel.usuario_id == usuario_id,
            UsuarioEstadoModel.chave == chave
        ).first()
        
        return estado.valor if estado else None
    
    def obter_todos(self, usuario_id: str) -> Dict[str, Any]:
        """Obtém todos os estados do usuário"""
        estados = self.db.query(UsuarioEstadoModel).filter(
            UsuarioEstadoModel.usuario_id == usuario_id
        ).all()
        
        return {estado.chave: estado.valor for estado in estados}
    
    def deletar(self, usuario_id: str, chave: str) -> bool:
        """Remove estado específico"""
        estado = self.db.query(UsuarioEstadoModel).filter(
            UsuarioEstadoModel.usuario_id == usuario_id,
            UsuarioEstadoModel.chave == chave
        ).first()
        
        if estado:
            self.db.delete(estado)
            self.db.commit()
            return True
        return False
    
    def deletar_todos(self, usuario_id: str) -> int:
        """Remove todos os estados do usuário"""
        count = self.db.query(UsuarioEstadoModel).filter(
            UsuarioEstadoModel.usuario_id == usuario_id
        ).delete()
        self.db.commit()
        return count
