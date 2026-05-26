import streamlit as st
import fitz  # PyMuPDF
from fpdf import FPDF
import deepl
import os
import arabic_reshaper
from bidi.algorithm import get_display

# إعداد المترجم
auth_key = os.environ.get("DEEPL_API_KEY")
translator = deepl.Translator(auth_key)

st.title("NovaTrans Pro - معالجة متقدمة")

uploaded_file = st.file_uploader("📂 ارفع ملف PDF", type="pdf")

if uploaded_file and st.button("ترجمة مع الحفاظ على التنسيق"):
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    pdf = FPDF()
    
    with st.spinner("جاري معالجة الصفحة كصورة..."):
        for page in doc:
            pdf.add_page()
            
            # 1. تحويل الصفحة لصور (Snapshot)
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2)) # دقة عالية
            img_path = f"page_{page.number}.png"
            pix.save(img_path)
            
            # 2. وضع الصورة كخلفية
            pdf.image(img_path, x=0, y=0, w=210) # A4 width
            os.remove(img_path)
            
            # 3. طباعة النص المترجم فوق الصورة
            pdf.add_font("ArabicFont", "", "font.ttf", uni=True)
            text = page.get_text()
            
            y_pos = 20 # بداية الكتابة من أعلى الصفحة
            for line in text.split('\n'):
                if line.strip():
                    try:
                        res = translator.translate_text(line, target_lang="AR").text
                        bidi_text = get_display(arabic_reshaper.reshape(res))
                        
                        pdf.set_font("ArabicFont", size=12)
                        pdf.set_xy(10, y_pos) # ضبط مكان النص
                        pdf.cell(190, 10, txt=bidi_text, ln=True, align='R')
                        y_pos += 15 # المسافة بين الأسطر
                    except:
                        continue

    pdf_output = pdf.output(dest='S').encode('latin-1')
    st.success("✅ تمت العملية!")
    st.download_button("📥 تحميل الملف النهائي", pdf_output, "Translated_Doc.pdf", "application/pdf")
