import streamlit as st
import fitz
import easyocr
import io
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from deep_translator import GoogleTranslator
import arabic_reshaper
from bidi.algorithm import get_display
from fpdf import FPDF

# --- التصميم ---
st.set_page_config(page_title="NovaTrans", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #2e3033; }
    h1 { color: #39ff14; text-align: center; text-shadow: 0 0 10px #39ff14; }
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
    start_page = st.number_input("من صفحة:", 1, total_pages, 1)
    end_page = st.number_input("إلى صفحة:", 1, total_pages, start_page)

    if st.button("🚀 معالجة وترجمة"):
        with st.spinner("جاري المعالجة..."):
            pdf = FPDF()
            for page_num in range(start_page - 1, end_page):
                pix = doc.load_page(page_num).get_pixmap()
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                draw = ImageDraw.Draw(img)
                results = reader.readtext(np.array(img))
                
                for (bbox, text, prob) in results:
                    if prob > 0.2:
                        pts = np.array(bbox, dtype=int)
                        # حماية الإحداثيات: نضمن أنها داخل حدود الصورة ولا يوجد قيم سالبة
                        x0 = max(0, pts[:, 0].min())
                        y0 = max(0, pts[:, 1].min())
                        x1 = min(img.width, pts[:, 0].max())
                        y1 = min(img.height, pts[:, 1].max())
                        
                        translated = GoogleTranslator(source='en', target='ar').translate(text)
                        bidi_text = get_display(arabic_reshaper.reshape(translated))
                        
                        # رسم مستطيل أبيض لتغطية النص الأصلي (فقط إذا كانت الأبعاد صحيحة)
                        if x1 > x0 and y1 > y0:
                            draw.rectangle([x0, y0, x1, y1 + 15], fill="white")
                            draw.text((x0, y0), text, fill="black")
                            draw.text((x0, y0 + 12), bidi_text, fill="black")
                
                # حفظ الصورة في الـ PDF
                img_byte_arr = io.BytesIO()
                img.save(img_byte_arr, format='PNG')
                pdf.add_page()
                pdf.image(img_byte_arr, x=0, y=0, w=210)
            
            output = io.BytesIO(pdf.output(dest='S').encode('latin-1'))
            st.success("✅ تمت العملية!")
            st.download_button("📥 تحميل PDF", output, "NovaTrans.pdf")
