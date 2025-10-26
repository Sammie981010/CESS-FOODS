import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime
from collections import defaultdict
try:
    from backup_system import backup_system
except ImportError:
    backup_system = None

class FoodApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("CESS FOODS")
        self.root.state('zoomed')
        self.root.withdraw()
        
        self.sales_items = []
        self.sales_total = 0.0
        self.user_role = None  # Track user permissions
        
        self.show_login()
    
    def show_login(self):
        self.login_window = tk.Toplevel()
        self.login_window.title("CESS FOODS - Login")
        self.login_window.geometry("500x400")
        self.login_window.configure(bg="#2193b0")
        
        # Header section with Fresh Farm Blue gradient effect
        header_frame = tk.Frame(self.login_window, bg="#2193b0", height=120)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="🐔 Welcome to", font=("Arial", 14), 
                fg="#E8F8FC", bg="#2193b0").pack(pady=(20,5))
        
        tk.Label(header_frame, text="CESS FOODS", font=("Arial", 24, "bold"), 
                fg="white", bg="#2193b0").pack()
        
        tk.Label(header_frame, text="Fresh, Reliable Supplies", font=("Arial", 12), 
                fg="#B8E6F0", bg="#2193b0").pack(pady=(0,10))
        
        # Middle transition section
        mid_frame = tk.Frame(self.login_window, bg="#4ABDD1", height=20)
        mid_frame.pack(fill="x")
        
        # Login form with light aqua styling
        login_frame = tk.Frame(self.login_window, bg="#6dd5ed", relief="flat")
        login_frame.pack(padx=60, pady=20, fill="both", expand=True)
        
        # Inner form with white background - centered
        inner_frame = tk.Frame(login_frame, bg="white", relief="flat")
        inner_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Center container
        center_frame = tk.Frame(inner_frame, bg="white")
        center_frame.pack(expand=True)
        
        tk.Label(center_frame, text="Sign In", font=("Arial", 18, "bold"), 
                fg="#2193b0", bg="white").pack(pady=(20,40))
        
        # Email field with placeholder
        self.email_entry = tk.Entry(center_frame, width=30, font=("Arial", 11), 
                                   relief="solid", bd=1, highlightcolor="#2193b0")
        self.email_entry.pack(pady=(0,20), ipady=8)
        self.email_entry.insert(0, "Email Address")
        self.email_entry.config(fg="#999999")
        self.email_entry.bind("<FocusIn>", self.clear_email_placeholder)
        self.email_entry.bind("<FocusOut>", self.restore_email_placeholder)
        
        # Password field with placeholder
        self.password_entry = tk.Entry(center_frame, width=30, font=("Arial", 11), 
                                      relief="solid", bd=1, highlightcolor="#2193b0")
        self.password_entry.pack(pady=(0,30), ipady=8)
        self.password_entry.insert(0, "Password")
        self.password_entry.config(fg="#999999")
        self.password_entry.bind("<FocusIn>", self.clear_password_placeholder)
        self.password_entry.bind("<FocusOut>", self.restore_password_placeholder)
        
        # Login button with Fresh Farm Blue styling
        tk.Button(center_frame, text="🌿 Sign In", command=self.validate_login,
                 bg="#2193b0", fg="white", font=("Arial", 12, "bold"),
                 relief="flat", width=20, height=2, cursor="hand2",
                 activebackground="#1a7a94").pack(pady=10)
        
        self.email_entry.focus()
    
    def clear_email_placeholder(self, event):
        if self.email_entry.get() == "Email Address":
            self.email_entry.delete(0, tk.END)
            self.email_entry.config(fg="black")
    
    def restore_email_placeholder(self, event):
        if not self.email_entry.get():
            self.email_entry.insert(0, "Email Address")
            self.email_entry.config(fg="#999999")
    
    def clear_password_placeholder(self, event):
        if self.password_entry.get() == "Password":
            self.password_entry.delete(0, tk.END)
            self.password_entry.config(fg="black", show="*")
    
    def restore_password_placeholder(self, event):
        if not self.password_entry.get():
            self.password_entry.insert(0, "Password")
            self.password_entry.config(fg="#999999", show="")
    
    def validate_login(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
        
        # Clear placeholders for validation
        if email == "Email Address":
            email = ""
        if password == "Password":
            password = ""
        
        if email == "admin@cess.com" and password == "admin123":
            self.user_role = "admin"
            self.login_window.destroy()
            self.root.deiconify()
            self.create_main_interface()
        elif email == "cashier@cess.com" and password == "cashier123":
            self.user_role = "cashier"
            self.login_window.destroy()
            self.root.deiconify()
            self.create_main_interface()
        else:
            messagebox.showerror("Login Failed", "Invalid email or password")
    
    def create_main_interface(self):
        # Title
        title_frame = tk.Frame(self.root, bg="#2E86AB", height=60)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)
        
        tk.Label(title_frame, text="CESS FOODS - MANAGEMENT SYSTEM", 
                font=("Arial", 20, "bold"), bg="#2E86AB", fg="white").pack(pady=15)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Initialize variables
        self.purchase_items = []
        self.purchase_total = 0.0
        self.order_items = []
        self.order_total = 0.0
        
        # Create all tabs based on user role
        self.create_dashboard_tab()
        if self.user_role == "admin":
            self.create_orders_tab()
        self.create_purchase_tab()
        self.create_sales_tab()
        self.create_supplier_payments_tab()  # Available for both roles
    
    def create_dashboard_tab(self):
        dashboard_frame = ttk.Frame(self.notebook)
        self.notebook.add(dashboard_frame, text="Dashboard")
        
        tk.Label(dashboard_frame, text="📊 BUSINESS DASHBOARD", 
                font=("Arial", 20, "bold"), fg="#2E86AB").pack(pady=10)
        
        # Stats cards
        stats_frame = tk.Frame(dashboard_frame)
        stats_frame.pack(fill="x", padx=20, pady=10)
        
        # Sales card
        sales_card = tk.Frame(stats_frame, bg="#4CAF50", relief="flat", bd=1)
        sales_card.pack(side="left", fill="both", expand=True, padx=(0, 8))
        
        tk.Label(sales_card, text="💰 SALES", font=("Arial", 10, "bold"), 
                fg="white", bg="#4CAF50").pack(pady=5)
        self.sales_amount_label = tk.Label(sales_card, text="KSH 0.00", 
                                          font=("Arial", 12, "bold"), fg="white", bg="#4CAF50")
        self.sales_amount_label.pack()
        
        # Purchases card
        purchases_card = tk.Frame(stats_frame, bg="#FF9800", relief="flat", bd=1)
        purchases_card.pack(side="left", fill="both", expand=True, padx=8)
        
        tk.Label(purchases_card, text="📦 PURCHASES", font=("Arial", 10, "bold"), 
                fg="white", bg="#FF9800").pack(pady=5)
        self.purchases_amount_label = tk.Label(purchases_card, text="KSH 0.00", 
                                              font=("Arial", 12, "bold"), fg="white", bg="#FF9800")
        self.purchases_amount_label.pack()
        
        # Profit card
        profit_card = tk.Frame(stats_frame, bg="#2196F3", relief="flat", bd=1)
        profit_card.pack(side="left", fill="both", expand=True, padx=(8, 0))
        
        tk.Label(profit_card, text="📈 PROFIT", font=("Arial", 10, "bold"), 
                fg="white", bg="#2196F3").pack(pady=5)
        self.profit_amount_label = tk.Label(profit_card, text="KSH 0.00", 
                                           font=("Arial", 12, "bold"), fg="white", bg="#2196F3")
        self.profit_amount_label.pack()
        
        # Export Reports section - available for both admin and cashier
        export_frame = tk.Frame(dashboard_frame)
        export_frame.pack(fill="x", padx=20, pady=5)
        
        tk.Label(export_frame, text="📊 Export Reports:", font=("Arial", 10, "bold")).pack(side="left", padx=5)
        
        self.export_var = tk.StringVar(value="Select Report")
        export_dropdown = ttk.Combobox(export_frame, textvariable=self.export_var, width=20, state="readonly",
                                      values=["Weekly Sales", "Monthly Sales", "Weekly Purchases", "Monthly Purchases", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])
        export_dropdown.pack(side="left", padx=5)
        
        tk.Button(export_frame, text="Export", command=self.export_selected_report,
                 bg="#2196F3", fg="white", font=("Arial", 9, "bold"),
                 width=8, height=1).pack(side="left", padx=5)
        
        # Sales, Purchases and Profit graph
        graph_frame = tk.LabelFrame(dashboard_frame, text="📊 Weekly Sales, Purchases & Profit", font=("Arial", 12, "bold"))
        graph_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.create_sales_graph(graph_frame)
        
        self.update_dashboard()
    
    def create_orders_tab(self):
        orders_frame = ttk.Frame(self.notebook)
        self.notebook.add(orders_frame, text="Orders")
        
        # Customer
        customer_frame = tk.Frame(orders_frame)
        customer_frame.pack(fill="x", padx=20, pady=10)
        tk.Label(customer_frame, text="Customer:", font=("Arial", 12, "bold")).pack(side="left")
        self.order_customer_entry = tk.Entry(customer_frame, width=30, font=("Arial", 12))
        self.order_customer_entry.pack(side="left", padx=10)
        
        # Order items
        order_item_frame = tk.LabelFrame(orders_frame, text="Add Order Items", font=("Arial", 12, "bold"))
        order_item_frame.pack(fill="x", padx=20, pady=10)
        
        order_fields_frame = tk.Frame(order_item_frame)
        order_fields_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Label(order_fields_frame, text="Item:").grid(row=0, column=0, padx=5, pady=5)
        self.order_item_entry = tk.Entry(order_fields_frame, width=20)
        self.order_item_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(order_fields_frame, text="Qty:").grid(row=0, column=2, padx=5, pady=5)
        self.order_qty_entry = tk.Entry(order_fields_frame, width=10)
        self.order_qty_entry.grid(row=0, column=3, padx=5, pady=5)
        
        tk.Label(order_fields_frame, text="Price:").grid(row=0, column=4, padx=5, pady=5)
        self.order_price_entry = tk.Entry(order_fields_frame, width=10)
        self.order_price_entry.grid(row=0, column=5, padx=5, pady=5)
        
        tk.Button(order_fields_frame, text="Add Item", command=self.add_order_item,
                 bg="#4CAF50", fg="white").grid(row=0, column=6, padx=10, pady=5)
        
        # Order list
        order_list_frame = tk.LabelFrame(orders_frame, text="Order Items", font=("Arial", 12, "bold"))
        order_list_frame.pack(fill="both", expand=True, padx=20, pady=5)
        
        self.order_tree = ttk.Treeview(order_list_frame, columns=("Item", "Qty", "Price", "Total"),
                                      show="headings", height=6)
        for col in ["Item", "Qty", "Price", "Total"]:
            self.order_tree.heading(col, text=col)
            self.order_tree.column(col, width=120, anchor="center")
        
        order_scrollbar = ttk.Scrollbar(order_list_frame, orient="vertical", command=self.order_tree.yview)
        self.order_tree.configure(yscrollcommand=order_scrollbar.set)
        
        self.order_tree.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        order_scrollbar.pack(side="right", fill="y")
        
        # Order total
        self.order_total_label = tk.Label(orders_frame, text="Total: KSH 0.00",
                                         font=("Arial", 14, "bold"), fg="#2E86AB", bg="#f8f9fa",
                                         relief="ridge", bd=2, padx=20, pady=10)
        self.order_total_label.pack(pady=5)
        
        # Order buttons - admin only
        if self.user_role == "admin":
            order_btn_frame = tk.Frame(orders_frame)
            order_btn_frame.pack(pady=10)
            
            tk.Button(order_btn_frame, text="Save Order", command=self.save_order,
                     bg="#4CAF50", fg="white", font=("Arial", 12, "bold"),
                     width=12, height=2).pack(side="left", padx=5)
            
            tk.Button(order_btn_frame, text="Clear All", command=self.clear_order,
                     bg="#FFC107", fg="black", font=("Arial", 12, "bold"),
                     width=12, height=2).pack(side="left", padx=5)
            
            tk.Button(order_btn_frame, text="Remove Selected", command=self.remove_selected_order,
                     bg="#f44336", fg="white", font=("Arial", 12, "bold"),
                     width=12, height=2).pack(side="left", padx=5)
    
    def create_purchase_tab(self):
        purchase_frame = ttk.Frame(self.notebook)
        self.notebook.add(purchase_frame, text="Purchases")
        
        # Invoice No and Date selection
        date_frame = tk.Frame(purchase_frame)
        date_frame.pack(fill="x", padx=20, pady=5)
        
        tk.Label(date_frame, text="Invoice No:", font=("Arial", 12, "bold")).pack(side="left")
        self.purchase_invoice_entry = tk.Entry(date_frame, width=15, font=("Arial", 12))
        self.purchase_invoice_entry.pack(side="left", padx=10)
        self.purchase_invoice_entry.insert(0, self.generate_purchase_invoice_no())
        
        tk.Label(date_frame, text="Purchase Date:", font=("Arial", 12, "bold")).pack(side="left", padx=(20,5))
        self.purchase_date_entry = tk.Entry(date_frame, width=12, font=("Arial", 12))
        self.purchase_date_entry.pack(side="left", padx=10)
        self.purchase_date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        
        # Purchase items
        item_frame = tk.LabelFrame(purchase_frame, text="Add Purchase Items", font=("Arial", 12, "bold"))
        item_frame.pack(fill="x", padx=20, pady=10)
        
        fields_frame = tk.Frame(item_frame)
        fields_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Label(fields_frame, text="Supplier:").grid(row=0, column=0, padx=5, pady=5)
        self.supplier_entry = tk.Entry(fields_frame, width=15)
        self.supplier_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(fields_frame, text="Item:").grid(row=0, column=2, padx=5, pady=5)
        self.purchase_item_entry = tk.Entry(fields_frame, width=15)
        self.purchase_item_entry.grid(row=0, column=3, padx=5, pady=5)
        
        tk.Label(fields_frame, text="Qty:").grid(row=0, column=4, padx=5, pady=5)
        self.purchase_qty_entry = tk.Entry(fields_frame, width=8)
        self.purchase_qty_entry.grid(row=0, column=5, padx=5, pady=5)
        
        tk.Label(fields_frame, text="Price:").grid(row=0, column=6, padx=5, pady=5)
        self.purchase_price_entry = tk.Entry(fields_frame, width=10)
        self.purchase_price_entry.grid(row=0, column=7, padx=5, pady=5)
        
        tk.Button(fields_frame, text="Add Item", command=self.add_purchase_item,
                 bg="#4CAF50", fg="white").grid(row=1, column=6, columnspan=2, padx=5, pady=5)
        
        # Purchase list
        list_frame = tk.LabelFrame(purchase_frame, text="Purchase Items", font=("Arial", 12, "bold"))
        list_frame.pack(fill="x", padx=20, pady=5)
        
        self.purchase_tree = ttk.Treeview(list_frame, columns=("Supplier", "Item", "Qty", "Price", "Total"),
                                         show="headings", height=5)
        for col in ["Supplier", "Item", "Qty", "Price", "Total"]:
            self.purchase_tree.heading(col, text=col)
            self.purchase_tree.column(col, width=120, anchor="center")
        
        purchase_scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.purchase_tree.yview)
        self.purchase_tree.configure(yscrollcommand=purchase_scrollbar.set)
        
        self.purchase_tree.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        purchase_scrollbar.pack(side="right", fill="y")
        
        # Purchase total
        self.purchase_total_label = tk.Label(purchase_frame, text="Total: KSH 0.00",
                                           font=("Arial", 14, "bold"), fg="#2E86AB", bg="#f8f9fa",
                                           relief="ridge", bd=2, padx=20, pady=10)
        self.purchase_total_label.pack(pady=15)
        
        # Purchase buttons - role-based access
        purchase_btn_frame = tk.Frame(purchase_frame)
        purchase_btn_frame.pack(pady=5)
        
        if self.user_role == "admin":
            tk.Button(purchase_btn_frame, text="Save Purchase", command=self.save_purchase,
                     bg="#4CAF50", fg="white", font=("Arial", 10, "bold"),
                     width=11, height=1).pack(side="left", padx=3)
            
            tk.Button(purchase_btn_frame, text="Clear All", command=self.clear_purchase,
                     bg="#FFC107", fg="black", font=("Arial", 10, "bold"),
                     width=11, height=1).pack(side="left", padx=3)
            
            tk.Button(purchase_btn_frame, text="Remove Selected", command=self.remove_selected_purchase,
                     bg="#f44336", fg="white", font=("Arial", 10, "bold"),
                     width=11, height=1).pack(side="left", padx=3)
        
        # Print and View buttons available for both roles
        tk.Button(purchase_btn_frame, text="Print Receipt", command=self.print_purchase_receipt,
                 bg="#9C27B0", fg="white", font=("Arial", 10, "bold"),
                 width=11, height=1).pack(side="left", padx=3)
        
        tk.Button(purchase_btn_frame, text="View Purchases", command=self.open_purchases_window,
                 bg="#2196F3", fg="white", font=("Arial", 10, "bold"),
                 width=11, height=1).pack(side="left", padx=3)
    
    def create_sales_tab(self):
        sales_frame = ttk.Frame(self.notebook)
        self.notebook.add(sales_frame, text="Sales")
        
        # Customer, Invoice No and Date
        customer_frame = tk.Frame(sales_frame)
        customer_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Label(customer_frame, text="Invoice No:", font=("Arial", 12, "bold")).pack(side="left")
        self.sales_invoice_entry = tk.Entry(customer_frame, width=15, font=("Arial", 12))
        self.sales_invoice_entry.pack(side="left", padx=10)
        self.sales_invoice_entry.insert(0, self.generate_sales_invoice_no())
        
        tk.Label(customer_frame, text="Customer:", font=("Arial", 12, "bold")).pack(side="left", padx=(20,5))
        self.customer_entry = tk.Entry(customer_frame, width=20, font=("Arial", 12))
        self.customer_entry.pack(side="left", padx=10)
        
        tk.Label(customer_frame, text="Date:", font=("Arial", 12, "bold")).pack(side="left", padx=(20,5))
        self.sales_date_entry = tk.Entry(customer_frame, width=12, font=("Arial", 12))
        self.sales_date_entry.pack(side="left", padx=5)
        self.sales_date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        
        # Item entry
        item_frame = tk.LabelFrame(sales_frame, text="Add Sale Items", font=("Arial", 12, "bold"))
        item_frame.pack(fill="x", padx=20, pady=10)
        
        fields_frame = tk.Frame(item_frame)
        fields_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Label(fields_frame, text="Item:").grid(row=0, column=0, padx=5, pady=5)
        self.item_entry = tk.Entry(fields_frame, width=20)
        self.item_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(fields_frame, text="Qty:").grid(row=0, column=2, padx=5, pady=5)
        self.qty_entry = tk.Entry(fields_frame, width=10)
        self.qty_entry.grid(row=0, column=3, padx=5, pady=5)
        
        tk.Label(fields_frame, text="Price:").grid(row=0, column=4, padx=5, pady=5)
        self.price_entry = tk.Entry(fields_frame, width=10)
        self.price_entry.grid(row=0, column=5, padx=5, pady=5)
        
        tk.Button(fields_frame, text="Add Item", command=self.add_item, 
                 bg="#4CAF50", fg="white").grid(row=0, column=6, padx=10, pady=5)
        
        # Items list
        list_frame = tk.LabelFrame(sales_frame, text="Sale Items", font=("Arial", 12, "bold"))
        list_frame.pack(fill="both", expand=True, padx=20, pady=5)
        
        self.tree = ttk.Treeview(list_frame, columns=("Item", "Qty", "Price", "Total"), 
                                show="headings", height=8)
        for col in ["Item", "Qty", "Price", "Total"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor="center")
        
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        scrollbar.pack(side="right", fill="y")
        
        # Total
        self.total_label = tk.Label(sales_frame, text="Total: KSH 0.00", 
                                   font=("Arial", 14, "bold"), fg="#2E86AB", bg="#f8f9fa", 
                                   relief="ridge", bd=2, padx=20, pady=10)
        self.total_label.pack(pady=5)
        

        
        # Buttons - role-based access
        btn_frame = tk.Frame(sales_frame)
        btn_frame.pack(pady=10)
        
        if self.user_role == "admin":
            tk.Button(btn_frame, text="Save Sale", command=self.save_sale, 
                     bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), 
                     width=12, height=2).pack(side="left", padx=5)
            
            tk.Button(btn_frame, text="Clear All", command=self.clear_sale, 
                     bg="#FFC107", fg="black", font=("Arial", 12, "bold"), 
                     width=12, height=2).pack(side="left", padx=5)
            
            tk.Button(btn_frame, text="Remove Selected", command=self.remove_selected_sale, 
                     bg="#f44336", fg="white", font=("Arial", 12, "bold"), 
                     width=12, height=2).pack(side="left", padx=5)
        
        # Print and View buttons available for both roles
        tk.Button(btn_frame, text="Print Receipt", command=self.print_sales_receipt, 
                 bg="#9C27B0", fg="white", font=("Arial", 12, "bold"), 
                 width=12, height=2).pack(side="left", padx=5)
        
        tk.Button(btn_frame, text="View Sales", command=self.open_sales_window,
                 bg="#2196F3", fg="white", font=("Arial", 12, "bold"),
                 width=12, height=2).pack(side="left", padx=5)
    
    def create_supplier_payments_tab(self):
        supplier_frame = ttk.Frame(self.notebook)
        self.notebook.add(supplier_frame, text="Supplier Payments")
        
        # Supplier selection
        selection_frame = tk.LabelFrame(supplier_frame, text="Select Supplier", font=("Arial", 12, "bold"))
        selection_frame.pack(fill="x", padx=20, pady=10)
        
        supplier_select_frame = tk.Frame(selection_frame)
        supplier_select_frame.pack(padx=10, pady=10)
        
        tk.Label(supplier_select_frame, text="Supplier:", font=("Arial", 10, "bold")).pack(side="left")
        self.supplier_var = tk.StringVar()
        self.supplier_combo = ttk.Combobox(supplier_select_frame, textvariable=self.supplier_var, width=25)
        self.supplier_combo.pack(side="left", padx=10)
        
        tk.Button(supplier_select_frame, text="Load Statement", command=self.load_supplier_statement,
                 bg="#2196F3", fg="white", font=("Arial", 10, "bold")).pack(side="left", padx=10)
        
        # Purchase statement - more compact
        statement_frame = tk.LabelFrame(supplier_frame, text="Purchase Statement", font=("Arial", 10, "bold"))
        statement_frame.pack(fill="x", padx=15, pady=5)
        
        self.supplier_tree = ttk.Treeview(statement_frame, columns=("Date", "Item", "Qty", "Amount"),
                                         show="headings", height=4)
        for col in ["Date", "Item", "Qty", "Amount"]:
            self.supplier_tree.heading(col, text=col)
            self.supplier_tree.column(col, width=150, anchor="center")
        
        supplier_scrollbar = ttk.Scrollbar(statement_frame, orient="vertical", command=self.supplier_tree.yview)
        self.supplier_tree.configure(yscrollcommand=supplier_scrollbar.set)
        
        self.supplier_tree.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        supplier_scrollbar.pack(side="right", fill="y")
        
        # Combined Balance & Payment section - compact layout
        bottom_frame = tk.Frame(supplier_frame)
        bottom_frame.pack(fill="x", padx=15, pady=5)
        
        # Balance summary - left side
        summary_frame = tk.LabelFrame(bottom_frame, text="Balance Summary", font=("Arial", 10, "bold"))
        summary_frame.pack(side="left", fill="both", expand=True, padx=(0,5))
        
        balance_grid = tk.Frame(summary_frame)
        balance_grid.pack(padx=8, pady=5)
        
        tk.Label(balance_grid, text="Purchases:", font=("Arial", 9, "bold")).grid(row=0, column=0, sticky="w", padx=3, pady=1)
        self.supplier_total_label = tk.Label(balance_grid, text="KSH 0.00", font=("Arial", 10, "bold"), fg="#2E86AB")
        self.supplier_total_label.grid(row=0, column=1, sticky="w", padx=5, pady=1)
        
        tk.Label(balance_grid, text="Payments:", font=("Arial", 9, "bold")).grid(row=1, column=0, sticky="w", padx=3, pady=1)
        self.supplier_payments_label = tk.Label(balance_grid, text="KSH 0.00", font=("Arial", 10, "bold"), fg="#4CAF50")
        self.supplier_payments_label.grid(row=1, column=1, sticky="w", padx=5, pady=1)
        
        tk.Label(balance_grid, text="BALANCE:", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky="w", padx=3, pady=3)
        self.supplier_balance_label = tk.Label(balance_grid, text="KSH 0.00", font=("Arial", 12, "bold"), fg="#f44336",
                                              relief="solid", bd=1, padx=5, pady=2, bg="#fff")
        self.supplier_balance_label.grid(row=2, column=1, sticky="w", padx=5, pady=3)
        
        tk.Button(balance_grid, text="Remove Selected", command=self.remove_selected_payment,
                 bg="#f44336", fg="white", font=("Arial", 8, "bold"),
                 width=15).grid(row=3, column=0, columnspan=2, pady=2)
        
        tk.Button(balance_grid, text="Export History", command=self.export_payment_history,
                 bg="#2196F3", fg="white", font=("Arial", 8, "bold"),
                 width=15).grid(row=4, column=0, columnspan=2, pady=2)
        
        # Payment section - role-based access
        if self.user_role == "admin":
            payment_section = tk.LabelFrame(bottom_frame, text="💳 MAKE PAYMENT", font=("Arial", 10, "bold"), fg="#4CAF50")
            payment_section.pack(side="right", fill="both", expand=True, padx=(5,0))
            
            payment_fields = tk.Frame(payment_section)
            payment_fields.pack(padx=8, pady=5)
            
            tk.Label(payment_fields, text="Amount:", font=("Arial", 9, "bold")).grid(row=0, column=0, padx=3, pady=3, sticky="w")
            self.supplier_payment_entry = tk.Entry(payment_fields, width=12, font=("Arial", 9))
            self.supplier_payment_entry.grid(row=0, column=1, padx=3, pady=3)
            
            tk.Label(payment_fields, text="Method:", font=("Arial", 9, "bold")).grid(row=1, column=0, padx=3, pady=3, sticky="w")
            self.supplier_payment_method = tk.StringVar(value="CASH")
            method_combo = ttk.Combobox(payment_fields, textvariable=self.supplier_payment_method,
                                       values=["CASH", "MPESA", "BANK"], width=10, state="readonly", font=("Arial", 9))
            method_combo.grid(row=1, column=1, padx=3, pady=3)
            
            tk.Label(payment_fields, text="Reference:", font=("Arial", 9, "bold")).grid(row=2, column=0, padx=3, pady=3, sticky="w")
            self.supplier_ref_entry = tk.Entry(payment_fields, width=15, font=("Arial", 9))
            self.supplier_ref_entry.grid(row=2, column=1, padx=3, pady=3)
            
            tk.Label(payment_fields, text="Date:", font=("Arial", 9, "bold")).grid(row=3, column=0, padx=3, pady=3, sticky="w")
            self.supplier_payment_date = tk.Entry(payment_fields, width=15, font=("Arial", 9))
            self.supplier_payment_date.grid(row=3, column=1, padx=3, pady=3)
            self.supplier_payment_date.insert(0, datetime.now().strftime('%Y-%m-%d %H:%M'))
            
            tk.Button(payment_fields, text="💰 MAKE PAYMENT", command=self.make_supplier_payment,
                     bg="#4CAF50", fg="white", font=("Arial", 9, "bold"),
                     width=18).grid(row=4, column=0, columnspan=2, padx=3, pady=5)
            
            tk.Button(payment_fields, text="Export Statement", command=self.export_supplier_statement,
                     bg="#2196F3", fg="white", font=("Arial", 8, "bold"),
                     width=18).grid(row=5, column=0, columnspan=2, padx=3, pady=3)
        else:
            # Cashier - Export only section
            export_section = tk.LabelFrame(bottom_frame, text="📝 EXPORT STATEMENT", font=("Arial", 10, "bold"), fg="#2196F3")
            export_section.pack(side="right", fill="both", expand=True, padx=(5,0))
            
            export_fields = tk.Frame(export_section)
            export_fields.pack(padx=8, pady=20)
            
            tk.Button(export_fields, text="Export Statement", command=self.export_supplier_statement,
                     bg="#2196F3", fg="white", font=("Arial", 10, "bold"),
                     width=20, height=2).pack(pady=10)
        
        self.refresh_suppliers()
    
    def create_sales_graph(self, parent):
        try:
            import matplotlib.pyplot as plt
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
            from matplotlib.figure import Figure
            from collections import defaultdict
            
            # Create figure
            self.fig = Figure(figsize=(10, 4), dpi=80)
            self.ax = self.fig.add_subplot(111)
            
            # Create canvas
            self.canvas = FigureCanvasTkAgg(self.fig, parent)
            self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
            
            self.update_sales_graph()
            
        except ImportError:
            tk.Label(parent, text="📈 Sales Trend Graph\n(Install matplotlib: pip install matplotlib)", 
                    font=("Arial", 12), fg="#666").pack(expand=True)
    
    def update_sales_graph(self):
        try:
            from datetime import datetime, timedelta
            
            sales = self.load_sales()
            purchases = self.load_purchases()
            
            if not sales:
                self.ax.clear()
                self.ax.text(0.5, 0.5, 'No data available', 
                           horizontalalignment='center', verticalalignment='center', 
                           transform=self.ax.transAxes, fontsize=12)
                self.canvas.draw()
                return
            
            # Get last 8 weeks of data
            end_date = datetime.now()
            weekly_sales = defaultdict(float)
            weekly_purchases = defaultdict(float)
            
            for i in range(8):
                week_start = end_date - timedelta(weeks=i+1)
                week_end = end_date - timedelta(weeks=i)
                week_key = f"W{i+1}"
                
                # Calculate weekly sales
                for sale in sales:
                    if sale.get('sale_date'):
                        try:
                            sale_date = datetime.fromisoformat(sale['sale_date'].replace('Z', '+00:00'))
                            if week_start <= sale_date <= week_end:
                                weekly_sales[week_key] += sale.get('total_amount', 0)
                        except:
                            pass
                
                # Calculate weekly purchases
                for purchase in purchases:
                    if purchase.get('purchase_date'):
                        try:
                            purchase_date = datetime.fromisoformat(purchase['purchase_date'].replace('Z', '+00:00'))
                            if week_start <= purchase_date <= week_end:
                                weekly_purchases[week_key] += purchase.get('total', 0)
                        except:
                            pass
            
            # Prepare data
            weeks = [f"W{i+1}" for i in range(8)][::-1]  # Reverse to show oldest first
            sales_values = [weekly_sales[week] / 1000 for week in weeks]  # Convert to thousands
            purchase_values = [weekly_purchases[week] / 1000 for week in weeks]
            profit_values = [s - p for s, p in zip(sales_values, purchase_values)]
            
            # Clear and create dual axis plot
            self.ax.clear()
            ax2 = self.ax.twinx()
            
            x_pos = range(len(weeks))
            bar_width = 0.35
            
            # Bar charts for sales and purchases
            sales_bars = self.ax.bar([x - bar_width/2 for x in x_pos], sales_values, 
                                   bar_width, color='#4CAF50', alpha=0.8, label='Sales')
            purchase_bars = self.ax.bar([x + bar_width/2 for x in x_pos], purchase_values, 
                                      bar_width, color='#FF9800', alpha=0.8, label='Purchases')
            
            # Line chart for profit
            line = ax2.plot(x_pos, profit_values, color='#FF5722', linewidth=3, marker='o', 
                           markersize=6, label='Profit')
            
            # Formatting
            self.ax.set_title('Weekly Sales & Purchases (Bars) + Profit (Line)', fontsize=14, fontweight='bold')
            self.ax.set_xlabel('Weeks', fontsize=10)
            self.ax.set_ylabel('Sales & Purchases (Thousands KSH)', fontsize=10)
            ax2.set_ylabel('Profit (Thousands KSH)', fontsize=10, color='#FF5722')
            
            self.ax.set_xticks(x_pos)
            self.ax.set_xticklabels(weeks)
            self.ax.grid(True, alpha=0.3, axis='y')
            
            # Add legend
            lines1, labels1 = self.ax.get_legend_handles_labels()
            lines2, labels2 = ax2.get_legend_handles_labels()
            self.ax.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=8)
            
            # Color the profit axis
            ax2.tick_params(axis='y', labelcolor='#FF5722')
            
            self.fig.tight_layout()
            self.canvas.draw()
            
        except Exception as e:
            pass
    
    def update_dashboard(self):
        try:
            sales = self.load_sales()
            purchases = self.load_purchases()
            
            total_sales = sum(s.get('total_amount', s.get('total', 0)) for s in sales)
            total_purchases = sum(p.get('total', 0) for p in purchases)
            profit = total_sales - total_purchases
            
            self.sales_amount_label.config(text=f"KSH {total_sales:,.2f}")
            self.purchases_amount_label.config(text=f"KSH {total_purchases:,.2f}")
            self.profit_amount_label.config(text=f"KSH {profit:,.2f}")
            
            # Update graph if it exists
            if hasattr(self, 'canvas'):
                self.update_sales_graph()
        except:
            pass
    
    def load_purchases(self):
        try:
            if os.path.exists("purchases.json"):
                with open("purchases.json", 'r') as f:
                    return json.load(f)
        except:
            pass
        return []
    
    def load_sales(self):
        try:
            if os.path.exists("sales.json"):
                with open("sales.json", 'r') as f:
                    return json.load(f)
        except:
            pass
        return []
    
    def add_item(self):
        item = self.item_entry.get()
        qty = self.qty_entry.get()
        price = self.price_entry.get()
        
        if item and qty and price:
            try:
                qty_val = float(qty)
                price_val = float(price)
                total = qty_val * price_val
                
                self.sales_items.append({"item": item, "quantity": qty_val, "price": price_val, "total": total})
                self.tree.insert("", "end", values=(item, qty_val, f"KSH {price_val:.2f}", f"KSH {total:.2f}"))
                
                self.sales_total += total
                self.total_label.config(text=f"Total: KSH {self.sales_total:.2f}")
                
                self.item_entry.delete(0, tk.END)
                self.qty_entry.delete(0, tk.END)
                self.price_entry.delete(0, tk.END)
            except:
                messagebox.showerror("Error", "Invalid input")
    
    def save_sale(self):
        customer = self.customer_entry.get().strip()
        sale_date = self.sales_date_entry.get().strip()
        if customer and self.sales_items:
            try:
                # Use custom date or current datetime
                if sale_date:
                    sale_datetime = f"{sale_date}T{datetime.now().strftime('%H:%M:%S')}"
                else:
                    sale_datetime = datetime.now().isoformat()
                
                sales = self.load_sales()
                
                invoice_no = self.sales_invoice_entry.get().strip() or self.generate_sales_invoice_no()
                
                new_sale = {
                    "id": len(sales) + 1,
                    "invoice_no": invoice_no,
                    "customer_name": customer,
                    "items": self.sales_items.copy(),
                    "total_amount": self.sales_total,
                    "sale_date": sale_datetime
                }
                
                sales.append(new_sale)
                with open("sales.json", 'w') as f:
                    json.dump(sales, f, indent=2)
                
                messagebox.showinfo("Success", f"Sale saved!\nCustomer: {customer}\nTotal: KSH {self.sales_total:.2f}")
                self.clear_sale()
                self.update_dashboard()  # Refresh dashboard
            except Exception as e:
                messagebox.showerror("Error", f"Could not save: {e}")
        else:
            messagebox.showerror("Error", "Customer and items required")
    
    def clear_sale(self):
        self.sales_items = []
        self.sales_total = 0.0
        self.customer_entry.delete(0, tk.END)
        self.sales_date_entry.delete(0, tk.END)
        self.sales_date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        self.sales_invoice_entry.delete(0, tk.END)
        self.sales_invoice_entry.insert(0, self.generate_sales_invoice_no())
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.total_label.config(text="Total: KSH 0.00")
    
    # Order functions
    def add_order_item(self):
        item = self.order_item_entry.get().strip()
        qty = self.order_qty_entry.get().strip()
        price = self.order_price_entry.get().strip()
        
        if not all([item, qty, price]):
            messagebox.showerror("Error", "All fields are required")
            return
        
        try:
            qty_val = float(qty)
            price_val = float(price)
            if qty_val <= 0 or price_val <= 0:
                raise ValueError("Values must be positive")
            
            total = qty_val * price_val
            
            self.order_items.append({
                "item": item,
                "quantity": qty_val,
                "price": price_val,
                "total": total
            })
            
            self.order_tree.insert("", "end", values=(item, qty_val, f"KSH {price_val:.2f}", f"KSH {total:.2f}"))
            
            self.order_total += total
            self.order_total_label.config(text=f"Total: KSH {self.order_total:.2f}")
            
            # Clear fields
            self.order_item_entry.delete(0, tk.END)
            self.order_qty_entry.delete(0, tk.END)
            self.order_price_entry.delete(0, tk.END)
            
        except ValueError:
            messagebox.showerror("Error", "Invalid quantity or price")
    
    def save_order(self):
        customer = self.order_customer_entry.get().strip()
        if not customer or not self.order_items:
            messagebox.showerror("Error", "Customer name and items required")
            return
        
        try:
            orders = self.load_orders()
            
            new_order = {
                "id": len(orders) + 1,
                "customer_name": customer,
                "items": self.order_items.copy(),
                "total_amount": self.order_total,
                "order_date": datetime.now().isoformat(),
                "status": "Pending"
            }
            
            orders.append(new_order)
            with open("orders.json", 'w') as f:
                json.dump(orders, f, indent=2)
            
            messagebox.showinfo("Success", f"Order saved!\nCustomer: {customer}\nTotal: KSH {self.order_total:.2f}")
            self.clear_order()
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not save order: {e}")
    
    def clear_order(self):
        self.order_items = []
        self.order_total = 0.0
        self.order_customer_entry.delete(0, tk.END)
        self.order_item_entry.delete(0, tk.END)
        self.order_qty_entry.delete(0, tk.END)
        self.order_price_entry.delete(0, tk.END)
        for item in self.order_tree.get_children():
            self.order_tree.delete(item)
        self.order_total_label.config(text="Total: KSH 0.00")
    
    def load_orders(self):
        try:
            if os.path.exists("orders.json"):
                with open("orders.json", 'r') as f:
                    return json.load(f)
        except:
            pass
        return []
    
    # Purchase functions
    def add_purchase_item(self):
        supplier = self.supplier_entry.get().strip()
        item = self.purchase_item_entry.get().strip()
        qty = self.purchase_qty_entry.get().strip()
        price = self.purchase_price_entry.get().strip()
        
        if not all([supplier, item, qty, price]):
            messagebox.showerror("Error", "All fields are required")
            return
        
        try:
            qty_val = float(qty)
            price_val = float(price)
            if qty_val <= 0 or price_val <= 0:
                raise ValueError("Values must be positive")
            
            total = qty_val * price_val
            
            self.purchase_items.append({
                "supplier": supplier,
                "item": item,
                "quantity": qty_val,
                "price": price_val,
                "total": total
            })
            
            self.purchase_tree.insert("", "end", values=(supplier, item, qty_val, f"KSH {price_val:.2f}", f"KSH {total:.2f}"))
            
            self.purchase_total += total
            self.purchase_total_label.config(text=f"Total: KSH {self.purchase_total:.2f}")
            
            # Clear item fields except supplier
            self.purchase_item_entry.delete(0, tk.END)
            self.purchase_qty_entry.delete(0, tk.END)
            self.purchase_price_entry.delete(0, tk.END)
            
        except ValueError:
            messagebox.showerror("Error", "Invalid quantity or price")
    
    def save_purchase(self):
        if not self.purchase_items:
            messagebox.showerror("Error", "No items to save")
            return
        
        try:
            purchase_date = self.purchase_date_entry.get().strip()
            # Use custom date or current datetime
            if purchase_date:
                purchase_datetime = f"{purchase_date}T{datetime.now().strftime('%H:%M:%S')}"
            else:
                purchase_datetime = datetime.now().isoformat()
            
            purchases = self.load_purchases()
            
            invoice_no = self.purchase_invoice_entry.get().strip() or self.generate_purchase_invoice_no()
            
            for item in self.purchase_items:
                new_purchase = {
                    "id": len(purchases) + 1,
                    "invoice_no": invoice_no,
                    "supplier": item["supplier"],
                    "item": item["item"],
                    "quantity": item["quantity"],
                    "price": item["price"],
                    "total": item["total"],
                    "purchase_date": purchase_datetime
                }
                purchases.append(new_purchase)
            
            with open("purchases.json", 'w') as f:
                json.dump(purchases, f, indent=2)
            
            messagebox.showinfo("Success", f"Purchase saved!\nItems: {len(self.purchase_items)}\nTotal: KSH {self.purchase_total:.2f}")
            self.clear_purchase()
            self.update_dashboard()  # Refresh dashboard
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not save: {e}")
    
    def clear_purchase(self):
        self.purchase_items = []
        self.purchase_total = 0.0
        self.supplier_entry.delete(0, tk.END)
        self.purchase_item_entry.delete(0, tk.END)
        self.purchase_qty_entry.delete(0, tk.END)
        self.purchase_price_entry.delete(0, tk.END)
        self.purchase_date_entry.delete(0, tk.END)
        self.purchase_date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        self.purchase_invoice_entry.delete(0, tk.END)
        self.purchase_invoice_entry.insert(0, self.generate_purchase_invoice_no())
        for item in self.purchase_tree.get_children():
            self.purchase_tree.delete(item)
        self.purchase_total_label.config(text="Total: KSH 0.00")
    
    # Supplier payment functions
    def refresh_suppliers(self):
        purchases = self.load_purchases()
        suppliers = list(set(p['supplier'] for p in purchases if p.get('supplier')))
        if hasattr(self, 'supplier_combo'):
            self.supplier_combo['values'] = sorted(suppliers)
    
    def load_supplier_statement(self):
        supplier = self.supplier_var.get().strip()
        if not supplier:
            messagebox.showwarning("Warning", "Please select a supplier")
            return
        
        # Clear existing data
        for item in self.supplier_tree.get_children():
            self.supplier_tree.delete(item)
        
        purchases = self.load_purchases()
        supplier_purchases = [p for p in purchases if p.get('supplier', '').lower() == supplier.lower()]
        
        if not supplier_purchases:
            messagebox.showinfo("Info", f"No purchases found for {supplier}")
            return
        
        total_purchases = 0
        
        for purchase in supplier_purchases:
            try:
                date_str = purchase['purchase_date'][:10] if purchase.get('purchase_date') else 'N/A'
            except:
                date_str = 'N/A'
            
            self.supplier_tree.insert("", "end", values=(
                date_str,
                purchase.get('item', ''),
                purchase.get('quantity', 0),
                f"KSH {purchase.get('total', 0):.2f}"
            ))
            
            total_purchases += purchase.get('total', 0)
        
        # Calculate payments
        payments = []
        if os.path.exists("payments.json"):
            with open("payments.json", 'r') as f:
                payments = json.load(f)
        
        total_payments = sum(p.get('amount', 0) for p in payments
                           if p.get('supplier', '').lower() == supplier.lower())
        
        balance_due = total_purchases - total_payments
        
        # Update summary
        self.supplier_total_label.config(text=f"KSH {total_purchases:,.2f}")
        self.supplier_payments_label.config(text=f"KSH {total_payments:,.2f}")
        self.supplier_balance_label.config(text=f"KSH {balance_due:,.2f}")
        
        # Update balance color
        if balance_due > 0:
            self.supplier_balance_label.config(fg="#f44336", bg="#ffebee")  # Red for outstanding
        elif balance_due < 0:
            self.supplier_balance_label.config(fg="#FF9800", bg="#fff3e0")  # Orange for overpaid
        else:
            self.supplier_balance_label.config(fg="#4CAF50", bg="#e8f5e8")  # Green for settled
    
    def make_supplier_payment(self):
        supplier = self.supplier_var.get().strip()
        amount_str = self.supplier_payment_entry.get().strip()
        reference = self.supplier_ref_entry.get().strip()
        payment_date_str = self.supplier_payment_date.get().strip()
        
        if not all([supplier, amount_str]):
            messagebox.showerror("Error", "Supplier and amount are required")
            return
        
        try:
            amount = float(amount_str)
            if amount <= 0:
                raise ValueError("Amount must be positive")
            
            # Parse custom date or use current datetime
            if payment_date_str:
                try:
                    # Try to parse the date string
                    if len(payment_date_str) == 16:  # YYYY-MM-DD HH:MM format
                        payment_datetime = datetime.strptime(payment_date_str, '%Y-%m-%d %H:%M').isoformat()
                    elif len(payment_date_str) == 10:  # YYYY-MM-DD format
                        payment_datetime = f"{payment_date_str}T{datetime.now().strftime('%H:%M:%S')}"
                    else:
                        payment_datetime = datetime.now().isoformat()
                except:
                    payment_datetime = datetime.now().isoformat()
            else:
                payment_datetime = datetime.now().isoformat()
            
            # Save payment record
            payments = []
            if os.path.exists("payments.json"):
                with open("payments.json", 'r') as f:
                    payments = json.load(f)
            
            new_payment = {
                "id": len(payments) + 1,
                "supplier": supplier,
                "amount": amount,
                "method": self.supplier_payment_method.get(),
                "reference": reference,
                "payment_date": payment_datetime,
                "type": "supplier_payment"
            }
            
            payments.append(new_payment)
            with open("payments.json", 'w') as f:
                json.dump(payments, f, indent=2)
            
            messagebox.showinfo("Success", f"Payment of KSH {amount:.2f} recorded for {supplier}")
            
            # Clear form and refresh
            self.supplier_payment_entry.delete(0, tk.END)
            self.supplier_ref_entry.delete(0, tk.END)
            self.supplier_payment_date.delete(0, tk.END)
            self.supplier_payment_date.insert(0, datetime.now().strftime('%Y-%m-%d %H:%M'))
            self.supplier_payment_method.set("CASH")
            self.load_supplier_statement()  # Refresh the statement
            
        except ValueError:
            messagebox.showerror("Error", "Invalid amount")
        except Exception as e:
            messagebox.showerror("Error", f"Could not process payment: {e}")
    
    def remove_selected_sale(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an item to remove")
            return
        
        for item in selected:
            values = self.tree.item(item, 'values')
            if values:
                # Find and remove from sales_items
                item_name = values[0]
                qty = float(values[1])
                for i, sale_item in enumerate(self.sales_items):
                    if (sale_item['item'] == item_name and 
                        sale_item['quantity'] == qty):
                        self.sales_total -= sale_item['total']
                        self.sales_items.pop(i)
                        break
                
                self.tree.delete(item)
        
        self.total_label.config(text=f"Total: KSH {self.sales_total:.2f}")
    
    def remove_selected_purchase(self):
        selected = self.purchase_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an item to remove")
            return
        
        for item in selected:
            values = self.purchase_tree.item(item, 'values')
            if values:
                # Find and remove from purchase_items
                supplier = values[0]
                item_name = values[1]
                qty = float(values[2])
                for i, purchase_item in enumerate(self.purchase_items):
                    if (purchase_item['supplier'] == supplier and 
                        purchase_item['item'] == item_name and 
                        purchase_item['quantity'] == qty):
                        self.purchase_total -= purchase_item['total']
                        self.purchase_items.pop(i)
                        break
                
                self.purchase_tree.delete(item)
        
        self.purchase_total_label.config(text=f"Total: KSH {self.purchase_total:.2f}")
    
    def export_sales_pdf(self):
        if not self.sales_items:
            messagebox.showwarning("Warning", "No sales items to export")
            return
        
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
            from reportlab.lib.styles import getSampleStyleSheet
            from reportlab.lib import colors
            
            filename = f"sales_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            doc = SimpleDocTemplate(filename, pagesize=letter)
            
            styles = getSampleStyleSheet()
            story = []
            
            # Title
            title = Paragraph("CESS FOODS - SALES EXPORT", styles['Title'])
            story.append(title)
            story.append(Spacer(1, 20))
            
            # Customer info
            customer = self.customer_entry.get().strip() or "N/A"
            customer_info = Paragraph(f"Customer: {customer}", styles['Normal'])
            story.append(customer_info)
            story.append(Spacer(1, 10))
            
            # Table data
            data = [['Item', 'Quantity', 'Price', 'Total']]
            for item in self.sales_items:
                data.append([
                    item['item'],
                    str(item['quantity']),
                    f"KSH {item['price']:.2f}",
                    f"KSH {item['total']:.2f}"
                ])
            
            # Add total row
            data.append(['', '', 'TOTAL:', f"KSH {self.sales_total:.2f}"])
            
            # Create table
            table = Table(data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -2), colors.beige),
                ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
                ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(table)
            doc.build(story)
            
            messagebox.showinfo("Success", f"Sales exported to {filename}")
            
        except ImportError:
            messagebox.showerror("Error", "ReportLab library not installed. Install with: pip install reportlab")
        except Exception as e:
            messagebox.showerror("Error", f"Export failed: {e}")
    
    def export_purchases_pdf(self):
        if not self.purchase_items:
            messagebox.showwarning("Warning", "No purchase items to export")
            return
        
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
            from reportlab.lib.styles import getSampleStyleSheet
            from reportlab.lib import colors
            
            filename = f"purchases_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            doc = SimpleDocTemplate(filename, pagesize=letter)
            
            styles = getSampleStyleSheet()
            story = []
            
            # Title
            title = Paragraph("CESS FOODS - PURCHASES EXPORT", styles['Title'])
            story.append(title)
            story.append(Spacer(1, 20))
            
            # Table data
            data = [['Supplier', 'Item', 'Quantity', 'Price', 'Total']]
            for item in self.purchase_items:
                data.append([
                    item['supplier'],
                    item['item'],
                    str(item['quantity']),
                    f"KSH {item['price']:.2f}",
                    f"KSH {item['total']:.2f}"
                ])
            
            # Add total row
            data.append(['', '', '', 'TOTAL:', f"KSH {self.purchase_total:.2f}"])
            
            # Create table
            table = Table(data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -2), colors.beige),
                ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
                ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(table)
            doc.build(story)
            
            messagebox.showinfo("Success", f"Purchases exported to {filename}")
            
        except ImportError:
            messagebox.showerror("Error", "ReportLab library not installed. Install with: pip install reportlab")
        except Exception as e:
            messagebox.showerror("Error", f"Export failed: {e}")
    
    def export_supplier_statement(self):
        supplier = self.supplier_var.get().strip()
        if not supplier:
            messagebox.showwarning("Warning", "Please select a supplier first")
            return
        
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
            from reportlab.lib.styles import getSampleStyleSheet
            from reportlab.lib import colors
            
            # Get supplier purchases and payments
            purchases = self.load_purchases()
            supplier_purchases = [p for p in purchases if p.get('supplier', '').lower() == supplier.lower()]
            
            payments = []
            if os.path.exists("payments.json"):
                with open("payments.json", 'r') as f:
                    payments = json.load(f)
            supplier_payments = [p for p in payments if p.get('supplier', '').lower() == supplier.lower()]
            
            if not supplier_purchases:
                messagebox.showinfo("Info", f"No purchases found for {supplier}")
                return
            
            filename = f"supplier_statement_{supplier}_{datetime.now().strftime('%Y%m%d')}.pdf"
            doc = SimpleDocTemplate(filename, pagesize=letter)
            
            styles = getSampleStyleSheet()
            story = []
            
            # Title
            title = Paragraph(f"CESS FOODS - SUPPLIER STATEMENT", styles['Title'])
            story.append(title)
            story.append(Spacer(1, 10))
            
            supplier_info = Paragraph(f"Supplier: {supplier}", styles['Heading2'])
            story.append(supplier_info)
            story.append(Spacer(1, 20))
            
            # Purchases table
            story.append(Paragraph("PURCHASES:", styles['Heading3']))
            purchase_data = [['Date', 'Item', 'Quantity', 'Amount']]
            total_purchases = 0
            
            for purchase in supplier_purchases:
                date_str = purchase.get('purchase_date', '')[:10] if purchase.get('purchase_date') else 'N/A'
                amount = purchase.get('total', 0)
                total_purchases += amount
                
                purchase_data.append([
                    date_str,
                    purchase.get('item', 'N/A'),
                    str(purchase.get('quantity', 0)),
                    f"KSH {amount:.2f}"
                ])
            
            purchase_data.append(['', '', 'TOTAL:', f"KSH {total_purchases:.2f}"])
            
            purchase_table = Table(purchase_data)
            purchase_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BACKGROUND', (0, 1), (-1, -2), colors.beige),
                ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
                ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(purchase_table)
            story.append(Spacer(1, 20))
            
            # Payments table
            story.append(Paragraph("PAYMENTS:", styles['Heading3']))
            payment_data = [['Date', 'Amount', 'Method', 'Reference']]
            total_payments = 0
            
            for payment in supplier_payments:
                date_str = payment.get('payment_date', '')[:10] if payment.get('payment_date') else 'N/A'
                amount = payment.get('amount', 0)
                total_payments += amount
                
                payment_data.append([
                    date_str,
                    f"KSH {amount:.2f}",
                    payment.get('method', 'N/A'),
                    payment.get('reference', 'N/A')
                ])
            
            if not supplier_payments:
                payment_data.append(['No payments recorded', '', '', ''])
            else:
                payment_data.append(['', f"KSH {total_payments:.2f}", 'TOTAL', ''])
            
            payment_table = Table(payment_data)
            payment_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BACKGROUND', (0, 1), (-1, -2), colors.lightblue),
                ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
                ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(payment_table)
            story.append(Spacer(1, 20))
            
            # Summary
            balance_due = total_purchases - total_payments
            status = "PAID" if balance_due <= 0 else "OUTSTANDING"
            
            summary_data = [
                ['Total Purchases:', f"KSH {total_purchases:.2f}"],
                ['Total Payments:', f"KSH {total_payments:.2f}"],
                ['BALANCE DUE:', f"KSH {balance_due:.2f}"],
                ['STATUS:', status]
            ]
            
            summary_table = Table(summary_data)
            summary_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 12),
                ('BACKGROUND', (0, -2), (-1, -1), colors.yellow if balance_due > 0 else colors.lightgreen),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(summary_table)
            doc.build(story)
            
            messagebox.showinfo("Success", f"Supplier statement exported to {filename}")
            
        except ImportError:
            messagebox.showerror("Error", "ReportLab library not installed")
        except Exception as e:
            messagebox.showerror("Error", f"Export failed: {e}")
    
    def export_weekly_sales(self):
        try:
            from datetime import datetime, timedelta
            from reportlab.lib.pagesizes import letter
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
            from reportlab.lib.styles import getSampleStyleSheet
            from reportlab.lib import colors
            
            # Get last 7 days of sales
            end_date = datetime.now()
            start_date = end_date - timedelta(days=7)
            
            sales = self.load_sales()
            weekly_sales = []
            for sale in sales:
                if sale.get('sale_date'):
                    sale_date = datetime.fromisoformat(sale['sale_date'].replace('Z', '+00:00'))
                    if start_date <= sale_date <= end_date:
                        weekly_sales.append(sale)
            
            if not weekly_sales:
                messagebox.showinfo("Info", "No sales found for the last 7 days")
                return
            
            filename = f"weekly_sales_{datetime.now().strftime('%Y%m%d')}.pdf"
            doc = SimpleDocTemplate(filename, pagesize=letter)
            
            styles = getSampleStyleSheet()
            story = []
            
            title = Paragraph("CESS FOODS - WEEKLY SALES REPORT", styles['Title'])
            story.append(title)
            story.append(Spacer(1, 15))
            
            period = Paragraph(f"Period: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}", styles['Normal'])
            story.append(period)
            story.append(Spacer(1, 10))
            
            data = [['Date', 'Customer', 'Items', 'Qty', 'Price/Kg', 'Item Total', 'Total']]
            total_amount = 0
            
            weekly_sales.sort(key=lambda x: x.get('sale_date', ''), reverse=True)
            for sale in weekly_sales:
                date_str = sale.get('sale_date', '')[:10]
                items_list = [item.get('item', '') for item in sale.get('items', [])]
                items_str = '\n'.join(items_list) if items_list else 'N/A'
                qty_list = [str(item.get('quantity', 0)) for item in sale.get('items', [])]
                qty_str = '\n'.join(qty_list) if qty_list else '0'
                price_list = [f"{item.get('price', 0):.0f}" for item in sale.get('items', [])]
                price_str = '\n'.join(price_list) if price_list else '0'
                item_total_list = [f"{item.get('total', 0):.0f}" for item in sale.get('items', [])]
                item_total_str = '\n'.join(item_total_list) if item_total_list else '0'
                amount = sale.get('total_amount', 0)
                total_amount += amount
                
                data.append([
                    date_str,
                    sale.get('customer_name', 'N/A'),
                    items_str,
                    qty_str,
                    price_str,
                    item_total_str,
                    f"KSH {amount:.2f}"
                ])
            
            data.append(['', '', '', '', '', 'TOTAL:', f"KSH {total_amount:.2f}"])
            
            table = Table(data, colWidths=[40, 70, 100, 30, 40, 50, 50])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 9),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                ('BACKGROUND', (0, 1), (-1, -2), colors.beige),
                ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
                ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(table)
            doc.build(story)
            
            messagebox.showinfo("Success", f"Weekly sales report exported to {filename}")
            
        except ImportError:
            messagebox.showerror("Error", "ReportLab library not installed")
        except Exception as e:
            messagebox.showerror("Error", f"Export failed: {e}")
    
    def export_monthly_sales(self):
        try:
            from datetime import datetime, timedelta
            from reportlab.lib.pagesizes import letter
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
            from reportlab.lib.styles import getSampleStyleSheet
            from reportlab.lib import colors
            
            # Get last 30 days of sales
            end_date = datetime.now()
            start_date = end_date - timedelta(days=30)
            
            sales = self.load_sales()
            monthly_sales = []
            for sale in sales:
                if sale.get('sale_date'):
                    sale_date = datetime.fromisoformat(sale['sale_date'].replace('Z', '+00:00'))
                    if start_date <= sale_date <= end_date:
                        monthly_sales.append(sale)
            
            if not monthly_sales:
                messagebox.showinfo("Info", "No sales found for the last 30 days")
                return
            
            filename = f"monthly_sales_{datetime.now().strftime('%Y%m%d')}.pdf"
            doc = SimpleDocTemplate(filename, pagesize=letter)
            
            styles = getSampleStyleSheet()
            story = []
            
            title = Paragraph("CESS FOODS - MONTHLY SALES REPORT", styles['Title'])
            story.append(title)
            story.append(Spacer(1, 20))
            
            period = Paragraph(f"Period: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}", styles['Normal'])
            story.append(period)
            story.append(Spacer(1, 10))
            
            data = [['Date', 'Customer', 'Items', 'Qty', 'Price/Kg', 'Item Total', 'Total']]
            total_amount = 0
            
            monthly_sales.sort(key=lambda x: x.get('sale_date', ''), reverse=True)
            for sale in monthly_sales:
                date_str = sale.get('sale_date', '')[:10]
                items_list = [item.get('item', '') for item in sale.get('items', [])]
                items_str = '\n'.join(items_list) if items_list else 'N/A'
                qty_list = [str(item.get('quantity', 0)) for item in sale.get('items', [])]
                qty_str = '\n'.join(qty_list) if qty_list else '0'
                price_list = [f"{item.get('price', 0):.0f}" for item in sale.get('items', [])]
                price_str = '\n'.join(price_list) if price_list else '0'
                item_total_list = [f"{item.get('total', 0):.0f}" for item in sale.get('items', [])]
                item_total_str = '\n'.join(item_total_list) if item_total_list else '0'
                amount = sale.get('total_amount', 0)
                total_amount += amount
                
                data.append([
                    date_str,
                    sale.get('customer_name', 'N/A'),
                    items_str,
                    qty_str,
                    price_str,
                    item_total_str,
                    f"KSH {amount:.2f}"
                ])
            
            data.append(['', '', '', '', '', 'TOTAL:', f"KSH {total_amount:.2f}"])
            
            table = Table(data, colWidths=[40, 70, 100, 30, 40, 50, 50])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 9),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                ('BACKGROUND', (0, 1), (-1, -2), colors.beige),
                ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
                ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(table)
            doc.build(story)
            
            messagebox.showinfo("Success", f"Monthly sales report exported to {filename}")
            
        except ImportError:
            messagebox.showerror("Error", "ReportLab library not installed")
        except Exception as e:
            messagebox.showerror("Error", f"Export failed: {e}")
    
    def export_weekly_purchases(self):
        try:
            from datetime import datetime, timedelta
            from reportlab.lib.pagesizes import letter
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
            from reportlab.lib.styles import getSampleStyleSheet
            from reportlab.lib import colors
            
            end_date = datetime.now()
            start_date = end_date - timedelta(days=7)
            
            purchases = self.load_purchases()
            weekly_purchases = []
            for purchase in purchases:
                if purchase.get('purchase_date'):
                    purchase_date = datetime.fromisoformat(purchase['purchase_date'].replace('Z', '+00:00'))
                    if start_date <= purchase_date <= end_date:
                        weekly_purchases.append(purchase)
            
            if not weekly_purchases:
                messagebox.showinfo("Info", "No purchases found for the last 7 days")
                return
            
            filename = f"weekly_purchases_{datetime.now().strftime('%Y%m%d')}.pdf"
            doc = SimpleDocTemplate(filename, pagesize=letter)
            
            styles = getSampleStyleSheet()
            story = []
            
            title = Paragraph("CESS FOODS - WEEKLY PURCHASES REPORT", styles['Title'])
            story.append(title)
            story.append(Spacer(1, 20))
            
            period = Paragraph(f"Period: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}", styles['Normal'])
            story.append(period)
            story.append(Spacer(1, 10))
            
            data = [['Date', 'Supplier', 'Item', 'Qty', 'Total']]
            total_amount = 0
            
            weekly_purchases.sort(key=lambda x: x.get('purchase_date', ''), reverse=True)
            for purchase in weekly_purchases:
                date_str = purchase.get('purchase_date', '')[:10]
                amount = purchase.get('total', 0)
                total_amount += amount
                
                data.append([
                    date_str,
                    purchase.get('supplier', 'N/A'),
                    purchase.get('item', 'N/A'),
                    str(purchase.get('quantity', 0)),
                    f"KSH {amount:.2f}"
                ])
            
            data.append(['', '', '', 'TOTAL:', f"KSH {total_amount:.2f}"])
            
            table = Table(data, colWidths=[70, 100, 80, 50, 70])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 9),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                ('BACKGROUND', (0, 1), (-1, -2), colors.beige),
                ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
                ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(table)
            doc.build(story)
            
            messagebox.showinfo("Success", f"Weekly purchases report exported to {filename}")
            
        except ImportError:
            messagebox.showerror("Error", "ReportLab library not installed")
        except Exception as e:
            messagebox.showerror("Error", f"Export failed: {e}")
    
    def export_monthly_purchases(self):
        try:
            from datetime import datetime, timedelta
            from reportlab.lib.pagesizes import letter
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
            from reportlab.lib.styles import getSampleStyleSheet
            from reportlab.lib import colors
            
            end_date = datetime.now()
            start_date = end_date - timedelta(days=30)
            
            purchases = self.load_purchases()
            monthly_purchases = []
            for purchase in purchases:
                if purchase.get('purchase_date'):
                    purchase_date = datetime.fromisoformat(purchase['purchase_date'].replace('Z', '+00:00'))
                    if start_date <= purchase_date <= end_date:
                        monthly_purchases.append(purchase)
            
            if not monthly_purchases:
                messagebox.showinfo("Info", "No purchases found for the last 30 days")
                return
            
            filename = f"monthly_purchases_{datetime.now().strftime('%Y%m%d')}.pdf"
            doc = SimpleDocTemplate(filename, pagesize=letter)
            
            styles = getSampleStyleSheet()
            story = []
            
            title = Paragraph("CESS FOODS - MONTHLY PURCHASES REPORT", styles['Title'])
            story.append(title)
            story.append(Spacer(1, 20))
            
            period = Paragraph(f"Period: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}", styles['Normal'])
            story.append(period)
            story.append(Spacer(1, 10))
            
            data = [['Date', 'Supplier', 'Item', 'Qty', 'Total']]
            total_amount = 0
            
            monthly_purchases.sort(key=lambda x: x.get('purchase_date', ''), reverse=True)
            for purchase in monthly_purchases:
                date_str = purchase.get('purchase_date', '')[:10]
                amount = purchase.get('total', 0)
                total_amount += amount
                
                data.append([
                    date_str,
                    purchase.get('supplier', 'N/A'),
                    purchase.get('item', 'N/A'),
                    str(purchase.get('quantity', 0)),
                    f"KSH {amount:.2f}"
                ])
            
            data.append(['', '', '', 'TOTAL:', f"KSH {total_amount:.2f}"])
            
            table = Table(data, colWidths=[70, 100, 80, 50, 70])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 9),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                ('BACKGROUND', (0, 1), (-1, -2), colors.beige),
                ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
                ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(table)
            doc.build(story)
            
            messagebox.showinfo("Success", f"Monthly purchases report exported to {filename}")
            
        except ImportError:
            messagebox.showerror("Error", "ReportLab library not installed")
        except Exception as e:
            messagebox.showerror("Error", f"Export failed: {e}")
    
    def remove_selected_order(self):
        selected = self.order_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an item to remove")
            return
        
        for item in selected:
            values = self.order_tree.item(item, 'values')
            if values:
                # Find and remove from order_items
                item_name = values[0]
                qty = float(values[1])
                for i, order_item in enumerate(self.order_items):
                    if (order_item['item'] == item_name and 
                        order_item['quantity'] == qty):
                        self.order_total -= order_item['total']
                        self.order_items.pop(i)
                        break
                
                self.order_tree.delete(item)
        
        self.order_total_label.config(text=f"Total: KSH {self.order_total:.2f}")
    
    def print_sales_receipt(self):
        if not self.sales_items:
            messagebox.showwarning("Warning", "No items to print")
            return
        
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
            from reportlab.lib.styles import getSampleStyleSheet
            from reportlab.lib import colors
            
            customer = self.customer_entry.get().strip() or "Walk-in Customer"
            sale_date = self.sales_date_entry.get().strip() or datetime.now().strftime('%Y-%m-%d')
            
            filename = f"sales_receipt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            doc = SimpleDocTemplate(filename, pagesize=letter)
            
            styles = getSampleStyleSheet()
            story = []
            
            title = Paragraph("CESS FOODS - SALES RECEIPT", styles['Title'])
            story.append(title)
            story.append(Spacer(1, 20))
            
            info = Paragraph(f"Customer: {customer}<br/>Date: {sale_date}", styles['Normal'])
            story.append(info)
            story.append(Spacer(1, 15))
            
            data = [['Item', 'Qty', 'Price', 'Total']]
            for item in self.sales_items:
                data.append([
                    item['item'],
                    str(item['quantity']),
                    f"KSH {item['price']:.2f}",
                    f"KSH {item['total']:.2f}"
                ])
            
            data.append(['', '', 'TOTAL:', f"KSH {self.sales_total:.2f}"])
            
            table = Table(data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -2), colors.beige),
                ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
                ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(table)
            doc.build(story)
            
            messagebox.showinfo("Success", f"Receipt printed to {filename}")
            
        except ImportError:
            messagebox.showerror("Error", "ReportLab library not installed")
        except Exception as e:
            messagebox.showerror("Error", f"Print failed: {e}")
    
    def print_purchase_receipt(self):
        if not self.purchase_items:
            messagebox.showwarning("Warning", "No items to print")
            return
        
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
            from reportlab.lib.styles import getSampleStyleSheet
            from reportlab.lib import colors
            
            purchase_date = self.purchase_date_entry.get().strip() or datetime.now().strftime('%Y-%m-%d')
            
            filename = f"purchase_receipt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            doc = SimpleDocTemplate(filename, pagesize=letter)
            
            styles = getSampleStyleSheet()
            story = []
            
            title = Paragraph("CESS FOODS - PURCHASE RECEIPT", styles['Title'])
            story.append(title)
            story.append(Spacer(1, 20))
            
            info = Paragraph(f"Purchase Date: {purchase_date}", styles['Normal'])
            story.append(info)
            story.append(Spacer(1, 15))
            
            data = [['Supplier', 'Item', 'Qty', 'Price', 'Total']]
            for item in self.purchase_items:
                data.append([
                    item['supplier'],
                    item['item'],
                    str(item['quantity']),
                    f"KSH {item['price']:.2f}",
                    f"KSH {item['total']:.2f}"
                ])
            
            data.append(['', '', '', 'TOTAL:', f"KSH {self.purchase_total:.2f}"])
            
            table = Table(data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -2), colors.beige),
                ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
                ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(table)
            doc.build(story)
            
            messagebox.showinfo("Success", f"Receipt printed to {filename}")
            
        except ImportError:
            messagebox.showerror("Error", "ReportLab library not installed")
        except Exception as e:
            messagebox.showerror("Error", f"Print failed: {e}")
    
    def remove_selected_payment(self):
        supplier = self.supplier_var.get().strip()
        if not supplier:
            messagebox.showwarning("Warning", "Please select a supplier first")
            return
        
        # Show payment history for selection
        try:
            payments = []
            if os.path.exists("payments.json"):
                with open("payments.json", 'r') as f:
                    payments = json.load(f)
            
            supplier_payments = [p for p in payments if p.get('supplier', '').lower() == supplier.lower()]
            
            if not supplier_payments:
                messagebox.showinfo("Info", f"No payments found for {supplier}")
                return
            
            # Create selection window
            selection_window = tk.Toplevel(self.root)
            selection_window.title(f"Remove Payment - {supplier}")
            selection_window.geometry("600x400")
            
            tk.Label(selection_window, text=f"Select payment to remove for {supplier}", 
                    font=("Arial", 12, "bold")).pack(pady=10)
            
            # Payment list
            payment_tree = ttk.Treeview(selection_window, columns=("Date", "Amount", "Method", "Reference"),
                                       show="headings", height=10)
            for col in ["Date", "Amount", "Method", "Reference"]:
                payment_tree.heading(col, text=col)
                payment_tree.column(col, width=120, anchor="center")
            
            payment_tree.pack(fill="both", expand=True, padx=20, pady=10)
            
            # Populate payment list
            for payment in supplier_payments:
                date_str = payment.get('payment_date', '')[:10] if payment.get('payment_date') else 'N/A'
                payment_tree.insert("", "end", values=(
                    date_str,
                    f"KSH {payment.get('amount', 0):.2f}",
                    payment.get('method', 'N/A'),
                    payment.get('reference', 'N/A')
                ), tags=(payment.get('id', ''),))
            
            def remove_payment():
                selected = payment_tree.selection()
                if not selected:
                    messagebox.showwarning("Warning", "Please select a payment to remove")
                    return
                
                # Confirm deletion
                if messagebox.askyesno("Confirm", "Are you sure you want to completely delete this payment?"):
                    try:
                        # Get payment ID from tags
                        item = selected[0]
                        payment_id = payment_tree.item(item, 'tags')[0]
                        
                        # Find and get payment amount for confirmation
                        payment_to_remove = None
                        for p in payments:
                            if str(p.get('id', '')) == str(payment_id):
                                payment_to_remove = p
                                break
                        
                        if payment_to_remove:
                            amount = payment_to_remove.get('amount', 0)
                            supplier_name = payment_to_remove.get('supplier', '')
                            
                            # Remove from payments list completely
                            updated_payments = [p for p in payments if str(p.get('id', '')) != str(payment_id)]
                            
                            # Also remove corresponding purchases for this supplier and amount
                            purchases = self.load_purchases()
                            # Remove purchases that match the supplier and total amount
                            updated_purchases = [p for p in purchases if not (
                                p.get('supplier', '').lower() == supplier_name.lower() and 
                                p.get('total', 0) == amount
                            )]
                            
                            # Save updated payments and purchases
                            with open("payments.json", 'w') as f:
                                json.dump(updated_payments, f, indent=2)
                            
                            with open("purchases.json", 'w') as f:
                                json.dump(updated_purchases, f, indent=2)
                            
                            messagebox.showinfo("Success", f"Payment and related purchases of KSH {amount:.2f} completely deleted")
                            selection_window.destroy()
                            self.load_supplier_statement()  # Refresh the statement
                            self.update_dashboard()  # Refresh dashboard
                        else:
                            messagebox.showerror("Error", "Payment not found")
                        
                    except Exception as e:
                        messagebox.showerror("Error", f"Could not remove payment: {e}")
            
            # Buttons
            btn_frame = tk.Frame(selection_window)
            btn_frame.pack(pady=10)
            
            tk.Button(btn_frame, text="Delete Payment", command=remove_payment,
                     bg="#f44336", fg="white", font=("Arial", 10, "bold")).pack(side="left", padx=5)
            
            tk.Button(btn_frame, text="Cancel", command=selection_window.destroy,
                     bg="#9E9E9E", fg="white", font=("Arial", 10, "bold")).pack(side="left", padx=5)
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not load payments: {e}")
    
    def export_payment_history(self):
        try:
            payments = []
            if os.path.exists("payments.json"):
                with open("payments.json", 'r') as f:
                    payments = json.load(f)
            
            if not payments:
                messagebox.showinfo("Info", "No payment history found")
                return
            
            from reportlab.lib.pagesizes import letter
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
            from reportlab.lib.styles import getSampleStyleSheet
            from reportlab.lib import colors
            
            filename = f"payment_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            doc = SimpleDocTemplate(filename, pagesize=letter)
            
            styles = getSampleStyleSheet()
            story = []
            
            title = Paragraph("CESS FOODS - PAYMENT HISTORY", styles['Title'])
            story.append(title)
            story.append(Spacer(1, 20))
            
            data = [['Date', 'Supplier', 'Amount', 'Method', 'Reference']]
            total_payments = 0
            
            for payment in payments:
                date_str = payment.get('payment_date', '')[:10] if payment.get('payment_date') else 'N/A'
                amount = payment.get('amount', 0)
                total_payments += amount
                
                data.append([
                    date_str,
                    payment.get('supplier', 'N/A'),
                    f"KSH {amount:.2f}",
                    payment.get('method', 'N/A'),
                    payment.get('reference', 'N/A')
                ])
            
            data.append(['', '', f"KSH {total_payments:.2f}", 'TOTAL', ''])
            
            table = Table(data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -2), colors.beige),
                ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
                ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(table)
            doc.build(story)
            
            messagebox.showinfo("Success", f"Payment history exported to {filename}")
            
        except ImportError:
            messagebox.showerror("Error", "ReportLab library not installed")
        except Exception as e:
            messagebox.showerror("Error", f"Export failed: {e}")
    
    def export_selected_report(self):
        selected = self.export_var.get()
        if selected == "Select Report":
            messagebox.showwarning("Warning", "Please select a report type")
            return
        
        if selected == "Weekly Sales":
            self.export_weekly_sales()
        elif selected == "Monthly Sales":
            self.export_monthly_sales()
        elif selected == "Weekly Purchases":
            self.export_weekly_purchases()
        elif selected == "Monthly Purchases":
            self.export_monthly_purchases()
        elif selected in ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]:
            self.export_month_by_name(selected)
    
    def refresh_sales_view(self):
        # Clear existing data
        for item in self.sales_history_tree.get_children():
            self.sales_history_tree.delete(item)
        
        # Load and display sales
        sales = self.load_sales()
        for sale in sales:
            date_str = sale.get('sale_date', '')[:10] if sale.get('sale_date') else 'N/A'
            items_count = len(sale.get('items', []))
            
            self.sales_history_tree.insert("", "end", values=(
                sale.get('id', 'N/A'),
                date_str,
                sale.get('customer_name', 'N/A'),
                f"{items_count} items",
                f"KSH {sale.get('total_amount', 0):.2f}"
            ))
    
    def open_sales_window(self):
        sales_window = tk.Toplevel(self.root)
        sales_window.title("View All Sales")
        sales_window.geometry("800x500")
        sales_window.configure(bg="white")
        
        tk.Label(sales_window, text="📊 ALL SALES RECORDS", 
                font=("Arial", 16, "bold"), fg="#2E86AB", bg="white").pack(pady=10)
        
        # Sales tree
        tree_frame = tk.Frame(sales_window, bg="white")
        tree_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        sales_tree = ttk.Treeview(tree_frame, columns=("Invoice", "Date", "Customer", "Items", "Total"),
                                 show="headings", height=15)
        for col in ["Invoice", "Date", "Customer", "Items", "Total"]:
            sales_tree.heading(col, text=col)
            sales_tree.column(col, width=150, anchor="center")
        
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=sales_tree.yview)
        sales_tree.configure(yscrollcommand=scrollbar.set)
        
        sales_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Load sales data sorted by date
        sales = self.load_sales()
        sales.sort(key=lambda x: x.get('sale_date', ''), reverse=True)
        for sale in sales:
            date_str = sale.get('sale_date', '')[:10] if sale.get('sale_date') else 'N/A'
            items_count = len(sale.get('items', []))
            
            invoice_no = f"SAL-{sale.get('id', 'N/A'):03d}"
            sales_tree.insert("", "end", values=(
                invoice_no,
                date_str,
                sale.get('customer_name', 'N/A'),
                f"{items_count} items",
                f"KSH {sale.get('total_amount', 0):.2f}"
            ))
        
        # Buttons
        btn_frame = tk.Frame(sales_window, bg="white")
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Refresh", command=lambda: self.refresh_sales_tree(sales_tree),
                 bg="#2196F3", fg="white", font=("Arial", 10, "bold"),
                 width=12, height=2).pack(side="left", padx=5)
        
        tk.Button(btn_frame, text="Edit Selected", 
                 command=lambda: self.edit_selected_sale(sales_tree),
                 bg="#FF9800", fg="white", font=("Arial", 10, "bold"),
                 width=12, height=2).pack(side="left", padx=5)
        
        if self.user_role == "admin":
            tk.Button(btn_frame, text="Delete Selected", 
                     command=lambda: self.delete_sale_from_tree(sales_tree),
                     bg="#f44336", fg="white", font=("Arial", 10, "bold"),
                     width=12, height=2).pack(side="left", padx=5)
    
    def refresh_sales_tree(self, tree):
        for item in tree.get_children():
            tree.delete(item)
        
        sales = self.load_sales()
        sales.sort(key=lambda x: x.get('sale_date', ''), reverse=True)
        for sale in sales:
            date_str = sale.get('sale_date', '')[:10] if sale.get('sale_date') else 'N/A'
            items_count = len(sale.get('items', []))
            invoice_no = f"SAL-{sale.get('id', 'N/A'):03d}"
            
            tree.insert("", "end", values=(
                invoice_no,
                date_str,
                sale.get('customer_name', 'N/A'),
                f"{items_count} items",
                f"KSH {sale.get('total_amount', 0):.2f}"
            ))
    
    def delete_sale_from_tree(self, tree):
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a sale to delete")
            return
        
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected sale(s)?"):
            sales = self.load_sales()
            
            for item in selected:
                values = tree.item(item, 'values')
                sale_id = values[0]
                sales = [s for s in sales if str(s.get('id', '')) != str(sale_id)]
            
            with open("sales.json", 'w') as f:
                json.dump(sales, f, indent=2)
            
            messagebox.showinfo("Success", "Selected sale(s) deleted successfully")
            self.refresh_sales_tree(tree)
            self.update_dashboard()
    
    def open_purchases_window(self):
        purchases_window = tk.Toplevel(self.root)
        purchases_window.title("View All Purchases")
        purchases_window.geometry("900x500")
        purchases_window.configure(bg="white")
        
        tk.Label(purchases_window, text="📦 ALL PURCHASE RECORDS", 
                font=("Arial", 16, "bold"), fg="#2E86AB", bg="white").pack(pady=10)
        
        # Purchases tree
        tree_frame = tk.Frame(purchases_window, bg="white")
        tree_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        purchases_tree = ttk.Treeview(tree_frame, columns=("Invoice", "Date", "Supplier", "Item", "Qty", "Total"),
                                     show="headings", height=15)
        for col in ["Invoice", "Date", "Supplier", "Item", "Qty", "Total"]:
            purchases_tree.heading(col, text=col)
            purchases_tree.column(col, width=140, anchor="center")
        
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=purchases_tree.yview)
        purchases_tree.configure(yscrollcommand=scrollbar.set)
        
        purchases_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Load purchases data sorted by date
        purchases = self.load_purchases()
        purchases.sort(key=lambda x: x.get('purchase_date', ''), reverse=True)
        for purchase in purchases:
            date_str = purchase.get('purchase_date', '')[:10] if purchase.get('purchase_date') else 'N/A'
            
            invoice_no = purchase.get('invoice_ref', f"INV-{purchase.get('id', 'N/A')}")
            purchases_tree.insert("", "end", values=(
                invoice_no,
                date_str,
                purchase.get('supplier', 'N/A'),
                purchase.get('item', 'N/A'),
                purchase.get('quantity', 0),
                f"KSH {purchase.get('total', 0):.2f}"
            ))
        
        # Buttons
        btn_frame = tk.Frame(purchases_window, bg="white")
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Refresh", command=lambda: self.refresh_purchases_tree(purchases_tree),
                 bg="#2196F3", fg="white", font=("Arial", 10, "bold"),
                 width=12, height=2).pack(side="left", padx=5)
        
        tk.Button(btn_frame, text="Edit Selected", 
                 command=lambda: self.edit_selected_purchase(purchases_tree),
                 bg="#FF9800", fg="white", font=("Arial", 10, "bold"),
                 width=12, height=2).pack(side="left", padx=5)
        
        if self.user_role == "admin":
            tk.Button(btn_frame, text="Delete Selected", 
                     command=lambda: self.delete_purchase_from_tree(purchases_tree),
                     bg="#f44336", fg="white", font=("Arial", 10, "bold"),
                     width=12, height=2).pack(side="left", padx=5)
    
    def refresh_purchases_tree(self, tree):
        for item in tree.get_children():
            tree.delete(item)
        
        purchases = self.load_purchases()
        purchases.sort(key=lambda x: x.get('purchase_date', ''), reverse=True)
        for purchase in purchases:
            date_str = purchase.get('purchase_date', '')[:10] if purchase.get('purchase_date') else 'N/A'
            invoice_no = purchase.get('invoice_ref', f"INV-{purchase.get('id', 'N/A')}")
            
            tree.insert("", "end", values=(
                invoice_no,
                date_str,
                purchase.get('supplier', 'N/A'),
                purchase.get('item', 'N/A'),
                purchase.get('quantity', 0),
                f"KSH {purchase.get('total', 0):.2f}"
            ))
    
    def delete_purchase_from_tree(self, tree):
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a purchase to delete")
            return
        
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected purchase(s)?"):
            purchases = self.load_purchases()
            
            for item in selected:
                values = tree.item(item, 'values')
                purchase_id = values[0]
                purchases = [p for p in purchases if str(p.get('id', '')) != str(purchase_id)]
            
            with open("purchases.json", 'w') as f:
                json.dump(purchases, f, indent=2)
            
            messagebox.showinfo("Success", "Selected purchase(s) deleted successfully")
            self.refresh_purchases_tree(tree)
            self.update_dashboard()
            self.refresh_suppliers()
    
    def export_specific_month(self):
        month_window = tk.Toplevel(self.root)
        month_window.title("Select Month")
        month_window.geometry("400x300")
        month_window.configure(bg="white")
        
        tk.Label(month_window, text="📅 SELECT MONTH TO EXPORT", 
                font=("Arial", 14, "bold"), fg="#2E86AB", bg="white").pack(pady=20)
        
        # Month selection
        month_frame = tk.Frame(month_window, bg="white")
        month_frame.pack(pady=20)
        
        tk.Label(month_frame, text="Month:", font=("Arial", 12, "bold"), bg="white").grid(row=0, column=0, padx=10, pady=5)
        month_var = tk.StringVar(value="01")
        month_combo = ttk.Combobox(month_frame, textvariable=month_var, width=15, state="readonly",
                                  values=["01-January", "02-February", "03-March", "04-April", "05-May", "06-June",
                                         "07-July", "08-August", "09-September", "10-October", "11-November", "12-December"])
        month_combo.grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(month_frame, text="Year:", font=("Arial", 12, "bold"), bg="white").grid(row=1, column=0, padx=10, pady=5)
        year_var = tk.StringVar(value=str(datetime.now().year))
        year_combo = ttk.Combobox(month_frame, textvariable=year_var, width=15, state="readonly",
                                 values=[str(y) for y in range(2020, datetime.now().year + 2)])
        year_combo.grid(row=1, column=1, padx=10, pady=5)
        
        # Report type selection
        type_frame = tk.Frame(month_window, bg="white")
        type_frame.pack(pady=20)
        
        tk.Label(type_frame, text="Report Type:", font=("Arial", 12, "bold"), bg="white").grid(row=0, column=0, padx=10, pady=5)
        type_var = tk.StringVar(value="Sales")
        type_combo = ttk.Combobox(type_frame, textvariable=type_var, width=15, state="readonly",
                                 values=["Sales", "Purchases"])
        type_combo.grid(row=0, column=1, padx=10, pady=5)
        
        # Export button
        def export_month():
            month = month_var.get()[:2]
            year = year_var.get()
            report_type = type_var.get()
            
            if report_type == "Sales":
                self.export_month_sales(month, year)
            else:
                self.export_month_purchases(month, year)
            
            month_window.destroy()
        
        tk.Button(month_window, text="Export Report", command=export_month,
                 bg="#4CAF50", fg="white", font=("Arial", 12, "bold"),
                 width=15, height=2).pack(pady=20)
    
    def export_month_sales(self, month, year):
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
            from reportlab.lib.styles import getSampleStyleSheet
            from reportlab.lib import colors
            
            sales = self.load_sales()
            month_sales = []
            for sale in sales:
                if sale.get('sale_date'):
                    sale_date = sale['sale_date'][:7]
                    if sale_date == f"{year}-{month}":
                        month_sales.append(sale)
            
            if not month_sales:
                messagebox.showinfo("Info", f"No sales found for {month}/{year}")
                return
            
            filename = f"sales_{month}_{year}.pdf"
            doc = SimpleDocTemplate(filename, pagesize=letter)
            
            styles = getSampleStyleSheet()
            story = []
            
            title = Paragraph(f"CESS FOODS - SALES REPORT ({month}/{year})", styles['Title'])
            story.append(title)
            story.append(Spacer(1, 15))
            
            data = [['Date', 'Customer', 'Items', 'Qty', 'Price/Kg', 'Item Total', 'Total']]
            total_amount = 0
            
            month_sales.sort(key=lambda x: x.get('sale_date', ''), reverse=True)
            for sale in month_sales:
                date_str = sale.get('sale_date', '')[:10]
                items_list = [item.get('item', '') for item in sale.get('items', [])]
                items_str = '\n'.join(items_list) if items_list else 'N/A'
                qty_list = [str(item.get('quantity', 0)) for item in sale.get('items', [])]
                qty_str = '\n'.join(qty_list) if qty_list else '0'
                price_list = [f"{item.get('price', 0):.0f}" for item in sale.get('items', [])]
                price_str = '\n'.join(price_list) if price_list else '0'
                item_total_list = [f"{item.get('total', 0):.0f}" for item in sale.get('items', [])]
                item_total_str = '\n'.join(item_total_list) if item_total_list else '0'
                amount = sale.get('total_amount', 0)
                total_amount += amount
                
                data.append([
                    date_str,
                    sale.get('customer_name', 'N/A'),
                    items_str,
                    qty_str,
                    price_str,
                    item_total_str,
                    f"KSH {amount:.2f}"
                ])
            
            data.append(['', '', '', '', '', 'TOTAL:', f"KSH {total_amount:.2f}"])
            
            table = Table(data, colWidths=[40, 70, 100, 30, 40, 50, 50])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 9),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                ('BACKGROUND', (0, 1), (-1, -2), colors.beige),
                ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
                ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(table)
            doc.build(story)
            
            messagebox.showinfo("Success", f"Sales report for {month}/{year} exported to {filename}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Export failed: {e}")
    
    def export_month_purchases(self, month, year):
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
            from reportlab.lib.styles import getSampleStyleSheet
            from reportlab.lib import colors
            
            purchases = self.load_purchases()
            month_purchases = []
            for purchase in purchases:
                if purchase.get('purchase_date'):
                    purchase_date = purchase['purchase_date'][:7]
                    if purchase_date == f"{year}-{month}":
                        month_purchases.append(purchase)
            
            if not month_purchases:
                messagebox.showinfo("Info", f"No purchases found for {month}/{year}")
                return
            
            filename = f"purchases_{month}_{year}.pdf"
            doc = SimpleDocTemplate(filename, pagesize=letter)
            
            styles = getSampleStyleSheet()
            story = []
            
            title = Paragraph(f"CESS FOODS - PURCHASES REPORT ({month}/{year})", styles['Title'])
            story.append(title)
            story.append(Spacer(1, 15))
            
            data = [['Date', 'Supplier', 'Item', 'Qty', 'Total']]
            total_amount = 0
            
            month_purchases.sort(key=lambda x: x.get('purchase_date', ''), reverse=True)
            for purchase in month_purchases:
                date_str = purchase.get('purchase_date', '')[:10]
                amount = purchase.get('total', 0)
                total_amount += amount
                
                data.append([
                    date_str,
                    purchase.get('supplier', 'N/A'),
                    purchase.get('item', 'N/A'),
                    str(purchase.get('quantity', 0)),
                    f"KSH {amount:.2f}"
                ])
            
            data.append(['', '', '', 'TOTAL:', f"KSH {total_amount:.2f}"])
            
            table = Table(data, colWidths=[70, 100, 80, 50, 70])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 9),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                ('BACKGROUND', (0, 1), (-1, -2), colors.beige),
                ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
                ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(table)
            doc.build(story)
            
            messagebox.showinfo("Success", f"Purchases report for {month}/{year} exported to {filename}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Export failed: {e}")
    
    def generate_sales_invoice_no(self):
        """Generate next sales invoice number"""
        sales = self.load_sales()
        next_id = len(sales) + 1
        return f"SAL-{next_id:04d}"
    
    def generate_purchase_invoice_no(self):
        """Generate next purchase invoice number"""
        purchases = self.load_purchases()
        next_id = len(purchases) + 1
        return f"PUR-{next_id:04d}"
    
    def edit_selected_sale(self, tree):
        """Edit selected sale invoice"""
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a sale to edit")
            return
        
        values = tree.item(selected[0], 'values')
        invoice_no = values[0]
        
        # Find the sale
        sales = self.load_sales()
        sale = None
        for s in sales:
            if s.get('invoice_no') == invoice_no or f"SAL-{s.get('id', 'N/A'):03d}" == invoice_no:
                sale = s
                break
        
        if not sale:
            messagebox.showerror("Error", "Sale not found")
            return
        
        self.open_sale_edit_window(sale, tree)
    
    def edit_selected_purchase(self, tree):
        """Edit selected purchase invoice"""
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a purchase to edit")
            return
        
        values = tree.item(selected[0], 'values')
        invoice_no = values[0]
        
        # Find the purchase
        purchases = self.load_purchases()
        purchase = None
        for p in purchases:
            if p.get('invoice_no') == invoice_no or p.get('invoice_ref') == invoice_no:
                purchase = p
                break
        
        if not purchase:
            messagebox.showerror("Error", "Purchase not found")
            return
        
        self.open_purchase_edit_window(purchase, tree)
    
    def open_sale_edit_window(self, sale, tree):
        """Open sale edit window"""
        edit_window = tk.Toplevel(self.root)
        edit_window.title(f"Edit Sale Invoice {sale.get('invoice_no', sale.get('id'))}")
        edit_window.geometry("600x500")
        
        # Customer and Date
        info_frame = tk.Frame(edit_window)
        info_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Label(info_frame, text="Customer:", font=("Arial", 12, "bold")).grid(row=0, column=0, sticky="w")
        customer_entry = tk.Entry(info_frame, width=25, font=("Arial", 12))
        customer_entry.grid(row=0, column=1, padx=10)
        customer_entry.insert(0, sale.get('customer_name', ''))
        
        tk.Label(info_frame, text="Date:", font=("Arial", 12, "bold")).grid(row=0, column=2, sticky="w")
        date_entry = tk.Entry(info_frame, width=15, font=("Arial", 12))
        date_entry.grid(row=0, column=3, padx=10)
        date_str = sale.get('sale_date', '')[:10] if sale.get('sale_date') else ''
        date_entry.insert(0, date_str)
        
        # Total display
        total_label = tk.Label(edit_window, text=f"Total: KSH {sale.get('total_amount', 0):.2f}", 
                              font=("Arial", 14, "bold"), fg="#2E86AB")
        total_label.pack(pady=10)
        
        # Save button
        def save_changes():
            customer = customer_entry.get().strip()
            date_str = date_entry.get().strip()
            
            if not customer:
                messagebox.showerror("Error", "Customer name is required")
                return
            
            # Update sale
            sales = self.load_sales()
            for i, s in enumerate(sales):
                if s.get('id') == sale.get('id'):
                    sales[i]['customer_name'] = customer
                    if date_str:
                        sales[i]['sale_date'] = f"{date_str}T{datetime.now().strftime('%H:%M:%S')}"
                    break
            
            with open("sales.json", 'w') as f:
                json.dump(sales, f, indent=2)
            
            messagebox.showinfo("Success", "Sale updated successfully!")
            edit_window.destroy()
            self.refresh_sales_tree(tree)
        
        tk.Button(edit_window, text="Save Changes", command=save_changes,
                 bg="#4CAF50", fg="white", font=("Arial", 12, "bold"),
                 width=15, height=2).pack(pady=20)
    
    def open_purchase_edit_window(self, purchase, tree):
        """Open purchase edit window"""
        edit_window = tk.Toplevel(self.root)
        edit_window.title(f"Edit Purchase Invoice {purchase.get('invoice_no', purchase.get('id'))}")
        edit_window.geometry("600x500")
        
        # Supplier and Date
        info_frame = tk.Frame(edit_window)
        info_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Label(info_frame, text="Supplier:", font=("Arial", 12, "bold")).grid(row=0, column=0, sticky="w")
        supplier_entry = tk.Entry(info_frame, width=20, font=("Arial", 12))
        supplier_entry.grid(row=0, column=1, padx=10)
        supplier_entry.insert(0, purchase.get('supplier', ''))
        
        tk.Label(info_frame, text="Date:", font=("Arial", 12, "bold")).grid(row=0, column=2, sticky="w")
        date_entry = tk.Entry(info_frame, width=15, font=("Arial", 12))
        date_entry.grid(row=0, column=3, padx=10)
        date_str = purchase.get('purchase_date', '')[:10] if purchase.get('purchase_date') else ''
        date_entry.insert(0, date_str)
        
        # Item details
        details_frame = tk.LabelFrame(edit_window, text="Item Details", font=("Arial", 12, "bold"))
        details_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Label(details_frame, text="Item:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        item_entry = tk.Entry(details_frame, width=20)
        item_entry.grid(row=0, column=1, padx=10, pady=5)
        item_entry.insert(0, purchase.get('item', ''))
        
        tk.Label(details_frame, text="Quantity:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        qty_entry = tk.Entry(details_frame, width=15)
        qty_entry.grid(row=1, column=1, padx=10, pady=5)
        qty_entry.insert(0, str(purchase.get('quantity', 0)))
        
        tk.Label(details_frame, text="Price:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        price_entry = tk.Entry(details_frame, width=15)
        price_entry.grid(row=2, column=1, padx=10, pady=5)
        price_entry.insert(0, str(purchase.get('price', 0)))
        
        # Total display
        total_label = tk.Label(edit_window, text=f"Total: KSH {purchase.get('total', 0):.2f}", 
                              font=("Arial", 14, "bold"), fg="#2E86AB")
        total_label.pack(pady=10)
        
        # Update total when qty or price changes
        def update_total(*args):
            try:
                qty = float(qty_entry.get() or 0)
                price = float(price_entry.get() or 0)
                total = qty * price
                total_label.config(text=f"Total: KSH {total:.2f}")
            except ValueError:
                pass
        
        qty_entry.bind('<KeyRelease>', update_total)
        price_entry.bind('<KeyRelease>', update_total)
        
        # Save button
        def save_changes():
            supplier = supplier_entry.get().strip()
            item = item_entry.get().strip()
            date_str = date_entry.get().strip()
            
            if not all([supplier, item]):
                messagebox.showerror("Error", "Supplier and item are required")
                return
            
            try:
                qty = float(qty_entry.get() or 0)
                price = float(price_entry.get() or 0)
                total = qty * price
                
                if qty <= 0 or price <= 0:
                    messagebox.showerror("Error", "Quantity and price must be positive")
                    return
                
                # Update purchase
                purchases = self.load_purchases()
                for i, p in enumerate(purchases):
                    if p.get('id') == purchase.get('id'):
                        purchases[i]['supplier'] = supplier
                        purchases[i]['item'] = item
                        purchases[i]['quantity'] = qty
                        purchases[i]['price'] = price
                        purchases[i]['total'] = total
                        if date_str:
                            purchases[i]['purchase_date'] = f"{date_str}T{datetime.now().strftime('%H:%M:%S')}"
                        break
                
                with open("purchases.json", 'w') as f:
                    json.dump(purchases, f, indent=2)
                
                messagebox.showinfo("Success", "Purchase updated successfully!")
                edit_window.destroy()
                self.refresh_purchases_tree(tree)
                
            except ValueError:
                messagebox.showerror("Error", "Invalid quantity or price")
        
        tk.Button(edit_window, text="Save Changes", command=save_changes,
                 bg="#4CAF50", fg="white", font=("Arial", 12, "bold"),
                 width=15, height=2).pack(pady=20)
    
    def export_month_by_name(self, month_name):
        months = {"January": "01", "February": "02", "March": "03", "April": "04", "May": "05", "June": "06",
                 "July": "07", "August": "08", "September": "09", "October": "10", "November": "11", "December": "12"}
        
        month = months[month_name]
        year = str(datetime.now().year)
        
        # Ask for report type
        choice = messagebox.askyesnocancel("Report Type", f"Export {month_name} {year} report:\n\nYes = Sales\nNo = Purchases\nCancel = Both")
        
        if choice is True:
            self.export_month_sales(month, year)
        elif choice is False:
            self.export_month_purchases(month, year)
        elif choice is None:
            self.export_month_sales(month, year)
            self.export_month_purchases(month, year)
    
    def create_manual_backup(self):
        """Create manual backup"""
        try:
            backup_path = backup_system.create_backup()
            messagebox.showinfo("Backup Created", f"Backup saved to:\n{backup_path}")
        except Exception as e:
            messagebox.showerror("Backup Failed", f"Could not create backup: {e}")
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = FoodApp()
    app.run()