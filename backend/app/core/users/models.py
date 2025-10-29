import enum
from sqlalchemy import Column, Integer, String, Enum as SAEnum
from sqlalchemy.orm import relationship
from app.db import Base # Importa a Base do seu app/db.py
from . import hashing

# 1. Define as opções de "função" (role)
class UserRole(str, enum.Enum):
    GESTOR = "gestor"
    VENDEDOR = "vendedor"
    SUPORTE = "suporte"

# 2. Define a tabela "users"
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False) # Armazena a senha hasheada

    # 3. A coluna de "função" (role) que discutimos
    role = Column(SAEnum(UserRole), nullable=False, default=UserRole.VENDEDOR)

    # 4. Relações do SunOps (substitui 'cart' e 'orders')
    # Um vendedor pode ter várias propostas
    propostas = relationship("Proposta", back_populates="vendedor_responsavel")
    
    # Um gestor pode ser responsável por vários projetos
    projetos = relationship("Projeto", back_populates="gestor_responsavel")


    def __repr__(self) -> str:
        '''Representação em string do objeto User'''
        return f"<User(id={self.id!r}, name={self.name!r}, role={self.role!r})>"
    
    def check_password(self, password):
        '''Verifica se a senha fornecida corresponde ao hash armazenado'''
        return hashing.verify_password(password, self.password_hash)