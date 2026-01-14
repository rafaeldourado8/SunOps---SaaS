# 04 - Contexto: Catálogo de Produtos

> **Linguagem Ubíqua:** Produto, Painel, Inversor, Estrutura, Cabo, Conector, Marca, Cotação, Preço

**Fase:** 1 (MVP Core)

---

## Diagrama de Entidades

```
                         ┌─────────────────┐
                         │     PRODUTO     │
                         │   (Abstract)    │
                         └────────┬────────┘
                                  │
        ┌────────────┬────────────┼────────────┬────────────┐
        │            │            │            │            │
        ▼            ▼            ▼            ▼            ▼
  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
  │  PAINEL  │ │ INVERSOR │ │ESTRUTURA │ │   CABO   │ │ CONECTOR │
  │  SOLAR   │ │          │ │          │ │  SOLAR   │ │          │
  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘
        │            │            │            │            │
        └────────────┴────────────┴────────────┴────────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │     MARCA       │
                         └─────────────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │   FORNECEDOR    │
                         └─────────────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │ COTAÇÃO PREÇO   │
                         └─────────────────┘
```

---

## Aggregate Root: Produto

### Produto (Entity - Abstract Base)

Base para todos os produtos solares.

| Atributo | Tipo | Obrigatório | Descrição |
|----------|------|-------------|-----------|
| `id` | UUID | ✅ | Identificador único |
| `sku` | String | ✅ | Código único do produto |
| `nome` | String | ✅ | Nome do produto |
| `descricao` | String | ❌ | Descrição detalhada |
| `categoria` | Categoria | ✅ | Tipo do produto |
| `marca` | MarcaId | ✅ | FK para Marca |
| `fornecedor` | FornecedorId | ✅ | FK para Fornecedor |
| `precoAtual` | Preco (VO) | ❌ | Último preço cotado |
| `ativo` | Boolean | ✅ | Disponível para venda |
| `dataCadastro` | DateTime | ✅ | Data de criação |

---

### PainelSolar (Entity)

**Extends:** Produto

| Atributo | Tipo | Obrigatório | Descrição |
|----------|------|-------------|-----------|
| `potenciaWp` | Integer | ✅ | Potência em Watts-pico (ex: 550, 700) |
| `eficiencia` | Decimal | ❌ | Percentual de eficiência |
| `dimensoes` | Dimensoes (VO) | ❌ | Largura × Altura × Profundidade |
| `peso` | Decimal | ❌ | Peso em kg |
| `garantiaAnos` | Integer | ❌ | Anos de garantia |
| `tipoCelula` | TipoCelula | ❌ | Monocristalino, Policristalino |

**Exemplos de Produtos:**
- OSDA 550W Mono
- OSDA 700W Mono
- Canadian 550W

**Regra:** Potência é obrigatória pois é usada nos cálculos de geração.

---

### Inversor (Entity)

**Extends:** Produto

| Atributo | Tipo | Obrigatório | Descrição |
|----------|------|-------------|-----------|
| `potenciaKwp` | Decimal | ✅ | Potência nominal em kWp (ex: 4, 5, 7) |
| `potenciaMaximaKwp` | Decimal | ❌ | Potência máxima com overload |
| `overloadPercentual` | Decimal | ❌ | % de overload suportado |
| `qtdMppt` | Integer | ❌ | Quantidade de MPPTs |
| `qtdStrings` | Integer | ❌ | Quantidade de strings |
| `tensaoEntrada` | String | ❌ | Range de tensão DC |
| `garantiaAnos` | Integer | ❌ | Anos de garantia |
| `wifi` | Boolean | ❌ | Possui WiFi integrado |
| `plataformaMonitoramento` | Plataforma | ❌ | SolisCloud, Growatt, Solarman |

**Exemplos de Produtos:**
- Solis 4kWp Mini
- Solis 5kWp
- Growatt 6kWp

**Regra de Overload:**
- Um kit pode ter potência de painéis MAIOR que o inversor
- Limite: até o percentual de overload do inversor
- Ex: Inversor 5kWp com 30% overload aceita até 6.5kWp de painéis

---

### Estrutura (Entity)

**Extends:** Produto

| Atributo | Tipo | Obrigatório | Descrição |
|----------|------|-------------|-----------|
| `tipoTelhado` | TipoTelhado | ✅ | Cerâmico, Fibrocimento, Zinco, Laje, Solo |
| `qtdPaineisPorKit` | Integer | ✅ | Painéis por kit (padrão: 4) |
| `materialFixacao` | String | ❌ | Alumínio, Aço galvanizado |
| `inclinacaoMin` | Integer | ❌ | Inclinação mínima em graus |
| `inclinacaoMax` | Integer | ❌ | Inclinação máxima em graus |

**Regra de Cálculo:**
```
Kits de estrutura = CEILING(qtdPaineis / qtdPaineisPorKit)

Exemplo: 10 painéis ÷ 4 painéis/kit = 3 kits de estrutura
```

**Tipos de Telhado:**
- **Cerâmico:** Telha de barro, colonial
- **Fibrocimento:** Brasilit, Eternit
- **Fibrometal:** Sanduíche
- **Laje:** Concreto (requer particularidades)
- **Zinco:** Metálica
- **Solo:** Ground mount (configuração manual)

---

### CaboSolar (Entity)

**Extends:** Produto

| Atributo | Tipo | Obrigatório | Descrição |
|----------|------|-------------|-----------|
| `bitola` | Bitola | ✅ | 4mm ou 6mm |
| `cor` | CorCabo | ✅ | Preto ou Vermelho |
| `metragemRolo` | Integer | ✅ | Metros por rolo |
| `material` | String | ❌ | Cobre, Alumínio |

