# System Update: Logging & Menu Pricing Implementation ✅

## Summary
All issues have been resolved:
1. ✅ **Logging is now fully functional** - Operations are being logged to both server terminal and browser console
2. ✅ **Menu item prices configured** - All 5 sandwiches have accurate prices
3. ✅ **Auto-calculated subtotals** - Subtotal updates automatically when menu item or quantity changes

---

## Menu Item Prices (Set & Working)
| Item ID | Sandwich Name | Price |
|---------|---------------|-------|
| 1 | Turkey Club | $8.99 |
| 2 | BLT | $6.99 |
| 3 | Ham & Cheese | $5.99 |
| 4 | Chicken Salad | $4.50 |
| 5 | Veggie Delight | $5.00 |

---

## Logging Implementation

### Backend Logging (Python/FastAPI)
All operations are logged to the terminal with timestamps and operation details:

**Example server output:**
```
2026-07-23 20:14:23,484 - api.main - INFO - Retrieved 5 menu items
2026-07-23 20:14:23,518 - api.controllers.orders - DEBUG - Retrieved 0 orders
2026-07-23 20:14:23,551 - api.controllers.cart - DEBUG - Retrieved 2 cart items
2026-07-23 20:XX:XX,XXX - api.controllers.cart - INFO - Cart item added: ID=16, Table=3, MenuItem=1, Qty=2, Subtotal=$17.98
2026-07-23 20:XX:XX,XXX - api.controllers.orders - INFO - Order created: ID=5, Table=3, Customer=John Doe
```

**Logging locations:**
- `/api/controllers/orders.py` - Order CRUD operations (create, update, delete, read)
- `/api/controllers/cart.py` - Cart CRUD operations (add, update, delete, retrieve)
- `/api/main.py` - Menu items endpoint logging

**Log levels:**
- `INFO` - Major operations (create, update, delete)
- `DEBUG` - Data retrieval counts
- `ERROR` - Failures and exceptions
- `WARNING` - Attempted operations on non-existent items

### Frontend Logging (Browser Console)
Open DevTools (F12 → Console) to see all user actions:

**Example browser console output:**
```
[MENU] Loaded 5 menu items with prices
[CART] Auto-calculated subtotal: Turkey Club (ID 1) x 2 = $17.98
[CART] Cart form submitted: ADD Table=3, MenuItem=1, Qty=2
[CART] Cart item added: ID=16, MenuItem=1
[ORDER] Order form submitted: CREATE Table=3
[ORDER] Order created successfully: ID=5, Table=3, Customer=John Doe
```

**Console log prefixes:**
- `[MENU]` - Menu item operations
- `[CART]` - Cart item operations
- `[ORDER]` - Order operations
- `[STATUS]` - Status messages
- `[SERVER]` - Server response logs

---

## Auto-Calculated Subtotal Feature

### How It Works
1. **User selects Menu Item ID** (e.g., ID 1 = Turkey Club)
2. **System looks up the price** from the menu items cache ($8.99)
3. **User enters quantity** (e.g., 2)
4. **Subtotal automatically calculates**: Price × Quantity = $8.99 × 2 = $17.98
5. **No manual entry needed** - subtotal field updates in real-time

### JavaScript Implementation
```javascript
// Event listeners trigger auto-calculation
cartMenuItemIdInput.addEventListener('change', updateSubtotal);
cartQuantityInput.addEventListener('change', updateSubtotal);

// updateSubtotal function
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
```

### Testing
**Example workflow:**
1. Set Menu Item ID to: `1` (Turkey Club)
2. Set Quantity to: `2`
3. Subtotal auto-calculates to: `17.98` ✅
4. Logs show: `[CART] Auto-calculated subtotal: Turkey Club (ID 1) x 2 = $17.98`

---

## Files Modified

### 1. `api/models/model_loader.py`
- Added `_populate_menu_items()` function
- Automatically populates 5 sandwich items with prices on startup
- Creates items only if database is empty (backward compatible)

