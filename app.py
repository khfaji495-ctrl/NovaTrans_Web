import streamlit as st
import os
import fitz
import deepl
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import arabic_reshaper
from bidi.algorithm import get_display
import io

# إعداد المترجم
auth_key = os.environ.get("DEEPL_API_KEY")
translator = deepl.Translator(auth_key)

def prepare_arabic_text(text):
    # إعادة تشكيل الحروف العربية وربطها
    reshaped_text = arabic_reshaper.reshape(text)
    return get_display(reshaped_text)

st.title("NovaTrans Pro - المترجم الذكي")

uploaded_file = st.file_uploader("ارفع ملف PDF", type="pdf")

if uploaded_file:
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    
    if st.button("ترجمة وحفظ"):
        pdf_buffer = io.BytesIO()
        c = canvas.Canvas(pdf_buffer)
        
        # تسجيل الخط العربي (تأكد من وجود font.ttf في مشروعك على GitHub)
        try:
            pdfmetrics.registerFont(TTFont('ArabicFont', 'font.ttf'))
        except:
            st.error("لم يتم العثور على ملف الخط 'font.ttf'.")
            st.stop()

        y = 750
        for page in doc:
            text = page.get_text()
            lines = text.split('\n')
            
            for line in lines:
                if line.strip():
                    if y < 50:
                        c.showPage()
                        y = 750
                    
                    # 1. كتابة النص الإنجليزي الأصلي
                    c.setFont("Helvetica", 10)
                    c.drawString(50, y, line[:100])
                    y -= 20
                    
                    # 2. الترجمة
                    result = translator.translate_text(line, target_lang="AR")
                    arabic_text = prepare_arabic_text(result.text)
                    
                    # 3. كتابة النص العربي
                    c.setFont("ArabicFont", 10)
                    c.drawRightString(550, y, arabic_text)
                    y -= 30
        
        c.save()
        st.success("تمت الترجمة بنجاح!")
        st.download_button("تحميل الملف المترجم", pdf_buffer.getvalue(), "Translated.pdf", "application/pdf")
