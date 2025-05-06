import tkinter as tk
from tkinter import ttk, messagebox
import requests
from datetime import datetime

class WalletApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Digital Wallet System")
        self.root.geometry("800x600")
        self.token = None
        self.user = None
        
        # Configure styles
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TButton', font=('Arial', 10), padding=5)
        self.style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        self.style.configure('Header.TLabel', font=('Arial', 14, 'bold'))
        
        # Create main container
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Show login screen by default
        self.show_login_screen()
    
    def clear_frame(self):
        """Clear all widgets from the main frame"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()
    
    def show_login_screen(self):
        """Display the login screen"""
        self.clear_frame()
        
        header = ttk.Label(self.main_frame, text="Login to Your Wallet", style='Header.TLabel')
        header.pack(pady=20)
        
        # Login form
        form_frame = ttk.Frame(self.main_frame)
        form_frame.pack(pady=20)
        
        ttk.Label(form_frame, text="Username:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        self.username_entry = ttk.Entry(form_frame)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Password:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        self.password_entry = ttk.Entry(form_frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)
        
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(pady=10)
        
        login_btn = ttk.Button(button_frame, text="Login", command=self.login)
        login_btn.pack(side=tk.LEFT, padx=5)
        
        register_btn = ttk.Button(button_frame, text="Register", command=self.show_register_screen)
        register_btn.pack(side=tk.LEFT, padx=5)
    
    def show_register_screen(self):
        """Display the registration screen"""
        self.clear_frame()
        
        header = ttk.Label(self.main_frame, text="Create New Account", style='Header.TLabel')
        header.pack(pady=20)
        
        # Registration form
        form_frame = ttk.Frame(self.main_frame)
        form_frame.pack(pady=20)
        
        ttk.Label(form_frame, text="Username:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        self.reg_username_entry = ttk.Entry(form_frame)
        self.reg_username_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Password:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        self.reg_password_entry = ttk.Entry(form_frame, show="*")
        self.reg_password_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Email:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        self.reg_email_entry = ttk.Entry(form_frame)
        self.reg_email_entry.grid(row=2, column=1, padx=5, pady=5)
        
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(pady=10)
        
        register_btn = ttk.Button(button_frame, text="Register", command=self.register)
        register_btn.pack(side=tk.LEFT, padx=5)
        
        back_btn = ttk.Button(button_frame, text="Back to Login", command=self.show_login_screen)
        back_btn.pack(side=tk.LEFT, padx=5)
    
    def show_dashboard(self):
        """Display the main dashboard after login"""
        self.clear_frame()
        
        # Header with user info
        header_frame = ttk.Frame(self.main_frame)
        header_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(header_frame, text=f"Welcome, {self.user['username']}!", style='Header.TLabel').pack(side=tk.LEFT)
        ttk.Label(header_frame, text=f"Balance: ${self.user['balance']:.2f}", style='Header.TLabel').pack(side=tk.LEFT, padx=20)
        ttk.Button(header_frame, text="Logout", command=self.logout).pack(side=tk.RIGHT)
        
        # Navigation buttons
        nav_frame = ttk.Frame(self.main_frame)
        nav_frame.pack(pady=20)
        
        ttk.Button(nav_frame, text="Send Money", command=self.show_send_money_screen, width=20).pack(side=tk.LEFT, padx=10)
        ttk.Button(nav_frame, text="Pay Bill", command=self.show_pay_bill_screen, width=20).pack(side=tk.LEFT, padx=10)
        ttk.Button(nav_frame, text="View Transactions", command=self.show_transactions_screen, width=20).pack(side=tk.LEFT, padx=10)
        
        # Recent transactions (simplified)
        ttk.Label(self.main_frame, text="Recent Transactions", style='Header.TLabel').pack(pady=10)
        
        # Create a treeview widget
        columns = ("id", "type", "amount", "details", "date")
        self.transactions_tree = ttk.Treeview(self.main_frame, columns=columns, show="headings", height=10)
        
        # Define headings
        self.transactions_tree.heading("id", text="ID")
        self.transactions_tree.heading("type", text="Type")
        self.transactions_tree.heading("amount", text="Amount")
        self.transactions_tree.heading("details", text="Details")
        self.transactions_tree.heading("date", text="Date")
        
        # Set column widths
        self.transactions_tree.column("id", width=50)
        self.transactions_tree.column("type", width=100)
        self.transactions_tree.column("amount", width=100)
        self.transactions_tree.column("details", width=300)
        self.transactions_tree.column("date", width=150)
        
        self.transactions_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Load transactions
        self.load_transactions()
    
    def show_send_money_screen(self):
        """Display the send money screen"""
        self.clear_frame()
        
        header = ttk.Label(self.main_frame, text="Send Money", style='Header.TLabel')
        header.pack(pady=20)
        
        # Current balance
        ttk.Label(self.main_frame, text=f"Current Balance: ${self.user['balance']:.2f}").pack()
        
        # Send money form
        form_frame = ttk.Frame(self.main_frame)
        form_frame.pack(pady=20)
        
        ttk.Label(form_frame, text="Recipient:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        self.recipient_entry = ttk.Entry(form_frame)
        self.recipient_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Amount:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        self.amount_entry = ttk.Entry(form_frame)
        self.amount_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Note (Optional):").grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        self.note_entry = ttk.Entry(form_frame)
        self.note_entry.grid(row=2, column=1, padx=5, pady=5)
        
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(pady=10)
        
        send_btn = ttk.Button(button_frame, text="Send Money", command=self.send_money)
        send_btn.pack(side=tk.LEFT, padx=5)
        
        back_btn = ttk.Button(button_frame, text="Back to Dashboard", command=self.show_dashboard)
        back_btn.pack(side=tk.LEFT, padx=5)
    
    def show_pay_bill_screen(self):
        """Display the pay bill screen"""
        self.clear_frame()
        
        header = ttk.Label(self.main_frame, text="Pay Bill", style='Header.TLabel')
        header.pack(pady=20)
        
        # Current balance
        ttk.Label(self.main_frame, text=f"Current Balance: ${self.user['balance']:.2f}").pack()
        
        # Pay bill form
        form_frame = ttk.Frame(self.main_frame)
        form_frame.pack(pady=20)
        
        ttk.Label(form_frame, text="Bill Type:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        self.bill_type_entry = ttk.Entry(form_frame)
        self.bill_type_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Account Number:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        self.account_number_entry = ttk.Entry(form_frame)
        self.account_number_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Amount:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        self.bill_amount_entry = ttk.Entry(form_frame)
        self.bill_amount_entry.grid(row=2, column=1, padx=5, pady=5)
        
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(pady=10)
        
        pay_btn = ttk.Button(button_frame, text="Pay Bill", command=self.pay_bill)
        pay_btn.pack(side=tk.LEFT, padx=5)
        
        back_btn = ttk.Button(button_frame, text="Back to Dashboard", command=self.show_dashboard)
        back_btn.pack(side=tk.LEFT, padx=5)
    
    def show_transactions_screen(self):
        """Display the transactions screen"""
        self.clear_frame()
        
        header = ttk.Label(self.main_frame, text="Transaction History", style='Header.TLabel')
        header.pack(pady=20)
        
        # Create a treeview widget
        columns = ("id", "type", "amount", "details", "direction", "date")
        self.transactions_tree = ttk.Treeview(self.main_frame, columns=columns, show="headings", height=20)
        
        # Define headings
        self.transactions_tree.heading("id", text="ID")
        self.transactions_tree.heading("type", text="Type")
        self.transactions_tree.heading("amount", text="Amount")
        self.transactions_tree.heading("details", text="Details")
        self.transactions_tree.heading("direction", text="Direction")
        self.transactions_tree.heading("date", text="Date")
        
        # Set column widths
        self.transactions_tree.column("id", width=50)
        self.transactions_tree.column("type", width=100)
        self.transactions_tree.column("amount", width=100)
        self.transactions_tree.column("details", width=250)
        self.transactions_tree.column("direction", width=80)
        self.transactions_tree.column("date", width=150)
        
        self.transactions_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Back button
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(pady=10)
        
        back_btn = ttk.Button(button_frame, text="Back to Dashboard", command=self.show_dashboard)
        back_btn.pack()
        
        # Load transactions
        self.load_transactions()
    
    def login(self):
        """Handle login"""
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        try:
            response = requests.post(
                "http://localhost:8000/token",
                data={"username": username, "password": password}
            )
            self.token = response.json()["access_token"]
            self.fetch_user()
            self.show_dashboard()
        except Exception as e:
            messagebox.showerror("Login Failed", str(e))
    
    def register(self):
        """Handle registration"""
        username = self.reg_username_entry.get()
        password = self.reg_password_entry.get()
        email = self.reg_email_entry.get()
        
        try:
            requests.post(
                "http://localhost:8000/users/",
                json={"username": username, "password": password, "email": email}
            )
            messagebox.showinfo("Success", "Registration successful! Please login.")
            self.show_login_screen()
        except Exception as e:
            messagebox.showerror("Registration Failed", str(e))
    
    def fetch_user(self):
        """Fetch current user data"""
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(
            "http://localhost:8000/users/me/",
            headers=headers
        )
        self.user = response.json()
    
    def send_money(self):
        """Handle sending money"""
        recipient = self.recipient_entry.get()
        amount = self.amount_entry.get()
        note = self.note_entry.get()
        
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.post(
                "http://localhost:8000/send_money/",
                headers=headers,
                json={
                    "recipient": recipient,
                    "amount": float(amount),
                    "note": note
                }
            )
            messagebox.showinfo("Success", "Money sent successfully!")
            self.fetch_user()  # Refresh user data
            self.show_dashboard()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def pay_bill(self):
        """Handle paying a bill"""
        bill_type = self.bill_type_entry.get()
        account_number = self.account_number_entry.get()
        amount = self.bill_amount_entry.get()
        
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.post(
                "http://localhost:8000/pay_bill/",
                headers=headers,
                json={
                    "bill_type": bill_type,
                    "account_number": account_number,
                    "amount": float(amount)
                }
            )
            messagebox.showinfo("Success", "Bill paid successfully!")
            self.fetch_user()  # Refresh user data
            self.show_dashboard()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def load_transactions(self):
        """Load transactions into the treeview"""
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.get(
                "http://localhost:8000/transactions/",
                headers=headers
            )
            transactions = response.json()
            
            # Clear existing items
            for item in self.transactions_tree.get_children():
                self.transactions_tree.delete(item)
            
            # Add new items
            for tx in transactions:
                self.transactions_tree.insert("", tk.END, values=(
                    tx["id"],
                    tx["transaction_type"],
                    f"${tx['amount']:.2f}",
                    tx["details"],
                    tx["direction"],
                    tx["timestamp"]
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load transactions: {str(e)}")
    
    def logout(self):
        """Handle logout"""
        self.token = None
        self.user = None
        self.show_login_screen()

if __name__ == "__main__":
    root = tk.Tk()
    app = WalletApp(root)
    root.mainloop()