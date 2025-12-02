# models/product.py
class Product:
    _id_counter = 1

    def __init__(self, category, name, price, stock):
        # assign an auto-increment id for each product
        self.id = Product._id_counter
        Product._id_counter += 1

        self.category = category  # can be string or object depending on your implementation
        self.name = name
        self.price = float(price)
        self.stock = int(stock)

    def to_dict(self):
        # send a consistent JSON shape to frontend
        return {
            "id": self.id,
            "category": self.category if isinstance(self.category, str) else (self.category if self.category else "General"),
            "name": self.name,
            "price": self.price,
            "stock": self.stock
        }

# Factory Method
class ProductFactory:
    def create_product(self, category, name, price, stock):
        return Product(category, name, price, stock)
