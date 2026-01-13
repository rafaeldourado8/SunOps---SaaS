"""initial schema

Revision ID: 001
Revises: 
Create Date: 2026-01-13

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB

revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Kits
    op.create_table(
        'kits',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('nome', sa.String(200), nullable=False),
        sa.Column('is_template', sa.Boolean(), default=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('data', JSONB)
    )
    
    # Itens Kit
    op.create_table(
        'itens_kit',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('kit_id', UUID(as_uuid=True), nullable=False),
        sa.Column('categoria', sa.String(50), nullable=False),
        sa.Column('nome', sa.String(200), nullable=False),
        sa.Column('marca', sa.String(100)),
        sa.Column('potencia_watts', sa.Integer()),
        sa.Column('preco', sa.Numeric(10, 2), nullable=False),
        sa.Column('quantidade', sa.Integer(), nullable=False),
        sa.Column('descricao', sa.Text()),
        sa.ForeignKeyConstraint(['kit_id'], ['kits.id'], ondelete='CASCADE')
    )
    
    # Orçamentos
    op.create_table(
        'orcamentos',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('kit_id', UUID(as_uuid=True), nullable=False),
        sa.Column('cliente_nome', sa.String(200), nullable=False),
        sa.Column('cliente_contato', sa.String(100), nullable=False),
        sa.Column('status', sa.String(50), nullable=False),
        sa.Column('validade_dias', sa.Integer(), default=3),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('aprovado_por', sa.String(200)),
        sa.Column('enviado_em', sa.DateTime()),
        sa.Column('data', JSONB),
        sa.ForeignKeyConstraint(['kit_id'], ['kits.id'])
    )
    
    # Domain Events
    op.create_table(
        'domain_events',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('aggregate_id', UUID(as_uuid=True), nullable=False),
        sa.Column('aggregate_type', sa.String(100), nullable=False),
        sa.Column('event_type', sa.String(100), nullable=False),
        sa.Column('event_data', JSONB, nullable=False),
        sa.Column('occurred_at', sa.DateTime(), nullable=False),
        sa.Column('version', sa.Integer(), nullable=False)
    )
    
    # Índices
    op.create_index('idx_events_aggregate', 'domain_events', ['aggregate_id', 'version'])
    op.create_index('idx_kits_template', 'kits', ['is_template'])
    op.create_index('idx_orcamentos_status', 'orcamentos', ['status'])


def downgrade() -> None:
    op.drop_index('idx_orcamentos_status')
    op.drop_index('idx_kits_template')
    op.drop_index('idx_events_aggregate')
    op.drop_table('domain_events')
    op.drop_table('orcamentos')
    op.drop_table('itens_kit')
    op.drop_table('kits')
