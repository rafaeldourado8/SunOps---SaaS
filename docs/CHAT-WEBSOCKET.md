# 💬 Sistema de Chat WebSocket - Admin ↔ Vendedor

## ✅ Implementado

Sistema completo de comunicação em tempo real entre admin e vendedor usando WebSocket.

---

## 🎯 FUNCIONALIDADES

✅ Chat em tempo real (WebSocket)  
✅ Múltiplas conversas simultâneas  
✅ Status de mensagens (ENVIADA, ENTREGUE, LIDA)  
✅ Tipos de remetente (ADMIN, VENDEDOR, IA)  
✅ Gestão de conversas (ABERTA, EM_ATENDIMENTO, RESOLVIDA)  
✅ Salas de chat (rooms)  
✅ API REST para histórico

---

## 📐 ARQUITETURA

```
shared/
├── domain/
│   └── entities/
│       └── chat.py              # Conversa, Mensagem, Enums
└── infrastructure/
    └── websocket/
        ├── connection_manager.py # Gerencia conexões WS
        └── chat_service.py       # Lógica de negócio

fastapi_app/
├── routers/
│   └── chat.py                  # Endpoints WS + REST
└── static/
    └── chat.html                # Cliente de teste
```

---

## 🔌 WEBSOCKET ENDPOINT

### Conectar

```javascript
const ws = new WebSocket('ws://localhost:8001/ws/chat/{user_id}');

ws.onopen = () => {
    console.log('Conectado!');
};

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log('Mensagem recebida:', data);
};
```

### Ações Disponíveis

#### 1. Criar Conversa

```javascript
ws.send(JSON.stringify({
    action: 'create_conversa',
    assunto: 'Solicitação de orçamento especial'
}));

// Resposta:
{
    type: 'conversa_created',
    conversa_id: 'uuid',
    assunto: 'Solicitação de orçamento especial'
}
```

#### 2. Entrar na Sala

```javascript
ws.send(JSON.stringify({
    action: 'join_room',
    conversa_id: 'conv-123'
}));

// Resposta:
{
    type: 'system',
    message: 'Conectado à conversa conv-123'
}
```

#### 3. Enviar Mensagem

```javascript
ws.send(JSON.stringify({
    action: 'send_message',
    conversa_id: 'conv-123',
    conteudo: 'Preciso de um orçamento para 500 kWh/mês',
    tipo_remetente: 'VENDEDOR'  // ou 'ADMIN' ou 'IA'
}));

// Broadcast para todos na sala:
{
    type: 'message',
    mensagem_id: 'uuid',
    conversa_id: 'conv-123',
    remetente_id: 'user-1',
    tipo_remetente: 'VENDEDOR',
    conteudo: 'Preciso de um orçamento para 500 kWh/mês',
    timestamp: '2024-01-15T10:30:00'
}
```

#### 4. Marcar como Lida

```javascript
ws.send(JSON.stringify({
    action: 'mark_read',
    conversa_id: 'conv-123',
    mensagem_id: 'msg-456'
}));
```

---

## 🌐 API REST

### Listar Conversas

**Vendedor:**
```bash
GET /api/chat/conversas?user_id=vend-1&tipo=vendedor
```

**Admin:**
```bash
GET /api/chat/conversas?user_id=admin-1&tipo=admin
```

**Resposta:**
```json
{
    "conversas": [
        {
            "id": "conv-123",
            "vendedor_id": "vend-1",
            "admin_id": "admin-1",
            "assunto": "Solicitação de orçamento",
            "status": "EM_ATENDIMENTO",
            "mensagens_nao_lidas": 2,
            "criada_em": "2024-01-15T10:00:00",
            "atualizada_em": "2024-01-15T10:30:00"
        }
    ]
}
```

### Listar Mensagens

```bash
GET /api/chat/conversas/{conversa_id}/mensagens
```

**Resposta:**
```json
{
    "conversa_id": "conv-123",
    "mensagens": [
        {
            "id": "msg-1",
            "remetente_id": "vend-1",
            "tipo_remetente": "VENDEDOR",
            "conteudo": "Preciso de ajuda",
            "timestamp": "2024-01-15T10:00:00",
            "status": "LIDA"
        },
        {
            "id": "msg-2",
            "remetente_id": "admin-1",
            "tipo_remetente": "ADMIN",
            "conteudo": "Como posso ajudar?",
            "timestamp": "2024-01-15T10:05:00",
            "status": "LIDA"
        }
    ]
}
```

### Atribuir Admin

```bash
POST /api/chat/conversas/{conversa_id}/atribuir
{
    "admin_id": "admin-1"
}
```

**Resposta:**
```json
{
    "success": true
}
```

**Broadcast para sala:**
```json
{
    "type": "admin_assigned",
    "conversa_id": "conv-123",
    "admin_id": "admin-1"
}
```

---

## 📊 ENTITIES

### Mensagem

```python
@dataclass
class Mensagem:
    id: str
    conversa_id: str
    remetente_id: str
    tipo_remetente: TipoRemetente  # ADMIN, VENDEDOR, IA
    conteudo: str
    timestamp: datetime
    status: StatusMensagem  # ENVIADA, ENTREGUE, LIDA
    metadata: Optional[dict] = None
```

