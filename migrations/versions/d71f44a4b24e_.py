"""empty message

Revision ID: d71f44a4b24e
Revises: 8fc7373879db
Create Date: 2023-06-24 10:45:13.480818

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd71f44a4b24e'
down_revision = '8fc7373879db'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('quote_info', schema=None) as batch_op:
        batch_op.drop_constraint('quote_info_quote_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'quote', ['quote_id'], ['id'], ondelete='CASCADE')

    with op.batch_alter_table('unit_quote', schema=None) as batch_op:
        batch_op.drop_constraint('unit_quote_quote_info_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'quote_info', ['quote_info_id'], ['id'], ondelete='CASCADE')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('unit_quote', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('unit_quote_quote_info_id_fkey', 'quote_info', ['quote_info_id'], ['id'])

    with op.batch_alter_table('quote_info', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('quote_info_quote_id_fkey', 'quote', ['quote_id'], ['id'])

    # ### end Alembic commands ###