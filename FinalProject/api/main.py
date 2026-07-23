import uvicorn
import logging
import sys
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from .routers import index as indexRoute
from .models import model_loader
from .dependencies.config import conf
from .models.menu_items import MenuItem
from .dependencies.database import SessionLocal

# Configure logging with console handler
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('app.log', mode='a')
    ]
)

logger = logging.getLogger(__name__)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model_loader.index()
indexRoute.load_routes(app)

@app.get("/menu-items")
def get_menu_items():
    """Fetch all menu items with prices."""
    db = SessionLocal()
    try:
        items = db.query(MenuItem).all()
        logger.info(f"Retrieved {len(items)} menu items")
        return [
            {
                "id": item.id,
                "item_name": item.item_name,
                "item_price": float(item.item_price)
            }
            for item in items
        ]
    except Exception as e:
        logger.error(f"Error retrieving menu items: {e}")
        return []
    finally:
        db.close()


@app.get("/", response_class=HTMLResponse)
def home():
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Sandwich Maker Order Placement Dashboard</title>
    <style>
        :root {
            color-scheme: light;
            --bg: #f4efe6;
            --panel: rgba(255, 255, 255, 0.86);
            --panel-strong: #ffffff;
            --text: #1f2937;
            --muted: #6b7280;
            --accent: #c2410c;
            --accent-2: #0f766e;
            --border: rgba(31, 41, 55, 0.12);
            --shadow: 0 24px 60px rgba(31, 41, 55, 0.12);
        }

        * { box-sizing: border-box; }
        body {
            margin: 0;
            min-height: 100vh;
            font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            color: var(--text);
            background:
                radial-gradient(circle at top left, rgba(194, 65, 12, 0.18), transparent 30%),
                radial-gradient(circle at top right, rgba(15, 118, 110, 0.16), transparent 25%),
                linear-gradient(180deg, #fffaf3 0%, var(--bg) 100%);
        }

        .shell {
            max-width: 1200px;
            margin: 0 auto;
            padding: 32px 20px 48px;
        }

        .hero {
            display: grid;
            grid-template-columns: 1.4fr 1fr;
            gap: 24px;
            align-items: stretch;
            margin-bottom: 24px;
        }

        .hero-card, .panel {
            background: var(--panel);
            backdrop-filter: blur(14px);
            border: 1px solid var(--border);
            border-radius: 24px;
            box-shadow: var(--shadow);
        }

        .hero-card {
            padding: 28px;
            position: relative;
            overflow: hidden;
        }

        .hero-card::after {
            content: "";
            position: absolute;
            inset: auto -80px -80px auto;
            width: 220px;
            height: 220px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(194, 65, 12, 0.18), transparent 70%);
            pointer-events: none;
        }

        h1 {
            margin: 0 0 10px;
            font-size: clamp(2rem, 5vw, 3.8rem);
            line-height: 0.98;
            letter-spacing: -0.05em;
        }

        .lede {
            max-width: 64ch;
            margin: 0 0 18px;
            color: var(--muted);
            font-size: 1rem;
            line-height: 1.6;
        }

        .chips {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }

        .chip {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 10px 14px;
            border-radius: 999px;
            background: rgba(255, 255, 255, 0.72);
            border: 1px solid var(--border);
            font-size: 0.92rem;
            color: #374151;
        }

        .status {
            margin-top: 18px;
            padding: 12px 14px;
            border-radius: 16px;
            background: rgba(15, 118, 110, 0.08);
            color: #115e59;
            border: 1px solid rgba(15, 118, 110, 0.18);
            min-height: 48px;
            display: flex;
            align-items: center;
        }

        .grid {
            display: grid;
            grid-template-columns: 1fr 1.3fr;
            gap: 24px;
        }

        .panel {
            padding: 20px;
        }

        .panel h2 {
            margin: 0 0 12px;
            font-size: 1.15rem;
            letter-spacing: -0.02em;
        }

        .reference-card {
            margin-top: 14px;
            padding: 16px;
            border-radius: 18px;
            border: 1px solid var(--border);
            background: rgba(255, 255, 255, 0.72);
        }

        .reference-card h3 {
            margin: 0 0 10px;
            font-size: 0.95rem;
            letter-spacing: -0.01em;
        }

        .reference-list {
            display: grid;
            gap: 8px;
            margin: 0;
            padding: 0;
            list-style: none;
        }

        .reference-list li {
            display: flex;
            justify-content: space-between;
            gap: 12px;
            font-size: 0.92rem;
            color: #374151;
        }

        .reference-id {
            font-weight: 800;
            color: var(--accent);
            white-space: nowrap;
        }

        .field {
            display: grid;
            gap: 6px;
            margin-bottom: 14px;
        }

        label {
            font-size: 0.85rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: var(--muted);
        }

        input, textarea {
            width: 100%;
            padding: 12px 14px;
            border-radius: 14px;
            border: 1px solid var(--border);
            background: rgba(255, 255, 255, 0.92);
            color: var(--text);
            font: inherit;
            outline: none;
            transition: border-color 0.15s ease, transform 0.15s ease, box-shadow 0.15s ease;
        }

        input:focus, textarea:focus {
            border-color: rgba(194, 65, 12, 0.6);
            box-shadow: 0 0 0 4px rgba(194, 65, 12, 0.12);
        }

        textarea { min-height: 92px; resize: vertical; }

        .actions {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 14px;
        }

        button {
            border: 0;
            border-radius: 14px;
            padding: 12px 16px;
            font: inherit;
            font-weight: 700;
            cursor: pointer;
            transition: transform 0.15s ease, opacity 0.15s ease, box-shadow 0.15s ease;
        }

        button:hover { transform: translateY(-1px); }
        button.primary {
            background: linear-gradient(135deg, var(--accent), #ea580c);
            color: #fff;
            box-shadow: 0 12px 28px rgba(194, 65, 12, 0.26);
        }
        button.secondary {
            background: rgba(15, 118, 110, 0.1);
            color: #115e59;
        }
        button.ghost {
            background: rgba(31, 41, 55, 0.06);
            color: var(--text);
        }
        button.danger {
            background: rgba(220, 38, 38, 0.12);
            color: #991b1b;
        }

        .toolbar {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            margin-bottom: 16px;
            align-items: center;
        }

        .list {
            display: grid;
            gap: 12px;
        }

        .order-card {
            padding: 16px;
            border-radius: 18px;
            background: var(--panel-strong);
            border: 1px solid var(--border);
            display: grid;
            gap: 10px;
        }

        .order-top {
            display: flex;
            justify-content: space-between;
            gap: 10px;
            align-items: start;
        }

        .order-title {
            font-weight: 800;
            font-size: 1rem;
        }

        .muted { color: var(--muted); }
        .meta {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            font-size: 0.9rem;
            color: var(--muted);
        }

        .empty {
            padding: 20px;
            border-radius: 18px;
            border: 1px dashed rgba(31, 41, 55, 0.18);
            color: var(--muted);
            text-align: center;
        }

        .inline {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 12px;
        }

        @media (max-width: 960px) {
            .hero, .grid { grid-template-columns: 1fr; }
        }

        @media (max-width: 640px) {
            .shell { padding-inline: 14px; }
            .hero-card, .panel { border-radius: 20px; }
            .inline { grid-template-columns: 1fr; }
            .order-top { flex-direction: column; }
        }
    </style>
</head>
<body>
    <div class="shell">
        <section class="hero">
            <div class="hero-card">
                <h1>Sandwich Maker Order Placement Dashboard</h1>
                <p class="lede">A lightweight dashboard for staging cart items first, then confirming them into an order record. This page talks to the FastAPI backend on the same origin.</p>
                <div class="chips">
                    <span class="chip">Live CRUD</span>
                    <span class="chip">No page reloads</span>
                    <span class="chip">Table-based carts</span>
                </div>
                <div id="status" class="status">Ready. Load orders or carts, or create a new one.</div>
            </div>
            <div class="panel">
                <h2>Quick Actions</h2>
                <div class="field">
                    <label for="table-number">Table Number</label>
                    <input id="table-number" type="number" min="1" step="1" placeholder="4" />
                </div>
                <div class="toolbar">
                    <button class="primary" type="button" onclick="confirmOrder()">Confirm &amp; create order</button>
                    <button class="secondary" type="button" onclick="loadOrders()">Refresh orders</button>
                    <button class="secondary" type="button" onclick="loadCarts()">Refresh cart</button>
                    <button class="ghost" type="button" onclick="loadDashboard()">Refresh all</button>
                    <button class="ghost" type="button" onclick="resetForm()">Reset form</button>
                </div>
                <p class="muted" style="margin: 0; line-height: 1.6;">
                    Use the shared table number to stage cart items, then confirm the order to create the order record. Clicking <strong>Edit</strong> loads an item into the matching form.
                </p>
            </div>
        </section>

        <section class="grid">
            <div class="panel">
                <h2>Create or Update Order</h2>
                <form id="order-form">
                    <input id="order-id" type="hidden" />
                    <div class="field">
                        <label for="customer-name">Customer Name</label>
                        <input id="customer-name" name="customer_name" type="text" placeholder="Jordan Lee" required />
                    </div>
                    <div class="field">
                        <label for="description">Description</label>
                        <textarea id="description" name="description" placeholder="2 turkey club sandwiches, no onions"></textarea>
                    </div>
                    <div class="actions">
                        <button class="primary" type="submit">Confirm Order</button>
                        <button class="danger" type="button" onclick="clearOrderEditState()">Cancel Edit</button>
                    </div>
                </form>
            </div>

            <div class="panel">
                <h2>Create or Update Cart Item</h2>
                <form id="cart-form">
                    <input id="cart-id" type="hidden" />
                    <div class="inline">
                        <div class="field">
                            <label for="cart-subtotal">Subtotal</label>
                            <input id="cart-subtotal" name="subtotal" type="number" min="0" step="0.01" placeholder="19.50" required />
                        </div>
                        <div class="field">
                            <label for="cart-quantity">Quantity</label>
                            <input id="cart-quantity" name="quantity" type="number" min="1" step="1" placeholder="2" required />
                        </div>
                    </div>
                    <div class="field">
                        <label for="cart-coupon">Coupon</label>
                        <input id="cart-coupon" name="coupon" type="text" placeholder="SAVE10" />
                    </div>
                    <div class="inline">
                        <div class="field">
                            <label for="cart-customer-id">Customer ID</label>
                            <input id="cart-customer-id" name="customer_id" type="number" min="1" step="1" placeholder="1" required />
                        </div>
                        <div class="field">
                            <label for="cart-menu-item-id">Menu Item ID</label>
                            <input id="cart-menu-item-id" name="menu_item_id" type="number" min="1" step="1" placeholder="3" required />
                        </div>
                    </div>
                    <div class="actions">
                        <button class="primary" type="submit">Add to Cart</button>
                        <button class="danger" type="button" onclick="clearCartEditState()">Cancel Edit</button>
                    </div>
                </form>

                <div class="reference-card">
                    <h3>Popular Sandwich Options</h3>
                    <ul class="reference-list">
                        <li><span>Turkey Club</span><span class="reference-id">Item ID 1</span></li>
                        <li><span>BLT</span><span class="reference-id">Item ID 2</span></li>
                        <li><span>Ham &amp; Cheese</span><span class="reference-id">Item ID 3</span></li>
                        <li><span>Chicken Salad</span><span class="reference-id">Item ID 4</span></li>
                        <li><span>Veggie Delight</span><span class="reference-id">Item ID 5</span></li>
                    </ul>
                </div>
            </div>

            <div class="panel">
                <h2>Orders</h2>
                <div id="orders" class="list"></div>
            </div>

            <div class="panel">
                <h2>Cart</h2>
                <div id="carts" class="list"></div>
            </div>
        </section>
    </div>

    <script>
        const statusBox = document.getElementById('status');
        const ordersBox = document.getElementById('orders');
        const cartsBox = document.getElementById('carts');
        const tableNumberInput = document.getElementById('table-number');
        const form = document.getElementById('order-form');
        const cartForm = document.getElementById('cart-form');
        const orderIdInput = document.getElementById('order-id');
        const customerNameInput = document.getElementById('customer-name');
        const descriptionInput = document.getElementById('description');
        const cartIdInput = document.getElementById('cart-id');
        const cartSubtotalInput = document.getElementById('cart-subtotal');
        const cartCouponInput = document.getElementById('cart-coupon');
        const cartQuantityInput = document.getElementById('cart-quantity');
        const cartCustomerIdInput = document.getElementById('cart-customer-id');
        const cartMenuItemIdInput = document.getElementById('cart-menu-item-id');

        // Store menu items globally for price lookup
        window.menuItems = {};
        
        // Load menu items on page load
        async function loadMenuItems() {
            try {
                const response = await fetch('/menu-items');
                const items = await response.json();
                window.menuItems = {};
                items.forEach(item => {
                    window.menuItems[item.id] = item;
                });
                console.log(`[MENU] Loaded ${items.length} menu items with prices`);
            } catch (error) {
                console.error(`[MENU] Error loading menu items:`, error);
            }
        }
        
        // Auto-calculate subtotal based on menu item price and quantity
        function updateSubtotal() {
            const menuItemId = Number(cartMenuItemIdInput.value);
            const quantity = Number(cartQuantityInput.value);
            
            if (menuItemId && window.menuItems[menuItemId] && quantity > 0) {
                const price = window.menuItems[menuItemId].item_price;
                const subtotal = (price * quantity).toFixed(2);
                cartSubtotalInput.value = subtotal;
                console.log(`[CART] Auto-calculated subtotal: ${window.menuItems[menuItemId].item_name} (ID ${menuItemId}) x ${quantity} = $${subtotal}`);
            }
        }

        function getTableNumber() {
            const value = Number(tableNumberInput.value);
            return Number.isInteger(value) && value > 0 ? value : null;
        }

        function requireTableNumber() {
            const tableNumber = getTableNumber();
            if (!tableNumber) {
                setStatus('Table number is required.', true);
                return null;
            }
            return tableNumber;
        }

        function filterByTableNumber(items) {
            const tableNumber = getTableNumber();
            if (!tableNumber) {
                return items || [];
            }
            return (items || []).filter((item) => Number(item.table_number) === tableNumber);
        }

        function setStatus(message, error = false) {
            statusBox.textContent = message;
            statusBox.style.background = error ? 'rgba(220, 38, 38, 0.08)' : 'rgba(15, 118, 110, 0.08)';
            statusBox.style.color = error ? '#991b1b' : '#115e59';
            statusBox.style.borderColor = error ? 'rgba(220, 38, 38, 0.18)' : 'rgba(15, 118, 110, 0.18)';
        }

        function resetForm() {
            clearOrderEditState();
            clearCartEditState();
            setStatus('Ready. Choose a table number, then load orders or carts, or create a new one.');
        }

        function clearOrderEditState() {
            orderIdInput.value = '';
            form.reset();
            tableNumberInput.focus();
        }

        function clearCartEditState() {
            cartIdInput.value = '';
            cartForm.reset();
            tableNumberInput.focus();
        }

        function buildCartSummary(carts) {
            if (!carts || carts.length === 0) {
                return '';
            }

            return carts.map((cart) => {
                const couponText = cart.coupon ? `, coupon ${cart.coupon}` : '';
                return `Item ${cart.menu_item_id} x${cart.quantity} ($${Number(cart.subtotal).toFixed(2)}${couponText})`;
            }).join('; ');
        }

        async function loadDashboard() {
            await Promise.all([loadOrders(), loadCarts()]);
        }

        function clearEditState() {
            resetForm();
            renderOrders(window.cachedOrders || []);
            renderCarts(window.cachedCarts || []);
        }

        async function loadOrders() {
            setStatus('Loading orders...');
            try {
                const response = await fetch('/orders/');
                if (!response.ok) {
                    throw new Error(`Failed to load orders (${response.status})`);
                }
                const data = await response.json();
                window.cachedOrders = data;
                const filtered = filterByTableNumber(data);
                renderOrders(filtered);
                setStatus(getTableNumber() ? `Loaded ${filtered.length} order${filtered.length === 1 ? '' : 's'} for table ${getTableNumber()}.` : `Loaded ${filtered.length} order${filtered.length === 1 ? '' : 's'}.`);
            } catch (error) {
                ordersBox.innerHTML = '';
                ordersBox.innerHTML = `<div class="empty">${error.message}</div>`;
                setStatus(error.message, true);
            }
        }

        async function loadCarts() {
            setStatus('Loading cart...');
            try {
                const response = await fetch('/cart/');
                if (!response.ok) {
                    throw new Error(`Failed to load cart (${response.status})`);
                }
                const data = await response.json();
                window.cachedCarts = data;
                const filtered = filterByTableNumber(data);
                renderCarts(filtered);
                setStatus(getTableNumber() ? `Loaded ${filtered.length} cart item${filtered.length === 1 ? '' : 's'} for table ${getTableNumber()}.` : `Loaded ${filtered.length} cart item${filtered.length === 1 ? '' : 's'}.`);
            } catch (error) {
                cartsBox.innerHTML = '';
                cartsBox.innerHTML = `<div class="empty">${error.message}</div>`;
                setStatus(error.message, true);
            }
        }

        async function clearPersistedCartItems(carts) {
            if (!carts || carts.length === 0) {
                return;
            }

            await Promise.all(carts.map((cart) => fetch(`/cart/${cart.id}`, { method: 'DELETE' })));
        }

        function formatDate(value) {
            if (!value) return 'No order date';
            const date = new Date(value);
            return Number.isNaN(date.getTime()) ? value : date.toLocaleString();
        }

        function renderOrders(orders) {
            if (!orders || orders.length === 0) {
                ordersBox.innerHTML = '<div class="empty">No orders yet. Create the first one using the form.</div>';
                return;
            }

            ordersBox.innerHTML = orders.map((order) => `
                <article class="order-card">
                    <div class="order-top">
                        <div>
                            <div class="order-title">#${order.id} ${order.customer_name ?? 'Unnamed customer'}</div>
                            <div class="muted">Table ${order.table_number}${order.description ? ` · ${order.description}` : ''}</div>
                        </div>
                        <div class="meta">
                            <span>${formatDate(order.order_date)}</span>
                        </div>
                    </div>
                    <div class="actions">
                        <button class="secondary" type="button" onclick='editOrder(${JSON.stringify(order).replace(/'/g, "&#39;")})'>Edit</button>
                        <button class="danger" type="button" onclick="deleteOrder(${order.id})">Delete</button>
                    </div>
                </article>
            `).join('');
        }

        function renderCarts(carts) {
            if (!carts || carts.length === 0) {
                cartsBox.innerHTML = '<div class="empty">No cart items yet. Add the first item using the cart form.</div>';
                return;
            }

            cartsBox.innerHTML = carts.map((cart) => `
                <article class="order-card">
                    <div class="order-top">
                        <div>
                            <div class="order-title">#${cart.id} Cart item</div>
                            <div class="muted">Table ${cart.table_number} · Subtotal: $${Number(cart.subtotal).toFixed(2)}${cart.coupon ? ` · Coupon ${cart.coupon}` : ''}</div>
                        </div>
                        <div class="meta">
                            <span>Qty ${cart.quantity}</span>
                            <span>Customer ${cart.customer_id}</span>
                            <span>Menu item ${cart.menu_item_id}</span>
                        </div>
                    </div>
                    <div class="actions">
                        <button class="secondary" type="button" onclick='editCart(${JSON.stringify(cart).replace(/'/g, "&#39;")})'>Edit</button>
                        <button class="danger" type="button" onclick="deleteCart(${cart.id})">Delete</button>
                    </div>
                </article>
            `).join('');
        }

        function editOrder(order) {
            orderIdInput.value = order.id ?? '';
            tableNumberInput.value = order.table_number ?? '';
            customerNameInput.value = order.customer_name ?? '';
            descriptionInput.value = order.description ?? '';
            console.log(`[ORDER] Loaded for editing: ID=${order.id}, Table=${order.table_number}, Customer=${order.customer_name}`);
            setStatus(`Editing order #${order.id}. Make changes and save.`);
            customerNameInput.focus();
        }

        function editCart(cart) {
            cartIdInput.value = cart.id ?? '';
            tableNumberInput.value = cart.table_number ?? '';
            cartSubtotalInput.value = cart.subtotal ?? '';
            cartCouponInput.value = cart.coupon ?? '';
            cartQuantityInput.value = cart.quantity ?? '';
            cartCustomerIdInput.value = cart.customer_id ?? '';
            cartMenuItemIdInput.value = cart.menu_item_id ?? '';
            console.log(`[CART] Loaded for editing: ID=${cart.id}, Table=${cart.table_number}, MenuItem=${cart.menu_item_id}, Qty=${cart.quantity}`);
            console.log(`[CART] Item name: ${window.menuItems[cart.menu_item_id]?.item_name || 'Unknown'}`);
            setStatus(`Editing cart item #${cart.id}. Make changes and save.`);
            cartSubtotalInput.focus();
        }

        async function deleteOrder(orderId) {
            const confirmed = window.confirm(`Delete order #${orderId}?`);
            if (!confirmed) {
                console.log(`[ORDER] Delete cancelled for order #${orderId}`);
                return;
            }
            console.log(`[ORDER] Deleting order #${orderId}`);

            setStatus(`Deleting order #${orderId}...`);
            try {
                const response = await fetch(`/orders/${orderId}`, { method: 'DELETE' });
                if (!response.ok && response.status !== 204) {
                    throw new Error(`Failed to delete order (${response.status})`);
                }
                console.log(`[ORDER] Order deleted successfully: ID=${orderId}`);
                setStatus(`Deleted order #${orderId}.`);
                await loadOrders();
                if (orderIdInput.value === String(orderId)) {
                    clearOrderEditState();
                }
            } catch (error) {
                setStatus(error.message, true);
            }
        }

        async function confirmOrder() {
            const tableNumber = requireTableNumber();
            const carts = filterByTableNumber(window.cachedCarts || []);
            console.log(`[ORDER] Confirm order action initiated for table ${tableNumber} with ${carts.length} cart items`);

            if (!tableNumber) {
                return;
            }

            const customerName = customerNameInput.value.trim();
            if (!customerName) {
                setStatus('Customer name is required before confirming the order.', true);
                return;
            }

            const description = descriptionInput.value.trim() || (carts.length > 0 ? buildCartSummary(carts) : null);

            setStatus(carts.length > 0 ? 'Creating order from confirmed cart items...' : 'Creating order...');
            try {
                const response = await fetch('/orders/', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        table_number: tableNumber,
                        customer_name: customerName,
                        description,
                    }),
                });

                if (!response.ok) {
                    const errorBody = await response.json().catch(() => null);
                    const detail = errorBody?.detail ?? `Request failed (${response.status})`;
                    throw new Error(detail);
                }

                const saved = await response.json().catch(() => null);
                console.log(`[ORDER] Order created successfully: ID=${saved?.id}, Table=${tableNumber}, Customer=${customerNameInput.value}`);
                if (carts.length > 0) {
                    await clearPersistedCartItems(carts);
                }
                await loadOrders();
                await loadCarts();
                setStatus(carts.length > 0
                    ? `Created order #${saved?.id ?? 'new'} from ${carts.length} confirmed cart item${carts.length === 1 ? '' : 's'}.`
                    : `Created order #${saved?.id ?? 'new'}.`);
            } catch (error) {
                setStatus(error.message, true);
            }
        }

        async function deleteCart(cartId) {
            const confirmed = window.confirm(`Delete cart item #${cartId}?`);
            if (!confirmed) {
                console.log(`[CART] Delete cancelled for cart item #${cartId}`);
                return;
            }
            console.log(`[CART] Deleting cart item #${cartId}`);

            setStatus(`Deleting cart item #${cartId}...`);
            try {
                const response = await fetch(`/cart/${cartId}`, { method: 'DELETE' });
                if (!response.ok && response.status !== 204) {
                    throw new Error(`Failed to delete cart item (${response.status})`);
                }
                console.log(`[CART] Cart item deleted successfully: ID=${cartId}`);
                setStatus(`Deleted cart item #${cartId}.`);
                await loadCarts();
                if (cartIdInput.value === String(cartId)) {
                    clearCartEditState();
                }
            } catch (error) {
                setStatus(error.message, true);
            }
        }

        form.addEventListener('submit', async (event) => {
            event.preventDefault();

            const tableNumber = requireTableNumber();
            const carts = filterByTableNumber(window.cachedCarts || []);
            const isEditing = Boolean(orderIdInput.value);
            console.log(`[ORDER] Order form submitted: ${isEditing ? 'UPDATE' : 'CREATE'} Table=${tableNumber}`);
            const payload = {
                table_number: tableNumber,
                customer_name: customerNameInput.value.trim(),
                description: descriptionInput.value.trim() || (carts.length > 0 ? buildCartSummary(carts) : null),
            };

            if (!payload.customer_name) {
                setStatus('Customer name is required.', true);
                return;
            }

            if (!tableNumber) {
                return;
            }

            const method = isEditing ? 'PUT' : 'POST';
            const url = isEditing ? `/orders/${orderIdInput.value}` : '/orders/';

            setStatus(isEditing ? `Updating order #${orderIdInput.value}...` : (carts.length > 0 ? 'Creating order from confirmed cart items...' : 'Creating order...'));
            try {
                const response = await fetch(url, {
                    method,
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload),
                });

                if (!response.ok) {
                    const errorBody = await response.json().catch(() => null);
                    const detail = errorBody?.detail ?? `Request failed (${response.status})`;
                    throw new Error(detail);
                }

                const saved = await response.json().catch(() => null);
                console.log(`[ORDER] Order ${isEditing ? 'updated' : 'created'}: ID=${saved?.id ?? orderIdInput.value}`);
                if (!isEditing && carts.length > 0) {
                    await clearPersistedCartItems(carts);
                    await loadCarts();
                }
                setStatus(isEditing
                    ? `Updated order #${saved?.id ?? orderIdInput.value}.`
                    : (carts.length > 0
                        ? `Created order #${saved?.id ?? 'new'} from ${carts.length} confirmed cart item${carts.length === 1 ? '' : 's'}.`
                        : `Created order #${saved?.id ?? 'new'}.`));
                resetForm();
                await loadOrders();
            } catch (error) {
                setStatus(error.message, true);
            }
        });

        cartForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const subtotal = Number(cartSubtotalInput.value);
            const quantity = Number(cartQuantityInput.value);
            const customerId = Number(cartCustomerIdInput.value);
            const menuItemId = Number(cartMenuItemIdInput.value);
            const tableNumber = requireTableNumber();
            const isEditing = Boolean(cartIdInput.value);
            console.log(`[CART] Cart form submitted: ${isEditing ? 'UPDATE' : 'ADD'} Table=${tableNumber}, MenuItem=${menuItemId}, Qty=${quantity}`);

            if (!tableNumber) {
                return;
            }

            if (!Number.isFinite(subtotal) || subtotal < 0) {
                setStatus('Subtotal must be a valid number.', true);
                return;
            }

            if (!Number.isInteger(quantity) || quantity < 1) {
                setStatus('Quantity must be a whole number greater than zero.', true);
                return;
            }

            if (!Number.isInteger(customerId) || customerId < 1 || !Number.isInteger(menuItemId) || menuItemId < 1) {
                setStatus('Customer ID and Menu Item ID must be valid positive integers.', true);
                return;
            }

            const payload = {
                table_number: tableNumber,
                subtotal,
                coupon: cartCouponInput.value.trim() || null,
                quantity,
                customer_id: customerId,
                menu_item_id: menuItemId,
            };

            const method = isEditing ? 'PUT' : 'POST';
            const url = isEditing ? `/cart/${cartIdInput.value}` : '/cart/';

            setStatus(isEditing ? `Updating cart item #${cartIdInput.value} for table ${tableNumber}...` : `Adding item to cart for table ${tableNumber}...`);
            try {
                const response = await fetch(url, {
                    method,
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload),
                });

                if (!response.ok) {
                    const errorBody = await response.json().catch(() => null);
                    const detail = errorBody?.detail ?? `Request failed (${response.status})`;
                    throw new Error(detail);
                }

                const saved = await response.json().catch(() => null);
                console.log(`[CART] Cart item ${isEditing ? 'updated' : 'added'}: ID=${saved?.id ?? cartIdInput.value}, MenuItem=${menuItemId}`);
                setStatus(isEditing ? `Updated cart item #${saved?.id ?? cartIdInput.value}.` : `Added cart item #${saved?.id ?? 'new'}.`);
                clearCartEditState();
                await loadCarts();
            } catch (error) {
                setStatus(error.message, true);
            }
        });

        cartQuantityInput.addEventListener('change', updateSubtotal);
        cartMenuItemIdInput.addEventListener('change', updateSubtotal);
        tableNumberInput.addEventListener('change', loadDashboard);

        // Load menu items first, then load dashboard
        loadMenuItems().then(() => loadDashboard());
    </script>
</body>
</html>"""


if __name__ == "__main__":
    uvicorn.run(app, host=conf.app_host, port=conf.app_port)