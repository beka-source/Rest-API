"""empty message

Revision ID: 2855bc9d4eb2
Revises: 
Create Date: 2021-03-29 16:58:13.386392

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '2855bc9d4eb2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('parent',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tbl_auth_service_verify_code',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('mobile', sa.String(length=10), nullable=False),
    sa.Column('code', sa.String(), nullable=False),
    sa.Column('sum_', sa.Integer(), nullable=True),
    sa.Column('create_time', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('tbl_role',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('tbl_vacancies',
    sa.Column('vacancy_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('organizations_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('vacancy_title', sa.String(length=80), nullable=True),
    sa.Column('request_count', sa.Integer(), nullable=True),
    sa.Column('start_date', sa.Date(), nullable=False),
    sa.Column('vacancy_info', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('vacancy_id')
    )
    op.create_table('child',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('parent_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['parent_id'], ['parent.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tbl_auth_service_users',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('full_name', sa.String(length=255), nullable=False),
    sa.Column('bin', sa.String(length=20), nullable=False),
    sa.Column('username', sa.String(length=20), nullable=False),
    sa.Column('mobile', sa.String(length=10), nullable=False),
    sa.Column('email', sa.String(length=128), nullable=True),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('create_time', sa.DateTime(timezone=True), nullable=True),
    sa.Column('update_time', sa.DateTime(timezone=True), nullable=True),
    sa.Column('role_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('is_resident', sa.Boolean(), nullable=True),
    sa.Column('status', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['tbl_role.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('bin'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('mobile'),
    sa.UniqueConstraint('username')
    )
    op.create_table('ds_token_black_list',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('jti', sa.String(length=36), nullable=False),
    sa.Column('token_type', sa.String(length=10), nullable=False),
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('revoked', sa.Boolean(), nullable=False),
    sa.Column('expires', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['tbl_auth_service_users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('jti')
    )
    op.create_table('tbl_tasks',
    sa.Column('task_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('task_status', sa.String(), nullable=True),
    sa.Column('task_owner', sa.String(length=50), nullable=False),
    sa.Column('task_executor', sa.String(length=50), nullable=False),
    sa.Column('task_text', sa.String(length=255), nullable=True),
    sa.Column('create_time', sa.DateTime(timezone=True), nullable=True),
    sa.Column('update_time', sa.DateTime(timezone=True), nullable=True),
    sa.Column('from_user_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('to_user_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.ForeignKeyConstraint(['from_user_id'], ['tbl_auth_service_users.id'], ),
    sa.ForeignKeyConstraint(['to_user_id'], ['tbl_auth_service_users.id'], ),
    sa.PrimaryKeyConstraint('task_id'),
    sa.UniqueConstraint('task_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tbl_tasks')
    op.drop_table('ds_token_black_list')
    op.drop_table('tbl_auth_service_users')
    op.drop_table('child')
    op.drop_table('tbl_vacancies')
    op.drop_table('tbl_role')
    op.drop_table('tbl_auth_service_verify_code')
    op.drop_table('parent')
    # ### end Alembic commands ###