"""Initial revision with UserAccount table

Revision ID: 75c9a8f2f225
Revises: 
Create Date: 2018-10-15 20:39:55.369372

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '75c9a8f2f225'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_activity')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_activity',
        sa.Column('id', sa.INTEGER(), nullable=False),
        sa.Column('user_id', sa.INTEGER(), nullable=True),
        sa.Column('username', sa.VARCHAR(), nullable=True),
        sa.Column('chat_id', sa.INTEGER(), nullable=True),
        sa.Column('chat_title', sa.VARCHAR(), nullable=True),
        sa.Column('datetime', sa.DATETIME(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
