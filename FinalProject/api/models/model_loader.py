from . import orders, order_details, recipes, sandwiches, resources, customers, ratings_reviews, payment_info, resource_management, promotions, menu_items, cart, statistics

from ..dependencies.database import engine


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
