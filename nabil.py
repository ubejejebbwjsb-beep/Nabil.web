import streamlit as st

# 1. السطرين بتوع الـ CSS (دول يفضلوا في الأول خالص دايماً)
with open("web.css", "r", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# 2. هنا بقى حط كل الأكواد القديمة بتاعتك اللي كانت في الملف
# (زي الأزرار، النصوص، القوائم، أو أي حاجة كنت كاتبها قبل كدة)

#st.title("موقع نبيل المطور 🚀")
#st.write("هنا بقية الأكواد القديمة بتاعتك هتشتغل عادي جداً...")

# حط أكوادك هنا بالترتيب تحت بعضها 👇
import streamlit as st

import streamlit as st
import pandas as pd
from datetime import datetime

# ============== إعدادات عامة ==============
st.set_page_config(page_title="Nabil Shop", page_icon="💎", layout="centered")

# قاموس الأسعار والصور (سهل التعديل والإضافة)
PRODUCTS = {
    "chips": {"price": 10, "emoji": "🥔"},
    "pepsi": {"price": 15, "emoji": "🥤"},
    "big chips": {"price": 20, "emoji": "🍟"},
}

# إنشاء "سجل فواتير" داخل الجلسة (يحفظ طول مدة استخدام التطبيق)
if "invoices" not in st.session_state:
    st.session_state.invoices = []

# ============== عنوان الموقع ==============
st.title("Welcome to the Nabil Website 💎")
st.write("اختار منتجاتك وحدد الكمية، وشوف فاتورتك فوراً 🧾")
st.write("---")

# ============== اسم العميل ==============
name = st.text_input("👤 Enter your name:")

st.write("---")

# ============== اختيار المنتجات بالأعمدة ==============
col1, col2 = st.columns(2)

with col1:
    st.subheader("🛍️ المنتج الأول")
    choice = st.selectbox("اختر المنتج الأول:", list(PRODUCTS.keys()), key="choice1")
    qty1 = st.number_input("الكمية:", min_value=1, max_value=20, value=1, step=1, key="qty1")
    price1 = PRODUCTS[choice]["price"]
    st.write(f"{PRODUCTS[choice]['emoji']} السعر: {price1} LE × {qty1} = **{price1 * qty1} LE**")

with col2:
    st.subheader("🛍️ المنتج الثاني")
    choice2 = st.selectbox("اختر المنتج الثاني:", list(PRODUCTS.keys()), key="choice2")
    qty2 = st.number_input("الكمية:", min_value=1, max_value=20, value=1, step=1, key="qty2")
    price2 = PRODUCTS[choice2]["price"]
    st.write(f"{PRODUCTS[choice2]['emoji']} السعر: {price2} LE × {qty2} = **{price2 * qty2} LE**")

st.write("---")

# ============== حساب الإجمالي والخصم ==============
subtotal = (price1 * qty1) + (price2 * qty2)

DISCOUNT_THRESHOLD = 30   # الحد الأدنى للخصم
DISCOUNT_RATE = 0.10      # نسبة الخصم 10%

discount = 0
if subtotal > DISCOUNT_THRESHOLD:
    discount = subtotal * DISCOUNT_RATE

total_price = subtotal - discount

# عرض ملخص سريع قبل الشراء
st.write(f"**الإجمالي قبل الخصم:** {subtotal} LE")
if discount > 0:
    st.success(f"🎉 مبروك! حصلت على خصم {int(DISCOUNT_RATE*100)}% = {discount:.2f} LE")
st.write(f"### 💰 الإجمالي النهائي: {total_price:.2f} LE")

st.write("---")

# ============== زر الشراء وإصدار الفاتورة ==============
if st.button("Buy Now 🛒"):
    if not name.strip():
        st.warning("⚠️ من فضلك أدخل اسمك أولاً قبل إتمام الشراء")
    else:
        st.write("### 📄 Receipt")
        st.write(f"**Customer Name:** {name}")
        st.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        st.write("---")
        st.write(f"{PRODUCTS[choice]['emoji']} **{choice}** × {qty1} = {price1 * qty1} LE")
        st.write(f"{PRODUCTS[choice2]['emoji']} **{choice2}** × {qty2} = {price2 * qty2} LE")
        st.write("---")
        st.write(f"Subtotal: {subtotal} LE")
        if discount > 0:
            st.write(f"Discount ({int(DISCOUNT_RATE*100)}%): -{discount:.2f} LE")
        st.write(f"### Total Price: {total_price:.2f} LE")

        # حفظ الفاتورة في السجل
        invoice_record = {
            "Customer": name,
            "Date": datetime.now().strftime('%Y-%m-%d %H:%M'),
            "Item 1": f"{choice} x{qty1}",
            "Item 2": f"{choice2} x{qty2}",
            "Subtotal": subtotal,
            "Discount": round(discount, 2),
            "Total": round(total_price, 2),
        }
        st.session_state.invoices.append(invoice_record)

        # تجهيز الفاتورة كنص قابل للتحميل
        receipt_text = f"""Nabil Shop - Receipt
Customer Name: {name}
Date: {invoice_record['Date']}
---------------------------
{choice} x{qty1} = {price1 * qty1} LE
{choice2} x{qty2} = {price2 * qty2} LE
---------------------------
Subtotal: {subtotal} LE
Discount: {discount:.2f} LE
Total: {total_price:.2f} LE
"""
        st.download_button(
            label="⬇️ تحميل الفاتورة",
            data=receipt_text,
            file_name=f"receipt_{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
        )

# ============== سجل كل الفواتير (Session) ==============
if st.session_state.invoices:
    st.write("---")
    st.write("### 🧾 سجل الفواتير (الجلسة الحالية)")
    df = pd.DataFrame(st.session_state.invoices)
    st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ تحميل كل الفواتير (CSV)",
        data=csv,
        file_name="all_invoices.csv",
        mime="text/csv",
    )