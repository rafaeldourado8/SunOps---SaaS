# 🎨 Agente de Vendas - Frontend

## ✅ Implementado

### ConfigPanel Atualizado
- **Seleção de Modelo IA**: Gemini Flash, Gemini Pro, GPT-4
- **Prompt Customizável**: Editor de prompt do sistema
- **Regras de Negócio**: Adicionar/remover regras dinamicamente
- **Métricas em Tempo Real**: 
  - Total de conversas
  - Conversas ativas
  - Orçamentos gerados
  - Taxa de conversão

### Integração com API
- `GET /api/v1/agents/vendas/metrics`: Busca métricas
- `POST /api/v1/agents/vendas/config`: Salva configuração
- `POST /api/v1/agents/vendas/message`: Envia mensagem (teste)

### Node "Bot de Vendas"
- Já existe no canvas inicial
- Clique no node para abrir ConfigPanel
- Configurações são salvas no backend

## 🧪 Como Testar

### 1. Testar no Canvas
```bash
# Abra o frontend
http://localhost

# 1. Clique no node "Bot de Vendas" no canvas
# 2. ConfigPanel abre à direita
# 3. Altere o modelo IA
# 4. Edite o prompt do sistema
# 5. Adicione/remova regras
# 6. Veja métricas em tempo real
# 7. Clique em "Salvar Alterações"
```

### 2. Página de Teste (Opcional)
Adicione rota no `App.tsx`:
```tsx
import { VendasAgentTestPage } from './components/Pages/VendasAgentTestPage';

// Adicione a rota:
<Route path="/test/vendas" element={<VendasAgentTestPage />} />
```

Acesse: `http://localhost/test/vendas`

## 📊 Features

### ConfigPanel
- ✅ Edição de nome do node
- ✅ Seleção de modelo IA (Gemini Flash/Pro, GPT-4)
- ✅ Editor de prompt do sistema
- ✅ Gerenciamento de regras (adicionar/remover)
- ✅ Métricas em tempo real
- ✅ Salvamento via API

### Métricas Exibidas
- **Total Conversas**: Número total de conversas
- **Conversas Ativas**: Conversas em andamento
- **Orçamentos Gerados**: Total de orçamentos criados
- **Taxa de Conversão**: Percentual de conversão

## 🔄 Fluxo de Uso

1. **Abrir Canvas**: Dashboard → Canvas
2. **Selecionar Node**: Clique em "Bot de Vendas"
3. **Configurar**: Altere modelo, prompt, regras
4. **Ver Métricas**: Métricas atualizam automaticamente
5. **Salvar**: Clique em "Salvar Alterações"

## 📝 Arquivos Modificados

- `ConfigPanel.tsx`: Integração com API, métricas, regras dinâmicas
- `canvasStore.ts`: Fix updateNode para atualizar data corretamente
- `api.ts`: Métodos genéricos get/post para agents
- `VendasAgentTestPage.tsx`: Página de teste (opcional)

## 🎯 Próximos Passos

1. Adicionar validação de campos obrigatórios
2. Implementar auto-refresh de métricas (polling/SSE)
3. Adicionar histórico de conversas no ConfigPanel
4. Implementar drag-and-drop de nodes da palette
5. Adicionar preview de resposta do agente
