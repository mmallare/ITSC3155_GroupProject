import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from .routers import index as indexRoute
from .models import model_loader
from .dependencies.config import conf


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


@app.get("/", response_class=HTMLResponse)
def home():
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Sandwich Maker Orders</title>
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
                <h1>Sandwich Maker Orders</h1>
                <p class="lede">A lightweight order dashboard for creating, reviewing, updating, and deleting orders directly from the browser. This page talks to the FastAPI backend on the same origin.</p>
                <div class="chips">
                    <span class="chip">Live CRUD</span>
                    <span class="chip">No page reloads</span>
                    <span class="chip">SQLite fallback ready</span>
                </div>
                <div id="status" class="status">Ready. Load orders or create a new one.</div>
            </div>
            <div class="panel">
                <h2>Quick Actions</h2>
                <div class="toolbar">
                    <button class="secondary" type="button" onclick="loadOrders()">Refresh orders</button>
                    <button class="ghost" type="button" onclick="resetForm()">Reset form</button>
                </div>
                <p class="muted" style="margin: 0; line-height: 1.6;">
                    Use the form below to create an order, then edit or remove it from the list. Clicking <strong>Edit</strong> loads the order into the form.
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
                        <button class="primary" type="submit">Save Order</button>
                        <button class="danger" type="button" onclick="clearEditState()">Cancel Edit</button>
                    </div>
                </form>
            </div>

            <div class="panel">
                <h2>Orders</h2>
                <div id="orders" class="list"></div>
            </div>
        </section>
    </div>

    <script>
        const statusBox = document.getElementById('status');
        const ordersBox = document.getElementById('orders');
        const form = document.getElementById('order-form');
        const orderIdInput = document.getElementById('order-id');
        const customerNameInput = document.getElementById('customer-name');
        const descriptionInput = document.getElementById('description');

        function setStatus(message, error = false) {
            statusBox.textContent = message;
            statusBox.style.background = error ? 'rgba(220, 38, 38, 0.08)' : 'rgba(15, 118, 110, 0.08)';
            statusBox.style.color = error ? '#991b1b' : '#115e59';
            statusBox.style.borderColor = error ? 'rgba(220, 38, 38, 0.18)' : 'rgba(15, 118, 110, 0.18)';
        }

        function resetForm() {
            orderIdInput.value = '';
            form.reset();
            customerNameInput.focus();
            setStatus('Ready. Load orders or create a new one.');
        }

        function clearEditState() {
            resetForm();
            renderOrders(window.cachedOrders || []);
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
                renderOrders(data);
                setStatus(`Loaded ${data.length} order${data.length === 1 ? '' : 's'}.`);
            } catch (error) {
                ordersBox.innerHTML = '';
                ordersBox.innerHTML = `<div class="empty">${error.message}</div>`;
                setStatus(error.message, true);
            }
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
                            <div class="muted">${order.description ?? 'No description provided'}</div>
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

        function editOrder(order) {
            orderIdInput.value = order.id ?? '';
            customerNameInput.value = order.customer_name ?? '';
            descriptionInput.value = order.description ?? '';
            setStatus(`Editing order #${order.id}. Make changes and save.`);
            customerNameInput.focus();
        }

        async function deleteOrder(orderId) {
            const confirmed = window.confirm(`Delete order #${orderId}?`);
            if (!confirmed) return;

            setStatus(`Deleting order #${orderId}...`);
            try {
                const response = await fetch(`/orders/${orderId}`, { method: 'DELETE' });
                if (!response.ok && response.status !== 204) {
                    throw new Error(`Failed to delete order (${response.status})`);
                }
                setStatus(`Deleted order #${orderId}.`);
                await loadOrders();
                if (orderIdInput.value === String(orderId)) {
                    resetForm();
                }
            } catch (error) {
                setStatus(error.message, true);
            }
        }

        form.addEventListener('submit', async (event) => {
            event.preventDefault();

            const payload = {
                customer_name: customerNameInput.value.trim(),
                description: descriptionInput.value.trim() || null,
            };

            if (!payload.customer_name) {
                setStatus('Customer name is required.', true);
                return;
            }

            const isEditing = Boolean(orderIdInput.value);
            const method = isEditing ? 'PUT' : 'POST';
            const url = isEditing ? `/orders/${orderIdInput.value}` : '/orders/';

            setStatus(isEditing ? `Updating order #${orderIdInput.value}...` : 'Creating order...');
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
                setStatus(isEditing ? `Updated order #${saved?.id ?? orderIdInput.value}.` : `Created order #${saved?.id ?? 'new'}.`);
                resetForm();
                await loadOrders();
            } catch (error) {
                setStatus(error.message, true);
            }
        });

        loadOrders();
    </script>
</body>
</html>"""


if __name__ == "__main__":
    uvicorn.run(app, host=conf.app_host, port=conf.app_port)