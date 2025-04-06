import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import mysql.connector
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime


LOGO_PATH = r"C:\Users\Ziad\Desktop\lucerne_logo.jpg"


def connect_to_db():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",  # Replace with your database password
            database="lucerne_boutique"
        )
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"Error connecting to database: {e}")
        return None


# Validate Login
def validate_login(user_id, password):
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT Password, Role FROM Users WHERE User_ID = %s", (user_id,))
            result = cursor.fetchone()
            if result:
                stored_password, role = result
                if password == stored_password:
                    return role
            return None
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Error fetching user: {e}")
        finally:
            conn.close()
    return None


# Login Function
def login():
    user_id = entry_id.get()
    password = entry_password.get()
    role = validate_login(user_id, password)
    if role:
        messagebox.showinfo("Login Success", f"Welcome, {role}!")
        root.withdraw()  # Hide the main window instead of destroying it
        if role == "Manager":
            manager_dashboard()  # Open the Manager dashboard
        elif role == "Employee":
            employee_dashboard()  # Open the Employee dashboard
    else:
        messagebox.showerror("Login Failed", "Invalid ID or password.")




# Open Sign-Up Screen (Manager Only)
def open_signup():
    def confirm_manager():
        manager_id = manager_id_entry.get()
        manager_password = manager_password_entry.get()
        role = validate_login(manager_id, manager_password)
        if role == "Manager":
            signup_window.deiconify()  # Show the signup window
            manager_confirm_window.destroy()  # Close the confirmation window
        else:
            messagebox.showerror("Access Denied", "Only managers can add new users.")

    # Manager Confirmation Window
    manager_confirm_window = tk.Toplevel(root)
    manager_confirm_window.title("Confirm Manager")
    manager_confirm_window.geometry("400x200")
    manager_confirm_window.configure(bg="#00796b")

    tk.Label(manager_confirm_window, text="Manager ID:", bg="#00796b", fg="white", font=("Segoe UI", 12)).pack(pady=5)
    manager_id_entry = ttk.Entry(manager_confirm_window, font=("Segoe UI", 12))
    manager_id_entry.pack(pady=5)

    tk.Label(manager_confirm_window, text="Password:", bg="#00796b", fg="white", font=("Segoe UI", 12)).pack(pady=5)
    manager_password_entry = ttk.Entry(manager_confirm_window, show="*", font=("Segoe UI", 12))
    manager_password_entry.pack(pady=5)

    ttk.Button(manager_confirm_window, text="Confirm", command=confirm_manager).pack(pady=10)
    ttk.Button(manager_confirm_window, text="Cancel", command=manager_confirm_window.destroy).pack(pady=5)


# Sign-Up Function
# Sign-Up Function
def signup_user():
    user_id = signup_id_entry.get()
    password = signup_password_entry.get()
    role = role_combobox.get()

    if not (user_id and password and role):
        messagebox.showerror("Input Error", "All fields are required!")
        return

    # Check if the role is valid
    if role not in ["Manager", "Employee"]:
        messagebox.showerror("Input Error", "Invalid role selected!")
        return

    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM Users WHERE User_ID = %s", (user_id,))
            exists = cursor.fetchone()[0]

            # Check if User_ID already exists
            if exists:
                messagebox.showerror("Input Error", "User ID already exists!")
                conn.close()
                return

            # Insert the new user into the database
            cursor.execute(
                "INSERT INTO Users (User_ID, Password, Role) VALUES (%s, %s, %s)",
                (user_id, password, role)
            )
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "User added successfully!")
            signup_window.withdraw()  # Hide the sign-up window after success
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Error adding user: {e}")
def employee_dashboard():
    dashboard = tk.Toplevel(root)
    dashboard.title("Employee Dashboard")
    dashboard.geometry("1300x700")
    dashboard.configure(bg="white")

    # Left Menu Frame (same as Manager Dashboard)
    menu_frame = tk.Frame(dashboard, bg="#00796b", width=400)
    menu_frame.pack(side="left", fill="y")

    def open_products():
        open_products_module(dashboard)
        
    def open_discounts():
        open_discounts_module(dashboard)



    def open_product_sales():
        open_product_sales_module(dashboard)


    # Add Buttons to Left Menu (same as Manager)
    style = ttk.Style()
    style.configure("CustomButton.TButton", padding=(10, 20), font=("Segoe UI", 10))

    # Add Buttons to Left Menu with the new style
    tk.Label(menu_frame, text="Menu", bg="#00796b", fg="white", font=("Segoe UI", 18, "bold")).pack(pady=10)
    ttk.Button(menu_frame, text="Products", command=open_products, style="CustomButton.TButton").pack(pady=10, fill="x")
    ttk.Button(menu_frame, text="Product Sales", command=open_product_sales, style="CustomButton.TButton").pack(pady=10, fill="x")
    ttk.Button(menu_frame, text="Discounts", command=open_discounts, style="CustomButton.TButton").pack(pady=10, fill="x")  # New Discounts Button
    tk.Button(menu_frame,text="Logout",bg="black",  fg="white",  font=("Segoe UI", 12, "bold"),  command=lambda: exit_to_login(dashboard)).pack(pady=10, fill="x")  # Add padding and make it fill horizontally

    # Display the Product Sales content by default
    open_product_sales_module(dashboard)

# Manager Dashboard
def fetch_dashboard_data():
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)

            # Total Employees
            cursor.execute("SELECT COUNT(*) AS total_employees FROM Users WHERE Role = 'Employee'")
            total_employees = cursor.fetchone()["total_employees"]

            # Total Customers
            cursor.execute("SELECT COUNT(*) AS total_customers FROM Customers")
            total_customers = cursor.fetchone()["total_customers"]

            # Total Products
            cursor.execute("SELECT COUNT(*) AS total_products FROM Products")
            total_products = cursor.fetchone()["total_products"]

            # Out of Stock
            cursor.execute("SELECT COUNT(*) AS out_of_stock FROM Inventory WHERE Quantity_In_Stock = 0")
            out_of_stock = cursor.fetchone()["out_of_stock"]

            conn.close()
            return total_employees, total_customers, total_products, out_of_stock
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Error fetching dashboard data: {e}")
    return 0, 0, 0, 0

# Manager Dashboard
# Manager Dashboard
# Manager Dashboard
def manager_dashboard():
    dashboard = tk.Toplevel(root)
    dashboard.title("Dashboard")
    dashboard.geometry("1300x1300")
    dashboard.configure(bg="white")

    # Left Menu Frame
    menu_frame = tk.Frame(dashboard, bg="#00796b", width=400)
    menu_frame.pack(side="left", fill="y")

    def open_customers():
        open_customers_module(dashboard)

    def open_employees():
        open_employees_module(dashboard)

    def open_sales_transactions():
        open_sales_transactions_module(dashboard)

    def open_suppliers():
        open_suppliers_module(dashboard)

    def open_products():
        open_products_module(dashboard)

    def open_product_sales():
        open_product_sales_module(dashboard)

    def open_discounts():
        open_discounts_module(dashboard)
    # Add Buttons to Left Menu
    # Create a custom style for buttons
    style = ttk.Style()
    style.configure("CustomButton.TButton", padding=(10, 20), font=("Segoe UI", 10))

    # Add Buttons to Left Menu with the new style
    tk.Label(menu_frame, text="Menu", bg="#00796b", fg="white", font=("Segoe UI", 18, "bold")).pack(pady=10)
    ttk.Button(menu_frame, text="Dashboard", command=lambda: display_dashboard(dashboard),style="CustomButton.TButton").pack(pady=10, fill="x")
    ttk.Button(menu_frame, text="Customers", command=open_customers, style="CustomButton.TButton").pack(pady=10,fill="x")
    ttk.Button(menu_frame, text="Employees", command=open_employees, style="CustomButton.TButton").pack(pady=10,fill="x")
    ttk.Button(menu_frame, text="Sales Transactions", command=open_sales_transactions, style="CustomButton.TButton").pack(pady=10, fill="x")
    ttk.Button(menu_frame, text="Suppliers", command=open_suppliers, style="CustomButton.TButton").pack(pady=10,fill="x")
    ttk.Button(menu_frame, text="Products", command=open_products, style="CustomButton.TButton").pack(pady=10, fill="x")
    ttk.Button(menu_frame, text="Product Sales", command=open_product_sales, style="CustomButton.TButton").pack(pady=10,fill="x")
    ttk.Button(menu_frame, text="Discounts", command=open_discounts, style="CustomButton.TButton").pack(pady=10, fill="x")  # New Discounts Button
    tk.Button(menu_frame,text="Logout",bg="black",  fg="white",  font=("Segoe UI", 12, "bold"),  command=lambda: exit_to_login(dashboard)).pack(pady=10, fill="x")  # Add padding and make it fill horizontally

    # Display the dashboard content by default
    display_dashboard(dashboard)
