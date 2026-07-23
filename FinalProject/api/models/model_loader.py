from . import orders, order_details, recipes, sandwiches, resources, customers, ratings_reviews, payment_info, resource_management, promotions, menu_items, cart, statistics

from sqlalchemy import inspect, text
from sqlalchemy.orm import sessionmaker
from decimal import Decimal

from ..dependencies.database import engine


def _add_column_if_missing(table_name, column_name, column_ddl):
    inspector = inspect(engine)
    existing_columns = {column["name"] for column in inspector.get_columns(table_name)}
    if column_name in existing_columns:
        return

    with engine.begin() as connection:
        connection.execute(text(f"ALTER TABLE {table_name} ADD COLUMN {column_ddl}"))


def _populate_menu_items():
    """Populate menu items with prices if not already present."""
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # Check if menu items already exist
        existing_items = session.query(menu_items.MenuItem).all()
        if existing_items:
            session.close()
            return
        
        # Add sandwich items with prices
        sandwich_data = [
            ("Turkey Club", Decimal("8.99")),
            ("BLT", Decimal("6.99")),
            ("Ham & Cheese", Decimal("5.99")),
            ("Chicken Salad", Decimal("4.50")),
            ("Veggie Delight", Decimal("5.00")),
        ]
        
        for name, price in sandwich_data:
            item = menu_items.MenuItem(item_name=name, item_price=price)
            session.add(item)
        
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error populating menu items: {e}")
    finally:
        session.close()


def index():
    orders.Base.metadata.create_all(engine)
    order_details.Base.metadata.create_all(engine)
    recipes.Base.metadata.create_all(engine)
    sandwiches.Base.metadata.create_all(engine)
    resources.Base.metadata.create_all(engine)
    customers.Base.metadata.create_all(engine)
    ratings_reviews.Base.metadata.create_all(engine)
    payment_info.Base.metadata.create_all(engine)
    resource_management.Base.metadata.create_all(engine)
    promotions.Base.metadata.create_all(engine)
    menu_items.Base.metadata.create_all(engine)
    cart.Base.metadata.create_all(engine)
    statistics.Base.metadata.create_all(engine)

    _add_column_if_missing("orders", "table_number", "table_number INTEGER NOT NULL DEFAULT 1")
    _add_column_if_missing("cart", "table_number", "table_number INTEGER NOT NULL DEFAULT 1")
    
    # Populate menu items
    _populate_menu_items()
