import streamlit as st
import fitz
from deep_translator import GoogleTranslator
from reportlab.pdfgen import canvas
import io

st.title("✨ NovaTrans Pro - PDF Generator")

uploaded_file = st.file_uploader("ارفع ملزمة الـ PDF:", type="pdf")

if uploaded_file:
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    page_num = st.number_input("اختر الصفحة للترجمة:", min_value=1, max_value=len(doc), value=1)
    
    if st.button("ترجمة وحفظ PDF"):
        with st.spinner("جاري المعالجة..."):
            page = doc.load_page(page_num - 1)
            text = page.get_text()
            lines = text.split('\n')
            
            # إعداد ملف الـ PDF الجديد
            pdf_buffer = io.BytesIO()
            c = canvas.Canvas(pdf_buffer)
            y = 800  # مكان الكتابة في الصفحة
            
            for line in lines:
                if line.strip():
                    translated = GoogleTranslator(source='en', target='ar').translate(line)
                    # كتابة النص الأصلي والترجمة
                    c.setFont("Helvetica", 12)
                    c.drawString(50, y, line)
                    y -= 20
                    c.setFont("Helvetica", 10)
                    c.drawString(50, y, translated) # ملاحظة: قد تحتاج لخط يدعم العربية
                    y -= 40
            
            c.save()
            pdf_buffer.seek(0)
            
            st.success("تم تجهيز الملف!")
            st.download_button("تحميل الملف المترجم PDF", pdf_buffer, "translated.pdf", "application/pdf")
