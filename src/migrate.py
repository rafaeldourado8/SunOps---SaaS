#!/usr/bin/env python
"""Script para executar migrações do banco de dados"""
import subprocess
import sys

def run_migrations():
    """Executa as migrações pendentes"""
    try:
        print("🔄 Executando migrações...")
        result = subprocess.run(
            ["alembic", "upgrade", "head"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ Migrações executadas com sucesso!")
            print(result.stdout)
        else:
            print("❌ Erro ao executar migrações:")
            print(result.stderr)
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_migrations()
