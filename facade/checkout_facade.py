from models.discounts import CartTotal, PercentageDiscount, FlatDiscount

class CheckoutFacade:
    def __init__(self, cart, inventory):
        self.cart = cart
        self.inventory = inventory
        self.discount = None  # no discount by default

    def apply_percentage_discount(self, percent):
        base_total = CartTotal(self.cart)
        self.discount = PercentageDiscount(base_total, percent)

    def apply_flat_discount(self, amount):
        base_total = CartTotal(self.cart)
        self.discount = FlatDiscount(base_total, amount)

    def checkout(self):
        if self.discount:
            total = self.discount.get_total()
        else:
            total = CartTotal(self.cart).get_total()
        self.cart.items.clear()  # empty cart
        return total
