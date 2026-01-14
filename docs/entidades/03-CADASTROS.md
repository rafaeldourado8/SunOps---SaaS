# 03 - Contexto: Cadastros (Identity)

> **Linguagem Ubíqua:** Cliente, Vendedor, Integrador, Fornecedor, Pessoa, Documento, Endereço

**Fase:** 1 (MVP Core)

---

## Diagrama de Entidades

```
                    ┌─────────────────┐
                    │     PESSOA      │
                    │   (Abstract)    │
                    └────────┬────────┘
                             │
          ┌──────────────────┼──────────────────┐
          │                  │                  │
          ▼                  ▼                  ▼
   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
   │   CLIENTE   │    │  VENDEDOR   │    │ INTEGRADOR  │
   └─────────────┘    └─────────────┘    └─────────────┘
          │
          │
          ▼
   ┌─────────────┐
   │ FORNECEDOR  │
   └─────────────┘
```

---

## Entidades

### Pessoa (Entity - Abstract Base)

Base abstrata para todos os tipos de pessoa no sistema.

| Atributo | Tipo | Obrigatório | Descrição |
|----------|------|-------------|-----------|
| `id` | UUID | ✅ | Identificador único |
| `nome` | String | ✅ | Nome completo |
| `documento` | Documento (VO) | ✅ | CPF ou CNPJ |
| `email` | Email (VO) | ✅ | Email principal |
| `telefone` | Telefone (VO) | ✅ | Telefone principal |
| `endereco` | Endereco (VO) | ❌ | Endereço completo |
| `dataCadastro` | DateTime | ✅ | Data de criação |
| `ativo` | Boolean | ✅ | Status ativo/inativo |

---

### Cliente (Entity)

Pessoa que compra ou pode comprar sistemas solares.

**Extends:** Pessoa

| Atributo | Tipo | Obrigatório | Descrição |
|----------|------|-------------|-----------|
| `tipo` | TipoCliente | ✅ | Residencial, Comercial, Industrial, Rural |
| `consumoMedioKwh` | Decimal | ❌ | Consumo médio mensal em kWh |
| `concessionaria` | String | ❌ | Nome da concessionária de energia |
| `origemLead` | OrigemLead | ❌ | Site, Indicação, WhatsApp, Outro |
| `vendedorResponsavel` | VendedorId | ❌ | FK para Vendedor |
| `observacoes` | String | ❌ | Notas internas |

**Regras:**
- Cliente pode existir sem vendedor (lead ainda não atribuído)
- Consumo médio é usado para cálculo de dimensionamento

---

### Vendedor (Entity)

Colaborador responsável por vendas.

**Extends:** Pessoa

| Atributo | Tipo | Obrigatório | Descrição |
|----------|------|-------------|-----------|
| `matricula` | String | ✅ | Código interno |
| `metaMensal` | Decimal | ❌ | Meta de vendas em R$ |
| `comissaoPercentual` | Decimal | ✅ | % de comissão padrão |
| `supervisor` | VendedorId | ❌ | FK para supervisor (hierarquia) |
| `dataAdmissao` | Date | ✅ | Data de admissão |

**Regras:**
- Vendedor pode ter supervisor (outro vendedor)
- Comissão padrão pode ser alterada por venda

---

### Integrador (Entity)

Parceiro técnico que realiza instalações.

**Extends:** Pessoa

| Atributo | Tipo | Obrigatório | Descrição |
|----------|------|-------------|-----------|
| `razaoSocial` | String | ✅ | Razão social da empresa |
| `registroCrea` | String | ❌ | Registro no CREA |
| `areaAtuacao` | List\<Cidade\> | ✅ | Cidades onde atua |
| `capacidadeInstalacao` | Integer | ❌ | Instalações/mês |
| `avaliacao` | Decimal | ❌ | Nota média (0-5) |
| `totalInstalacoes` | Integer | ❌ | Contador de instalações |

