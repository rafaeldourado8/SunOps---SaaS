#!/bin/bash
# Setup SSL com Let's Encrypt (Certbot)

set -e

echo "🔒 Configurando SSL/HTTPS com Let's Encrypt..."

# Verificar se está rodando como root
if [ "$EUID" -ne 0 ]; then 
    echo "❌ Execute como root: sudo ./setup-ssl.sh"
    exit 1
fi

# Solicitar domínio
read -p "Digite seu domínio (ex: crm.seusite.com): " DOMAIN
read -p "Digite seu email: " EMAIL

if [ -z "$DOMAIN" ] || [ -z "$EMAIL" ]; then
    echo "❌ Domínio e email são obrigatórios"
    exit 1
fi

# Instalar Certbot
echo "📦 Instalando Certbot..."
apt-get update
apt-get install -y certbot python3-certbot-nginx

# Parar nginx temporariamente
echo "⏸️  Parando nginx..."
cd /opt/crm-solar
docker-compose stop nginx

# Obter certificado
echo "🔐 Obtendo certificado SSL..."
certbot certonly --standalone \
    --non-interactive \
    --agree-tos \
    --email "$EMAIL" \
    -d "$DOMAIN"

# Criar configuração nginx com SSL
echo "📝 Criando configuração nginx com SSL..."
cat > /opt/crm-solar/nginx/nginx.ssl.conf << 'EOF'
# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name DOMAIN_PLACEHOLDER;
    return 301 https://$server_name$request_uri;
}

# HTTPS Server
server {
    listen 443 ssl http2;
    server_name DOMAIN_PLACEHOLDER;

    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/DOMAIN_PLACEHOLDER/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/DOMAIN_PLACEHOLDER/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;

    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Frontend
    location / {
        proxy_pass http://frontend:5173;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Backend API
    location /api/ {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Admin
    location /admin/ {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Health Check
    location /health/ {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
    }

    # Static Files
    location /static/ {
        alias /app/staticfiles/;
    }

    # Media Files
    location /media/ {
        alias /app/media/;
    }
}
EOF

# Substituir placeholder pelo domínio
sed -i "s/DOMAIN_PLACEHOLDER/$DOMAIN/g" /opt/crm-solar/nginx/nginx.ssl.conf

# Atualizar docker-compose para usar SSL
cat > /opt/crm-solar/docker-compose.ssl.yml << 'EOF'
services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.ssl.conf:/etc/nginx/conf.d/default.conf
      - /etc/letsencrypt:/etc/letsencrypt:ro
    depends_on:
      - backend
      - frontend
    networks:
      - crm_network
    restart: unless-stopped
EOF

# Atualizar .env
echo "📝 Atualizando .env..."
sed -i "s|CORS_ORIGINS=.*|CORS_ORIGINS=https://$DOMAIN|g" /opt/crm-solar/.env
sed -i "s|ALLOWED_HOSTS=.*|ALLOWED_HOSTS=$DOMAIN,localhost|g" /opt/crm-solar/.env
echo "SECURE_SSL_REDIRECT=True" >> /opt/crm-solar/.env
echo "SESSION_COOKIE_SECURE=True" >> /opt/crm-solar/.env
echo "CSRF_COOKIE_SECURE=True" >> /opt/crm-solar/.env

# Atualizar frontend .env
echo "VITE_API_URL=https://$DOMAIN" > /opt/crm-solar/frontend/.env

# Reiniciar com SSL
echo "🚀 Reiniciando com SSL..."
cd /opt/crm-solar
docker-compose -f docker-compose.yml -f docker-compose.ssl.yml up -d

# Configurar renovação automática
echo "⏰ Configurando renovação automática..."
(crontab -l 2>/dev/null; echo "0 3 * * * certbot renew --quiet && docker-compose -f /opt/crm-solar/docker-compose.yml -f /opt/crm-solar/docker-compose.ssl.yml restart nginx") | crontab -

echo ""
echo "✅ SSL configurado com sucesso!"
echo ""
echo "🌐 Acesse: https://$DOMAIN"
echo "🔐 Certificado válido por 90 dias"
echo "♻️  Renovação automática configurada"
echo ""
echo "⚠️  Certifique-se de que:"
echo "   1. DNS do domínio aponta para: $(curl -s ifconfig.me)"
echo "   2. Portas 80 e 443 estão abertas no Security Group"
echo ""