### Conversa

```python
@dataclass
class Conversa:
    id: str
    vendedor_id: str
    admin_id: Optional[str] = None
    assunto: str = "Solicitação de orçamento"
    status: StatusConversa  # ABERTA, EM_ATENDIMENTO, RESOLVIDA, FECHADA
    mensagens: List[Mensagem]
    criada_em: datetime
    atualizada_em: datetime
    
    # Métodos
    def adicionar_mensagem(mensagem)
    def atribuir_admin(admin_id)
    def resolver()
    
    # Propriedades
    @property
    def mensagens_nao_lidas() -> int
```

---

## 🧪 TESTAR

### 1. Iniciar FastAPI

```bash
docker-compose up fastapi
```

### 2. Abrir Cliente de Teste

Abra 2 abas do navegador:

**Aba 1 (Vendedor):**
```
http://localhost:8001/static/chat.html
```
- User ID: `vendedor-1`
- Tipo: `VENDEDOR`
- Clique em "Conectar"
- Clique em "Criar Conversa"
- Clique em "Entrar na Sala"

**Aba 2 (Admin):**
```
http://localhost:8001/static/chat.html
```
- User ID: `admin-1`
- Tipo: `ADMIN`
- Clique em "Conectar"
- Use o mesmo Conversa ID da aba 1
- Clique em "Entrar na Sala"

### 3. Trocar Mensagens

Digite mensagens em ambas as abas e veja a comunicação em tempo real!

---

## 🔄 FLUXO COMPLETO

### Vendedor solicita ajuda

```
1. Vendedor → Conecta WebSocket
2. Vendedor → Cria conversa
3. Vendedor → Entra na sala
4. Vendedor → Envia mensagem: "Preciso de orçamento para 500 kWh"
```

### Admin responde

```
5. Admin → Conecta WebSocket
6. Admin → Lista conversas abertas (REST API)
7. Admin → Entra na sala da conversa
8. Sistema → Atribui admin à conversa
9. Admin → Envia mensagem: "Vou dimensionar o sistema"
```

### IA pode intervir (opcional)

```
10. Se admin não responder em 15 min
11. IA → Entra na sala
12. IA → Envia mensagem automática (tipo_remetente: IA)
13. Admin → Revisa depois
```

---

## 🎨 INTERFACE HTML

Cliente de teste inclui:

✅ Conexão WebSocket  
✅ Criar conversa  
✅ Entrar em sala  
✅ Enviar mensagens  
✅ Receber mensagens em tempo real  
✅ Alternar entre VENDEDOR/ADMIN  
✅ Visual diferenciado por tipo

---

## 🔐 SEGURANÇA (TODO)

Para produção, adicionar:

- [ ] Autenticação JWT no WebSocket
- [ ] Validação de permissões (vendedor só vê suas conversas)
- [ ] Rate limiting
- [ ] Sanitização de mensagens
- [ ] Criptografia end-to-end (opcional)

---

## 📈 PRÓXIMOS PASSOS

1. **Persistência:**
   - Salvar conversas no PostgreSQL
   - Salvar mensagens no PostgreSQL
   - Histórico completo

2. **Notificações:**
   - Push notifications
   - Email quando admin não responde
   - Badge de mensagens não lidas

3. **Features:**
   - Anexar arquivos
   - Enviar imagens
   - Áudio/vídeo
   - Typing indicator
   - Online/offline status

4. **Integração:**
   - Conectar com SSE para notificar admin
   - Conectar com IA fallback
   - Conectar com motor de orçamento

---

## 🚀 ENDPOINTS DISPONÍVEIS

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| WS | `/ws/chat/{user_id}` | WebSocket principal |
| GET | `/api/chat/conversas` | Lista conversas |
| GET | `/api/chat/conversas/{id}/mensagens` | Lista mensagens |
| POST | `/api/chat/conversas/{id}/atribuir` | Atribui admin |
| GET | `/static/chat.html` | Cliente de teste |

---

## ✅ STATUS

**Implementado:** Sistema completo de chat WebSocket funcional  
**Testado:** Cliente HTML funcionando  
**Pronto para:** Integração com frontend React/Vue  
**Falta:** Persistência em banco de dados

---

## 📝 EXEMPLO DE USO

```python
# Backend - Enviar mensagem via código
from shared.infrastructure.websocket.chat_service import chat_service
from shared.infrastructure.websocket.connection_manager import manager
from shared.domain.entities.chat import TipoRemetente

# Criar conversa
conversa = chat_service.criar_conversa(
    vendedor_id="vend-1",
    assunto="Orçamento urgente"
)

# Enviar mensagem
mensagem = chat_service.enviar_mensagem(
    conversa_id=conversa.id,
    remetente_id="admin-1",
    tipo_remetente=TipoRemetente.ADMIN,
    conteudo="Vou preparar o orçamento"
)

# Broadcast para sala
await manager.broadcast_to_room({
    "type": "message",
    "conteudo": mensagem.conteudo,
    "tipo_remetente": "ADMIN"
}, conversa.id)
```

---

**🎉 Chat WebSocket Admin ↔ Vendedor implementado com sucesso!**