**Regra Padrão:**
- Todo kit inclui 2 rolos: 1 preto + 1 vermelho
- Bitolas mais comuns: 4mm (residencial) e 6mm (comercial)

---

### Conector (Entity)

**Extends:** Produto

| Atributo | Tipo | Obrigatório | Descrição |
|----------|------|-------------|-----------|
| `tipo` | TipoConector | ✅ | MC4, MC4 Paralelo, etc |
| `genero` | GeneroConector | ✅ | Macho, Fêmea, Par |
| `amperagem` | Integer | ❌ | Amperagem suportada |

**Tipos Comuns:**
- MC4 Par (macho + fêmea)
- MC4 Y (derivação)
- MC4 Paralelo

---

## Entidades de Suporte

### Marca (Entity)

| Atributo | Tipo | Obrigatório | Descrição |
|----------|------|-------------|-----------|
| `id` | UUID | ✅ | Identificador único |
| `nome` | String | ✅ | Nome da marca |
| `paisOrigem` | String | ❌ | País de origem |
| `site` | String | ❌ | Website oficial |
| `ativa` | Boolean | ✅ | Marca ativa no sistema |

**Marcas Comuns:**
- OSDA
- Solis
- CCM
- Flex
- Canadian
- Growatt
- Trina

---

### CotacaoPreco (Entity)

Histórico de preços cotados com fornecedores.

| Atributo | Tipo | Obrigatório | Descrição |
|----------|------|-------------|-----------|
| `id` | UUID | ✅ | Identificador único |
| `produto` | ProdutoId | ✅ | FK para Produto |
| `fornecedor` | FornecedorId | ✅ | FK para Fornecedor |
| `preco` | Preco (VO) | ✅ | Valor cotado |
| `dataCotacao` | DateTime | ✅ | Data da cotação |
| `dataValidade` | DateTime | ✅ | Data limite (padrão: +3 dias úteis) |
| `valido` | Boolean | ✅ | Calculado: dataValidade >= hoje |
| `observacao` | String | ❌ | Condições especiais |

**⚠️ REGRA IMPORTANTE:**

> O preço tem **validade de 3 dias úteis**.
> 
> Após isso, o sistema mantém a cotação para histórico, mas marca como inválida.
> 
> Segunda-feira de manhã: Sistema envia alerta **"Realizar cotações hoje"**

---

## Value Objects

### Preco (VO)

| Atributo | Tipo | Validação |
|----------|------|-----------|
| `valor` | Decimal | > 0 |
| `moeda` | Moeda | BRL (default) |
| `dataReferencia` | DateTime | Data da cotação |

```typescript
class Preco {
  constructor(valor: number, dataReferencia: Date) {
    if (valor <= 0) throw new Error('Preço deve ser maior que zero');
    this.valor = valor;
    this.moeda = 'BRL';
    this.dataReferencia = dataReferencia;
  }
  
  estaValido(): boolean {
    const diasUteis = this.calcularDiasUteis(this.dataReferencia, new Date());
    return diasUteis <= 3;
  }
}
```

---

### Dimensoes (VO)

| Atributo | Tipo | Validação |
|----------|------|-----------|
| `larguraMm` | Integer | > 0 |
| `alturaMm` | Integer | > 0 |
| `profundidadeMm` | Integer | > 0 |

---

## Enums

```typescript
enum Categoria {
  PAINEL_SOLAR = 'PAINEL_SOLAR',
  INVERSOR = 'INVERSOR',
  ESTRUTURA = 'ESTRUTURA',
  CABO_SOLAR = 'CABO_SOLAR',
  CONECTOR = 'CONECTOR',
  OUTROS = 'OUTROS'
}

enum TipoTelhado {
  CERAMICO = 'CERAMICO',
  FIBROCIMENTO = 'FIBROCIMENTO',
  FIBROMETAL = 'FIBROMETAL',
  LAJE = 'LAJE',
  ZINCO = 'ZINCO',
  SOLO = 'SOLO'
}

enum Bitola {
  MM_4 = '4mm',
  MM_6 = '6mm'
}

enum CorCabo {
  PRETO = 'PRETO',
  VERMELHO = 'VERMELHO'
}

enum TipoConector {
  MC4 = 'MC4',
  MC4_PARALELO = 'MC4_PARALELO',
  MC4_Y = 'MC4_Y'
}

enum TipoCelula {
  MONOCRISTALINO = 'MONOCRISTALINO',
  POLICRISTALINO = 'POLICRISTALINO'
}

enum Plataforma {
  SOLISCLOUD = 'SOLISCLOUD',
  GROWATT = 'GROWATT',
  SHINEPHONE = 'SHINEPHONE',
  SOLARMAN_BUSINESS = 'SOLARMAN_BUSINESS',
  SOLARMAN_SMART = 'SOLARMAN_SMART'
}
```

---

## Regras de Negócio

| ID | Regra |
|----|-------|
| RN-CAT-01 | Preço tem validade de 3 dias úteis |
| RN-CAT-02 | Após validade, preço fica inválido para novos orçamentos |
| RN-CAT-03 | Segunda-feira 8h: alerta "Realizar cotações hoje" |
| RN-CAT-04 | Histórico de preços nunca é deletado |
| RN-CAT-05 | Todo produto deve ter fornecedor obrigatório |
| RN-CAT-06 | Potência é obrigatória para Painéis e Inversores |

---

## Eventos de Domínio

| Evento | Quando | Dados |
|--------|--------|-------|
| `ProdutoCadastrado` | Novo produto criado | produtoId, categoria, nome |
| `PrecoCotado` | Nova cotação registrada | produtoId, fornecedorId, preco |
| `PrecoExpirado` | Cotação passou validade | produtoId, cotacaoId |
| `AlertaCotacao` | Segunda-feira 8h | lista de produtos sem preço válido |
