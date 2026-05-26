import streamlit as st
import fitz
import easyocr
import io
import numpy as np
from PIL import Image, ImageDraw
from deep_translator import GoogleTranslator
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# 1. إعدادات الواجهة
st.set_page_config(page_title="NovaTrans", layout="wide")
st.markdown("<style>.stApp { background-color: #333; } h1 { color: #39ff14; text-align: center; }</style>", unsafe_allow_html=True)
st.title("NovaTrans")

@st.cache_resource
def load_reader():
    return easyocr.Reader(['en'])

reader = load_reader()

uploaded_file = st.file_uploader("📂 ارفع ملزمة PDF:", type=["pdf"])

if uploaded_file:
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    
    if st.button("🚀 معالجة وترجمة"):
        with st.spinner("جاري التحليل..."):
            pdf_buffer = io.BytesIO()
            c = canvas.Canvas(pdf_buffer, pagesize=letter)
            
            for page in doc:
                # محاولة استخراج النص
                text = page.get_text()
                
                # إذا كان النص رموزاً أو فارغاً، نستخدم OCR
                if len(text.strip()) < 10:
                    pix = page.get_pixmap()
                    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                    results = reader.readtext(np.array(img))
                    
                    # تجميع النص من الـ OCR
                    text = " ".join([res[1] for res in results])
                
                # الترجمة
                if text.strip():
                    translated = GoogleTranslator(source='auto', target='ar').translate(text[:2000])
                    
                    c.setFont("Helvetica-Bold", 12)
                    c.drawString(50, 750, "English Text (Extracted):")
                    c.setFont("Helvetica", 10)
                    c.drawString(50, 730, text[:100])
                    
                    c.setFont("Helvetica-Bold", 12)
                    c.drawString(50, 700, "الترجمة:")
                    c.setFont("Helvetica", 10)
                    c.drawString(50, 680, translated[:100])
                
                c.showPage()
            
            c.save()
            st.success("✅ تمت العملية!")
            st.download_button("📥 تحميل PDF", pdf_buffer.getvalue(), "NovaTrans.pdf")
