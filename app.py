import streamlit as st
import fitz
from deep_translator import GoogleTranslator
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from bidi.algorithm import get_display
import arabic_reshaper
import io
import time  # تأكد من هذا الاستيراد

# الإعدادات
st.set_page_config(page_title="NovaTrans Pro", layout="wide")

st.title("✨ NovaTrans Pro")

def prepare_arabic_text(text):
    reshaped_text = arabic_reshaper.reshape(text)
    return get_display(reshaped_text)

uploaded_file = st.file_uploader("📂 ارفع ملف الـ PDF هنا", type="pdf")

if uploaded_file is not None:
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    total_pages = len(doc)
    start = st.number_input("من صفحة:", 1, total_pages, 1)
    end = st.number_input("إلى صفحة:", 1, total_pages, start)

    if st.button("🚀 ترجم واحفظ PDF"):
        with st.spinner("جاري المعالجة..."):
            pdf_buffer = io.BytesIO()
            c = canvas.Canvas(pdf_buffer)
            try:
                pdfmetrics.registerFont(TTFont('Arabic', 'font.ttf'))
            except:
                st.warning("تنبيه: ملف الخط غير موجود.")
            
            y = 800
            # حلقة الصفحات
            for i in range(start - 1, end):
                text = doc.load_page(i).get_text()
                lines = text.split('\n')
                
                # حلقة الأسطر (داخل زر الترجمة)
                for line in lines:
                    if line.strip():
                        if y < 100:
                            c.showPage()
                            y = 800
                        
                        time.sleep(0.5) # راحة للسيرفر
                        try:
                            translated = GoogleTranslator(source='en', target='ar').translate(line)
                            proper_arabic = prepare_arabic_text(translated)
                            
                            c.setFont("Helvetica", 12)
                            c.drawString(50, y, line[:60])
                            y -= 20
                            c.setFont("Arabic", 12)
                            c.drawString(50, y, proper_arabic)
                            y -= 40
                        except:
                            continue
            
          # ... بعد نهاية حلقات الترجمة ...
            
            c.save() # حفظ ملف الـ PDF
            
            # التأكد من أن المؤشر في بداية الـ buffer قبل القراءة
            pdf_buffer.seek(0)
            
            # إظهار زر التحميل بعد التأكد من سلامة العملية
            st.success("✅ تمت العملية بنجاح!")
            st.download_button(
                label="📥 تحميل الملف المترجم PDF",
                data=pdf_buffer,
                file_name="NovaTrans_Translated.pdf",
                mime="application/pdf"
            )
