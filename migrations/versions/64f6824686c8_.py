"""empty message

Revision ID: 64f6824686c8
Revises: ca9ea72d8d14
Create Date: 2023-08-17 00:27:25.393674

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '64f6824686c8'
down_revision = 'ca9ea72d8d14'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('status', sa.Integer(), server_default='1', nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.create_foreign_key(None, 'roles', ['role_id'], ['id'], ondelete='CASCADE')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')

    op.drop_table('roles')
    # ### end Alembic commands ###