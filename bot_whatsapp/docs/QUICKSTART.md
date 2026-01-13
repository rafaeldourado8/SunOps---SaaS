# 🚀 Guia Rápido - SunOps WhatsApp Gateway

## 1️⃣ Instalar Dependências

```bash
npm install
```

## 2️⃣ Iniciar RabbitMQ (Docker)

```bash
docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
```

Acesse: http://localhost:15672 (guest/guest)

## 3️⃣ Testar Conexão RabbitMQ

```bash
npm run test:rabbitmq
```

Deve exibir:
```
✅ Filas criadas com sucesso!
   - whatsapp_messages (entrada)
   - whatsapp_responses (saída)
```

## 4️⃣ Iniciar Gateway

```bash
npm start
```

Você verá:
1. QR Code no terminal
2. WebSocket rodando na porta 3001
3. RabbitMQ conectado

## 5️⃣ Escanear QR Code

Abra WhatsApp no celular → Aparelhos conectados → Escanear QR Code

## 6️⃣ Testar Mensagem

Envie uma mensagem para o número conectado. Você verá no console:

```
📩 Mensagem recebida de João Silva: Olá
```

A mensagem será publicada na fila `whatsapp_messages`.

## 7️⃣ Enviar Resposta (Teste Manual)

Abra o RabbitMQ Management (http://localhost:15672):

1. Vá em **Queues** → `whatsapp_responses`
2. Clique em **Publish message**
3. Cole o JSON:

```json
{
  "to": "5511999999999@c.us",
  "text": "Olá! Esta é uma resposta automática.",
  "typing": 3000
}
```

4. Clique em **Publish message**

O gateway enviará a mensagem para o WhatsApp com indicador de digitação.

## 🔧 Troubleshooting

### Erro: "Cannot find module 'amqplib'"
```bash
npm install
```

### Erro: "ECONNREFUSED localhost:5672"
RabbitMQ não está rodando. Execute:
```bash
docker start rabbitmq
```

### QR Code não aparece
Aguarde 10-15 segundos. O Puppeteer precisa inicializar o Chromium.

### WhatsApp desconecta
Verifique se o celular está com internet e o WhatsApp aberto.

## 📊 Monitoramento

- **RabbitMQ**: http://localhost:15672
- **WebSocket**: ws://localhost:3001
- **Logs**: Console com emojis

## 🎯 Próximos Passos

1. Implementar FastAPI AI Agents (consumir `whatsapp_messages`)
2. Integrar Gemini Flash + Pro
3. Adicionar Redis Cache
4. Criar agentes especializados (Vendedor, Suporte, Marketing)

## 📝 Estrutura de Mensagens

### Entrada (WhatsApp → RabbitMQ)
```json
{
  "id": "msg_id",
  "from": "5511999999999@c.us",
  "body": "Olá",
  "contact": {
    "name": "João Silva",
    "number": "5511999999999"
  }
}
```

### Saída (RabbitMQ → WhatsApp)
```json
{
  "to": "5511999999999@c.us",
  "text": "Resposta do AI Agent",
  "typing": 3000
}
```

## ✅ Checklist

- [ ] RabbitMQ rodando
- [ ] Dependências instaladas (`npm install`)
- [ ] Gateway iniciado (`npm start`)
- [ ] QR Code escaneado
- [ ] WhatsApp conectado
- [ ] Mensagem de teste recebida
- [ ] Resposta manual enviada

Tudo funcionando? Agora você pode integrar com os AI Agents! 🎉
