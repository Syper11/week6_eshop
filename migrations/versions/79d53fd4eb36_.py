"""empty message

Revision ID: 79d53fd4eb36
Revises: acf249be5c0a
Create Date: 2023-02-14 10:58:55.332912

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '79d53fd4eb36'
down_revision = 'acf249be5c0a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint('user_first_name_key', type_='unique')
        batch_op.drop_constraint('user_last_name_key', type_='unique')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_unique_constraint('user_last_name_key', ['last_name'])
        batch_op.create_unique_constraint('user_first_name_key', ['first_name'])

    # ### end Alembic commands ###
