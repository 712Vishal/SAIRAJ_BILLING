import sqlite3
import re
import random
import string
import streamlit as st
from datetime import datetime, date
import time

# Initialize session state
if 'cart' not in st.session_state:
    st.session_state.cart = []
    st.session_state.cart_dict = {}
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.current_bill = None
    st.session_state.bill_generated = False
    st.session_state.selected_category = None
    st.session_state.selected_subcat = None
    st.session_state.selected_product = None

# Database connection
conn = sqlite3.connect("./Database/store.db")
cur = conn.cursor()

# Utility functions
def random_bill_number(stringLength):
    lettersAndDigits = string.ascii_letters.upper() + string.digits
    strr = ''.join(random.choice(lettersAndDigits) for i in range(stringLength-2))
    return ('CC'+strr)

def valid_phone(phn):
    if re.match(r"[789]\d{9}$", phn):
        return True
    return False

def get_categories():
    cur.execute("SELECT DISTINCT product_cat FROM raw_inventory")
    return [row[0] for row in cur.fetchall()]

def get_subcategories(category):
    cur.execute("SELECT DISTINCT product_subcat FROM raw_inventory WHERE product_cat = ?", [category])
    return [row[0] for row in cur.fetchall()]

def get_products(category, subcategory):
    cur.execute("SELECT product_name FROM raw_inventory WHERE product_cat = ? AND product_subcat = ?", 
               [category, subcategory])
    return [row[0] for row in cur.fetchall()]

def get_product_details(product_name):
    cur.execute("SELECT mrp, stock FROM raw_inventory WHERE product_name = ?", [product_name])
    return cur.fetchone()

# Login Page
def login_page():
    st.title("Employee Login")
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Login")
        
        if submit_button:
            cur.execute("SELECT * FROM employee WHERE emp_id = ? AND password = ?", [username, password])
            results = cur.fetchall()
            
            if results:
                st.success("Login successful!")
                st.session_state.logged_in = True
                st.session_state.username = username
                st.experimental_rerun()
            else:
                st.error("Incorrect username or password.")

