import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime

class InvoiceEditor:
    def __init__(self, parent, invoice_type="sales"):
        self.parent = parent
        self.invoice_type = invoice_type  # "sales" or "purchases"
        self.current_invoice = None
        self.items = []
        
    def open_editor_window(self):
        """Open the invoice editor window"""
        self.editor_window = tk.Toplevel(self.parent)
        self.editor_window.title(f"Edit {self.invoice_type.title()} Invoices")
        self.editor_window.geometry("1000x700")
        self.editor_window.configure(bg="white")
        
        # Header
        header_frame = tk.Frame(self.editor_window, bg="#2E86AB", height=60)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text=f"📝 EDIT {self.invoice_type.upper()} INVOICES", 
                font=("Arial", 18, "bold"), bg="#2E86AB", fg="white").pack(pady=15)
        
        # Main content
        main_frame = tk.Frame(self.editor_window, bg="white")
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Invoice list section
        list_frame = tk.LabelFrame(main_frame, text=f"{self.invoice_type.title()} List", 
                                  font=("Arial", 12, "bold"))
        list_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        # Invoice tree
        columns = self.get_tree_columns()
        self.invoice_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=12)
        
        for col in columns:
            self.invoice_tree.heading(col, text=col)
            self.invoice_tree.column(col, width=120, anchor="center")
        
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.invoice_tree.yview)
        self.invoice_tree.configure(yscrollcommand=scrollbar.set)
        
        self.invoice_tree.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        scrollbar.pack(side="right", fill="y")
        
        # Buttons
        btn_frame = tk.Frame(main_frame, bg="white")
        btn_frame.pack(fill="x", pady=5)
        
        tk.Button(btn_frame, text="Edit Selected", command=self.edit_selected_invoice,
                 bg="#4CAF50", fg="white", font=("Arial", 10, "bold"),
                 width=12, height=2).pack(side="left", padx=5)
        
        tk.Button(btn_frame, text="Refresh List", command=self.refresh_invoice_list,
                 bg="#2196F3", fg="white", font=("Arial", 10, "bold"),
                 width=12, height=2).pack(side="left", padx=5)
        
        tk.Button(btn_frame, text="Close", command=self.editor_window.destroy,
                 bg="#9E9E9E", fg="white", font=("Arial", 10, "bold"),
                 width=12, height=2).pack(side="right", padx=5)
        
        # Load initial data
        self.refresh_invoice_list()
        
    def get_tree_columns(self):
        """Get appropriate columns based on invoice type"""
        if self.invoice_type == "sales":
            return ["ID", "Date", "Customer", "Items", "Total"]
        else:
            return ["ID", "Date", "Supplier", "Items", "Total"]
    
    def refresh_invoice_list(self):
        """Refresh the invoice list"""
        # Clear existing items
        for item in self.invoice_tree.get_children():
            self.invoice_tree.delete(item)
        
        # Load data
        data = self.load_invoice_data()
        
        for invoice in data:
            if self.invoice_type == "sales":
                self.add_sales_row(invoice)
            else:
                self.add_purchase_row(invoice)
    
    def add_sales_row(self, sale):
        """Add a sales row to the tree"""
        date_str = sale.get('sale_date', '')[:10] if sale.get('sale_date') else 'N/A'
        items_count = len(sale.get('items', []))
        
        self.invoice_tree.insert("", "end", values=(
            sale.get('id', 'N/A'),
            date_str,
            sale.get('customer_name', 'N/A'),
            f"{items_count} items",
            f"KSH {sale.get('total_amount', 0):.2f}"
        ))
    
    def add_purchase_row(self, purchase):
        """Add a purchase row to the tree"""
        date_str = purchase.get('purchase_date', '')[:10] if purchase.get('purchase_date') else 'N/A'
        
        self.invoice_tree.insert("", "end", values=(
            purchase.get('id', 'N/A'),
            date_str,
            purchase.get('supplier', 'N/A'),
            purchase.get('item', 'N/A'),
            f"KSH {purchase.get('total', 0):.2f}"
        ))
    
    def load_invoice_data(self):
        """Load invoice data from JSON file"""
        filename = f"{self.invoice_type}.json"
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                # Sort by date, newest first
                if self.invoice_type == "sales":
                    return sorted(data, key=lambda x: x.get('sale_date', ''), reverse=True)
                else:
                    return sorted(data, key=lambda x: x.get('purchase_date', ''), reverse=True)
        except:
            return []
    
    def edit_selected_invoice(self):
        """Edit the selected invoice"""
        selected = self.invoice_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an invoice to edit")
            return
        
        # Get selected invoice ID
        item = selected[0]
        values = self.invoice_tree.item(item, 'values')
        invoice_id = values[0]
        
        # Find the invoice in data
        data = self.load_invoice_data()
        invoice = None
        for inv in data:
            if str(inv.get('id', '')) == str(invoice_id):
                invoice = inv
                break
        
        if not invoice:
            messagebox.showerror("Error", "Invoice not found")
            return
        
        self.current_invoice = invoice
        self.open_edit_form()
    
    def open_edit_form(self):
        """Open the edit form for the selected invoice"""
        self.edit_window = tk.Toplevel(self.editor_window)
        self.edit_window.title(f"Edit {self.invoice_type.title()} Invoice")
        self.edit_window.geometry("800x600")
        self.edit_window.configure(bg="white")
        
        # Header
        header_frame = tk.Frame(self.edit_window, bg="#FF9800", height=50)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text=f"✏️ EDIT INVOICE #{self.current_invoice.get('id', 'N/A')}", 
                font=("Arial", 16, "bold"), bg="#FF9800", fg="white").pack(pady=10)
        
        # Form content
        form_frame = tk.Frame(self.edit_window, bg="white")
        form_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        if self.invoice_type == "sales":
            self.create_sales_edit_form(form_frame)
        else:
            self.create_purchase_edit_form(form_frame)
    
    def create_sales_edit_form(self, parent):
        """Create sales invoice edit form"""
        # Customer and Date
        info_frame = tk.Frame(parent, bg="white")
        info_frame.pack(fill="x", pady=10)
        
        tk.Label(info_frame, text="Customer:", font=("Arial", 12, "bold"), bg="white").grid(row=0, column=0, sticky="w", padx=5)
        self.customer_entry = tk.Entry(info_frame, width=25, font=("Arial", 12))
        self.customer_entry.grid(row=0, column=1, padx=10)
        self.customer_entry.insert(0, self.current_invoice.get('customer_name', ''))
        
        tk.Label(info_frame, text="Date:", font=("Arial", 12, "bold"), bg="white").grid(row=0, column=2, sticky="w", padx=5)
        self.date_entry = tk.Entry(info_frame, width=15, font=("Arial", 12))
        self.date_entry.grid(row=0, column=3, padx=10)
        date_str = self.current_invoice.get('sale_date', '')[:10] if self.current_invoice.get('sale_date') else ''
        self.date_entry.insert(0, date_str)
        
        # Items section
        items_frame = tk.LabelFrame(parent, text="Invoice Items", font=("Arial", 12, "bold"))
        items_frame.pack(fill="both", expand=True, pady=10)
        
        # Items tree
        self.items_tree = ttk.Treeview(items_frame, columns=("Item", "Qty", "Price", "Total"), 
                                      show="headings", height=8)
        for col in ["Item", "Qty", "Price", "Total"]:
            self.items_tree.heading(col, text=col)
            self.items_tree.column(col, width=120, anchor="center")
        
        items_scrollbar = ttk.Scrollbar(items_frame, orient="vertical", command=self.items_tree.yview)
        self.items_tree.configure(yscrollcommand=items_scrollbar.set)
        
        self.items_tree.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        items_scrollbar.pack(side="right", fill="y")
        
        # Load current items
        self.items = self.current_invoice.get('items', []).copy()
        self.refresh_items_tree()
        
        # Edit controls
        controls_frame = tk.Frame(parent, bg="white")
        controls_frame.pack(fill="x", pady=10)
        
        # Add/Edit item fields
        tk.Label(controls_frame, text="Item:", bg="white").grid(row=0, column=0, padx=5)
        self.item_entry = tk.Entry(controls_frame, width=15)
        self.item_entry.grid(row=0, column=1, padx=5)
        
        tk.Label(controls_frame, text="Qty:", bg="white").grid(row=0, column=2, padx=5)
        self.qty_entry = tk.Entry(controls_frame, width=10)
        self.qty_entry.grid(row=0, column=3, padx=5)
        
        tk.Label(controls_frame, text="Price:", bg="white").grid(row=0, column=4, padx=5)
        self.price_entry = tk.Entry(controls_frame, width=10)
        self.price_entry.grid(row=0, column=5, padx=5)
        
        tk.Button(controls_frame, text="Add Item", command=self.add_item,
                 bg="#4CAF50", fg="white").grid(row=0, column=6, padx=10)
        
        tk.Button(controls_frame, text="Update Selected", command=self.update_selected_item,
                 bg="#FF9800", fg="white").grid(row=0, column=7, padx=5)
        
        tk.Button(controls_frame, text="Remove Selected", command=self.remove_selected_item,
                 bg="#f44336", fg="white").grid(row=0, column=8, padx=5)
        
        # Total display
        self.total_label = tk.Label(parent, text="Total: KSH 0.00", 
                                   font=("Arial", 14, "bold"), fg="#2E86AB", bg="white")
        self.total_label.pack(pady=10)
        self.update_total()
        
        # Save/Cancel buttons
        btn_frame = tk.Frame(parent, bg="white")
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="Save Changes", command=self.save_changes,
                 bg="#4CAF50", fg="white", font=("Arial", 12, "bold"),
                 width=15, height=2).pack(side="left", padx=10)
        
        tk.Button(btn_frame, text="Cancel", command=self.edit_window.destroy,
                 bg="#9E9E9E", fg="white", font=("Arial", 12, "bold"),
                 width=15, height=2).pack(side="left", padx=10)
    
    def create_purchase_edit_form(self, parent):
        """Create purchase invoice edit form"""
        # Supplier and Date
        info_frame = tk.Frame(parent, bg="white")
        info_frame.pack(fill="x", pady=10)
        
        tk.Label(info_frame, text="Supplier:", font=("Arial", 12, "bold"), bg="white").grid(row=0, column=0, sticky="w", padx=5)
        self.supplier_entry = tk.Entry(info_frame, width=20, font=("Arial", 12))
        self.supplier_entry.grid(row=0, column=1, padx=10)
        self.supplier_entry.insert(0, self.current_invoice.get('supplier', ''))
        
        tk.Label(info_frame, text="Date:", font=("Arial", 12, "bold"), bg="white").grid(row=0, column=2, sticky="w", padx=5)
        self.date_entry = tk.Entry(info_frame, width=15, font=("Arial", 12))
        self.date_entry.grid(row=0, column=3, padx=10)
        date_str = self.current_invoice.get('purchase_date', '')[:10] if self.current_invoice.get('purchase_date') else ''
        self.date_entry.insert(0, date_str)
        
        # Item details
        details_frame = tk.LabelFrame(parent, text="Item Details", font=("Arial", 12, "bold"))
        details_frame.pack(fill="x", pady=10)
        
        details_grid = tk.Frame(details_frame)
        details_grid.pack(padx=10, pady=10)
        
        tk.Label(details_grid, text="Item:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w", padx=5)
        self.item_entry = tk.Entry(details_grid, width=20, font=("Arial", 10))
        self.item_entry.grid(row=0, column=1, padx=10)
        self.item_entry.insert(0, self.current_invoice.get('item', ''))
        
        tk.Label(details_grid, text="Quantity:", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky="w", padx=5)
        self.qty_entry = tk.Entry(details_grid, width=15, font=("Arial", 10))
        self.qty_entry.grid(row=1, column=1, padx=10)
        self.qty_entry.insert(0, str(self.current_invoice.get('quantity', 0)))
        
        tk.Label(details_grid, text="Price per unit:", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky="w", padx=5)
        self.price_entry = tk.Entry(details_grid, width=15, font=("Arial", 10))
        self.price_entry.grid(row=2, column=1, padx=10)
        self.price_entry.insert(0, str(self.current_invoice.get('price', 0)))
        
        # Total display
        self.total_label = tk.Label(parent, text=f"Total: KSH {self.current_invoice.get('total', 0):.2f}", 
                                   font=("Arial", 14, "bold"), fg="#2E86AB", bg="white")
        self.total_label.pack(pady=10)
        
        # Bind events to update total
        self.qty_entry.bind('<KeyRelease>', self.update_purchase_total)
        self.price_entry.bind('<KeyRelease>', self.update_purchase_total)
        
        # Save/Cancel buttons
        btn_frame = tk.Frame(parent, bg="white")
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="Save Changes", command=self.save_purchase_changes,
                 bg="#4CAF50", fg="white", font=("Arial", 12, "bold"),
                 width=15, height=2).pack(side="left", padx=10)
        
        tk.Button(btn_frame, text="Cancel", command=self.edit_window.destroy,
                 bg="#9E9E9E", fg="white", font=("Arial", 12, "bold"),
                 width=15, height=2).pack(side="left", padx=10)
    
    def refresh_items_tree(self):
        """Refresh the items tree view"""
        for item in self.items_tree.get_children():
            self.items_tree.delete(item)
        
        for item in self.items:
            self.items_tree.insert("", "end", values=(
                item.get('item', ''),
                item.get('quantity', 0),
                f"KSH {item.get('price', 0):.2f}",
                f"KSH {item.get('total', 0):.2f}"
            ))
    
    def add_item(self):
        """Add new item to the invoice"""
        item_name = self.item_entry.get().strip()
        qty_str = self.qty_entry.get().strip()
        price_str = self.price_entry.get().strip()
        
        if not all([item_name, qty_str, price_str]):
            messagebox.showerror("Error", "All fields are required")
            return
        
        try:
            qty = float(qty_str)
            price = float(price_str)
            total = qty * price
            
            new_item = {
                "item": item_name,
                "quantity": qty,
                "price": price,
                "total": total
            }
            
            self.items.append(new_item)
            self.refresh_items_tree()
            self.update_total()
            
            # Clear fields
            self.item_entry.delete(0, tk.END)
            self.qty_entry.delete(0, tk.END)
            self.price_entry.delete(0, tk.END)
            
        except ValueError:
            messagebox.showerror("Error", "Invalid quantity or price")
    
    def update_selected_item(self):
        """Update the selected item"""
        selected = self.items_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an item to update")
            return
        
        item_name = self.item_entry.get().strip()
        qty_str = self.qty_entry.get().strip()
        price_str = self.price_entry.get().strip()
        
        if not all([item_name, qty_str, price_str]):
            messagebox.showerror("Error", "All fields are required")
            return
        
        try:
            qty = float(qty_str)
            price = float(price_str)
            total = qty * price
            
            # Get selected index
            item_index = self.items_tree.index(selected[0])
            
            # Update item
            self.items[item_index] = {
                "item": item_name,
                "quantity": qty,
                "price": price,
                "total": total
            }
            
            self.refresh_items_tree()
            self.update_total()
            
            # Clear fields
            self.item_entry.delete(0, tk.END)
            self.qty_entry.delete(0, tk.END)
            self.price_entry.delete(0, tk.END)
            
        except ValueError:
            messagebox.showerror("Error", "Invalid quantity or price")
    
    def remove_selected_item(self):
        """Remove the selected item"""
        selected = self.items_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an item to remove")
            return
        
        if messagebox.askyesno("Confirm", "Remove selected item?"):
            item_index = self.items_tree.index(selected[0])
            self.items.pop(item_index)
            self.refresh_items_tree()
            self.update_total()
    
    def update_total(self):
        """Update the total amount display"""
        total = sum(item.get('total', 0) for item in self.items)
        self.total_label.config(text=f"Total: KSH {total:.2f}")
    
    def update_purchase_total(self, event=None):
        """Update purchase total when qty or price changes"""
        try:
            qty = float(self.qty_entry.get() or 0)
            price = float(self.price_entry.get() or 0)
            total = qty * price
            self.total_label.config(text=f"Total: KSH {total:.2f}")
        except ValueError:
            pass
    
    def save_changes(self):
        """Save changes to sales invoice"""
        customer = self.customer_entry.get().strip()
        date_str = self.date_entry.get().strip()
        
        if not customer:
            messagebox.showerror("Error", "Customer name is required")
            return
        
        if not self.items:
            messagebox.showerror("Error", "At least one item is required")
            return
        
        try:
            # Update invoice data
            total_amount = sum(item.get('total', 0) for item in self.items)
            
            # Format date
            if date_str:
                sale_datetime = f"{date_str}T{datetime.now().strftime('%H:%M:%S')}"
            else:
                sale_datetime = self.current_invoice.get('sale_date', datetime.now().isoformat())
            
            updated_invoice = {
                "id": self.current_invoice.get('id'),
                "customer_name": customer,
                "items": self.items.copy(),
                "total_amount": total_amount,
                "sale_date": sale_datetime
            }
            
            # Save to file
            self.save_invoice_data(updated_invoice)
            
            messagebox.showinfo("Success", "Invoice updated successfully!")
            self.edit_window.destroy()
            self.refresh_invoice_list()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save changes: {e}")
    
    def save_purchase_changes(self):
        """Save changes to purchase invoice"""
        supplier = self.supplier_entry.get().strip()
        item = self.item_entry.get().strip()
        date_str = self.date_entry.get().strip()
        
        if not all([supplier, item]):
            messagebox.showerror("Error", "Supplier and item are required")
            return
        
        try:
            qty = float(self.qty_entry.get() or 0)
            price = float(self.price_entry.get() or 0)
            total = qty * price
            
            if qty <= 0 or price <= 0:
                messagebox.showerror("Error", "Quantity and price must be positive")
                return
            
            # Format date
            if date_str:
                purchase_datetime = f"{date_str}T{datetime.now().strftime('%H:%M:%S')}"
            else:
                purchase_datetime = self.current_invoice.get('purchase_date', datetime.now().isoformat())
            
            updated_invoice = {
                "id": self.current_invoice.get('id'),
                "supplier": supplier,
                "item": item,
                "quantity": qty,
                "price": price,
                "total": total,
                "purchase_date": purchase_datetime
            }
            
            # Save to file
            self.save_purchase_data(updated_invoice)
            
            messagebox.showinfo("Success", "Purchase updated successfully!")
            self.edit_window.destroy()
            self.refresh_invoice_list()
            
        except ValueError:
            messagebox.showerror("Error", "Invalid quantity or price")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save changes: {e}")
    
    def save_invoice_data(self, updated_invoice):
        """Save updated sales invoice data"""
        filename = "sales.json"
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
        except:
            data = []
        
        # Find and update the invoice
        for i, invoice in enumerate(data):
            if str(invoice.get('id', '')) == str(updated_invoice.get('id', '')):
                data[i] = updated_invoice
                break
        
        # Save back to file
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
    
    def save_purchase_data(self, updated_invoice):
        """Save updated purchase invoice data"""
        filename = "purchases.json"
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
        except:
            data = []
        
        # Find and update the invoice
        for i, invoice in enumerate(data):
            if str(invoice.get('id', '')) == str(updated_invoice.get('id', '')):
                data[i] = updated_invoice
                break
        
        # Save back to file
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)