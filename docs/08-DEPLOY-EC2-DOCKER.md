# 08 - Deploy: EC2 com Docker vs Outras Opções

## 🎯 Comparação de Opções

### Opção 1: EC2 com Docker Compose (Recomendado!)

```
┌─────────────────────────────────────────────────────┐
│ AWS EC2 t3.small (2 vCPU, 2 GB RAM)                │
├─────────────────────────────────────────────────────┤
│ Docker Compose rodando:                             │
│ ├── PostgreSQL (master + 2 tenants)                │
│ ├── Redis                                           │
│ ├── RabbitMQ                                        │
│ ├── Django                                          │
│ ├── FastAPI                                         │
│ └── Celery                                          │
│                                                     │
│ Storage: 30 GB EBS (SSD)                           │
│ Backup: Snapshots EBS                              │
└─────────────────────────────────────────────────────┘

Custo: $15.18/mês (On-Demand)
Custo: $10.63/mês (Reserved 1 ano)
```

### Opção 2: Lightsail (Mais Simples)

```
┌─────────────────────────────────────────────────────┐
│ AWS Lightsail $10/mês (2 GB RAM, 1 vCPU)          │
├─────────────────────────────────────────────────────┤
│ Mesma stack Docker Compose                         │
│ Mais fácil de configurar                           │
│ IP fixo incluído                                    │
│ 3 TB transfer incluído                             │
└─────────────────────────────────────────────────────┘

Custo: $10/mês (fixo)
```

### Opção 3: EC2 + RDS (Produção)

```
┌─────────────────────────────────────────────────────┐
│ EC2 t3.small: $15.18/mês                           │
│ RDS db.t3.micro: $16.61/mês                        │
│ ElastiCache t3.micro: $12.41/mês                   │
└─────────────────────────────────────────────────────┘

Custo: $44.20/mês
Vantagens: Backups automáticos, alta disponibilidade
```

---

## ✅ Recomendação: EC2 com Docker

### Por quê?

```
✅ Controle total (aprende mais)
✅ Mesma stack local e produção
✅ Fácil de migrar depois
✅ Terraform para automatizar
✅ Pode usar Free Tier (12 meses)
✅ Snapshots para backup
✅ Elastic IP (IP fixo)
```

### Quando NÃO usar?

```
❌ Precisa alta disponibilidade (99.99%)
❌ Mais de 20 tenants
❌ Compliance rigoroso
❌ Time sem conhecimento DevOps
```

---

## 💰 Custo Detalhado: EC2 com Docker

### Breakdown Mensal

```
┌─────────────────────────────────────────────────────┐
│ CUSTOS AWS (2 Tenants)                              │
├─────────────────────────────────────────────────────┤
│                                                     │
│ EC2 t3.small (On-Demand)                           │
│ └─ $0.0208/hora × 730h = $15.18                    │
│                                                     │
│ EBS 30 GB (gp3)                                     │
│ └─ $0.08/GB × 30 = $2.40                           │
│                                                     │
│ Elastic IP (se parado)                             │
│ └─ $0.00 (grátis se EC2 rodando)                   │
│                                                     │
│ Data Transfer OUT                                   │
│ └─ 2 GB × $0.09 = $0.18                            │
│                                                     │
│ Snapshots (backup semanal)                         │
│ └─ 4 × 30 GB × $0.05 = $6.00                       │
│                                                     │
├─────────────────────────────────────────────────────┤
│ TOTAL: $23.76/mês                                  │
├─────────────────────────────────────────────────────┤
│ Com Reserved Instance (1 ano):                     │
│ TOTAL: $19.21/mês (-19%)                           │
└─────────────────────────────────────────────────────┘
```

**Conversão**: $23.76 × R$ 5.00 = **R$ 118.80/mês**

```
Receita: R$ 600/mês (2 tenants)
Custo: R$ 118.80/mês
Lucro: R$ 481.20/mês (80% margem)
```

---

## 🚀 Setup EC2 com Docker (Passo a Passo)

### 1. Criar EC2 via Console AWS

```
1. Acesse EC2 Dashboard
2. Launch Instance
3. Configurações:
   ├── Name: ops-crm-production
   ├── AMI: Ubuntu 22.04 LTS
   ├── Instance Type: t3.small
   ├── Key Pair: Criar nova (ops-crm-key.pem)
   ├── Network: Default VPC
   ├── Security Group:
   │   ├── SSH (22): Seu IP
   │   ├── HTTP (80): 0.0.0.0/0
   │   ├── HTTPS (443): 0.0.0.0/0
   │   └── Custom (8000-8001): 0.0.0.0/0 (temporário)
   └── Storage: 30 GB gp3
4. Launch
```

### 2. Conectar via SSH

```bash
# Dar permissão na chave
chmod 400 ops-crm-key.pem

# Conectar
ssh -i ops-crm-key.pem ubuntu@<EC2_PUBLIC_IP>
```

### 3. Instalar Docker

