"""empty message

Revision ID: 6f4d4cc6e756
Revises: 046ac512a351
Create Date: 2021-04-13 18:53:00.882405

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6f4d4cc6e756'
down_revision = '046ac512a351'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'tbl_comment', ['comment_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'tbl_comment', type_='unique')
    # ### end Alembic commands ###