def exit_to_login(dashboard):
    dashboard.destroy()  # Close the dashboard window
    root.deiconify()  # Show the login page again

# Product Sales Module
def open_product_sales_module(parent):
    for widget in parent.winfo_children():
        if isinstance(widget, tk.Frame) and widget != parent.children.get("!frame"):
            widget.destroy()

    content_frame = tk.Frame(parent, bg="white")
    content_frame.pack(side="right", expand=True, fill="both")

    tk.Label(content_frame, text="Product Sales", bg="white", fg="#00796b", font=("Segoe UI", 24, "bold")).pack(pady=20)

    # Table Frame
    table_frame = tk.Frame(content_frame, bg="white")
    table_frame.pack(fill="both", expand=True, padx=20, pady=10)

    columns = ("Transaction_ID", "Customer_ID", "Product_ID", "Product_Name", "Quantity", "Sale_Price", "Discount_ID", "Discount_Percentage", "Total")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
    tree.pack(fill="both", expand=True)

    tree.heading("Transaction_ID", text="Transaction ID")
    tree.heading("Customer_ID", text="Customer ID")  # New Column for Customer ID
    tree.heading("Product_ID", text="Product ID")
    tree.heading("Product_Name", text="Product Name")
    tree.heading("Quantity", text="Quantity")
    tree.heading("Sale_Price", text="Sale Price")
    tree.heading("Discount_ID", text="Discount ID")
    tree.heading("Discount_Percentage", text="Discount (%)")
    tree.heading("Total", text="Total")

    def fetch_product_sales():
        conn = connect_to_db()
        if conn:
            try:
                cursor = conn.cursor()
                query = """
                    SELECT ps.Transaction_ID, st.Customer_ID, ps.Product_ID, p.Name, ps.Quantity, ps.Sale_Price, 
                           ps.Discount_ID, ps.Discount_Percentage, ps.Total
                    FROM Product_Sales ps
                    JOIN Products p ON ps.Product_ID = p.Product_ID
                    JOIN Sales_Transactions st ON ps.Transaction_ID = st.Transaction_ID
                """
                cursor.execute(query)
                rows = cursor.fetchall()
                for row in tree.get_children():
                    tree.delete(row)
                for row in rows:
                    tree.insert("", "end", values=row)
                conn.close()
            except mysql.connector.Error as e:
                messagebox.showerror("Database Error", f"Error fetching product sales: {e}")

    fetch_product_sales()

    fetch_product_sales()

    # Input Frame for Product Sales
    input_frame = tk.Frame(content_frame, bg="white")
    input_frame.pack(fill="x", pady=10)

    tk.Label(input_frame, text="Customer ID:", bg="white", font=("Segoe UI", 12)).grid(row=0, column=0, padx=10, pady=5)
    customer_id_entry = ttk.Entry(input_frame, font=("Segoe UI", 12))
    customer_id_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(input_frame, text="Product ID:", bg="white", font=("Segoe UI", 12)).grid(row=1, column=0, padx=10, pady=5)
    product_id_entry = ttk.Entry(input_frame, font=("Segoe UI", 12))
    product_id_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(input_frame, text="Quantity:", bg="white", font=("Segoe UI", 12)).grid(row=2, column=0, padx=10, pady=5)
    quantity_entry = ttk.Entry(input_frame, font=("Segoe UI", 12))
    quantity_entry.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(input_frame, text="Discount ID:", bg="white", font=("Segoe UI", 12)).grid(row=3, column=0, padx=10, pady=5)
    discount_id_entry = ttk.Entry(input_frame, font=("Segoe UI", 12))  # Discount ID entry
    discount_id_entry.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(input_frame, text="Date:", bg="white", font=("Segoe UI", 12)).grid(row=4, column=0, padx=10, pady=5)
    sale_date_entry = ttk.Entry(input_frame, font=("Segoe UI", 12))  # Date entry field
    sale_date_entry.grid(row=4, column=1, padx=10, pady=5)
    from decimal import Decimal

    from datetime import datetime
    from decimal import Decimal

    def insert_product_sales():
        customer_id = customer_id_entry.get()
        product_id = product_id_entry.get()
        quantity = quantity_entry.get()
        discount_id = discount_id_entry.get() if discount_id_entry.get() else None
        sale_date = sale_date_entry.get()  # Get the date entered by the user

        # Validate required fields
        if not (customer_id and product_id and quantity):
            messagebox.showerror("Input Error", "Please provide all fields (Customer ID, Product ID, Quantity).")
            return

        # Convert sale_date to datetime if provided, else use current date
        if sale_date:
            try:
                sale_date = datetime.strptime(sale_date, '%Y-%m-%d').date()  # Convert to date object
            except ValueError:
                messagebox.showerror("Input Error", "Invalid date format! Please use YYYY-MM-DD.")
                return
        else:
            sale_date = datetime.now().date()  # Default to current date if not provided

        conn = connect_to_db()
        if conn:
            try:
                cursor = conn.cursor()
                # Fetch product details (price and stock level)
                cursor.execute("SELECT Price, Stock_Level FROM Products WHERE Product_ID = %s", (product_id,))
                product = cursor.fetchone()
                if product:
                    product_price, stock_level = product

                    # Check if stock level is 0
                    if stock_level == 0:
                        messagebox.showerror("Stock Error",
                                             "This product is out of stock. The sale cannot be processed.")
                        return

                    # Check if the requested quantity exceeds stock level
                    if int(quantity) > stock_level:
                        messagebox.showerror("Stock Error", "Insufficient stock for this product.")
                        return

                    product_price = Decimal(product_price)  # Convert to Decimal for accuracy
                    quantity = int(quantity)

                    # Apply discount logic
                    total_price = product_price * quantity  # Price before discount
                    discount_percentage = None  # Default value for discount percentage

                    if discount_id:
                        cursor.execute("SELECT Discount_Percentage, End_Date FROM Discounts WHERE Discount_ID = %s",
                                       (discount_id,))
                        discount = cursor.fetchone()
                        if discount:
                            discount_percentage = Decimal(discount[0])  # Convert to Decimal
                            discount_end_date = discount[1]

                            if sale_date <= discount_end_date:  # Valid discount
                                total_price -= total_price * (discount_percentage / Decimal(100))  # Apply discount
                            else:
                                messagebox.showerror("Input Error", "Discount ID has expired.")
                                return
                        else:
                            messagebox.showerror("Input Error", "Invalid Discount ID!")
                            return

                    # Insert Sales Transaction Record
                    cursor.execute(
                        "INSERT INTO Sales_Transactions (Customer_ID, Transaction_Date, Total_Amount) VALUES (%s, %s, %s)",
                        (customer_id, sale_date, total_price)
                    )
                    transaction_id = cursor.lastrowid  # Get the last inserted transaction ID

                    # Insert Product Sales Record (Add Customer_ID to this table)
                    cursor.execute(
                        "INSERT INTO Product_Sales (Transaction_ID, Customer_ID, Product_ID, Quantity, Sale_Price, Discount_ID, Discount_Percentage, Total) "
                        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                        (transaction_id, customer_id, product_id, quantity, product_price, discount_id,
                         discount_percentage,
                         total_price)
                    )

                    # Reduce Stock Level
                    cursor.execute(
                        "UPDATE Products SET Stock_Level = Stock_Level - %s WHERE Product_ID = %s",
                        (quantity, product_id)
                    )

                    conn.commit()
                    fetch_product_sales()  # Refresh the product sales table
                    customer_id_entry.delete(0, tk.END)
                    product_id_entry.delete(0, tk.END)
                    quantity_entry.delete(0, tk.END)
                    discount_id_entry.delete(0, tk.END)
                    sale_date_entry.delete(0, tk.END)
                    messagebox.showinfo("Success", "Product sales record added successfully!")
                else:
                    messagebox.showerror("Input Error", "Product ID not found!")
            except mysql.connector.Error as e:
                messagebox.showerror("Database Error", f"Error adding product sales: {e}")
            finally:
                conn.close()

    # Buttons
    tk.Button(input_frame, text="Insert", bg="#00796b", fg="white", command=insert_product_sales).grid(row=5, column=0, padx=10, pady=5)
    tk.Button(input_frame, text="Refresh", bg="#00796b", fg="white", command=fetch_product_sales).grid(row=5, column=1, padx=10, pady=5)


