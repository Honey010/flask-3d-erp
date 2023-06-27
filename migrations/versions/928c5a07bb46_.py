"""empty message

Revision ID: 928c5a07bb46
Revises: 6ccb541d6188
Create Date: 2023-06-26 20:55:48.142496

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '928c5a07bb46'
down_revision = '6ccb541d6188'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('quote', schema=None) as batch_op:
        batch_op.drop_column('grand_total2')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('quote', schema=None) as batch_op:
        batch_op.add_column(sa.Column('grand_total2', sa.NUMERIC(), autoincrement=False, nullable=True))

    # ### end Alembic commands ###