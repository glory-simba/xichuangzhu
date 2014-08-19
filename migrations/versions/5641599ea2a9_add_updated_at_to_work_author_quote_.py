"""add updated_at to Work, Author, Quote model

Revision ID: 5641599ea2a9
Revises: 1fc20d4b117a
Create Date: 2014-07-23 19:42:44.589944

"""

# revision identifiers, used by Alembic.
revision = '5641599ea2a9'
down_revision = '1fc20d4b117a'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('author', sa.Column('updated_at', sa.DateTime(), nullable=True))
    op.add_column('quote', sa.Column('updated_at', sa.DateTime(), nullable=True))
    op.add_column('work', sa.Column('updated_at', sa.DateTime(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('work', 'updated_at')
    op.drop_column('quote', 'updated_at')
    op.drop_column('author', 'updated_at')
    ### end Alembic commands ###