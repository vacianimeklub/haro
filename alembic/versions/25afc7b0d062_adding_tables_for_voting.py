"""Adding tables for voting

Revision ID: 25afc7b0d062
Revises: 9466e6267c24
Create Date: 2019-06-05 09:27:18.339622

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '25afc7b0d062'
down_revision = '9466e6267c24'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'voting',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=True),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('is_multi_choice', sa.Boolean(), nullable=True),
        sa.Column('creator_user_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['creator_user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'voting_options',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('voting_id', sa.Integer(), nullable=True),
        sa.Column('option', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['voting_id'], ['voting.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('voting_options')
    op.drop_table('voting')
