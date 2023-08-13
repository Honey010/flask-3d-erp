"""empty message

Revision ID: eabfe06ed388
Revises: d94fc99c4706
Create Date: 2023-08-12 22:50:33.327728

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eabfe06ed388'
down_revision = 'd94fc99c4706'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('quote_info', schema=None) as batch_op:
        batch_op.add_column(sa.Column('file_name', sa.Text(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('quote_info', schema=None) as batch_op:
        batch_op.drop_column('file_name')

    # ### end Alembic commands ###