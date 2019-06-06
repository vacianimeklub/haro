"""Adds votes table

Revision ID: 87217436ada6
Revises: 25afc7b0d062
Create Date: 2019-06-06 20:38:28.314787

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '87217436ada6'
down_revision = '25afc7b0d062'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'votes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('voting_option_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['voting_option_id'], ['voting_options.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('votes')
