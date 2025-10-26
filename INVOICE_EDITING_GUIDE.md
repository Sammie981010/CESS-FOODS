# Invoice Editing Guide - CESS FOODS Management System

## Overview
The CESS FOODS Management System now includes comprehensive invoice editing capabilities for both sales and purchase transactions. This feature allows users to modify existing invoices with proper validation and data integrity.

## Features

### 1. Editable Sales Invoices
- Edit customer information
- Modify sale dates
- Add, update, or remove items
- Automatic total recalculation
- Real-time validation

### 2. Editable Purchase Invoices
- Edit supplier information
- Modify purchase dates
- Update item details (name, quantity, price)
- Automatic total recalculation
- Real-time validation

### 3. Inline Editing
- Double-click any item in sales/purchase lists to edit
- Quick modification without opening separate windows
- Immediate feedback and validation

## How to Use

### Accessing Invoice Editors

#### From Sales Tab:
1. Navigate to the **Sales** tab
2. Click the **"Edit Invoices"** button (orange button)
3. Select an invoice from the list
4. Click **"Edit Selected"**

#### From Purchases Tab:
1. Navigate to the **Purchases** tab
2. Click the **"Edit Invoices"** button (orange button)
3. Select a purchase from the list
4. Click **"Edit Selected"**

### Inline Editing (Quick Edit)

#### Sales Items:
1. In the Sales tab, double-click any item in the current sale list
2. The item details will populate the input fields
3. Modify the values as needed
4. Click **"Add Item"** to update

#### Purchase Items:
1. In the Purchases tab, double-click any item in the current purchase list
2. The item details will populate the input fields
3. Modify the values as needed
4. Click **"Add Item"** to update

### Full Invoice Editing

#### Sales Invoice Editor:
1. **Customer Information**: Update customer name
2. **Date**: Modify the sale date (YYYY-MM-DD format)
3. **Items Management**:
   - **Add Item**: Enter item name, quantity, and price
   - **Update Selected**: Select an item and modify its details
   - **Remove Selected**: Delete unwanted items
4. **Save Changes**: Click to save all modifications

#### Purchase Invoice Editor:
1. **Supplier Information**: Update supplier name
2. **Date**: Modify the purchase date (YYYY-MM-DD format)
3. **Item Details**:
   - **Item Name**: Update the product name
   - **Quantity**: Modify the quantity purchased
   - **Price per Unit**: Update the unit price
4. **Save Changes**: Click to save all modifications

## Validation Rules

### Sales Invoices:
- Customer name is required
- At least one item must be present
- Quantities and prices must be positive numbers
- Dates must be in valid format

### Purchase Invoices:
- Supplier name is required
- Item name is required
- Quantity and price must be positive numbers
- Dates must be in valid format

## Data Safety

### Backup Recommendations:
- The system automatically maintains data integrity
- Original data is preserved until changes are saved
- Consider creating manual backups before major edits

### Audit Trail:
- All changes update the original JSON files
- Modified dates reflect the edit timestamp
- Original invoice IDs are preserved

## Troubleshooting

### Common Issues:

#### "Invoice editor not available" Error:
- Ensure `invoice_editor.py` is in the same directory as `app.py`
- Check that the file is not corrupted

#### Changes Not Saving:
- Verify all required fields are filled
- Check that quantities and prices are valid numbers
- Ensure you have write permissions to the data files

#### Items Not Loading:
- Check that `sales.json` and `purchases.json` files exist
- Verify the JSON files are not corrupted
- Restart the application if needed

### File Dependencies:
- `invoice_editor.py` - Main editor module
- `sales.json` - Sales data storage
- `purchases.json` - Purchase data storage
- `app.py` - Main application (updated with editor integration)

## Technical Details

### File Structure:
```
decent_foods/
├── app.py (main application)
├── invoice_editor.py (editor module)
├── sales.json (sales data)
├── purchases.json (purchase data)
└── test_invoice_editor.py (testing script)
```

### Key Classes:
- `InvoiceEditor`: Main editor class handling both sales and purchases
- Integration methods in `FoodApp` class

### Data Format:
- Sales invoices maintain the existing JSON structure
- Purchase invoices preserve all original fields
- Timestamps are updated to reflect edit times

## Best Practices

1. **Before Editing**:
   - Review the current invoice details
   - Note any special requirements
   - Consider the impact on reports and totals

2. **During Editing**:
   - Make one change at a time for complex edits
   - Verify calculations before saving
   - Use descriptive item names

3. **After Editing**:
   - Verify the changes in the main application
   - Check that totals are correct
   - Update any related documentation

## Support

For technical support or feature requests related to invoice editing:
1. Check this guide for common solutions
2. Verify all files are properly installed
3. Test with the provided test script: `python test_invoice_editor.py`

## Version Information
- Feature added: January 2025
- Compatible with: CESS FOODS Management System v2.0+
- Dependencies: tkinter, json, datetime