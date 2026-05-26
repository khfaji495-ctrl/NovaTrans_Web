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

st.title("NovaTrans Pro - معالجة النصوص والصور")

uploaded_file = st.file_uploader("📂 ارفع ملف PDF", type="pdf")

if uploaded_file and st.button("ترجمة مع الصور"):
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    pdf = FPDF()
    
    with st.spinner("جاري المعالجة... قد يستغرق الأمر بعض الوقت"):
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            pdf.add_page()
            
            # --- 1. استخراج وإضافة الصور ---
            image_list = page.get_images(full=True)
            for img in image_list:
                xref = img[0]
                pix = fitz.Pixmap(doc, xref)
                # حفظ الصورة مؤقتاً
                img_path = f"temp_{xref}.png"
                pix.save(img_path)
                
                # إضافة الصورة للـ PDF (استخدام الإحداثيات الأساسية)
                pdf.image(img_path, x=10, y=10, w=100)
                os.remove(img_path)
            
            # --- 2. معالجة النصوص وترجمتها ---
            pdf.add_font("ArabicFont", "", "font.ttf", uni=True)
            pdf.set_font("ArabicFont", size=12)
            
            text = page.get_text()
            for line in text.split('\n'):
                if line.strip():
                    try:
                        # كتابة النص الإنجليزي (للرجوع إليه)
                        pdf.set_font("Helvetica", size=10)
                        pdf.cell(0, 10, txt=line, ln=True, align='L')
                        
                        # ترجمة وكتابة العربي
                        res = translator.translate_text(line, target_lang="AR").text
                        bidi_text = get_display(arabic_reshaper.reshape(res))
                        
                        pdf.set_font("ArabicFont", size=12)
                        pdf.cell(0, 10, txt=bidi_text, ln=True, align='R')
                        pdf.ln(5) # مسافة
                    except:
                        continue

    pdf_output = pdf.output(dest='S').encode('latin-1')
    st.success("✅ تمت المعالجة!")
    st.download_button("📥 تحميل الملف", pdf_output, "NovaTrans_Translated_Images.pdf", "application/pdf")
