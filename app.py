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
st.set_page_config(page_title="NovaTrans Pro - AI", layout="wide")
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
        with st.spinner("جاري التحليل والترجمة..."):
            pdf_buffer = io.BytesIO()
            c = canvas.Canvas(pdf_buffer)
            
            try:
                font = ImageFont.truetype("font.ttf", 14)
            except:
                font = ImageFont.load_default()

            for page_num in range(start_page - 1, end_page):
                page = doc.load_page(page_num)
                pix = page.get_pixmap()
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                draw = ImageDraw.Draw(img)
                results = reader.readtext(np.array(img))
                
                for (bbox, text, prob) in results:
                    if prob > 0.2:
                        # استخراج وتأمين الإحداثيات
                        x0, y0 = int(bbox[0][0]), int(bbox[0][1])
                        x1, y1 = int(bbox[2][0]), int(bbox[2][1])
                        
                        # تأمين حدود الرسم داخل الصورة
                        r_x0, r_y0 = max(0, x0), max(0, y0 - 30)
                        r_x1, r_y1 = min(img.width, x1), min(img.height, y1 + 10)
                        
                        # ترجمة
                        translated = GoogleTranslator(source='en', target='ar').translate(text)
                        bidi_text = get_display(arabic_reshaper.reshape(translated))
                        
                        # رسم الخلفية والترجمة
                        draw.rectangle([r_x0, r_y0, r_x1, r_y1], fill="white")
                        draw.text((r_x0, r_y0), text, fill="black", font=font)
                        draw.text((r_x0, r_y0 + 15), bidi_text, fill="black", font=font)
                
                # إضافة الصفحة للـ PDF
                img_byte_arr = io.BytesIO()
                img.save(img_byte_arr, format='PNG')
                c.setPageSize((pix.width, pix.height))
                c.drawImage(io.BytesIO(img_byte_arr.getvalue()), 0, 0, width=pix.width, height=pix.height)
                c.showPage()
            
            c.save()
            st.success("✅ تمت العملية بنجاح!")
            st.download_button("📥 تحميل PDF المترجم", pdf_buffer.getvalue(), "NovaTrans_Result.pdf")
