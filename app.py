# app.py
from flask import Flask, jsonify, request, render_template
from models.cart import Cart
from models.inventory import InventorySingleton
from models.category import ElectronicsFactory, ClothingFactory
from models.bundles import Bundle
from facade.checkout_facade import CheckoutFacade
from utils.notifications import PriceDropNotifier

app = Flask(__name__, template_folder="templates", static_folder="static")

# ----------------- Singletons ----------------- #
inventory = InventorySingleton()
cart = Cart()
notifier = PriceDropNotifier()

# ----------------- Sample Products ----------------- #
electronics_factory = ElectronicsFactory()
clothing_factory = ClothingFactory()

# If products already added (on server reload), don't duplicate
if not inventory.get_all_products():
    sample_products = [
    electronics_factory.create_product("Laptop", 1000, 10),
    electronics_factory.create_product("Smartphone", 500, 20),
    clothing_factory.create_product("T-Shirt", 20, 50)
]


    for p in sample_products:
        inventory.add_product(p)

# ----------------- Bundles ----------------- #
bundles = [
    Bundle("Laptop + Smartphone",
           [inventory.get_product_by_name("Laptop"), inventory.get_product_by_name("Smartphone")],
           discount_percentage=10),
    Bundle("Smartphone + T-Shirt",
           [inventory.get_product_by_name("Smartphone"), inventory.get_product_by_name("T-Shirt")],
           discount_percentage=5)
]

# ----------------- Routes ----------------- #
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/products")
def get_products():
    return jsonify([p.to_dict() for p in inventory.get_all_products()])


@app.route("/bundles")
def get_bundles():
    """Return available bundles with calculated price after discount"""
    bundle_list = []
    for b in bundles:
        bundle_list.append({
            "name": b.name,
            "products": [p.name for p in b.products],
            "price": b.get_bundle_total()
        })
    return jsonify(bundle_list)


@app.route("/cart")
def view_cart():
    return jsonify(cart.to_dict())


@app.route("/cart/add", methods=["POST"])
def add_to_cart():
    data = request.json or {}
    # Prefer id (robust). Accept "id" or "product_id"
    pid = data.get("id") or data.get("product_id")
    product_name = data.get("name")
    quantity = int(data.get("quantity", 1))

    product = None
    if pid is not None:
        try:
            pid = int(pid)
            product = inventory.get_product_by_id(pid)
        except:
            product = None

    if product is None and product_name:
        product = inventory.get_product_by_name(product_name)

    if not product:
        return jsonify({"error": "Product not found"}), 404

    if product.stock < quantity:
        return jsonify({"error": "Out of stock"}), 400

    # Notify if price drops (example placeholder)
    old_price = product.price
    new_price = product.price
    if new_price < old_price:
        notifier.notify(product.name, old_price, new_price)

    cart.add_item(product, quantity)
    inventory.reduce_stock(product.name, quantity)
    return jsonify({"success": True, "cart": cart.to_dict()})


@app.route("/cart/add_bundle", methods=["POST"])
def add_bundle_to_cart():
    data = request.json or {}
    bundle_name = data.get("bundle_name")

    bundle_obj = next((b for b in bundles if b.name == bundle_name), None)
    if not bundle_obj:
        return jsonify({"error": "Bundle not found"}), 404

    # Check stock for each product in bundle
    for p in bundle_obj.products:
        if not inventory.is_in_stock(p.name, 1):
            return jsonify({"error": f"{p.name} is out of stock"}), 400

    # Add bundle products to cart
    for p in bundle_obj.products:
        cart.add_item(p, 1)
        inventory.reduce_stock(p.name, 1)

    return jsonify({"success": True, "cart": cart.to_dict(), "bundle_total": bundle_obj.get_bundle_total()})


@app.route("/checkout", methods=["POST"])
def checkout():
    data = request.json or {}
    discount_type = data.get("discount_type")
    discount_value = data.get("discount_value", 0)

    facade = CheckoutFacade(cart, inventory)

    if discount_type == "percentage":
        facade.apply_percentage_discount(discount_value)
    elif discount_type == "flat":
        facade.apply_flat_discount(discount_value)

    total = facade.checkout()
    return jsonify({"total": total})


# ------------------------------
# OPTIONAL FEATURE: WISHLIST
# ------------------------------

wishlist = []  # simple list to store wished product IDs


@app.route("/wishlist/add/<int:pid>", methods=["POST"])
def add_to_wishlist(pid):
    if pid not in wishlist:
        wishlist.append(pid)
    return jsonify({"message": "Added to wishlist", "wishlist": wishlist})


@app.route("/wishlist")
def get_wishlist():
    items = []
    for product in inventory.get_products():
        if getattr(product, "id", None) in wishlist:
            items.append(product.to_dict())
    return jsonify(items)


# ------------------------------
# OPTIONAL FEATURE: SEARCH
# ------------------------------

@app.route("/search")
def search_products():
    query = request.args.get("q", "").lower()
    results = []
    for product in inventory.get_products():
        name = (product.name or "").lower()
        category = (product.category or "").lower() if isinstance(product.category, str) else ""
        if query in name or query in category:
            results.append(product.to_dict())
    return jsonify(results)


# ------------------------------
# OPTIONAL FEATURE: FILTER BY CATEGORY
# ------------------------------

@app.route("/filter")
def filter_category():
    cat = request.args.get("category", "").lower()
    results = []
    for product in inventory.get_products():
        category = (product.category or "").lower() if isinstance(product.category, str) else ""
        if category == cat:
            results.append(product.to_dict())
    return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True)
