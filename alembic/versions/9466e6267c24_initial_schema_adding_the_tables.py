"""Initial schema - adding the tables

Revision ID: 9466e6267c24
Revises: 
Create Date: 2019-06-03 09:27:12.330842

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9466e6267c24'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
        sa.Column('id', sa.INTEGER(), nullable=False),
        sa.Column('first_name', sa.VARCHAR(), nullable=True),
        sa.Column('last_name', sa.VARCHAR(), nullable=True),
        sa.Column('username', sa.VARCHAR(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('chats',
        sa.Column('id', sa.INTEGER(), nullable=False),
        sa.Column('chat_title', sa.VARCHAR(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_activity',
        sa.Column('id', sa.INTEGER(), nullable=False),
        sa.Column('user_id', sa.INTEGER(), nullable=True),
        sa.Column('chat_id', sa.INTEGER(), nullable=True),
        sa.Column('datetime', sa.DATETIME(), nullable=True),
        sa.ForeignKeyConstraint(['chat_id'], ['chats.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('user_activity')
    op.drop_table('chats')
    op.drop_table('users')
