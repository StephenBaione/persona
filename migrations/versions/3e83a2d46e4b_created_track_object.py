"""Created Track Object

Revision ID: 3e83a2d46e4b
Revises: 2ca79f627f8b
Create Date: 2021-03-05 14:18:34.342417

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3e83a2d46e4b'
down_revision = '2ca79f627f8b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('track_object',
    sa.Column('id', sa.String(length=80), nullable=False),
    sa.Column('album_id', sa.Integer(), nullable=True),
    sa.Column('available_markets', sa.String(length=200), nullable=True),
    sa.Column('disc_number', sa.Integer(), nullable=True),
    sa.Column('duration_ms', sa.Integer(), nullable=True),
    sa.Column('explicit', sa.Boolean(), nullable=True),
    sa.Column('href', sa.String(length=80), nullable=True),
    sa.Column('is_local', sa.Boolean(), nullable=True),
    sa.Column('is_playable', sa.Boolean(), nullable=True),
    sa.Column('name', sa.String(length=80), nullable=True),
    sa.Column('popularity', sa.Integer(), nullable=True),
    sa.Column('preview_url', sa.String(length=120), nullable=True),
    sa.Column('track_number', sa.Integer(), nullable=True),
    sa.Column('type', sa.String(length=20), nullable=True),
    sa.Column('uri', sa.String(length=80), nullable=True),
    sa.ForeignKeyConstraint(['album_id'], ['album_object.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('artist_track',
    sa.Column('artist_id', sa.String(), nullable=True),
    sa.Column('track_id', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['artist_id'], ['artist_object.id'], ),
    sa.ForeignKeyConstraint(['track_id'], ['track_object.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('artist_track')
    op.drop_table('track_object')
    # ### end Alembic commands ###
