# 09 - Contexto: Monitoramento (Integrações)

> **Linguagem Ubíqua:** Planta, Inversor, Alerta, Falha, Geração, Status

**Fase:** 4

---

## Integrações Externas

| Plataforma | API | Dados Obtidos |
|------------|-----|---------------|
| SolisCloud | api.soliscloud.com | Geração, Status, Alertas |
| Growatt/ShinePhone | api.growatt.com | Geração, Status, Alertas |
| Solarman | api.solarmanpv.com | Geração, Status, Alertas |

---

## Entidades

### PlantaSolar (Entity)

Representa uma instalação solar monitorada.

| Atributo | Tipo | Obrigatório | Descrição |
|----------|------|-------------|-----------|
| `id` | UUID | ✅ | ID interno |
| `idExterno` | String | ✅ | ID na plataforma de monitoramento |
| `plataforma` | Plataforma | ✅ | SolisCloud, Growatt, Solarman |
| `contrato` | ContratoId | ✅ | FK para Contrato |
| `cliente` | ClienteId | ✅ | FK para Cliente |
| `nome` | String | ✅ | Nome da planta |
| `potenciaInstalada` | Decimal | ✅ | Potência em kWp |
| `dataAtivacao` | Date | ✅ | Data de ativação |
| `status` | StatusPlanta | ✅ | Online, Offline, Alerta |
| `ultimaAtualizacao` | DateTime | ✅ | Último dado recebido |

### AlertaFalha (Entity)

| Atributo | Tipo | Obrigatório | Descrição |
|----------|------|-------------|-----------|
| `id` | UUID | ✅ | Identificador único |
| `planta` | PlantaId | ✅ | FK para Planta |
| `tipoFalha` | TipoFalha | ✅ | Offline, Baixa geração, Erro |
| `codigoErro` | String | ❌ | Código da plataforma |
| `descricao` | String | ✅ | Descrição do problema |
| `dataDeteccao` | DateTime | ✅ | Quando foi detectado |
| `dataNotificacao` | DateTime | ❌ | Quando cliente foi notificado |
| `status` | StatusAlerta | ✅ | Novo, Aguardando, Notificado |
| `mensagemCliente` | String | ❌ | Mensagem enviada |
| `ticketGerado` | TicketId | ❌ | FK para Ticket |

---

## ⚠️ Regra dos 2 Dias

> **CRÍTICO:** Aguardar 2 dias antes de notificar o cliente sobre falhas.

### Fluxo de Notificação

```
1. Erro detectado → Status = NOVO
         ↓
2. Sistema aguarda 48 horas
         ↓
3. Após 2 dias, verifica se ainda offline
         ↓
   ┌─────────────────────────────────────┐
   │                                     │
   ▼                                     ▼
Sistema voltou                    Ainda offline
     ↓                                   ↓
Status = RESOLVIDO              Preparar mensagem
                                         ↓
                              Status = AGUARDANDO_REVISAO
                                         ↓
                                Admin revisa e aprova
                                         ↓
                              Enviar para cliente
                                         ↓
                              Status = NOTIFICADO
```

### Template de Mensagem

```
Olá {nome_cliente}! 👋

Identificamos que seu sistema solar está apresentando uma 
inconsistência na comunicação. Isso pode ocorrer por diversos 
fatores externos, como oscilações na rede de internet ou 
atualizações na rede elétrica da região.

Já estamos monitorando a situação e, caso necessário, nossa 
equipe técnica entrará em contato para auxiliá-lo.

Se preferir, você pode verificar se o Wi-Fi do inversor está 
conectado corretamente.

Qualquer dúvida, estamos à disposição! 🌞

Equipe SunwOps
```

**Regras da mensagem:**
- ✅ Educada e empática
- ✅ Paciente
- ✅ Responsabiliza fatores externos quando for erro interno
- ✅ Oferece ajuda
- ❌ Nunca culpar a empresa diretamente

---

## Enums

```typescript
enum StatusPlanta {
  ONLINE = 'ONLINE',
  OFFLINE = 'OFFLINE',
  ALERTA = 'ALERTA',
  ERRO = 'ERRO'
}

enum TipoFalha {
  OFFLINE = 'OFFLINE',
  BAIXA_GERACAO = 'BAIXA_GERACAO',
  ERRO_INVERSOR = 'ERRO_INVERSOR',
  COMUNICACAO = 'COMUNICACAO'
}

enum StatusAlerta {
  NOVO = 'NOVO',
  AGUARDANDO_2_DIAS = 'AGUARDANDO_2_DIAS',
  AGUARDANDO_REVISAO = 'AGUARDANDO_REVISAO',
  NOTIFICADO = 'NOTIFICADO',
  RESOLVIDO = 'RESOLVIDO'
}
```

---

## Eventos de Domínio

| Evento | Quando | Ação |
|--------|--------|------|
| `FalhaDetectada` | API retorna erro | Criar alerta, iniciar timer 2 dias |
| `FalhaPersistente` | Após 2 dias offline | Preparar mensagem, aguardar revisão |
| `MensagemAprovada` | Admin aprova | Enviar WhatsApp/Email |
| `PlantaVoltouOnline` | Status normalizado | Fechar alerta |
