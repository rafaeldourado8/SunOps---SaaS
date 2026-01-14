# 07 - Contexto: Contratos

> **Linguagem Ubíqua:** Contrato, Parcela, Assinatura, Garantia, Instalação

**Fase:** 2

---

## Diagrama de Entidades

```
┌─────────────────────────────────────────────────────────────────┐
│                     CONTEXTO CONTRATOS                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────┐                                            │
│  │    CONTRATO     │                                            │
│  │ (Aggregate Root)│                                            │
│  └────────┬────────┘                                            │
│           │                                                      │
│           ▼                                                      │
│  ┌─────────────────┐                                            │
│  │    PARCELA      │                                            │
│  │   CONTRATO      │                                            │
│  │    (Entity)     │                                            │
│  └─────────────────┘                                            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Aggregate Root: Contrato

### Contrato (Aggregate Root)

| Atributo | Tipo | Obrigatório | Descrição |
|----------|------|-------------|-----------|
| `id` | UUID | ✅ | Identificador único |
| `numero` | String | ✅ | Número do contrato (ex: CTR-2026-0001) |
| `venda` | VendaId | ✅ | FK para Venda fechada |
| `cliente` | ClienteId | ✅ | FK para Cliente |
| `integrador` | IntegradorId | ❌ | FK para Integrador responsável |
| `valorTotal` | Decimal | ✅ | Valor total do contrato |
| `status` | StatusContrato | ✅ | Status atual |
| `dataEmissao` | Date | ✅ | Data de emissão |
| `dataAssinatura` | Date | ❌ | Data de assinatura |
| `dataPrevisaoInstalacao` | Date | ❌ | Previsão de instalação |
| `dataInstalacao` | Date | ❌ | Data efetiva de instalação |
| `garantiaMeses` | Integer | ✅ | Meses de garantia |
| `dataFimGarantia` | Date | 🔄 Calculado | dataInstalacao + garantiaMeses |
| `parcelas` | List\<ParcelaContrato\> | ✅ | Condições de pagamento |
| `observacoes` | String | ❌ | Observações gerais |

---

### ParcelaContrato (Entity)

| Atributo | Tipo | Obrigatório | Descrição |
|----------|------|-------------|-----------|
| `id` | UUID | ✅ | Identificador único |
| `contrato` | ContratoId | ✅ | FK para Contrato |
| `numeroParcela` | Integer | ✅ | Número da parcela (1, 2, 3...) |
| `valor` | Decimal | ✅ | Valor da parcela |
| `dataVencimento` | Date | ✅ | Data de vencimento |
| `dataPagamento` | Date | ❌ | Data de pagamento efetivo |
| `status` | StatusParcela | ✅ | Pendente, Paga, Atrasada |
| `comprovante` | String | ❌ | URL do comprovante |

---

## Enums

```typescript
enum StatusContrato {
  AGUARDANDO_ASSINATURA = 'AGUARDANDO_ASSINATURA',
  ASSINADO = 'ASSINADO',
  EM_EXECUCAO = 'EM_EXECUCAO',
  INSTALADO = 'INSTALADO',
  FINALIZADO = 'FINALIZADO',
  CANCELADO = 'CANCELADO'
}

enum StatusParcela {
  PENDENTE = 'PENDENTE',
  PAGA = 'PAGA',
  ATRASADA = 'ATRASADA',
  CANCELADA = 'CANCELADA'
}
```

---

## Fluxo de Status do Contrato

```
┌───────────────────┐
│    AGUARDANDO     │
│    ASSINATURA     │
└─────────┬─────────┘
          │
          │ Assinatura recebida
          ▼
┌───────────────────┐
│     ASSINADO      │
└─────────┬─────────┘
          │
          │ Instalação iniciada
          ▼
┌───────────────────┐
│   EM EXECUÇÃO     │
└─────────┬─────────┘
          │
          │ Instalação concluída
          ▼
┌───────────────────┐
│     INSTALADO     │
└─────────┬─────────┘
          │
          │ Todas parcelas pagas
          ▼
┌───────────────────┐
│    FINALIZADO     │
└───────────────────┘

        │
        │ A qualquer momento
        ▼
