"""Create tables for File and SensitiveData"""

# revision identifiers, used by Alembic.
revision = '568aa682f6f6'
down_revision = None  # Set this to None if it's the first migration, or to the previous revision ID

from alembic import op
import sqlalchemy as sa

def upgrade():
    # Create the 'file' table
    op.create_table(
        'file',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('upload_date', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # Create the 'sensitive_data' table
    op.create_table(
        'sensitive_data',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('type', sa.String(length=50), nullable=False),
        sa.Column('content', sa.String(length=200), nullable=False),
        sa.Column('classification', sa.String(length=50), nullable=False),
        sa.Column('file_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['file_id'], ['file.id']),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    # Drop the 'sensitive_data' table
    op.drop_table('sensitive_data')

    # Drop the 'file' table
    op.drop_table('file')
