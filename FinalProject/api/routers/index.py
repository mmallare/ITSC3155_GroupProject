from . import (
    cart,
    menu_items,
    order_details,
    orders,
    payment_info,
    promotions,
    recipes,
    resources,
    sandwiches,
    statistics,
)


def load_routes(app):
    app.include_router(orders.router)
    app.include_router(order_details.router)
    app.include_router(cart.router)
    app.include_router(payment_info.router)
    app.include_router(recipes.router)
    app.include_router(resources.router)
    app.include_router(sandwiches.router)
    app.include_router(statistics.router)
    app.include_router(menu_items.router)
    app.include_router(promotions.router)
