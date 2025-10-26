import tkinter as tk
from tkinter import messagebox

class SimpleApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("CESS FOODS - Management System")
        self.root.state('zoomed')
        self.root.withdraw()
        self.show_login()
    
    def show_login(self):
        self.login_window = tk.Toplevel()
        self.login_window.title("CESS FOODS - Login")
        self.login_window.geometry("400x300")
        self.login_window.configure(bg="#2E86AB")
        
        tk.Label(self.login_window, text="CESS FOODS", font=("Arial", 20, "bold"), 
                fg="white", bg="#2E86AB").pack(pady=30)
        
        login_frame = tk.Frame(self.login_window, bg="white")
        login_frame.pack(padx=50, pady=20, fill="both", expand=True)
        
        tk.Label(login_frame, text="Username:", bg="white").pack(pady=5)
        self.username_entry = tk.Entry(login_frame, width=25)
        self.username_entry.pack(pady=5)
        
        tk.Label(login_frame, text="Password:", bg="white").pack(pady=5)
        self.password_entry = tk.Entry(login_frame, width=25, show="*")
        self.password_entry.pack(pady=5)
        
        tk.Button(login_frame, text="Login", command=self.validate_login,
                 bg="#4CAF50", fg="white").pack(pady=20)
        
        self.username_entry.focus()
    
    def validate_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if username == "admin" and password == "admin123":
            self.login_window.destroy()
            self.root.deiconify()
            self.create_main_interface()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")
    
    def create_main_interface(self):
        tk.Label(self.root, text="CESS FOODS - MANAGEMENT SYSTEM", 
                font=("Arial", 20, "bold"), bg="#2E86AB", fg="white").pack(pady=20)
        
        tk.Label(self.root, text="Welcome to CESS FOODS Management System!", 
                font=("Arial", 16)).pack(pady=50)
        
        tk.Button(self.root, text="Exit", command=self.root.quit,
                 bg="#f44336", fg="white", font=("Arial", 12, "bold")).pack(pady=20)

if __name__ == "__main__":
    app = SimpleApp()
    app.root.mainloop()