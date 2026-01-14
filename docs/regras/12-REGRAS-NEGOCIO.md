# 12 - Regras de Negócio Consolidadas

## Sumário

1. [Regras de Kit](#regras-de-kit)
2. [Regras de Preço](#regras-de-preço)
3. [Regras de Cálculo](#regras-de-cálculo)
4. [Regras de Venda](#regras-de-venda)
5. [Regras de Contrato](#regras-de-contrato)
6. [Regras de Monitoramento](#regras-de-monitoramento)
7. [Regras de Agentes IA](#regras-de-agentes-ia)
8. [Regras de Comunicação](#regras-de-comunicação)

---

## Regras de Kit

| ID | Regra | Validação |
|----|-------|-----------|
| RN-KIT-01 | Kit deve ter itens de **no mínimo 2 categorias** diferentes | Ao salvar |
| RN-KIT-02 | Potência total = soma das potências dos painéis | Calculado |
| RN-KIT-03 | Estruturas = 1 kit para cada 4 painéis (arredondar cima) | Sugestão automática |
| RN-KIT-04 | Cabos padrão: 2 rolos (1 preto + 1 vermelho) | Sugestão automática |
| RN-KIT-05 | Template não pode ser editado após uso em orçamento | Ao editar |
| RN-KIT-06 | Preço do item é snapshot no momento da inclusão | Ao adicionar item |

---

## Regras de Preço

| ID | Regra | Validação |
|----|-------|-----------|
| RN-PRECO-01 | Preço tem validade de **3 dias úteis** | Data calculada |
| RN-PRECO-02 | Após validade, preço fica inválido para novos orçamentos | Ao criar orçamento |
| RN-PRECO-03 | **Segunda-feira 8h**: alerta "Realizar cotações hoje" | Job agendado |
| RN-PRECO-04 | Histórico de preços **nunca é deletado** | Soft delete |
| RN-PRECO-05 | Orçamento existente mantém preço original (snapshot) | Imutável |

### Cálculo de Dias Úteis

```typescript
function adicionarDiasUteis(data: Date, dias: number): Date {
  let resultado = new Date(data);
  let diasAdicionados = 0;
  
  while (diasAdicionados < dias) {
    resultado.setDate(resultado.getDate() + 1);
    const diaSemana = resultado.getDay();
    // 0 = domingo, 6 = sábado
    if (diaSemana !== 0 && diaSemana !== 6) {
      diasAdicionados++;
    }
  }
  
  return resultado;
}

// Validade = dataCotacao + 3 dias úteis
```

---

## Regras de Cálculo de Geração

| ID | Regra | Fórmula |
|----|-------|---------|
| RN-CALC-01 | Geração por painel | `potenciaWp × 0.7 × 30 × 4.2` |
| RN-CALC-02 | Geração total | `geracaoPainel × qtdPaineis × fatorOrientacao × fatorSombreamento` |
| RN-CALC-03 | Payback em meses | `valorSistema / (economiaAnual / 12)` |
| RN-CALC-04 | Economia anual | `geracaoAnualKwh × tarifaKwh` |
| RN-CALC-05 | Cobertura consumo | `(geracaoMensal / consumoMedio) × 100` |

### Fatores de Orientação

| Orientação | Fator |
|------------|-------|
| Norte | 1.00 |
| Nordeste/Noroeste | 0.95 |
| Leste/Oeste | 0.85 |
| Sudeste/Sudoeste | 0.80 |
| Sul | 0.70 |

### Fatores de Sombreamento

| Nível | Fator |
|-------|-------|
| Nenhum | 1.00 |
| Parcial (até 10%) | 0.90 |
| Significativo (>10%) | 0.75 |

---

## Regras de Venda

| ID | Regra | Validação |
|----|-------|-----------|
| RN-VND-01 | Venda **PERDIDA** exige motivo obrigatório | Ao mudar status |
| RN-VND-02 | Motivo deve ter categoria + descrição (mín 10 chars) | Ao salvar |
| RN-VND-03 | Toda mudança de status gera registro no histórico | Evento automático |
| RN-VND-04 | Apenas admin pode reabrir venda perdida | Permissão |
| RN-VND-05 | Venda de orçamento herda valor e vai para etapa PROPOSTA | Ao converter |

---

## Regras de Contrato

| ID | Regra | Validação |
|----|-------|-----------|
| RN-CTR-01 | Contrato só de Venda **FECHADA** | Ao criar |
| RN-CTR-02 | Data fim garantia = data instalação + garantia meses | Calculado |
| RN-CTR-03 | Parcela vira ATRASADA após vencimento | Job diário |
| RN-CTR-04 | FINALIZADO só quando todas parcelas PAGAS | Ao pagar |
| RN-CTR-05 | Cancelamento exige justificativa | Ao cancelar |

---

## Regras de Monitoramento

| ID | Regra | Validação |
|----|-------|-----------|
| RN-MON-01 | **Aguardar 2 dias** antes de notificar cliente | Job verifica 48h |
| RN-MON-02 | Mensagem passa por **revisão do admin** | Status AGUARDANDO_REVISAO |
| RN-MON-03 | Erro interno: **nunca culpar empresa** diretamente | Template mensagem |
| RN-MON-04 | Mensagem deve ser educada, empática e paciente | Template mensagem |
| RN-MON-05 | Se sistema voltar antes de 2 dias, não notificar | Verificação automática |

### Fluxo de Notificação

```
Erro detectado
     ↓
Timer 48 horas inicia
     ↓
Após 48h: ainda offline?
     ├── NÃO → Cancelar alerta
     └── SIM → Preparar mensagem → Admin revisa → Enviar
```

---

## Regras de Agentes IA

| ID | Regra | Validação |
|----|-------|-----------|
| RN-IA-01 | Não sair do contexto configurado | Configuração |
| RN-IA-02 | Não alucinar (inventar informações) | Configuração |
| RN-IA-03 | Transição IA → Humano **imperceptível** ao cliente | Ao fazer takeover |
| RN-IA-04 | Todo histórico de conversa **salvo** | Automático |
| RN-IA-05 | Orçamento pode requerer aprovação | Configuração |
| RN-IA-06 | Compreender mensagens de áudio | Feature |

---

## Regras de Comunicação com Cliente

| ID | Regra | Aplicação |
|----|-------|-----------|
| RN-COM-01 | Atendimento **humanizado** | Todos os canais |
| RN-COM-02 | Usar **analogias** para pessoas leigas | Suporte, Ensino |
| RN-COM-03 | **Paciência** especial com idosos | Suporte, Ensino |
| RN-COM-04 | Mensagens com **empatia** e **entendimento** | Alertas, Suporte |
| RN-COM-05 | Link de garantia único e criptografado | Suporte |

---

## Matriz de Validação por Contexto

| Contexto | Regras Aplicáveis |
|----------|-------------------|
| Cadastros | - |
| Catálogo | RN-PRECO-01 a 05 |
| Orçamentos | RN-KIT-01 a 06, RN-CALC-01 a 05 |
| Vendas | RN-VND-01 a 05 |
| Contratos | RN-CTR-01 a 05 |
| Suporte | RN-COM-01 a 05 |
| Monitoramento | RN-MON-01 a 05, RN-COM-01 a 05 |
| Agentes IA | RN-IA-01 a 06, RN-COM-01 a 05 |
