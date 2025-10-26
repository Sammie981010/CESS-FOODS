"""
Test script for the invoice editor functionality
"""
import tkinter as tk
from invoice_editor import InvoiceEditor

def test_sales_editor():
    """Test the sales invoice editor"""
    root = tk.Tk()
    root.withdraw()  # Hide main window
    
    editor = InvoiceEditor(root, "sales")
    editor.open_editor_window()
    
    root.mainloop()

def test_purchase_editor():
    """Test the purchase invoice editor"""
    root = tk.Tk()
    root.withdraw()  # Hide main window
    
    editor = InvoiceEditor(root, "purchases")
    editor.open_editor_window()
    
    root.mainloop()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "purchases":
        test_purchase_editor()
    else:
        test_sales_editor()