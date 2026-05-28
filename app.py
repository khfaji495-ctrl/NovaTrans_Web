import streamlit as st
import fitz  # PyMuPDF
import deepl
import io
from bidi.algorithm import get_display
import arabic_reshaper

# 1. إعدادات المترجم
translator = deepl.Translator(st.secrets["DEEPL_API_KEY"])

def prepare_arabic_text(text):
    return get_display(arabic_reshaper.reshape(text))

# 2. الواجهة
uploaded_file = st.file_uploader("😸 ارسل ملف الملزمة للسيد قط", type="pdf")

if uploaded_file is not None:
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    
    if st.button("😸 ابدأ الترجمة مع سيد قط"):
        output_pdf = fitz.open()
        
        with st.spinner("🐈 سيد قط يضيف الترجمة العربية.."):
            for i in range(len(doc)):
                page = doc.load_page(i)
                # إنشاء صفحة جديدة بنفس أبعاد الأصلية
                new_page = output_pdf.new_page(width=page.rect.width, height=page.rect.height)
                
                # وضع صورة الصفحة الأصلية كخلفية (لضمان بقاء كل شيء كما هو)
                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
                new_page.insert_image(page.rect, pixmap=pix)
                
                # معالجة النصوص
                blocks = page.get_text("blocks")
                for block in blocks:
                    if block[6] == 0:  # نص
                        text = block[4].strip()
                        if len(text) > 3:
                            x0, y0 = block[0], block[1]
                            
                            # إضافة الترجمة العربية فوق النص الأصلي بمسافة 15 نقطة
                            # (لا نلمس النص الإنجليزي الموجود في صورة الخلفية)
                            try:
                                translated = translator.translate_text(text, target_lang="AR")
                                new_page.insert_text((x0, y0 - 5), # Y0-5 تجعل الترجمة فوق النص
                                                     prepare_arabic_text(translated.text), 
                                                     fontsize=10, color=(0, 0, 0))
                            except:
                                continue
            
            # حفظ الملف
            output_buffer = io.BytesIO()
            output_pdf.save(output_buffer)
            output_buffer.seek(0)
            
            st.success("😼 تم بنجاح! الترجمة فوق النص الأصلي.")
            st.download_button("تحميل الملزمة", data=output_buffer, file_name="Translated.pdf", mime="application/pdf")
