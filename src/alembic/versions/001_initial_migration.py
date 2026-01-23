"""initial migration

Revision ID: 001
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Usuarios
    op.create_table('usuarios',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('nome', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('senha_hash', sa.String(), nullable=False),
        sa.Column('ativo', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )

    # Clientes
    op.create_table('clientes',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('nome', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('telefone', sa.String(), nullable=True),
        sa.Column('cpf_cnpj', sa.String(), nullable=True),
        sa.Column('tipo', sa.String(), nullable=False),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id')
    )

    # Premissas
    op.create_table('premissas_preco',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('tipo_item', sa.String(), nullable=False),
        sa.Column('descricao', sa.String(), nullable=False),
        sa.Column('preco_base', sa.Numeric(10, 2), nullable=False),
        sa.Column('unidade', sa.String(), nullable=False),
        sa.Column('ativo', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table('configuracoes',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('chave', sa.String(), nullable=False),
        sa.Column('valor', sa.String(), nullable=False),
        sa.Column('descricao', sa.String(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('chave')
    )

    # Propostas
    op.create_table('propostas',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('cliente_id', sa.String(), nullable=False),
        sa.Column('numero', sa.String(), nullable=False),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('valor_total', sa.Numeric(10, 2), nullable=False, server_default='0'),
        sa.Column('desconto_percentual', sa.Numeric(5, 2), nullable=False, server_default='0'),
        sa.Column('desconto_aprovado', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('observacoes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['cliente_id'], ['clientes.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('numero')
    )

    op.create_table('itens_proposta',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('proposta_id', sa.String(), nullable=False),
        sa.Column('tipo_item', sa.String(), nullable=False),
        sa.Column('descricao', sa.String(), nullable=False),
        sa.Column('quantidade', sa.Integer(), nullable=False),
        sa.Column('preco_unitario', sa.Numeric(10, 2), nullable=False),
        sa.Column('preco_total', sa.Numeric(10, 2), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['proposta_id'], ['propostas.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Contratos
    op.create_table('contratos',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('proposta_id', sa.String(), nullable=False),
        sa.Column('numero', sa.String(), nullable=False),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('valor_total', sa.Numeric(10, 2), nullable=False),
        sa.Column('data_assinatura', sa.DateTime(), nullable=True),
        sa.Column('pdf_path', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['proposta_id'], ['propostas.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('numero')
    )

    # Índices
    op.create_index('idx_clientes_email', 'clientes', ['email'])
    op.create_index('idx_clientes_status', 'clientes', ['status'])
    op.create_index('idx_propostas_cliente', 'propostas', ['cliente_id'])
    op.create_index('idx_propostas_status', 'propostas', ['status'])
    op.create_index('idx_contratos_proposta', 'contratos', ['proposta_id'])


def downgrade() -> None:
    op.drop_index('idx_contratos_proposta')
    op.drop_index('idx_propostas_status')
    op.drop_index('idx_propostas_cliente')
    op.drop_index('idx_clientes_status')
    op.drop_index('idx_clientes_email')
    
    op.drop_table('contratos')
    op.drop_table('itens_proposta')
    op.drop_table('propostas')
    op.drop_table('configuracoes')
    op.drop_table('premissas_preco')
    op.drop_table('clientes')
    op.drop_table('usuarios')
