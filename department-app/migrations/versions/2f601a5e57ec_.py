"""empty message

Revision ID: 2f601a5e57ec
Revises: 094ca38a0bfa
Create Date: 2020-11-20 00:33:34.779558

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2f601a5e57ec'
down_revision = '094ca38a0bfa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('departments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('avg_salary', sa.Float(), server_default='0.0', nullable=False),
    sa.Column('count_employees', sa.Integer(), server_default='0', nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('employees',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=False),
    sa.Column('birthday', sa.Date(), nullable=True),
    sa.Column('salary', sa.Float(), nullable=False),
    sa.Column('department_id', sa.Integer(), nullable=False),
    sa.Column('working_since', sa.Date(), nullable=True),
    sa.ForeignKeyConstraint(['department_id'], ['departments.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('employees')
    op.drop_table('departments')
    # ### end Alembic commands ###
