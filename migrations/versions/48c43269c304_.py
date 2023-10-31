"""empty message

Revision ID: 48c43269c304
Revises: 0d9d4d002734
Create Date: 2023-08-26 21:00:57.077359

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '48c43269c304'
down_revision = '0d9d4d002734'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('quote', schema=None) as batch_op:
        batch_op.add_column(sa.Column('uuid', sa.UUID(), nullable=True))
        batch_op.drop_column('uuid2')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('quote', schema=None) as batch_op:
        batch_op.add_column(sa.Column('uuid2', sa.UUID(), autoincrement=False, nullable=True))
        batch_op.drop_column('uuid')

    # ### end Alembic commands ###