┌───────────────────┐
│    CANCELADO      │
└───────────────────┘
```

---

## Regras de Negócio

| ID | Regra |
|----|-------|
| RN-CTR-01 | Contrato só pode ser criado a partir de Venda FECHADA |
| RN-CTR-02 | Data fim garantia = Data instalação + garantia em meses |
| RN-CTR-03 | Parcela vira ATRASADA automaticamente após vencimento |
| RN-CTR-04 | Contrato só vai para FINALIZADO quando todas parcelas PAGAS |
| RN-CTR-05 | Cancelamento exige justificativa |

---

## Cálculo de Garantia

```typescript
function calcularFimGarantia(dataInstalacao: Date, garantiaMeses: number): Date {
  const dataFim = new Date(dataInstalacao);
  dataFim.setMonth(dataFim.getMonth() + garantiaMeses);
  return dataFim;
}

// Exemplo:
// Instalação: 15/01/2026
// Garantia: 60 meses (5 anos)
// Fim garantia: 15/01/2031
```

---

## Criação de Contrato a partir de Venda

```typescript
function criarContratoDeVenda(venda: Venda, condicoes: CondicoesContrato): Contrato {
  if (venda.status !== StatusVenda.FECHADA) {
    throw new Error('Só é possível criar contrato de venda fechada');
  }
  
  const contrato = new Contrato({
    numero: gerarNumeroContrato(), // CTR-2026-0001
    venda: venda.id,
    cliente: venda.clienteId,
    valorTotal: venda.valorPrevisto,
    status: StatusContrato.AGUARDANDO_ASSINATURA,
    dataEmissao: new Date(),
    garantiaMeses: condicoes.garantiaMeses || 60 // 5 anos padrão
  });
  
  // Criar parcelas
  const parcelas = gerarParcelas(
    contrato.valorTotal,
    condicoes.qtdParcelas,
    condicoes.dataVencimentoPrimeira
  );
  
  contrato.parcelas = parcelas;
  
  return contrato;
}
```

---

## Geração de Parcelas

```typescript
function gerarParcelas(
  valorTotal: number, 
  qtdParcelas: number, 
  dataPrimeira: Date
): ParcelaContrato[] {
  const valorParcela = valorTotal / qtdParcelas;
  const parcelas: ParcelaContrato[] = [];
  
  for (let i = 0; i < qtdParcelas; i++) {
    const vencimento = new Date(dataPrimeira);
    vencimento.setMonth(vencimento.getMonth() + i);
    
    parcelas.push({
      numeroParcela: i + 1,
      valor: valorParcela,
      dataVencimento: vencimento,
      status: StatusParcela.PENDENTE
    });
  }
  
  return parcelas;
}

// Exemplo:
// Valor: R$ 30.000
// Parcelas: 3x
// Primeira: 01/02/2026
// Resultado:
// - Parcela 1: R$ 10.000 - 01/02/2026
// - Parcela 2: R$ 10.000 - 01/03/2026
// - Parcela 3: R$ 10.000 - 01/04/2026
```

---

## Eventos de Domínio

| Evento | Quando | Dados |
|--------|--------|-------|
| `ContratoCriado` | Novo contrato gerado | contratoId, vendaId, valorTotal |
| `ContratoAssinado` | Cliente assinou | contratoId, dataAssinatura |
| `InstalacaoIniciada` | Começou instalação | contratoId, integradorId |
| `InstalacaoConcluida` | Terminou instalação | contratoId, dataInstalacao |
| `ParcelaPaga` | Pagamento registrado | contratoId, parcelaId, valor |
| `ParcelaAtrasada` | Passou vencimento | contratoId, parcelaId, diasAtraso |
| `ContratoFinalizado` | Todas parcelas pagas | contratoId |
| `ContratoCancelado` | Cancelamento | contratoId, motivo |

---

## Integração com Suporte

Quando `InstalacaoConcluida`:
1. Calcular `dataFimGarantia`
2. Criar registro de garantia no contexto Suporte
3. Cliente pode abrir tickets de garantia até essa data

```typescript
// Evento: InstalacaoConcluida
function onInstalacaoConcluida(evento: InstalacaoConcluida) {
  const contrato = contratoRepository.findById(evento.contratoId);
  
  // Criar garantia no contexto Suporte
  garantiaService.criarGarantia({
    contrato: contrato.id,
    cliente: contrato.clienteId,
    dataInicio: contrato.dataInstalacao,
    dataFim: contrato.dataFimGarantia,
    descricao: `Garantia do contrato ${contrato.numero}`
  });
}
```
