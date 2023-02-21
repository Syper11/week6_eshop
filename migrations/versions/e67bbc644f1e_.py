"""empty message

Revision ID: e67bbc644f1e
Revises: 
Create Date: 2023-02-20 15:22:05.118655

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e67bbc644f1e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('cart', schema=None) as batch_op:
        batch_op.add_column(sa.Column('product_id', sa.Integer(), nullable=False))
        batch_op.drop_constraint('cart_item_id_fkey', type_='foreignkey')
        batch_op.drop_constraint('cart_user_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'product', ['product_id'], ['item_id'], ondelete='CASCADE')
        batch_op.create_foreign_key(None, 'user', ['user_id'], ['id'], ondelete='CASCADE')
        batch_op.drop_column('item_id')
        batch_op.drop_column('cart_id')

    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.alter_column('item_name',
               existing_type=sa.VARCHAR(length=50),
               type_=sa.String(length=1000),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.alter_column('item_name',
               existing_type=sa.String(length=1000),
               type_=sa.VARCHAR(length=50),
               existing_nullable=False)

    with op.batch_alter_table('cart', schema=None) as batch_op:
        batch_op.add_column(sa.Column('cart_id', sa.INTEGER(), autoincrement=True, nullable=False))
        batch_op.add_column(sa.Column('item_id', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('cart_user_id_fkey', 'user', ['user_id'], ['id'])
        batch_op.create_foreign_key('cart_item_id_fkey', 'product', ['item_id'], ['item_id'])
        batch_op.drop_column('product_id')

    # ### end Alembic commands ###