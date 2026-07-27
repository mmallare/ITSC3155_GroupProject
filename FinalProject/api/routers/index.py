from . import orders, order_details, payment_info, recipes, resources, sandwiches, cart, statistics, menu_items, resource_management


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
    app.include_router(resource_management.router)