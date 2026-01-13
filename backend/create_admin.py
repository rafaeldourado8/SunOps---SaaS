import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from passlib.context import CryptContext
import os

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def create_admin():
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://admin:changeme@localhost:5432/sunwops")
    
    engine = create_async_engine(DATABASE_URL)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        # Check if admin exists
        result = await session.execute(
            text("SELECT id FROM users WHERE email = 'admin@sunops.com'")
        )
        if result.scalar_one_or_none():
            print("Admin user already exists")
            return
        
        # Create admin
        hashed_password = pwd_context.hash("admin123")
        await session.execute(
            text("""
            INSERT INTO users (email, hashed_password, full_name, is_active, is_superuser)
            VALUES ('admin@sunops.com', :password, 'Admin', true, true)
            """),
            {"password": hashed_password}
        )
        await session.commit()
        print("Admin user created: admin@sunops.com / admin123")

if __name__ == "__main__":
    asyncio.run(create_admin())
