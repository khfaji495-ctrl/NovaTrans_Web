import streamlit as st
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
import io
import deepl
import os

# --- إعداد المترجم ---
auth_key = os.environ.get("DEEPL_API_KEY")
translator = deepl.Translator(auth_key)

st.title("NovaTrans Pro - المترجم الذكي")

uploaded_file = st.file_uploader("📂 ارفع ملف الملزمة", type="pdf")

if uploaded_file and st.button("ترجمة الملازم"):
    reader = PdfReader(uploaded_file)
    writer = PdfWriter()
    
    with st.spinner("جاري معالجة الصفحات..."):
        for i, page in enumerate(reader.pages):
            # إنشاء طبقة نصية مؤقتة للترجمة
            packet = io.BytesIO()
            can = canvas.Canvas(packet)
            
            # استخراج النص وترجمته
            text = page.extract_text()
            if text:
                res = translator.translate_text(text[:500], target_lang="AR").text
                can.setFont("Helvetica", 10)
                can.drawString(50, 750, "الترجمة العربية:")
                can.setFont("Helvetica", 10) # لاحظ: ستحتاج لخط عربي هنا لاحقاً
                can.drawString(50, 730, res[:100])
            
            can.save()
            packet.seek(0)
            
            # دمج الطبقة مع الصفحة الأصلية (اللوغو سيبقى كما هو)
            new_pdf = PdfReader(packet)
            page.merge_page(new_pdf.pages[0])
            writer.add_page(page)

    # التحميل
    result_pdf = io.BytesIO()
    writer.write(result_pdf)
    st.success("✅ تمت العملية بنجاح!")
    st.download_button("📥 تحميل الملف المترجم", result_pdf.getvalue(), "NovaTrans_Final.pdf")
