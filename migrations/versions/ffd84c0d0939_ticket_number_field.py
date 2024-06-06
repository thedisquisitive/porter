"""ticket number field

Revision ID: ffd84c0d0939
Revises: 30575dc57526
Create Date: 2024-06-05 19:45:26.558101

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ffd84c0d0939'
down_revision = '30575dc57526'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('order', schema=None) as batch_op:
        batch_op.add_column(sa.Column('sc_ticket', sa.String(length=120), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('order', schema=None) as batch_op:
        batch_op.drop_column('sc_ticket')

    # ### end Alembic commands ###