def open_suppliers_module(parent):
    # Clear previous widgets
    for widget in parent.winfo_children():
        if isinstance(widget, tk.Frame) and widget != parent.children.get("!frame"):
            widget.destroy()

    # Content Frame
    content_frame = tk.Frame(parent, bg="white")
    content_frame.pack(side="right", expand=True, fill="both")

    # Title
    tk.Label(content_frame, text="Suppliers Management", bg="white", fg="#00796b", font=("Segoe UI", 24, "bold")).pack(pady=20)

    # Table Frame
    table_frame = tk.Frame(content_frame, bg="white")
    table_frame.pack(fill="both", expand=True, padx=20, pady=10)

    columns = ("Supplier_ID", "Name", "Phone", "Address")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
    tree.pack(fill="both", expand=True)

    for col in columns:
        tree.heading(col, text=col)

    # Fetch Suppliers
    def fetch_suppliers():
        conn = connect_to_db()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT Supplier_ID, Name, Phone, Address FROM Suppliers")
                rows = cursor.fetchall()
                for row in tree.get_children():
                    tree.delete(row)
                for row in rows:
                    tree.insert("", "end", values=row)
                conn.close()
            except mysql.connector.Error as e:
                messagebox.showerror("Database Error", f"Error fetching suppliers: {e}")

    fetch_suppliers()

    # Input Frame
    input_frame = tk.Frame(content_frame, bg="white")
    input_frame.pack(fill="x", pady=10)

    tk.Label(input_frame, text="Supplier ID:", bg="white", font=("Segoe UI", 12)).grid(row=0, column=0, padx=10, pady=5)
    supplier_id_entry = ttk.Entry(input_frame, font=("Segoe UI", 12))
    supplier_id_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(input_frame, text="Name:", bg="white", font=("Segoe UI", 12)).grid(row=1, column=0, padx=10, pady=5)
    supplier_name_entry = ttk.Entry(input_frame, font=("Segoe UI", 12))
    supplier_name_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(input_frame, text="Phone:", bg="white", font=("Segoe UI", 12)).grid(row=2, column=0, padx=10, pady=5)
    supplier_phone_entry = ttk.Entry(input_frame, font=("Segoe UI", 12))
    supplier_phone_entry.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(input_frame, text="Address:", bg="white", font=("Segoe UI", 12)).grid(row=3, column=0, padx=10, pady=5)
    supplier_address_entry = ttk.Entry(input_frame, font=("Segoe UI", 12))
    supplier_address_entry.grid(row=3, column=1, padx=10, pady=5)

    # Insert Supplier
    def insert_supplier():
        name = supplier_name_entry.get()
        phone = supplier_phone_entry.get()
        address = supplier_address_entry.get()

        if not (name and phone and address):
            messagebox.showerror("Input Error", "Please provide all fields (Name, Phone, Address).")
            return

        conn = connect_to_db()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO Suppliers (Name, Phone, Address) VALUES (%s, %s, %s)", (name, phone, address))
                conn.commit()
                fetch_suppliers()
                supplier_name_entry.delete(0, tk.END)
                supplier_phone_entry.delete(0, tk.END)
                supplier_address_entry.delete(0, tk.END)
                messagebox.showinfo("Success", "Supplier added successfully!")
            except mysql.connector.Error as e:
                messagebox.showerror("Database Error", f"Error adding supplier: {e}")

    # Update Supplier
    def update_supplier():
        supplier_id = supplier_id_entry.get()
        name = supplier_name_entry.get()
        phone = supplier_phone_entry.get()
        address = supplier_address_entry.get()

        if not supplier_id:
            messagebox.showerror("Input Error", "Please provide the Supplier ID.")
            return

        conn = connect_to_db()
        if conn:
            try:
                cursor = conn.cursor()
                updates = []
                params = []

                if name:
                    updates.append("Name = %s")
                    params.append(name)
                if phone:
                    updates.append("Phone = %s")
                    params.append(phone)
                if address:
                    updates.append("Address = %s")
                    params.append(address)

                if not updates:
                    messagebox.showerror("Input Error", "Please provide at least one field to update.")
                    return

                params.append(supplier_id)
                cursor.execute(f"UPDATE Suppliers SET {', '.join(updates)} WHERE Supplier_ID = %s", params)
                conn.commit()
                fetch_suppliers()
                supplier_id_entry.delete(0, tk.END)
                supplier_name_entry.delete(0, tk.END)
                supplier_phone_entry.delete(0, tk.END)
                supplier_address_entry.delete(0, tk.END)
                messagebox.showinfo("Success", "Supplier updated successfully!")
            except mysql.connector.Error as e:
                messagebox.showerror("Database Error", f"Error updating supplier: {e}")

    # Delete Supplier
    def delete_supplier():
        supplier_id = supplier_id_entry.get()

        if not supplier_id:
            messagebox.showerror("Input Error", "Please provide the Supplier ID.")
            return

        conn = connect_to_db()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM Suppliers WHERE Supplier_ID = %s", (supplier_id,))
                conn.commit()
                fetch_suppliers()
                supplier_id_entry.delete(0, tk.END)
                messagebox.showinfo("Success", "Supplier deleted successfully!")
            except mysql.connector.Error as e:
                messagebox.showerror("Database Error", f"Error deleting supplier: {e}")

    # Buttons
    tk.Button(input_frame, text="Insert", bg="#00796b", fg="white", command=insert_supplier).grid(row=4, column=0, padx=10, pady=5)
    tk.Button(input_frame, text="Update", bg="#00796b", fg="white", command=update_supplier).grid(row=4, column=1, padx=10, pady=5)
    tk.Button(input_frame, text="Delete", bg="#8B0000", fg="white", command=delete_supplier).grid(row=4, column=2, padx=10, pady=5)


