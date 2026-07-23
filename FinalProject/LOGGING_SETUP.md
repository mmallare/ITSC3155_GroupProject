# Logging Implementation - Complete Audit Trail

## Overview
Comprehensive logging has been added to track all order and cart operations across the system.

## Backend Logging (Python/FastAPI)

### Order Controller (`api/controllers/orders.py`)
- **CREATE**: Logs order ID, table number, and customer name when order is created
- **UPDATE**: Logs order ID and all changed fields when order is updated
- **DELETE**: Logs order ID when order is deleted
- **READ_ALL**: Logs total number of orders retrieved
- **ERROR**: Logs all database errors with operation context

Example log output:
```
INFO - Order created: ID=42, Table=5, Customer=PJ Yang
INFO - Order updated: ID=42, Changes={'customer_name': 'PJ Yang Updated'}
INFO - Order deleted: ID=42
ERROR - Failed to create order: [specific error message]
```

### Cart Controller (`api/controllers/cart.py`)
- **CREATE**: Logs cart item ID, table number, menu item ID, quantity, and subtotal when item is added
- **UPDATE**: Logs cart item ID and all changed fields when item is updated
- **DELETE**: Logs cart item ID when item is deleted
- **READ_ALL**: Logs total number of cart items retrieved
- **ERROR**: Logs all database errors with operation context

Example log output:
```
INFO - Cart item added: ID=15, Table=5, MenuItem=3, Qty=2, Subtotal=$18.99
INFO - Cart item updated: ID=15, Changes={'quantity': 3}
INFO - Cart item deleted: ID=15
WARNING - Update attempted on non-existent cart item ID=999
```

## Frontend Logging (JavaScript Console)

### Order Operations
- **Confirm Order**: Logs when user initiates order confirmation with table number and cart count
- **Create/Update Order**: Logs order creation or update with ID and customer details
- **Load for Edit**: Logs when order is loaded for editing with full order details
- **Delete Order**: Logs when delete is initiated or cancelled
- **Delete Success**: Logs when order is successfully deleted

Example console output:
```
[ORDER] Confirm order action initiated for table 5 with 2 cart items
[ORDER] Order form submitted: CREATE Table=5
[ORDER] Order created successfully: ID=42, Table=5, Customer=PJ Yang
[ORDER] Loaded for editing: ID=42, Table=5, Customer=PJ Yang Yang
[ORDER] Deleting order #42
[ORDER] Order deleted successfully: ID=42
```

### Cart Operations
- **Add/Update Cart**: Logs when user submits cart form with table number, menu item ID, and quantity
- **Load for Edit**: Logs when cart item is loaded for editing with full item details
- **Delete Cart**: Logs when delete is initiated or cancelled
- **Delete Success**: Logs when cart item is successfully deleted

Example console output:
```
[CART] Cart form submitted: ADD Table=5, MenuItem=3, Qty=2
[CART] Cart item added: ID=15, MenuItem=3
[CART] Loaded for editing: ID=15, Table=5, MenuItem=3, Qty=2
[CART] Deleting cart item #15
[CART] Cart item deleted successfully: ID=15
```

## How to View Logs

### Server Logs (Terminal)
Run the server with:
```bash
cd FinalProject
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --log-level info
```

Server logs appear in the terminal where the command runs:
- INFO level: Order/cart operations
- DEBUG level: Data retrieval counts
- WARNING level: Attempted operations on non-existent items
- ERROR level: Database and validation failures

### Browser Console Logs
1. Open the dashboard at http://127.0.0.1:8000/
2. Press **F12** or **Ctrl+Shift+I** to open Developer Tools
3. Click the **Console** tab
4. Perform order or cart operations
5. View logs with [ORDER] or [CART] prefixes showing all user actions

## Log Categories

### [ORDER] Logs
- Form submissions (CREATE/UPDATE)
- Successful creates and updates
- Item loading for editing
- Deletions (initiated and successful)
- Cancellations

### [CART] Logs
- Form submissions (ADD/UPDATE)
- Successful adds and updates
- Item loading for editing
- Deletions (initiated and successful)
- Cancellations

## Benefits
- **Complete audit trail** of all order/cart modifications
- **User action tracking** through browser console
- **Backend operation verification** through server logs
- **Error context** for debugging issues
- **Performance monitoring** of database operations
- **Compliance tracking** for order management

## Testing the Logging

1. Open the dashboard
2. Set Table Number to 1
3. Fill in cart form (Subtotal: 10.99, Quantity: 1, Customer ID: 1, Menu Item ID: 3)
4. Click "Add to Cart"
5. Check browser console (F12) for [CART] logs
6. Check server terminal for INFO logs
7. Fill in order form (Customer Name: "Test Order")
8. Click "Confirm Order"
9. Check both console and server logs for order creation records
