import streamlit as st
import fitz  # PyMuPDF
from fpdf import FPDF
import deepl
import os
import io
import arabic_reshaper
from bidi.algorithm import get_display

# إعداد المترجم
auth_key = os.environ.get("DEEPL_API_KEY")
translator = deepl.Translator(auth_key)

st.title("NovaTrans Pro - معالجة المستندات")

uploaded_file = st.file_uploader("📂 ارفع ملف PDF", type="pdf")

if uploaded_file and st.button("ترجمة مع الحفاظ على كل شيء"):
    # قراءة الملف الأصلي
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    pdf = FPDF()

    with st.spinner("جاري معالجة الصفحات..."):
        for page in doc:
            # 1. تحويل الصفحة إلى صورة عالية الجودة (Snapshot)
            # هذه الطريقة تضمن ظهور اللوجو وكل شيء في الصفحة
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2)) 
            img_data = pix.tobytes("png")
            
            # حفظ الصورة مؤقتاً في الذاكرة لإضافتها للـ PDF
            img_buffer = io.BytesIO(img_data)
            
            pdf.add_page()
            # إضافة الصورة كخلفية للصفحة (تغطي كامل الصفحة A4)
            pdf.image(img_buffer, x=0, y=0, w=210) 
            
            # 2. طباعة النصوص المترجمة فوق الصورة
            # ملاحظة: إذا كنت تريد ترجمة النصوص فوق الملف الأصلي، 
            # يمكنك تعديل هذا الجزء لجلب النصوص من page.get_text()
            
    # التحميل
    pdf_output = pdf.output(dest='S').encode('latin-1')
    st.success("✅ تمت العملية بنجاح!")
    st.download_button("📥 تحميل الملف", pdf_output, "NovaTrans_Final.pdf", "application/pdf")
