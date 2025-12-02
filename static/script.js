// static/script.js
let products = [];
let bundles = [];
let cart = [];

// ------------------ RENDER HELPERS ------------------
function displayProducts(list) {
    const container = document.getElementById("products-list");
    container.innerHTML = "";
    if (!list || list.length === 0) {
        container.innerHTML = "<p>No products found.</p>";
        return;
    }
    list.forEach(p => {
        const div = document.createElement("div");
        div.className = "product-card";
        div.innerHTML = `
            <h3>${p.name}</h3>
            <p>Category: ${p.category}</p>
            <p>Price: $${p.price}</p>
            <p>Stock: ${p.stock}</p>

            <button onclick="addToCart(${p.id})" ${p.stock <= 0 ? 'disabled' : ''}>Add to Cart</button>
            <button onclick="addToWishlist(${p.id})">Add to Wishlist</button>
        `;
        container.appendChild(div);
    });
}

function displayBundles(list) {
    const container = document.getElementById("bundles-list");
    if (!container) return;
    container.innerHTML = "";
    if (!list || list.length === 0) {
        container.innerHTML = "<p>No bundles available.</p>";
        return;
    }
    list.forEach(b => {
        const div = document.createElement("div");
        div.className = "product-card";
        div.innerHTML = `
            <h3>${b.name}</h3>
            <p>Products: ${b.products.join(", ")}</p>
            <p>Bundle Price: $${b.price}</p>
            <button onclick="addBundle('${b.name}')">Add Bundle</button>
        `;
        container.appendChild(div);
    });
}

// ------------------ LOADERS ------------------
async function loadProducts() {
    try {
        const res = await fetch("/products");
        products = await res.json();
        displayProducts(products);
    } catch (err) {
        console.error("Failed to load products", err);
    }
}

async function loadBundles() {
    try {
        const res = await fetch("/bundles");
        bundles = await res.json();
        displayBundles(bundles);
    } catch (err) {
        console.error("Failed to load bundles", err);
    }
}

async function loadCart() {
    try {
        const res = await fetch("/cart");
        cart = await res.json();
        const container = document.getElementById("cart-list");
        container.innerHTML = "";
        let total = 0;
        if (!cart || cart.length === 0) {
            container.innerHTML = "<p>Cart is empty.</p>";
        } else {
            cart.forEach(item => {
                const div = document.createElement("div");
                div.className = "cart-row";
                div.innerHTML = `
                    <div>${item.name} x ${item.quantity}</div>
                    <div>$${item.price}</div>
                `;
                container.appendChild(div);
                total += item.price * item.quantity;
            });
        }
        document.getElementById("cart-total").innerText = total.toFixed(2);
    } catch (err) {
        console.error("Failed to load cart", err);
    }
}

// ------------------ ACTIONS ------------------
async function addToCart(id) {
    try {
        const res = await fetch("/cart/add", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ id: id, quantity: 1 })
        });
        const data = await res.json();
        if (data.error) alert(data.error);
        else {
            alert("Added to cart!");
            await loadProducts();
            await loadCart();
            await loadBundles();
        }
    } catch (err) {
        console.error("Add to cart error:", err);
        alert("Error adding to cart");
    }
}

async function addBundle(bundleName) {
    try {
        const res = await fetch("/cart/add_bundle", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ bundle_name: bundleName })
        });
        const data = await res.json();
        if (data.error) alert(data.error);
        else {
            alert("Bundle added!");
            await loadProducts();
            await loadCart();
            await loadBundles();
        }
    } catch (err) {
        console.error("Add bundle error:", err);
        alert("Error adding bundle");
    }
}

async function addToWishlist(id) {
    try {
        const res = await fetch(`/wishlist/add/${id}`, { method: "POST" });
        const data = await res.json();
        if (data && data.message) alert(data.message);
    } catch (err) {
        console.error("Wishlist error:", err);
    }
}

async function loadWishlist() {
    try {
        const res = await fetch("/wishlist");
        const items = await res.json();
        // Reuse displayProducts for wishlist (it expects array of products)
        displayProducts(items);
    } catch (err) {
        console.error("Failed to load wishlist", err);
    }
}

async function searchProducts() {
    const q = (document.getElementById("searchInput").value || "").trim();
    if (!q) {
        displayProducts(products);
        return;
    }
    try {
        const res = await fetch(`/search?q=${encodeURIComponent(q)}`);
        const results = await res.json();
        displayProducts(results);
    } catch (err) {
        console.error("Search failed", err);
    }
}

function filterCategory() {
    const cat = document.getElementById("filterSelect").value;
    if (!cat) return displayProducts(products);
    fetch(`/filter?category=${encodeURIComponent(cat)}`)
        .then(r => r.json())
        .then(list => displayProducts(list))
        .catch(err => console.error("Filter failed", err));
}

function clearCart() {
    // For demo: perform checkout with zero discount to clear cart
    fetch("/checkout", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ discount_type: "flat", discount_value: 0 })
    }).then(_ => {
        alert("Cart cleared");
        loadProducts();
        loadCart();
        loadBundles();
    });
}

async function checkout() {
    if (!cart || cart.length === 0) {
        alert("Cart is empty!");
        return;
    }
    const discountType = prompt("Enter discount type (percentage/flat/none):").toLowerCase();
    let discountValue = 0;
    if (discountType === "percentage" || discountType === "flat") {
        discountValue = parseFloat(prompt("Enter discount value:")) || 0;
    }
    try {
        const res = await fetch("/checkout", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ discount_type: discountType === "none" ? None : discountType, discount_value: discountValue })
        });
        const data = await res.json();
        alert(`Checkout complete! Total: $${data.total}`);
        await loadProducts();
        await loadCart();
        await loadBundles();
    } catch (err) {
        console.error("Checkout failed", err);
    }
}

// ------------------ INIT ------------------
window.onload = async function() {
    await loadProducts();
    await loadBundles();
    await loadCart();
};
