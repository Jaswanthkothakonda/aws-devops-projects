let products = [];
let cart = [];
let activeCategory = "all";

async function loadMenu() {
    const grid = document.getElementById("product-grid");

    try {
        const response = await fetch("/api/menu");
        if (!response.ok) throw new Error("Menu unavailable");

        products = await response.json();
        renderMenu();
    } catch (error) {
        grid.innerHTML = "<p>Unable to load menu. Please try again.</p>";
        console.error(error);
    }
}

function escapeHTML(value) {
    return String(value).replace(/[&<>"']/g, char => ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#39;"
    })[char]);
}

// Product image or placeholder
function renderProductImage(product) {
    if (product.image_url) {
        return `
            <img src="${escapeHTML(product.image_url)}"
                 alt="${escapeHTML(product.name)}"
                 loading="lazy"
                 onerror="this.outerHTML='<div class=&quot;product-image-placeholder&quot;>${escapeHTML(product.name)}</div>'">
        `;
    }

    return `
        <div class="product-image-placeholder">
            ${escapeHTML(product.name)}
        </div>
    `;
}

// Nutrition information
function renderNutrition(product) {
    const fields = [
        ["Serving Size", product.serving_size_g, "g"],
        ["Protein", product.protein_g, "g"],
        ["Carbs", product.carbs_g, "g"],
        ["Calories", product.calories_kcal, "kcal"],
        ["Fibre", product.fibre_g, "g"]
    ];

    const available = fields.filter(
        ([, value]) => value !== null && value !== undefined
    );

    if (!available.length) return "";

    return `
        <div class="nutrition-panel">
            <div class="nutrition-title">
                NUTRITION INFORMATION
            </div>

            <div class="nutrition-grid">
                ${available.map(([label, value, unit]) => `
                    <div class="nutrition-item">
                        <span>${label}</span>
                        <strong>${Number(value)} ${unit}</strong>
                    </div>
                `).join("")}
            </div>
        </div>
    `;
}

// Display products
function renderMenu() {
    const grid = document.getElementById("product-grid");
    const search = document.getElementById("menu-search")
        .value.toLowerCase();

    const filtered = products.filter(product => {
        const matchesCategory =
            activeCategory === "all" ||
            product.category === activeCategory;

        const matchesSearch =
            product.name.toLowerCase().includes(search) ||
            (product.description || "").toLowerCase().includes(search);

        return matchesCategory && matchesSearch;
    });

    if (!filtered.length) {
        grid.innerHTML = "<p>No meals found. Try another search.</p>";
        return;
    }

    grid.innerHTML = filtered.map(product => `
        <article class="product-card">

            ${renderProductImage(product)}

            <div class="product-info">

                <span class="tag">
                    ${escapeHTML(product.category)}
                </span>

                <h3>${escapeHTML(product.name)}</h3>

                <p>${escapeHTML(product.description || "")}</p>

                ${renderNutrition(product)}

                <div class="product-bottom">

                    <span class="product-price">
                        ₹${Number(product.price).toFixed(2)}
                    </span>

                    <button class="add-button"
                        onclick="addToCart(${Number(product.id)})">
                        Add +
                    </button>

                </div>
            </div>
        </article>
    `).join("");
}

// Category filtering
function filterCategory(category) {
    activeCategory = category;

    document.querySelectorAll(".category").forEach(button => {
        button.classList.toggle(
            "active",
            button.dataset.category === category
        );
    });

    renderMenu();
}

// Search
function filterMenu() {
    renderMenu();
}

// Add product to cart
function addToCart(productId) {
    const product = products.find(p => p.id === productId);
    if (!product) return;

    const existing = cart.find(item => item.id === productId);

    if (existing) {
        existing.quantity++;
    } else {
        cart.push({...product, quantity: 1});
    }

    updateCart();
}

// Change product quantity
function changeQuantity(productId, change) {
    const item = cart.find(p => p.id === productId);
    if (!item) return;

    item.quantity += change;

    if (item.quantity <= 0) {
        cart = cart.filter(p => p.id !== productId);
    }

    updateCart();
}

// Remove product from cart
function removeFromCart(productId) {
    cart = cart.filter(p => p.id !== productId);
    updateCart();
}

// Update cart display
function updateCart() {
    const count = cart.reduce(
        (sum, item) => sum + item.quantity, 0
    );

    const total = cart.reduce(
        (sum, item) => sum + Number(item.price) * item.quantity, 0
    );

    document.getElementById("cart-count").textContent = count;

    document.getElementById("cart-total").textContent =
        total.toFixed(2);

    document.getElementById("cart-items").innerHTML =
        cart.map(item => `
            <div class="cart-item">
                <div>
                    <strong>${escapeHTML(item.name)}</strong>

                    <p>
                        ₹${Number(item.price).toFixed(2)}
                        × ${item.quantity}
                    </p>

                    <button onclick="changeQuantity(${item.id}, -1)">
                        −
                    </button>

                    <button onclick="changeQuantity(${item.id}, 1)">
                        +
                    </button>
                </div>

                <button onclick="removeFromCart(${item.id})">
                    Remove
                </button>
            </div>
        `).join("");

    if (!cart.length) {
        document.getElementById("cart-items").textContent =
            "Your cart is empty.";
    }
}

// Toggle cart panel
function toggleCart() {
    document.getElementById("cart-panel")
        .classList.toggle("open");
}

// Checkout
function checkout() {
    if (!cart.length) {
        alert("Your cart is empty!");
        return;
    }

    alert("Checkout will be connected to the BeastEats order API next.");
}

// Initialize application
document.addEventListener("DOMContentLoaded", () => {
    loadMenu();
    updateCart();
});