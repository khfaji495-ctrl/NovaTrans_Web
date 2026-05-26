import streamlit as st
import fitz
from deep_translator import GoogleTranslator
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from bidi.algorithm import get_display
import arabic_reshaper
import io

# --- الإعدادات والواجهة (Neon Style) ---
st.set_page_config(page_title="NovaTrans Pro", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #060911; color: white; }
    h1 { color: #ff00ff; text-align: center; text-shadow: 0 0 10px #ff00ff; }
    </style>
""", unsafe_allow_html=True)

st.title("✨ NovaTrans Pro")

# --- دوال المعالجة ---
def prepare_arabic_text(text):
    reshaped_text = arabic_reshaper.reshape(text)
    return get_display(reshaped_text)

# --- واجهة المستخدم ---
uploaded_file = st.file_uploader("📂 ارفع ملف الـ PDF هنا", type="pdf")

if uploaded_file:
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    total_pages = len(doc)
    
    start = st.number_input("من صفحة:", 1, total_pages, 1)
    end = st.number_input("إلى صفحة:", 1, total_pages, start)

    if st.button("🚀 ترجم واحفظ PDF"):
        with st.spinner("جاري المعالجة..."):
            pdf_buffer = io.BytesIO()
            c = canvas.Canvas(pdf_buffer)
            
            # تسجيل الخط (تأكد من وجود font.ttf في المستودع)
            pdfmetrics.registerFont(TTFont('Arabic', 'font.ttf'))
            
            y = 800
            for i in range(start - 1, end):
                text = doc.load_page(i).get_text()
                lines = text.split('\n')
                
                for line in lines:
                    if line.strip():
                        if y < 100:
                            c.showPage()
                            y = 800
                        
                        # ترجمة
                        translated = GoogleTranslator(source='en', target='ar').translate(line)
                        proper_arabic = prepare_arabic_text(translated)
                        
                        # طباعة النص
                        c.setFont("Helvetica", 12)
                        c.drawString(50, y, line)
                        y -= 20
                        c.setFont("Arabic", 12)
                        c.drawString(50, y, proper_arabic)
                        y -= 40
            
            c.save()
            pdf_buffer.seek(0)
            st.success("✅ تم الانتهاء!")
            st.download_button("📥 تحميل الملف المترجم PDF", pdf_buffer, "NovaTrans_Translated.pdf")
