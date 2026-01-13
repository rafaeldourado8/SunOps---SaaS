# 📚 Exemplos de Integração

Esta pasta contém exemplos práticos de como integrar com o SunOps WhatsApp Gateway.

## 🎨 Frontend - QR Code Display

**Arquivo**: `qrcode-frontend.html`

Interface web para exibir o QR Code do WhatsApp em tempo real via WebSocket.

### Como usar:

1. Inicie o gateway:
```bash
npm start
```

2. Abra o arquivo HTML no navegador:
```bash
# Windows
start qrcode-frontend.html

# Linux/Mac
open qrcode-frontend.html
```

3. O QR Code aparecerá automaticamente
4. Escaneie com seu WhatsApp

### Recursos:
- ✅ QR Code renderizado com qrcode.js
- ✅ Status em tempo real (conectando, autenticado, pronto)
- ✅ Design responsivo e moderno
- ✅ Reconexão automática

---

## 🐍 Backend - Consumidor Python

**Arquivo**: `consumer-example.py`

Exemplo de consumidor Python que processa mensagens do WhatsApp e envia respostas automáticas.

### Como usar:

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

2. Inicie o RabbitMQ:
```bash
docker run -d -p 5672:5672 -p 15672:15672 rabbitmq:3-management
```

3. Inicie o gateway Node.js:
```bash
npm start
```

4. Execute o consumidor Python:
```bash
python consumer-example.py
```

5. Envie uma mensagem para o WhatsApp conectado

### Fluxo:
```
WhatsApp → Gateway Node.js → RabbitMQ (whatsapp_messages)
                                        ↓
                                  Python Consumer
                                        ↓
                              RabbitMQ (whatsapp_responses)
                                        ↓
                              Gateway Node.js → WhatsApp
```

### Recursos:
- ✅ Consumo de mensagens com confirmação (ACK)
- ✅ Processamento assíncrono
- ✅ Simulação de "digitando..." (typing indicator)
- ✅ Tratamento de erros com requeue
- ✅ QoS configurado (1 mensagem por vez)

---

## 🔧 Adaptando para FastAPI

Para integrar com FastAPI AI Agents, substitua a função `process_message()` por:

```python
async def process_message(message_data):
    # 1. Extrair intent com Gemini Flash
    intent = await extract_intent_with_flash(message_data['body'])
    
    # 2. Verificar cache Redis
    cached_response = await redis.get(f"response:{intent}")
    if cached_response:
        return json.loads(cached_response)
    
    # 3. Processar com Gemini Pro
    response_text = await generate_response_with_pro(intent, message_data)
    
    # 4. Salvar no cache
    await redis.setex(f"response:{intent}", 3600, json.dumps(response_text))
    
    return {
        'to': message_data['from'],
        'text': response_text,
        'typing': 3000
    }
```

---

## 📊 Monitoramento

Enquanto os exemplos estão rodando, você pode monitorar:

- **RabbitMQ Management**: http://localhost:15672 (guest/guest)
  - Ver mensagens nas filas
  - Monitorar taxa de processamento
  - Verificar consumidores ativos

- **WebSocket**: ws://localhost:3001
  - Eventos em tempo real
  - Status da conexão WhatsApp

---

## 🎯 Próximos Passos

1. Adaptar `consumer-example.py` para FastAPI
2. Integrar Gemini Flash + Pro
3. Adicionar Redis Cache
4. Implementar agentes especializados (Vendedor, Suporte, Marketing)
5. Adicionar suporte a áudio (Whisper)

---

## 💡 Dicas

- Use `nodemon` para desenvolvimento: `npm run dev`
- Monitore logs do gateway para debug
- Teste com múltiplos usuários simultâneos
- Configure QoS no RabbitMQ para controlar carga
- Use filas separadas para diferentes tipos de agentes

---

## 🐛 Troubleshooting

### Frontend não conecta
- Verifique se o gateway está rodando (`npm start`)
- Confirme a porta WebSocket (padrão: 3001)
- Verifique o console do navegador para erros

### Python não recebe mensagens
- Confirme que o RabbitMQ está rodando
- Verifique se o gateway publicou a mensagem (logs)
- Acesse RabbitMQ Management para ver a fila

### Mensagens não chegam no WhatsApp
- Verifique se o WhatsApp está conectado (QR Code escaneado)
- Confirme que a resposta foi publicada em `whatsapp_responses`
- Verifique logs do gateway para erros de envio
