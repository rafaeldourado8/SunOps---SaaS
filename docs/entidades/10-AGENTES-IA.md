# 10 - Contexto: Agentes de IA

> **Linguagem Ubíqua:** Agente, Conversa, Mensagem, Takeover, Configuração

**Fase:** 4

---

## Visão Geral

Os Agentes de IA são chatbots configuráveis que atendem clientes via WhatsApp e outras plataformas.

```
┌─────────────────────────────────────────────────────────────┐
│                                                              │
│   CLIENTE        AGENTE IA         HUMANO                   │
│      │               │                │                      │
│      │──mensagem────▶│                │                      │
│      │◀──resposta────│                │                      │
│      │               │                │                      │
│      │──mensagem────▶│                │                      │
│      │◀──resposta────│                │                      │
│      │               │                │                      │
│      │               │ ──takeover───▶ │ (humano assume)      │
│      │               │                │                      │
│      │◀────────────resposta───────────│                      │
│      │                                │                      │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Entidades

### Agente (Entity)

Configuração de um agente de IA.

| Atributo | Tipo | Obrigatório | Descrição |
|----------|------|-------------|-----------|
| `id` | UUID | ✅ | Identificador único |
| `nome` | String | ✅ | Ex: "Vendedor Virtual" |
| `tipo` | TipoAgente | ✅ | Vendas, Suporte, Marketing |
| `ativo` | Boolean | ✅ | Agente ativo? |
| `configuracao` | ConfiguracaoAgente | ✅ | Regras e comportamentos |
| `plataformas` | List\<Plataforma\> | ✅ | WhatsApp, Instagram... |

### Conversa (Aggregate Root)

| Atributo | Tipo | Obrigatório | Descrição |
|----------|------|-------------|-----------|
| `id` | UUID | ✅ | Identificador único |
| `agente` | AgenteId | ✅ | FK para Agente |
| `cliente` | ClienteId | ❌ | FK para Cliente (se identificado) |
| `plataforma` | PlataformaChat | ✅ | WhatsApp, Instagram |
| `identificadorExterno` | String | ✅ | ID do chat na plataforma |
| `status` | StatusConversa | ✅ | Ativa, Pausada, Encerrada |
| `modoAtendimento` | ModoAtendimento | ✅ | IA, Humano, Híbrido |
| `atendente` | UsuarioId | ❌ | Se humano assumiu |
| `dataInicio` | DateTime | ✅ | Início |
| `mensagens` | List\<Mensagem\> | ✅ | Histórico completo |

### Mensagem (Entity)

| Atributo | Tipo | Obrigatório | Descrição |
|----------|------|-------------|-----------|
| `id` | UUID | ✅ | Identificador único |
| `direcao` | Direcao | ✅ | Entrada (cliente), Saída (agente) |
| `tipo` | TipoMensagem | ✅ | Texto, Audio, Imagem |
| `conteudo` | String | ✅ | Texto ou URL do arquivo |
| `remetente` | String | ✅ | 'IA', 'Cliente' ou nome |
| `dataHora` | DateTime | ✅ | Data e hora |

---

## Value Object: ConfiguracaoAgente

| Atributo | Tipo | Descrição |
|----------|------|-----------|
| `personalidade` | String | Tom de voz, estilo |
| `regrasNegocio` | List\<String\> | Regras que deve seguir |
| `perguntasChave` | List\<String\> | Perguntas para orçamento |
| `respostasProibidas` | List\<String\> | O que nunca dizer |
| `exemplosConversa` | List\<Exemplo\> | Prints de referência |
| `podeEnviarOrcamento` | Boolean | Pode gerar PDF? |
| `requerAprovacao` | Boolean | Orçamento precisa revisão? |

---

## Funcionalidades do Agente de Vendas

1. **Atendimento automatizado** via WhatsApp
2. **Compreender áudios** do cliente
3. **Linguagem humana** e natural
4. **Montar orçamento** com perguntas-chave:
   - Qual seu consumo médio?
   - Qual tipo de telhado?
   - Cidade/Estado?
5. **Enviar orçamento em PDF** (após revisão se configurado)
6. **Guardar histórico** completo

---

## Takeover (Assumir Conversa)

O administrador pode assumir a conversa a qualquer momento:

```typescript
function assumirConversa(conversaId: UUID, atendenteId: UUID) {
  const conversa = conversaRepository.findById(conversaId);
  
  conversa.modoAtendimento = ModoAtendimento.HUMANO;
  conversa.atendente = atendenteId;
  
  // Cliente NÃO deve perceber a mudança
  // Não enviar mensagem tipo "Agora você fala com humano"
  
  conversaRepository.save(conversa);
  eventBus.publish(new TakeoverRealizado(conversaId, atendenteId));
}
```

**Regra:** A transição deve ser imperceptível ao cliente.

---

## Enums

```typescript
enum TipoAgente {
  VENDAS = 'VENDAS',
  SUPORTE = 'SUPORTE',
  MARKETING = 'MARKETING'
}

enum PlataformaChat {
  WHATSAPP = 'WHATSAPP',
  INSTAGRAM = 'INSTAGRAM',
  FACEBOOK = 'FACEBOOK',
  TELEGRAM = 'TELEGRAM',
  WEBCHAT = 'WEBCHAT'
}

enum StatusConversa {
  ATIVA = 'ATIVA',
  PAUSADA = 'PAUSADA',
  ENCERRADA = 'ENCERRADA'
}

enum ModoAtendimento {
  IA = 'IA',
  HUMANO = 'HUMANO',
  HIBRIDO = 'HIBRIDO'
}

enum TipoMensagem {
  TEXTO = 'TEXTO',
  AUDIO = 'AUDIO',
  IMAGEM = 'IMAGEM',
  DOCUMENTO = 'DOCUMENTO',
  VIDEO = 'VIDEO'
}
```

---

## Regras de Negócio

| ID | Regra |
|----|-------|
| RN-IA-01 | Agente não deve sair do contexto configurado |
| RN-IA-02 | Agente não deve alucinar (inventar informações) |
| RN-IA-03 | Transição IA → Humano deve ser imperceptível |
| RN-IA-04 | Todo histórico de conversa deve ser salvo |
| RN-IA-05 | Orçamento pode requerer aprovação do admin |
| RN-IA-06 | Agente pode interagir com outros agentes se configurado |
