"""use flask security instead of flask user

Revision ID: 183ef9b0798
Revises: None
Create Date: 2015-11-21 17:20:28.051739

"""

# revision identifiers, used by Alembic.
revision = '183ef9b0798'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('roles_users',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    op.add_column('user', sa.Column('active', sa.Boolean(), nullable=True))
    op.alter_column('user', 'email',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
    op.alter_column('user', 'password',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
    op.alter_column('user', 'username',
               existing_type=sa.VARCHAR(length=50),
               nullable=True)
    op.drop_column('user', 'is_active')
    op.drop_column('user', 'reset_password_token')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('reset_password_token', sa.VARCHAR(length=100), server_default='', autoincrement=False, nullable=False))
    op.add_column('user', sa.Column('is_active', sa.BOOLEAN(), autoincrement=False, server_default=sa.schema.DefaultClause("0"), nullable=False))
    op.alter_column('user', 'username',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)
    op.alter_column('user', 'password',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
    op.alter_column('user', 'email',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
    op.drop_column('user', 'active')
    op.drop_table('roles_users')
    op.drop_table('role')
    ### end Alembic commands ###
