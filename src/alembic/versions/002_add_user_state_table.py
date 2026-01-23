"""add user state table

Revision ID: 002
Revises: 001
Create Date: 2024-01-02 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('usuario_estado',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('usuario_id', sa.String(), nullable=False),
        sa.Column('chave', sa.String(), nullable=False),
        sa.Column('valor', postgresql.JSONB(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['usuario_id'], ['usuarios.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('usuario_id', 'chave', name='uq_usuario_chave')
    )
    
    op.create_index('idx_usuario_estado_usuario', 'usuario_estado', ['usuario_id'])
    op.create_index('idx_usuario_estado_chave', 'usuario_estado', ['chave'])


def downgrade() -> None:
    op.drop_index('idx_usuario_estado_chave')
    op.drop_index('idx_usuario_estado_usuario')
    op.drop_table('usuario_estado')