# Products Module
def open_products_module(parent):
    for widget in parent.winfo_children():
        if isinstance(widget, tk.Frame) and widget != parent.children.get("!frame"):
            widget.destroy()

    content_frame = tk.Frame(parent, bg="white")
    content_frame.pack(side="right", expand=True, fill="both")

    tk.Label(content_frame, text="Products Management", bg="white", fg="#00796b", font=("Segoe UI", 24, "bold")).pack(pady=20)

    # Table Frame
    table_frame = tk.Frame(content_frame, bg="white")
    table_frame.pack(fill="both", expand=True, padx=20, pady=10)

    # Add Supplier_ID to columns
    columns = ("Product_ID", "Supplier_ID", "Name", "Stock_Level", "Price", "Image_Path")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
    tree.pack(fill="both", expand=True)

    tree.heading("Product_ID", text="Product ID")
    tree.heading("Supplier_ID", text="Supplier ID")
    tree.heading("Name", text="Name")
    tree.heading("Stock_Level", text="Stock Level")
    tree.heading("Price", text="Price")
    tree.heading("Image_Path", text="Image Path")

    # Image and Details Frame
    details_frame = tk.Frame(content_frame, bg="white")
    details_frame.pack(fill="x", pady=10)

    # Display image on the right side
    product_image_label = tk.Label(details_frame, bg="white")
    product_image_label.grid(row=0, column=1, padx=20)  # Adjust grid placement for right alignment

    product_details_label = tk.Label(details_frame, text="", bg="white", font=("Segoe UI", 12))
    product_details_label.grid(row=0, column=0, padx=20)

    def fetch_products():
        conn = connect_to_db()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT 
                        Product_ID, 
                        Supplier_ID,  
                        Name, 
                        Stock_Level, 
                        Price, 
                        Product_Image_Path AS Image_Path
                    FROM Products
                """)
                rows = cursor.fetchall()
                for row in tree.get_children():
                    tree.delete(row)
                for row in rows:
                    tree.insert("", "end", values=row)
                conn.close()
            except mysql.connector.Error as e:
                messagebox.showerror("Database Error", f"Error fetching products: {e}")

    fetch_products()

    def display_product_image(event):
        selected_item = tree.selection()
        if not selected_item:
            return
        product_id, supplier_id, name, stock, price, image_path = tree.item(selected_item)["values"]

        # Display product details
        product_details = f"Name: {name}\nStock Level: {stock}\nPrice: ${price}\nSupplier ID: {supplier_id}"
        product_details_label.config(text=product_details)

        if os.path.exists(image_path):  # Check if the image file exists
            try:
                image = Image.open(image_path)
                image = image.resize((150, 150), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                product_image_label.config(image=photo)
                product_image_label.image = photo
            except Exception as e:
                product_image_label.config(image=None)
                product_image_label.image = None
                messagebox.showerror("Image Error", f"Error loading image: {e}")
        else:
            product_image_label.config(image=None)
            product_image_label.image = None
            messagebox.showerror("Image Error", f"Image not found: {image_path}")

    # Bind the display_product_image function to the treeview selection event
    tree.bind("<<TreeviewSelect>>", display_product_image)

    # Input Frame for Insert, Update, Delete
    input_frame = tk.Frame(content_frame, bg="white")
    input_frame.pack(fill="x", pady=10)

    tk.Label(input_frame, text="Product ID (for Update/Delete):", bg="white", font=("Segoe UI", 12)).grid(row=0, column=0, padx=10, pady=5)
    product_id_entry = ttk.Entry(input_frame, font=("Segoe UI", 12))
    product_id_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(input_frame, text="Name:", bg="white", font=("Segoe UI", 12)).grid(row=1, column=0, padx=10, pady=5)
    product_name_entry = ttk.Entry(input_frame, font=("Segoe UI", 12))
    product_name_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(input_frame, text="Stock Level:", bg="white", font=("Segoe UI", 12)).grid(row=2, column=0, padx=10, pady=5)
    product_stock_entry = ttk.Entry(input_frame, font=("Segoe UI", 12))
    product_stock_entry.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(input_frame, text="Price:", bg="white", font=("Segoe UI", 12)).grid(row=3, column=0, padx=10, pady=5)
    product_price_entry = ttk.Entry(input_frame, font=("Segoe UI", 12))
    product_price_entry.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(input_frame, text="Image Path:", bg="white", font=("Segoe UI", 12)).grid(row=4, column=0, padx=10, pady=5)
    product_image_path_entry = ttk.Entry(input_frame, font=("Segoe UI", 12))
    product_image_path_entry.grid(row=4, column=1, padx=10, pady=5)

    tk.Label(input_frame, text="Supplier ID:", bg="white", font=("Segoe UI", 12)).grid(row=5, column=0, padx=10, pady=5)
    supplier_id_entry = ttk.Entry(input_frame, font=("Segoe UI", 12))
    supplier_id_entry.grid(row=5, column=1, padx=10, pady=5)

    def insert_product():
        name = product_name_entry.get()
        stock = product_stock_entry.get()
        price = product_price_entry.get()
        image_path = product_image_path_entry.get()
        supplier_id = supplier_id_entry.get()  # Get the Supplier ID

        # Check that at least `name` and `stock` are provided for insertion
        if not name or not stock or not supplier_id:
            messagebox.showerror("Input Error", "Name, Stock Level, and Supplier ID are required.")
            return

        conn = connect_to_db()
        if conn:
            try:
                cursor = conn.cursor()
                # Dynamically construct the query and parameters
                fields = ["Supplier_ID", "Name", "Stock_Level"]
                values = [supplier_id, name, stock]

                if price:
                    fields.append("Price")
                    values.append(price)
                if image_path:
                    fields.append("Product_Image_Path")
                    values.append(image_path)

                query = f"INSERT INTO Products ({', '.join(fields)}) VALUES ({', '.join(['%s'] * len(values))})"
                cursor.execute(query, values)
                conn.commit()

                fetch_products()  # Refresh the product list
                product_name_entry.delete(0, tk.END)
                product_stock_entry.delete(0, tk.END)
                product_price_entry.delete(0, tk.END)
                product_image_path_entry.delete(0, tk.END)
                supplier_id_entry.delete(0, tk.END)  # Clear Supplier ID field
                messagebox.showinfo("Success", "Product added successfully!")
            except mysql.connector.Error as e:
                messagebox.showerror("Database Error", f"Error inserting product: {e}")
            finally:
                conn.close()

    def update_product():
        product_id = product_id_entry.get()
        name = product_name_entry.get()
        stock = product_stock_entry.get()
        price = product_price_entry.get()
        image_path = product_image_path_entry.get()
        supplier_id = supplier_id_entry.get()  # Get the Supplier ID

        # Ensure `Product_ID` is provided for updates
        if not product_id:
            messagebox.showerror("Input Error", "Product ID is required for updates.")
            return

        conn = connect_to_db()
        if conn:
            try:
                # Dynamically construct the update query based on provided fields
                updates = []
                params = []

                if supplier_id:  # Only update Supplier_ID if provided
                    updates.append("Supplier_ID = %s")
                    params.append(supplier_id)
                if name:
                    updates.append("Name = %s")
                    params.append(name)
                if stock:
                    updates.append("Stock_Level = %s")
                    params.append(stock)
                if price:
                    updates.append("Price = %s")
                    params.append(price)
                if image_path:
                    updates.append("Product_Image_Path = %s")
                    params.append(image_path)

                # Ensure there is at least one field to update
                if not updates:
                    messagebox.showerror("Input Error", "At least one field must be provided for an update.")
                    return

                # Add `Product_ID` to the parameters and execute the query
                params.append(product_id)
                query = f"UPDATE Products SET {', '.join(updates)} WHERE Product_ID = %s"
                cursor = conn.cursor()
                cursor.execute(query, params)
                conn.commit()

                fetch_products()  # Refresh the product list
                product_id_entry.delete(0, tk.END)
                product_name_entry.delete(0, tk.END)
                product_stock_entry.delete(0, tk.END)
                product_price_entry.delete(0, tk.END)
                product_image_path_entry.delete(0, tk.END)
                supplier_id_entry.delete(0, tk.END)  # Clear Supplier ID field
                messagebox.showinfo("Success", "Product updated successfully!")
            except mysql.connector.Error as e:
                messagebox.showerror("Database Error", f"Error updating product: {e}")
            finally:
                conn.close()

    def delete_product():
        product_id = product_id_entry.get()

        if not product_id:
            messagebox.showerror("Input Error", "Please provide the Product ID to delete.")
            return

        conn = connect_to_db()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM Products WHERE Product_ID = %s", (product_id,))
                conn.commit()
                fetch_products()
                product_id_entry.delete(0, tk.END)
                messagebox.showinfo("Success", "Product deleted successfully!")
            except mysql.connector.Error as e:
                messagebox.showerror("Database Error", f"Error deleting product: {e}")

    # Fetch products and bind events
    fetch_products()

    # Buttons
    button_frame = tk.Frame(content_frame, bg="white")
    button_frame.pack(fill="x", pady=10)

    tk.Button(button_frame, text="Insert", bg="#00796b", fg="white", command=insert_product).pack(side="right", padx=10)
    tk.Button(button_frame, text="Update", bg="#00796b", fg="white", command=update_product).pack(side="right", padx=10)
    tk.Button(button_frame, text="Delete", bg='#8B0000', fg="white", command=delete_product).pack(side="right", padx=10)



# Display Dashboard Content
# Dashboard Function
def display_dashboard(parent):
    # Clear existing widgets
    for widget in parent.winfo_children():
        if isinstance(widget, tk.Frame) and widget != parent.children["!frame"]:
            widget.destroy()

    content_frame = tk.Frame(parent, bg="white")
    content_frame.pack(side="right", expand=True, fill="both")

    tk.Label(content_frame, text="Dashboard", bg="white", fg="#00796b", font=("Segoe UI", 24, "bold")).pack(pady=20)

    # Summary Cards
    card_frame = tk.Frame(content_frame, bg="white", padx=20, pady=10)
    card_frame.pack(fill="x")

    def create_summary_card(frame, title, value, color):
        card = tk.Frame(frame, bg=color, padx=20, pady=20, width=200, height=100)
        card.pack(side="left", padx=10, pady=10)
        tk.Label(card, text=title, bg=color, fg="white", font=("Segoe UI", 14, "bold")).pack()
        tk.Label(card, text=value, bg=color, fg="white", font=("Segoe UI", 20, "bold")).pack()

    # Fetch data for summary cards
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)

            # Total Employees
            cursor.execute("SELECT COUNT(*) AS total_employees FROM Users WHERE Role = 'Employee'")
            total_employees = cursor.fetchone()["total_employees"]

            # Total Customers
            cursor.execute("SELECT COUNT(*) AS total_customers FROM Customers")
            total_customers = cursor.fetchone()["total_customers"]

            # Total Products
            cursor.execute("SELECT COUNT(*) AS total_products FROM Products")
            total_products = cursor.fetchone()["total_products"]

            # Out of Stock
            cursor.execute("SELECT COUNT(*) AS out_of_stock FROM Products WHERE Stock_Level = 0")
            out_of_stock = cursor.fetchone()["out_of_stock"]

            # Total Suppliers
            cursor.execute("SELECT COUNT(*) AS total_suppliers FROM Suppliers")
            total_suppliers = cursor.fetchone()["total_suppliers"]

            # Best Seller Product
            cursor.execute("""
                SELECT p.Name, SUM(ps.Quantity) AS total_sales
                FROM Product_Sales ps
                JOIN Products p ON ps.Product_ID = p.Product_ID
                GROUP BY ps.Product_ID
                ORDER BY total_sales DESC
                LIMIT 1
            """)
            best_seller = cursor.fetchone()
            best_seller_name = best_seller["Name"] if best_seller else "N/A"
            best_seller_sales = best_seller["total_sales"] if best_seller else 0

            conn.close()

            # Create summary cards
            create_summary_card(card_frame, "Total Employees", total_employees, "#5A9BD4")
            create_summary_card(card_frame, "Total Customers", total_customers, "#FF6F61")
            create_summary_card(card_frame, "Total Products", total_products, "#009688")
            create_summary_card(card_frame, "Out of Stock", out_of_stock, "#F4C430")
            create_summary_card(card_frame, "Total Suppliers", total_suppliers, "#673AB7")

            # Best Seller Product Section
            best_seller_frame = tk.Frame(content_frame, bg="white", padx=20, pady=20)
            best_seller_frame.pack(fill="x", pady=20)
            tk.Label(best_seller_frame, text="Best Seller Product", bg="white", fg="#00796b",
                     font=("Segoe UI", 16, "bold")).pack()
            tk.Label(best_seller_frame, text=f"Product: {best_seller_name}\nTotal Sales: {best_seller_sales}",
                     bg="white", fg="#333", font=("Segoe UI", 14)).pack(pady=10)

        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Error fetching data: {e}")

    def create_sales_chart():
        conn = connect_to_db()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT Transaction_Date, SUM(Total_Amount) AS Total_Amount
                    FROM Sales_Transactions
                    GROUP BY Transaction_Date
                    ORDER BY Transaction_Date
                """)
                data = cursor.fetchall()
                conn.close()

                if data:
                    transaction_dates = [row[0].strftime("%Y-%m-%d") for row in data]
                    total_amounts = [row[1] for row in data]
                    fig, ax = plt.subplots(figsize=(8, 4), dpi=100)
                    ax.plot(transaction_dates, total_amounts, color="#FF5722", marker="o", markersize=6, linewidth=2)
                    ax.set_xticks(transaction_dates)
                    ax.set_xticklabels(transaction_dates, rotation=45, ha="right", fontsize=10)
                    ax.set_title("Sales Transactions by Date", fontsize=16, color="#333")
                    ax.set_xlabel("Transaction Date", fontsize=12)
                    ax.set_ylabel("Total Sales (USD)", fontsize=12)
                    ax.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.7)
                    fig.subplots_adjust(bottom=0.3, top=0.9)
                    plt.tight_layout(pad=1.5)
                    chart_canvas = FigureCanvasTkAgg(fig, content_frame)
                    chart_canvas.get_tk_widget().pack(fill="x", expand=False)
                    chart_canvas.draw()
                else:
                    tk.Label(content_frame, text="No sales data available to display.", bg="white", fg="red",
                             font=("Segoe UI", 12)).pack(pady=20)
            except mysql.connector.Error as e:
                messagebox.showerror("Database Error", f"Error fetching sales data: {e}")

    # Create and display the sales chart
    create_sales_chart()

