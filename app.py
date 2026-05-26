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

# 1. إعداد المترجم
auth_key = os.environ.get("DEEPL_API_KEY")
translator = deepl.Translator(auth_key)

# 2. وظيفة معالجة النص العربي
def prepare_arabic_text(text):
    reshaped_text = arabic_reshaper.reshape(text)
    return get_display(reshaped_text)

st.title("NovaTrans Pro - المترجم الذكي")

uploaded_file = st.file_uploader("ارفع ملف PDF", type="pdf")

if uploaded_file:
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    
    if st.button("ترجمة وحفظ"):
        with st.spinner("جاري الترجمة والمعالجة..."):
            pdf_buffer = io.BytesIO()
            c = canvas.Canvas(pdf_buffer)
            
            # 3. التأكد من وجود الخط وتسجيله
            font_name = 'ArabicFont'
            font_path = 'font.ttf' # تأكد أن هذا هو اسم الملف في GitHub
            
            if os.path.exists(font_path):
                pdfmetrics.registerFont(TTFont(font_name, font_path))
            else:
                st.error("خطأ: لم يتم العثور على ملف 'font.ttf' في المستودع. تأكد من رفعه!")
                st.stop()

            y = 750
            for page in doc:
                text = page.get_text()
                lines = text.split('\n')
                
                for line in lines:
                    if line.strip():
                        # إضافة صفحة جديدة إذا وصلنا لنهاية الصفحة
                        if y < 50:
                            c.showPage()
                            y = 750
                        
                        # كتابة النص الإنجليزي الأصلي
                        c.setFont("Helvetica", 10)
                        c.drawString(50, y, line[:100])
                        y -= 20
                        
                        # ترجمة السطر
                        try:
                            result = translator.translate_text(line, target_lang="AR")
                            arabic_text = prepare_arabic_text(result.text)
                            
                            # كتابة النص العربي بالخط الصحيح
                            c.setFont(font_name, 12)
                            # نستخدم drawRightString لأن النص العربي يُكتب من اليمين
                            c.drawRightString(550, y, arabic_text)
                            y -= 40
                        except Exception as e:
                            continue
            
            c.save()
            pdf_buffer.seek(0)
            st.success("تمت الترجمة بنجاح!")
            st.download_button("تحميل الملف المترجم", pdf_buffer, "Translated_Final.pdf", "application/pdf")
