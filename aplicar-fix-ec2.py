#!/usr/bin/env python3
"""
Script para aplicar correção na EC2 via SSH
Execute: python aplicar-fix-ec2.py
"""

import subprocess
import sys

EC2_HOST = "ec2-user@3.226.196.27"
PROJECT_PATH = "/var/www/SunOps---SaaS"
FILE_PATH = f"{PROJECT_PATH}/backend/apps/orcamentos/views.py"

# Comando sed para adicionar o decorator antes da linha do método
FIX_COMMAND = f"""
sudo sed -i '289i\\    @action(detail=True, methods=[\\'get\\'])' {FILE_PATH} && \
sudo systemctl restart gunicorn && \
echo "✅ Correção aplicada e Gunicorn reiniciado!"
"""

print("🚀 Aplicando correção na EC2...")
print(f"Host: {EC2_HOST}")
print(f"Arquivo: {FILE_PATH}")
print()

try:
    result = subprocess.run(
        ["ssh", EC2_HOST, FIX_COMMAND],
        capture_output=True,
        text=True,
        timeout=30
    )
    
    print(result.stdout)
    if result.stderr:
        print("Erros:", result.stderr)
    
    if result.returncode == 0:
        print("\n✅ Deploy concluído com sucesso!")
        print("Teste: https://sunops.com.br/api/orcamentos/1/detalhamento/")
    else:
        print(f"\n❌ Erro no deploy (código {result.returncode})")
        sys.exit(1)
        
except subprocess.TimeoutExpired:
    print("❌ Timeout na conexão SSH")
    sys.exit(1)
except Exception as e:
    print(f"❌ Erro: {e}")
    sys.exit(1)
