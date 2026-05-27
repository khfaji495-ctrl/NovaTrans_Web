import streamlit as st
import fitz
import deepl
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from bidi.algorithm import get_display
import arabic_reshaper
import io
import pytesseract
from PIL import Image

# 1. الإعدادات الأساسية (تأكد أن هذه في بداية الكود)
st.set_page_config(page_title="سيد قط", layout="wide")

# 2. إعدادات المترجم
try:
    auth_key = st.secrets["DEEPL_API_KEY"]
    translator = deepl.Translator(auth_key)
except:
    st.error("⚠️ تأكد من إضافة API Key في الـ Secrets")
    st.stop()

# 3. واجهة رفع الملفات (تأكد أن هذا المتغير يُعرف هنا)
uploaded_file = st.file_uploader("😸 اسحب ملف الملزمة هنا", type="pdf")

# 4. المنطق الأساسي (يجب أن يكون داخل هذا الشرط)
if uploaded_file is not None:
    # قراءة الملف
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    total_pages = len(doc)
    
    # اختيار الصفحات
    start = st.number_input("من صفحة:", 1, total_pages, 1)
    end = st.number_input("إلى صفحة:", 1, total_pages, start)

    if st.button("😸 ابدأ الترجمة مع سيد قط"):
        with st.spinner("🐈 سيد قط يشتغل.. يرجى الانتظار"):
            pdf_buffer = io.BytesIO()
            c = canvas.Canvas(pdf_buffer)
            
            try:
                pdfmetrics.registerFont(TTFont('Arabic', 'font.ttf'))
            except:
                st.warning("⚠️ ملف الخط مفقود")

            y = 800
            for i in range(start - 1, end):
                page = doc.load_page(i)
                text = page.get_text().strip()
                
                # OCR إذا كان النص قليلاً
                if len(text) < 20:
                    pix = page.get_pixmap()
                    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                    text = pytesseract.image_to_string(img, lang='eng').strip()
                
                clean_text = " ".join(text.split())
                
                if clean_text:
                    if y < 100:
                        c.showPage()
                        y = 800
                    
                    c.setFont("Helvetica", 10)
                    c.drawString(50, y, clean_text[:100])
                    y -= 25
                    
                    try:
                        result = translator.translate_text(clean_text, target_lang="AR")
                        proper_arabic = get_display(arabic_reshaper.reshape(result.text))
                        c.setFont("Arabic", 10)
                        c.drawRightString(550, y, proper_arabic)
                        y -= 35
                    except:
                        continue
            
            c.save()
            pdf_buffer.seek(0)
            st.success("✅ أتم سيد قط المهمة!")
            st.download_button("📥 تحميل الملزمة", pdf_buffer, "SayedQatt_Translated.pdf", "application/pdf")
