from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy import Integer, String, Text, ForeignKey, Boolean


# revision identifiers, used by Alembic.
revision = '39aad976c109'
down_revision = 'e22458a4dac6'
branch_labels = None
depends_on = None


def upgrade():
    # 1. Переименовываем старую таблицу
    op.rename_table('repair_services', 'repair_services_old')

    # 2. Создаём новую таблицу с nullable полем price и duration
    op.create_table(
        'repair_services',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('city_id', sa.Integer, sa.ForeignKey('city.id')),
        sa.Column('service_id', sa.String),
        sa.Column('name', sa.String),
        sa.Column('description', sa.String),
        sa.Column('duration', sa.String, nullable=True),
        sa.Column('price', sa.Integer, nullable=True),
        sa.Column('category_id', sa.String),
        sa.Column('product_id', sa.String),
        sa.Column('model', sa.String),
    )

    # 3. Копируем данные
    op.execute("""
        INSERT INTO repair_services (
            id, city_id, service_id, name, description, duration,
            price, category_id, product_id, model
        )
        SELECT id, city_id, service_id, name, description, duration,
               price, category_id, product_id, model
        FROM repair_services_old
    """)

    # 4. Удаляем старую таблицу
    op.drop_table('repair_services_old')


def downgrade():
    # аналогично, если хочешь откат
    op.rename_table('repair_services', 'repair_services_new')

    op.create_table(
        'repair_services',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('city_id', sa.Integer, sa.ForeignKey('city.id')),
        sa.Column('service_id', sa.String),
        sa.Column('name', sa.String),
        sa.Column('description', sa.String),
        sa.Column('duration', sa.String, nullable=False),
        sa.Column('price', sa.Integer, nullable=False),
        sa.Column('category_id', sa.String),
        sa.Column('product_id', sa.String),
        sa.Column('model', sa.String),
    )

    op.execute("""
        INSERT INTO repair_services (
            id, city_id, service_id, name, description, duration,
            price, category_id, product_id, model
        )
        SELECT id, city_id, service_id, name, description, duration,
               price, category_id, product_id, model
        FROM repair_services_new
    """)

    op.drop_table('repair_services_new')