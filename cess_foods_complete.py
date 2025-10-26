import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import json
import os
from datetime import datetime, timedelta
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
try:
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

class FullScreenApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("CESS FOODS - Management System")
        self.root.state('zoomed')
        self.root.withdraw()
        
        self.purchase_items = []
        self.purchase_total = 0.0
        self.sales_items = []
        self.sales_total = 0.0
        self.order_items = []
        self.order_total = 0.0
        self.invoice_counter = 1
        self.order_counter = 1
        
        self.show_login()
    
    def show_login(self):
        self.login_window = tk.Toplevel()
        self.login_window.title("CESS FOODS - Login")
        self.login_window.geometry("400x300")
        self.login_window.resizable(False, False)
        self.login_window.configure(bg="#2E86AB")
        
        self.login_window.transient(self.root)
        self.login_window.grab_set()
        
        tk.Label(self.login_window, text="CESS FOODS", font=("Arial", 20, "bold"), 
                fg="white", bg="#2E86AB").pack(pady=30)
        
        login_frame = tk.Frame(self.login_window, bg="white", relief="raised", bd=2)
        login_frame.pack(padx=50, pady=20, fill="both", expand=True)
        
        tk.Label(login_frame, text="Login", font=("Arial", 16, "bold"), bg="white").pack(pady=20)
        
        tk.Label(login_frame, text="Username:", font=("Arial", 12), bg="white").pack(pady=5)
        self.username_entry = tk.Entry(login_frame, width=25, font=("Arial", 12))
        self.username_entry.pack(pady=5)
        
        tk.Label(login_frame, text="Password:", font=("Arial", 12), bg="white").pack(pady=5)
        self.password_entry = tk.Entry(login_frame, width=25, font=("Arial", 12), show="*")
        self.password_entry.pack(pady=5)
        
        tk.Button(login_frame, text="Login", command=self.validate_login,
                 bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), 
                 width=15, height=2).pack(pady=20)
        
        self.username_entry.focus()
        self.login_window.bind('<Return>', lambda e: self.validate_login())
    
    def validate_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if username == "admin" and password == "admin123":
            self.login_window.destroy()
            self.root.deiconify()
            self.create_main_interface()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")
            self.password_entry.delete(0, tk.END)
            self.username_entry.focus()
    
    def create_main_interface(self):
        title_frame = tk.Frame(self.root, bg="#2E86AB", height=60)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)
        
        tk.Label(title_frame, text="CESS FOODS - MANAGEMENT SYSTEM", 
                font=("Arial", 20, "bold"), bg="#2E86AB", fg="white").pack(pady=15)
        
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.invoice_counter = self.get_next_invoice_number()
        self.order_counter = self.get_next_order_number()
        
        self.create_summary_tab()
        self.create_orders_tab()
        self.create_purchase_tab()
        self.create_sales_tab()
        self.create_supplier_payments_tab()
    
    def get_next_invoice_number(self):
        try:
            sales = self.load_sales()
            if sales:
                return max([int(s.get('invoice_no', 'INV-0000').split('-')[1]) for s in sales if 'invoice_no' in s]) + 1
        except:
            pass
        return 1
    
    def get_next_order_number(self):
        try:
            orders = self.load_orders()
            if orders:
                return max([int(o.get('order_no', 'ORD-0000').split('-')[1]) for o in orders if 'order_no' in o]) + 1
        except:
            pass
        return 1
    
    def load_sales(self):
        try:
            if os.path.exists("sales.json"):
                with open("sales.json", 'r') as f:
                    return json.load(f)
        except:
            pass
        return []
    
    def load_orders(self):
        try:
            if os.path.exists("orders.json"):
                with open("orders.json", 'r') as f:
                    return json.load(f)
        except:
            pass
        return []
    
    def load_purchases(self):
        try:
            if os.path.exists("purchases.json"):
                with open("purchases.json", 'r') as f:
                    return json.load(f)
        except:
            pass
        return []
    
    def load_payments(self):
        try:
            if os.path.exists("payments.json"):
                with open("payments.json", 'r') as f:
                    return json.load(f)
        except:
            pass
        return []
    
    def save_sales(self, sales):
        with open("sales.json", 'w') as f:
            json.dump(sales, f, indent=2)
    
    def save_purchases(self, purchases):
        with open("purchases.json", 'w') as f:
            json.dump(purchases, f, indent=2)
    
    def save_orders(self, orders):
        with open("orders.json", 'w') as f:
            json.dump(orders, f, indent=2)
    
    def save_payments(self, payments):
        with open("payments.json", 'w') as f:
            json.dump(payments, f, indent=2)
    
    def create_summary_tab(self):
        summary_frame = ttk.Frame(self.notebook)
        self.notebook.add(summary_frame, text="📊 SUMMARY")
        
        # Create main container with scrollbar
        canvas = tk.Canvas(summary_frame)
        scrollbar = ttk.Scrollbar(summary_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Title
        title_label = tk.Label(scrollable_frame, text="BUSINESS SUMMARY", 
                              font=("Arial", 18, "bold"), bg="#2E86AB", fg="white")
        title_label.pack(fill="x", pady=(0, 20))
        
        # Summary cards frame
        cards_frame = tk.Frame(scrollable_frame)
        cards_frame.pack(fill="x", padx=20, pady=10)
        
        # Load data
        sales = self.load_sales()
        purchases = self.load_purchases()
        payments = self.load_payments()
        
        # Calculate totals
        total_sales = sum(sale.get('total_amount', 0) for sale in sales)
        total_purchases = sum(purchase.get('total', 0) for purchase in purchases)
        total_payments = sum(payment.get('amount', 0) for payment in payments)
        outstanding_balance = total_purchases - total_payments
        profit = total_sales - total_purchases
        
        # Create summary cards
        self.create_summary_card(cards_frame, "TOTAL SALES", f"KSH {total_sales:,.2f}", "#4CAF50", 0, 0)
        self.create_summary_card(cards_frame, "TOTAL PURCHASES", f"KSH {total_purchases:,.2f}", "#FF9800", 0, 1)
        self.create_summary_card(cards_frame, "TOTAL PAYMENTS", f"KSH {total_payments:,.2f}", "#2196F3", 1, 0)
        self.create_summary_card(cards_frame, "OUTSTANDING BALANCE", f"KSH {outstanding_balance:,.2f}", "#F44336", 1, 1)
        self.create_summary_card(cards_frame, "GROSS PROFIT", f"KSH {profit:,.2f}", "#9C27B0", 2, 0, columnspan=2)
        
        # Recent transactions
        recent_frame = tk.LabelFrame(scrollable_frame, text="Recent Transactions", font=("Arial", 12, "bold"))
        recent_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Recent sales
        recent_sales_frame = tk.Frame(recent_frame)
        recent_sales_frame.pack(side="left", fill="both", expand=True, padx=10)
        
        tk.Label(recent_sales_frame, text="Recent Sales", font=("Arial", 11, "bold")).pack()
        recent_sales = sorted(sales, key=lambda x: x.get('sale_date', ''), reverse=True)[:5]
        
        for sale in recent_sales:
            sale_text = f"{sale.get('customer_name', 'N/A')} - KSH {sale.get('total_amount', 0):,.2f}"
            tk.Label(recent_sales_frame, text=sale_text, font=("Arial", 9)).pack(anchor="w")
        
        # Recent purchases
        recent_purchases_frame = tk.Frame(recent_frame)
        recent_purchases_frame.pack(side="right", fill="both", expand=True, padx=10)
        
        tk.Label(recent_purchases_frame, text="Recent Purchases", font=("Arial", 11, "bold")).pack()
        recent_purchases = sorted(purchases, key=lambda x: x.get('purchase_date', ''), reverse=True)[:5]
        
        for purchase in recent_purchases:
            purchase_text = f"{purchase.get('item', 'N/A')} - KSH {purchase.get('total', 0):,.2f}"
            tk.Label(recent_purchases_frame, text=purchase_text, font=("Arial", 9)).pack(anchor="w")
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def create_summary_card(self, parent, title, value, color, row, col, columnspan=1):
        card = tk.Frame(parent, bg=color, relief="raised", bd=2)
        card.grid(row=row, column=col, columnspan=columnspan, padx=10, pady=10, sticky="ew")
        
        tk.Label(card, text=title, font=("Arial", 10, "bold"), bg=color, fg="white").pack(pady=5)
        tk.Label(card, text=value, font=("Arial", 14, "bold"), bg=color, fg="white").pack(pady=5)
        
        parent.grid_columnconfigure(col, weight=1)
        if columnspan > 1:
            parent.grid_columnconfigure(col+1, weight=1)
    
    def create_orders_tab(self):
        orders_frame = ttk.Frame(self.notebook)
        self.notebook.add(orders_frame, text="📋 ORDERS")
        
        # Create order form
        form_frame = tk.LabelFrame(orders_frame, text="New Order", font=("Arial", 12, "bold"))
        form_frame.pack(fill="x", padx=10, pady=5)
        
        # Customer name
        tk.Label(form_frame, text="Customer Name:", font=("Arial", 10)).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.order_customer_entry = tk.Entry(form_frame, width=20, font=("Arial", 10))
        self.order_customer_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Item details
        tk.Label(form_frame, text="Item:", font=("Arial", 10)).grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.order_item_entry = tk.Entry(form_frame, width=15, font=("Arial", 10))
        self.order_item_entry.grid(row=0, column=3, padx=5, pady=5)
        
        tk.Label(form_frame, text="Quantity:", font=("Arial", 10)).grid(row=0, column=4, sticky="w", padx=5, pady=5)
        self.order_quantity_entry = tk.Entry(form_frame, width=10, font=("Arial", 10))
        self.order_quantity_entry.grid(row=0, column=5, padx=5, pady=5)
        
        tk.Label(form_frame, text="Price:", font=("Arial", 10)).grid(row=0, column=6, sticky="w", padx=5, pady=5)
        self.order_price_entry = tk.Entry(form_frame, width=10, font=("Arial", 10))
        self.order_price_entry.grid(row=0, column=7, padx=5, pady=5)
        
        # Buttons
        tk.Button(form_frame, text="Add Item", command=self.add_order_item, 
                 bg="#4CAF50", fg="white", font=("Arial", 9, "bold")).grid(row=0, column=8, padx=5, pady=5)
        
        # Order items display
        items_frame = tk.LabelFrame(orders_frame, text="Order Items", font=("Arial", 12, "bold"))
        items_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Treeview for order items
        columns = ("Item", "Quantity", "Price", "Total")
        self.order_tree = ttk.Treeview(items_frame, columns=columns, show="headings", height=8)
        
        for col in columns:
            self.order_tree.heading(col, text=col)
            self.order_tree.column(col, width=100)
        
        self.order_tree.pack(side="left", fill="both", expand=True)
        
        # Scrollbar for order tree
        order_scrollbar = ttk.Scrollbar(items_frame, orient="vertical", command=self.order_tree.yview)
        order_scrollbar.pack(side="right", fill="y")
        self.order_tree.configure(yscrollcommand=order_scrollbar.set)
        
        # Order total and actions
        bottom_frame = tk.Frame(orders_frame)
        bottom_frame.pack(fill="x", padx=10, pady=5)
        
        self.order_total_label = tk.Label(bottom_frame, text="Total: KSH 0.00", 
                                         font=("Arial", 14, "bold"))
        self.order_total_label.pack(side="left")
        
        tk.Button(bottom_frame, text="Clear Order", command=self.clear_order,
                 bg="#FF5722", fg="white", font=("Arial", 10, "bold")).pack(side="right", padx=5)
        
        tk.Button(bottom_frame, text="Save Order", command=self.save_order,
                 bg="#2196F3", fg="white", font=("Arial", 10, "bold")).pack(side="right", padx=5)
        
        # Orders history
        history_frame = tk.LabelFrame(orders_frame, text="Orders History", font=("Arial", 12, "bold"))
        history_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Treeview for orders history
        history_columns = ("Order No", "Customer", "Date", "Total", "Status")
        self.orders_history_tree = ttk.Treeview(history_frame, columns=history_columns, show="headings", height=10)
        
        for col in history_columns:
            self.orders_history_tree.heading(col, text=col)
            self.orders_history_tree.column(col, width=120)
        
        self.orders_history_tree.pack(side="left", fill="both", expand=True)
        
        # Scrollbar for history tree
        history_scrollbar = ttk.Scrollbar(history_frame, orient="vertical", command=self.orders_history_tree.yview)
        history_scrollbar.pack(side="right", fill="y")
        self.orders_history_tree.configure(yscrollcommand=history_scrollbar.set)
        
        self.refresh_orders_history()
    
    def add_order_item(self):
        try:
            item = self.order_item_entry.get().strip().upper()
            quantity = float(self.order_quantity_entry.get())
            price = float(self.order_price_entry.get())
            total = quantity * price
            
            if not item:
                messagebox.showerror("Error", "Please enter item name")
                return
            
            # Add to order items list
            self.order_items.append({
                "item": item,
                "quantity": quantity,
                "price": price,
                "total": total
            })
            
            # Add to treeview
            self.order_tree.insert("", "end", values=(item, quantity, price, f"{total:.2f}"))
            
            # Update total
            self.order_total += total
            self.order_total_label.config(text=f"Total: KSH {self.order_total:.2f}")
            
            # Clear entries
            self.order_item_entry.delete(0, tk.END)
            self.order_quantity_entry.delete(0, tk.END)
            self.order_price_entry.delete(0, tk.END)
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for quantity and price")
    
    def clear_order(self):
        self.order_items = []
        self.order_total = 0.0
        self.order_total_label.config(text="Total: KSH 0.00")
        
        for item in self.order_tree.get_children():
            self.order_tree.delete(item)
        
        self.order_customer_entry.delete(0, tk.END)
    
    def save_order(self):
        if not self.order_items:
            messagebox.showerror("Error", "No items in order")
            return
        
        customer_name = self.order_customer_entry.get().strip().upper()
        if not customer_name:
            messagebox.showerror("Error", "Please enter customer name")
            return
        
        # Create order
        order = {
            "id": len(self.load_orders()) + 1,
            "order_no": f"ORD-{self.order_counter:04d}",
            "customer_name": customer_name,
            "items": self.order_items.copy(),
            "total_amount": self.order_total,
            "order_date": datetime.now().isoformat(),
            "status": "Pending"
        }
        
        # Save to file
        orders = self.load_orders()
        orders.append(order)
        self.save_orders(orders)
        
        messagebox.showinfo("Success", f"Order {order['order_no']} saved successfully!")
        
        self.order_counter += 1
        self.clear_order()
        self.refresh_orders_history()
    
    def refresh_orders_history(self):
        # Clear existing items
        for item in self.orders_history_tree.get_children():
            self.orders_history_tree.delete(item)
        
        # Load and display orders
        orders = self.load_orders()
        for order in reversed(orders):  # Show newest first
            self.orders_history_tree.insert("", "end", values=(
                order.get('order_no', 'N/A'),
                order.get('customer_name', 'N/A'),
                order.get('order_date', 'N/A')[:10],  # Show date only
                f"KSH {order.get('total_amount', 0):.2f}",
                order.get('status', 'Pending')
            ))
    
    def create_purchase_tab(self):
        purchase_frame = ttk.Frame(self.notebook)
        self.notebook.add(purchase_frame, text="🛒 PURCHASES")
        
        # Create purchase form
        form_frame = tk.LabelFrame(purchase_frame, text="New Purchase", font=("Arial", 12, "bold"))
        form_frame.pack(fill="x", padx=10, pady=5)
        
        # Supplier and item details
        tk.Label(form_frame, text="Supplier:", font=("Arial", 10)).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.purchase_supplier_entry = tk.Entry(form_frame, width=15, font=("Arial", 10))
        self.purchase_supplier_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(form_frame, text="Item:", font=("Arial", 10)).grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.purchase_item_entry = tk.Entry(form_frame, width=15, font=("Arial", 10))
        self.purchase_item_entry.grid(row=0, column=3, padx=5, pady=5)
        
        tk.Label(form_frame, text="Quantity:", font=("Arial", 10)).grid(row=0, column=4, sticky="w", padx=5, pady=5)
        self.purchase_quantity_entry = tk.Entry(form_frame, width=10, font=("Arial", 10))
        self.purchase_quantity_entry.grid(row=0, column=5, padx=5, pady=5)
        
        tk.Label(form_frame, text="Price:", font=("Arial", 10)).grid(row=0, column=6, sticky="w", padx=5, pady=5)
        self.purchase_price_entry = tk.Entry(form_frame, width=10, font=("Arial", 10))
        self.purchase_price_entry.grid(row=0, column=7, padx=5, pady=5)
        
        tk.Label(form_frame, text="Invoice Ref:", font=("Arial", 10)).grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.purchase_invoice_entry = tk.Entry(form_frame, width=15, font=("Arial", 10))
        self.purchase_invoice_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(form_frame, text="Date:", font=("Arial", 10)).grid(row=1, column=2, sticky="w", padx=5, pady=5)
        self.purchase_date_entry = tk.Entry(form_frame, width=15, font=("Arial", 10))
        self.purchase_date_entry.grid(row=1, column=3, padx=5, pady=5)
        self.purchase_date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        # Buttons
        tk.Button(form_frame, text="Add Purchase", command=self.add_purchase, 
                 bg="#4CAF50", fg="white", font=("Arial", 9, "bold")).grid(row=1, column=4, padx=5, pady=5)
        
        # Purchases history
        history_frame = tk.LabelFrame(purchase_frame, text="Purchases History", font=("Arial", 12, "bold"))
        history_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Treeview for purchases
        columns = ("ID", "Supplier", "Item", "Quantity", "Price", "Total", "Date", "Invoice", "Paid")
        self.purchase_tree = ttk.Treeview(history_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.purchase_tree.heading(col, text=col)
            self.purchase_tree.column(col, width=100)
        
        self.purchase_tree.pack(side="left", fill="both", expand=True)
        
        # Scrollbar
        purchase_scrollbar = ttk.Scrollbar(history_frame, orient="vertical", command=self.purchase_tree.yview)
        purchase_scrollbar.pack(side="right", fill="y")
        self.purchase_tree.configure(yscrollcommand=purchase_scrollbar.set)
        
        # Action buttons
        action_frame = tk.Frame(purchase_frame)
        action_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Button(action_frame, text="Mark as Paid", command=self.mark_purchase_paid,
                 bg="#2196F3", fg="white", font=("Arial", 10, "bold")).pack(side="left", padx=5)
        
        tk.Button(action_frame, text="Generate Report", command=self.generate_purchase_report,
                 bg="#FF9800", fg="white", font=("Arial", 10, "bold")).pack(side="left", padx=5)
        
        self.refresh_purchases()
    
    def add_purchase(self):
        try:
            supplier = self.purchase_supplier_entry.get().strip().upper()
            item = self.purchase_item_entry.get().strip().upper()
            quantity = float(self.purchase_quantity_entry.get())
            price = float(self.purchase_price_entry.get())
            invoice_ref = self.purchase_invoice_entry.get().strip()
            date_str = self.purchase_date_entry.get().strip()
            
            if not all([supplier, item, invoice_ref]):
                messagebox.showerror("Error", "Please fill all required fields")
                return
            
            total = quantity * price
            
            # Create purchase record
            purchase = {
                "id": len(self.load_purchases()) + 1,
                "supplier": supplier,
                "item": item,
                "quantity": quantity,
                "price": price,
                "total": total,
                "purchase_date": f"{date_str}T00:00:00",
                "invoice_ref": invoice_ref,
                "paid": False,
                "balance": total
            }
            
            # Save to file
            purchases = self.load_purchases()
            purchases.append(purchase)
            self.save_purchases(purchases)
            
            messagebox.showinfo("Success", "Purchase added successfully!")
            
            # Clear entries
            self.purchase_supplier_entry.delete(0, tk.END)
            self.purchase_item_entry.delete(0, tk.END)
            self.purchase_quantity_entry.delete(0, tk.END)
            self.purchase_price_entry.delete(0, tk.END)
            self.purchase_invoice_entry.delete(0, tk.END)
            
            self.refresh_purchases()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for quantity and price")
    
    def mark_purchase_paid(self):
        selected = self.purchase_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a purchase to mark as paid")
            return
        
        item = self.purchase_tree.item(selected[0])
        purchase_id = int(item['values'][0])
        
        purchases = self.load_purchases()
        for purchase in purchases:
            if purchase['id'] == purchase_id:
                purchase['paid'] = True
                purchase['balance'] = 0
                break
        
        self.save_purchases(purchases)
        messagebox.showinfo("Success", "Purchase marked as paid!")
        self.refresh_purchases()
    
    def refresh_purchases(self):
        # Clear existing items
        for item in self.purchase_tree.get_children():
            self.purchase_tree.delete(item)
        
        # Load and display purchases
        purchases = self.load_purchases()
        for purchase in reversed(purchases):  # Show newest first
            paid_status = "Yes" if purchase.get('paid', False) else "No"
            self.purchase_tree.insert("", "end", values=(
                purchase.get('id', 'N/A'),
                purchase.get('supplier', 'N/A'),
                purchase.get('item', 'N/A'),
                purchase.get('quantity', 0),
                f"{purchase.get('price', 0):.2f}",
                f"{purchase.get('total', 0):.2f}",
                purchase.get('purchase_date', 'N/A')[:10],
                purchase.get('invoice_ref', 'N/A'),
                paid_status
            ))
    
    def generate_purchase_report(self):
        try:
            filename = f"purchases_{datetime.now().strftime('%m_%Y')}.pdf"
            c = canvas.Canvas(filename, pagesize=letter)
            
            # Title
            c.setFont("Helvetica-Bold", 16)
            c.drawString(50, 750, f"CESS FOODS - PURCHASE REPORT")
            c.drawString(50, 730, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
            
            # Headers
            c.setFont("Helvetica-Bold", 10)
            y = 700
            c.drawString(50, y, "Supplier")
            c.drawString(150, y, "Item")
            c.drawString(250, y, "Quantity")
            c.drawString(320, y, "Price")
            c.drawString(380, y, "Total")
            c.drawString(450, y, "Date")
            c.drawString(520, y, "Paid")
            
            # Data
            c.setFont("Helvetica", 9)
            purchases = self.load_purchases()
            total_amount = 0
            
            for i, purchase in enumerate(purchases):
                y = 680 - (i * 20)
                if y < 50:  # New page if needed
                    c.showPage()
                    y = 750
                
                c.drawString(50, y, str(purchase.get('supplier', 'N/A'))[:15])
                c.drawString(150, y, str(purchase.get('item', 'N/A'))[:15])
                c.drawString(250, y, str(purchase.get('quantity', 0)))
                c.drawString(320, y, f"{purchase.get('price', 0):.2f}")
                c.drawString(380, y, f"{purchase.get('total', 0):.2f}")
                c.drawString(450, y, str(purchase.get('purchase_date', 'N/A'))[:10])
                c.drawString(520, y, "Yes" if purchase.get('paid', False) else "No")
                
                total_amount += purchase.get('total', 0)
            
            # Total
            c.setFont("Helvetica-Bold", 12)
            c.drawString(300, y-30, f"TOTAL: KSH {total_amount:,.2f}")
            
            c.save()
            messagebox.showinfo("Success", f"Report saved as {filename}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report: {str(e)}")
    
    def create_sales_tab(self):
        sales_frame = ttk.Frame(self.notebook)
        self.notebook.add(sales_frame, text="💰 SALES")
        
        # Create sales form
        form_frame = tk.LabelFrame(sales_frame, text="New Sale", font=("Arial", 12, "bold"))
        form_frame.pack(fill="x", padx=10, pady=5)
        
        # Customer name
        tk.Label(form_frame, text="Customer:", font=("Arial", 10)).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.sales_customer_entry = tk.Entry(form_frame, width=20, font=("Arial", 10))
        self.sales_customer_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Item details
        tk.Label(form_frame, text="Item:", font=("Arial", 10)).grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.sales_item_entry = tk.Entry(form_frame, width=15, font=("Arial", 10))
        self.sales_item_entry.grid(row=0, column=3, padx=5, pady=5)
        
        tk.Label(form_frame, text="Quantity:", font=("Arial", 10)).grid(row=0, column=4, sticky="w", padx=5, pady=5)
        self.sales_quantity_entry = tk.Entry(form_frame, width=10, font=("Arial", 10))
        self.sales_quantity_entry.grid(row=0, column=5, padx=5, pady=5)
        
        tk.Label(form_frame, text="Price:", font=("Arial", 10)).grid(row=0, column=6, sticky="w", padx=5, pady=5)
        self.sales_price_entry = tk.Entry(form_frame, width=10, font=("Arial", 10))
        self.sales_price_entry.grid(row=0, column=7, padx=5, pady=5)
        
        # Buttons
        tk.Button(form_frame, text="Add Item", command=self.add_sales_item, 
                 bg="#4CAF50", fg="white", font=("Arial", 9, "bold")).grid(row=0, column=8, padx=5, pady=5)
        
        # Sales items display
        items_frame = tk.LabelFrame(sales_frame, text="Sale Items", font=("Arial", 12, "bold"))
        items_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Treeview for sales items
        columns = ("Item", "Quantity", "Price", "Total")
        self.sales_tree = ttk.Treeview(items_frame, columns=columns, show="headings", height=8)
        
        for col in columns:
            self.sales_tree.heading(col, text=col)
            self.sales_tree.column(col, width=100)
        
        self.sales_tree.pack(side="left", fill="both", expand=True)
        
        # Scrollbar for sales tree
        sales_scrollbar = ttk.Scrollbar(items_frame, orient="vertical", command=self.sales_tree.yview)
        sales_scrollbar.pack(side="right", fill="y")
        self.sales_tree.configure(yscrollcommand=sales_scrollbar.set)
        
        # Sales total and actions
        bottom_frame = tk.Frame(sales_frame)
        bottom_frame.pack(fill="x", padx=10, pady=5)
        
        self.sales_total_label = tk.Label(bottom_frame, text="Total: KSH 0.00", 
                                         font=("Arial", 14, "bold"))
        self.sales_total_label.pack(side="left")
        
        tk.Button(bottom_frame, text="Clear Sale", command=self.clear_sale,
                 bg="#FF5722", fg="white", font=("Arial", 10, "bold")).pack(side="right", padx=5)
        
        tk.Button(bottom_frame, text="Complete Sale", command=self.complete_sale,
                 bg="#2196F3", fg="white", font=("Arial", 10, "bold")).pack(side="right", padx=5)
        
        # Sales history
        history_frame = tk.LabelFrame(sales_frame, text="Sales History", font=("Arial", 12, "bold"))
        history_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Treeview for sales history
        history_columns = ("ID", "Customer", "Date", "Total")
        self.sales_history_tree = ttk.Treeview(history_frame, columns=history_columns, show="headings", height=10)
        
        for col in history_columns:
            self.sales_history_tree.heading(col, text=col)
            self.sales_history_tree.column(col, width=120)
        
        self.sales_history_tree.pack(side="left", fill="both", expand=True)
        
        # Scrollbar for history tree
        sales_history_scrollbar = ttk.Scrollbar(history_frame, orient="vertical", command=self.sales_history_tree.yview)
        sales_history_scrollbar.pack(side="right", fill="y")
        self.sales_history_tree.configure(yscrollcommand=sales_history_scrollbar.set)
        
        # Action buttons
        action_frame = tk.Frame(sales_frame)
        action_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Button(action_frame, text="Generate Sales Report", command=self.generate_sales_report,
                 bg="#FF9800", fg="white", font=("Arial", 10, "bold")).pack(side="left", padx=5)
        
        self.refresh_sales_history()
    
    def add_sales_item(self):
        try:
            item = self.sales_item_entry.get().strip().upper()
            quantity = float(self.sales_quantity_entry.get())
            price = float(self.sales_price_entry.get())
            total = quantity * price
            
            if not item:
                messagebox.showerror("Error", "Please enter item name")
                return
            
            # Add to sales items list
            self.sales_items.append({
                "item": item,
                "quantity": quantity,
                "price": price,
                "total": total
            })
            
            # Add to treeview
            self.sales_tree.insert("", "end", values=(item, quantity, price, f"{total:.2f}"))
            
            # Update total
            self.sales_total += total
            self.sales_total_label.config(text=f"Total: KSH {self.sales_total:.2f}")
            
            # Clear entries
            self.sales_item_entry.delete(0, tk.END)
            self.sales_quantity_entry.delete(0, tk.END)
            self.sales_price_entry.delete(0, tk.END)
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for quantity and price")
    
    def clear_sale(self):
        self.sales_items = []
        self.sales_total = 0.0
        self.sales_total_label.config(text="Total: KSH 0.00")
        
        for item in self.sales_tree.get_children():
            self.sales_tree.delete(item)
        
        self.sales_customer_entry.delete(0, tk.END)
    
    def complete_sale(self):
        if not self.sales_items:
            messagebox.showerror("Error", "No items in sale")
            return
        
        customer_name = self.sales_customer_entry.get().strip().upper()
        if not customer_name:
            messagebox.showerror("Error", "Please enter customer name")
            return
        
        # Create sale record
        sale = {
            "id": len(self.load_sales()) + 1,
            "invoice_no": f"INV-{self.invoice_counter:04d}",
            "customer_name": customer_name,
            "items": self.sales_items.copy(),
            "total_amount": self.sales_total,
            "sale_date": datetime.now().isoformat()
        }
        
        # Save to file
        sales = self.load_sales()
        sales.append(sale)
        self.save_sales(sales)
        
        messagebox.showinfo("Success", f"Sale completed! Invoice: {sale['invoice_no']}")
        
        self.invoice_counter += 1
        self.clear_sale()
        self.refresh_sales_history()
    
    def refresh_sales_history(self):
        # Clear existing items
        for item in self.sales_history_tree.get_children():
            self.sales_history_tree.delete(item)
        
        # Load and display sales
        sales = self.load_sales()
        for sale in reversed(sales):  # Show newest first
            self.sales_history_tree.insert("", "end", values=(
                sale.get('id', 'N/A'),
                sale.get('customer_name', 'N/A'),
                sale.get('sale_date', 'N/A')[:10],  # Show date only
                f"KSH {sale.get('total_amount', 0):.2f}"
            ))
    
    def generate_sales_report(self):
        try:
            filename = f"sales_{datetime.now().strftime('%m_%Y')}.pdf"
            c = canvas.Canvas(filename, pagesize=letter)
            
            # Title
            c.setFont("Helvetica-Bold", 16)
            c.drawString(50, 750, f"CESS FOODS - SALES REPORT")
            c.drawString(50, 730, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
            
            # Headers
            c.setFont("Helvetica-Bold", 10)
            y = 700
            c.drawString(50, y, "Invoice")
            c.drawString(120, y, "Customer")
            c.drawString(220, y, "Date")
            c.drawString(300, y, "Total")
            
            # Data
            c.setFont("Helvetica", 9)
            sales = self.load_sales()
            total_amount = 0
            
            for i, sale in enumerate(sales):
                y = 680 - (i * 20)
                if y < 50:  # New page if needed
                    c.showPage()
                    y = 750
                
                c.drawString(50, y, str(sale.get('invoice_no', 'N/A')))
                c.drawString(120, y, str(sale.get('customer_name', 'N/A'))[:15])
                c.drawString(220, y, str(sale.get('sale_date', 'N/A'))[:10])
                c.drawString(300, y, f"KSH {sale.get('total_amount', 0):.2f}")
                
                total_amount += sale.get('total_amount', 0)
            
            # Total
            c.setFont("Helvetica-Bold", 12)
            c.drawString(200, y-30, f"TOTAL SALES: KSH {total_amount:,.2f}")
            
            c.save()
            messagebox.showinfo("Success", f"Sales report saved as {filename}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report: {str(e)}")
    
    def create_supplier_payments_tab(self):
        payments_frame = ttk.Frame(self.notebook)
        self.notebook.add(payments_frame, text="💳 PAYMENTS")
        
        # Payment form
        form_frame = tk.LabelFrame(payments_frame, text="New Payment", font=("Arial", 12, "bold"))
        form_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Label(form_frame, text="Supplier:", font=("Arial", 10)).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.payment_supplier_entry = tk.Entry(form_frame, width=20, font=("Arial", 10))
        self.payment_supplier_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(form_frame, text="Amount:", font=("Arial", 10)).grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.payment_amount_entry = tk.Entry(form_frame, width=15, font=("Arial", 10))
        self.payment_amount_entry.grid(row=0, column=3, padx=5, pady=5)
        
        tk.Label(form_frame, text="Method:", font=("Arial", 10)).grid(row=0, column=4, sticky="w", padx=5, pady=5)
        self.payment_method_var = tk.StringVar(value="CASH")
        payment_method_combo = ttk.Combobox(form_frame, textvariable=self.payment_method_var, 
                                           values=["CASH", "MPESA", "BANK"], width=12)
        payment_method_combo.grid(row=0, column=5, padx=5, pady=5)
        
        tk.Label(form_frame, text="Reference:", font=("Arial", 10)).grid(row=0, column=6, sticky="w", padx=5, pady=5)
        self.payment_reference_entry = tk.Entry(form_frame, width=15, font=("Arial", 10))
        self.payment_reference_entry.grid(row=0, column=7, padx=5, pady=5)
        
        tk.Button(form_frame, text="Add Payment", command=self.add_payment,
                 bg="#4CAF50", fg="white", font=("Arial", 9, "bold")).grid(row=0, column=8, padx=5, pady=5)
        
        # Payments history
        history_frame = tk.LabelFrame(payments_frame, text="Payment History", font=("Arial", 12, "bold"))
        history_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Treeview for payments
        columns = ("ID", "Supplier", "Amount", "Method", "Reference", "Date")
        self.payments_tree = ttk.Treeview(history_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.payments_tree.heading(col, text=col)
            self.payments_tree.column(col, width=120)
        
        self.payments_tree.pack(side="left", fill="both", expand=True)
        
        # Scrollbar
        payments_scrollbar = ttk.Scrollbar(history_frame, orient="vertical", command=self.payments_tree.yview)
        payments_scrollbar.pack(side="right", fill="y")
        self.payments_tree.configure(yscrollcommand=payments_scrollbar.set)
        
        # Action buttons
        action_frame = tk.Frame(payments_frame)
        action_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Button(action_frame, text="Generate Payment Report", command=self.generate_payment_report,
                 bg="#FF9800", fg="white", font=("Arial", 10, "bold")).pack(side="left", padx=5)
        
        tk.Button(action_frame, text="Supplier Statement", command=self.generate_supplier_statement,
                 bg="#9C27B0", fg="white", font=("Arial", 10, "bold")).pack(side="left", padx=5)
        
        self.refresh_payments()
    
    def add_payment(self):
        try:
            supplier = self.payment_supplier_entry.get().strip().upper()
            amount = float(self.payment_amount_entry.get())
            method = self.payment_method_var.get()
            reference = self.payment_reference_entry.get().strip()
            
            if not supplier:
                messagebox.showerror("Error", "Please enter supplier name")
                return
            
            # Create payment record
            payment = {
                "id": len(self.load_payments()) + 1,
                "supplier": supplier,
                "amount": amount,
                "method": method,
                "reference": reference,
                "payment_date": datetime.now().isoformat(),
                "type": "supplier_payment"
            }
            
            # Save to file
            payments = self.load_payments()
            payments.append(payment)
            self.save_payments(payments)
            
            messagebox.showinfo("Success", "Payment recorded successfully!")
            
            # Clear entries
            self.payment_supplier_entry.delete(0, tk.END)
            self.payment_amount_entry.delete(0, tk.END)
            self.payment_reference_entry.delete(0, tk.END)
            
            self.refresh_payments()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount")
    
    def refresh_payments(self):
        # Clear existing items
        for item in self.payments_tree.get_children():
            self.payments_tree.delete(item)
        
        # Load and display payments
        payments = self.load_payments()
        for payment in reversed(payments):  # Show newest first
            self.payments_tree.insert("", "end", values=(
                payment.get('id', 'N/A'),
                payment.get('supplier', 'N/A'),
                f"KSH {payment.get('amount', 0):,.2f}",
                payment.get('method', 'N/A'),
                payment.get('reference', 'N/A'),
                payment.get('payment_date', 'N/A')[:10]
            ))
    
    def generate_payment_report(self):
        try:
            filename = f"payment_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            c = canvas.Canvas(filename, pagesize=letter)
            
            # Title
            c.setFont("Helvetica-Bold", 16)
            c.drawString(50, 750, f"CESS FOODS - PAYMENT HISTORY")
            c.drawString(50, 730, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
            
            # Headers
            c.setFont("Helvetica-Bold", 10)
            y = 700
            c.drawString(50, y, "Supplier")
            c.drawString(150, y, "Amount")
            c.drawString(220, y, "Method")
            c.drawString(280, y, "Reference")
            c.drawString(380, y, "Date")
            
            # Data
            c.setFont("Helvetica", 9)
            payments = self.load_payments()
            total_amount = 0
            
            for i, payment in enumerate(payments):
                y = 680 - (i * 20)
                if y < 50:  # New page if needed
                    c.showPage()
                    y = 750
                
                c.drawString(50, y, str(payment.get('supplier', 'N/A'))[:15])
                c.drawString(150, y, f"KSH {payment.get('amount', 0):,.2f}")
                c.drawString(220, y, str(payment.get('method', 'N/A')))
                c.drawString(280, y, str(payment.get('reference', 'N/A'))[:15])
                c.drawString(380, y, str(payment.get('payment_date', 'N/A'))[:10])
                
                total_amount += payment.get('amount', 0)
            
            # Total
            c.setFont("Helvetica-Bold", 12)
            c.drawString(200, y-30, f"TOTAL PAYMENTS: KSH {total_amount:,.2f}")
            
            c.save()
            messagebox.showinfo("Success", f"Payment report saved as {filename}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report: {str(e)}")
    
    def generate_supplier_statement(self):
        # Get supplier name
        supplier = tk.simpledialog.askstring("Supplier Statement", "Enter supplier name:")
        if not supplier:
            return
        
        supplier = supplier.upper()
        
        try:
            filename = f"supplier_statement_{supplier}_{datetime.now().strftime('%Y%m%d')}.pdf"
            c = canvas.Canvas(filename, pagesize=letter)
            
            # Title
            c.setFont("Helvetica-Bold", 16)
            c.drawString(50, 750, f"CESS FOODS - SUPPLIER STATEMENT")
            c.drawString(50, 730, f"Supplier: {supplier}")
            c.drawString(50, 710, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
            
            # Purchases section
            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, 680, "PURCHASES:")
            
            c.setFont("Helvetica-Bold", 10)
            y = 660
            c.drawString(50, y, "Date")
            c.drawString(120, y, "Item")
            c.drawString(220, y, "Quantity")
            c.drawString(280, y, "Price")
            c.drawString(340, y, "Total")
            c.drawString(400, y, "Invoice")
            c.drawString(480, y, "Paid")
            
            # Purchase data
            c.setFont("Helvetica", 9)
            purchases = [p for p in self.load_purchases() if p.get('supplier', '').upper() == supplier]
            total_purchases = 0
            
            for i, purchase in enumerate(purchases):
                y = 640 - (i * 15)
                if y < 300:  # Leave space for payments section
                    break
                
                c.drawString(50, y, str(purchase.get('purchase_date', 'N/A'))[:10])
                c.drawString(120, y, str(purchase.get('item', 'N/A'))[:12])
                c.drawString(220, y, str(purchase.get('quantity', 0)))
                c.drawString(280, y, f"{purchase.get('price', 0):.2f}")
                c.drawString(340, y, f"{purchase.get('total', 0):.2f}")
                c.drawString(400, y, str(purchase.get('invoice_ref', 'N/A'))[:10])
                c.drawString(480, y, "Yes" if purchase.get('paid', False) else "No")
                
                total_purchases += purchase.get('total', 0)
            
            # Payments section
            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, y-40, "PAYMENTS:")
            
            c.setFont("Helvetica-Bold", 10)
            y = y-60
            c.drawString(50, y, "Date")
            c.drawString(120, y, "Amount")
            c.drawString(200, y, "Method")
            c.drawString(260, y, "Reference")
            
            # Payment data
            c.setFont("Helvetica", 9)
            payments = [p for p in self.load_payments() if p.get('supplier', '').upper() == supplier]
            total_payments = 0
            
            for i, payment in enumerate(payments):
                y = y - 20
                if y < 100:
                    break
                
                c.drawString(50, y, str(payment.get('payment_date', 'N/A'))[:10])
                c.drawString(120, y, f"KSH {payment.get('amount', 0):,.2f}")
                c.drawString(200, y, str(payment.get('method', 'N/A')))
                c.drawString(260, y, str(payment.get('reference', 'N/A'))[:15])
                
                total_payments += payment.get('amount', 0)
            
            # Summary
            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, y-40, f"TOTAL PURCHASES: KSH {total_purchases:,.2f}")
            c.drawString(50, y-60, f"TOTAL PAYMENTS: KSH {total_payments:,.2f}")
            c.drawString(50, y-80, f"BALANCE: KSH {total_purchases - total_payments:,.2f}")
            
            c.save()
            messagebox.showinfo("Success", f"Supplier statement saved as {filename}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate statement: {str(e)}")

if __name__ == "__main__":
    app = FullScreenApp()
    app.root.mainloop()