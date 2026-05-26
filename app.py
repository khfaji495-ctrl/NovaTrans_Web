import streamlit as st
import fitz
import easyocr
import io
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from deep_translator import GoogleTranslator
import arabic_reshaper
from bidi.algorithm import get_display
from reportlab.pdfgen import canvas

# --- الإعدادات وتصميم الواجهة ---
st.set_page_config(page_title="NovaTrans", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #2e3033; }
    h1 { color: #39ff14; text-align: center; text-shadow: 0 0 10px #39ff14; font-size: 50px; }
    </style>
""", unsafe_allow_html=True)

st.title("NovaTrans")

@st.cache_resource
def load_reader():
    return easyocr.Reader(['en'])

reader = load_reader()
uploaded_file = st.file_uploader("📂 ارفع ملزمة PDF:", type=["pdf"])

if uploaded_file:
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    total_pages = len(doc)
    
    col1, col2 = st.columns(2)
    start_page = col1.number_input("من صفحة:", 1, total_pages, 1)
    end_page = col2.number_input("إلى صفحة:", 1, total_pages, start_page)

    if st.button("🚀 معالجة وترجمة"):
        with st.spinner("جاري العمل..."):
            pdf_buffer = io.BytesIO()
            c = canvas.Canvas(pdf_buffer)
            
            for page_num in range(start_page - 1, end_page):
                pix = doc.load_page(page_num).get_pixmap()
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                draw = ImageDraw.Draw(img)
                results = reader.readtext(np.array(img))
                
                for (bbox, text, prob) in results:
                    if prob > 0.2:
                        pts = np.array(bbox, dtype=int)
                        x0, y0 = pts[:, 0].min(), pts[:, 1].min()
                        x1, y1 = pts[:, 0].max(), pts[:, 1].max()
                        
                        translated = GoogleTranslator(source='en', target='ar').translate(text)
                        bidi_text = get_display(arabic_reshaper.reshape(translated))
                        
                        # رسم خلفية وتغطية
                        draw.rectangle([x0, y0, x1, y1 + 15], fill="white")
                        # النص الإنجليزي فوق (خط افتراضي)
                        draw.text((x0, y0), text, fill="black")
                        # الترجمة تحت
                        draw.text((x0, y0 + 15), bidi_text, fill="black")
                
                # حفظ في الـ PDF
                img_byte_arr = io.BytesIO()
                img.save(img_byte_arr, format='PNG')
                c.setPageSize((pix.width, pix.height))
                c.drawImage(img_byte_arr, 0, 0, width=pix.width, height=pix.height)
                c.showPage()
            
            c.save()
            st.success("✅ تمت العملية!")
            st.download_button("📥 تحميل PDF", pdf_buffer.getvalue(), "NovaTrans.pdf")
