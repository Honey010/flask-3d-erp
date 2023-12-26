"""empty message

Revision ID: 7e64d82a09da
Revises: 06880d3f0c24
Create Date: 2023-08-26 20:59:24.982022

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7e64d82a09da'
down_revision = '06880d3f0c24'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('quote', schema=None) as batch_op:
        batch_op.alter_column('uuid',
               existing_type=sa.TEXT(),
               type_=sa.UUID(),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('quote', schema=None) as batch_op:
        batch_op.alter_column('uuid',
               existing_type=sa.UUID(),
               type_=sa.TEXT(),
               existing_nullable=True)

    # ### end Alembic commands ###