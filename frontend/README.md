# SunOPS Frontend

## ✅ Features Implementadas

- ✅ Login com autenticação JWT
- ✅ Dashboard com estatísticas
- ✅ CRUD Clientes (criar, editar, excluir, promover)
- ✅ CRUD Propostas (criar, visualizar, gerar PDF)
- ✅ CRUD Premissas (criar, editar, excluir)
- ✅ Upload de Templates PDF
- ✅ Configurações globais
- ✅ Timeout de sessão (4 minutos)
- ✅ Toast notifications
- ✅ Design dark theme com gradiente solar

## 📦 Estrutura

```
frontend/
├── src/
│   ├── components/
│   │   ├── Layout.jsx
│   │   ├── ProtectedRoute.jsx
│   │   └── Sidebar.jsx
│   ├── pages/
│   │   ├── LoginPage.jsx
│   │   ├── DashboardPage.jsx
│   │   ├── ClientesPage.jsx
│   │   ├── PropostasPage.jsx
│   │   ├── PremissasPage.jsx
│   │   ├── TemplatesPage.jsx
│   │   └── ConfiguracoesPage.jsx
│   ├── services/
│   │   └── api.js
│   ├── store/
│   │   └── authStore.js
│   ├── App.jsx
│   ├── main.jsx
│   └── index.css
├── .env
├── package.json
├── tailwind.config.js
└── vite.config.js
```

## 🚀 Como Rodar

### Desenvolvimento Local
```bash
cd frontend
npm install
npm run dev
```

### Build para Produção
```bash
npm run build
```

### Com Docker
```bash
docker-compose build frontend
docker-compose up -d frontend
```

## 🔌 Endpoints Configurados

- `/api/auth/login` - Login
- `/api/clientes/` - CRUD Clientes
- `/api/propostas/` - CRUD Propostas
- `/api/premissas/` - CRUD Premissas
- `/api/templates/` - Upload Templates

## 🎨 Design System

- **Cores**: Solar (#f59e0b) + Dark (#0f172a)
- **Componentes**: Glassmorphism cards
- **Ícones**: React Icons
- **Notificações**: React Hot Toast

## 🔐 Credenciais Padrão

- **Admin**: admin@sunops.com / admin123
- **Gestor**: gestor@sunops.com / gestor123
- **Vendedor**: vendedor@sunops.com / vendedor123