# Open Customers Module
def open_customers_module(parent):
    for widget in parent.winfo_children():
        if isinstance(widget, tk.Frame) and widget != parent.children["!frame"]:
            widget.destroy()

    content_frame = tk.Frame(parent, bg="white")
    content_frame.pack(side="right", expand=True, fill="both")

    tk.Label(content_frame, text="Customers Management", bg="white", fg="#00796b", font=("Segoe UI", 24, "bold")).pack(pady=20)

    # Table Frame
    table_frame = tk.Frame(content_frame, bg="white")
    table_frame.pack(fill="both", expand=True, padx=20, pady=10)

    columns = ("Customer_ID", "Name", "Phone")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
    tree.pack(fill="both", expand=True)

    tree.heading("Customer_ID", text="Customer ID")
    tree.heading("Name", text="Name")
    tree.heading("Phone", text="Phone")

    # Fetch All Customers with Phone Numbers
    def fetch_customers():
        conn = connect_to_db()
        if conn:
            try:
                cursor = conn.cursor()
                query = """
                    SELECT c.Customer_ID, c.Name, cp.Phone 
                    FROM Customers c
                    LEFT JOIN CustomerPhones cp ON c.Customer_ID = cp.Customer_ID
                """
                cursor.execute(query)
                rows = cursor.fetchall()
                for row in tree.get_children():
                    tree.delete(row)
                for row in rows:
                    tree.insert("", "end", values=row)
                conn.close()
            except mysql.connector.Error as e:
                messagebox.showerror("Database Error", f"Error fetching customers: {e}")

    fetch_customers()

    # Input Frame
    input_frame = tk.Frame(content_frame, bg="white")
    input_frame.pack(fill="x", pady=10)

    tk.Label(input_frame, text="Customer ID:", bg="white", font=("Segoe UI", 12)).grid(row=0, column=0, padx=10, pady=5)
    customer_id_entry = ttk.Entry(input_frame, font=("Segoe UI", 12))
    customer_id_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(input_frame, text="Customer Name:", bg="white", font=("Segoe UI", 12)).grid(row=1, column=0, padx=10, pady=5)
    customer_name_entry = ttk.Entry(input_frame, font=("Segoe UI", 12))
    customer_name_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(input_frame, text="Phone:", bg="white", font=("Segoe UI", 12)).grid(row=2, column=0, padx=10, pady=5)
    customer_phone_entry = ttk.Entry(input_frame, font=("Segoe UI", 12))
    customer_phone_entry.grid(row=2, column=1, padx=10, pady=5)

    def insert_customer():
        customer_name = customer_name_entry.get()
        customer_phone = customer_phone_entry.get()

        if not (customer_name and customer_phone):
            messagebox.showerror("Input Error", "Please provide all fields (Name, Phone).")
            return

        conn = connect_to_db()
        if conn:
            try:
                cursor = conn.cursor()
                # Insert customer and get the generated Customer_ID
                cursor.execute("INSERT INTO Customers (Name) VALUES (%s)", (customer_name,))
                customer_id = cursor.lastrowid  # Get the auto-generated Customer_ID

                # Insert the phone with the generated Customer_ID
                cursor.execute("INSERT INTO CustomerPhones (Customer_ID, Phone) VALUES (%s, %s)",
                               (customer_id, customer_phone))
                conn.commit()
                fetch_customers()
                customer_name_entry.delete(0, tk.END)
                customer_phone_entry.delete(0, tk.END)
                messagebox.showinfo("Success", "Customer added successfully!")
            except mysql.connector.Error as e:
                messagebox.showerror("Database Error", f"Error adding customer: {e}")

    def update_customer():
        customer_id = customer_id_entry.get()
        customer_name = customer_name_entry.get()
        customer_phone = customer_phone_entry.get()

        if not customer_id:
            messagebox.showerror("Input Error", "Please provide the Customer ID.")
            return

        conn = connect_to_db()
        if conn:
            try:
                cursor = conn.cursor()
                if customer_name:
                    cursor.execute("UPDATE Customers SET Name = %s WHERE Customer_ID = %s", (customer_name, customer_id))
                if customer_phone:
                    cursor.execute("UPDATE CustomerPhones SET Phone = %s WHERE Customer_ID = %s", (customer_phone, customer_id))
                conn.commit()
                fetch_customers()
                customer_id_entry.delete(0, tk.END)
                customer_name_entry.delete(0, tk.END)
                customer_phone_entry.delete(0, tk.END)
                messagebox.showinfo("Success", "Customer updated successfully!")
            except mysql.connector.Error as e:
                messagebox.showerror("Database Error", f"Error updating customer: {e}")

    def delete_customer():
        customer_id = customer_id_entry.get()

        if not customer_id:
            messagebox.showerror("Input Error", "Please provide the Customer ID.")
            return

        conn = connect_to_db()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM Customers WHERE Customer_ID = %s", (customer_id,))
                conn.commit()
                fetch_customers()
                customer_id_entry.delete(0, tk.END)
                messagebox.showinfo("Success", "Customer deleted successfully!")
            except mysql.connector.Error as e:
                messagebox.showerror("Database Error", f"Error deleting customer: {e}")

    # Buttons
    tk.Button(input_frame, text="Insert", bg="#00796b", fg="white", command=insert_customer).grid(row=3, column=0, padx=10, pady=5)
    tk.Button(input_frame, text="Update", bg="#00796b", fg="white", command=update_customer).grid(row=3, column=1, padx=10, pady=5)
    tk.Button(input_frame, text="Delete", bg='#8B0000', fg="white", command=delete_customer).grid(row=3, column=2, padx=10, pady=5)
