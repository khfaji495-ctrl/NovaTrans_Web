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

# إعداد الواجهة
st.set_page_config(page_title="NovaTrans Pro", layout="wide")
st.title("✨ NovaTrans Pro - Final Version")

# تحميل القارئ (مع كاش لزيادة السرعة)
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

    if st.button("🚀 ابدأ المعالجة"):
        with st.spinner("جاري الترجمة الذكية..."):
            pdf_buffer = io.BytesIO()
            c = canvas.Canvas(pdf_buffer)
            
            for page_num in range(start_page - 1, end_page):
                page = doc.load_page(page_num)
                pix = page.get_pixmap()
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                draw = ImageDraw.Draw(img)
                results = reader.readtext(np.array(img))
                
                for (bbox, text, prob) in results:
                    if prob > 0.1: # خفضنا النسبة لضمان قراءة النص
                        try:
                            # حساب الإحداثيات بأمان
                            pts = np.array(bbox, dtype=int)
                            x0, y0 = pts[:, 0].min(), pts[:, 1].min()
                            x1, y1 = pts[:, 0].max(), pts[:, 1].max()
                            
                            # ترجمة
                            translated = GoogleTranslator(source='en', target='ar').translate(text)
                            bidi_text = get_display(arabic_reshaper.reshape(translated))
                            
                            # رسم مستطيل أبيض يغطي النص الأصلي
                            draw.rectangle([x0, y0, x1, y1], fill="white")
                            
                            # رسم النص الجديد (الإنجليزي فوق والعربي تحت)
                            draw.text((x0, y0), text, fill="black")
                            draw.text((x0, y0 + 12), bidi_text, fill="black")
                        except Exception as e:
                            continue # في حال حدوث خطأ في سطر معين، انتقل للذي يليه فوراً
                
                # إضافة الصفحة للـ PDF
                img_byte_arr = io.BytesIO()
                img.save(img_byte_arr, format='PNG')
                c.setPageSize((pix.width, pix.height))
                c.drawImage(io.BytesIO(img_byte_arr.getvalue()), 0, 0, width=pix.width, height=pix.height)
                c.showPage()
            
            c.save()
            st.success("✅ تمت المعالجة!")
            st.download_button("📥 تحميل الملزمة المترجمة", pdf_buffer.getvalue(), "Result.pdf")
