"""initial

Revision ID: bcd83a064841
Revises: 
Create Date: 2024-12-19 13:26:38.187731

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bcd83a064841'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('url_map',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('original', sa.String(), nullable=False),
    sa.Column('short', sa.String(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('short')
    )
    with op.batch_alter_table('url_map', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_url_map_timestamp'), ['timestamp'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('url_map', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_url_map_timestamp'))

    op.drop_table('url_map')
    # ### end Alembic commands ###
