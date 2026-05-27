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

# إعدادات الـ OCR (تأكد من تثبيت tesseract-ocr على السيرفر)
# pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract' # قد تحتاج لهذا المسار على السيرفر

# ... (نفس إعدادات CSS والـ UI السابقة) ...

if uploaded_file is not None:
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    # ... (نفس كود المدخلات start/end) ...

    if st.button("😸 ابدأ الترجمة مع سيد قط"):
        with st.spinner("🐈 سيد قط يعمل الآن.. يرجى الانتظار"):
            pdf_buffer = io.BytesIO()
            c = canvas.Canvas(pdf_buffer)
            
            try:
                pdfmetrics.registerFont(TTFont('Arabic', 'font.ttf'))
            except:
                st.warning("⚠️ ملف الخط (font.ttf) مفقود.")
            
            y = 800
            for i in range(start - 1, end):
                page = doc.load_page(i)
                text = page.get_text().strip()
                
                # منطق الـ OCR الذكي: إذا كان النص فارغاً أو أقل من 20 حرفاً
                if len(text) < 20:
                    pix = page.get_pixmap()
                    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                    text = pytesseract.image_to_string(img, lang='eng').strip()
                
                # تنظيف النص ودمجه
                clean_text = " ".join(text.split())
                
                if clean_text:
                    if y < 100:
                        c.showPage()
                        y = 800
                    
                    # طباعة الإنجليزي
                    c.setFont("Helvetica", 10)
                    c.drawString(50, y, clean_text[:120])
                    y -= 20
                    
                    # الترجمة
                    try:
                        result = translator.translate_text(clean_text, target_lang="AR")
                        proper_arabic = get_display(arabic_reshaper.reshape(result.text))
                        
                        c.setFont("Arabic", 10)
                        # استخدام drawRightString للمحاذاة اليمينية الصحيحة
                        c.drawRightString(550, y, proper_arabic)
                        y -= 35 # المسافة المحددة بين الفقرات
                    except:
                        continue
            
            c.save()
            pdf_buffer.seek(0)
            st.success("✅ سيد قط أتم المهمة!")
            # ... (كود زر التحميل) ...
