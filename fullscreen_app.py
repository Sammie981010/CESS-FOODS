import tkinter as tk
from tkinter import ttk, messagebox, filedialog
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

if __name__ == "__main__":
    app = FullScreenApp()
    app.root.mainloop()
    
    def create_orders_tab(self):
        orders_frame = ttk.Frame(self.notebook)
        self.notebook.add(orders_frame, text="Orders")
        
        customer_frame = tk.Frame(orders_frame)
        customer_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Label(customer_frame, text="Customer Name:", font=("Arial", 12, "bold")).pack(side="left")
        self.order_customer_entry = tk.Entry(customer_frame, width=30, font=("Arial", 12))
        self.order_customer_entry.pack(side="left", padx=10)
        
        self.order_no_label = tk.Label(customer_frame, text=f"Order No: ORD-{self.order_counter:04d}", 
                                      font=("Arial", 12, "bold"), fg="#2E86AB")
        self.order_no_label.pack(side="right", padx=10)
        
        order_item_frame = tk.LabelFrame(orders_frame, text="Add Order Items", font=("Arial", 12, "bold"))
        order_item_frame.pack(fill="x", padx=20, pady=10)
        
        order_fields_frame = tk.Frame(order_item_frame)
        order_fields_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Label(order_fields_frame, text="Item:", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.order_item_entry = tk.Entry(order_fields_frame, width=20, font=("Arial", 10))
        self.order_item_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(order_fields_frame, text="Qty:", font=("Arial", 10, "bold")).grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.order_qty_entry = tk.Entry(order_fields_frame, width=10, font=("Arial", 10))
        self.order_qty_entry.grid(row=0, column=3, padx=5, pady=5)
        
        tk.Label(order_fields_frame, text="Price (KSH):", font=("Arial", 10, "bold")).grid(row=0, column=4, padx=5, pady=5, sticky="w")
        self.order_price_entry = tk.Entry(order_fields_frame, width=12, font=("Arial", 10))
        self.order_price_entry.grid(row=0, column=5, padx=5, pady=5)
        
        tk.Button(order_fields_frame, text="Add Item", command=self.add_order_item,
                 bg="#4CAF50", fg="white", font=("Arial", 10, "bold")).grid(row=0, column=6, padx=5, pady=5)
        
        order_list_frame = tk.LabelFrame(orders_frame, text="Order Items", font=("Arial", 12, "bold"))
        order_list_frame.pack(fill="both", expand=True, padx=20, pady=5)
        
        self.order_tree = ttk.Treeview(order_list_frame, columns=("Item", "Qty", "Price", "Total"), 
                                      show="headings", height=6)
        for col in ["Item", "Qty", "Price", "Total"]:
            self.order_tree.heading(col, text=col)
            self.order_tree.column(col, width=120, anchor="center")
        
        scrollbar_o = ttk.Scrollbar(order_list_frame, orient="vertical", command=self.order_tree.yview)
        self.order_tree.configure(yscrollcommand=scrollbar_o.set)
        
        self.order_tree.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        scrollbar_o.pack(side="right", fill="y")
        
        self.order_total_label = tk.Label(orders_frame, text="Total: KSH 0.00", 
                                         font=("Arial", 14, "bold"), fg="#2E86AB", bg="#f8f9fa", 
                                         relief="ridge", bd=2, padx=20, pady=10)
        self.order_total_label.pack(pady=5)
        
        order_btn_frame = tk.Frame(orders_frame)
        order_btn_frame.pack(pady=5)
        
        tk.Button(order_btn_frame, text="Save Order", command=self.save_order,
                 bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), 
                 width=15, height=3).pack(side="left", padx=2)
        
        tk.Button(order_btn_frame, text="Clear All", command=self.clear_order,
                 bg="#FFC107", fg="black", font=("Arial", 12, "bold"), 
                 width=15, height=3).pack(side="left", padx=2)
        
        tk.Button(order_btn_frame, text="Remove Selected", command=self.remove_order_item,
                 bg="#f44336", fg="white", font=("Arial", 12, "bold"), 
                 width=15, height=3).pack(side="left", padx=2)
        
        tk.Button(order_btn_frame, text="Export PDF", command=self.download_orders_pdf,
                 bg="#FF6B35", fg="white", font=("Arial", 12, "bold"), 
                 width=15, height=3).pack(side="left", padx=2)