**Regras:**
- Integrador é sempre PJ (CNPJ)
- Avaliação calculada a partir de feedbacks

---

### Fornecedor (Entity)

Distribuidor de equipamentos solares.

**Extends:** Pessoa

| Atributo | Tipo | Obrigatório | Descrição |
|----------|------|-------------|-----------|
| `razaoSocial` | String | ✅ | Razão social |
| `nomeFantasia` | String | ❌ | Nome fantasia |
| `prazoEntregaDias` | Integer | ❌ | Prazo médio de entrega |
| `prazoPagamentoDias` | Integer | ❌ | Prazo de pagamento |
| `contatoComercial` | String | ❌ | Nome do contato |
| `categoriasFornecidas` | List\<Categoria\> | ✅ | O que fornece |

**Regras:**
- Fornecedor é sempre PJ (CNPJ)
- Obrigatório informar quais categorias fornece

---

## Value Objects

### Documento (VO)

| Atributo | Tipo | Validação |
|----------|------|-----------|
| `numero` | String | CPF ou CNPJ válido |
| `tipo` | TipoDocumento | CPF, CNPJ |

```typescript
class Documento {
  constructor(numero: string) {
    this.tipo = numero.length === 11 ? 'CPF' : 'CNPJ';
    if (!this.isValid(numero)) throw new Error('Documento inválido');
    this.numero = numero;
  }
}
```

---

### Email (VO)

| Atributo | Tipo | Validação |
|----------|------|-----------|
| `endereco` | String | Formato email válido |

---

### Telefone (VO)

| Atributo | Tipo | Validação |
|----------|------|-----------|
| `ddd` | String | 2 dígitos |
| `numero` | String | 8-9 dígitos |
| `tipo` | TipoTelefone | Celular, Fixo, WhatsApp |

---

### Endereco (VO)

| Atributo | Tipo | Validação |
|----------|------|-----------|
| `cep` | String | 8 dígitos, válido |
| `logradouro` | String | Obrigatório |
| `numero` | String | Obrigatório |
| `complemento` | String | Opcional |
| `bairro` | String | Obrigatório |
| `cidade` | String | Obrigatório |
| `uf` | String | 2 caracteres, UF válida |

---

## Enums

```typescript
enum TipoCliente {
  RESIDENCIAL = 'RESIDENCIAL',
  COMERCIAL = 'COMERCIAL',
  INDUSTRIAL = 'INDUSTRIAL',
  RURAL = 'RURAL'
}

enum TipoDocumento {
  CPF = 'CPF',
  CNPJ = 'CNPJ'
}

enum TipoTelefone {
  CELULAR = 'CELULAR',
  FIXO = 'FIXO',
  WHATSAPP = 'WHATSAPP'
}

enum OrigemLead {
  SITE = 'SITE',
  INDICACAO = 'INDICACAO',
  WHATSAPP = 'WHATSAPP',
  INSTAGRAM = 'INSTAGRAM',
  FACEBOOK = 'FACEBOOK',
  OUTRO = 'OUTRO'
}
```

---

## Eventos de Domínio

| Evento | Quando | Dados |
|--------|--------|-------|
| `ClienteCriado` | Novo cliente cadastrado | clienteId, nome, vendedorId |
| `ClienteAtualizado` | Dados alterados | clienteId, camposAlterados |
| `VendedorAtribuido` | Vendedor assumiu cliente | clienteId, vendedorId |

---

## Exemplo de Uso

```typescript
// Criar cliente
const cliente = new Cliente({
  nome: 'João Silva',
  documento: new Documento('12345678901'),
  email: new Email('joao@email.com'),
  telefone: new Telefone('67', '999998888', TipoTelefone.WHATSAPP),
  tipo: TipoCliente.RESIDENCIAL,
  consumoMedioKwh: 450,
  origemLead: OrigemLead.WHATSAPP
});

// Atribuir vendedor
cliente.atribuirVendedor(vendedorId);
```
