aps import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime
import uuid
from hirewise_phase2 import HireWisePhase2Features
from hirewise_gps import HireWiseGPS

class HireWiseApp:
    
    def refresh_professionals_list(self, tree, service_filter, location_filter, rating_filter, price_filter):
        # Clear existing items
        for item in tree.get_children():
            tree.delete(item)
        
        # Load professionals
        with open(self.professionals_file, 'r') as f:
            professionals = json.load(f)
        
        # Apply filters
        for pro_id, pro in professionals.items():
            # Service filter
            if service_filter != "All" and pro['service'] != service_filter:
                continue
            
            # Location filter
            if location_filter != "All" and pro['location'] != location_filter:
                continue
            
            # Rating filter
            if rating_filter != "All":
                min_rating = float(rating_filter.replace("+", ""))
                if pro['rating'] < min_rating:
                    continue
            
            # Price filter
            if price_filter != "All":
                if price_filter == "300+" and not pro['price'].startswith("300") and not pro['price'].startswith("500"):
                    continue
                elif price_filter != "300+" and pro['price'] != price_filter:
                    continue
            
            badge = " ✓" if pro.get('certified', False) else ""
            tree.insert('', 'end', text=pro['name'] + badge,
                       values=(pro['service'], f"{pro['rating']}⭐", pro['price'], pro['location']))
    
    def show_messages(self):
        msg_window = tk.Toplevel(self.root)
        msg_window.title("Messages")
        msg_window.geometry("700x500")
        
        frame = ttk.Frame(msg_window, padding="20")
        frame.pack(expand=True, fill='both')
        
        ttk.Label(frame, text="Messages", font=('Arial', 16, 'bold')).pack(pady=10)
        
        # Load messages
        with open(self.messages_file, 'r') as f:
            messages = json.load(f)
        
        # Filter user's messages
        user_messages = {k: v for k, v in messages.items() 
                        if v.get('sender') == self.current_user['email'] or v.get('receiver') == self.current_user['email']}
        
        if not user_messages:
            ttk.Label(frame, text="No messages yet").pack(pady=20)
            return
        
        # Messages list
        msg_frame = ttk.Frame(frame)
        msg_frame.pack(expand=True, fill='both')
        
        for msg_id, msg in user_messages.items():
            msg_item = ttk.LabelFrame(msg_frame, text=f"From: {msg['sender']}", padding="10")
            msg_item.pack(fill='x', pady=5)
            
            ttk.Label(msg_item, text=msg['content']).pack(anchor='w')
            ttk.Label(msg_item, text=f"Date: {msg['created'][:10]}", font=('Arial', 8)).pack(anchor='e')
        
        # Send new message
        send_frame = ttk.LabelFrame(frame, text="Send Message", padding="10")
        send_frame.pack(fill='x', pady=10)
        
        ttk.Label(send_frame, text="To:").pack(anchor='w')
        to_entry = ttk.Entry(send_frame)
        to_entry.pack(fill='x', pady=2)
        
        ttk.Label(send_frame, text="Message:").pack(anchor='w')
        msg_text = tk.Text(send_frame, height=3)
        msg_text.pack(fill='x', pady=2)
        
        def send_message():
            if not to_entry.get().strip() or not msg_text.get("1.0", tk.END).strip():
                messagebox.showerror("Error", "Please fill in recipient and message")
                return
            
            msg_id = str(uuid.uuid4())[:8]
            messages[msg_id] = {
                "id": msg_id,
                "sender": self.current_user['email'],
                "receiver": to_entry.get().strip(),
                "content": msg_text.get("1.0", tk.END).strip(),
                "created": datetime.now().isoformat()
            }
            
            with open(self.messages_file, 'w') as f:
                json.dump(messages, f)
            
            messagebox.showinfo("Success", "Message sent!")
            msg_window.destroy()
        
        ttk.Button(send_frame, text="Send", command=send_message).pack(pady=5)
    
    def show_payments(self):
        pay_window = tk.Toplevel(self.root)
        pay_window.title("Payments & Wallet")
        pay_window.geometry("600x500")
        
        frame = ttk.Frame(pay_window, padding="20")
        frame.pack(expand=True, fill='both')
        
        ttk.Label(frame, text="Payment System", font=('Arial', 16, 'bold')).pack(pady=10)
        
        # Wallet balance
        balance_frame = ttk.LabelFrame(frame, text="Wallet Balance", padding="10")
        balance_frame.pack(fill='x', pady=10)
        
        ttk.Label(balance_frame, text="Current Balance: KSH 1,250", font=('Arial', 12, 'bold')).pack()
        
        # M-Pesa integration
        mpesa_frame = ttk.LabelFrame(frame, text="M-Pesa Top Up", padding="10")
        mpesa_frame.pack(fill='x', pady=10)
        
        ttk.Label(mpesa_frame, text="Phone Number:").pack(anchor='w')
        phone_entry = ttk.Entry(mpesa_frame)
        phone_entry.pack(fill='x', pady=2)
        
        ttk.Label(mpesa_frame, text="Amount (KSH):").pack(anchor='w')
        amount_entry = ttk.Entry(mpesa_frame)
        amount_entry.pack(fill='x', pady=2)
        
        def initiate_mpesa():
            if not phone_entry.get().strip() or not amount_entry.get().strip():
                messagebox.showerror("Error", "Please fill in phone and amount")
                return
            
            # Simulate M-Pesa STK push
            messagebox.showinfo("M-Pesa", f"STK push sent to {phone_entry.get()}\nEnter PIN to complete payment")
            
            # Save payment record
            with open(self.payments_file, 'r') as f:
                payments = json.load(f)
            
            pay_id = str(uuid.uuid4())[:8]
            payments[pay_id] = {
                "id": pay_id,
                "user": self.current_user['email'],
                "type": "Top Up",
                "amount": amount_entry.get().strip(),
                "method": "M-Pesa",
                "status": "Completed",
                "created": datetime.now().isoformat()
            }
            
            with open(self.payments_file, 'w') as f:
                json.dump(payments, f)
        
        ttk.Button(mpesa_frame, text="Pay via M-Pesa", command=initiate_mpesa).pack(pady=5)
    
    def show_admin_pros(self):
        admin_window = tk.Toplevel(self.root)
        admin_window.title("Manage Professionals")
        admin_window.geometry("800x600")
        
        frame = ttk.Frame(admin_window, padding="20")
        frame.pack(expand=True, fill='both')
        
        ttk.Label(frame, text="Professional Management", font=('Arial', 16, 'bold')).pack(pady=10)
        
        # Load professionals
        with open(self.professionals_file, 'r') as f:
            professionals = json.load(f)
        
        # Create treeview
        tree = ttk.Treeview(frame, columns=('Service', 'Rating', 'Certified', 'Status'), show='tree headings')
        tree.heading('#0', text='Name')
        tree.heading('Service', text='Service')
        tree.heading('Rating', text='Rating')
        tree.heading('Certified', text='Certified')
        tree.heading('Status', text='Status')
        
        for pro_id, pro in professionals.items():
            certified = "Yes" if pro.get('certified', False) else "No"
            status = pro.get('status', 'Active')
            tree.insert('', 'end', text=pro['name'],
                       values=(pro['service'], f"{pro['rating']}⭐", certified, status))
        
        tree.pack(expand=True, fill='both', pady=10)
        
        def approve_professional():
            messagebox.showinfo("Success", "Professional approved and certified!")
        
        ttk.Button(frame, text="Approve & Certify", command=approve_professional).pack(pady=10)
    
    def show_analytics(self):
        analytics_window = tk.Toplevel(self.root)
        analytics_window.title("System Analytics")
        analytics_window.geometry("600x500")
        
        frame = ttk.Frame(analytics_window, padding="20")
        frame.pack(expand=True, fill='both')
        
        ttk.Label(frame, text="System Analytics", font=('Arial', 16, 'bold')).pack(pady=10)
        
        # Load data for analytics
        with open(self.users_file, 'r') as f:
            users = json.load(f)
        with open(self.jobs_file, 'r') as f:
            jobs = json.load(f)
        with open(self.professionals_file, 'r') as f:
            professionals = json.load(f)
        
        # Statistics
        stats_frame = ttk.LabelFrame(frame, text="Platform Statistics", padding="20")
        stats_frame.pack(fill='x', pady=10)
        
        total_users = len(users)
        total_jobs = len(jobs)
        total_pros = len(professionals)
        active_jobs = len([j for j in jobs.values() if j['status'] == 'Open'])
        
        ttk.Label(stats_frame, text=f"Total Users: {total_users}", font=('Arial', 12)).pack(anchor='w')
        ttk.Label(stats_frame, text=f"Total Jobs Posted: {total_jobs}", font=('Arial', 12)).pack(anchor='w')
        ttk.Label(stats_frame, text=f"Active Professionals: {total_pros}", font=('Arial', 12)).pack(anchor='w')
        ttk.Label(stats_frame, text=f"Open Jobs: {active_jobs}", font=('Arial', 12)).pack(anchor='w')
    
    def show_disputes(self):
        disputes_window = tk.Toplevel(self.root)
        disputes_window.title("Manage Disputes")
        disputes_window.geometry("700x400")
        
        frame = ttk.Frame(disputes_window, padding="20")
        frame.pack(expand=True, fill='both')
        
        ttk.Label(frame, text="Dispute Management", font=('Arial', 16, 'bold')).pack(pady=10)
        
        # Sample disputes
        disputes = [
            {"id": "D001", "client": "john@email.com", "professional": "mary@email.com", "issue": "Work not completed", "status": "Open"},
            {"id": "D002", "client": "jane@email.com", "professional": "mike@email.com", "issue": "Payment dispute", "status": "Resolved"}
        ]
        
        tree = ttk.Treeview(frame, columns=('Client', 'Professional', 'Issue', 'Status'), show='tree headings')
        tree.heading('#0', text='Dispute ID')
        tree.heading('Client', text='Client')
        tree.heading('Professional', text='Professional')
        tree.heading('Issue', text='Issue')
        tree.heading('Status', text='Status')
        
        for dispute in disputes:
            tree.insert('', 'end', text=dispute['id'],
                       values=(dispute['client'], dispute['professional'], dispute['issue'], dispute['status']))
        
        tree.pack(expand=True, fill='both', pady=10)
        
        def resolve_dispute():
            messagebox.showinfo("Success", "Dispute resolved and parties notified!")
        
        ttk.Button(frame, text="Resolve Dispute", command=resolve_dispute).pack(pady=10)
    
    def show_contact(self):
        """Show contact support window"""
        contact_window = tk.Toplevel(self.root)
        contact_window.title("📞 Contact Support")
        contact_window.geometry("500x600")
        contact_window.configure(bg='white')
        
        # Header
        header_frame = tk.Frame(contact_window, bg='#3498db', height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="📞 Contact Support", font=('Arial', 18, 'bold'), 
                bg='#3498db', fg='white').pack(expand=True)
        
        # Content
        content_frame = tk.Frame(contact_window, bg='white')
        content_frame.pack(fill='both', expand=True, padx=30, pady=20)
        
        # Contact methods
        methods_frame = tk.LabelFrame(content_frame, text="Get in Touch", font=('Arial', 12, 'bold'), 
                                    bg='white', fg='#2c3e50', padx=20, pady=15)
        methods_frame.pack(fill='x', pady=10)
        
        contact_methods = [
            ("📞 Phone Support", "+254 700 123 456", "Available 24/7"),
            ("📧 Email Support", "support@hirewise.co.ke", "Response within 2 hours"),
            ("💬 WhatsApp", "+254 700 123 456", "Instant messaging support"),
            ("🏢 Office Address", "Westlands, Nairobi", "Visit us Mon-Fri 8AM-6PM")
        ]
        
        for icon_title, contact, desc in contact_methods:
            method_frame = tk.Frame(methods_frame, bg='white')
            method_frame.pack(fill='x', pady=8)
            
            tk.Label(method_frame, text=icon_title, font=('Arial', 11, 'bold'), 
                    bg='white', fg='#2c3e50').pack(anchor='w')
            tk.Label(method_frame, text=contact, font=('Arial', 10, 'bold'), 
                    bg='white', fg='#3498db').pack(anchor='w')
            tk.Label(method_frame, text=desc, font=('Arial', 9), 
                    bg='white', fg='#7f8c8d').pack(anchor='w')
        
        # Quick message form
        message_frame = tk.LabelFrame(content_frame, text="Send Quick Message", font=('Arial', 12, 'bold'),
                                    bg='white', fg='#2c3e50', padx=20, pady=15)
        message_frame.pack(fill='both', expand=True, pady=10)
        
        tk.Label(message_frame, text="Subject:", font=('Arial', 10, 'bold'), bg='white', fg='#2c3e50').pack(anchor='w')
        subject_entry = tk.Entry(message_frame, font=('Arial', 10), bg='#f8f9fa', relief='solid', bd=1)
        subject_entry.pack(fill='x', pady=(5,10), ipady=5)
        
        tk.Label(message_frame, text="Message:", font=('Arial', 10, 'bold'), bg='white', fg='#2c3e50').pack(anchor='w')
        message_text = tk.Text(message_frame, height=6, font=('Arial', 10), bg='#f8f9fa', relief='solid', bd=1)
        message_text.pack(fill='both', expand=True, pady=(5,10))
        
        def send_support_message():
            if subject_entry.get().strip() and message_text.get("1.0", tk.END).strip():
                messagebox.showinfo("Message Sent", "Your message has been sent to our support team!\nWe'll respond within 2 hours.")
                contact_window.destroy()
            else:
                messagebox.showerror("Error", "Please fill in both subject and message")
        
        send_btn = tk.Button(message_frame, text="Send Message", command=send_support_message,
                           font=('Arial', 11, 'bold'), bg='#27ae60', fg='white', relief='flat',
                           padx=20, pady=8, cursor='hand2')
        send_btn.pack(pady=10)
        
        # FAQ section
        faq_frame = tk.LabelFrame(content_frame, text="Frequently Asked Questions", font=('Arial', 12, 'bold'),
                                bg='white', fg='#2c3e50', padx=20, pady=15)
        faq_frame.pack(fill='x', pady=10)
        
        faqs = [
            "❓ How do I verify my professional account?",
            "❓ What payment methods are accepted?",
            "❓ How does the GPS location feature work?",
            "❓ How to resolve disputes with clients/professionals?"
        ]
        
        for faq in faqs:
            tk.Label(faq_frame, text=faq, font=('Arial', 9), bg='white', fg='#3498db', cursor='hand2').pack(anchor='w', pady=2)
    
    def show_nearest_jobs(self):
        """Show nearest jobs for professionals using GPS"""
        jobs_window = tk.Toplevel(self.root)
        jobs_window.title("📍 Nearest Jobs")
        jobs_window.geometry("700x500")
        
        frame = ttk.Frame(jobs_window, padding="20")
        frame.pack(expand=True, fill='both')
        
        ttk.Label(frame, text="📍 Jobs Near You", font=('Arial', 16, 'bold')).pack(pady=10)
        
        # Current location
        current_area, coords = self.gps.get_current_location()
        ttk.Label(frame, text=f"Your Location: {current_area}", font=('Arial', 12)).pack()
        
        # Load jobs
        with open(self.jobs_file, 'r') as f:
            jobs = json.load(f)
        
        # Filter open jobs and add distance
        open_jobs = []
        for job_id, job in jobs.items():
            if job['status'] == 'Open':
                # Simulate distance calculation
                import random
                distance = round(random.uniform(0.5, 15.0), 1)
                job['distance'] = distance
                job['id'] = job_id
                open_jobs.append(job)
        
        # Sort by distance
        open_jobs.sort(key=lambda x: x['distance'])
        
        # Create treeview
        tree = ttk.Treeview(frame, columns=('Service', 'Distance', 'Budget', 'Timing'), show='tree headings')
        tree.heading('#0', text='Description')
        tree.heading('Service', text='Service')
        tree.heading('Distance', text='Distance (km)')
        tree.heading('Budget', text='Budget')
        tree.heading('Timing', text='Timing')
        
        for job in open_jobs:
            desc = job['description'][:30] + "..." if len(job['description']) > 30 else job['description']
            distance_color = "🟢" if job['distance'] < 5 else "🟡" if job['distance'] < 10 else "🔴"
            tree.insert('', 'end', text=desc,
                       values=(job['service'], f"{distance_color} {job['distance']} km", job['budget'], job['timing']))
        
        tree.pack(expand=True, fill='both', pady=10)
        
        def apply_to_job():
            selection = tree.selection()
            if not selection:
                messagebox.showwarning("Warning", "Please select a job")
                return
            
            messagebox.showinfo("Success", "Quote sent to nearby client!")
        
        ttk.Button(frame, text="Send Quote", command=apply_to_job).pack(pady=10)
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("HireWise - Find & Hire Professionals")
        self.root.geometry("600x600")
        self.root.minsize(500, 500)
        
        # Data storage
        self.users_file = "hirewise_users.json"
        self.jobs_file = "hirewise_jobs.json"
        self.professionals_file = "hirewise_professionals.json"
        self.quotes_file = "hirewise_quotes.json"
        self.messages_file = "hirewise_messages.json"
        self.payments_file = "hirewise_payments.json"
        self.reviews_file = "hirewise_reviews.json"
        self.notifications_file = "hirewise_notifications.json"
        
        # Phase 2 features
        self.phase2 = None
        
        self.current_user = None
        self.load_data()
        self.create_main_interface()
    
    def load_data(self):
        # Load or create data files
        files = [self.users_file, self.jobs_file, self.professionals_file, self.quotes_file, 
                self.messages_file, self.payments_file, self.reviews_file, self.notifications_file]
        for file in files:
            if not os.path.exists(file):
                with open(file, 'w') as f:
                    json.dump({}, f)
        
        # Sample professionals data
        if os.path.getsize(self.professionals_file) == 0:
            sample_pros = {
                "pro1": {"name": "John Plumber", "service": "Plumber", "rating": 4.8, "price": "50-100", "location": "Nairobi", "certified": True, "bio": "Expert plumber with 5+ years experience"},
                "pro2": {"name": "Mary Cleaner", "service": "Cleaner", "rating": 4.9, "price": "30-60", "location": "Nairobi", "certified": True, "bio": "Professional cleaning services"},
                "pro3": {"name": "Tech Mike", "service": "Web Designer", "rating": 4.7, "price": "100-300", "location": "Nairobi", "certified": False, "bio": "Modern web design solutions"}
            }
            with open(self.professionals_file, 'w') as f:
                json.dump(sample_pros, f)
    
    def create_main_interface(self):
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        if not self.current_user:
            self.show_login_screen()
        else:
            self.show_dashboard()
    
    def show_login_screen(self):
        # BASIC LOGIN - GUARANTEED VISIBLE BUTTONS
        frame = tk.Frame(self.root)
        frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        tk.Label(frame, text="HireWise - Login", font=('Arial', 20, 'bold')).pack(pady=20)
        
        # Email
        tk.Label(frame, text="Email:", font=('Arial', 12)).pack()
        self.email_entry = tk.Entry(frame, font=('Arial', 12), width=30)
        self.email_entry.pack(pady=5)
        
        # Name
        tk.Label(frame, text="Name:", font=('Arial', 12)).pack()
        self.name_entry = tk.Entry(frame, font=('Arial', 12), width=30)
        self.name_entry.pack(pady=5)
        

        
        # User type
        tk.Label(frame, text="Account Type:", font=('Arial', 12)).pack(pady=(10,5))
        self.user_type = tk.StringVar(value="Client")
        tk.Radiobutton(frame, text="Client", variable=self.user_type, value="Client").pack()
        tk.Radiobutton(frame, text="Professional", variable=self.user_type, value="Professional").pack()
        tk.Radiobutton(frame, text="Admin", variable=self.user_type, value="Admin").pack()
        
        # Auto-detect GPS location
        tk.Label(frame, text="📍 Detecting precise GPS location...", font=('Arial', 10), fg='blue').pack(pady=5)
        tk.Label(frame, text="(Building, Road, Area)", font=('Arial', 8), fg='gray').pack(pady=5)
        
        # LOGIN BUTTON - MINIMIZED
        tk.Button(frame, text="LOGIN", command=self.login_user,
                 font=('Arial', 12, 'bold'), bg='green', fg='white',
                 width=10, height=1).pack(pady=20)
    
    def get_auto_location(self):
        """Simulate accurate GPS location detection with specific addresses"""
        import random
        accurate_locations = [
            "Greenspan Mall, Donholm Road, Nairobi",
            "Sarit Centre, Westlands Avenue, Westlands",
            "Karen Shopping Centre, Dagoretti Road, Karen",
            "Yaya Centre, Argwings Kodhek Road, Kilimani",
            "KICC Building, Harambee Avenue, CBD",
            "Thika Road Mall, Thika Road, Kasarani",
            "Junction Mall, Ngong Road, Dagoretti",
            "Village Market, Limuru Road, Gigiri",
            "Galleria Mall, Langata Road, Langata",
            "Two Rivers Mall, Limuru Road, Runda",
            "Garden City Mall, Thika Road, Ruiru",
            "Prestige Plaza, Ngong Road, Karen",
            "ABC Place, Waiyaki Way, Westlands",
            "The Hub, Karen Road, Karen",
            "Nextgen Mall, Mombasa Road, South C"
        ]
        return random.choice(accurate_locations)
    
    def login_user(self):
        email = self.email_entry.get().strip()
        name = self.name_entry.get().strip()
        
        if not email or not name:
            messagebox.showerror("Error", "Please fill in email and name")
            return
        
        # Auto-detect precise location
        auto_location = self.get_auto_location()
        messagebox.showinfo("📍 Location Detected", f"Precise location detected:\n{auto_location}")
        
        # Load users
        with open(self.users_file, 'r') as f:
            users = json.load(f)
        
        # Create or update user with auto-detected location
        users[email] = {"name": name, "location": auto_location, "email": email, "type": self.user_type.get()}
        
        with open(self.users_file, 'w') as f:
            json.dump(users, f)
        
        self.current_user = users[email]
        self.create_main_interface()
    
    def show_dashboard(self):
        frame = ttk.Frame(self.root, padding="10")
        frame.pack(expand=True, fill='both')
        
        # Header
        header = ttk.Frame(frame)
        header.pack(fill='x', pady=10)
        
        ttk.Label(header, text=f"Welcome, {self.current_user['name']}", 
                 font=('Arial', 16, 'bold')).pack(side='left')
        ttk.Button(header, text="Logout", command=self.logout).pack(side='right')
        
        # Main buttons
        button_frame = ttk.Frame(frame)
        button_frame.pack(pady=20)
        
        # Initialize Phase 2 features and GPS
        self.phase2 = HireWisePhase2Features()
        self.gps = HireWiseGPS()
        
        if self.current_user['type'] == 'Client':
            ttk.Button(button_frame, text="Post a Job", 
                      command=self.show_post_job, width=20).pack(pady=3)
            ttk.Button(button_frame, text="My Jobs", 
                      command=self.show_my_jobs, width=20).pack(pady=3)
            ttk.Button(button_frame, text="Find Professionals", 
                      command=self.show_professionals, width=20).pack(pady=3)
            ttk.Button(button_frame, text="Messages", 
                      command=self.show_messages, width=20).pack(pady=3)
            ttk.Button(button_frame, text="HireWise Wallet 💳", 
                      command=self.phase2.show_hirewise_wallet, width=20).pack(pady=3)
            ttk.Button(button_frame, text="AI Job Match 🤖", 
                      command=lambda: self.phase2.show_ai_job_suggestions(self.current_user), width=20).pack(pady=3)
            ttk.Button(button_frame, text="📍 Nearest Providers", 
                      command=lambda: self.gps.show_gps_professionals(self.root, self.professionals_file), width=20).pack(pady=3)
            ttk.Button(button_frame, text="Referral Program 🎁", 
                      command=self.phase2.show_referral_system, width=20).pack(pady=3)
        elif self.current_user['type'] == 'Professional':
            ttk.Button(button_frame, text="My Profile", 
                      command=self.show_pro_profile, width=20).pack(pady=3)
            ttk.Button(button_frame, text="Browse Jobs", 
                      command=self.show_available_jobs, width=20).pack(pady=3)
            ttk.Button(button_frame, text="My Quotes", 
                      command=self.show_my_quotes, width=20).pack(pady=3)
            ttk.Button(button_frame, text="Messages", 
                      command=self.show_messages, width=20).pack(pady=3)
            ttk.Button(button_frame, text="Skill Badges 🏆", 
                      command=self.phase2.show_skill_verification_badges, width=20).pack(pady=3)
            ttk.Button(button_frame, text="AI Suggestions 🤖", 
                      command=lambda: self.phase2.show_ai_job_suggestions(self.current_user), width=20).pack(pady=3)
            ttk.Button(button_frame, text="HireWise Wallet 💳", 
                      command=self.phase2.show_hirewise_wallet, width=20).pack(pady=3)
            ttk.Button(button_frame, text="📍 Nearest Jobs", 
                      command=self.show_nearest_jobs, width=20).pack(pady=3)
            ttk.Button(button_frame, text="Referral Program 🎁", 
                      command=self.phase2.show_referral_system, width=20).pack(pady=3)
        else:  # Admin
            ttk.Button(button_frame, text="Manage Professionals", 
                      command=self.show_admin_pros, width=20).pack(pady=5)
            ttk.Button(button_frame, text="System Analytics", 
                      command=self.show_analytics, width=20).pack(pady=5)
            ttk.Button(button_frame, text="Manage Disputes", 
                      command=self.show_disputes, width=20).pack(pady=5)
            ttk.Button(button_frame, text="📞 Contact Support", 
                      command=self.show_contact, width=20).pack(pady=5)
        
        # Add contact button for all user types
        ttk.Separator(button_frame, orient='horizontal').pack(fill='x', pady=10)
        ttk.Button(button_frame, text="📞 Contact Support", 
                  command=self.show_contact, width=20).pack(pady=5)
    
    def show_post_job(self):
        job_window = tk.Toplevel(self.root)
        job_window.title("Post a Job")
        job_window.geometry("500x600")
        
        frame = ttk.Frame(job_window, padding="20")
        frame.pack(expand=True, fill='both')
        
        ttk.Label(frame, text="Post a New Job", font=('Arial', 16, 'bold')).pack(pady=10)
        
        # Service type
        ttk.Label(frame, text="Service Type:").pack(anchor='w')
        service_var = tk.StringVar()
        service_combo = ttk.Combobox(frame, textvariable=service_var, 
                                   values=["Plumber", "Cleaner", "Web Designer", "Electrician", "Carpenter"])
        service_combo.pack(fill='x', pady=5)
        
        # Description
        ttk.Label(frame, text="Description:").pack(anchor='w')
        desc_text = tk.Text(frame, height=4)
        desc_text.pack(fill='x', pady=5)
        
        # Budget
        ttk.Label(frame, text="Budget Range (KSH):").pack(anchor='w')
        budget_var = tk.StringVar()
        budget_combo = ttk.Combobox(frame, textvariable=budget_var,
                                  values=["0-50", "50-100", "100-300", "300-500", "500+"])
        budget_combo.pack(fill='x', pady=5)
        
        # Timing
        ttk.Label(frame, text="Timing:").pack(anchor='w')
        timing_var = tk.StringVar(value="Scheduled")
        ttk.Radiobutton(frame, text="Urgent (ASAP)", variable=timing_var, value="Urgent").pack(anchor='w')
        ttk.Radiobutton(frame, text="Scheduled", variable=timing_var, value="Scheduled").pack(anchor='w')
        
        def submit_job():
            if not service_var.get() or not desc_text.get("1.0", tk.END).strip():
                messagebox.showerror("Error", "Please fill in service type and description")
                return
            
            # Load jobs
            with open(self.jobs_file, 'r') as f:
                jobs = json.load(f)
            
            job_id = str(uuid.uuid4())[:8]
            jobs[job_id] = {
                "id": job_id,
                "client": self.current_user['email'],
                "service": service_var.get(),
                "description": desc_text.get("1.0", tk.END).strip(),
                "budget": budget_var.get(),
                "timing": timing_var.get(),
                "status": "Open",
                "created": datetime.now().isoformat()
            }
            
            with open(self.jobs_file, 'w') as f:
                json.dump(jobs, f)
            
            messagebox.showinfo("Success", "Job posted successfully!")
            job_window.destroy()
        
        ttk.Button(frame, text="Post Job", command=submit_job).pack(pady=20)
    
    def show_professionals(self):
        pros_window = tk.Toplevel(self.root)
        pros_window.title("Find Professionals")
        pros_window.geometry("600x500")
        
        frame = ttk.Frame(pros_window, padding="20")
        frame.pack(expand=True, fill='both')
        
        ttk.Label(frame, text="Find Professionals", font=('Arial', 16, 'bold')).pack(pady=10)
        
        # Search and filter frame
        filter_frame = ttk.LabelFrame(frame, text="Search & Filters", padding="10")
        filter_frame.pack(fill='x', pady=10)
        
        # Service filter
        ttk.Label(filter_frame, text="Service:").grid(row=0, column=0, sticky='w')
        service_filter = ttk.Combobox(filter_frame, values=["All", "Plumber", "Cleaner", "Web Designer", "Electrician", "Carpenter"], width=15)
        service_filter.set("All")
        service_filter.grid(row=0, column=1, padx=5)
        
        # Location filter
        ttk.Label(filter_frame, text="Location:").grid(row=0, column=2, sticky='w', padx=(10,0))
        location_filter = ttk.Combobox(filter_frame, values=["All", "Nairobi", "Mombasa", "Kisumu"], width=15)
        location_filter.set("All")
        location_filter.grid(row=0, column=3, padx=5)
        
        # Rating filter
        ttk.Label(filter_frame, text="Min Rating:").grid(row=1, column=0, sticky='w', pady=(5,0))
        rating_filter = ttk.Combobox(filter_frame, values=["All", "4.0+", "4.5+", "4.8+"], width=15)
        rating_filter.set("All")
        rating_filter.grid(row=1, column=1, padx=5, pady=(5,0))
        
        # Price filter
        ttk.Label(filter_frame, text="Price Range:").grid(row=1, column=2, sticky='w', padx=(10,0), pady=(5,0))
        price_filter = ttk.Combobox(filter_frame, values=["All", "0-50", "50-100", "100-300", "300+"], width=15)
        price_filter.set("All")
        price_filter.grid(row=1, column=3, padx=5, pady=(5,0))
        
        def apply_filters():
            self.refresh_professionals_list(tree, service_filter.get(), location_filter.get(), rating_filter.get(), price_filter.get())
        
        ttk.Button(filter_frame, text="Apply Filters", command=apply_filters).grid(row=2, column=1, pady=10)
        
        # Load professionals
        with open(self.professionals_file, 'r') as f:
            professionals = json.load(f)
        
        # Create treeview
        tree = ttk.Treeview(frame, columns=('Service', 'Rating', 'Price', 'Location'), show='tree headings')
        tree.heading('#0', text='Name')
        tree.heading('Service', text='Service')
        tree.heading('Rating', text='Rating')
        tree.heading('Price', text='Price (KSH)')
        tree.heading('Location', text='Location')
        
        # Initial load
        self.refresh_professionals_list(tree, "All", "All", "All", "All")
        
        tree.pack(expand=True, fill='both', pady=10)
        
        def hire_professional():
            selection = tree.selection()
            if not selection:
                messagebox.showwarning("Warning", "Please select a professional")
                return
            
            item = tree.item(selection[0])
            pro_name = item['text']
            
            # Option for video verification
            result = messagebox.askyesno("Hire Professional", 
                                       f"Hire {pro_name}?\n\nWould you like to verify via video call first?")
            if result:
                self.phase2.show_video_call_verification("pro@email.com")
            else:
                messagebox.showinfo("Hire", f"Chat request sent to {pro_name}!\nThey will contact you soon.")
        
        ttk.Button(frame, text="Send Hire Request", command=hire_professional).pack(pady=10)
    
    def show_pro_profile(self):
        profile_window = tk.Toplevel(self.root)
        profile_window.title("Professional Profile")
        profile_window.geometry("500x700")
        
        frame = ttk.Frame(profile_window, padding="20")
        frame.pack(expand=True, fill='both')
        
        ttk.Label(frame, text="Professional Profile", font=('Arial', 16, 'bold')).pack(pady=10)
        
        # Service category
        ttk.Label(frame, text="Service Category:").pack(anchor='w')
        service_var = tk.StringVar()
        service_combo = ttk.Combobox(frame, textvariable=service_var,
                                   values=["Plumber", "Cleaner", "Web Designer", "Electrician", "Carpenter"])
        service_combo.pack(fill='x', pady=5)
        
        # Bio
        ttk.Label(frame, text="Bio:").pack(anchor='w')
        bio_text = tk.Text(frame, height=3)
        bio_text.pack(fill='x', pady=5)
        
        # Pricing
        ttk.Label(frame, text="Price Range (KSH):").pack(anchor='w')
        price_var = tk.StringVar()
        price_combo = ttk.Combobox(frame, textvariable=price_var,
                                 values=["0-50", "50-100", "100-300", "300-500", "500+"])
        price_combo.pack(fill='x', pady=5)
        
        # ID Number for verification
        ttk.Label(frame, text="ID Number (for verification):").pack(anchor='w')
        id_entry = ttk.Entry(frame)
        id_entry.pack(fill='x', pady=5)
        
        # License
        ttk.Label(frame, text="License Number (if applicable):").pack(anchor='w')
        license_entry = ttk.Entry(frame)
        license_entry.pack(fill='x', pady=5)
        
        def save_profile():
            if not service_var.get() or not bio_text.get("1.0", tk.END).strip():
                messagebox.showerror("Error", "Please fill in service and bio")
                return
            
            # Load professionals
            with open(self.professionals_file, 'r') as f:
                professionals = json.load(f)
            
            pro_id = self.current_user['email']
            certified = bool(id_entry.get().strip() and len(id_entry.get().strip()) >= 8)
            
            professionals[pro_id] = {
                "name": self.current_user['name'],
                "service": service_var.get(),
                "bio": bio_text.get("1.0", tk.END).strip(),
                "price": price_var.get(),
                "location": self.current_user['location'],
                "rating": 5.0,
                "certified": certified,
                "id_number": id_entry.get().strip(),
                "license": license_entry.get().strip()
            }
            
            with open(self.professionals_file, 'w') as f:
                json.dump(professionals, f)
            
            badge = " ✓ HireWise Certified" if certified else ""
            messagebox.showinfo("Success", f"Profile saved successfully!{badge}")
            profile_window.destroy()
        
        ttk.Button(frame, text="Save Profile", command=save_profile).pack(pady=20)
    
    def show_available_jobs(self):
        jobs_window = tk.Toplevel(self.root)
        jobs_window.title("Available Jobs")
        jobs_window.geometry("700x500")
        
        frame = ttk.Frame(jobs_window, padding="20")
        frame.pack(expand=True, fill='both')
        
        ttk.Label(frame, text="Available Jobs", font=('Arial', 16, 'bold')).pack(pady=10)
        
        # Load jobs
        with open(self.jobs_file, 'r') as f:
            jobs = json.load(f)
        
        # Filter open jobs
        open_jobs = {k: v for k, v in jobs.items() if v['status'] == 'Open'}
        
        if not open_jobs:
            ttk.Label(frame, text="No jobs available").pack(pady=20)
            return
        
        # Create treeview
        tree = ttk.Treeview(frame, columns=('Service', 'Budget', 'Timing', 'Location'), show='tree headings')
        tree.heading('#0', text='Description')
        tree.heading('Service', text='Service')
        tree.heading('Budget', text='Budget')
        tree.heading('Timing', text='Timing')
        tree.heading('Location', text='Location')
        
        for job_id, job in open_jobs.items():
            desc = job['description'][:30] + "..." if len(job['description']) > 30 else job['description']
            tree.insert('', 'end', text=desc, values=(job['service'], job['budget'], job['timing'], "Nairobi"))
        
        tree.pack(expand=True, fill='both', pady=10)
        
        def send_quote():
            selection = tree.selection()
            if not selection:
                messagebox.showwarning("Warning", "Please select a job")
                return
            
            self.show_quote_form(list(open_jobs.keys())[tree.index(selection[0])])
        
        ttk.Button(frame, text="Send Quote", command=send_quote).pack(pady=10)
    
    def show_quote_form(self, job_id):
        quote_window = tk.Toplevel(self.root)
        quote_window.title("Send Quote")
        quote_window.geometry("400x500")
        
        frame = ttk.Frame(quote_window, padding="20")
        frame.pack(expand=True, fill='both')
        
        ttk.Label(frame, text="Send Quote", font=('Arial', 16, 'bold')).pack(pady=10)
        
        # Quote amount
        ttk.Label(frame, text="Quote Amount (KSH):").pack(anchor='w')
        amount_entry = ttk.Entry(frame)
        amount_entry.pack(fill='x', pady=5)
        
        # Message
        ttk.Label(frame, text="Message to Client:").pack(anchor='w')
        message_text = tk.Text(frame, height=4)
        message_text.pack(fill='x', pady=5)
        
        # Availability
        ttk.Label(frame, text="Available to start:").pack(anchor='w')
        avail_var = tk.StringVar(value="Immediately")
        ttk.Radiobutton(frame, text="Immediately", variable=avail_var, value="Immediately").pack(anchor='w')
        ttk.Radiobutton(frame, text="Within 24 hours", variable=avail_var, value="24 hours").pack(anchor='w')
        ttk.Radiobutton(frame, text="Within a week", variable=avail_var, value="1 week").pack(anchor='w')
        
        def submit_quote():
            if not amount_entry.get().strip() or not message_text.get("1.0", tk.END).strip():
                messagebox.showerror("Error", "Please fill in amount and message")
                return
            
            # Load quotes
            with open(self.quotes_file, 'r') as f:
                quotes = json.load(f)
            
            quote_id = str(uuid.uuid4())[:8]
            quotes[quote_id] = {
                "id": quote_id,
                "job_id": job_id,
                "professional": self.current_user['email'],
                "amount": amount_entry.get().strip(),
                "message": message_text.get("1.0", tk.END).strip(),
                "availability": avail_var.get(),
                "status": "Sent",
                "created": datetime.now().isoformat()
            }
            
            with open(self.quotes_file, 'w') as f:
                json.dump(quotes, f)
            
            messagebox.showinfo("Success", "Quote sent successfully!")
            quote_window.destroy()
        
        ttk.Button(frame, text="Send Quote", command=submit_quote).pack(pady=20)
    
    def show_my_quotes(self):
        quotes_window = tk.Toplevel(self.root)
        quotes_window.title("My Quotes")
        quotes_window.geometry("700x400")
        
        frame = ttk.Frame(quotes_window, padding="20")
        frame.pack(expand=True, fill='both')
        
        ttk.Label(frame, text="My Quotes", font=('Arial', 16, 'bold')).pack(pady=10)
        
        # Load quotes
        with open(self.quotes_file, 'r') as f:
            quotes = json.load(f)
        
        # Filter user's quotes
        user_quotes = {k: v for k, v in quotes.items() if v['professional'] == self.current_user['email']}
        
        if not user_quotes:
            ttk.Label(frame, text="No quotes sent yet").pack(pady=20)
            return
        
        # Create treeview
        tree = ttk.Treeview(frame, columns=('Amount', 'Status', 'Availability', 'Date'), show='tree headings')
        tree.heading('#0', text='Job ID')
        tree.heading('Amount', text='Amount (KSH)')
        tree.heading('Status', text='Status')
        tree.heading('Availability', text='Availability')
        tree.heading('Date', text='Date')
        
        for quote_id, quote in user_quotes.items():
            date = datetime.fromisoformat(quote['created']).strftime('%Y-%m-%d')
            tree.insert('', 'end', text=quote['job_id'],
                       values=(quote['amount'], quote['status'], quote['availability'], date))
        
        tree.pack(expand=True, fill='both', pady=10)
    
    def show_my_jobs(self):
        jobs_window = tk.Toplevel(self.root)
        jobs_window.title("My Jobs")
        jobs_window.geometry("700x400")
        
        frame = ttk.Frame(jobs_window, padding="20")
        frame.pack(expand=True, fill='both')
        
        ttk.Label(frame, text="My Posted Jobs", font=('Arial', 16, 'bold')).pack(pady=10)
        
        # Load jobs
        with open(self.jobs_file, 'r') as f:
            jobs = json.load(f)
        
        # Filter user's jobs
        user_jobs = {k: v for k, v in jobs.items() if v['client'] == self.current_user['email']}
        
        if not user_jobs:
            ttk.Label(frame, text="No jobs posted yet").pack(pady=20)
            return
        
        # Create treeview
        tree = ttk.Treeview(frame, columns=('Service', 'Budget', 'Status', 'Date'), show='tree headings')
        tree.heading('#0', text='Description')
        tree.heading('Service', text='Service')
        tree.heading('Budget', text='Budget')
        tree.heading('Status', text='Status')
        tree.heading('Date', text='Date')
        
        for job_id, job in user_jobs.items():
            desc = job['description'][:30] + "..." if len(job['description']) > 30 else job['description']
            date = datetime.fromisoformat(job['created']).strftime('%Y-%m-%d')
            tree.insert('', 'end', text=desc,
                       values=(job['service'], job['budget'], job['status'], date))
        
        tree.pack(expand=True, fill='both', pady=10)
        
        def view_quotes():
            selection = tree.selection()
            if not selection:
                messagebox.showwarning("Warning", "Please select a job")
                return
            
            job_id = list(user_jobs.keys())[tree.index(selection[0])]
            self.show_job_quotes(job_id)
        
        ttk.Button(frame, text="View Quotes", command=view_quotes).pack(pady=10)
    
    def show_job_quotes(self, job_id):
        quotes_window = tk.Toplevel(self.root)
        quotes_window.title("Job Quotes")
        quotes_window.geometry("600x400")
        
        frame = ttk.Frame(quotes_window, padding="20")
        frame.pack(expand=True, fill='both')
        
        ttk.Label(frame, text="Quotes for Job", font=('Arial', 16, 'bold')).pack(pady=10)
        
        # Load quotes
        with open(self.quotes_file, 'r') as f:
            quotes = json.load(f)
        
        # Filter quotes for this job
        job_quotes = {k: v for k, v in quotes.items() if v['job_id'] == job_id}
        
        if not job_quotes:
            ttk.Label(frame, text="No quotes received yet").pack(pady=20)
            return
        
        # Create treeview
        tree = ttk.Treeview(frame, columns=('Professional', 'Amount', 'Availability'), show='tree headings')
        tree.heading('#0', text='Message')
        tree.heading('Professional', text='Professional')
        tree.heading('Amount', text='Amount (KSH)')
        tree.heading('Availability', text='Availability')
        
        for quote_id, quote in job_quotes.items():
            message = quote['message'][:30] + "..." if len(quote['message']) > 30 else quote['message']
            tree.insert('', 'end', text=message,
                       values=(quote['professional'], quote['amount'], quote['availability']))
        
        tree.pack(expand=True, fill='both', pady=10)
        
        def accept_quote():
            selection = tree.selection()
            if not selection:
                messagebox.showwarning("Warning", "Please select a quote")
                return
            
            messagebox.showinfo("Success", "Quote accepted! Professional will be notified.")
            quotes_window.destroy()
        
        ttk.Button(frame, text="Accept Quote", command=accept_quote).pack(pady=10)
    
    def logout(self):
        self.current_user = None
        self.create_main_interface()
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = HireWiseApp()
    app.run()