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
st.set_page_config(page_title="NovaTrans", layout="wide")

st.title("مترجم الملازم الذكي")

# رفع الملف
uploaded_file = st.file_uploader("ارفع ملزمتك هنا (PDF):", type="pdf")

if uploaded_file is not None:
    # فتح ملف الـ PDF
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    
    # اختيار الصفحات
    start_page = st.number_input("من صفحة:", 1, len(doc), 1)
    end_page = st.number_input("إلى صفحة:", 1, len(doc), start_page)

    if st.button("ابدأ الترجمة"):
        with st.spinner("جاري ترجمة الملازم، لحظات.."):
            pdf_buffer = io.BytesIO()
            c = canvas.Canvas(pdf_buffer)
            
            # تسجيل الخط (تأكد أن ملف font.ttf موجود في المجلد)
            try:
                pdfmetrics.registerFont(TTFont('Arabic', 'font.ttf'))
            except:
                st.error("خطأ: ملف الخط font.ttf مفقود في المجلد!")
            
            y_position = 800
            
            # المعالجة
            for i in range(start_page - 1, end_page):
                page = doc.load_page(i)
                text = page.get_text()
                lines = text.split('\n') # هنا عرفنا المتغير lines داخل الدالة
                
                for line in lines:
                    if line.strip():
                        # ترجمة
                        translated = GoogleTranslator(source='en', target='ar').translate(line)
                        
                        # تنسيق العربي
                        reshaped = arabic_reshaper.reshape(translated)
                        bidi_text = get_display(reshaped)
                        
                        # الرسم على الـ PDF
                        c.setFont("Helvetica", 10)
                        c.drawString(50, y_position, line[:60]) # النص الإنجليزي
                        y_position -= 20
                        c.setFont("Arabic", 10)
                        c.drawString(50, y_position, bidi_text) # النص العربي
                        y_position -= 40
                        
                        if y_position < 50:
                            c.showPage()
                            y_position = 800
            
            c.save()
            st.success("تمت الترجمة!")
            st.download_button("تحميل الملزمة المترجمة", pdf_buffer.getvalue(), "translated.pdf")
