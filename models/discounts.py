# models/discounts.py

class BaseCart:
    """Base class for cart total calculation"""
    def get_total(self):
        raise NotImplementedError


class CartTotal(BaseCart):
    """Regular cart total calculation"""
    def __init__(self, cart):
        self.cart = cart

    def get_total(self):
        total = 0
        for item in self.cart.items:
            total += item["product"].price * item["quantity"]
        return total


# Decorator Pattern
class DiscountDecorator(BaseCart):
    def __init__(self, base_cart):
        self.base_cart = base_cart

    def get_total(self):
        return self.base_cart.get_total()


class PercentageDiscount(DiscountDecorator):
    def __init__(self, base_cart, percentage):
        super().__init__(base_cart)
        self.percentage = percentage

    def get_total(self):
        total = self.base_cart.get_total()
        return total - (total * self.percentage / 100)


class FlatDiscount(DiscountDecorator):
    def __init__(self, base_cart, amount):
        super().__init__(base_cart)
        self.amount = amount

    def get_total(self):
        total = self.base_cart.get_total()
        return max(total - self.amount, 0)  # avoid negative total
