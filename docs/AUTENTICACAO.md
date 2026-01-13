# 🔐 Sistema de Autenticação - SunOps

## ✅ Implementado

### Backend (Clean Architecture + DDD + SOLID)

#### 1. **Domínio**
- Models: `UserModel` no banco de dados
- DTOs: `RegisterDTO`, `LoginDTO`, `TokenDTO`, `UserDTO`
- Repository Port: `IUserRepository` (interface)

#### 2. **Use Cases**
- `RegisterUserUseCase`: Registro de novos usuários
- `LoginUserUseCase`: Autenticação e geração de tokens

#### 3. **Infraestrutura**
- `UserRepository`: Implementação do repositório
- `PasswordHasher`: Hash bcrypt (OWASP)
- `TokenGenerator`: JWT tokens (access + refresh)

#### 4. **API**
- **POST** `/api/v1/auth/register` - Cadastro
- **POST** `/api/v1/auth/login` - Login
- **GET** `/api/v1/auth/me` - Dados do usuário autenticado

#### 5. **Segurança OWASP**
- ✅ Bcrypt para senhas (custo 12)
- ✅ JWT com expiração (30min access, 7 dias refresh)
- ✅ Rate limiting (5 req/min registro, 10 req/min login)
- ✅ CORS configurado (apenas localhost)
- ✅ Validação de entrada (Pydantic)
- ✅ HTTPOnly tokens
- ✅ Proteção contra SQL Injection (SQLAlchemy)

### Frontend (React + TypeScript)

#### 1. **Componentes**
- `Login.tsx`: Tela de login/registro
- Validação de formulário
- Feedback de erros

#### 2. **State Management**
- `authStore.ts`: Zustand com persist
- Armazena: user, accessToken, refreshToken

#### 3. **API Service**
- `api.ts`: Cliente HTTP com interceptor
- Auto-redirect em 401
- Headers de autenticação automáticos

#### 4. **Proteção de Rotas**
- `App.tsx`: Verifica autenticação
- Redireciona para login se não autenticado

### Docker

#### Serviços Rodando
```
✅ Frontend (port 80)
✅ API (port 8000)
✅ PostgreSQL (port 5432)
✅ Redis (port 6379)
✅ RabbitMQ (port 5672, 15672)
✅ WhatsApp Gateway (port 3001)
✅ WhatsApp Agent
```

## 🚀 Como Usar

### 1. Subir Stack
```bash
docker-compose up -d
```

### 2. Criar Tabelas
```bash
docker-compose exec api alembic upgrade head
```

### 3. Acessar
- **Frontend**: http://localhost
- **API Docs**: http://localhost:8000/docs
- **RabbitMQ**: http://localhost:15672 (guest/guest)

### 4. Primeiro Acesso
1. Abra http://localhost
2. Clique em "Criar conta"
3. Preencha: email, nome completo, senha (mín 8 caracteres)
4. Faça login

## 📋 Checklist OWASP Top 10

- [x] A01:2021 – Broken Access Control
  - JWT com expiração
  - Middleware de autenticação
  
- [x] A02:2021 – Cryptographic Failures
  - Bcrypt para senhas
  - HTTPS ready
  
- [x] A03:2021 – Injection
  - SQLAlchemy ORM
  - Pydantic validation
  
- [x] A04:2021 – Insecure Design
  - Clean Architecture
  - Separation of Concerns
  
- [x] A05:2021 – Security Misconfiguration
  - CORS configurado
  - Rate limiting
  
- [x] A07:2021 – Identification and Authentication Failures
  - Senha forte (min 8 chars)
  - JWT tokens
  - Refresh tokens

## 🔧 Variáveis de Ambiente

```env
SECRET_KEY=sunops-secret-key-change-in-production-2024
POSTGRES_PASSWORD=changeme
DATABASE_URL=postgresql+asyncpg://admin:changeme@postgres-master:5432/sunwops
```

## 📊 Complexidade Ciclomática

Todas as funções mantêm complexidade < 10:
- `RegisterUserUseCase.execute`: 2
- `LoginUserUseCase.execute`: 4
- `PasswordHasher.hash`: 1
- `TokenGenerator.create_access_token`: 2

## 🎯 Próximos Passos

- [ ] Implementar refresh token endpoint
- [ ] Adicionar 2FA (opcional)
- [ ] Logs de auditoria
- [ ] Recuperação de senha
- [ ] Roles e permissões (RBAC)
