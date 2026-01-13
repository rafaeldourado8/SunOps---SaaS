"""add tickets and conversations tables

Revision ID: 004_tickets_conversations
Revises: 003_add_conversations
Create Date: 2026-01-13

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '004_tickets_conversations'
down_revision = '003_add_conversations'
branch_labels = None
depends_on = None


def upgrade():
    # Create tickets table
    op.create_table('tickets',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('ticket_number', sa.String(length=20), nullable=False),
        sa.Column('phone', sa.String(length=20), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('priority', sa.String(length=20), nullable=True),
        sa.Column('subject', sa.String(length=200), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('inverter_serial', sa.String(length=100), nullable=True),
        sa.Column('warranty_status', sa.String(length=50), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('resolved_at', sa.DateTime(), nullable=True),
        sa.Column('data', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_tickets_ticket_number', 'tickets', ['ticket_number'], unique=True)
    op.create_index('ix_tickets_status', 'tickets', ['status'])


def downgrade():
    op.drop_index('ix_tickets_status', table_name='tickets')
    op.drop_index('ix_tickets_ticket_number', table_name='tickets')
    op.drop_table('tickets')
