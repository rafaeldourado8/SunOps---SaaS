from sqlalchemy.orm import Session
from passlib.context import CryptContext
import uuid

from shared.infrastructure.database import SessionLocal, Base, engine
from usuarios.infrastructure.models import UsuarioModel

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_users():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    # Verificar se já existe admin
    existing_admin = db.query(UsuarioModel).filter(UsuarioModel.email == "admin@sunops.com").first()
    if existing_admin:
        print("Admin já existe!")
        db.close()
        return
    
    # Criar Admin
    admin = UsuarioModel(
        id=uuid.uuid4(),
        nome="Administrador",
        email="admin@sunops.com",
        senha_hash=pwd_context.hash("admin123"),
        tipo="ADMIN",
        ativo=True
    )
    db.add(admin)
    
    # Criar Gestor
    gestor = UsuarioModel(
        id=uuid.uuid4(),
        nome="Gestor",
        email="gestor@sunops.com",
        senha_hash=pwd_context.hash("gestor123"),
        tipo="GESTOR",
        ativo=True
    )
    db.add(gestor)
    
    # Criar Vendedor
    vendedor = UsuarioModel(
        id=uuid.uuid4(),
        nome="Vendedor",
        email="vendedor@sunops.com",
        senha_hash=pwd_context.hash("vendedor123"),
        tipo="VENDEDOR",
        ativo=True
    )
    db.add(vendedor)
    
    db.commit()
    db.close()
    
    print("✅ Usuários criados com sucesso!")
    print("\n📋 Credenciais:")
    print("Admin: admin@sunops.com / admin123")
    print("Gestor: gestor@sunops.com / gestor123")
    print("Vendedor: vendedor@sunops.com / vendedor123")


if __name__ == "__main__":
    create_users()
