# 11 - Contexto: Marketing

> **Linguagem Ubíqua:** Campanha, Lead, Automação, Sequência

**Fase:** 4 (Básico)

---

## Entidades

### Campanha (Entity)

| Atributo | Tipo | Obrigatório | Descrição |
|----------|------|-------------|-----------|
| `id` | UUID | ✅ | Identificador único |
| `nome` | String | ✅ | Nome da campanha |
| `tipo` | TipoCampanha | ✅ | Email, WhatsApp, SMS |
| `status` | StatusCampanha | ✅ | Rascunho, Ativa, Pausada, Finalizada |
| `publicoAlvo` | FiltroPublico | ❌ | Critérios de segmentação |
| `dataInicio` | DateTime | ❌ | Início programado |
| `dataFim` | DateTime | ❌ | Fim programado |
| `metrica` | MetricaCampanha | 🔄 Calculado | Resultados |

---

## Enums

```typescript
enum TipoCampanha {
  EMAIL = 'EMAIL',
  WHATSAPP = 'WHATSAPP',
  SMS = 'SMS'
}

enum StatusCampanha {
  RASCUNHO = 'RASCUNHO',
  ATIVA = 'ATIVA',
  PAUSADA = 'PAUSADA',
  FINALIZADA = 'FINALIZADA'
}
```

---

## Escopo Fase 4 (Básico)

- Relatório de ocorrências de marketing
- Configuração básica do Agente de Marketing
- Campanhas simples de WhatsApp

**Nota:** Funcionalidades avançadas de automação e sequências ficam para versões futuras.
