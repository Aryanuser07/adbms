import psycopg2
import tkinter as tk
from tkinter import messagebox

def connect_db():
    return psycopg2.connect(
        host="localhost",
        user="postgres",
        password="0763",
        database="bake"
    )

def view_items():
    for widget in items_frame.winfo_children():
        widget.destroy()
    
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bakery_items")
    items = cursor.fetchall()
    conn.close()

    for row in items:
        item_label = tk.Label(items_frame, text=f"{row[0]}: {row[1]} - ${row[2]:.2f}", bg="#add8e6", fg="black")
        item_label.pack()

def place_order():
    item_id = entry_item_id.get()
    quantity = entry_quantity.get()

    if not item_id or not quantity.isdigit():
        messagebox.showerror("Input Error", "Please enter a valid item ID and quantity.")
        return

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT price FROM bakery_items WHERE id = %s", (item_id,))
    item = cursor.fetchone()
    
    if not item:
        messagebox.showerror("Error", "Item ID does not exist.")
        conn.close()
        return

    total_price = item[0] * int(quantity)
    cursor.execute("INSERT INTO orders (item_id, quantity, total_price) VALUES (%s, %s, %s)",
                   (item_id, quantity, total_price))
    conn.commit()
    conn.close()
    
    messagebox.showinfo("Success", "Order placed successfully!")
    clear_order_fields()
    
def clear_order_fields():
    entry_item_id.delete(0, tk.END)
    entry_quantity.delete(0, tk.END)

def view_orders():
    for widget in orders_frame.winfo_children():
        widget.destroy()

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders")
    orders = cursor.fetchall()
    conn.close()

    for row in orders:
        order_label = tk.Label(orders_frame, text=f"Order ID {row[0]}, Item ID {row[1]}, Quantity {row[2]}, Total: ${row[3]:.2f}", bg="#90ee90", fg="black")
        order_label.pack()

def delete_order():
    order_id = entry_order_id.get()

    if not order_id.isdigit():
        messagebox.showerror("Input Error", "Please enter a valid order ID.")
        return

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM orders WHERE order_id = %s", (order_id,))
    conn.commit()
    conn.close()
    
    messagebox.showinfo("Success", "Order deleted successfully!")
    entry_order_id.delete(0, tk.END)
    view_orders()

root = tk.Tk()
root.title("Bakery Ordering System")
root.geometry('800x700')
root.configure(bg="#d3d3d3")  

items_frame = tk.Frame(root, bg="#add8e6") 
items_frame.pack(pady=10)

orders_frame = tk.Frame(root, bg="#90ee90")  
orders_frame.pack(pady=10)

button_frame = tk.Frame(root, bg="#d3d3d3")  
button_frame.pack(pady=10)


tk.Button(button_frame, text="Place Order", command=place_order, bg="#4682b4", fg="white").pack(side=tk.LEFT, padx=30)
tk.Button(button_frame, text="View Bakery Items", command=view_items, bg="#4682b4", fg="white").pack(side=tk.LEFT, padx=30)
tk.Button(button_frame, text="View Orders", command=view_orders, bg="#4682b4", fg="white").pack(side=tk.LEFT, padx=30)
tk.Button(button_frame, text="Delete Order", command=delete_order, bg="#4682b4", fg="white").pack(side=tk.LEFT, padx=30)


tk.Label(root, text="", bg="#d3d3d3").pack()
tk.Label(root, text="Item ID:", bg="#d3d3d3").pack()
entry_item_id = tk.Entry(root, bg="#f5f5f5")  
entry_item_id.pack()

tk.Label(root, text="Quantity:", bg="#d3d3d3").pack()
entry_quantity = tk.Entry(root, bg="#f5f5f5")
entry_quantity.pack()

tk.Label(root, text="Order ID to delete:", bg="#d3d3d3").pack()
entry_order_id = tk.Entry(root, bg="#f5f5f5")
entry_order_id.pack()

root.mainloop()
