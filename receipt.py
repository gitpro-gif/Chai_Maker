import streamlit as st
from fpdf import FPDF

st.title("Chai Maker App")

name = st.text_input("Name")
dob = st.date_input("Date of Birth")
amount = st.text_input("Amount(amount enter in dollar)")
date = st.date_input("Date")
payment_id = st.text_input("Payment ID")

chai = st.subheader(f"Lets Make Chai for {name}")

add_masala = st.checkbox("Add Masala")
if add_masala:
    masala_msg = "Masala is added to Chai"
else:
    masala_msg = "No Masala added"

tea_type = st.radio("Pick your chai base", ["Milk", "Water", "Almond Milk"])
st.write(f"Selected base: {tea_type}")

flavour = st.selectbox("Choose Flavour", ["Adrak", "Elaichi", "Chocolate"])
st.write(f"Your selected Flavour is {flavour}")

sugar = st.slider("Select sugar level", 0, 5, 2)
st.write(f"Selected sugar level: {sugar}")

cups = st.number_input("How many cups?", min_value=1, max_value=10, step=1)
st.write(f"Selected number of cups: {cups}")

if st.button("Create Receipt"):
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
    
    # Add information to PDF
    pdf.cell(50, 10, "Name:", 0, 0)
    pdf.cell(100, 10, name, 0, 1)

    pdf.cell(50, 10, "DOB:", 0, 0)
    pdf.cell(100, 10, str(dob), 0, 1)

    pdf.cell(50, 10, "Amount Paid:", 0, 0)
    pdf.cell(100, 10, f"${amount}", 0, 1)

    pdf.cell(50, 10, "Date:", 0, 0)
    pdf.cell(100, 10, str(date), 0, 1)

    pdf.cell(50, 10, "Payment ID:", 0, 0)
    pdf.cell(100, 10, payment_id, 0, 1)

    pdf.cell(50, 10, "Masala:", 0, 0)
    pdf.cell(100, 10, masala_msg, 0, 1)

    pdf.cell(50, 10, "Tea Base:", 0, 0)
    pdf.cell(100, 10, tea_type, 0, 1)

    pdf.cell(50, 10, "Flavour:", 0, 0)
    pdf.cell(100, 10, flavour, 0, 1)

    pdf.cell(50, 10, "Sugar Level:", 0, 0)
    pdf.cell(100, 10, str(sugar), 0, 1)

    pdf.cell(50, 10, "Cups:", 0, 0)
    pdf.cell(100, 10, str(cups), 0, 1)

    pdf.ln(10)
    pdf.set_font("Arial", 'I', 12)
    pdf.cell(0, 10, "Thank you for using Chai Maker!", ln=True)

    pdf_bytes = pdf.output(dest="S").encode('latin-1')

    st.download_button(
        label="Download Receipt",
        data=pdf_bytes,
        file_name="receipt.pdf",
        mime="application/pdf",
    )
