import streamlit as st
import fitz
import easyocr
import io
from PIL import Image, ImageDraw, ImageFont
from deep_translator import GoogleTranslator
import numpy as np
import arabic_reshaper
from bidi.algorithm import get_display
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

st.set_page_config(page_title="NovaTrans Pro", layout="wide")
st.title("✨ NovaTrans Pro - Final Stability")

@st.cache_resource
def load_reader():
    return easyocr.Reader(['en'])

reader = load_reader()
uploaded_file = st.file_uploader("📂 ارفع ملزمة PDF:", type=["pdf"])

if uploaded_file:
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    
    if st.button("🚀 ابدأ المعالجة"):
        with st.spinner("جاري المعالجة..."):
            pdf_buffer = io.BytesIO()
            c = canvas.Canvas(pdf_buffer, pagesize=letter)
            
            for page in doc:
                pix = page.get_pixmap()
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                draw = ImageDraw.Draw(img)
                results = reader.readtext(np.array(img))
                
                for (bbox, text, prob) in results:
                    if prob > 0.1:
                        try:
                            pts = np.array(bbox, dtype=int)
                            x0, y0 = pts[:, 0].min(), pts[:, 1].min()
                            x1, y1 = pts[:, 0].max(), pts[:, 1].max()
                            
                            translated = GoogleTranslator(source='en', target='ar').translate(text)
                            bidi_text = get_display(arabic_reshaper.reshape(translated))
                            
                            draw.rectangle([x0, y0, x1, y1], fill="white")
                            draw.text((x0, y0), text[:30], fill="black") # النص الإنجليزي
                            draw.text((x0, y0 + 12), bidi_text, fill="black") # الترجمة
                        except: continue
                
                # تصحيح طريقة الرسم في الـ PDF
                img_path = io.BytesIO()
                img.save(img_path, format='PNG')
                c.setPageSize((pix.width, pix.height))
                c.drawImage(img_path, 0, 0, width=pix.width, height=pix.height)
                c.showPage()
            
            c.save()
            st.success("✅ تم!")
            st.download_button("📥 تحميل PDF", pdf_buffer.getvalue(), "Result.pdf")
