import streamlit as st
import fitz
import io
from deep_translator import GoogleTranslator
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from bidi.algorithm import get_display
import arabic_reshaper

# --- إعدادات الواجهة (ألوان مريحة للعين) ---
st.set_page_config(page_title="NovaTrans Pro", layout="wide")
st.markdown("""
    <style>
    /* خلفية رمادية غامقة مريحة */
    .stApp { background-color: #1e1e2e; color: #dcd7ba; }
    
    /* عنوان بلون تركوازي هادئ وجميل */
    h1 { 
        color: #7aa89f; 
        text-align: center; 
        font-family: sans-serif;
    }
    
    /* تنسيق زر التحميل */
    div.stButton > button {
        background-color: #7aa89f;
        color: #1e1e2e;
        font-weight: bold;
        border: none;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("✨ NovaTrans Pro")

# --- دالة تحضير النص العربي ---
def prepare_arabic_text(text):
    reshaped_text = arabic_reshaper.reshape(text)
    return get_display(reshaped_text)

# --- واجهة المستخدم ---
uploaded_file = st.file_uploader("📂 ارفع ملف الـ PDF هنا", type="pdf")

if uploaded_file:
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    total_pages = len(doc)
    
    col1, col2 = st.columns(2)
    start = col1.number_input("من صفحة:", 1, total_pages, 1)
    end = col2.number_input("إلى صفحة:", 1, total_pages, start)

    if st.button("🚀 ترجم واحفظ PDF"):
        with st.spinner("جاري المعالجة..."):
            pdf_buffer = io.BytesIO()
            c = canvas.Canvas(pdf_buffer)
            
            # تسجيل الخط
            try:
                pdfmetrics.registerFont(TTFont('Arabic', 'font.ttf'))
            except:
                st.error("خطأ: تأكد من رفع ملف 'font.ttf' في المجلد!")
                st.stop()
            
            y = 800
            for i in range(start - 1, end):
                text = doc.load_page(i).get_text()
                lines = text.split('\n')
                
                for line in lines:
                    if line.strip():
                        if y < 100:
                            c.showPage()
                            y = 800
                        
                        # الترجمة
                        translated = GoogleTranslator(source='auto', target='ar').translate(line[:500])
                        proper_arabic = prepare_arabic_text(translated)
                        
                        # طباعة النص الإنجليزي
                        c.setFont("Helvetica", 12)
                        c.drawString(50, y, line[:80])
                        y -= 25
                        
                        # طباعة النص العربي
                        c.setFont("Arabic", 12)
                        c.drawString(50, y, proper_arabic)
                        y -= 45
            
            c.save()
            pdf_buffer.seek(0)
            st.success("✅ تم الانتهاء بنجاح!")
            st.download_button("📥 تحميل الملف المترجم PDF", pdf_buffer, "NovaTrans_Translated.pdf")
