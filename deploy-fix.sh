#!/bin/bash
# Deploy rápido da correção

echo "🚀 Fazendo deploy da correção..."

# Commit e push
git add backend/apps/orcamentos/views.py
git commit -m "fix: adicionar decorator @action ao método detalhamento"
git push origin prod

echo "✅ Push realizado! Aguarde o deploy automático ou execute na EC2:"
echo ""
echo "ssh ec2-user@sunops.com.br"
echo "cd /var/www/SunOps---SaaS"
echo "git pull origin prod"
echo "sudo systemctl restart gunicorn"
echo "sudo systemctl restart nginx"
