import streamlit as st
import fitz  # PyMuPDF
import deepl
import io
from bidi.algorithm import get_display
import arabic_reshaper

# 1. إعدادات المترجم
try:
    auth_key = st.secrets["DEEPL_API_KEY"]
    translator = deepl.Translator(auth_key)
except:
    st.error("⚠️ خطأ: تأكد من إضافة مفتاح API في إعدادات Secrets")
    st.stop()

def prepare_arabic_text(text):
    # نستخدم arabic_reshaper لجعل الخطوط العربية تظهر متصلة وواضحة
    reshaped_text = arabic_reshaper.reshape(text)
    return get_display(reshaped_text)

# 2. واجهة الرفع
uploaded_file = st.file_uploader("😸 ارسل ملف الملزمة للسيد قط", type="pdf")

if uploaded_file is not None:
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    
    if st.button("😸 ابدأ الترجمة مع سيد قط"):
        output_pdf = fitz.open()
        progress_bar = st.progress(0)
        
        with st.spinner("🐈 سيد قط يترجم الملزمة.."):
            for i in range(len(doc)):
                page = doc.load_page(i)
                # إنشاء صفحة جديدة بنفس أبعاد الأصلية
                new_page = output_pdf.new_page(width=page.rect.width, height=page.rect.height)
                
                # وضع صورة الصفحة الأصلية كخلفية (للحفاظ على الصور والتصاميم)
                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
                new_page.insert_image(page.rect, pixmap=pix)
                
                # استخراج النصوص وإضافة الترجمة فقط فوقها
                blocks = page.get_text("blocks")
                for block in blocks:
                    if block[6] == 0:  # نص
                        text = block[4].strip()
                        if len(text) > 3:
                            x, y = block[0], block[1]
                            
                            try:
                                # ترجمة النص
                                translated = translator.translate_text(text, target_lang="AR")
                                # إدراج الترجمة العربية (لون أسود، خط واضح)
                                # سنضعها في نفس إحداثيات النص الإنجليزي لتغطيه أو فوقه
                                new_page.insert_text((x, y + 10), prepare_arabic_text(translated.text), 
                                                     fontsize=12, color=(0, 0, 0))
                            except:
                                continue
                
                progress_bar.progress((i + 1) / len(doc))
            
            # حفظ الملف
            output_buffer = io.BytesIO()
            output_pdf.save(output_buffer)
            output_buffer.seek(0)
            
            st.success("😼 تم بنجاح!")
            st.download_button("😸 تحميل الملزمة المترجمة", data=output_buffer, 
                               file_name="Translated_SayedQatt.pdf", mime="application/pdf")
