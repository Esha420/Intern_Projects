import tkinter as tk
from tkinter import ttk, messagebox
import requests
import os

BASE_URL = os.getenv("API_URL", "http://127.0.0.1:8000/wallet")

class WalletApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Digital Wallet GUI")
        self.username = None

        self.main_frame = ttk.Frame(root, padding=20)
        self.main_frame.grid(row=0, column=0, sticky="NSEW")

        self.create_login_ui()

    def create_login_ui(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        ttk.Label(self.main_frame, text="Username").grid(row=0, column=0, pady=5)
        self.username_entry = ttk.Entry(self.main_frame)
        self.username_entry.grid(row=0, column=1, pady=5)

        ttk.Label(self.main_frame, text="Password").grid(row=1, column=0, pady=5)
        self.password_entry = ttk.Entry(self.main_frame, show="*")
        self.password_entry.grid(row=1, column=1, pady=5)

        ttk.Button(self.main_frame, text="Login", command=self.login).grid(row=2, column=0, pady=10)
        ttk.Button(self.main_frame, text="Register", command=self.register).grid(row=2, column=1, pady=10)

    def create_wallet_ui(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        ttk.Label(self.main_frame, text=f"Welcome {self.username}!").grid(row=0, column=0, columnspan=2, pady=10)

        # Send money
        ttk.Label(self.main_frame, text="Receiver Username").grid(row=1, column=0)
        self.receiver_entry = ttk.Entry(self.main_frame)
        self.receiver_entry.grid(row=1, column=1)

        ttk.Label(self.main_frame, text="Amount").grid(row=2, column=0)
        self.amount_entry = ttk.Entry(self.main_frame)
        self.amount_entry.grid(row=2, column=1)

        ttk.Label(self.main_frame, text="Note").grid(row=3, column=0)
        self.note_entry = ttk.Entry(self.main_frame)
        self.note_entry.grid(row=3, column=1)

        ttk.Button(self.main_frame, text="Send Money", command=self.send_money).grid(row=4, column=0, columnspan=2, pady=10)

        # Pay bill
        ttk.Label(self.main_frame, text="Bill Details").grid(row=5, column=0)
        self.bill_details = ttk.Entry(self.main_frame)
        self.bill_details.grid(row=5, column=1)

        ttk.Label(self.main_frame, text="Bill Amount").grid(row=6, column=0)
        self.bill_amount = ttk.Entry(self.main_frame)
        self.bill_amount.grid(row=6, column=1)

        ttk.Button(self.main_frame, text="Pay Bill", command=self.pay_bill).grid(row=7, column=0, columnspan=2, pady=10)

        ttk.Button(self.main_frame, text="Transaction History", command=self.transaction_history).grid(row=8, column=0, columnspan=2, pady=10)

        ttk.Button(self.main_frame, text="Logout", command=self.create_login_ui).grid(row=9, column=0, columnspan=2, pady=10)

    def login(self):
        data = {
            "username": self.username_entry.get(),
            "password": self.password_entry.get()
        }
        try:
            res = requests.post(f"{BASE_URL}/login", json=data)
            if res.status_code == 200:
                self.username = data['username']
                self.create_wallet_ui()
            else:
                messagebox.showerror("Login Failed", res.json()['detail'])
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def register(self):
        def do_register():
            data = {
                "username": self.username_entry.get(),
                "password": self.password_entry.get(),
                "tier": tier_var.get()
            }
            try:
                res = requests.post(f"{BASE_URL}/register", json=data)
                if res.status_code == 200:
                    messagebox.showinfo("Success", "Registered successfully! Please login.")
                else:
                    messagebox.showerror("Error", res.json()['detail'])
            except Exception as e:
                messagebox.showerror("Error", str(e))

        register_win = tk.Toplevel(self.root)
        register_win.title("Select Tier")
        tier_var = tk.StringVar(value="Gold")
        for i, tier in enumerate(["Gold", "Platinum", "Diamond"]):
            ttk.Radiobutton(register_win, text=tier, variable=tier_var, value=tier).grid(row=i, column=0)
        ttk.Button(register_win, text="Submit", command=lambda: [do_register(), register_win.destroy()]).grid(row=3, column=0)

    def send_money(self):
        data = {
            "receiver_username": self.receiver_entry.get(),
            "amount": float(self.amount_entry.get()),
            "type": "Send Money",
            "details": self.note_entry.get()
        }
        try:
            res = requests.post(f"{BASE_URL}/send", params={"username": self.username}, json=data)
            if res.status_code == 200:
                messagebox.showinfo("Success", "Money sent!")
            else:
                messagebox.showerror("Error", res.json()['detail'])
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def pay_bill(self):
        data = {
            "amount": float(self.bill_amount.get()),
            "type": "Pay Bill",
            "details": self.bill_details.get()
        }
        try:
            res = requests.post(f"{BASE_URL}/pay", params={"username": self.username}, json=data)
            if res.status_code == 200:
                messagebox.showinfo("Success", "Bill paid!")
            else:
                messagebox.showerror("Error", res.json()['detail'])
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def transaction_history(self):
        try:
            res = requests.get(f"{BASE_URL}/history", params={"username": self.username})
            if res.status_code == 200:
                history = res.json()
                history_text = "\n".join([
                    f"{t['timestamp']} - {t['type']} - {t['amount']} ({t['details']})" for t in history
                ])
                messagebox.showinfo("Transaction History", history_text or "No transactions found.")
            else:
                messagebox.showerror("Error", res.json()['detail'])
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = WalletApp(root)
    root.mainloop()
