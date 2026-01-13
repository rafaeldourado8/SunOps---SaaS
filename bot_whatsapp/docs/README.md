# 🤖 SunOps WhatsApp Gateway

Gateway Node.js para integração WhatsApp com Agentes AI usando arquitetura de filas.

## 🏗️ Arquitetura

```
WhatsApp → Node.js Gateway → RabbitMQ → FastAPI AI Agents → Redis Cache → Gemini AI
                ↓                                    ↓
            WebSocket                          RabbitMQ (responses)
                ↓                                    ↓
            Frontend                          Node.js Gateway → WhatsApp
```

## 🚀 Funcionalidades

- ✅ **QR Code**: Terminal + WebSocket para frontend
- ✅ **RabbitMQ**: Fila `whatsapp_messages` (entrada) e `whatsapp_responses` (saída)
- ✅ **Typing Indicator**: Simula digitação antes de enviar resposta
- ✅ **Áudio**: Suporte para mensagens de voz (PTT)
- ✅ **Reconexão Automática**: Retry em caso de falha no RabbitMQ
- ✅ **Graceful Shutdown**: Encerramento limpo com SIGINT

## 📦 Instalação

```bash
npm install
```

## ⚙️ Configuração

Copie `.env.example` para `.env`:

```bash
cp .env.example .env
```

Variáveis disponíveis:

```env
RABBITMQ_URL=amqp://guest:guest@localhost:5672
RABBITMQ_QUEUE=whatsapp_messages
WS_PORT=3001
WHATSAPP_SESSION_NAME=sunops-session
```

## 🎯 Uso

### Desenvolvimento
```bash
npm run dev
```

### Produção
```bash
npm start
```

## 📡 WebSocket Events

O gateway emite os seguintes eventos via WebSocket:

- `qr`: QR Code para autenticação (string)
- `authenticated`: WhatsApp autenticado
- `ready`: WhatsApp conectado e pronto
- `auth_failure`: Falha na autenticação
- `disconnected`: WhatsApp desconectado

### Exemplo Frontend

```javascript
const ws = new WebSocket('ws://localhost:3001');

ws.onmessage = (event) => {
  const { event: eventName, data } = JSON.parse(event.data);
  
  if (eventName === 'qr') {
    // Renderizar QR Code: data contém a string do QR
    QRCode.toCanvas(canvas, data);
  }
  
  if (eventName === 'ready') {
    console.log('WhatsApp conectado!');
  }
};
```

## 📨 Formato de Mensagens

### Entrada (WhatsApp → RabbitMQ)

```json
{
  "id": "msg_id",
  "from": "5511999999999@c.us",
  "to": "5511888888888@c.us",
  "body": "Olá, preciso de um orçamento",
  "timestamp": 1234567890,
  "hasMedia": false,
  "type": "chat",
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
  "text": "Olá! Vou te ajudar com o orçamento...",
  "typing": 3000
}
```

## 🔧 Estrutura do Projeto

```
src/
├── config/
│   └── index.js          # Configurações (env vars)
├── services/
│   ├── rabbitmq.js       # Publicação de mensagens
│   ├── websocket.js      # Broadcast de eventos
│   └── whatsapp.js       # Cliente WhatsApp
├── handlers/
│   ├── message.js        # Processa mensagens recebidas
│   └── response.js       # Consome respostas e envia
└── index.js              # Entry point
```

## 🐳 Docker

Para rodar com Docker Compose (junto com RabbitMQ):

```yaml
whatsapp-gateway:
  build: ./bot_whatsapp
  environment:
    - RABBITMQ_URL=amqp://guest:guest@rabbitmq:5672
  depends_on:
    - rabbitmq
  ports:
    - "3001:3001"
```

## 📊 Monitoramento

- **RabbitMQ Management**: http://localhost:15672 (guest/guest)
- **WebSocket**: ws://localhost:3001
- **Logs**: Console com emojis para fácil identificação

## 🔐 Segurança

- Sessão WhatsApp armazenada localmente (`.wwebjs_auth`)
- Credenciais RabbitMQ via variáveis de ambiente
- Sem exposição de tokens ou senhas no código

## 🤝 Integração com FastAPI

O FastAPI deve consumir a fila `whatsapp_messages` e publicar respostas em `whatsapp_responses`.

Exemplo Python:

```python
import pika
import json

# Consumir mensagens
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='whatsapp_messages', durable=True)

def callback(ch, method, properties, body):
    message = json.loads(body)
    # Processar com AI Agent
    response = process_with_ai(message)
    
    # Publicar resposta
    channel.basic_publish(
        exchange='',
        routing_key='whatsapp_responses',
        body=json.dumps(response)
    )

channel.basic_consume(queue='whatsapp_messages', on_message_callback=callback)
channel.start_consuming()
```

## 📝 Licença

MIT