# Billing Page
def billing_page():
    st.title("Billing Software")
    st.write(f"Logged in as: {st.session_state.username}")
    
    # Logout button
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.cart = []
        st.session_state.cart_dict = {}
        st.session_state.current_bill = None
        st.session_state.bill_generated = False
        st.experimental_rerun()
    
    # Customer details
    with st.expander("Customer Details", expanded=True):
        col1, col2 = st.columns(2)
        cust_name = col1.text_input("Customer Name", key="cust_name")
        cust_num = col2.text_input("Customer Phone", key="cust_num")
        
        # Search bill
        search_bill = st.text_input("Search Bill by Number")
        if st.button("Search Bill"):
            if search_bill:
                cur.execute("SELECT * FROM bill WHERE bill_no = ?", [search_bill.strip()])
                results = cur.fetchone()
                
                if results:
                    st.session_state.current_bill = {
                        'bill_no': results[0],
                        'date': results[1],
                        'customer_name': results[2],
                        'customer_no': results[3],
                        'details': results[4]
                    }
                    st.session_state.bill_generated = True
                    st.success("Bill found!")
                else:
                    st.error("Bill not found.")
    
    # Product selection
    with st.expander("Add Products", expanded=True):
        categories = get_categories()
        selected_category = st.selectbox(
            "Category", 
            ["Select"] + categories, 
            key="category",
            index=0 if not st.session_state.selected_category else categories.index(st.session_state.selected_category)+1
        )
        
        if selected_category != "Select":
            st.session_state.selected_category = selected_category
            subcategories = get_subcategories(selected_category)
            selected_subcat = st.selectbox(
                "Subcategory", 
                ["Select"] + subcategories, 
                key="subcategory",
                index=0 if not st.session_state.selected_subcat else subcategories.index(st.session_state.selected_subcat)+1
            )
            
            if selected_subcat != "Select":
                st.session_state.selected_subcat = selected_subcat
                products = get_products(selected_category, selected_subcat)
                selected_product = st.selectbox(
                    "Product", 
                    ["Select"] + products, 
                    key="product",
                    index=0 if not st.session_state.selected_product else products.index(st.session_state.selected_product)+1
                )
                
                if selected_product != "Select":
                    st.session_state.selected_product = selected_product
                    mrp, stock = get_product_details(selected_product)
                    st.write(f"Price: ₹{mrp} | In Stock: {stock}")
                    
                    qty = st.number_input("Quantity", min_value=1, max_value=stock, value=1, key="qty")
                    
                    col1, col2, col3 = st.columns(3)
                    if col1.button("Add to Cart"):
                        item = {
                            'name': selected_product,
                            'price': mrp,
                            'qty': qty,
                            'total': mrp * qty
                        }
                        st.session_state.cart.append(item)
                        
                        # Update cart dictionary for stock management
                        if selected_product in st.session_state.cart_dict:
                            st.session_state.cart_dict[selected_product] += qty
                        else:
                            st.session_state.cart_dict[selected_product] = qty
                        
                        st.success(f"Added {qty} x {selected_product} to cart")
                    
                    if col2.button("Remove Last Item"):
                        if st.session_state.cart:
                            removed_item = st.session_state.cart.pop()
                            st.session_state.cart_dict[removed_item['name']] -= removed_item['qty']
                            if st.session_state.cart_dict[removed_item['name']] <= 0:
                                del st.session_state.cart_dict[removed_item['name']]
                            st.success(f"Removed {removed_item['name']} from cart")
                        else:
                            st.warning("Cart is empty")
                    
                    if col3.button("Clear Cart"):
                        st.session_state.cart = []
                        st.session_state.cart_dict = {}
                        st.success("Cart cleared")
    
    # Cart display
    with st.expander("Current Bill", expanded=True):
        if st.session_state.cart:
            st.write("### Items in Cart")
            for idx, item in enumerate(st.session_state.cart, 1):
                st.write(f"{idx}. {item['name']} - {item['qty']} x ₹{item['price']} = ₹{item['total']}")
            
            total = sum(item['total'] for item in st.session_state.cart)
            st.write(f"### Total: ₹{total}")
            
            # Bill actions
            col1, col2, col3 = st.columns(3)
            if col1.button("Generate Bill"):
                if not cust_name:
                    st.error("Please enter customer name")
                elif not cust_num:
                    st.error("Please enter customer phone")
                elif not valid_phone(cust_num):
                    st.error("Please enter valid phone number")
                else:
                    # Generate bill details
                    bill_details = "Item\t\tQuantity\tPrice\tTotal\n"
                    bill_details += "-"*50 + "\n"
                    for item in st.session_state.cart:
                        bill_details += f"{item['name']}\t{item['qty']}\t₹{item['price']}\t₹{item['total']}\n"
                    bill_details += "-"*50 + "\n"
                    bill_details += f"Total\t\t\t\t₹{total}"
                    
                    # Save to database
                    bill_no = random_bill_number(8)
                    bill_date = date.today().strftime("%Y-%m-%d")
                    
                    cur.execute(
                        "INSERT INTO bill(bill_no, date, customer_name, customer_no, bill_details) VALUES(?,?,?,?,?)",
                        [bill_no, bill_date, cust_name, cust_num, bill_details]
                    )
                    
                    # Update inventory
                    for product, qty in st.session_state.cart_dict.items():
                        cur.execute(
                            "UPDATE raw_inventory SET stock = stock - ? WHERE product_name = ?",
                            [qty, product]
                        )
                    
                    conn.commit()
                    
                    st.session_state.current_bill = {
                        'bill_no': bill_no,
                        'date': bill_date,
                        'customer_name': cust_name,
                        'customer_no': cust_num,
                        'details': bill_details
                    }
                    st.session_state.bill_generated = True
                    st.success("Bill generated successfully!")
            
            if col2.button("Clear Bill"):
                st.session_state.cart = []
                st.session_state.cart_dict = {}
                st.session_state.current_bill = None
                st.session_state.bill_generated = False
                st.experimental_rerun()
            
            if col3.button("Print Bill"):
                st.warning("Print functionality would be implemented here")
        else:
            st.info("Cart is empty. Add products to generate bill.")
    
    # Display current bill if generated
    if st.session_state.bill_generated and st.session_state.current_bill:
        with st.expander("Generated Bill Details", expanded=True):
            st.write(f"**Bill No:** {st.session_state.current_bill['bill_no']}")
            st.write(f"**Date:** {st.session_state.current_bill['date']}")
            st.write(f"**Customer:** {st.session_state.current_bill['customer_name']}")
            st.write(f"**Phone:** {st.session_state.current_bill['customer_no']}")
            st.text(st.session_state.current_bill['details'])

# Main app flow
def main():
    if not st.session_state.logged_in:
        login_page()
    else:
        billing_page()

if __name__ == "__main__":
    main()
