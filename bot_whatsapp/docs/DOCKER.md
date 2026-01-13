# 🐳 Deploy com Docker

O WhatsApp Gateway está integrado no docker-compose.yml principal do SunOps.

## 🚀 Iniciar Gateway (junto com toda stack)

```bash
# Na raiz do projeto SunOps
cd d:\SunOps
docker-compose up -d
```

Isso iniciará:
- ✅ FastAPI (porta 8000)
- ✅ PostgreSQL Master + Replica (5432, 5433)
- ✅ Redis (6379)
- ✅ RabbitMQ (5672, 15672)
- ✅ Celery Worker
- ✅ **WhatsApp Gateway (porta 3001)**

## 📱 Ver QR Code

```bash
docker-compose logs -f whatsapp-gateway
```

Ou abra: `bot_whatsapp/examples/qrcode-frontend.html`

## 📊 Monitoramento

- **FastAPI**: http://localhost:8000/docs
- **RabbitMQ**: http://localhost:15672 (guest/guest)
- **WebSocket**: ws://localhost:3001
- **Logs**: `docker-compose logs -f whatsapp-gateway`

## 🔄 Rebuild Gateway

```bash
cd d:\SunOps
docker-compose up -d --build whatsapp-gateway
```

---

## 💾 Persistência de Dados

Os volumes Docker garantem que os dados persistam entre restarts:

- `whatsapp_session`: Sessão autenticada do WhatsApp
- `whatsapp_cache`: Cache do whatsapp-web.js
- `rabbitmq_data`: Mensagens e configurações do RabbitMQ

### Backup da sessão:

```bash
docker run --rm -v whatsapp_session:/data -v $(pwd):/backup alpine tar czf /backup/whatsapp-session-backup.tar.gz -C /data .
```

### Restaurar sessão:

```bash
docker run --rm -v whatsapp_session:/data -v $(pwd):/backup alpine tar xzf /backup/whatsapp-session-backup.tar.gz -C /data
```

## 🐛 Troubleshooting

```bash
# Ver logs
docker-compose logs -f whatsapp-gateway

# Resetar sessão WhatsApp
docker-compose down
docker volume rm sunops_whatsapp-session sunops_whatsapp-cache
docker-compose up -d whatsapp-gateway
```
