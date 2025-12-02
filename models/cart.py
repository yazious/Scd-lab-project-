# models/cart.py
class Cart:
    def __init__(self):
        self.items = []

    def add_item(self, product, quantity):
        self.items.append({"product": product, "quantity": quantity})

    def to_dict(self):
        return [
            {"name": item["product"].name, "price": item["product"].price, "quantity": item["quantity"]}
            for item in self.items
        ]

# Builder Pattern
class CartBuilder:
    def create_cart(self):
        return Cart()
