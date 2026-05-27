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
from pdf2image import convert_from_bytes

# (استخدم نفس إعداداتك السابقة للـ CSS والـ UI)

def extract_text_from_page(doc, page_num):
    page = doc.load_page(page_num)
    text = page.get_text()
    # إذا كان النص أقل من 50 حرفاً، نفترض أنها صورة ونستخدم OCR
    if len(text.strip()) < 50:
        pix = page.get_pixmap()
        img_data = pix.tobytes("png")
        text = pytesseract.image_to_string(img_data, lang='eng')
    return text

# في جزء زر الترجمة:
if st.button("😸 ابدأ الترجمة مع سيد قط"):
    with st.spinner(".... 🐈سيد قط يترجم الملزمة الآن.. يرجى الانتظار"):
        pdf_buffer = io.BytesIO()
        c = canvas.Canvas(pdf_buffer)
        
        try:
            pdfmetrics.registerFont(TTFont('Arabic', 'font.ttf'))
        except:
            st.warning("⚠️ تنبيه: ملف الخط (font.ttf) غير موجود.")
        
        y = 800 
        for i in range(start - 1, end):
            # استخدام الدالة الذكية التي تستخرج النص أو تقرأ الصورة
            full_text = extract_text_from_page(doc, i)
            # دمج الفقرات لتجنب المسافات العشوائية
            clean_text = " ".join(full_text.split())
            
            if clean_text:
                if y < 100:
                    c.showPage()
                    y = 800
                
                # ترجمة الفقرة كاملة
                result = translator.translate_text(clean_text, target_lang="AR")
                proper_arabic = get_display(arabic_reshaper.reshape(result.text))
                
                # طباعة الإنجليزي ثم العربي
                c.setFont("Helvetica", 12)
                c.drawString(50, y, "Original Text:")
                y -= 20
                c.setFont("Helvetica", 10)
                # استخدام split-text-by-width لضمان عدم خروج النص عن الصفحة
                from reportlab.lib.utils import simpleSplit
                lines = simpleSplit(clean_text, "Helvetica", 10, 500)
                for line in lines:
                    c.drawString(50, y, line)
                    y -= 15
                
                y -= 10
                c.setFont("Arabic", 12)
                # رسم النص العربي بوضوح
                c.rightDrawString(550, y, proper_arabic)
                y -= 40 # المسافة الثابتة بين كل فقرة وأخرى
        
        c.save()
        pdf_buffer.seek(0)
        st.success("😼سيد قط أتم المهمة بنجاح!")
        # (زر التحميل كما هو)
