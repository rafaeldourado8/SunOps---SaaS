# Sistema de Estado do Usuário

## 📊 Visão Geral

Sistema para salvar preferências, filtros e configurações personalizadas por usuário usando JSONB no PostgreSQL.

## 🗄️ Estrutura

### Tabela: `usuario_estado`
- `id` - UUID
- `usuario_id` - FK para usuarios
- `chave` - String (ex: "pref:tema", "filtro:clientes")
- `valor` - JSONB (qualquer estrutura JSON)
- `updated_at` - Timestamp

## 🔌 Endpoints

### Preferências
```bash
# Salvar preferência
POST /usuarios/estado/preferencia
{
  "chave": "tema",
  "valor": "dark"
}

# Obter preferência
GET /usuarios/estado/preferencia/tema
```

### Filtros de Tela
```bash
# Salvar filtros
POST /usuarios/estado/filtro/clientes
{
  "status": "PROSPECT",
  "data_inicio": "2024-01-01"
}

# Obter filtros
GET /usuarios/estado/filtro/clientes
```

### Dashboard
```bash
# Salvar configuração
POST /usuarios/estado/dashboard
{
  "widgets": ["vendas", "propostas"],
  "layout": "grid"
}

# Obter configuração
GET /usuarios/estado/dashboard
```

### Todos os Estados
```bash
# Listar tudo
GET /usuarios/estado/todos

# Limpar tudo
DELETE /usuarios/estado/limpar
```

## 💡 Casos de Uso

### 1. Preferências do Usuário
```python
# Tema, idioma, notificações
use_case.salvar_preferencia(user_id, "tema", "dark")
use_case.salvar_preferencia(user_id, "idioma", "pt-BR")
use_case.salvar_preferencia(user_id, "notificacoes", True)
```

### 2. Filtros Salvos
```python
# Salvar filtros aplicados em cada tela
filtros = {
    "status": ["PROSPECT", "LEAD"],
    "data_inicio": "2024-01-01",
    "ordenacao": "nome"
}
use_case.salvar_filtro(user_id, "clientes", filtros)
```

### 3. Configuração de Dashboard
```python
# Layout personalizado
config = {
    "widgets": ["vendas", "propostas", "contratos"],
    "layout": "grid",
    "refresh_interval": 30
}
use_case.salvar_dashboard(user_id, config)
```

### 4. Estado de Tela
```python
# Posição de scroll, abas abertas, etc
estado = {
    "scroll_position": 1200,
    "aba_ativa": "detalhes",
    "sidebar_aberta": True
}
use_case.salvar_estado_tela(user_id, "proposta_detalhes", estado)
```

## 🎯 Exemplos Frontend

### React
```javascript
// Salvar tema
await api.post('/usuarios/estado/preferencia', {
  chave: 'tema',
  valor: 'dark'
});

// Obter tema
const { valor } = await api.get('/usuarios/estado/preferencia/tema');
setTema(valor);

// Salvar filtros
await api.post('/usuarios/estado/filtro/clientes', {
  status: 'PROSPECT',
  ordenacao: 'nome'
});

// Obter filtros
const { filtros } = await api.get('/usuarios/estado/filtro/clientes');
setFiltros(filtros);
```

## 🔐 Segurança

- Todos os endpoints requerem autenticação JWT
- Cada usuário só acessa seus próprios estados
- Cascade delete: estados são removidos ao deletar usuário

## 📈 Performance

- Índices em `usuario_id` e `chave`
- JSONB permite queries eficientes
- Constraint única em `(usuario_id, chave)`
