# models/bundles.py

class Bundle:
    def __init__(self, name, products, discount_percentage):
        """
        products: list of product objects
        discount_percentage: discount applied on total bundle price
        """
        self.name = name
        self.products = products
        self.discount_percentage = discount_percentage

    def get_bundle_total(self):
        total = sum([p.price for p in self.products])
        discount = total * self.discount_percentage / 100
        return total - discount