# Open Discounts Module
def open_discounts_module(parent):
    # Clear previous widgets
    for widget in parent.winfo_children():
        if isinstance(widget, tk.Frame) and widget != parent.children.get("!frame"):
            widget.destroy()

    # Content Frame
    content_frame = tk.Frame(parent, bg="white")
    content_frame.pack(side="right", expand=True, fill="both")

    # Title
    tk.Label(content_frame, text="Discounts Management", bg="white", fg="#00796b", font=("Segoe UI", 24, "bold")).pack(pady=20)

    # Table Frame
    table_frame = tk.Frame(content_frame, bg="white")
    table_frame.pack(fill="both", expand=True, padx=20, pady=10)

    columns = ("Discount_ID", "Code", "Discount_Percentage", "Start_Date", "End_Date", "Status")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
    tree.pack(fill="both", expand=True)

    for col in columns:
        tree.heading(col, text=col)

    # Fetch Discounts
    def fetch_discounts():
        conn = connect_to_db()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT Discount_ID, Code, Discount_Percentage, Start_Date, End_Date, Status FROM Discounts")
                rows = cursor.fetchall()
                for row in tree.get_children():
                    tree.delete(row)
                for row in rows:
                    tree.insert("", "end", values=row)
                conn.close()
            except mysql.connector.Error as e:
                messagebox.showerror("Database Error", f"Error fetching discounts: {e}")

    fetch_discounts()

    # Input Frame
    input_frame = tk.Frame(content_frame, bg="white")
    input_frame.pack(fill="x", pady=10)

    tk.Label(input_frame, text="Code:", bg="white", font=("Segoe UI", 12)).grid(row=0, column=0, padx=10, pady=5)
    code_entry = ttk.Entry(input_frame, font=("Segoe UI", 12))
    code_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(input_frame, text="Discount %:", bg="white", font=("Segoe UI", 12)).grid(row=1, column=0, padx=10, pady=5)
    percentage_entry = ttk.Entry(input_frame, font=("Segoe UI", 12))
    percentage_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(input_frame, text="Start Date (YYYY-MM-DD):", bg="white", font=("Segoe UI", 12)).grid(row=2, column=0, padx=10, pady=5)
    start_date_entry = ttk.Entry(input_frame, font=("Segoe UI", 12))
    start_date_entry.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(input_frame, text="End Date (YYYY-MM-DD):", bg="white", font=("Segoe UI", 12)).grid(row=3, column=0, padx=10, pady=5)
    end_date_entry = ttk.Entry(input_frame, font=("Segoe UI", 12))
    end_date_entry.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(input_frame, text="Status:", bg="white", font=("Segoe UI", 12)).grid(row=4, column=0, padx=10, pady=5)
    status_entry = ttk.Entry(input_frame, font=("Segoe UI", 12))
    status_entry.grid(row=4, column=1, padx=10, pady=5)

    # Insert Discount
    def insert_discount():
        code = code_entry.get()
        percentage = percentage_entry.get()
        start_date = start_date_entry.get()
        end_date = end_date_entry.get()
        status = status_entry.get()

        if not (code and percentage and start_date and end_date and status):
            messagebox.showerror("Input Error", "Please provide all fields.")
            return

        conn = connect_to_db()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO Discounts (Code, Discount_Percentage, Start_Date, End_Date, Status) VALUES (%s, %s, %s, %s, %s)",
                    (code, percentage, start_date, end_date, status)
                )
                conn.commit()
                fetch_discounts()
                code_entry.delete(0, tk.END)
                percentage_entry.delete(0, tk.END)
                start_date_entry.delete(0, tk.END)
                end_date_entry.delete(0, tk.END)
                status_entry.delete(0, tk.END)
                messagebox.showinfo("Success", "Discount added successfully!")
            except mysql.connector.Error as e:
                messagebox.showerror("Database Error", f"Error adding discount: {e}")

    # Update Discount
    def update_discount():
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Selection Error", "Please select a discount to update.")
            return

        discount_id = tree.item(selected[0], "values")[0]
        code = code_entry.get()
        percentage = percentage_entry.get()
        start_date = start_date_entry.get()
        end_date = end_date_entry.get()
        status = status_entry.get()

        if not (code or percentage or start_date or end_date or status):
            messagebox.showerror("Input Error", "Please provide at least one field to update.")
            return

        conn = connect_to_db()
        if conn:
            try:
                cursor = conn.cursor()
                updates = []
                params = []

                if code:
                    updates.append("Code = %s")
                    params.append(code)
                if percentage:
                    updates.append("Discount_Percentage = %s")
                    params.append(percentage)
                if start_date:
                    updates.append("Start_Date = %s")
                    params.append(start_date)
                if end_date:
                    updates.append("End_Date = %s")
                    params.append(end_date)
                if status:
                    updates.append("Status = %s")
                    params.append(status)

                params.append(discount_id)
                query = f"UPDATE Discounts SET {', '.join(updates)} WHERE Discount_ID = %s"
                cursor.execute(query, params)
                conn.commit()
                fetch_discounts()
                code_entry.delete(0, tk.END)
                percentage_entry.delete(0, tk.END)
                start_date_entry.delete(0, tk.END)
                end_date_entry.delete(0, tk.END)
                status_entry.delete(0, tk.END)
                messagebox.showinfo("Success", "Discount updated successfully!")
            except mysql.connector.Error as e:
                messagebox.showerror("Database Error", f"Error updating discount: {e}")

    # Delete Discount
    def delete_discount():
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Selection Error", "Please select a discount to delete.")
            return

        discount_id = tree.item(selected[0], "values")[0]

        conn = connect_to_db()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM Discounts WHERE Discount_ID = %s", (discount_id,))
                conn.commit()
                fetch_discounts()
                messagebox.showinfo("Success", "Discount deleted successfully!")
            except mysql.connector.Error as e:
                messagebox.showerror("Database Error", f"Error deleting discount: {e}")

    # Buttons
    tk.Button(input_frame, text="Insert", bg="#00796b", fg="white", command=insert_discount).grid(row=5, column=0, padx=10, pady=5)
    tk.Button(input_frame, text="Update", bg="#00796b", fg="white", command=update_discount).grid(row=5, column=1, padx=10, pady=5)
    tk.Button(input_frame, text="Delete", bg="#8B0000", fg="white", command=delete_discount).grid(row=5, column=2, padx=10, pady=5)

