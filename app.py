import streamlit as st
import fitz
import io
import numpy as np
from PIL import Image, ImageDraw
from deep_translator import GoogleTranslator
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# إعدادات الواجهة
st.set_page_config(page_title="NovaTrans", layout="wide")
st.markdown("<style>.stApp { background-color: #333; } h1 { color: #39ff14; text-align: center; }</style>", unsafe_allow_html=True)
st.title("NovaTrans")

uploaded_file = st.file_uploader("📂 ارفع ملزمة PDF:", type=["pdf"])

if uploaded_file:
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    
    col1, col2 = st.columns(2)
    start_page = col1.number_input("من صفحة:", 1, len(doc), 1)
    end_page = col2.number_input("إلى صفحة:", 1, len(doc), start_page)

    if st.button("🚀 ابدأ المعالجة"):
        with st.spinner("جاري الترجمة وحفظ الملف..."):
            pdf_buffer = io.BytesIO()
            c = canvas.Canvas(pdf_buffer, pagesize=letter)
            
            for i in range(start_page - 1, end_page):
                page = doc.load_page(i)
                text = page.get_text()
                
                if text.strip():
                    # ترجمة النص
                    translated = GoogleTranslator(source='auto', target='ar').translate(text[:2000])
                    
                    # الرسم على الـ PDF مباشرة بدلاً من معالجة الصور الثقيلة
                    c.setFont("Helvetica-Bold", 14)
                    c.drawString(50, 750, "English Text:")
                    c.setFont("Helvetica", 12)
                    c.drawString(50, 730, text[:80]) # عرض السطر الأول
                    
                    c.setFont("Helvetica-Bold", 14)
                    c.drawString(50, 700, "الترجمة:")
                    c.setFont("Helvetica", 12)
                    c.drawString(50, 680, translated[:80])
                
                c.showPage()
            
            c.save()
            st.success("✅ تمت العملية بنجاح!")
            st.download_button("📥 تحميل ملف NovaTrans PDF", pdf_buffer.getvalue(), "NovaTrans.pdf")
