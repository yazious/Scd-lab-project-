# models/inventory.py
class InventorySingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.products = []
        return cls._instance

    def add_product(self, product):
        # avoid adding the same product object twice
        if product not in self.products:
            self.products.append(product)

    def get_all_products(self):
        return self.products

    # alias used by optional endpoints
    def get_products(self):
        return self.products

    def get_product_by_id(self, pid):
        for p in self.products:
            if getattr(p, "id", None) == pid:
                return p
        return None

    def get_product_by_name(self, name):
        for p in self.products:
            if p.name == name:
                return p
        return None

    def is_in_stock(self, name, quantity):
        product = self.get_product_by_name(name)
        return product and product.stock >= int(quantity)

    def reduce_stock(self, name, quantity):
        product = self.get_product_by_name(name)
        if product:
            product.stock = max(product.stock - int(quantity), 0)

    def add_stock(self, name, quantity):
        product = self.get_product_by_name(name)
        if product:
            product.stock += int(quantity)
