# 🌞 SunOps Frontend

Interface visual para gerenciamento de agentes IA e workflows do SunOps.

## 🚀 Quick Start

```bash
# Instalar dependências
pnpm install

# Copiar .env
cp .env.example .env

# Iniciar dev server
pnpm dev
```

Acesse: http://localhost:5173

## 🎨 Features

- **Workflow Canvas**: Editor visual de fluxos (ReactFlow)
- **Dashboard**: Métricas em tempo real
- **Node Palette**: Componentes drag-and-drop
- **Config Panel**: Configuração de agentes IA
- **WebSocket**: Conexão em tempo real com WhatsApp Gateway

## 📦 Stack

- React 18 + TypeScript
- Vite
- TailwindCSS
- ReactFlow (workflow editor)
- Zustand (state management)
- Lucide Icons

## 🔌 API Integration

O frontend se conecta com:
- **FastAPI Backend**: `http://localhost:8000/api/v1`
- **WhatsApp Gateway**: `ws://localhost:3001`

## 📁 Estrutura

```
src/
├── components/
│   ├── Canvas/          # Workflow editor
│   ├── Dashboard/       # Métricas
│   └── Sidebar/         # Paleta e config
├── hooks/
│   └── useApi.ts        # React hooks para API
├── lib/
│   ├── api.ts           # Cliente HTTP
│   └── websocket.ts     # Cliente WebSocket
├── stores/
│   └── canvasStore.ts   # Estado global
└── types/
    └── index.ts         # TypeScript types
```

## 🎯 Próximos Passos

- [ ] Drag-and-drop funcional
- [ ] Salvar workflows no backend
- [ ] Métricas em tempo real via WebSocket
- [ ] Histórico de conversas
- [ ] Editor de prompts
- [ ] Testes de agentes
