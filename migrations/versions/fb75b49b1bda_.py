"""empty message

Revision ID: fb75b49b1bda
Revises: f6df53bcdd7a
Create Date: 2020-01-17 11:51:55.197877

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fb75b49b1bda'
down_revision = 'f6df53bcdd7a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('User_Details', sa.Column('image', sa.String(length=1000), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('User_Details', 'image')
    # ### end Alembic commands ###