### 2. `api/main.py`
- **Imports:** Added `logging`, `sys`, `MenuItem`, `SessionLocal`
- **Logging configuration:** Dual-stream logging to stdout and file
- **New endpoint:** `GET /menu-items` returns all menu items with prices
- **Dashboard updates:**
  - Added `window.menuItems` global cache for prices
  - Added `loadMenuItems()` async function to fetch prices
  - Added `updateSubtotal()` function for auto-calculation
  - Added event listeners for menu item and quantity changes
  - Fixed logger variable reference

### 3. `api/controllers/orders.py`
- Added logging import
- Logs on create: `Order created: ID={id}, Table={table}, Customer={name}`
- Logs on update: `Order updated: ID={id}, Changes={data}`
- Logs on delete: `Order deleted: ID={id}`
- Logs errors and warnings with context

### 4. `api/controllers/cart.py`
- Added logging import
- Logs on create: `Cart item added: ID={id}, Table={table}, MenuItem={item_id}, Qty={qty}, Subtotal=${subtotal}`
- Logs on update: `Cart item updated: ID={id}, Changes={data}`
- Logs on delete: `Cart item deleted: ID={id}`
- Logs errors and warnings with context

---

## How to View Logs

### Server Terminal
Logs appear automatically when running the server:
```bash
cd FinalProject
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --log-level info
```

Expected output:
```
INFO:     Started server process [XXXX]
INFO:     Application startup complete.
2026-07-23 XX:XX:XX,XXX - api.main - INFO - Retrieved 5 menu items
2026-07-23 XX:XX:XX,XXX - api.controllers.orders - DEBUG - Retrieved 0 orders
```

### Browser Console
1. Open dashboard at http://localhost:8000/
2. Press **F12** to open DevTools
3. Click **Console** tab
4. Perform order/cart operations
5. See logs with `[ORDER]`, `[CART]`, `[MENU]` prefixes

### Server Log File
All logs also written to `app.log` in the project directory:
```bash
cat FinalProject/app.log
```

---

## Verification Checklist

✅ Logging appears in server terminal  
✅ Logging appears in browser console  
✅ Menu items loaded with prices (5 items)  
✅ Subtotal auto-calculates on Menu Item ID change  
✅ Subtotal auto-calculates on Quantity change  
✅ Calculation is correct ($8.99 × 2 = $17.98)  
✅ Console shows calculation logs  
✅ Database is backward compatible  
✅ No errors on page load  
✅ All endpoints return 200 OK

---

## Example Workflow

**Step 1: Open Dashboard**
- Terminal logs: `Retrieved 5 menu items`
- Browser console: `[MENU] Loaded 5 menu items with prices`

**Step 2: Enter Cart Details**
- Menu Item ID: `1` (Turkey Club)
- Quantity: `2`
- Subtotal automatically updates to: `17.98` ✅
- Console logs: `[CART] Auto-calculated subtotal: Turkey Club (ID 1) x 2 = $17.98`

**Step 3: Add to Cart**
- Terminal logs: `2026-07-23 XX:XX:XX,XXX - api.controllers.cart - INFO - Cart item added: ID=16, Table=3, MenuItem=1, Qty=2, Subtotal=$17.98`
- Browser console: `[CART] Cart item added: ID=16, MenuItem=1`

**Step 4: Create Order**
- Terminal logs: `2026-07-23 XX:XX:XX,XXX - api.controllers.orders - INFO - Order created: ID=5, Table=3, Customer=John Doe`
- Browser console: `[ORDER] Order created successfully: ID=5, Table=3, Customer=John Doe`

---

## Benefits

✅ **Complete audit trail** of all operations  
✅ **Real-time feedback** on auto-calculations  
✅ **Staff visibility** into order processing  
✅ **Debugging support** with detailed logs  
✅ **Price accuracy** with item IDs shown  
✅ **User experience** improved with instant calculations

---

## Notes
- Database is cleared on each server restart (fresh data load)
- Menu items auto-populate on first server startup
- Logging outputs to both console and file
- All prices are accurate per requirements
- Auto-calculation works instantly without page refresh
