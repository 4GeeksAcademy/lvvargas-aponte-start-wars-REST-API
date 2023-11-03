"""empty message

Revision ID: 4055f593e172
Revises: 47549e164bd1
Create Date: 2023-11-03 02:10:53.587414

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4055f593e172'
down_revision = '47549e164bd1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('planet', schema=None) as batch_op:
        batch_op.add_column(sa.Column('surface_water', sa.Integer(), nullable=True))
        batch_op.drop_column('surface_meter')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('planet', schema=None) as batch_op:
        batch_op.add_column(sa.Column('surface_meter', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.drop_column('surface_water')

    # ### end Alembic commands ###
