import tkinter as tk
from tkinter import ttk, messagebox
import random
from datetime import datetime

class DigitalWallet:
    def __init__(self, root):
        self.root = root
        self.root.title("Digital Wallet")
        self.root.geometry("700x600")
        
        # User data
        self.users = {
            "user1": {"password": "pass1", "tier": "Basic", "balance": 1000.00},
            "user2": {"password": "pass2", "tier": "Premium", "balance": 5000.00},
            "user3": {"password": "pass3", "tier": "Business", "balance": 10000.00}
        }
        
        # Transaction types
        self.transaction_types = ["Send Money", "Pay Bill", "View History"]
        
        # Bill types
        self.bill_types = ["Electricity", "Water", "Internet", "Phone"]
        
        # Transaction history (stores all transactions)
        self.transaction_history = []
        
        # Current user
        self.current_user = None
        
        # Create login frame
        self.create_login_frame()
    
    def create_login_frame(self):
        self.clear_frame()
        
        self.login_frame = ttk.Frame(self.root, padding="20")
        self.login_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(self.login_frame, text="Username:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.username_entry = ttk.Entry(self.login_frame)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(self.login_frame, text="Password:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.password_entry = ttk.Entry(self.login_frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)
        
        login_button = ttk.Button(self.login_frame, text="Login", command=self.login)
        login_button.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Set focus to username entry
        self.username_entry.focus()
    
    def create_main_frame(self):
        self.clear_frame()
        
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # User info
        user_info = f"Welcome, {self.current_user} ({self.users[self.current_user]['tier']} Tier)"
        ttk.Label(self.main_frame, text=user_info, font=('Arial', 12, 'bold')).pack(pady=10)
        
        # Balance
        balance_info = f"Balance: ${self.users[self.current_user]['balance']:.2f}"
        self.balance_label = ttk.Label(self.main_frame, text=balance_info, font=('Arial', 12))
        self.balance_label.pack(pady=5)
        
        # Transaction type selection
        ttk.Label(self.main_frame, text="Select Transaction Type:").pack(pady=5)
        
        self.transaction_var = tk.StringVar()
        transaction_menu = ttk.OptionMenu(self.main_frame, self.transaction_var, 
                                         self.transaction_types[0], *self.transaction_types)
        transaction_menu.pack(pady=5)
        
        # Transaction frame (will be populated based on selection)
        self.transaction_frame = ttk.Frame(self.main_frame)
        self.transaction_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Bind the transaction type change
        self.transaction_var.trace('w', self.update_transaction_frame)
        
        # Initial frame update
        self.update_transaction_frame()
        
        # Logout button
        ttk.Button(self.main_frame, text="Logout", command=self.create_login_frame).pack(pady=10)
    
    def update_transaction_frame(self, *args):
        # Clear the transaction frame
        for widget in self.transaction_frame.winfo_children():
            widget.destroy()
        
        transaction_type = self.transaction_var.get()
        
        if transaction_type == "Send Money":
            self.create_send_money_frame()
        elif transaction_type == "Pay Bill":
            self.create_pay_bill_frame()
        elif transaction_type == "View History":
            self.create_view_history_frame()
    
    def create_send_money_frame(self):
        ttk.Label(self.transaction_frame, text="Recipient:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.recipient_entry = ttk.Entry(self.transaction_frame)
        self.recipient_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(self.transaction_frame, text="Amount:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.amount_entry = ttk.Entry(self.transaction_frame)
        self.amount_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(self.transaction_frame, text="Note:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.note_entry = ttk.Entry(self.transaction_frame)
        self.note_entry.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Button(self.transaction_frame, text="Send", command=self.process_send_money).grid(row=3, column=0, columnspan=2, pady=10)
    
    def create_pay_bill_frame(self):
        ttk.Label(self.transaction_frame, text="Bill Type:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        
        self.bill_type_var = tk.StringVar()
        bill_menu = ttk.OptionMenu(self.transaction_frame, self.bill_type_var, 
                                  self.bill_types[0], *self.bill_types)
        bill_menu.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        
        ttk.Label(self.transaction_frame, text="Account Number:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.account_entry = ttk.Entry(self.transaction_frame)
        self.account_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(self.transaction_frame, text="Amount:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.bill_amount_entry = ttk.Entry(self.transaction_frame)
        self.bill_amount_entry.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Button(self.transaction_frame, text="Pay Bill", command=self.process_pay_bill).grid(row=3, column=0, columnspan=2, pady=10)
    
    def create_view_history_frame(self):
        # Create a frame for the history display
        history_frame = ttk.Frame(self.transaction_frame)
        history_frame.pack(fill=tk.BOTH, expand=True)
        
        # Add a scrollbar
        scrollbar = ttk.Scrollbar(history_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create a treeview to display transactions
        self.history_tree = ttk.Treeview(
            history_frame,
            columns=("ID", "Type", "Amount", "Details", "Date"),
            show="headings",
            yscrollcommand=scrollbar.set
        )
        
        # Configure columns
        self.history_tree.heading("ID", text="Transaction ID")
        self.history_tree.heading("Type", text="Type")
        self.history_tree.heading("Amount", text="Amount")
        self.history_tree.heading("Details", text="Details")
        self.history_tree.heading("Date", text="Date")
        
        self.history_tree.column("ID", width=100)
        self.history_tree.column("Type", width=100)
        self.history_tree.column("Amount", width=100)
        self.history_tree.column("Details", width=200)
        self.history_tree.column("Date", width=150)
        
        self.history_tree.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.history_tree.yview)
        
        # Filter buttons frame
        filter_frame = ttk.Frame(self.transaction_frame)
        filter_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(filter_frame, text="All Transactions", 
                  command=lambda: self.filter_history("All")).pack(side=tk.LEFT, padx=5)
        ttk.Button(filter_frame, text="Sent Money", 
                  command=lambda: self.filter_history("Send Money")).pack(side=tk.LEFT, padx=5)
        ttk.Button(filter_frame, text="Received Money", 
                  command=lambda: self.filter_history("Receive Money")).pack(side=tk.LEFT, padx=5)
        ttk.Button(filter_frame, text="Bill Payments", 
                  command=lambda: self.filter_history("Pay Bill")).pack(side=tk.LEFT, padx=5)
        
        # Load the history
        self.load_history()
    
    def load_history(self, filter_type="All"):
        # Clear the treeview
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        # Add transactions to the treeview
        for transaction in self.transaction_history:
            # Only show transactions where the current user is the main user
            if transaction["user"] == self.current_user:
                if filter_type == "All" or transaction["type"] == filter_type:
                    amount_display = f"${transaction['amount']:.2f}"
                    if transaction.get("direction") == "out":
                        amount_display = f"-{amount_display}"
                    elif transaction.get("direction") == "in":
                        amount_display = f"+{amount_display}"
                    
                    self.history_tree.insert("", tk.END, values=(
                        transaction["id"],
                        transaction["type"],
                        amount_display,
                        transaction["details"],
                        transaction["date"]
                    ))
    
    def filter_history(self, filter_type):
        self.load_history(filter_type)
    
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if username in self.users and self.users[username]["password"] == password:
            self.current_user = username
            self.create_main_frame()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")
    
    def process_send_money(self):
        try:
            recipient = self.recipient_entry.get()
            amount = float(self.amount_entry.get())
            note = self.note_entry.get()
            
            if recipient not in self.users:
                messagebox.showerror("Error", "Recipient not found")
                return
            
            if amount <= 0:
                messagebox.showerror("Error", "Amount must be positive")
                return
                
            user_balance = self.users[self.current_user]["balance"]
            
            # Check if user has sufficient balance
            if amount > user_balance:
                messagebox.showerror("Error", "Insufficient balance")
                return
            
            # Apply tier-based transaction limits
            tier = self.users[self.current_user]["tier"]
            if tier == "Basic" and amount > 500:
                messagebox.showerror("Error", "Basic tier limit: $500 per transaction")
                return
            elif tier == "Premium" and amount > 2000:
                messagebox.showerror("Error", "Premium tier limit: $2000 per transaction")
                return
            
            # Process transaction
            self.users[self.current_user]["balance"] -= amount
            self.users[recipient]["balance"] += amount
            
            # Update balance display
            self.update_balance()
            
            # Generate transaction ID
            transaction_id = ''.join(random.choices('0123456789ABCDEF', k=8))
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Record sender's transaction
            self.record_transaction(
                transaction_id,
                "Send Money",
                amount,
                f"To: {recipient}, Note: {note}",
                current_time,
                direction="out"
            )
            
            # Record recipient's transaction (with recipient as the user)
            self.record_transaction(
                transaction_id,
                "Receive Money",
                amount,
                f"From: {self.current_user}, Note: {note}",
                current_time,
                user=recipient,
                direction="in"
            )
            
            messagebox.showinfo("Success", 
                              f"Transaction successful!\n"
                              f"Transaction ID: {transaction_id}\n"
                              f"Sent ${amount:.2f} to {recipient}\n"
                              f"Note: {note}")
            
            # Clear fields
            self.recipient_entry.delete(0, tk.END)
            self.amount_entry.delete(0, tk.END)
            self.note_entry.delete(0, tk.END)
            
        except ValueError:
            messagebox.showerror("Error", "Invalid amount")
    
    def process_pay_bill(self):
        try:
            bill_type = self.bill_type_var.get()
            account = self.account_entry.get()
            amount = float(self.bill_amount_entry.get())
            
            if amount <= 0:
                messagebox.showerror("Error", "Amount must be positive")
                return
                
            user_balance = self.users[self.current_user]["balance"]
            
            # Check if user has sufficient balance
            if amount > user_balance:
                messagebox.showerror("Error", "Insufficient balance")
                return
            
            # Process bill payment
            self.users[self.current_user]["balance"] -= amount
            
            # Update balance display
            self.update_balance()
            
            # Generate payment ID
            payment_id = ''.join(random.choices('0123456789ABCDEF', k=8))
            
            # Record transaction
            self.record_transaction(
                payment_id,
                "Pay Bill",
                amount,
                f"Bill: {bill_type}, Account: {account}",
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                direction="out"
            )
            
            messagebox.showinfo("Payment Successful", 
                              f"Bill payment processed!\n"
                              f"Payment ID: {payment_id}\n"
                              f"Bill Type: {bill_type}\n"
                              f"Account: {account}\n"
                              f"Amount: ${amount:.2f}")
            
            # Clear fields
            self.account_entry.delete(0, tk.END)
            self.bill_amount_entry.delete(0, tk.END)
            
        except ValueError:
            messagebox.showerror("Error", "Invalid amount")
    
    def record_transaction(self, transaction_id, transaction_type, amount, details, date, 
                         user=None, direction=None):
        """Record a transaction in the history"""
        if user is None:
            user = self.current_user
            
        self.transaction_history.append({
            "id": transaction_id,
            "user": user,
            "type": transaction_type,
            "amount": amount,
            "details": details,
            "date": date,
            "direction": direction
        })
    
    def update_balance(self):
        balance_info = f"Balance: ${self.users[self.current_user]['balance']:.2f}"
        self.balance_label.config(text=balance_info)
    
    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = DigitalWallet(root)
    root.mainloop()