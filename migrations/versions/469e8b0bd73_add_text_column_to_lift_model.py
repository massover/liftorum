"""Add text column to lift model

Revision ID: 469e8b0bd73
Revises: 30adcac68f1
Create Date: 2015-12-24 11:04:32.272982

"""

# revision identifiers, used by Alembic.
revision = '469e8b0bd73'
down_revision = '30adcac68f1'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('lift', sa.Column('text', sa.Text(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('lift', 'text')
    ### end Alembic commands ###
