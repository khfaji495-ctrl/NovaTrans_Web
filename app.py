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

# --- الإعدادات والواجهة النيون ---
st.set_page_config(page_title="NovaTrans Pro - AI", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #2e3033; }
    h1 { color: #39ff14; text-align: center; text-shadow: 0 0 10px #39ff14; }
    </style>
""", unsafe_allow_html=True)

st.title("✨ NovaTrans Pro - AI Vision")

@st.cache_resource
def load_reader():
    return easyocr.Reader(['en'])

reader = load_reader()

uploaded_file = st.file_uploader("📂 ارفع ملزمة (PDF):", type=["pdf"])

if uploaded_file:
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    total_pages = len(doc)
    
    start_page = st.number_input("من صفحة:", 1, total_pages, 1)
    end_page = st.number_input("إلى صفحة:", 1, total_pages, start_page)

    if st.button("🚀 معالجة وترجمة بصرية"):
        with st.spinner("جاري التحليل والترجمة الذكية..."):
            pdf_buffer = io.BytesIO()
            c = canvas.Canvas(pdf_buffer)
            
            try:
                font = ImageFont.truetype("font.ttf", 16)
            except:
                font = ImageFont.load_default()

            for page_num in range(start_page - 1, end_page):
                pix = doc.load_page(page_num).get_pixmap()
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                draw = ImageDraw.Draw(img)
                results = reader.readtext(np.array(img))
                
                for (bbox, text, prob) in results:
                    if prob > 0.2:
                        translated = GoogleTranslator(source='en', target='ar').translate(text)
                        reshaped_text = arabic_reshaper.reshape(translated)
                        bidi_text = get_display(reshaped_text)
                        
                        x0, y0 = int(bbox[0][0]), int(bbox[0][1])
                        x1, y1 = int(bbox[2][0]), int(bbox[2][1])
                        
                        # رسم الخلفية البيضاء
                        draw.rectangle([x0, y0 - 30, x1, y1 + 10], fill="white")
                        # طباعة الإنجليزي فوق
                        draw.text((x0, y0 - 25), text, fill="black", font=font)
                        # طباعة العربي تحت
                        draw.text((x0, y0), bidi_text, fill="black", font=font)
                
                # حفظ الصورة المترجمة كصفحة في الـ PDF
                img_byte_arr = io.BytesIO()
                img.save(img_byte_arr, format='PNG')
                c.setPageSize((pix.width, pix.height))
                c.drawImage(io.BytesIO(img_byte_arr.getvalue()), 0, 0, width=pix.width, height=pix.height)
                c.showPage()
            
            c.save()
            st.success("✅ تم الانتهاء بنجاح!")
            st.download_button("📥 تحميل الملزمة المترجمة PDF", pdf_buffer.getvalue(), "NovaTrans_Result.pdf")
