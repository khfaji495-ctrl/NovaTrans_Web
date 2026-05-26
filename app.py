import streamlit as st
import fitz
from deep_translator import GoogleTranslator
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from bidi.algorithm import get_display
import arabic_reshaper
import io

# إعدادات الصفحة
st.set_page_config(page_title="NovaTrans Neon", layout="wide")

# تنسيق النيون
st.markdown("""
    <style>
    .stApp { background-color: #060911; }
    h1 { color: #ff00ff; text-align: center; text-shadow: 0 0 10px #ff00ff; }
    </style>
""", unsafe_allow_html=True)

st.title("✨ NovaTrans Neon Pro")

uploaded_file = st.file_uploader("📂 ارفع ملف الـ PDF هنا", type="pdf")

if uploaded_file:
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    total_pages = len(doc)
    
    start = st.number_input("من صفحة:", 1, total_pages, 1)
    end = st.number_input("إلى صفحة:", 1, total_pages, start)

    if st.button("🚀 ترجم واحفظ PDF"):
        pdf_buffer = io.BytesIO()
        c = canvas.Canvas(pdf_buffer)
        
        # تسجيل الخط العربي (تأكد من وجود font.ttf في ملفاتك)
        try:
            pdfmetrics.registerFont(TTFont('Arabic', 'font.ttf'))
            c.setFont("Arabic", 12)
        except:
            st.error("خطأ: لم يتم العثور على ملف الخط font.ttf في المستودع!")
            st.stop()

        y = 800
        for i in range(start - 1, end):
            text = doc.load_page(i).get_text()
            lines = text.split('\n')
            
            for line in lines:
                if line.strip():
                    if y < 50: # صفحة جديدة إذا امتلأت
                        c.showPage()
                        c.setFont("Arabic", 12)
                        y = 800
                    
                    # ترجمة
                    translated = GoogleTranslator(source='en', target='ar').translate(line)
                    
                    # معالجة النص العربي ليظهر بشكل صحيح
                    reshaped_text = arabic_reshaper.reshape(translated)
                    bidi_text = get_display(reshaped_text)
                    
                    c.drawString(400, y, line) # إنجليزي
                    y -= 20
                    c.drawString(400, y, bidi_text) # عربي
                    y -= 40
        
        c.save()
        pdf_buffer.seek(0)
        st.download_button("📥 تحميل الملف المترجم PDF", pdf_buffer, "NovaTrans_Translated.pdf")
