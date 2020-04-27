"""empty message

Revision ID: 47833fb40b10
Revises: 
Create Date: 2020-04-25 13:22:35.746320

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '47833fb40b10'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('farm',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=True),
    sa.Column('address', sa.String(length=120), nullable=True),
    sa.Column('city', sa.String(length=32), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('product',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.Column('farm_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['farm_id'], ['farm.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('product')
    op.drop_table('farm')
    # ### end Alembic commands ###