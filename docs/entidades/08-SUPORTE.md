# 08 - Contexto: Suporte e Garantias

> **Linguagem Ubíqua:** Ticket, Garantia, Atendimento, Solução, SLA, Prioridade

**Fase:** 3

---

## Entidades

### Ticket (Aggregate Root)

| Atributo | Tipo | Obrigatório | Descrição |
|----------|------|-------------|-----------|
| `id` | UUID | ✅ | Identificador único |
| `numero` | String | ✅ | Ex: TKT-2026-0001 |
| `cliente` | ClienteId | ✅ | FK para Cliente |
| `contrato` | ContratoId | ❌ | FK para Contrato (se aplicável) |
| `tipo` | TipoTicket | ✅ | Garantia, Dúvida, Suporte técnico |
| `prioridade` | Prioridade | ✅ | Baixa, Média, Alta, Urgente |
| `status` | StatusTicket | ✅ | Aberto, Em andamento, Resolvido |
| `titulo` | String | ✅ | Resumo do problema |
| `descricao` | String | ✅ | Descrição detalhada |
| `solucao` | String | ❌ | Descrição da solução |
| `dataAbertura` | DateTime | ✅ | Data de abertura |
| `dataResolucao` | DateTime | ❌ | Data de resolução |
| `atendente` | UsuarioId | ❌ | Responsável |
| `linkAcompanhamento` | String | 🔄 Calculado | URL única para cliente |
| `interacoes` | List\<Interacao\> | ✅ | Histórico de mensagens |

### InteracaoTicket (Entity)

| Atributo | Tipo | Obrigatório | Descrição |
|----------|------|-------------|-----------|
| `id` | UUID | ✅ | Identificador único |
| `tipo` | TipoInteracao | ✅ | Mensagem cliente, Resposta, Nota interna |
| `mensagem` | String | ✅ | Conteúdo |
| `autor` | String | ✅ | Nome de quem escreveu |
| `dataHora` | DateTime | ✅ | Data e hora |

---

## Enums

```typescript
enum TipoTicket {
  GARANTIA = 'GARANTIA',
  DUVIDA = 'DUVIDA',
  SUPORTE_TECNICO = 'SUPORTE_TECNICO',
  RECLAMACAO = 'RECLAMACAO',
  OUTRO = 'OUTRO'
}

enum StatusTicket {
  ABERTO = 'ABERTO',
  EM_ANDAMENTO = 'EM_ANDAMENTO',
  AGUARDANDO_CLIENTE = 'AGUARDANDO_CLIENTE',
  RESOLVIDO = 'RESOLVIDO',
  FECHADO = 'FECHADO'
}

enum Prioridade {
  BAIXA = 'BAIXA',
  MEDIA = 'MEDIA',
  ALTA = 'ALTA',
  URGENTE = 'URGENTE'
}
```

---

## Link de Acompanhamento

O cliente recebe um link único e criptografado para acompanhar o ticket:

```
https://sunwops.com.br/garantia/{token}

Token = base64(encrypt(ticketId + clienteId + timestamp))
```

**Funcionalidades do link:**
- Ver status atual
- Ver histórico de interações
- Adicionar comentários
- Não requer login

---

## Regras de Negócio

| ID | Regra |
|----|-------|
| RN-SUP-01 | Ticket de garantia só pode ser aberto se contrato dentro da validade |
| RN-SUP-02 | Link de acompanhamento é único por ticket |
| RN-SUP-03 | Atendimento humanizado (ver requisitos de comunicação) |
| RN-SUP-04 | Usar analogias para pessoas leigas e idosas |
