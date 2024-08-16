import tkinter as tk
from tkinter import messagebox, simpledialog
import pandas as pd
import os

# Define your Bankaccount class here if it's not already defined
class Bankaccount:
    def __init__(self, account_number, balance, date_of_opening, customer_name):
        self.account_number = account_number
        self.balance = balance
        self.date_of_opening = date_of_opening
        self.customer_name = customer_name
    
    def deposit(self, amount):
        self.balance += amount
        
    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("Insufficient balance")
        else:
            self.balance -= amount
            return amount, self.balance
    
    def check_balance(self):
        return self.balance
    
    def print_details(self):
        print("Customer name:", self.customer_name)
        print("Account number:", self.account_number)
        print("Balance:", self.balance)
        print("Opening date:", self.date_of_opening)

class BankAccountGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Bank Account Management")
        
        # Define colors
        self.bg_color = "#e0f7fa"  # cyan light
        self.button_color = "#00796b"  # teal dark
        self.label_color = "#004d40"  # teal very dark
        self.entry_bg_color = "#ffffff"  # white
        self.entry_fg_color = "#000000"  # black
        
        # Set full screen
        self.root.attributes('-fullscreen', True)
        self.root.bind("<Escape>", self.exit_full_screen)
        
        # Create a frame in the center
        self.frame = tk.Frame(root, bg=self.bg_color)
        self.frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Create labels
        self.label_customer_name = tk.Label(self.frame, text="Customer Name:", bg=self.bg_color, fg=self.label_color)
        self.label_customer_name.grid(row=0, column=0, padx=10, pady=10)
        
        self.label_account_number = tk.Label(self.frame, text="Account Number:", bg=self.bg_color, fg=self.label_color)
        self.label_account_number.grid(row=1, column=0, padx=10, pady=10)
        
        self.label_balance = tk.Label(self.frame, text="Balance:", bg=self.bg_color, fg=self.label_color)
        self.label_balance.grid(row=2, column=0, padx=10, pady=10)
        
        # Create entry fields
        self.entry_customer_name = tk.Entry(self.frame, width=30, bg=self.entry_bg_color, fg=self.entry_fg_color)
        self.entry_customer_name.grid(row=0, column=1, padx=10, pady=10)
        
        self.entry_account_number = tk.Entry(self.frame, width=30, bg=self.entry_bg_color, fg=self.entry_fg_color)
        self.entry_account_number.grid(row=1, column=1, padx=10, pady=10)
        
        self.entry_balance = tk.Entry(self.frame, width=30, bg=self.entry_bg_color, fg=self.entry_fg_color)
        self.entry_balance.grid(row=2, column=1, padx=10, pady=10)
        
        # Create buttons
        self.button_create_account = tk.Button(self.frame, text="Create Account", bg=self.button_color, fg="white", command=self.create_account)
        self.button_create_account.grid(row=3, columnspan=2, padx=10, pady=10, sticky="we")
        
        # Create transaction section
        self.label_transaction_account_number = tk.Label(self.frame, text="Account Number:", bg=self.bg_color, fg=self.label_color)
        self.label_transaction_account_number.grid(row=4, column=0, padx=10, pady=10)
        
        self.entry_transaction_account_number = tk.Entry(self.frame, width=30, bg=self.entry_bg_color, fg=self.entry_fg_color)
        self.entry_transaction_account_number.grid(row=4, column=1, padx=10, pady=10)
        
        self.button_deposit_transaction = tk.Button(self.frame, text="Deposit", bg=self.button_color, fg="white", command=self.deposit_transaction)
        self.button_deposit_transaction.grid(row=5, column=0, padx=10, pady=10, sticky="we")
        
        self.button_withdraw_transaction = tk.Button(self.frame, text="Withdraw", bg=self.button_color, fg="white", command=self.withdraw_transaction)
        self.button_withdraw_transaction.grid(row=5, column=1, padx=10, pady=10, sticky="we")
        
        self.button_check_balance_transaction = tk.Button(self.frame, text="Check Balance", bg=self.button_color, fg="white", command=self.check_balance_transaction)
        self.button_check_balance_transaction.grid(row=6, columnspan=2, padx=10, pady=10, sticky="we")
        
        # Initialize Bankaccount instance and account number set
        self.account = None
        self.existing_account_numbers = self.load_existing_account_numbers()
    
    def load_existing_account_numbers(self):
        if os.path.exists("bank_accounts.xlsx"):
            df = pd.read_excel("bank_accounts.xlsx")
            return set(df["Account Number"].astype(str))
        return set()
    
    def create_account(self):
        customer_name = self.entry_customer_name.get()
        account_number = self.entry_account_number.get()
        balance = self.entry_balance.get()
        
        if account_number in self.existing_account_numbers:
            messagebox.showerror("Error", "Account number already exists. Please enter a unique account number.")
            return
        
        try:
            balance = float(balance)
            self.account = Bankaccount(account_number, balance, "10-11-2010", customer_name)
            self.save_account_to_excel()
            self.existing_account_numbers.add(account_number)
            self.clear_input_fields()
            messagebox.showinfo("Account Created", "Account created successfully!")
        except ValueError:
            messagebox.showerror("Error", "Invalid balance amount. Please enter a valid number.")
    
    def save_account_to_excel(self):
        data = {
            "Customer Name": [self.account.customer_name],
            "Account Number": [self.account.account_number],
            "Balance": [self.account.balance],
            "Date of Opening": [self.account.date_of_opening]
        }
        df = pd.DataFrame(data)
        try:
            existing_df = pd.read_excel("bank_accounts.xlsx")
            df = pd.concat([existing_df, df], ignore_index=True)
        except FileNotFoundError:
            pass
        df.to_excel("bank_accounts.xlsx", index=False)
    
    def clear_input_fields(self):
        self.entry_customer_name.delete(0, tk.END)
        self.entry_account_number.delete(0, tk.END)
        self.entry_balance.delete(0, tk.END)
    
    def deposit_transaction(self):
        account_number = self.entry_transaction_account_number.get()
        if account_number:
            amount = simpledialog.askfloat("Deposit", "Enter amount to deposit:")
            if amount is not None:
                df = pd.read_excel("bank_accounts.xlsx")
                account_row = df[df["Account Number"] == int(account_number)]
                if not account_row.empty:
                    current_balance = account_row["Balance"].values[0]
                    new_balance = current_balance + amount
                    df.loc[df["Account Number"] == int(account_number), "Balance"] = new_balance
                    df.to_excel("bank_accounts.xlsx", index=False)
                    messagebox.showinfo("Deposit", f"${amount} deposited successfully!\nNew balance: ${new_balance}")
                else:
                    messagebox.showerror("Error", "Account number not found.")
    
    def withdraw_transaction(self):
        account_number = self.entry_transaction_account_number.get()
        if account_number:
            amount = simpledialog.askfloat("Withdraw", "Enter amount to withdraw:")
            if amount is not None:
                df = pd.read_excel("bank_accounts.xlsx")
                account_row = df[df["Account Number"] == int(account_number)]
                if not account_row.empty:
                    current_balance = account_row["Balance"].values[0]
                    if amount > current_balance:
                        messagebox.showerror("Error", "Insufficient balance")
                    else:
                        new_balance = current_balance - amount
                        df.loc[df["Account Number"] == int(account_number), "Balance"] = new_balance
                        df.to_excel("bank_accounts.xlsx", index=False)
                        messagebox.showinfo("Withdraw", f"${amount} withdrawn successfully!\nRemaining balance: ${new_balance}")
                else:
                    messagebox.showerror("Error", "Account number not found.")
    
    def check_balance_transaction(self):
        account_number = self.entry_transaction_account_number.get()
        if account_number:
            df = pd.read_excel("bank_accounts.xlsx")
            account_row = df[df["Account Number"] == int(account_number)]
            if not account_row.empty:
                balance = account_row["Balance"].values[0]
                messagebox.showinfo("Balance", f"Current balance: ${balance}")
            else:
                messagebox.showerror("Error", "Account number not found.")
    
    def exit_full_screen(self, event):
        self.root.attributes('-fullscreen', False)

if __name__ == "__main__":
    root = tk.Tk()
    app = BankAccountGUI(root)
    root.mainloop()
