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

st.title("NovaTrans Pro - معالجة النصوص والصور")

uploaded_file = st.file_uploader("📂 ارفع ملف PDF", type="pdf")

if uploaded_file and st.button("ترجمة مع الصور"):
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    pdf = FPDF()
    
    with st.spinner("جاري استخراج النصوص والصور..."):
        for page in doc:
            pdf.add_page()
            
            # 1. معالجة الصور
            image_list = page.get_images(full=True)
            for img_index, img in enumerate(image_list):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                
                # حفظ الصورة مؤقتاً لإضافتها للـ PDF
                img_path = f"temp_img_{img_index}.png"
                with open(img_path, "wb") as f:
                    f.write(image_bytes)
                
                # إضافة الصورة للـ PDF (في إحداثيات مشابهة)
                try:
                    pdf.image(img_path, x=10, y=10, w=100)
                except:
                    pass
                os.remove(img_path)
            
            # 2. معالجة النصوص وترجمتها
            pdf.add_font("ArabicFont", "", "font.ttf", uni=True)
            pdf.set_font("ArabicFont", size=12)
            
            text = page.get_text()
            for line in text.split('\n'):
                if line.strip():
                    try:
                        res = translator.translate_text(line, target_lang="AR").text
                        bidi_text = get_display(arabic_reshaper.reshape(res))
                        pdf.ln(10) # مسافة بين الأسطر
                        pdf.cell(0, 10, txt=bidi_text, ln=True, align='R')
                    except:
                        continue

    pdf_output = pdf.output(dest='S').encode('latin-1')
    st.success("✅ تمت المعالجة!")
    st.download_button("📥 تحميل الملف", pdf_output, "NovaTrans_With_Images.pdf", "application/pdf")
