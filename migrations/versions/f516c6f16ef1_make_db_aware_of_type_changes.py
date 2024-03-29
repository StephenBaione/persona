"""Make db aware of type changes

Revision ID: f516c6f16ef1
Revises: 603a70e42db4
Create Date: 2021-03-05 12:09:42.234489

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f516c6f16ef1'
down_revision = '603a70e42db4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('album_object', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.INTEGER(),
               type_=sa.String(length=80))

    with op.batch_alter_table('album_to_artist', schema=None) as batch_op:
        batch_op.alter_column('album_id',
               existing_type=sa.INTEGER(),
               type_=sa.String(),
               existing_nullable=True)
        batch_op.alter_column('artist_id',
               existing_type=sa.INTEGER(),
               type_=sa.String(),
               existing_nullable=True)

    with op.batch_alter_table('artist_object', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.INTEGER(),
               type_=sa.String(length=80))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('artist_object', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.String(length=80),
               type_=sa.INTEGER())

    with op.batch_alter_table('album_to_artist', schema=None) as batch_op:
        batch_op.alter_column('artist_id',
               existing_type=sa.String(),
               type_=sa.INTEGER(),
               existing_nullable=True)
        batch_op.alter_column('album_id',
               existing_type=sa.String(),
               type_=sa.INTEGER(),
               existing_nullable=True)

    with op.batch_alter_table('album_object', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.String(length=80),
               type_=sa.INTEGER())

    # ### end Alembic commands ###
