# 13 - Eventos de Domínio

## O que são Eventos de Domínio?

Eventos representam **algo que aconteceu** no sistema e que outros contextos podem precisar saber.

```
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│  Contexto A │ ──────▶ │   EVENTO    │ ──────▶ │  Contexto B │
│  (publica)  │         │             │         │   (escuta)  │
└─────────────┘         └─────────────┘         └─────────────┘
```

---

## Eventos por Contexto

### Contexto: Cadastros

| Evento | Quando | Payload | Listeners |
|--------|--------|---------|-----------|
| `ClienteCriado` | Novo cliente | clienteId, nome, vendedorId | Dashboard |
| `ClienteAtualizado` | Dados alterados | clienteId, campos | - |
| `VendedorAtribuido` | Vendedor assumiu | clienteId, vendedorId | Dashboard |

---

### Contexto: Catálogo

| Evento | Quando | Payload | Listeners |
|--------|--------|---------|-----------|
| `ProdutoCadastrado` | Novo produto | produtoId, categoria, nome | - |
| `PrecoCotado` | Nova cotação | produtoId, fornecedorId, preco, validade | Dashboard |
| `PrecoExpirado` | Passou validade | produtoId, cotacaoId | Alerta |
| `AlertaCotacaoSegunda` | Segunda 8h | listaProdutosSemPreco | Notificação |

---

### Contexto: Orçamentos

| Evento | Quando | Payload | Listeners |
|--------|--------|---------|-----------|
| `KitCriado` | Novo kit | kitId, nome, valorTotal | Dashboard |
| `TemplateCriado` | Salvo como template | kitId, nome | - |
| `OrcamentoCriado` | Nova proposta | orcamentoId, clienteId, vendedorId, valor | Dashboard, Notificação |
| `OrcamentoAprovado` | Cliente aprovou | orcamentoId, dataAprovacao | **Vendas** (criar venda) |
| `OrcamentoRejeitado` | Cliente rejeitou | orcamentoId, motivo | Dashboard |
| `OrcamentoExpirado` | Passou validade | orcamentoId | Notificação |

---

### Contexto: Vendas

| Evento | Quando | Payload | Listeners |
|--------|--------|---------|-----------|
| `VendaAberta` | Nova venda | vendaId, clienteId, vendedorId, valor | Dashboard |
| `VendaMudouEtapa` | Moveu no funil | vendaId, etapaAnterior, etapaNova | Dashboard |
| `VendaFechada` | Status = FECHADA | vendaId, valorFinal, data | **Contratos** (criar contrato), Comissão |
| `VendaPerdida` | Status = PERDIDA | vendaId, motivoPerda | Dashboard, Relatório |

---

### Contexto: Contratos

| Evento | Quando | Payload | Listeners |
|--------|--------|---------|-----------|
| `ContratoCriado` | Novo contrato | contratoId, vendaId, valorTotal | Dashboard |
| `ContratoAssinado` | Cliente assinou | contratoId, dataAssinatura | - |
| `InstalacaoIniciada` | Começou | contratoId, integradorId | - |
| `InstalacaoConcluida` | Terminou | contratoId, dataInstalacao | **Suporte** (criar garantia), **Monitoramento** (criar planta) |
| `ParcelaPaga` | Pagamento | contratoId, parcelaId, valor | Dashboard |
| `ParcelaAtrasada` | Venceu | contratoId, parcelaId, diasAtraso | Notificação, Cobrança |
| `ContratoFinalizado` | Todas pagas | contratoId | Dashboard |

---

### Contexto: Suporte

| Evento | Quando | Payload | Listeners |
|--------|--------|---------|-----------|
| `TicketAberto` | Novo ticket | ticketId, clienteId, tipo | Dashboard, Notificação |
| `TicketAtribuido` | Atendente assumiu | ticketId, atendenteId | - |
| `TicketResolvido` | Solucionado | ticketId, solucao, dataResolucao | Dashboard |
| `GarantiaCriada` | Instalação concluída | garantiaId, contratoId, dataFim | - |

---

### Contexto: Monitoramento

| Evento | Quando | Payload | Listeners |
|--------|--------|---------|-----------|
| `PlantaCriada` | Nova planta | plantaId, contratoId, plataforma | - |
| `FalhaDetectada` | API erro | plantaId, tipoFalha, codigo | Timer 2 dias |
| `FalhaPersistente` | Após 2 dias | alertaId, plantaId | Preparar mensagem |
| `MensagemAprovada` | Admin aprovou | alertaId, mensagem | Enviar WhatsApp |
| `PlantaVoltouOnline` | Normalizado | plantaId, alertaId | Cancelar alerta |

---

### Contexto: Agentes IA

| Evento | Quando | Payload | Listeners |
|--------|--------|---------|-----------|
| `ConversaIniciada` | Primeira msg | conversaId, agenteId, plataforma | - |
| `MensagemRecebida` | Cliente enviou | conversaId, mensagem, tipo | IA processa |
| `TakeoverRealizado` | Humano assumiu | conversaId, atendenteId | - |
| `OrcamentoSolicitadoIA` | IA identificou interesse | conversaId, dadosCliente | **Orçamentos** |

---

## Fluxo de Eventos Críticos

### Orçamento → Venda → Contrato

```
OrcamentoAprovado
       │
       ▼
┌─────────────────┐
│  Criar Venda    │
│ (status=ABERTA) │
│ (etapa=PROPOSTA)│
└────────┬────────┘
         │
         ▼
    VendaAberta
         │
    (vendedor trabalha)
         │
         ▼
    VendaFechada
         │
         ▼
┌─────────────────┐
│ Criar Contrato  │
│ (AGUARD_ASSIN)  │
└────────┬────────┘
         │
         ▼
   ContratoCriado
```

### Instalação → Garantia + Monitoramento

```
InstalacaoConcluida
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌────────┐ ┌────────┐
│ Criar  │ │ Criar  │
│Garantia│ │ Planta │
│(Suporte│ │(Monitor│
└────────┘ └────────┘
```

### Falha → Notificação

```
FalhaDetectada
       │
       ▼
  Timer 2 dias
       │
       ▼
  Ainda offline?
       │
   ┌───┴───┐
   │       │
   ▼       ▼
  NÃO     SIM
   │       │
   ▼       ▼
Cancelar  FalhaPersistente
               │
               ▼
         Preparar mensagem
               │
               ▼
         Admin revisa
               │
               ▼
         MensagemAprovada
               │
               ▼
         Enviar WhatsApp
```

---

## Implementação Sugerida

```typescript
// Interface do evento
interface DomainEvent {
  eventId: string;
  eventType: string;
  occurredAt: Date;
  payload: any;
}

// Publicar evento
class EventBus {
  publish(event: DomainEvent): void {
    // Salvar no banco (outbox pattern)
    // Processar listeners
  }
}

// Listener
interface EventListener {
  eventType: string;
  handle(event: DomainEvent): Promise<void>;
}

// Exemplo: Criar venda quando orçamento aprovado
class CriarVendaQuandoOrcamentoAprovado implements EventListener {
  eventType = 'OrcamentoAprovado';
  
  async handle(event: DomainEvent): Promise<void> {
    const { orcamentoId, clienteId, vendedorId, valorTotal } = event.payload;
    
    const venda = new Venda({
      cliente: clienteId,
      vendedor: vendedorId,
      orcamento: orcamentoId,
      valorPrevisto: valorTotal,
      status: StatusVenda.ABERTA,
      etapaFunil: EtapaFunil.PROPOSTA
    });
    
    await vendaRepository.save(venda);
    await eventBus.publish(new VendaAberta(venda));
  }
}
```
