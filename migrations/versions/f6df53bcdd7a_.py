"""empty message

Revision ID: f6df53bcdd7a
Revises: 987255b1fd01
Create Date: 2020-01-17 10:13:12.941307

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f6df53bcdd7a'
down_revision = '987255b1fd01'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'Category', ['name'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'Category', type_='unique')
    # ### end Alembic commands ###
