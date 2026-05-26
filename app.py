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

uploaded_file = st.file_uploader("📂 ضع ملفك هنا", type="pdf")

if uploaded_file is not None:
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    total_pages = len(doc)
    start = st.number_input("من صفحة:", 1, total_pages, 1)
    end = st.number_input("إلى صفحة:", 1, total_pages, start)

    if st.button("ترجمه PDF"):
        with st.spinner("جاري المعالجة..."):
            # داخل حلقة الصفحات (for i in range(start - 1, end):)
for i in range(start - 1, end):
    # 1. افتح صفحة جديدة لكل صفحة
    page_buffer = io.BytesIO()
    c = canvas.Canvas(page_buffer)
    # ... (كود تسجيل الخط والرسم) ...
    
    # 2. احفظ الصفحة فوراً
    c.save()
    page_buffer.seek(0)
    
    # 3. اعرض زر تحميل خاص بهذه الصفحة
    st.download_button(
        label=f"📥 تحميل الصفحة {i + 1}",
        data=page_buffer,
        file_name=f"page_{i + 1}.pdf",
        mime="application/pdf"
    )
            pdf_buffer = io.BytesIO()
            c = canvas.Canvas(pdf_buffer)
            try:
                pdfmetrics.registerFont(TTFont('Arabic', 'font.ttf'))
            except:
                st.warning("تنبيه: ملف الخط غير موجود.")
            
            y = 800

            st.info("💡 تنبيه .  انتظر الترجمه تأخذ وقتاً بسيطاً لضمان الجوده.")
            
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
            st.success("✅ ااكتمل الملف!")
            st.download_button(
                label="📥  PDF تحميل الملف ",
                data=pdf_buffer,
                file_name="NovaTrans_Translated.pdf",
                mime="application/pdf"
            )
