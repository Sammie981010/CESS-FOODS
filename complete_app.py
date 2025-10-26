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
    
    def create_summary_tab(self):
        summary_frame = ttk.Frame(self.notebook)
        self.notebook.add(summary_frame, text="Dashboard")
        
        main_container = tk.Frame(summary_frame, bg="#f8f9fa")
        main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        title_frame = tk.Frame(main_container, bg="#f8f9fa")
        title_frame.pack(fill="x", pady=(0, 10))
        
        tk.Label(title_frame, text="📊 BUSINESS DASHBOARD", 
                font=("Arial", 20, "bold"), fg="#2E86AB", bg="#f8f9fa").pack()
        
        export_frame = tk.Frame(main_container, bg="#f8f9fa")
        export_frame.pack(fill="x", pady=(0, 20))
        
        tk.Label(export_frame, text="Export Period:", font=("Arial", 10, "bold"), bg="#f8f9fa").pack(side="left", padx=5)
        self.export_period = tk.StringVar(value="All Time")
        export_dropdown = ttk.Combobox(export_frame, textvariable=self.export_period,
                                     values=["Weekly", "Monthly", "All Time"],
                                     width=10, font=("Arial", 9), state="readonly")
        export_dropdown.pack(side="left", padx=5)
        
        tk.Button(export_frame, text="📄 Export Sales PDF", command=self.download_sales_pdf,
                 bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), 
                 width=18, height=1, relief="flat", bd=0, padx=10, pady=8).pack(side="left", padx=8)
        
        tk.Button(export_frame, text="📦 Export Purchases PDF", command=self.download_purchase_pdf,
                 bg="#FF9800", fg="white", font=("Arial", 10, "bold"), 
                 width=18, height=1, relief="flat", bd=0, padx=10, pady=8).pack(side="left", padx=8)
        
        tk.Button(export_frame, text="💾 Backup Data", command=self.backup_data,
                 bg="#607D8B", fg="white", font=("Arial", 10, "bold"), 
                 width=18, height=1, relief="flat", bd=0, padx=10, pady=8).pack(side="left", padx=8)
        
        stats_frame = tk.Frame(main_container, bg="#f8f9fa")
        stats_frame.pack(fill="x", pady=(0, 20))
        
        self.sales_card = tk.Frame(stats_frame, bg="#4CAF50", relief="flat", bd=1)
        self.sales_card.pack(side="left", fill="both", expand=True, padx=(0, 8))
        
        tk.Label(self.sales_card, text="💰 SALES", font=("Arial", 10, "bold"), 
                fg="white", bg="#4CAF50").pack(pady=5)
        self.sales_amount_label = tk.Label(self.sales_card, text="KSH 0.00", 
                                          font=("Arial", 12, "bold"), fg="white", bg="#4CAF50")
        self.sales_amount_label.pack()
        self.sales_count_label = tk.Label(self.sales_card, text="0 transactions", 
                                         font=("Arial", 8), fg="white", bg="#4CAF50")
        self.sales_count_label.pack(pady=(0, 5))
        
        self.purchases_card = tk.Frame(stats_frame, bg="#FF9800", relief="flat", bd=1)
        self.purchases_card.pack(side="left", fill="both", expand=True, padx=8)
        
        tk.Label(self.purchases_card, text="📦 PURCHASES", font=("Arial", 10, "bold"), 
                fg="white", bg="#FF9800").pack(pady=5)
        self.purchases_amount_label = tk.Label(self.purchases_card, text="KSH 0.00", 
                                              font=("Arial", 12, "bold"), fg="white", bg="#FF9800")
        self.purchases_amount_label.pack()
        self.purchases_count_label = tk.Label(self.purchases_card, text="0 transactions", 
                                             font=("Arial", 8), fg="white", bg="#FF9800")
        self.purchases_count_label.pack(pady=(0, 5))
        
        self.profit_card = tk.Frame(stats_frame, bg="#2196F3", relief="flat", bd=1)
        self.profit_card.pack(side="left", fill="both", expand=True, padx=(8, 0))
        
        tk.Label(self.profit_card, text="📈 PROFIT", font=("Arial", 10, "bold"), 
                fg="white", bg="#2196F3").pack(pady=5)
        self.profit_amount_label = tk.Label(self.profit_card, text="KSH 0.00", 
                                           font=("Arial", 12, "bold"), fg="white", bg="#2196F3")
        self.profit_amount_label.pack()
        self.profit_margin_label = tk.Label(self.profit_card, text="0% margin", 
                                           font=("Arial", 8), fg="white", bg="#2196F3")
        self.profit_margin_label.pack(pady=(0, 5))
        
        if MATPLOTLIB_AVAILABLE:
            self.graph_frame = tk.Frame(main_container, bg="white", relief="raised", bd=1, height=300)
            self.graph_frame.pack(fill="both", expand=True, pady=20)
            self.graph_frame.pack_propagate(False)
            
            tk.Label(self.graph_frame, text="Monthly Sales Trend", 
                    font=("Arial", 14, "bold"), bg="white").pack(pady=5)
        else:
            graph_placeholder = tk.Frame(main_container, bg="white", relief="raised", bd=1)
            graph_placeholder.pack(fill="both", expand=True, pady=20)
            tk.Label(graph_placeholder, text="Sales Graph\n(Install matplotlib for charts)", 
                    font=("Arial", 12), bg="white", fg="gray").pack(expand=True)
        
        self.root.after(300, self.update_dashboard)
    
    def get_next_invoice_number(self):
        return 1
    
    def get_next_order_number(self):
        return 1
    
    def create_orders_tab(self):
        tk.Label(self.notebook, text="Orders tab - Coming soon").pack()
    
    def create_purchase_tab(self):
        tk.Label(self.notebook, text="Purchase tab - Coming soon").pack()
    
    def create_sales_tab(self):
        tk.Label(self.notebook, text="Sales tab - Coming soon").pack()
    
    def create_supplier_payments_tab(self):
        tk.Label(self.notebook, text="Supplier Payments tab - Coming soon").pack()
    
    def update_dashboard(self):
        pass
    
    def download_sales_pdf(self):
        messagebox.showinfo("Info", "Sales PDF export - Coming soon")
    
    def download_purchase_pdf(self):
        messagebox.showinfo("Info", "Purchase PDF export - Coming soon")
    
    def backup_data(self):
        messagebox.showinfo("Info", "Data backup - Coming soon")

if __name__ == "__main__":
    app = FullScreenApp()
    app.root.mainloop()