```bash
# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Adicionar usuário ao grupo docker
sudo usermod -aG docker ubuntu

# Instalar Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Verificar
docker --version
docker-compose --version

# Relogar para aplicar grupo
exit
ssh -i ops-crm-key.pem ubuntu@<EC2_PUBLIC_IP>
```

### 4. Clonar Projeto

```bash
# Instalar Git
sudo apt install git -y

# Clonar repositório
git clone <seu-repo-url> ops-crm
cd ops-crm

# Criar .env
cp .env.example .env
nano .env  # Editar com valores de produção
```

### 5. Subir Aplicação

```bash
# Subir containers
docker-compose up -d

# Ver logs
docker-compose logs -f

# Verificar status
docker-compose ps
```

### 6. Configurar Domínio (Opcional)

```bash
# Instalar Nginx
sudo apt install nginx -y

# Configurar reverse proxy
sudo nano /etc/nginx/sites-available/ops-crm

# Conteúdo:
server {
    listen 80;
    server_name seudominio.com *.seudominio.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /api/ {
        proxy_pass http://localhost:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

# Ativar site
sudo ln -s /etc/nginx/sites-available/ops-crm /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Instalar SSL (Let's Encrypt)
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d seudominio.com -d *.seudominio.com
```

---

## 🔧 Terraform para Automatizar

### Estrutura

```
terraform/
├── main.tf           # Recursos principais
├── variables.tf      # Variáveis
├── outputs.tf        # Outputs
└── user-data.sh      # Script de inicialização
```

### main.tf (Simplificado)

```hcl
provider "aws" {
  region = "us-east-1"
}

# Security Group
resource "aws_security_group" "ops_crm" {
  name        = "ops-crm-sg"
  description = "Security group for OPS CRM"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # Mudar para seu IP
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# EC2 Instance
resource "aws_instance" "ops_crm" {
  ami           = "ami-0c7217cdde317cfec"  # Ubuntu 22.04 us-east-1
  instance_type = "t3.small"
  key_name      = "ops-crm-key"

  vpc_security_group_ids = [aws_security_group.ops_crm.id]

  root_block_device {
    volume_size = 30
    volume_type = "gp3"
  }

  user_data = file("user-data.sh")

  tags = {
    Name = "ops-crm-production"
  }
}

# Elastic IP
resource "aws_eip" "ops_crm" {
  instance = aws_instance.ops_crm.id
  domain   = "vpc"
}

output "public_ip" {
  value = aws_eip.ops_crm.public_ip
}
```

### user-data.sh

```bash
#!/bin/bash

# Atualizar sistema
apt update && apt upgrade -y

# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Instalar Docker Compose
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Instalar Git
apt install git -y

# Clonar projeto
cd /home/ubuntu
git clone <seu-repo-url> ops-crm
cd ops-crm

# Criar .env (você precisa configurar depois)
cp .env.example .env

# Subir aplicação
docker-compose up -d

echo "Setup completo! Configure o .env e reinicie os containers."
```

### Usar Terraform

```bash
# Inicializar
terraform init

# Planejar
terraform plan

# Aplicar
terraform apply

# Ver IP público
terraform output public_ip

# Destruir (quando quiser deletar tudo)
terraform destroy
```

---

## 📊 Comparação Final

| Aspecto | EC2 Docker | Lightsail | EC2 + RDS |
|---------|------------|-----------|-----------|
| **Custo/mês** | R$ 119 | R$ 57 | R$ 221 |
| **Controle** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Facilidade** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| **Escalabilidade** | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Aprendizado** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Backup** | Manual | Automático | Automático |
| **Terraform** | ✅ Sim | ✅ Sim | ✅ Sim |

---

## 🎯 Recomendação por Fase

### Fase 1: MVP (0-5 tenants)
**Use: Lightsail $10/mês**
- Mais barato
- Mais simples
- Suficiente para validar

### Fase 2: Crescimento (5-20 tenants)
**Use: EC2 t3.small com Docker**
- Mais controle
- Aprende DevOps
- Terraform para IaC

### Fase 3: Escala (20+ tenants)
**Use: EC2 + RDS + ElastiCache**
- Alta disponibilidade
- Backups automáticos
- Multi-AZ

---

## 🔐 Checklist de Segurança

```
□ Mudar senhas padrão do .env
□ Security Group restrito (SSH só seu IP)
□ Firewall (ufw) configurado
□ SSL/TLS (Let's Encrypt)
□ Backups automáticos (snapshots)
□ Monitoring (CloudWatch)
□ Logs centralizados
□ Secrets no AWS Secrets Manager
□ IAM roles (não usar root)
□ MFA habilitado
```

---

## 💡 Dica Final

**Para aprender**: Use **EC2 com Docker + Terraform**

**Para produzir rápido**: Use **Lightsail**

**Para escalar**: Migre para **EC2 + RDS**

---

Quer que eu crie os arquivos Terraform completos para você provisionar tudo automaticamente?