# Open Employees Module
def open_employees_module(parent):
    # Clear previous widgets
    for widget in parent.winfo_children():
        if isinstance(widget, tk.Frame) and widget != parent.children.get("!frame"):
            widget.destroy()

    # Content Frame
    content_frame = tk.Frame(parent, bg="white")
    content_frame.pack(side="right", expand=True, fill="both")

    # Header
    tk.Label(content_frame, text="Employees Management", bg="white", fg="#00796b", font=("Segoe UI", 24, "bold")).pack(pady=20)

    # Table Frame
    table_frame = tk.Frame(content_frame, bg="white")
    table_frame.pack(fill="both", expand=True, padx=20, pady=10)

    columns = ("User_ID", "Role")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
    tree.pack(fill="both", expand=True)

    tree.heading("User_ID", text="User ID")
    tree.heading("Role", text="Role")

    # Fetch All Employees
    def fetch_employees():
        conn = connect_to_db()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT User_ID, Role FROM Users WHERE Role = 'Employee'")
                rows = cursor.fetchall()
                for row in tree.get_children():
                    tree.delete(row)
                for row in rows:
                    tree.insert("", "end", values=row)
                conn.close()
            except mysql.connector.Error as e:
                messagebox.showerror("Database Error", f"Error fetching employees: {e}")

    fetch_employees()

    # Input Frame
    input_frame = tk.Frame(content_frame, bg="white")
    input_frame.pack(fill="x", pady=10)

    # Input Fields
    tk.Label(input_frame, text="User ID:", bg="white", font=("Segoe UI", 12)).grid(row=0, column=0, padx=10, pady=5)
    user_id_entry = ttk.Entry(input_frame, font=("Segoe UI", 12))
    user_id_entry.grid(row=0, column=1, padx=10, pady=5)



    # Select Employee for Editing
    def select_employee(event):
        selected = tree.selection()
        if selected:
            values = tree.item(selected, "values")
            user_id_entry.delete(0, tk.END)
            user_id_entry.insert(0, values[0])


    tree.bind("<<TreeviewSelect>>", select_employee)



    # Delete Employee
    def delete_employee():
        user_id = user_id_entry.get()

        if not user_id:
            messagebox.showerror("Input Error", "Please provide the User ID to delete.")
            return

        conn = connect_to_db()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM Users WHERE User_ID = %s", (user_id,))
                conn.commit()
                fetch_employees()  # Refresh table
                messagebox.showinfo("Success", "Employee deleted successfully!")
                user_id_entry.delete(0, tk.END)
            except mysql.connector.Error as e:
                messagebox.showerror("Database Error", f"Error deleting employee: {e}")
            finally:
                conn.close()

    # Buttons
    tk.Button(input_frame, text="Delete", bg='#8B0000', fg="white", command=delete_employee).grid(row=2, column=1, padx=10, pady=10)


