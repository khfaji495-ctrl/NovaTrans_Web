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

# إعدادات الصفحة
st.set_page_config(page_title="سيد قط", layout="wide")

# إعداد المترجم
auth_key = st.secrets.get("DEEPL_API_KEY")
translator = deepl.Translator(auth_key) if auth_key else None

uploaded_file = st.file_uploader("😸 اسحب ملف الملزمة هنا", type="pdf")

if uploaded_file is not None:
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    start = st.number_input("من صفحة:", 1, len(doc), 1)
    end = st.number_input("إلى صفحة:", 1, len(doc), start)

    if st.button("😸 ابدأ الترجمة مع سيد قط"):
        with st.spinner("جاري المعالجة.."):
            pdf_buffer = io.BytesIO()
            c = canvas.Canvas(pdf_buffer)
            
            # تسجيل الخط العربي (تأكد من وجود font.ttf)
            try:
                pdfmetrics.registerFont(TTFont('Arabic', 'font.ttf'))
            except:
                st.warning("⚠️ ملف الخط مفقود، قد يظهر النص بشكل مربعات.")
            
            y = 750
            for i in range(start - 1, end):
                page = doc.load_page(i)
                text = page.get_text().strip()
                
                # إذا كانت الصفحة صورة (OCR)
                if len(text) < 50:
                    pix = page.get_pixmap()
                    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                    text = pytesseract.image_to_string(img).strip()
                
                # تنظيف النص لمنع الفراغات الكبيرة
                clean_text = " ".join(text.split())
                
                if clean_text:
                    if y < 100:
                        c.showPage()
                        y = 750
                    
                    # طباعة النص الإنجليزي (أصلي)
                    c.setFont("Helvetica", 10)
                    c.drawString(50, y, clean_text[:100])
                    y -= 20
                    
                    # ترجمة وطباعة النص العربي
                    if translator:
                        translated = translator.translate_text(clean_text, target_lang="AR").text
                        proper_arabic = get_display(arabic_reshaper.reshape(translated))
                        c.setFont("Arabic", 10)
                        c.drawRightString(550, y, proper_arabic)
                        y -= 30 # هذه المسافة تتحكم في تباعد الأسطر
            
            c.save()
            pdf_buffer.seek(0)
            st.success("✅ تم!")
            st.download_button("📥 تحميل", pdf_buffer, "Translated.pdf", "application/pdf")
