# utils/notifications.py

class PriceDropNotifier:
    def __init__(self):
        self.subscribers = {}  # {product_name: [email1, email2]}

    def subscribe(self, product_name, user_email):
        if product_name not in self.subscribers:
            self.subscribers[product_name] = []
        self.subscribers[product_name].append(user_email)

    def notify(self, product_name, old_price, new_price):
        if product_name in self.subscribers:
            for email in self.subscribers[product_name]:
                print(f"Notification to {email}: {product_name} price dropped from {old_price} to {new_price}!")
