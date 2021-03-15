"""Added Spotify to Tracks relationship for tracking saved tracks

Revision ID: b50cdc5c575c
Revises: c68f27259c7f
Create Date: 2021-03-15 09:08:15.580295

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b50cdc5c575c'
down_revision = 'c68f27259c7f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('spotify_to_saved_tracks',
    sa.Column('spotify_id', sa.Integer(), nullable=True),
    sa.Column('track_id', sa.String(length=80), nullable=True),
    sa.ForeignKeyConstraint(['spotify_id'], ['spotify.id'], ),
    sa.ForeignKeyConstraint(['track_id'], ['track_object.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('spotify_to_saved_tracks')
    # ### end Alembic commands ###
