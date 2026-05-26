import streamlit as st
import fitz  # مكتبة PyMuPDF لقراءة الـ PDF
from deep_translator import GoogleTranslator

st.title("NovaTrans Pro - المترجم الذكي")

# 1. رفع ملف الـ PDF
uploaded_file = st.file_uploader("ارفع الملزمة (PDF) هنا:", type="pdf")

if uploaded_file:
    # 2. قراءة الملف
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    all_text = ""
    
    # استخراج النص من الصفحات
    for page in doc:
        all_text += page.get_text()
    
    st.success("تم رفع الملف بنجاح! جاري التحضير للترجمة...")
    
    # 3. زر الترجمة
    if st.button("ترجم الآن"):
        with st.spinner("جاري الترجمة، انتظر قليلاً..."):
            # تقسيم النص لترجمته (لأن المترجم له حد أقصى للحروف)
            lines = all_text.split('\n')
            final_output = ""
            
            for line in lines:
                if line.strip(): # إذا كان السطر يحتوي نصاً
                    translated = GoogleTranslator(source='en', target='ar').translate(line)
                    final_output += f"{line}\n{translated}\n\n"
            
            st.text_area("النتيجة (نصك الأصلي + الترجمة):", final_output, height=500)
            st.download_button("حفظ النص المترجم", final_output)