# Open Sales Transactions Module
# Open Sales Transactions Module with Filter and Search
def open_sales_transactions_module(parent):
    # Clear previous widgets in parent frame
    for widget in parent.winfo_children():
        if isinstance(widget, tk.Frame) and widget != parent.children["!frame"]:
            widget.destroy()

    # Create content frame
    content_frame = tk.Frame(parent, bg="white")
    content_frame.pack(side="right", expand=True, fill="both")

    # Title
    tk.Label(content_frame, text="Sales Transactions", bg="white", fg="#00796b", font=("Segoe UI", 24, "bold")).pack(pady=20)

    # Filter Frame (with filter inputs and transaction delete ID)
    filter_frame = tk.Frame(content_frame, bg="white", pady=10)
    filter_frame.pack(fill="x")

    # Transaction ID for Deletion
    tk.Label(filter_frame, text="Delete by Transaction ID:", bg="white", font=("Segoe UI", 12)).grid(row=0, column=0, padx=10, pady=5)
    transaction_id_delete_entry = ttk.Entry(filter_frame, font=("Segoe UI", 12), width=15)
    transaction_id_delete_entry.grid(row=0, column=1, padx=10, pady=5)

    # Start Date Entry
    tk.Label(filter_frame, text="Start Date:", bg="white", font=("Segoe UI", 12)).grid(row=1, column=0, padx=10, pady=5)
    start_date_entry = ttk.Entry(filter_frame, font=("Segoe UI", 12), width=15)
    start_date_entry.grid(row=1, column=1, padx=10, pady=5)

    # End Date Entry
    tk.Label(filter_frame, text="End Date:", bg="white", font=("Segoe UI", 12)).grid(row=1, column=2, padx=10, pady=5)
    end_date_entry = ttk.Entry(filter_frame, font=("Segoe UI", 12), width=15)
    end_date_entry.grid(row=1, column=3, padx=10, pady=5)

    # Customer ID Entry
    tk.Label(filter_frame, text="Customer ID:", bg="white", font=("Segoe UI", 12)).grid(row=2, column=0, padx=10, pady=5)
    customer_id_entry = ttk.Entry(filter_frame, font=("Segoe UI", 12), width=15)
    customer_id_entry.grid(row=2, column=1, padx=10, pady=5)

    # Min Amount Entry
    tk.Label(filter_frame, text="Min Amount:", bg="white", font=("Segoe UI", 12)).grid(row=2, column=2, padx=10, pady=5)
    min_amount_entry = ttk.Entry(filter_frame, font=("Segoe UI", 12), width=15)
    min_amount_entry.grid(row=2, column=3, padx=10, pady=5)

    # Max Amount Entry
    tk.Label(filter_frame, text="Max Amount:", bg="white", font=("Segoe UI", 12)).grid(row=2, column=4, padx=10, pady=5)
    max_amount_entry = ttk.Entry(filter_frame, font=("Segoe UI", 12), width=15)
    max_amount_entry.grid(row=2, column=5, padx=10, pady=5)

    # Table Frame for displaying transactions
    table_frame = tk.Frame(content_frame, bg="white")
    table_frame.pack(fill="both", expand=True, padx=20, pady=10)

    columns = ("Transaction_ID", "Customer_ID", "Transaction_Date", "Total_Amount")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
    tree.pack(fill="both", expand=True)

    tree.heading("Transaction_ID", text="Transaction ID")
    tree.heading("Customer_ID", text="Customer ID")
    tree.heading("Transaction_Date", text="Transaction Date")
    tree.heading("Total_Amount", text="Total Amount")

    # Fetch and Display Transactions with Filters
    def fetch_sales_transactions():
        conn = connect_to_db()
        if conn:
            try:
                cursor = conn.cursor()

                # Build the SQL query dynamically based on filter inputs
                query = "SELECT Transaction_ID, Customer_ID, Transaction_Date, Total_Amount FROM Sales_Transactions WHERE 1=1"
                params = []

                if start_date_entry.get() and end_date_entry.get():
                    query += " AND Transaction_Date BETWEEN %s AND %s"
                    params.append(start_date_entry.get())
                    params.append(end_date_entry.get())

                if customer_id_entry.get():
                    query += " AND Customer_ID = %s"
                    params.append(customer_id_entry.get())

                if min_amount_entry.get():
                    query += " AND Total_Amount >= %s"
                    params.append(min_amount_entry.get())

                if max_amount_entry.get():
                    query += " AND Total_Amount <= %s"
                    params.append(max_amount_entry.get())

                query += " ORDER BY Transaction_Date DESC"
                cursor.execute(query, params)
                rows = cursor.fetchall()

                # Clear existing rows
                for row in tree.get_children():
                    tree.delete(row)

                # Populate the tree with fetched data
                for row in rows:
                    tree.insert("", "end", values=row)

                conn.close()
            except mysql.connector.Error as e:
                messagebox.showerror("Database Error", f"Error fetching sales transactions: {e}")

    # Delete Sales Transaction by Transaction ID
    def delete_sales_transaction():
        transaction_id = transaction_id_delete_entry.get()

        if not transaction_id:
            messagebox.showerror("Input Error", "Please provide the Transaction ID to delete.")
            return

        conn = connect_to_db()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM Product_Sales WHERE Transaction_ID = %s", (transaction_id,))
                cursor.execute("DELETE FROM Sales_Transactions WHERE Transaction_ID = %s", (transaction_id,))
                conn.commit()
                fetch_sales_transactions()  # Refresh the transactions list
                transaction_id_delete_entry.delete(0, tk.END)
                messagebox.showinfo("Success", f"Transaction {transaction_id} deleted successfully!")
            except mysql.connector.Error as e:
                messagebox.showerror("Database Error", f"Error deleting transaction: {e}")
            finally:
                conn.close()

    # Buttons for filtering, clearing filters and deleting transactions
    tk.Button(filter_frame, text="Apply Filters", bg="#00796b", fg="white", command=fetch_sales_transactions).grid(row=3, column=1, padx=10, pady=10)
    tk.Button(filter_frame, text="Clear Filters", bg="#00796b", fg="white", command=lambda: [
        start_date_entry.delete(0, tk.END),
        end_date_entry.delete(0, tk.END),
        customer_id_entry.delete(0, tk.END),
        min_amount_entry.delete(0, tk.END),
        max_amount_entry.delete(0, tk.END),
        fetch_sales_transactions()]).grid(row=3, column=3, padx=10, pady=10)

    tk.Button(filter_frame, text="Delete Transaction", bg='#8B0000', fg="white", command=delete_sales_transaction).grid(row=0, column=2, padx=5, pady=5)

    # Fetch all transactions initially
    fetch_sales_transactions()



# GUI Setup
root = tk.Tk()
root.title("Lucerne Boutique Management System")
root.geometry("1200x1200")
root.configure(bg="white")

# Header
header_frame = tk.Frame(root, bg="white", height=600)
header_frame.pack(fill="x", side="left")

# Load and display the logo
# Load and display the logo
try:
    logo_image = Image.open(LOGO_PATH)
    logo_image = logo_image.resize((400, 350), Image.Resampling.LANCZOS)
    logo = ImageTk.PhotoImage(logo_image)
    logo_label = tk.Label(root, image=logo, bg="white")
    logo_label.image = logo
    logo_label.pack(pady=10)  # Add padding to position the logo
except Exception as e:
    messagebox.showerror("Image Error", f"Error loading logo: {e}")

# Add "Management System" text under the logo

# Login Form
login_frame = tk.Frame(root, bg="white", padx=20, pady=20)
login_frame.pack(side="right", expand=True, fill="both")

tk.Label(login_frame, text="LOG IN", bg="white", fg="#00796b", font=("Segoe UI", 24, "bold")).pack(pady=10)

tk.Label(login_frame, text="ID:", bg="white", font=("Segoe UI", 12)).pack(anchor="w", padx=10)
entry_id = ttk.Entry(login_frame, font=("Segoe UI", 12), width=15)
entry_id.pack(fill="x", padx=10, pady=5)

tk.Label(login_frame, text="Password:", bg="white", font=("Segoe UI", 12)).pack(anchor="w", padx=10)
entry_password = ttk.Entry(login_frame, show="*", font=("Segoe UI", 12), width=15)
entry_password.pack(fill="x", padx=10, pady=5)

ttk.Button(login_frame, text="LOG IN", command=login).pack(pady=10)
ttk.Button(login_frame, text="SIGN UP", command=open_signup).pack(pady=10)
ttk.Button(login_frame, text="Cancel", command=root.destroy).pack(pady=5)

# Sign-Up Window
signup_window = tk.Toplevel(root)
signup_window.withdraw()  # Initially hidden
signup_window.title("Sign Up New User")
signup_window.geometry("400x300")
signup_window.configure(bg="white")

tk.Label(signup_window, text="New User ID:", bg="white", font=("Segoe UI", 12)).pack(anchor="w", padx=10, pady=5)
signup_id_entry = ttk.Entry(signup_window, font=("Segoe UI", 12))
signup_id_entry.pack(fill="x", padx=10)

tk.Label(signup_window, text="New Password:", bg="white", font=("Segoe UI", 12)).pack(anchor="w", padx=10, pady=5)
signup_password_entry = ttk.Entry(signup_window, show="*", font=("Segoe UI", 12))
signup_password_entry.pack(fill="x", padx=10)

tk.Label(signup_window, text="Role:", bg="white", font=("Segoe UI", 12)).pack(anchor="w", padx=10, pady=5)
role_combobox = ttk.Combobox(signup_window, values=["Manager", "Employee"], font=("Segoe UI", 12))
role_combobox.pack(fill="x", padx=10)

ttk.Button(signup_window, text="Sign Up", command=signup_user).pack(pady=10)
ttk.Button(signup_window, text="Cancel", command=signup_window.withdraw).pack(pady=5)

root.mainloop()
