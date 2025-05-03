import streamlit as st
from fpdf import FPDF

st.set_page_config(page_title="Food Ordering App", layout="centered")

st.title("Food Ordering App")

st.sidebar.title("Menu Options")
menu_options = ["Chai", "Burger", "Pizza", "Pasta"]
selected_menu = st.sidebar.selectbox("Choose an item to order", menu_options)

st.sidebar.title("User Details")
name = st.sidebar.text_input("Name")
dob = st.sidebar.date_input("Date of Birth")
date = st.sidebar.date_input("Order Date")
payment_id = st.sidebar.text_input("Payment ID")

if "order_items" not in st.session_state:
    st.session_state.order_items = []
if "total_amount" not in st.session_state:
    st.session_state.total_amount = 0

menu_data = {
    "Chai": {
        "base": ["Milk", "Water", "Almond Milk"],
        "flavour": ["Adrak", "Elaichi", "Chocolate"],
        "sugar_range": range(0, 6),
        "price": 2.0
    },
    "Burger": {
        "flavour": ["Cheese", "Chicken", "Veggie"],
        "price": 5.0
    },
    "Pizza": {
        "flavour": ["Margherita", "Pepperoni", "BBQ Chicken"],
        "size": ["Small", "Medium", "Large"],
        "price": 8.0
    },
    "Pasta": {
        "flavour": ["Alfredo", "Arrabbiata", "Pesto"],
        "price": 6.0
    }
}

st.subheader(f"Ordering: {selected_menu}")
details = menu_data[selected_menu]

order_description = f"{selected_menu}: "

if selected_menu == "Chai":
    base = st.radio("Choose base", details["base"])
    flavour = st.selectbox("Choose flavour", details["flavour"])
    sugar = st.slider("Sugar level", 0, 5, 2)
    quantity = st.number_input("Quantity", min_value=1, max_value=10, step=1)
    masala = st.checkbox("Add Masala")
    masala_text = "with Masala" if masala else "no Masala"
    item_price = details["price"] * quantity
    order_description += f"{quantity} cup(s), Base: {base}, Flavour: {flavour}, Sugar: {sugar}, {masala_text}"
elif selected_menu == "Burger":
    flavour = st.selectbox("Choose flavour", details["flavour"])
    quantity = st.number_input("Quantity", min_value=1, max_value=10, step=1)
    item_price = details["price"] * quantity
    order_description += f"{quantity} Burger(s), Flavour: {flavour}"
elif selected_menu == "Pizza":
    flavour = st.selectbox("Choose flavour", details["flavour"])
    size = st.selectbox("Choose size", details["size"])
    quantity = st.number_input("Quantity", min_value=1, max_value=10, step=1)
    item_price = details["price"] * quantity
    order_description += f"{quantity} Pizza(s), Flavour: {flavour}, Size: {size}"
elif selected_menu == "Pasta":
    flavour = st.selectbox("Choose flavour", details["flavour"])
    quantity = st.number_input("Quantity", min_value=1, max_value=10, step=1)
    item_price = details["price"] * quantity
    order_description += f"{quantity} Pasta(s), Flavour: {flavour}"

if st.button("Add to Order"):
    st.session_state.order_items.append(order_description)
    st.session_state.total_amount += item_price
    st.success(f"{selected_menu} added to order!")

st.subheader("Order Summary")
if st.session_state.order_items:
    for item in st.session_state.order_items:
        st.write(f"- {item}")
    st.write(f"**Total Amount: ${st.session_state.total_amount:.2f}**")
else:
    st.info("No items added yet.")

if st.button("Proceed to Payment"):
    pdf = FPDF()
    pdf.add_page()

    pdf.set_fill_color(245, 245, 245)
    pdf.rect(5, 5, 200, 287, 'F')

    pdf.set_font("Arial", 'B', 18)
    pdf.set_text_color(0, 102, 204)
    pdf.cell(0, 20, "Payment Receipt", ln=True, align='C')

    pdf.set_font("Arial", '', 14)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(10)

    pdf.cell(50, 10, "Name:", 0, 0)
    pdf.cell(100, 10, name, 0, 1)
    pdf.cell(50, 10, "DOB:", 0, 0)
    pdf.cell(100, 10, str(dob), 0, 1)
    pdf.cell(50, 10, "Date:", 0, 0)
    pdf.cell(100, 10, str(date), 0, 1)
    pdf.cell(50, 10, "Payment ID:", 0, 0)
    pdf.cell(100, 10, payment_id, 0, 1)
    pdf.cell(50, 10, "Amount Paid:", 0, 0)
    pdf.cell(100, 10, f"${st.session_state.total_amount:.2f}", 0, 1)

    pdf.ln(5)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Order Details:", ln=True)
    pdf.set_font("Arial", '', 12)

    for item in st.session_state.order_items:
        pdf.multi_cell(0, 10, f"- {item}")

    pdf.ln(10)
    pdf.set_font("Arial", 'I', 12)
    pdf.cell(0, 10, "Thank you for using Food Ordering App!", ln=True)

    pdf_bytes = pdf.output(dest="S").encode('latin-1')
    st.download_button(
        label="Download Receipt",
        data=pdf_bytes,
        file_name="receipt.pdf",
        mime="application/pdf",
    )
