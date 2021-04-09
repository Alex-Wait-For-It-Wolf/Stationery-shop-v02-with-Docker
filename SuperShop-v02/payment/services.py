from loguru import logger


@logger.catch
def _get_list_of_products_from_the_order(order):
    order_items = order.items.all()
    products = [item.product for item in order_items]
    return products
