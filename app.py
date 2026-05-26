import streamlit as st
import fitz  # مكتبة قراءة الـ PDF

st.title("NovaTrans Pro - قارئ PDF")

# زر لرفع الملف
uploaded_file = st.file_uploader("اختر ملف PDF للترجمة", type="pdf")

if uploaded_file is not None:
    # فتح ملف الـ PDF
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    
    st.write(f"عدد الصفحات: {len(doc)}")
    
    # عرض الصفحة الأولى كمثال
    page = doc.load_page(0)
    text = page.get_text()
    
    st.text_area("نص الصفحة الأولى:", text, height=300)
else:
    st.info("الرجاء رفع ملف PDF للبدء.")
