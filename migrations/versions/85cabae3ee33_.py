"""empty message

Revision ID: 85cabae3ee33
Revises: 2029924e1fbb
Create Date: 2021-04-12 16:02:36.088820

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '85cabae3ee33'
down_revision = '2029924e1fbb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tbl_tasks', sa.Column('deadline', sa.Date(), nullable=True))
    op.drop_index('ix_tbl_tasks_end_time', table_name='tbl_tasks')
    op.create_index(op.f('ix_tbl_tasks_deadline'), 'tbl_tasks', ['deadline'], unique=False)
    op.drop_column('tbl_tasks', 'end_time')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tbl_tasks', sa.Column('end_time', sa.DATE(), autoincrement=False, nullable=True))
    op.drop_index(op.f('ix_tbl_tasks_deadline'), table_name='tbl_tasks')
    op.create_index('ix_tbl_tasks_end_time', 'tbl_tasks', ['end_time'], unique=False)
    op.drop_column('tbl_tasks', 'deadline')
    # ### end Alembic commands ###
